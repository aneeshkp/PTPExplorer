import os

# Directory Paths
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
DOCS_DIR = os.path.join(BASE_DIR, "openshift_docs")
MODELS_DIR = os.path.join(BASE_DIR, "models")

CHUNKS_FILE = os.path.join(MODELS_DIR,"chunks.jsonl")

# PDF and Index Files
INDEX_FILE = os.path.join(MODELS_DIR, "ptp_faiss.index")
METADATA_FILE = os.path.join(MODELS_DIR, "ptp_metadata.json")

# Model Settings
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
MODEL_NAME = "all-MiniLM-L6-v2"# HuggingFace model for embeddings

# LLM Configuration
LLM_TYPE = "ollama"  # Options: "ollama", "openai"
LLM_API_URL = "http://localhost:11434/api/generate"  # Ollama API for local LLM

# Chunking Configuration
CHUNK_SIZE = 800  # Number of words per chunk

# Search Settings
TOP_K = 5  # Number of search results to retrieve

# Error Logging
LOGGING_ENABLED = True
LOG_FILE = os.path.join(BASE_DIR, "logs", "ptp_explorer.log")

# Environment Variables (for API keys)
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
