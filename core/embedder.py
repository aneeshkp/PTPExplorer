import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import json
import os

MODEL_NAME = "all-MiniLM-L6-v2"

def embed_texts(texts):
    model = SentenceTransformer(MODEL_NAME)
    return model.encode(texts, show_progress_bar=True)

def build_faiss_index(embeddings, metadata, index_path, metadata_path):
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    faiss.write_index(index, index_path)

    with open(metadata_path, "w") as f:
        json.dump(metadata, f)
    print("Index and Metadata saved.")

def generate_index_from_chunks(chunks, index_path="models/ptp_faiss.index", metadata_path="models/ptp_metadata.json"):
    texts = [chunk['text'] for chunk in chunks]
    embeddings = embed_texts(texts)
    embeddings_np = np.array(embeddings).astype("float32")

    build_faiss_index(embeddings_np, chunks, index_path, metadata_path)
