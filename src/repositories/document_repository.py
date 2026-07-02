from src.models.document import Document, DocumentStatus
from datetime import datetime

from src.services.database_service import get_connection

def save(document: Document) -> None:
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

def get(document_id: str) -> Document | None:
    # Implement the logic to retrieve the document from the database
    pass

def list_documents() -> list[Document]:
   with get_connection() as connection:
        cursor = connection.execute(
            """
            SELECT document_id, filename, uploaded_at, status, chunk_count
            FROM documents
            """
        )
        rows = cursor.fetchall()  
        documents = []
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
        return documents

def delete(document_id: str) -> None:
    # Implement the logic to delete the document from the database
    pass