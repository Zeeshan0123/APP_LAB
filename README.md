# FastAPI and Gradio App with LangChain and Llama3-70B

This project combines a **FastAPI backend** with a **Gradio frontend** to create a conversational AI application. It uses **LangChain** for orchestration, **Llama3.3-70B** (via Cerebras API) which provide us the fastest inference in the world as the conversational model, and **ChromaDB** as the vector database for similarity-based search. The application also uses **FlagEmbeddings** for faster embeddings and maintains conversation history for context-aware responses.

## Features

- **PDF Upload**: Upload multiple PDF files to store their embeddings in ChromaDB.
- **Conversational Bot**: Interact with a chatbot powered by the **Llama3-70B** model.
- **Conversation History**: The bot maintains conversation history for context-aware responses.
- **Similarity-Based Search**: Retrieve relevant context from uploaded PDFs using ChromaDB.
- **Prompt Templates**: Ensure the bot answers only from the provided context.
- **FlagEmbeddings**: Use optimized embeddings for faster processing compared to standard Hugging Face embeddings.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- Cerebras API key (if using Llama3-70B via Cerebras)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
