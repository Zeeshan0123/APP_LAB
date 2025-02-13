import gradio as gr
import requests
import os

# FastAPI backend URL
FASTAPI_URL = "http://127.0.0.1:4100"  # Replace with your FastAPI server URL

# Function to handle PDF uploads
def upload_pdfs(files):
    file_paths = [file.name for file in files]
    response = requests.post(
        f"{FASTAPI_URL}/upload-pdfs/",
        files=[("files", open(file, "rb")) for file in file_paths]
    )
    if response.status_code == 200:
        return f"Files uploaded successfully: {response.json()['files']}"
    else:
        return f"Error uploading files: {response.text}"

# Function to handle chatbot interaction
def chat_with_llm(user_query):
    response = requests.post(
        f"{FASTAPI_URL}/submit",
        json={"user_query": user_query}
    )
    if response.status_code == 200:
        result = response.json()
        return result['answer']
    else:
        return f"Error in chatbot response: {response.text}"

# Gradio interface for PDF upload
pdf_upload_interface = gr.Interface(
    fn=upload_pdfs,
    inputs=gr.File(file_count="multiple", label="Upload PDFs"),
    outputs=gr.Textbox(label="Upload Status"),
    title="Upload PDFs to ChromaDB",
    description="Upload multiple PDF files to store their embeddings in ChromaDB.",
    theme=gr.themes.Soft()
)

# Gradio interface for chatbot interaction
chat_interface = gr.Interface(
    fn=chat_with_llm,
    inputs=gr.Textbox(label="Your Query"),
    outputs=gr.Textbox(label="Chatbot Response"),
    title="Chat with LLM",
    description="Ask questions and get responses from the chatbot.",
    theme=gr.themes.Soft()
)

# Combine both interfaces into a single Gradio app
app = gr.TabbedInterface(
    [pdf_upload_interface, chat_interface],
    ["Upload PDFs", "Chat with LLM"]
)

# Launch the Gradio app
if __name__ == "__main__":
    app.launch()