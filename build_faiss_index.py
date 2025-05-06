import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer
import os

CHUNKS_FILE = "chunks.jsonl"
INDEX_FILE = "ptp_faiss.index"
METADATA_FILE = "ptp_metadata.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"

def load_chunks(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return [json.loads(line.strip()) for line in f]

def embed_chunks(chunks, model):
    texts = [c["text"] for c in chunks]
    return model.encode(texts, show_progress_bar=True)

def build_faiss_index(embeddings):
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    return index

if __name__ == "__main__":
    print("🔍 Loading chunks...")
    chunks = load_chunks(CHUNKS_FILE)

    print("💡 Loading embedding model...")
    model = SentenceTransformer(EMBEDDING_MODEL)

    print("⚙️  Generating embeddings...")
    embeddings = embed_chunks(chunks, model)
    embeddings_np = np.array(embeddings).astype("float32")

    print("📦 Building FAISS index...")
    index = build_faiss_index(embeddings_np)

    print(f"💾 Saving index to {INDEX_FILE}...")
    faiss.write_index(index, INDEX_FILE)

    print(f"📝 Saving metadata to {METADATA_FILE}...")
    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f)

    print("✅ Done! You can now run search queries.")