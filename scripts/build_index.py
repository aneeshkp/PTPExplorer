import os
import json
import faiss
import numpy as np
import sys
# Ensure the parent directory is in the sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from sentence_transformers import SentenceTransformer
from core.pdf_loader import load_pdfs_from_folder
from core.chunker import chunk_text
# Ensure the parent directory is in the sys.path
from config.settings import INDEX_FILE,MODEL_NAME, METADATA_FILE,CHUNK_SIZE

def generate_chunks():
    print("🔍 Loading PDFs...")
    pdf_texts = load_pdfs_from_folder("openshift_docs")
    chunks = []

    for version, text in pdf_texts.items():
        print(f"📖 Processing OpenShift {version}...")
        chunked_texts = chunk_text(text, CHUNK_SIZE)
        for i, chunk in enumerate(chunked_texts):
            chunks.append({
                "version": version,
                "chunk_id": f"{version}_{i}",
                "text": chunk
            })

    print(f"✅ Total Chunks Generated: {len(chunks)}")
    return chunks

def generate_embeddings(texts):
    print("💡 Generating Embeddings...")
    model = SentenceTransformer(MODEL_NAME)
    embeddings = model.encode(texts, show_progress_bar=True)
    return np.array(embeddings).astype("float32")

def build_faiss_index(chunks):
    print("⚙️ Building FAISS Index...")
    texts = [chunk["text"] for chunk in chunks]
    embeddings = generate_embeddings(texts)

    # Initialize FAISS index
    d = embeddings.shape[1]
    index = faiss.IndexFlatL2(d)
    index.add(embeddings)
    faiss.write_index(index, INDEX_FILE)

    with open(METADATA_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f)

    print(f"✅ FAISS index saved to {INDEX_FILE}")
    print(f"✅ Metadata saved to {METADATA_FILE}")

if __name__ == "__main__":
    os.makedirs("models", exist_ok=True)
    chunks = generate_chunks()
    build_faiss_index(chunks)
