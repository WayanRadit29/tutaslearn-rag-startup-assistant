from llama_index.core import StorageContext, load_index_from_storage, Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
from llama_index.llms.ollama import Ollama

STORAGE_DIR = "storage"
EMBED_MODEL_NAME = "sentence-transformer/all-MiniLM-L6-v2"
OLLAMA_MODEL_NAME = "mistral"

