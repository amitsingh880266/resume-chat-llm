from pathlib import Path

import chromadb

from models.chunk import Chunk

PROJECT_ROOT = Path(__file__).resolve().parents[2]

chroma_client = chromadb.PersistentClient(
    path=str(PROJECT_ROOT / "storage" / "chroma")
)


def _get_collection():
    return chroma_client.get_or_create_collection(
        name="documents"
    )


def add_chunks(
    document_id: str,
    chunks: list[Chunk],
) -> None:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    if not chunks:
        raise ValueError("Chunks cannot be empty.")

    collection = _get_collection()

    ids: list[str] = []
    documents: list[str] = []
    embeddings: list[list[float]] = []
    metadatas: list[dict] = []

    for index, chunk in enumerate(chunks):
        ids.append(f"{document_id}_{index}")
        documents.append(chunk.text)
        embeddings.append(chunk.embedding)
        metadatas.append(
            {
                "document_id": document_id,
            }
        )

    collection.add(
        ids=ids,
        documents=documents,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_chunks(
    document_id: str,
    query_embedding: list[float],
    top_k: int = 3,
) -> list[Chunk]:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    if not query_embedding:
        raise ValueError("Query embedding cannot be empty.")

    collection = _get_collection()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
        where={"document_id": document_id},
        include=[
            "documents",
            "embeddings",
        ],
    )

    documents = results["documents"][0]
    embeddings = results["embeddings"][0]

    chunks: list[Chunk] = []

    for text, embedding in zip(documents, embeddings):
        chunks.append(
            Chunk(
                text=text,
                embedding=embedding,
            )
        )

    return chunks


def document_exists(
    document_id: str,
) -> bool:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    collection = _get_collection()

    results = collection.get(
        where={"document_id": document_id},
    )

    return len(results["ids"]) > 0


def delete_document(
    document_id: str,
) -> None:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    collection = _get_collection()

    collection.delete(
        where={
            "document_id": document_id,
        }
    )