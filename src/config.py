import os
from dotenv import load_dotenv
import yaml
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini API
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise ValueError("Please set GEMINI_API_KEY in .env file")

genai.configure(api_key=GEMINI_API_KEY)

# File paths
DATA_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data")
PDF_PATH = os.path.join(DATA_DIR, "harry_potter.pdf")
AGENT_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "agents", "agent_config.yaml")
TASK_CONFIG_PATH = os.path.join(os.path.dirname(__file__), "tasks", "task_config.yaml")


# Helper functions for loading YAML configs
def load_agent_config():
    with open(AGENT_CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

def load_task_config():
    with open(TASK_CONFIG_PATH, 'r') as f:
        return yaml.safe_load(f)

# Vector store configuration
CHUNK_SIZE = 1000
CHUNK_OVERLAP = 200
EMBEDDING_MODEL = "all-MiniLM-L6-v2"