from dataclasses import dataclass
from datetime import datetime
from enum import Enum


class DocumentStatus(Enum):
    INDEXING = "indexing"
    READY = "ready"
    FAILED = "failed"


@dataclass
class Document:
    document_id: str
    filename: str
    uploaded_at: datetime
    status: DocumentStatus
    chunk_count: int