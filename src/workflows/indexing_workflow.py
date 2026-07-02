from pathlib import Path
from uuid import uuid4

from src.models.chunk import Chunk
from src.services.chunk_service import split_into_chunks
from src.services.embedding_service import generate_embedding
from src.services.pdf_service import read_pdf
from src.services.chroma_service import add_chunks
from src.repositories.document_repository import save
from src.models.document import Document, DocumentStatus
from datetime import UTC, datetime

def index_document(
    document_path: Path,
) -> str:
    
    if not document_path.is_file():
        raise FileNotFoundError(f"Document not found: {document_path}")
    
    document_id = str(uuid4())

    document_text = read_pdf(document_path)

    chunk_texts = split_into_chunks(document_text)

    chunks: list[Chunk] = []

    for chunk_text in chunk_texts:
        embedding = generate_embedding(chunk_text)

        chunks.append(
            Chunk(
                text=chunk_text,
                embedding=embedding,
            )
        )

    add_chunks(
        document_id=document_id,
        chunks=chunks,
    )

    save(Document(
        document_id=document_id,
        filename=document_path.name,
        uploaded_at=datetime.now(UTC),
        status= DocumentStatus.READY,
        chunk_count=len(chunk_texts),
    ))

    return document_id