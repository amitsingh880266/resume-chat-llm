from pathlib import Path
from uuid import uuid4

from src.models.chunk import Chunk
from src.services.chunk_service import split_into_chunks
from src.services.embedding_service import generate_embedding
from src.services.pdf_service import read_pdf
from src.services.chroma_service import add_chunks
from src.repositories.document_repository import save
from src.models.document import Document, DocumentStatus
import time
from datetime import UTC, datetime
from src.utils.logger import logger

def index_document(
    document_path: Path,
) -> str:
    
    if not document_path.is_file():
        raise FileNotFoundError(f"Document not found: {document_path}")
    
    logger.info("Starting indexing for %s", document_path.name)

    document_id = str(uuid4())

    document_text = read_pdf(document_path)

    chunk_texts = split_into_chunks(document_text)

    logger.info("Generated %s chunks", len(chunk_texts))

    chunks: list[Chunk] = []

    start = time.perf_counter()

    for chunk_text in chunk_texts:
        embedding = generate_embedding(chunk_text)

        chunks.append(
            Chunk(
                text=chunk_text,
                embedding=embedding,
            )
        )
    elapsed_ms = (time.perf_counter() - start) * 1000

    logger.info(
        "Generated %d embeddings in %.2f ms",
        len(chunks),
        elapsed_ms,
    )

    add_chunks(
        document_id=document_id,
        chunks=chunks,
    )

    logger.info("Stored %d chunks", len(chunks))

    save(Document(
        document_id=document_id,
        filename=document_path.name,
        uploaded_at=datetime.now(UTC),
        status= DocumentStatus.READY,
        chunk_count=len(chunk_texts),
    ))

    return document_id