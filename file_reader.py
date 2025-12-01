
import csv
import json
from pathlib import Path


def load_file(file_path: str):
    """
    Reads a CSV or JSON file and returns Python data.
    This function is ready to be integrated with FastAPI.
    """

    path = Path(file_path)

    # 1. Check if file exists
    if not path.exists():
        raise FileNotFoundError(f"❌ File not found: {file_path}")

    # 2. Check file extension
    ext = path.suffix.lower()

    if ext == ".csv":
        return load_csv(path)

    elif ext == ".json":
        return load_json(path)

    else:
        raise ValueError("❌ Only .csv or .json file formats are supported.")


def load_csv(path: Path):
    """
    Read CSV file and return a list of dictionaries.
    """
    rows = []

    with path.open("r", encoding="utf-8") as file:
        reader = csv.DictReader(file)

        for row in reader:
            rows.append(row)

    return rows


def load_json(path: Path):
    """
    Read JSON file and return Python objects.
    """
    with path.open("r", encoding="utf-8") as file:
        return json.load(file)


# --------------------------------------------------
# LOCAL TESTING (This part runs only when executed directly)
# --------------------------------------------------
if __name__ == "__main__":
    file_name = input("Enter file name (example: data.csv or data.json): ")

    try:
        result = load_file(file_name)
        print("\n✅ File Loaded Successfully!")
        #print(result)

    except Exception as e:
        print("\nError:", e)
