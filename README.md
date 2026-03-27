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
* OpenAI API (Embeddings and LLM)
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

### 1. Clone the repository

```bash
git clone https://github.com/your-username/tutaslearn-rag-startup-assistant.git
cd tutaslearn-rag-startup-assistant
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Set up environment variables

Create a `.env` file and add:

```
OPENAI_API_KEY=your_api_key_here
```

### 4. Build the index

```bash
python build_index.py
```

### 5. Run the application

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

* Backend and Integration: [Your Name]
* Data and Evaluation: [Member Name]
* UI and Experience: [Member Name]

---

## License

This project is for academic and educational purposes.
