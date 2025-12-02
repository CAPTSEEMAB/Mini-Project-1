"""
FastAPI application with CSV upload, embeddings, and RAG-based chat.
Refactored with clean modular architecture.
"""
import json
import shutil
from pathlib import Path

from fastapi import FastAPI, Request, UploadFile, File
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse

from config import UPLOAD_DIR, EMBEDDINGS_DIR, TEMPLATES_DIR
from models import ChatRequest, ChatResponse
from text_cleaner import clean_text
from llm_service import get_embeddings, ask_llm
from embedding_service import find_top_matches
from file_processor import generate_row_embeddings, load_csv

app = FastAPI(title="CSV RAG Chat API")

templates = Jinja2Templates(directory=TEMPLATES_DIR)


@app.get("/", response_class=HTMLResponse)
def home(request: Request, message: str = ""):
    return templates.TemplateResponse("index.html", {"request": request, "message": message})


@app.get("/chat-ui", response_class=HTMLResponse)
def chat_ui(request: Request):
    return templates.TemplateResponse("chat.html", {"request": request})


@app.post("/", response_class=HTMLResponse)
async def upload_and_generate(request: Request, file: UploadFile = File(...)):
    # Upload CSV file and generate row-wise embeddings
    try:
        file_path = UPLOAD_DIR / file.filename
        with file_path.open("wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        data = load_csv(file_path) if file.filename.endswith('.csv') else []
        
        output_path = generate_row_embeddings(file_path, EMBEDDINGS_DIR)

        return templates.TemplateResponse(
            "upload_result.html",
            {
                "request": request,
                "filename": file.filename,
                "data": data,
                "rows_count": len(data),
                "embed_file": str(output_path)
            }
        )

    except Exception as e:
        return templates.TemplateResponse(
            "index.html",
            {"request": request, "message": f"❌ Error: {str(e)}"}
        )


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):

    cleaned_query = clean_text(request.question)
    query_embedding = get_embeddings(cleaned_query)
    
    if not query_embedding:
        return ChatResponse(answer="Failed to generate embedding for your question.")
    
    # find_top_matches function = Finds top matching rows using similarity search
    top_matches = find_top_matches(query_embedding, EMBEDDINGS_DIR, top_k=5)
    
    if not top_matches:
        return ChatResponse(answer="No data found. Please upload a CSV file first.")
    
    # Build context from matched rows
    context_lines = []
    for match in top_matches:
        row_data = match["row_data"]
        row_text = ", ".join([f"{k}: {v}" for k, v in row_data.items()])
        context_lines.append(row_text)
    
    context = "\n".join(context_lines)
    
    #ask_llm function=  Generates intelligent answer using Llama 3.2 which takes query and context (which is  our data from embeddings search)
    answer = ask_llm(request.question, context)
    
    return ChatResponse(answer=answer)



if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)