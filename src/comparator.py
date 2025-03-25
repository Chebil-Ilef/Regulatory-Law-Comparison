import os
import json
from llama_index.core import load_index_from_storage, StorageContext
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from src.parser import extract_text_from_pdf, classify_and_store_document

EN_INDEX_PATH = "./data/indexes/english"
DE_INDEX_PATH = "./data/indexes/german"

EMBED_MODEL = HuggingFaceEmbedding(model_name="sentence-transformers/distiluse-base-multilingual-cased-v1")


def load_index(language):
    index_dir = DE_INDEX_PATH if language == "de" else EN_INDEX_PATH
    storage_context = StorageContext.from_defaults(persist_dir=index_dir)
    index = load_index_from_storage(storage_context)
    return index


def compare_new_document(pdf_path):
    print(f"\nLoading and processing: {pdf_path}")

    # Detect language to find the right JSON path
    lang= classify_and_store_document(pdf_path)['language']
    lang_folder = "german" if lang == "de" else "english"
    base_filename = os.path.splitext(os.path.basename(pdf_path))[0] + ".json"
    json_path = os.path.join("./data/processed_docs", lang_folder, base_filename)

    if not os.path.exists(json_path):
        print(f"Processed JSON not found at {json_path}.")
        return

    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    chunks = data.get("chunks", [])

    if not chunks:
        print("No chunks found in document.")
        return

    # Load the correct vector index

    index = load_index(lang)
    retriever = index.as_retriever()
    top_k = 1000  #top 1000 similar chunks set fixed now for testing

    print(f"Language detected: {'German' if lang == 'de' else 'English'}")
    print(f"Searching for top-{top_k} similar chunks from existing docs...\n")

    for i, chunk in enumerate(chunks):
        new_text = chunk["text"]
        results = retriever.retrieve(new_text)

        print(f"\n--- Chunk {i+1} ---")
        print(f"New: {new_text[:300]}...")

        if results:
            print("Most similar in existing docs:")
            for j, result in enumerate(results):
                print(f"  Match #{j+1}: {result.node.get_content()[:300]}...")
        else:
            print("No similar content found.")