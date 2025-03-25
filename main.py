from src.parser import organize_existing_docs
from src.vector_store import index_all_documents
from src.comparator import compare_new_document

def main():
    print("Organizing existing documentation...")
    EXISTING_DOCS_DIR = "./data/existing_docs" 
    organize_existing_docs(EXISTING_DOCS_DIR)


    print("\nIndexing documents...")
    index_all_documents()

    print("\n Adding a new document for classification...")
    new_doc_path = "./data/new_docs/clV2.pdf"

    print("\nRunning comparison on new document...")
    compare_new_document(new_doc_path)



if __name__ == "__main__":
    main()
