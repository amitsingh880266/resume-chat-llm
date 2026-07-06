from src.models.document import Document, DocumentStatus
from datetime import datetime

from src.services.database_service import get_connection
from src.utils.logger import logger
import time

def save(document: Document) -> None:
    start = time.perf_counter()
    try:
        with get_connection() as connection:
            connection.execute(
                """
                INSERT INTO documents (
                    document_id,
                    filename,
                    uploaded_at,
                    status,
                    chunk_count
                )
                VALUES (?, ?, ?, ?, ?)
                """,
                (
                    document.document_id,
                    document.filename,
                    document.uploaded_at.isoformat(),
                    document.status.value,
                    document.chunk_count,
                ),
            )

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "save: persisted document_id=%s filename=%s chunk_count=%d in %.2f ms",
            document.document_id,
            document.filename,
            document.chunk_count,
            elapsed_ms,
        )
    except Exception:
        logger.exception("save: failed to persist document %s", document.document_id)
        raise

def get(document_id: str) -> Document | None:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT document_id, filename, uploaded_at, status, chunk_count
                FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            )
            row = cursor.fetchone()
            if row:
                doc = Document(
                    document_id=row[0],
                    filename=row[1],
                    uploaded_at=datetime.fromisoformat(row[2]),
                    status=DocumentStatus(row[3]),
                    chunk_count=row[4],
                )
                logger.debug("get: found document_id=%s filename=%s", doc.document_id, doc.filename)
                return doc
            logger.debug("get: document_id=%s not found", document_id)
            return None
    except Exception:
        logger.exception("get: failed to retrieve document %s", document_id)
        raise


def list_documents() -> list[Document]:
    try:
        with get_connection() as connection:
            cursor = connection.execute(
                """
                SELECT document_id, filename, uploaded_at, status, chunk_count
                FROM documents
                """
            )
            rows = cursor.fetchall()

            documents: list[Document] = []
            for row in rows:
                documents.append(
                    Document(
                        document_id=row[0],
                        filename=row[1],
                        uploaded_at=datetime.fromisoformat(row[2]),
                        status=DocumentStatus(row[3]),
                        chunk_count=row[4],
                    )
                )

            logger.debug("list_documents: returned %d documents", len(documents))
            return documents
    except Exception:
        logger.exception("list_documents: failed to list documents")
        raise

def delete(document_id: str) -> None:
    document = get(document_id)
    if not document:
        raise ValueError(f"Document with ID {document_id} does not exist.")
    start = time.perf_counter()
    try:
        with get_connection() as connection:
            connection.execute(
                """
                DELETE FROM documents
                WHERE document_id = ?
                """,
                (document_id,),
            )

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info("delete: removed document_id=%s in %.2f ms", document_id, elapsed_ms)
    except Exception:
        logger.exception("delete: failed to remove document %s", document_id)
        raise

    
