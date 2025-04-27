# src/tools/pdf_vector_search_tool.py

from typing import Any, Union, List
from pydantic import PrivateAttr
# ← use LangChain’s BaseTool instead of crewai_tools.BaseTool
from crewai.tools import BaseTool
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.utils.pdf_processor import PDFProcessor
import os
import hashlib
import pickle

INDEX_FOLDER = "./faiss_index"
PDF_HASH_FILE = os.path.join(INDEX_FOLDER, "pdf_hash.pkl")


class PDFVectorSearchTool(BaseTool):
    name: str = "Harry Potter PDF Vector Search Tool"
    description: str = (
        "Finds the most semantically relevant passages from the Harry Potter PDF."
    )

    # these are NOT Pydantic fields—we store them privately
    _emb: Any = PrivateAttr()
    _vs: Any = PrivateAttr()
    _processor: PDFProcessor = PrivateAttr()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # initialize our PDFProcessor (make sure it points at the right file)
        self._processor = PDFProcessor()  
        
        # verify PDF exists
        if not os.path.exists(self._processor.pdf_path):
            raise FileNotFoundError(
                f"PDF not found at {self._processor.pdf_path}. "
                "Please correct PDF_PATH in config."
            )

        # embedding model
        self._emb = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

        # load or rebuild index
        if self._index_is_valid():
            print("✅ Loading existing FAISS index...")
            self._vs = FAISS.load_local(INDEX_FOLDER, self._emb, allow_dangerous_deserialization=True)
        else:
            print("🔄 Building new FAISS index...")
            self._vs = self._build_index()

    def _index_is_valid(self) -> bool:
        if not os.path.exists(INDEX_FOLDER) or not os.path.exists(PDF_HASH_FILE):
            return False
        current = self._compute_pdf_hash()
        try:
            with open(PDF_HASH_FILE, "rb") as f:
                saved = pickle.load(f)
            return saved == current
        except Exception:
            return False

    def _compute_pdf_hash(self) -> str:
        h = hashlib.md5()
        with open(self._processor.pdf_path, "rb") as f:
            h.update(f.read())
        return h.hexdigest()

    def _build_index(self) -> FAISS:
        # extract -> clean -> chunk
        docs = self._processor.process()
        if not docs:
            raise RuntimeError("No documents extracted from PDF—check text extraction!")
        
        splitter = RecursiveCharacterTextSplitter(chunk_size=512, chunk_overlap=100)
        chunks = splitter.split_documents(docs)
        if not chunks:
            raise RuntimeError("No chunks created—your splitter settings may be too strict.")

        # build FAISS
        vs = FAISS.from_documents(chunks, embedding=self._emb)
        os.makedirs(INDEX_FOLDER, exist_ok=True)
        vs.save_local(INDEX_FOLDER)

        # save hash
        pdf_hash = self._compute_pdf_hash()
        with open(PDF_HASH_FILE, "wb") as f:
            pickle.dump(pdf_hash, f)

        return vs

    def _run(self, query: Union[str, dict]) -> str:
        if isinstance(query, dict):
            # unbox if CrewAI passed a dict
            query = query.get("question") or query.get("query") or str(query)

        results = self._vs.similarity_search(query, k=5)
        if not results:
            return "No relevant passages found."
        return "\n---\n".join(doc.page_content for doc in results)

    async def _arun(self, query: Union[str, dict]) -> str:
        return self._run(query)
   
# tool = PDFVectorSearchTool()
# answer = tool.run("How does Harry first meet Hagrid?")
# print(answer)