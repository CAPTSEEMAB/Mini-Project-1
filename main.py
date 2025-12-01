import json
from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from pathlib import Path
import shutil

from file_reader import load_file
from generate_embeddings import get_embeddings, save_embeddings
from text_cleaner import clean_text

app = FastAPI()
templates = Jinja2Templates(directory="templates")

UPLOAD_DIR = Path("upload")
UPLOAD_DIR.mkdir(exist_ok=True)
EMBEDDINGS_DIR = Path("embeddings")
EMBEDDINGS_DIR.mkdir(exist_ok=True)

# ----------------- Home + Upload + Save Embeddings -----------------
@app.get("/", response_class=HTMLResponse)
def home(request: Request, message: str = ""):
    return templates.TemplateResponse("index.html", {"request": request, "message": message})

@app.post("/", response_class=HTMLResponse)
async def upload_and_generate(request: Request, file: UploadFile = File(...)):
    try:
        
        # Save uploaded file
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        cleaned_rows = []
        embeddings_list = []

        # Load file and generate embeddings
        rows = load_file(str(file_path))
        print(rows)
        
        for key, value in rows.items():
            cleaned = clean_text(value)
            print(f"{key} => {value}")

#         print(cleaned)  # Shows the number of rows
        emb = get_embeddings(cleaned)
        if emb:
            embeddings_list.append(emb)
  
#         # Save embeddings
        output_path = EMBEDDINGS_DIR / f"{file.filename}_embeddings.json"
        with output_path.open("w", encoding="utf-8") as f:
            json.dump(embeddings_list, f, indent=2)

#         #output_file = save_embeddings(embeddings, file.filename)

        message = f"✅ File '{file.filename}' uploaded successfully! Rows processed: {len(rows)}. Embeddings saved at '{output_file}: embeddings {embeddings}  '."

    except Exception as e:
        message = f"❌ Error: {str(e)}"

#    # Redirect to success page
    return templates.TemplateResponse(
        "upload_result.html",
        {
            "request": request,
            "filename": file.filename,
            "rows_count": len(rows),
            "embed_file": str(output_path)
        }
     )