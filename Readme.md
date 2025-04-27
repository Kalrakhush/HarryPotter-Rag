# Hogwarts Knowledge Vault

A magical question-answering system powered by CrewAI and Retrieval-Augmented Generation.


## 🧙‍♂️ Overview

Hogwarts Knowledge Vault is an interactive application that allows users to ask questions about the Harry Potter universe and receive answers in the style of various characters from the series. The system uses advanced AI techniques including:

- **Retrieval-Augmented Generation (RAG)** to find relevant information from the Harry Potter books
- **Character-specific response generation** to mimic the speaking style of different wizarding world characters
- **CrewAI orchestration** to manage a team of specialized AI agents working together

## ✨ Features

- Ask questions about anything in the Harry Potter universe
- Choose from 10 different characters to answer your questions:
  - Harry Potter
  - Hermione Granger
  - Ron Weasley
  - Albus Dumbledore
  - Severus Snape
  - Draco Malfoy
  - Luna Lovegood
  - Rubeus Hagrid
  - Minerva McGonagall
  - Sirius Black
- Beautiful wizarding-themed UI with responsive design
- Real-time response generation with progress indicators

## 🛠️ Technical Architecture

The application uses a multi-agent architecture with CrewAI:

1. **Retrieval Agent**: Searches through Harry Potter text using semantic search to find relevant context
2. **Character Analysis Agent**: Analyzes character speech patterns and personality traits
3. **Response Generation Agent**: Creates final responses in the style of the selected character

## 📋 Requirements

- Python 3.8+
- Streamlit
- CrewAI
- LangChain (for PDF processing)
- Other dependencies listed in `requirements.txt`

## 🚀 Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/Kalrakhush/HarryPotter-Rag.git
   cd HarryPotter-Rag
   ```

2. Create and activate a virtual environment:
   ```bash
   bashpython -m venv venv
   source venv/bin/activate
   ```  

3. Install required packages:
   ```bash
   pip install -r requirements.txt
   ```

  ## Set up environment variables:

   Create a .env file in the project root
   Add your API keys:
   OPENAI_API_KEY=your_openai_api_key
   # Add any other required API keys



## Download the Harry Potter data:

Place the PDF file containing Harry Potter text in the data directory
Default path: data/harry_potter.pdf



## 🧪 Usage

Start the Streamlit application:
```bash
streamlit run app.py
```

Open your browser and navigate to http://localhost:8501
Select a character from the dropdown menu
Type your question about the Harry Potter universe in the input field
Click "🪄 Ask" and wait for the magical response!

## 📁 Project Structure
HarryPotter-Rag/
├── app.py                        # Main Streamlit application
├── README.md                     # This file
├── requirements.txt              # Python dependencies
├── .env                          # Environment variables (create this)
├── .gitignore                    # Git ignore file
├── data/
│   ├── harry_potter.pdf          # PDF containing Harry Potter text
│   └── faiss_index/              # Vector store indices
└── src/
    ├── __init__.py               # Package initialization
    ├── agents/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   ├── config/               # Configuration files
    │   ├── harry_potter_crew.py  # CrewAI implementation
    │   └── faiss_index/          # Agent-specific indices
    ├── utils/
    │   ├── __init__.py
    │   ├── __pycache__/
    │   ├── config.py             # Configuration utilities
    │   ├── llm_service.py        # LLM service wrapper
    │   ├── pdf_processor.py      # PDF processing utilities
    │   └── tools.py              # Custom tools including PDFVectorSearchTool
    └── test/                     # Test files

## ⚙️ Configuration
The behavior of agents and tasks can be customized by modifying the YAML configuration files:

src/agents/config/agents.yaml: Define agent personalities, capabilities, and goals
src/agents/config/tasks.yaml: Define tasks for each agent to perform

🧠 How It Works

When a user submits a question:

The Retrieval Agent searches the Harry Potter corpus for relevant context
The Character Analysis Agent determines how the chosen character would respond
The Response Generation Agent creates the final answer in character


The entire process is orchestrated by CrewAI, which manages the sequential workflow

## 🤝 Contributing
Contributions are welcome! Please feel free to submit a Pull Request to the GitHub repository.
📄 License
This project is licensed under the MIT License - see the LICENSE file for details.

## 🔮 Acknowledgments

J.K. Rowling for creating the magical world of Harry Potter
The CrewAI team for the multi-agent framework
All contributors to this project