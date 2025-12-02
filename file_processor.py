import json
from pathlib import Path
import pandas as pd

from text_cleaner import clean_text
from llm_service import get_embeddings


def load_csv(file_path: Path) -> list[dict]:
    df = pd.read_csv(file_path)
    return df.to_dict('records')


def generate_row_embeddings(file_path: Path, embeddings_dir: Path) -> Path:
    file_path = Path(file_path)
    embeddings_dir = Path(embeddings_dir)
    
    data = load_csv(file_path)
    
    # Generate embeddings for each row
    rows_with_embeddings = []
    for row in data:
        row_text = ", ".join([f"{k}: {v}" for k, v in row.items()])
        cleaned_row = clean_text(row_text)
        embedding = get_embeddings(cleaned_row)
        
        rows_with_embeddings.append({
            "row_data": row,
            "row_text": row_text,
            "cleaned_text": cleaned_row,
            "embedding": embedding
        })
    
    # Save embeddings to JSON file
    output_path = embeddings_dir / f"{file_path.stem}_embeddings.json"
    output_path.write_text(json.dumps({
        "source_file": file_path.name,
        "total_rows": len(rows_with_embeddings),
        "rows": rows_with_embeddings
    }, indent=2))
    
    return output_path
