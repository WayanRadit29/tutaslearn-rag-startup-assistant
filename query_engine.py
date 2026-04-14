from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama
from llama_index.core.prompts import PromptTemplate
import streamlit as st
import os

STORAGE_DIR = "storage"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL_NAME = "llama3.2:1b"
OLLAMA_BASE_URL = os.environ.get("OLLAMA_BASE_URL", "http://localhost:11434")

QA_PROMPT = PromptTemplate(
"""
Kamu adalah asisten belajar startup.

Tugas kamu adalah menjawab pertanyaan HANYA berdasarkan konteks yang diberikan.

ATURAN WAJIB:
- Gunakan hanya informasi dari konteks.
- DILARANG menambahkan informasi di luar konteks.
- Jika tidak ada di konteks, jangan menebak.
- Gunakan bahasa Indonesia yang sederhana, jelas, dan natural.
- Hindari kata-kata aneh atau tidak umum.
- Jawaban harus langsung ke inti, tidak bertele-tele.

PENTING:
Jawaban harus disesuaikan dengan jenis pertanyaan:

1. Jika pertanyaan DEFINISI:
→ Jawab dengan 2–3 kalimat yang jelas dan langsung.

2. Jika pertanyaan TANDA / CIRI:
→ Jawab dalam bentuk poin-poin (bullet points), maksimal 4 poin.

3. Jika pertanyaan ALASAN / KENAPA:
→ Jelaskan singkat (2–4 kalimat).

4. Jika pertanyaan STUDI KASUS / PENJELASAN:
→ Jawab lebih detail (4–6 kalimat)
→ Jelaskan urutan kejadian atau insight utama
→ Tetap hanya dari konteks

ATURAN TAMBAHAN:
- Jangan mengulang pertanyaan.
- Jangan mencampur definisi dengan tanda jika tidak diminta.
- Jangan menambahkan opini pribadi.
- Jangan mengarang contoh baru.

Jika konteks tidak cukup:
Jawab: "Informasi pada dokumen belum cukup untuk menjawab pertanyaan ini."

Konteks:
---------------------
{context_str}
---------------------

Pertanyaan:
{query_str}

Jawaban:
"""
)

@st.cache_resource
def get_query_engine():
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL_NAME
    )

    Settings.llm = Ollama(
        model=OLLAMA_MODEL_NAME,
        base_url=OLLAMA_BASE_URL,
        request_timeout=180.0
    )

    storage_context = StorageContext.from_defaults(
        persist_dir=STORAGE_DIR
    )
    index = load_index_from_storage(storage_context)

    query_engine = index.as_query_engine(
        similarity_top_k=3,
        text_qa_template=QA_PROMPT,
    )

    return query_engine


def ask_question(question: str):
    query_engine = get_query_engine()
    response = query_engine.query(question)

    answer = str(response).strip()

    sources = []
    if hasattr(response, "source_nodes"):
        for node in response.source_nodes:
            sources.append({
                "score": round(node.score, 4) if node.score is not None else None,
                "text": node.text,
                "metadata": node.metadata
            })

    # fallback sederhana kalau source terlalu lemah
    if sources:
        best_score = sources[0]["score"]
        if best_score is not None and best_score < 0.45:
            answer = (
                "Saya belum menemukan konteks yang cukup kuat di dokumen untuk menjawab "
                "pertanyaan ini dengan yakin. Coba buat pertanyaannya lebih spesifik."
            )

    return {
        "answer": answer,
        "sources": sources
    }