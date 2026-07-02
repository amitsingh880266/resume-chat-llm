from datetime import datetime

from pydantic import BaseModel


class DocumentSummaryResponse(BaseModel):
    document_id: str
    filename: str
    uploaded_at: datetime
    status: str
    chunk_count: int

