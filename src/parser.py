import os
import fitz  # PyMuPDF
import json
import re
import langid

OUTPUT_DIR = "./data/processed_docs"
EN_DIR = os.path.join(OUTPUT_DIR, "english")
DE_DIR = os.path.join(OUTPUT_DIR, "german")


def extract_text_from_pdf(pdf_path):
    doc = fitz.open(pdf_path)
    text_pages = []
    for page in doc:
        text = page.get_text("text")
        text_pages.append(text)
    return "\n".join(text_pages)


def chunk_text(text):
    # Try structured legal heading-based chunking first because this preserves more context than chunking by paragraphs
    chunks = re.split(r"(?i)(?=\\b(Article|Section|§)\\s+\\d+)", text)
    structured = []
    for i in range(0, len(chunks) - 1, 2):
        title = chunks[i].strip()
        body = chunks[i + 1].strip()
        if title or body:
            structured.append({"title": title, "text": body})

    # If no chunks found, fallback to paragraph-based chunking
    if not structured:
        paragraphs = text.split("\\n\\n")
        for para in paragraphs:
            para = para.strip()
            if para:
                structured.append({"title": "", "text": para})

    return structured


def classify_and_store_document(pdf_path):
    filename = os.path.basename(pdf_path)
    print(f"Classifying and processing {filename}...")

    text = extract_text_from_pdf(pdf_path)
    lang, _ = langid.classify(text[:2000])  # Detect language from first 2000 characters
    chunks = chunk_text(text)

    doc_data = {
        "filename": filename,
        "language": lang,
        "chunks": chunks
    }

    # Determine output directory based on language
    if lang == "de":
        output_path = os.path.join(DE_DIR, filename.replace(".pdf", ".json"))
    else:
        output_path = os.path.join(EN_DIR, filename.replace(".pdf", ".json"))

    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(doc_data, f, ensure_ascii=False, indent=2)

    print(f"Document stored in {'german' if lang == 'de' else 'english'} folder.")
    return doc_data


def organize_existing_docs(doc_dir):
    os.makedirs(EN_DIR, exist_ok=True)
    os.makedirs(DE_DIR, exist_ok=True)
    all_docs = []

    for filename in os.listdir(doc_dir):
        if not filename.endswith(".pdf"):
            continue

        filepath = os.path.join(doc_dir, filename)
        doc_data = classify_and_store_document(filepath)
        all_docs.append(doc_data)

    print(f"Processed {len(all_docs)} documents.")
    return all_docs


if __name__ == "__main__":
    organize_existing_docs(doc_dir='./data/existing_docs')
