# FastAPI and Gradio App

This project combines a **FastAPI backend** with a **Gradio frontend** to create a web application that allows users to upload PDFs, store their embeddings in ChromaDB, and interact with a chatbot powered by OpenAI's GPT model.

## Features

- **PDF Upload**: Upload multiple PDF files to store their embeddings in ChromaDB.
- **Chatbot Interaction**: Ask questions and get responses from the chatbot based on the uploaded PDFs.
- **FastAPI Backend**: Handles PDF processing, embedding storage, and chatbot responses.
- **Gradio Frontend**: Provides a user-friendly interface for uploading PDFs and chatting with the bot.

## Prerequisites

Before running the project, ensure you have the following installed:

- Python 3.9 or higher
- Docker (optional, for containerized deployment)
- OpenAI API key (stored in a `.env` file)

## Setup

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/your-repo-name.git
cd your-repo-name
