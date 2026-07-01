# Resume Chat LLM

A Python project to learn and implement **Retrieval-Augmented Generation (RAG)** from first principles without relying on high-level frameworks.

## Overview

This project started as a simple application that sent an entire resume to an LLM and returned an answer.

It has gradually evolved into a full RAG application with a FastAPI backend:

- PDF parsing and text cleaning
- Document chunking
- Local embedding generation (sentence-transformers)
- ChromaDB vector storage and retrieval
- Workflow-oriented architecture
- GPT-powered question answering using retrieved context
- REST API for document upload and question answering

The goal is to understand how RAG systems work internally before introducing orchestration frameworks.

---

## Project Structure

```text
src/
├── config.py
├── main.py                  # CLI entrypoint
├── openai_client.py
├── api/
│   ├── app.py               # FastAPI app
│   ├── router.py
│   └── routes/
│       ├── health.py        # GET /health
│       ├── documents.py     # POST /documents
│       └── questions.py     # POST /questions
├── models/
├── services/
│   ├── chroma_service.py
│   ├── chunk_service.py
│   ├── embedding_service.py
│   ├── llm_service.py
│   ├── pdf_service.py
│   ├── prompt_service.py
│   └── text_cleaning_service.py
└── workflows/
    ├── indexing_workflow.py
    └── question_answering_workflow.py

resumes/
storage/
├── chroma/
└── uploads/
```

---

## Prerequisites

- Python 3.14+
- OpenAI API Key

Create a `.env` file:

```env
OPENAI_API_KEY=your_api_key
SEND_TO_OPENAI=True
OPENAI_MODEL=gpt-4o
```

---

## Installation

```bash
python3 -m venv .venv
source .venv/bin/activate

pip install -r requirements.txt
```

---

## Run

### FastAPI Server

Start the API server from the project root:

```bash
uvicorn src.api.app:app --reload
```

The API will be available at `http://localhost:8000`.

Interactive docs (Swagger UI): `http://localhost:8000/docs`

#### Endpoints

| Method | Path         | Description                              |
| ------ | ------------ | ---------------------------------------- |
| `GET`  | `/health`    | Health check                             |
| `POST` | `/documents` | Upload and index a PDF                   |
| `POST` | `/questions` | Ask a question about an indexed document |

#### Upload a document

```bash
curl -X POST http://localhost:8000/documents \
  -F "file=@resumes/resume.pdf"
```

Returns a `document_id` to use when asking questions.

#### Ask a question

```bash
curl -X POST http://localhost:8000/questions \
  -H "Content-Type: application/json" \
  -d '{"document_id": "<document_id>", "question": "Can this candidate fit a full stack developer role?"}'
```

---

### CLI (alternative)

From the project root:

```bash
python src/main.py --question "Can this candidate fit a full stack developer role?"
```

The CLI uses a hardcoded `document_id` of `amit_resume` and expects a resume at `resumes/resume.pdf`. It indexes the document on first run and reuses the existing index on subsequent runs.

---

## Architecture

```text
PDF Upload
    │
    ▼
Indexing Workflow
    │  ├── PDF parsing
    │  ├── Text cleaning
    │  ├── Chunking
    │  └── Embedding + ChromaDB storage
    ▼
ChromaDB

Question (via API or CLI)
    │
    ▼
Question Answering Workflow
    │  ├── Embed question
    │  ├── Semantic retrieval from ChromaDB
    │  └── GPT response with retrieved context
    ▼
Answer
```

---

## Learning Progress

- ✅ OpenAI Responses API
- ✅ Project refactoring into services and workflows
- ✅ PDF parsing
- ✅ Prompt engineering
- ✅ Local embeddings (sentence-transformers)
- ✅ Semantic search
- ✅ Retrieval-Augmented Generation (RAG)
- ✅ ChromaDB vector storage
- ✅ CLI-based question input using `argparse`
- ✅ FastAPI backend with document upload and question answering

---

## Next Steps

- Improve chunking strategy with chunk overlap
- Add a React frontend
