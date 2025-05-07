import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer
import requests  # Required for LLM API calls
import sys
import os
# Ensure the parent directory is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config.settings import EMBEDDING_MODEL
# Load FAISS Index and Metadata
def load_faiss_index():
    return faiss.read_index("models/ptp_faiss.index")

def load_metadata():
    with open("models/ptp_metadata.json", "r", encoding="utf-8") as f:
        return json.load(f)

def search(query, top_k=5, versions=None, prioritize_keyword=None):
    index = load_faiss_index()
    metadata = load_metadata()
    model = SentenceTransformer(EMBEDDING_MODEL)

    query_vec = model.encode([query]).astype("float32")
    D, I = index.search(query_vec, top_k * 3)  # Increased range for better filtering

    results = []
    for idx in I[0]:
        if idx < len(metadata):
            entry = metadata[idx]
            if versions and entry['version'] not in versions:
                continue
            if prioritize_keyword:
                if prioritize_keyword.lower() in entry['text'].lower():
                    results.insert(0, entry)  # Prioritize matching keyword
                else:
                    results.append(entry)
            else:
                results.append(entry)
    return results[:top_k]

# LLM Query Function (Ollama - Mistral)
def query_ollama(prompt, model="mistral"):
    """
    Queries a local Ollama LLM (Mistral) and returns the response.
    """
    try:
        response = requests.post("http://localhost:11434/api/generate", json={
            "model": model,
            "prompt": prompt,
            "stream": False
        })
        if response.status_code == 200:
            return response.json().get("response", "No response from LLM.")
        else:
            return f"Error: {response.status_code} - {response.text}"
    except requests.exceptions.RequestException as e:
        return f"Error contacting Ollama API: {str(e)}"
