# Harry Potter Character RAG Agent

A Retrieval-Augmented Generation (RAG) AI system that answers questions in the voice of Harry Potter characters using CrewAI.

## Overview

This project implements a RAG pipeline that:
1. Processes the Harry Potter and the Sorcerer's Stone PDF
2. Extracts and indexes text for retrieval
3. Analyzes character traits and speech patterns
4. Generates responses in authentic character voices

## Architecture

### RAG Pipeline Design

The system uses a multi-agent approach with CrewAI to handle different aspects of the RAG pipeline:

1. **Retrieval Agent**: Finds relevant passages from the book based on the question and character
2. **Character Analysis Agent**: Analyzes character traits, speech patterns, and behaviors
3. **Response Generation Agent**: Creates in-character responses using the retrieved context

### PDF Processing

- The PDF is processed using `pdfplumber` to extract text
- Text is cleaned to remove headers, footers, and page numbers
- Content is segmented by chapters and paragraphs for better context retention

### Vector Store

- Uses ChromaDB as the vector database
- SentenceTransformer embeddings for semantic search
- Documents are stored with metadata including chapter and paragraph information

### Character Analysis

- Pre-defined base traits for main characters
- Dynamic character analysis using retrieved passages
- Identifies speech patterns and typical reactions

### Response Generation

- Uses Google's Gemini model for generating responses
- Responses are crafted based on character traits and relevant book context
- Includes explanation of how the response aligns with character personality

### Memory System

- Logs interactions to maintain conversation history
- Stores questions, character selections, and responses
- Enables character consistency across multiple questions

## Setup Instructions

### Prerequisites

- Python 3.9+
- Google Gemini API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/harry-potter-rag.git
   cd harry-potter-rag
   ```

2. Install dependencies:
   ```
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```
   export GEMINI_API_KEY="your_gemini_api_key"
   ```
   
   Alternatively, create a `.env` file with:
   ```
   GEMINI_API_KEY="your_gemini_api_key"
   ```

4. Download the Harry Potter book:
   - Download [Harry Potter and the Sorcerer's Stone](https://hazidesaratcollege.ac.in/library/uploads/85jkr_harrypotter_1.pdf)
   - Save it to `data/harry_potter_book.pdf`

### Running the Application

1. Run in interactive mode:
   ```
   python -m src.main
   ```

2. Run test cases:
   ```
   python -m src.main --test
   ```

3. Ask a specific question to a character:
   ```
   python -m src.main --question "What would you do if you found a mysterious artifact in Hogwarts?" --character "Hermione Granger"
   ```

## Example Outputs

### Test Case 1: Ron Weasley

**Question**: "How would you react to seeing a ghost for the first time?"

**Response**:
```
Bloody hell! I mean, I've heard about the Hogwarts ghosts from my brothers, but seeing one float through a wall still gives me the creeps! Fred and George kept telling me Nearly Headless Nick would pop out during breakfast and show how his head dangles by a bit of skin. They're not so bad once you get used to them though. Just don't get me started on Peeves - that poltergeist is a nightmare! He's not even a proper ghost, just likes causing trouble. At least the Bloody Baron can keep him in line.
```

**Explanation**:
This response captures Ron's informal speech patterns with expressions like "Bloody hell!" and references to his brothers' stories. I emphasized Ron's tendency to be easily startled yet quick to adapt, while incorporating his knowledge of wizarding world elements that would be familiar to him as someone from a wizarding family. His mention of Peeves reflects his practical concerns about troublemakers.

### Test Case 2: Harry Potter

**Question**: "What would you say to someone bullying a friend?"

**Response**:
```
Leave them alone! What's the matter with you? I don't care who your father is or what house you're in - you don't get to treat people like that. My friend hasn't done anything wrong to you. 

I know what it's like when no one stands up for you. Before Hogwarts, my cousin Dudley and his gang bullied me for years, and nobody ever stepped in. I'm not letting that happen to my friends.
```

**Explanation**:
The response reflects Harry's straightforward defense of others and his strong sense of justice, drawing on his experiences with Dudley's bullying. I focused on Harry's courage to stand up against intimidation regardless of consequences, which is consistent with scenes where he confronts Malfoy. His personal connection to being bullied adds emotional depth characteristic of his empathetic nature.

### Test Case 3: Draco Malfoy

**Question**: "What's your plan to win a Quidditch match?"

**Response**:
```
Win a Quidditch match? Well, unlike Potter who gets by on sheer dumb luck, I actually have skill and strategy. Father bought the entire Slytherin team Nimbus 2001s - the fastest brooms gold can buy. Superior equipment for superior players, naturally.

The Slytherin way is to use every advantage. We play aggressive - intimidate the other team, especially their Seeker. If they're scared, they make mistakes. My father says winning isn't about playing fair, it's about ensuring victory by any means necessary. When I spot the Snitch, I won't hesitate like some Gryffindors might.
```

**Explanation**:
This response captures Draco's arrogant personality with his dismissive attitude toward Harry, emphasis on wealth and connections, and Slytherin's win-at-all-costs mentality. I incorporated his frequent references to his father and material advantages (like brooms) that feature prominently in his character. His speech pattern includes the condescending tone he typically uses when discussing other houses.

## Project Structure

```
harry_potter_rag/
├── data/
│   └── harry_potter_book.pdf
├── db/
│   └── vector_store/
├── logs/
│   └── agent_memory.log
├── src/
│   ├── __init__.py
│   ├── config.py
│   ├── pdf_processor.py
│   ├── vector_store.py
│   ├── agents.py
│   ├── tools.py
│   ├── memory.py
│   └── main.py
├── requirements.txt
└── README.md
```

## Future Improvements

- Fine-tune a language model specifically for Harry Potter characters
- Add support for multiple books for broader character knowledge
- Implement a web interface for easier interaction
- Expand memory system to better track conversation history
- Add emotion detection to respond appropriately to user sentiment