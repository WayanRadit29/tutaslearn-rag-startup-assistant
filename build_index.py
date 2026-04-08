import os
import json
from llama_index.core import VectorStoreIndex, Document, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

JSONL_PATH = "data/chunk/chunk1.jsonl"
STORAGE_DIR = "storage"


def load_chunks_from_jsonl(jsonl_path):
    documents = []

    with open(jsonl_path, "r", encoding="utf-8") as f:
        for line_number, line in enumerate(f, start=1):
            line = line.strip()

            if not line:
                continue

            try:
                item = json.loads(line)
            except json.JSONDecodeError:
                print(f"[WARNING] Baris {line_number} bukan JSON valid, dilewati.")
                continue

            content = item.get("content", "").strip()

            if not content:
                print(f"[WARNING] Baris {line_number} tidak punya 'content', dilewati.")
                continue

            metadata = {
                "id": item.get("id", ""),
                "source": item.get("source", ""),
                "title": item.get("title", ""),
                "tags": ", ".join(item.get("tags", [])),
                "category": item.get("category", "")
            }

            doc = Document(
                text=content,
                metadata=metadata
            )
            documents.append(doc)

    return documents


def main():
    print(f"Loading chunks from: {JSONL_PATH}")

    if not os.path.exists(JSONL_PATH):
        print(f"[ERROR] File tidak ditemukan: {JSONL_PATH}")
        return

    # Embedding model ringan dan cocok untuk MVP
    Settings.embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    documents = load_chunks_from_jsonl(JSONL_PATH)

    print(f"Total chunks loaded: {len(documents)}")

    if len(documents) == 0:
        print("[ERROR] Tidak ada chunk valid yang berhasil dimuat.")
        return

    print("Building vector index...")
    index = VectorStoreIndex.from_documents(documents)

    os.makedirs(STORAGE_DIR, exist_ok=True)

    print(f"Saving index to: {STORAGE_DIR}")
    index.storage_context.persist(persist_dir=STORAGE_DIR)

    print("Build index selesai.")


if __name__ == "__main__":
    main()