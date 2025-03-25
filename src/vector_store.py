from llama_index.core import VectorStoreIndex, SimpleDirectoryReader
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.core import Settings
import os

EN_PROCESSED_DIR = "./data/processed_docs/english"
DE_PROCESSED_DIR = "./data/processed_docs/german"
INDEX_OUTPUT_DIR = "./data/indexes"

embedding_model = HuggingFaceEmbedding(model_name="sentence-transformers/distiluse-base-multilingual-cased-v1") # model is cached locally 
# we chose this model because it supports multiple languages and we need english and german support, also it is lightweight and can be ran localy


def load_documents_from_json(folder_path):
    documents = []
    for filename in os.listdir(folder_path):
        if filename.endswith(".json"):
            full_path = os.path.join(folder_path, filename)
            docs = SimpleDirectoryReader(input_files=[full_path]).load_data()
            documents.extend(docs)
    return documents



def build_index(documents, index_name):
    Settings.embed_model = embedding_model  # Set globally for all index operations
    index = VectorStoreIndex.from_documents(documents)
    index_path = os.path.join(INDEX_OUTPUT_DIR, index_name)
    os.makedirs(index_path, exist_ok=True)
    index.storage_context.persist(persist_dir=index_path)
    print(f"Index saved at: {index_path}")
    return index


def index_all_documents():
    print("Indexing English documents...")
    en_docs = load_documents_from_json(EN_PROCESSED_DIR)
    build_index(en_docs, "english")

    print("Indexing German documents...")
    de_docs = load_documents_from_json(DE_PROCESSED_DIR)
    build_index(de_docs, "german")


if __name__ == "__main__":
    index_all_documents()
