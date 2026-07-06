from pathlib import Path
import time
import chromadb

from src.models.chunk import Chunk
from src.utils.logger import logger

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
    start = time.perf_counter()
    try:
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

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "add_chunks: stored %d chunks for document_id=%s in %.2f ms",
            len(chunks),
            document_id,
            elapsed_ms,
        )
    except Exception:
        logger.exception("add_chunks: failed to add chunks for %s", document_id)
        raise


def query_chunks(
    document_id: str,
    query_embedding: list[float],
    top_k: int = 3,
) -> list[Chunk]:
    start = time.perf_counter()
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

    elapsed_ms = (time.perf_counter() - start) * 1000
    logger.info(
        "query_chunks: returned %d results for document_id=%s in %.2f ms",
        len(chunks),
        document_id,
        elapsed_ms,
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

    exists = len(results["ids"]) > 0
    logger.debug("document_exists: document_id=%s exists=%s", document_id, exists)
    return exists


def delete_document(
    document_id: str,
) -> None:
    start = time.perf_counter()
    try:
        if not document_id.strip():
            raise ValueError("Document ID cannot be empty.")

        collection = _get_collection()

        collection.delete(
            where={
                "document_id": document_id,
            }
        )

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("delete_document: deleted document_id=%s in %.2f ms", document_id, elapsed_ms)
    except Exception:
        logger.exception("delete_document: failed to delete %s", document_id)
        raise