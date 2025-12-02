import json
import numpy as np
from pathlib import Path


def cosine_similarity(vec1: list, vec2: list) -> float:
    a = np.array(vec1)
    b = np.array(vec2)
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def find_top_matches(query_embedding: list, embeddings_dir: Path, top_k: int = 5) -> list:
    all_matches = []
    embeddings_path = Path(embeddings_dir)
    
    for emb_file in embeddings_path.glob("*_embeddings.json"):
        data = json.loads(emb_file.read_text())
        rows = data.get("rows", [])
        source_file = data.get("source_file", emb_file.name)
        
        for row in rows:
            stored_embedding = row.get("embedding", [])
            if stored_embedding:
                score = cosine_similarity(query_embedding, stored_embedding)
                all_matches.append({
                    "row_data": row.get("row_data", {}),
                    "score": score,
                    "source_file": source_file
                })
    
    all_matches.sort(key=lambda x: x["score"], reverse=True)
    return all_matches[:top_k]
