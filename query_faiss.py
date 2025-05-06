import faiss
import json
import numpy as np
from sentence_transformers import SentenceTransformer

INDEX_FILE = "ptp_faiss.index"
METADATA_FILE = "ptp_metadata.json"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
TOP_K = 5

def search(query, top_k=TOP_K):
    print("🔍 Loading FAISS index...")
    index = faiss.read_index(INDEX_FILE)

    print("💡 Loading metadata...")
    with open(METADATA_FILE, "r", encoding="utf-8") as f:
        metadata = json.load(f)

    print("💬 Embedding query...")
    model = SentenceTransformer(EMBEDDING_MODEL)
    query_vec = model.encode([query]).astype("float32")

    print("🔎 Searching FAISS...")
    D, I = index.search(query_vec, top_k)

    results = []
    for idx in I[0]:
        entry = metadata[idx]
        results.append({
            "version": entry["version"],
            "chunk_id": entry["chunk_id"],
            "text": entry["text"]
        })

    return results

if __name__ == "__main__":
    user_query = input("❓ Enter your question: ")
    matches = search(user_query)

    print("\n🎯 Top Results:")
    for match in matches:
        print(f"\n--- Version {match['version']} | Chunk {match['chunk_id']} ---\n{match['text'][:500]}...\n")