from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

STORAGE_DIR = "storage"
EMBED_MODEL_NAME = "sentence-transformers/all-MiniLM-L6-v2"
OLLAMA_MODEL_NAME = "llama3.2:1b"


def load_query_engine():
    # Embedding harus sama dengan saat build index
    Settings.embed_model = HuggingFaceEmbedding(
        model_name=EMBED_MODEL_NAME
    )

    # LLM lokal dari Ollama
    Settings.llm = Ollama(
        model=OLLAMA_MODEL_NAME,
        request_timeout=180.0
    )

    # Load index dari folder storage
    storage_context = StorageContext.from_defaults(
        persist_dir=STORAGE_DIR
    )
    index = load_index_from_storage(storage_context)

    # Ambil 2 source paling relevan dulu biar ringan
    query_engine = index.as_query_engine(
        similarity_top_k=1
    )

    return query_engine


def ask_question(question: str):
    query_engine = load_query_engine()
    response = query_engine.query(question)

    answer = str(response)

    sources = []
    if hasattr(response, "source_nodes"):
        for node in response.source_nodes:
            sources.append({
                "score": round(node.score, 4) if node.score is not None else None,
                "text": node.text,
                "metadata": node.metadata
            })

    return {
        "answer": answer,
        "sources": sources
    }


if __name__ == "__main__":
    print("=== Startup Knowledge Assistant ===")
    question = input("Masukkan pertanyaan: ").strip()

    if not question:
        print("Pertanyaan tidak boleh kosong.")
    else:
        result = ask_question(question)

        print("\n=== JAWABAN ===")
        print(result["answer"])

        print("\n=== SOURCES ===")
        if not result["sources"]:
            print("Tidak ada source ditemukan.")
        else:
            for i, source in enumerate(result["sources"], start=1):
                metadata = source["metadata"]

                print(f"\nSource {i}")
                print(f"Score    : {source['score']}")
                print(f"ID       : {metadata.get('id', '-')}")
                print(f"Title    : {metadata.get('title', '-')}")
                print(f"Source   : {metadata.get('source', '-')}")
                print(f"Category : {metadata.get('category', '-')}")
                print(f"Tags     : {metadata.get('tags', '-')}")
                print(f"Text     : {source['text'][:250]}...")