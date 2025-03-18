### RAG Model Implementation

#### Overview

This repository contains an implementation of a Retrieval-Augmented Generation (RAG) Model using LangChain, ChromaDB, and FastAPI. The model allows users to query contract documents by their contract number, retrieving relevant information from stored PDFs and generating responses using an LLM.

#### Features

PDF Processing: Extracts text from PDF documents stored in contract folders.

Chunking & Embedding: Splits extracted text into meaningful chunks and generates embeddings.

Vector Storage: Stores embeddings in ChromaDB for fast retrieval.

Query Handling: Accepts a contract number and retrieves relevant chunks from ChromaDB.

LLM Integration: Uses an LLM (e.g., OpenAI, Mistral, or Llama) to generate responses.

FastAPI & Gradio: Provides a user-friendly web interface to input contract numbers and chat with the RAG model.

Persistence: Saves and loads vector data from an OVHCloud S3 bucket for efficiency.

#### Installation

Prerequisites

Python 3.9+

Docker (optional, for containerized deployment)

OVHCloud storage account (for persistence)

Clone the Repository

git clone https://github.com/your-username/your-repo.git
cd your-repo

Install Dependencies

pip install -r requirements.txt
