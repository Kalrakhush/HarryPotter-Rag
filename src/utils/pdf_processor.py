import os
import pdfplumber
import re
from typing import List, Dict, Any
from langchain_core.documents import Document
from src.config import PDF_PATH, CHUNK_SIZE, CHUNK_OVERLAP

class PDFProcessor:
    def __init__(self, pdf_path: str = None):
        # allow override, else use config
        self.pdf_path = pdf_path or PDF_PATH
        if not os.path.exists(self.pdf_path):
            raise FileNotFoundError(f"PDF not found at {self.pdf_path}")

    def extract_text(self) -> str:
        """Extract raw text from the PDF; raise if empty."""
        full_text = []
        with pdfplumber.open(self.pdf_path) as pdf:
            for i, page in enumerate(pdf.pages, start=1):
                text = page.extract_text()
                if text:
                    full_text.append(text)

        combined = "\n".join(full_text)
        if not combined.strip():
            raise RuntimeError(f"No text extracted from PDF: {self.pdf_path}")
        return combined

    def clean_text(self, text: str) -> str:
        """Strip page numbers, headers/footers, and collapse whitespace."""
        # strip page numbers like "\n   23\n"
        text = re.sub(r"\n\s*\d+\s*\n", "\n", text)

        # remove common headers/footers (parameterize if you have multiple editions)
        editions = [
            r"HARRY POTTER AND THE SORCERER['’]S STONE",
            r"J\.K\. ROWLING"
        ]
        for hdr in editions:
            text = re.sub(hdr + r"\s*\n", "", text, flags=re.IGNORECASE)

        # collapse 3+ newlines into two
        text = re.sub(r"\n{3,}", "\n\n", text)
        return text.strip()

    def extract_chapters(self, text: str) -> List[Dict[str, Any]]:
        """
        Locate chapter headings and split out their text.
        Supports both roman (I, II, III) and Arabic numerals.
        """
        pattern = re.compile(
            r"^(CHAPTER|Chapter)\s+([IVX]+|\d+)\s*[:-]?\s*(.*)$",
            re.MULTILINE
        )
        matches = list(pattern.finditer(text))
        if not matches:
            # fallback: treat entire text as one “chapter”
            return [{"chapter_num": "1", "title": "", "content": text}]

        chapters = []
        for idx, m in enumerate(matches):
            start = m.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            chapters.append({
                "chapter_num": m.group(2),
                "title": m.group(3).strip(),
                "content": text[start:end].strip()
            })
        return chapters

    def split_into_chunks(self, chapters: List[Dict[str, Any]]) -> List[Document]:
        """Break each chapter into overlapping chunks of ~CHUNK_SIZE."""
        docs: List[Document] = []
        for chap in chapters:
            paras = re.split(r"\n\s*\n", chap["content"])
            buffer = ""
            meta_paras: List[str] = []
            for p in paras:
                p = p.strip()
                if not p:
                    continue
                # if adding this paragraph will overflow
                if len(buffer) + len(p) > CHUNK_SIZE:
                    docs.append(Document(
                        page_content=buffer.strip(),
                        metadata={
                            "source": os.path.basename(self.pdf_path),
                            "chapter": chap["chapter_num"],
                            "title": chap["title"],
                            "paragraphs": meta_paras.copy()
                        }
                    ))
                    # prepare next buffer with overlap
                    overlap = buffer[-CHUNK_OVERLAP:] if CHUNK_OVERLAP < len(buffer) else buffer
                    buffer = overlap + "\n\n" + p + "\n\n"
                    # keep only paras still in buffer
                    meta_paras = [pp for pp in meta_paras if pp in buffer] + [p]
                else:
                    buffer += p + "\n\n"
                    meta_paras.append(p)

            # final leftover
            if buffer.strip():
                docs.append(Document(
                    page_content=buffer.strip(),
                    metadata={
                        "source": os.path.basename(self.pdf_path),
                        "chapter": chap["chapter_num"],
                        "title": chap["title"],
                        "paragraphs": meta_paras.copy()
                    }
                ))

        return docs

    def process(self) -> List[Document]:
        """Full pipeline: extract → clean → chapter-split → chunk."""
        raw = self.extract_text()
        cleaned = self.clean_text(raw)
        chapters = self.extract_chapters(cleaned)
        docs = self.split_into_chunks(chapters)
        if not docs:
            raise RuntimeError("No chunks produced; check CHUNK_SIZE/OVERLAP settings.")
        return docs
