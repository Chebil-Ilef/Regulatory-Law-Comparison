from src.parser import organize_existing_docs, classify_and_store_document
import os

def main():
    print("Organizing existing documentation...")
    EXISTING_DOCS_DIR = "./data/existing_docs" 
    NEW_DOC_DIR = "./data/new_docs"
    organize_existing_docs(EXISTING_DOCS_DIR)
    print("Organizing new documentation...")
    organize_existing_docs(NEW_DOC_DIR)

    print("\n Adding a new document for classification...")
    new_doc_path = "./data/dummy/bmbf_medtec_leitfaden_mp.pdf"
    # new_doc_path = "./data/dummy/User-Guide-Regulatory-documents-and-reports.pdf"

    if os.path.exists(new_doc_path):
        classify_and_store_document(new_doc_path)
    else:
        print(f"No new document found at: {new_doc_path}")

if __name__ == "__main__":
    main()
