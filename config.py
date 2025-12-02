from pathlib import Path

BASE_DIR = Path(__file__).parent

UPLOAD_DIR = BASE_DIR / "upload"
EMBEDDINGS_DIR = BASE_DIR / "embeddings"
TEMPLATES_DIR = BASE_DIR / "templates"

UPLOAD_DIR.mkdir(exist_ok=True)
EMBEDDINGS_DIR.mkdir(exist_ok=True)

OLLAMA_BASE_URL = "http://localhost:11434/api"
EMBEDDING_MODEL = "nomic-embed-text"
CHAT_MODEL = "llama3.2"
