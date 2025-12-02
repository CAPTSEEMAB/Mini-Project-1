from pydantic import BaseModel


class UploadResponse(BaseModel):
    original_filename: str
    stored_path: str
    extracted_path: str
    embedding_path: str


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str
