# Regulatory Document Comparator

A fully local, private system for comparing incoming regulatory documents (PDFs) against existing documentation in English and German. Designed for legal and compliance workflows with support for LLM-powered semantic change detection.

---

## Features

- Fully offline and local (no external APIs)
- Multilingual support
- Semantic clause comparison powered by LLM (via Ollama)
- Modular pipeline for parsing, indexing, and comparison
- Automatic generation of human-readable change reports
- Built on **LlamaIndex** for chunk embedding and retrieval

---

## Project Structure

```
├── main.py                      # Main pipeline runner
├── requirements.txt             # Requirements
├── src/
│   ├── parser.py               # PDF extraction, language detection, chunking
│   ├── vector_store.py         # Indexing and embedding using LlamaIndex
│   ├── comparator.py           # Finds similar chunks and runs comparisons
│   └── ollama_comparison.py    # Uses Ollama LLM (currently deepseek-r1:8b) to summarize and classify changes
├── data/
│   ├── existing_docs/          # Input PDFs (existing regulations)
│   ├── new_docs/               # Incoming PDF updates
│   ├── processed_docs/         # Chunked JSON files
│   ├── indexes/                # LlamaIndex vector index per language
├── reports/                    # Text report with LLM outputs
```

---

## Requirements

- Python 3.10+
- [`ollama`](https://ollama.com/) (local LLM runtime)
- Recommended model: `deepseek-r1:8b` (under 6GB memory)

```bash
ollama run deepseek-r1:8b
```

- Create a virtual environment and install dependencies

```bash
python -m venv .venv
```

```bash
source venv/bin/activate
```

```bash
pip install -r requirements.txt
```

---

## 🧪 How to Run

1. Place your existing PDFs under `data/existing_docs/`
2. Place new incoming PDFs under `data/new_docs/`
3. Run the pipeline:

```bash
python main.py
```

This will:
- Organize and index all documents
- Classify and process the new PDF (added in pipeline)
- Compare it chunk-by-chunk
- Save a report under `reports/comparison_report.txt`

---

## Technologies Used

- Python, PyMuPDF, langid
- LlamaIndex (vector DB)
- sentence-transformers (multilingual embeddings)
- Ollama (local LLM runtime)

---

## License
MIT License

---
