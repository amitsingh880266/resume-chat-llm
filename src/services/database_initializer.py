from src.services.database_service import get_connection

def initialize_database() -> None:
    with get_connection() as connection:
        connection.execute(
            """
            CREATE TABLE IF NOT EXISTS documents (
                document_id TEXT PRIMARY KEY,
                filename TEXT NOT NULL,
                uploaded_at TIMESTAMP,
                status TEXT NOT NULL,
                chunk_count INTEGER NOT NULL
            )
            """
        )