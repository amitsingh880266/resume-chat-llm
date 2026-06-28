Resume Chat LLM

A Python project to learn and implement Retrieval-Augmented Generation (RAG) from first principles without relying on high-level frameworks.

Overview

This project started as a simple application that sent an entire resume to an LLM and returned an answer.

It has gradually evolved into a structured RAG application with:

PDF parsing

Document chunking

Local embedding generation

Cosine similarity implementation

Semantic retrieval

JSON-based document indexing

Workflow-oriented architecture

GPT-powered question answering using retrieved context

The goal is to understand how RAG systems work internally before introducing vector databases and orchestration frameworks.

Project Structure

src/
├── config.py
├── models/
├── services/
├── workflows/
└── main.py

resumes/
storage/

Prerequisites

Python 3.14+

OpenAI API Key

Create a .env file:

OPENAI_API_KEY=your_api_key
SEND_TO_OPENAI=True

Installation

python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt

Run

From the project root:

python src/main.py

Current Architecture

Document
│
▼
Indexing Workflow
│
▼
JSON Storage
│
▼
Question Answering Workflow
│
▼
Semantic Retrieval
│
▼
GPT Response

Learning Progress

✅ OpenAI Responses API

✅ Project refactoring into services and workflows

✅ PDF parsing

✅ Prompt engineering

✅ Local embeddings

✅ Custom cosine similarity

✅ Semantic search

✅ Retrieval-Augmented Generation (RAG)

✅ Persistent document indexing (JSON)

Next Steps

Improve chunking strategy

Add chunk overlap

Replace JSON storage with a vector database

Build a FastAPI backend

Add a React frontend
