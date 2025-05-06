import os
import fitz  # PyMuPDF
from pathlib import Path
import json

BASE_DIR = "openshift_docs"
CHUNK_SIZE = 800  # words
OUTPUT_FILE = "chunks.jsonl"

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def chunk_text(text, chunk_size):
    words = text.split()
    return [
        " ".join(words[i:i + chunk_size])
        for i in range(0, len(words), chunk_size)
    ]

def parse_all_pdfs(base_dir):
    chunks = []
    for version in os.listdir(base_dir):
        pdf_path = Path(base_dir) /version/ f"networking.pdf"
        if not pdf_path.exists():
            print(f"Missing PDF for version {version}, skipping.")
            continue

        print(f"Processing {pdf_path}...")
        text = extract_text_from_pdf(pdf_path)
        chunked = chunk_text(text, CHUNK_SIZE)

        for i, chunk in enumerate(chunked):
            chunks.append({
                "version": version,
                "chunk_id": f"{version}_{i}",
                "text": chunk
            })

    return chunks

if __name__ == "__main__":
    all_chunks = parse_all_pdfs(BASE_DIR)

    with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
        for chunk in all_chunks:
            f.write(json.dumps(chunk) + "\n")

    print(f"\n✅ Done! Extracted and chunked {len(all_chunks)} text blocks into {OUTPUT_FILE}")