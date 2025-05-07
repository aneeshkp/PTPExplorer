import fitz  # PyMuPDF
import os

def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text = "\n".join(page.get_text() for page in doc)
    return text

def load_pdfs_from_folder(folder):
    pdf_texts = {}
    for version in os.listdir(folder):
        pdf_path = os.path.join(folder, version, f"networking.pdf")
        if os.path.exists(pdf_path):
            print(f"Loading PDF for version {version}...")
            text = extract_text_from_pdf(pdf_path)
            pdf_texts[version] = text
    return pdf_texts
