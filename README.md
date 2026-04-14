# TutasLearn: RAG-based Startup Knowledge Assistant

## Overview

TutasLearn is a Retrieval-Augmented Generation (RAG) based AI system designed to help users understand startup fundamentals through reliable, document-grounded answers.

This system retrieves knowledge from curated startup resources (articles, case studies, and frameworks) and generates responses with clear references to the original sources.

---

## Objective

The goal of this project is to build a focused and feasible MVP that:

* Answers startup-related questions using trusted sources
* Provides grounded responses with citations
* Demonstrates the practical implementation of RAG architecture

---

## Key Features

* Retrieval-based question answering (RAG)
* Context-aware responses from curated startup materials
* Source citation for every answer
* Insight extraction from articles and case studies
* Simple interactive UI for querying the system

---

## System Architecture

```
User Query
    ↓
Streamlit UI
    ↓
Query Engine (LlamaIndex)
    ↓
VectorStoreIndex (Embeddings)
    ↓
Curated Dataset (Articles, Case Studies, Book Summary)
```

---

## Tech Stack

* Python
* LlamaIndex
* Ollama (`llama3.2:1b`) — local LLM, no API key needed
* HuggingFace Embeddings (`all-MiniLM-L6-v2`) — local embeddings
* Streamlit
* Local Vector Store

---

## Project Structure

```
startup-rag/
│
├── app.py
├── build_index.py
├── query_engine.py
├── requirements.txt
├── README.md
│
├── data/
│   ├── articles/
│   ├── case_studies/
│   └── books/
│
└── storage/
```

---

## Dataset

The dataset is intentionally small and high-quality, consisting of:

* 7 curated startup articles (Y Combinator, a16z, etc.)
* 3 startup case studies (Airbnb, Uber, Dropbox)
* 1 Lean Startup summary

All documents are structured for efficient retrieval and minimal noise.

---

## How It Works

1. Documents are loaded and split into chunks
2. Each chunk is converted into embeddings
3. Embeddings are stored in a vector index
4. User queries are embedded and matched with relevant chunks
5. The system generates answers based on retrieved context

---

## How to Run

### Option A — Docker (Recommended)

```bash
# 1. Build & start everything (app + Ollama)
docker compose up -d --build

# 2. On first run, pull the model into Ollama (one-time, ~1.3 GB)
docker compose exec ollama ollama pull llama3.2:1b

# 3. Open in browser
open http://localhost:8501

# Stop
docker compose down
```

> **Note:** The first startup takes ~1–2 minutes while Ollama loads the model. GPU is automatically used if available (NVIDIA Docker runtime). Without GPU, it still works but is slower.

### Option B — Local (No Docker)

#### 1. Prerequisites
- Python 3.11+
- [Ollama](https://ollama.com/) installed and running
- Pull the model: `ollama pull llama3.2:1b`

#### 2. Clone & install

```bash
git clone https://github.com/WayanRadit29/tutaslearn-rag-startup-assistant.git
cd tutaslearn-rag-startup-assistant
pip install -r requirements.txt
```

#### 3. Build the index (first time only)

```bash
python build_index.py
```

#### 4. Run

```bash
streamlit run app.py
```

---

## Example Queries

* What is product-market fit?
* Why did Airbnb succeed in the early stage?
* What is the Lean Startup methodology?
* How did Dropbox achieve viral growth?

---

## Limitations

* Only answers based on the provided dataset
* No real-time web search
* Not designed for personalized business advice

---

## Future Improvements

* Improved retrieval tuning
* Metadata filtering
* Enhanced UI/UX
* Expanded dataset

---

## Team

* Backend and Integration: Wayan Raditya Putra
* Data and Evaluation: Salsabila Hana Adniah
* UI and Experience: Ustu Bina Syahdiba

---

## License

This project is for academic and educational purposes.
