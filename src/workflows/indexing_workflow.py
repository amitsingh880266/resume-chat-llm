from pathlib import Path

from models.chunk import Chunk
from services.chunk_service import split_into_chunks
from services.embedding_service import generate_embedding
from services.pdf_service import read_pdf
from services.storage_service import save_chunks


def index_document(
    document_id: str,
    document_path: Path,
) -> None:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    document_text = read_pdf(document_path)

    chunk_texts = split_into_chunks(document_text)

    chunks: list[Chunk] = []

    for chunk in chunk_texts:
        embedding = generate_embedding(chunk)

        chunks.append(
            Chunk(
                text=chunk,
                embedding=embedding,
            )
        )

    save_chunks(
        document_id=document_id,
        chunks=chunks,
    )