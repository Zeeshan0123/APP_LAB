import shutil
from fastapi import UploadFile
from langchain.document_loaders import PyPDFLoader
from langchain.schema import Document
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.embeddings.fastembed import FastEmbedEmbeddings
import os
import re
import json
from langchain_cerebras import ChatCerebras
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationalRetrievalChain
from langchain_core.prompts import ChatPromptTemplate

UPLOAD_DIR = "uploads/"  # Directory to store uploaded PDFs

def save_pdf(file: UploadFile):
    """Saves the uploaded PDF to the uploads directory."""
    file_location = f"{UPLOAD_DIR}{file.filename}"
    
    # Save the file
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    return {"filename": file.filename, "path": file_location}

# Function to process PDF and extract documents
def pdf_to_documents(pdf_file_path):
    loader = PyPDFLoader(pdf_file_path)
    documents = loader.load()
    return [Document(page_content=doc.page_content, metadata={"page_number": idx + 1}) for idx, doc in enumerate(documents)]

# Function to generate embeddings using Hugging Face
def get_embeddings():
    return FastEmbedEmbeddings(model_name="BAAI/bge-base-en-v1.5")

# Function to store document embeddings in ChromaDB
def store_embeddings_in_chroma(documents):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
    texts = text_splitter.split_documents(documents)

    # Generate embeddings
    embeddings = get_embeddings()

    # Store embeddings in ChromaDB
    db = Chroma.from_documents(texts, embeddings, persist_directory="./chroma_db")
    # db.persist()
    
    return db

CHAT_HISTORY_FILE = "chat_history.txt"

def read_chat_history():
    """Reads chat history from a file."""
    try:
        with open(CHAT_HISTORY_FILE, "r", encoding="utf-8") as file:
            data = json.load(file)  # Read full structured JSON data
            return [tuple(entry) for entry in data]  # Convert lists back to tuples
    except (FileNotFoundError, json.JSONDecodeError):
        return []  # Return an empty list if file does not exist or is corrupted


def update_chat_history(user_query, answer):
    chat_history = read_chat_history()

    # Append new entry
    chat_history.append([user_query, answer])

    # Keep only last 3 interactions
    if len(chat_history) > 3:
        chat_history.pop(0)  # Remove the oldest entry

    # Save back to file using JSON to preserve structure
    with open(CHAT_HISTORY_FILE, "w", encoding="utf-8") as file:
        json.dump(chat_history, file, ensure_ascii=False, indent=2)  # Ensure full text is saved



# Function to handle chatbot interaction
def chat_llm(user_query: str):
    # Load the existing Chroma database
    db = Chroma(persist_directory="./chroma_db", embedding_function=get_embeddings())

    # Create a retriever from the vector store
    retriever = db.as_retriever(k=2)

    # Initialize the LLM
    llm = ChatCerebras(
        model="llama-3.3-70b",
        api_key="csk-dvkndyx2p3pw99pnn3jpd4cwf2rxwpnmmdmx5f4vv39rcee5",
        temperature=0.2,
        max_tokens=1500
    )

    # Read existing chat history
    chat_history = read_chat_history()

    # Create memory for conversation history
    # memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
    qa_template = """You are a helpful AI assistant for question-answering tasks. 
    Use the following pieces of retrieved context to answer the question. 
    If you don't know the answer, just say that you don't know. 
    Keep the answer concise and directly related to the context.

    Context:
    {context}

    Chat History:
    {chat_history}

    Question: {question}
    Helpful Answer:"""
    qa_prompt = ChatPromptTemplate.from_template(qa_template)

    # Create the ConversationalRetrievalChain
    qa = ConversationalRetrievalChain.from_llm(
        llm=llm, 
        retriever=retriever, 
        # memory=memory,
        combine_docs_chain_kwargs={"prompt": qa_prompt},
        return_source_documents=True,
        verbose=True  # Optional: for debugging
    )

    # Process the query
    # result = qa({"question": user_query, "chat_history": chat_history})
    result = qa({"question": user_query, "chat_history": chat_history})
    answer = result['answer']
    
    history_text = str(answer)
    # Check if "</think>" exists before splitting
    if "</think>" in history_text:
        history_text = re.split(r"</think>\s*", str(answer))[-1]
        
    print(f"Text history:{history_text}")

    # Update chat history
    update_chat_history(user_query, history_text)

    return {"answer": answer, "chat_history": read_chat_history()}
    
    
    
