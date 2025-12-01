import json
import csv
from pathlib import Path
import requests  # for calling Ollama API

# -----------------------------------------
# CONFIG: Ollama API
# -----------------------------------------
OLLAMA_URL = "http://127.0.0.1:11434/api/embeddings"  # Docker Ollama API endpoint
MODEL_NAME = "nomic-embed-text"  # or your installed model

# -----------------------------------------
# FUNCTIONS
# -----------------------------------------

def load_file(file_path: str):
    """
    Load CSV or JSON file and return a list of text rows
    """
    path = Path(file_path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {file_path}")

    ext = path.suffix.lower()

    rows = []

    if ext == ".csv":
        with path.open("r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert dict to single text string
                rows.append(" | ".join([f"{k}: {v}" for k, v in row.items()]))

    elif ext == ".json":
        with path.open("r", encoding="utf-8") as f:
            data = json.load(f)
            if isinstance(data, list):
                for item in data:
                    if isinstance(item, dict):
                        rows.append(" | ".join([f"{k}: {v}" for k, v in item.items()]))
                    else:
                        rows.append(str(item))
            else:
                rows.append(str(data))
    else:
        raise ValueError("Only CSV or JSON files are supported")

    return rows



def get_embeddings(text_list):
    embeddings = []

    for text in text_list:
        payload = {
            "model": MODEL_NAME,
            "prompt": text
        }

        #print("Sending:", payload)

        response = requests.post(OLLAMA_URL, json=payload)
        #print("Raw response:", response.text)

        response.raise_for_status()
        data = response.json()

        emb = data.get("embedding")

        if not emb:
            print(f"❌ No embedding returned for: {text}")
        else:
            embeddings.append(emb)

    return embeddings


def save_embeddings(embeddings, output_file: str):
    """
    Save embeddings to JSON file and return the file path
    """
    Path("embeddings").mkdir(exist_ok=True)  # ensure folder exists
    output_path = Path("embeddings") / output_file
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(embeddings, f, ensure_ascii=False, indent=2)
    print(f"✅ Embeddings saved to {output_path}")
    return str(output_path)

# -----------------------------------------
# MAIN (for testing)
# -----------------------------------------
if __name__ == "__main__":
    filename = input("Enter CSV/JSON filename (e.g., upload/data.csv): ").strip()
    rows = load_file(filename)
    print(f"Loaded {len(rows)} rows from {filename}")

    embeddings = get_embeddings(rows)
    print(f"Generated {len(embeddings)} embeddings")

    output_file = Path(filename).stem + "_embeddings.json"
    save_embeddings(embeddings, output_file)
