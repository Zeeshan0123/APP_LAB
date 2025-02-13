from fastapi import FastAPI, UploadFile, File
import uvicorn
import shutil
import os
from utils import save_pdf, pdf_to_documents, store_embeddings_in_chroma, chat_llm
from pydantic import BaseModel
from typing import List


app = FastAPI()

# Request model for chatbot input
class ChatRequest(BaseModel):
    user_query: str

UPLOAD_DIR = "uploads/"


@app.post("/upload-pdfs/")
async def upload_pdfs(files: List[UploadFile] = File(...)):
    os.makedirs(UPLOAD_DIR, exist_ok=True)  # Ensure upload directory exists
    file_names = []
    
    for file in files:
        print("Starting Ingestion: ",file)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        file_names.append(file.filename)

        # Save the uploaded file
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        # Convert PDF to documents
        documents = pdf_to_documents(file_path)

        # Store documents in ChromaDB
        store_embeddings_in_chroma(documents)
        print("Successfully ingested file: ",file)

    shutil.rmtree(UPLOAD_DIR)
    return {"message": "All PDFs processed and embeddings stored successfully", "files": file_names}

# API endpoint for chatbot interaction
@app.post("/submit")
def chat_endpoint(request: ChatRequest):
    response = chat_llm(request.user_query)
    return response


# Run the app with: uvicorn app:app --reload


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=4100)