# Product Roadmap — Document Chat LLM

**Start date:** 2 July 2026  
**Duration:** 4 sprints × 2 weeks = 8 weeks  
**Goal:** Evolve from a resume-chat demo into a market-fit document intelligence platform for large enterprises managing complex manuals, SOPs, and technical documentation.

---

## Current State Snapshot

What's working well:

- Full RAG pipeline: PDF → text → chunks → embeddings → ChromaDB → retrieval
- FastAPI backend with document upload, listing, and question routes
- SQLite for document metadata tracking
- Local sentence-transformer embeddings (no API cost per query)

What's broken or incomplete:

- `llm_service.py` has inverted logic — `can_call_openai=True` skips the LLM call instead of making one
- `ask_llm()` uses the deprecated `client.responses.create()` instead of `client.chat.completions.create()`
- `answer_question()` workflow has the LLM call commented out — returns the raw prompt instead of an answer
- Default model is `"gpt-5.5"` which does not exist
- No source citations — the user cannot see which part of the document was used to answer
- Chunking is purely character-based; it splits mid-sentence and loses context

---

## Why This Can Become Market-Fit for Enterprises

Large companies (manufacturing, healthcare, finance, legal, engineering) have:

- Thousands of SOPs, compliance docs, technical manuals, runbooks
- Teams that waste hours searching for answers that already exist in documents
- New employees who need to ramp up on complex institutional knowledge
- Audit requirements — every answer must be traceable back to a source

A RAG-based document chat tool directly solves this. The architecture already exists in this project. The next 8 weeks will close the gap between "learning project" and "production-ready product."

---

## Sprint 1 — 2 July to 15 July 2026

### Theme: Make the Core Work, Understand Every Layer

**Learning goal:** Truly understand the full RAG loop by fixing it and watching it work end-to-end. Before adding anything new, you need confidence that the foundation is solid.

---

### 1.1 Fix the Broken LLM Integration

This is the most important task. Right now the system can retrieve relevant chunks but never actually asks the LLM anything.

**Tasks:**

- Fix the inverted `if/else` in `llm_service.py`
- Switch from `client.responses.create()` to `client.chat.completions.create()`
- Change the default model to `"gpt-4o-mini"` (cheap, fast, good enough for development)
- Uncomment `answer = ask_llm(prompt)` in `question_answering_workflow.py`
- Set `can_call_openai=true` in your `.env` and ask a real question

**Why this matters:** You cannot improve what you cannot run. Every future improvement depends on seeing real LLM responses.

**Learning checkpoint:** After this task, you should be able to explain what happens at each step when you POST to `/questions`. Draw the flow on paper before writing any code.

---

### 1.2 Add Source Citations to Every Answer

Right now the answer comes back with no reference to where the information came from. Enterprise users will never trust a system that cannot prove its sources.

**Tasks:**

- Modify `query_chunks()` in `chroma_service.py` to also return the source text alongside each chunk
- Update `QuestionResponse` schema to include a `sources: list[str]` field (the actual chunk texts used)
- Update the prompt template in `prompt_service.py` to number each context chunk (Context 1, Context 2, Context 3) and instruct the LLM to cite them in the answer
- Return sources in the API response

**Why this matters:** Traceability is a legal and compliance requirement in most enterprise environments. An answer without a source is a liability.

**Learning checkpoint:** Look up what "grounding" means in the context of LLMs. Understand the difference between a hallucination and a grounded response.

---

### 1.3 Replace Character Chunking with Sentence-Aware Chunking

The current chunker splits every 500 characters regardless of sentence boundaries. A chunk might end mid-sentence: `"...the torque spec for bolt`" — this breaks the semantic meaning and confuses the LLM.

**Tasks:**

- Install `nltk` and use `sent_tokenize()` to split text into sentences first
- Build chunks by accumulating sentences until the chunk reaches the target size (e.g. 400 tokens)
- Keep the overlap logic but overlap at sentence boundaries, not character positions
- Add a `chunk_index` and `total_chunks` field to the `Chunk` model for debugging
- Write a small test: index a short PDF and print all chunks — verify none cut mid-sentence

**Why this matters:** Chunk quality directly affects retrieval quality. Better chunks = more relevant retrieved context = better answers. This is one of the highest-leverage improvements in any RAG system.

**Learning checkpoint:** Read about why token-based splitting is preferred over character-based in production RAG systems.

---

### 1.4 Structured Logging

Replace all `print()` statements with Python's `logging` module. Every service should log what it receives, what it returns, and how long it took.

**Tasks:**

- Create `src/utils/logger.py` — a single place to configure and export a logger
- Add log statements at each workflow step: "Starting indexing for {filename}", "Generated {n} chunks", "Query returned {k} results", "LLM responded in {ms}ms"
- Log errors with full stack traces using `logger.exception()`

**Why this matters:** In a real company, you can only debug production issues if you have logs. This is a non-negotiable engineering practice.

---

### Sprint 1 Deliverable

Demo: Upload a technical PDF (a product manual, a policy document, anything complex). Ask three questions. The API returns a real answer with numbered source citations. All steps are visible in logs.

---

## Sprint 2 — 16 July to 29 July 2026

### Theme: Handle the Real World — More Document Types, Async Processing, Multi-Document Search

**Learning goal:** Understand that production systems must handle inputs you don't control — different file formats, large files that take time to process, and queries that span multiple documents.

---

### 2.1 Support Word Documents and Plain Text

Most enterprise documents are not PDFs. Operations teams write in Word (.docx). Developers write in Markdown. Policies come as plain text files.

**Tasks:**

- Install `python-docx` and create `src/services/docx_service.py` with a `read_docx(path)` function
- Update `indexing_workflow.py` to detect file extension and call the right parser
- Support `.txt` files with a simple `read_text(path)` function
- Add file type validation in the upload route — reject unsupported formats with a clear 422 error message

**Why this matters:** Your target customers have document libraries in mixed formats. If you only handle PDFs you lose 60% of their use cases immediately.

**Learning checkpoint:** Look up what "MIME type" is and why validating file extension alone is not sufficient security.

---

### 2.2 Async Document Indexing with Status Tracking

Right now, uploading a large PDF blocks the HTTP request until the entire indexing pipeline finishes. For a 200-page technical manual this could take 30–60 seconds, and the request would time out.

**Tasks:**

- Use FastAPI's `BackgroundTasks` to run `index_document()` after the HTTP response returns
- When upload starts, immediately save the document to SQLite with `status=INDEXING` and return the `document_id` to the caller
- Update status to `READY` when indexing completes, or `FAILED` if an exception occurs (with error message stored)
- Add a `GET /documents/{document_id}` route that returns the current status
- Add a `GET /documents/{document_id}/status` route for polling

**Why this matters:** This is the difference between a toy app and a real backend. Users should never wait for a background job — they should get an immediate response and poll for completion.

**Learning checkpoint:** Understand what an async task queue is and why FastAPI's `BackgroundTasks` is good for simple cases but not for production (hint: look up Celery and why it exists).

---

### 2.3 Cross-Document Querying

Right now every question is scoped to a single `document_id`. Enterprise users want to ask: "What does our safety manual say about this?" without knowing which specific document contains the answer.

**Tasks:**

- Add an optional `document_id` field to `QuestionRequest` — if omitted, search across all documents
- When `document_id` is None, query all ChromaDB collections or use a single shared collection with document metadata filtering
- Return the `document_id` and `filename` in each source citation so the user knows which document the answer came from
- Update the prompt to include document names alongside chunk text: "From [Employee Handbook v2]: ..."

**Why this matters:** This changes the product from "chat with one file" to "chat with your entire knowledge base" — that is the actual value proposition for enterprise customers.

**Learning checkpoint:** Understand the difference between a ChromaDB collection-per-document vs. a single collection with metadata filtering. Think about which scales better.

---

### 2.4 Delete Document (Full Cleanup)

The `document_repository.py` has a `delete()` function but there is no API route for it, and it does not clean up ChromaDB.

**Tasks:**

- Add `DELETE /documents/{document_id}` route
- Delete from SQLite via the repository
- Delete all chunks from ChromaDB using `chroma_service.delete_document()`
- Return 404 if the document does not exist
- Return 409 if the document is currently in `INDEXING` status

**Why this matters:** Data hygiene is critical in enterprise environments. Outdated documents should be removable without leaving ghost vectors polluting search results.

---

### Sprint 2 Deliverable

Demo: Upload a Word doc and a PDF with related content. Ask a question without specifying a document ID. The system searches both documents and returns an answer citing which document it came from. Upload a large file and immediately get a `document_id` back — poll the status endpoint to watch it go from `INDEXING` to `READY`.

---

## Sprint 3 — 30 July to 12 August 2026

### Theme: Better Retrieval, Conversation Memory, Answer Quality

**Learning goal:** RAG quality is not just about the LLM — 80% of failures come from poor retrieval. This sprint is about learning what "good retrieval" means and how to measure it.

---

### 3.1 Hybrid Search: BM25 + Semantic

Semantic search (embedding-based) is great at finding conceptually related content. But it fails on exact terms like part numbers, error codes, and technical identifiers (e.g. "Error E-2047", "Valve assembly P/N 884-C"). BM25 (keyword search) handles these perfectly.

**Tasks:**

- Install `rank-bm25`
- Create `src/services/bm25_service.py` that indexes chunks using BM25 and supports keyword-based retrieval
- Persist the BM25 index alongside the document (use Python's `pickle` or `json` for now)
- In `question_answering_workflow.py`, run both semantic search and BM25 in parallel
- Merge and deduplicate results, take top-5 combined
- Basic fusion: score both lists and use Reciprocal Rank Fusion (RRF) to combine scores

**Why this matters:** Semantic search alone fails on exact identifiers. Most enterprise documents are full of part numbers, error codes, and references. Hybrid search is now the industry standard for production RAG.

**Learning checkpoint:** Understand what TF-IDF is. BM25 is an improvement on TF-IDF — read why. Then understand why neither can replace semantic search for conceptual questions.

---

### 3.2 Multi-Turn Conversation (Session Memory)

Right now every question is stateless. Users cannot say "explain that in simpler terms" or "give me more detail about the second point." This makes the tool feel robotic.

**Tasks:**

- Create a `Conversation` model with `session_id`, `document_id`, `messages: list[Message]`, and `created_at`
- Store conversations in SQLite (new `conversations` and `messages` tables)
- Add `session_id` (optional) to `QuestionRequest`
- If `session_id` is provided, fetch the last 5 message pairs and include them in the LLM prompt as conversation history
- Add `POST /sessions` to create a session and `GET /sessions/{session_id}` to retrieve history

**Why this matters:** Conversation memory is what separates a search engine from an assistant. Follow-up questions and clarifications dramatically improve the user experience, especially for complex technical content.

**Learning checkpoint:** Understand the LLM context window. Why can't you just keep passing the full conversation history forever? Research "context window management" strategies.

---

### 3.3 Retrieval Quality Evaluation

You cannot improve what you cannot measure. This task introduces evaluation as a discipline.

**Tasks:**

- Create `src/utils/evaluator.py` with a simple function that takes a question, the retrieved chunks, and the expected answer source, and scores whether the right chunk was retrieved
- Write a test dataset: 10 question-answer pairs from one of your indexed documents (manually written)
- Script that runs all 10 questions, measures: "Was the correct chunk in the top-3 results?" (this is called Recall@3 or Hit Rate)
- Log the score after every significant change to chunking or retrieval logic
- Add a `GET /eval/quick` endpoint that runs the test suite and returns the score

**Why this matters:** In every real AI project, if you don't build evaluation infrastructure early, you end up making changes blindly. This is how teams accidentally make their product worse while thinking they improved it.

**Learning checkpoint:** Look up "RAG evaluation frameworks" — specifically RAGAS. You don't need to implement it now, but understand what metrics it measures (faithfulness, answer relevance, context recall).

---

### 3.4 Document Re-indexing

When a document is updated (a new version of the SOP is published), users need to re-index it without deleting and re-uploading manually.

**Tasks:**

- Add `POST /documents/{document_id}/reindex` route
- Route accepts a new file upload, deletes old chunks from ChromaDB, and runs the full indexing pipeline with the same `document_id`
- Update `uploaded_at`, `chunk_count`, and `status` in SQLite
- Increment a `version` counter in the document model

**Why this matters:** Enterprise documents change. SOPs are revised, manuals are updated. A platform that cannot handle document updates is not useful in practice.

---

### Sprint 3 Deliverable

Demo: Have a multi-turn conversation about a technical document. Ask a follow-up question that references the previous answer. Search for a specific error code that semantic search alone would miss. Show the evaluation score before and after enabling hybrid search.

---

## Sprint 4 — 13 August to 26 August 2026

### Theme: Enterprise Readiness — Security, Observability, Deployment

**Learning goal:** Understand what separates a working prototype from a product a real company can trust. Learn about authentication, access control, containerization, and monitoring.

---

### 4.1 API Key Authentication

Right now, anyone who can reach the server can upload documents and ask questions. That is unacceptable for enterprise use.

**Tasks:**

- Create an `api_keys` table in SQLite with `key_hash`, `name`, `created_at`, `is_active`
- Store keys as bcrypt hashes — never store raw keys
- Create a FastAPI dependency `verify_api_key(request)` that reads the `X-API-Key` header and validates it against the database
- Apply the dependency to all routes except `GET /health`
- Add a management script `scripts/create_api_key.py` that generates a key, hashes it, stores it, and prints the raw key once
- Return `401 Unauthorized` for missing or invalid keys, `403 Forbidden` for inactive keys

**Why this matters:** Authentication is the first security control in any enterprise product. Without it, your document system is a data leak waiting to happen. This also introduces you to hashing, which is a foundational security concept.

**Learning checkpoint:** Understand why you should never store passwords or API keys in plaintext. Learn what a hash function is, what salting means, and why bcrypt is preferred over SHA-256 for secrets.

---

### 4.2 Request Tracing with Correlation IDs

When a request fails in production, you need to trace it through every service. Correlation IDs are the standard mechanism for this.

**Tasks:**

- Create a FastAPI middleware `src/api/middleware/tracing.py`
- For every request: if `X-Request-ID` header is present use it, otherwise generate a UUID
- Store the request ID in a context variable (Python's `contextvars.ContextVar`)
- Update the logger to include the request ID in every log line
- Return the `X-Request-ID` in every response header

**Why this matters:** In a microservices environment, a single user action creates dozens of log lines across many services. Without a correlation ID, debugging is nearly impossible. This is standard practice in every enterprise backend.

**Learning checkpoint:** Look up OpenTelemetry — the requirements.txt already includes it. Understand what distributed tracing is and how it builds on the correlation ID concept.

---

### 4.3 Rate Limiting

Without rate limiting, a single client can overload your server or rack up massive OpenAI API bills.

**Tasks:**

- Install `slowapi`
- Add rate limits per API key: 10 questions per minute, 50 document uploads per hour
- Return `429 Too Many Requests` with a `Retry-After` header when limits are exceeded
- Exempt the `/health` route from rate limiting

**Why this matters:** Rate limiting protects both your infrastructure and your API costs. It is a basic security control that prevents abuse, whether accidental or intentional.

---

### 4.4 Docker Containerization

A product that only works on the developer's machine is not a product.

**Tasks:**

- Write a `Dockerfile` using a Python 3.12 slim base image
- Use multi-stage build: first stage installs dependencies, second stage copies only what's needed
- Write a `docker-compose.yml` with the app service and volume mounts for `storage/`
- Add a `.dockerignore` file to exclude `source/`, `__pycache__/`, `.env`, `resumes/`
- Document how to build and run in `readme.md`
- Verify the full flow works inside Docker: upload → index → question → answer

**Why this matters:** Containerization is the baseline deployment requirement for every enterprise software product today. This also teaches you about environment isolation, which is why "works on my machine" problems exist.

**Learning checkpoint:** Understand what Docker layers are and why their order in a Dockerfile matters for build speed. Understand why secrets (`.env`) must never be baked into a Docker image.

---

### 4.5 README and API Documentation Overhaul

A product without documentation does not get adopted.

**Tasks:**

- Rewrite `readme.md` with: project description, architecture diagram (text-based), setup instructions, environment variables reference, API endpoint reference with example curl commands
- Add docstrings to all workflow functions and service functions
- FastAPI auto-generates OpenAPI docs at `/docs` — verify every endpoint has a description, all request/response schemas are documented, and example values are provided

**Why this matters:** Your first enterprise customer will evaluate your product by reading the documentation before ever running it.

---

### Sprint 4 Deliverable

Demo: Run the entire application in Docker. Make an authenticated API call with an API key. Trigger rate limiting and show the 429 response. Show the correlation ID flowing through logs. Show the `/docs` UI with full documentation.

---

## Architecture Evolution Map

```
Current State (July 2)
───────────────────────────────────────────────
PDF only → basic chunks → local embeddings →
ChromaDB → broken LLM call → returns prompt

After Sprint 1 (July 15)
───────────────────────────────────────────────
PDF → sentence-aware chunks → local embeddings →
ChromaDB → working GPT call → answer + citations

After Sprint 2 (July 29)
───────────────────────────────────────────────
PDF + DOCX + TXT → async indexing → status tracking
→ cross-document semantic search → GPT → answer
citing source documents

After Sprint 3 (August 12)
───────────────────────────────────────────────
Any doc → async pipeline → hybrid search (BM25 + semantic)
→ conversation history → GPT → grounded answer
with evaluation score tracking

After Sprint 4 (August 26)
───────────────────────────────────────────────
Authenticated API → rate limited → traced requests
→ full hybrid RAG → containerized deployment
→ production-grade documentation
```

---

## Skills You Will Have Built by August 26

| Skill                                           | Where You Learn It                            |
| ----------------------------------------------- | --------------------------------------------- |
| How RAG actually works end-to-end               | Sprint 1.1 — fixing and running the full loop |
| Why retrieval quality matters more than the LLM | Sprint 3.1 — hybrid search                    |
| How to evaluate AI systems                      | Sprint 3.3 — building your own eval harness   |
| Async backend patterns                          | Sprint 2.2 — background tasks                 |
| API security fundamentals                       | Sprint 4.1 — API key authentication           |
| Observability in distributed systems            | Sprint 4.2 — correlation IDs                  |
| Container-based deployment                      | Sprint 4.4 — Docker                           |
| Multi-turn LLM conversations                    | Sprint 3.2 — session memory                   |
| NLP text processing                             | Sprint 1.3 — sentence-aware chunking          |
| Data schema design                              | Sprint 3.2 — conversations table              |

---

## What This Product Could Become

After these 8 weeks the architecture directly supports:

- **Manufacturing companies** — index equipment manuals, surface relevant maintenance procedures when a technician describes a symptom
- **Healthcare providers** — index clinical protocols, answer nurse/doctor questions with source citations for audit trails
- **Financial firms** — index compliance documents, answer queries about regulatory requirements with exact policy references
- **Law firms** — index case files and contracts, retrieve relevant clauses for a given legal question
- **SRE/DevOps teams** — index runbooks, get step-by-step troubleshooting answers during incidents

The next evolution after Sprint 4 would be: multi-tenant workspace isolation, SSO/SAML authentication, fine-grained document permissions, and a React/Next.js frontend — but that is a story for a future roadmap.
