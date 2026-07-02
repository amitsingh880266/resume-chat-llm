
from pydantic import BaseModel
from src.api.schemas.document_summary_response import DocumentSummaryResponse

class DocumentListResponse(BaseModel):
    documents: list[DocumentSummaryResponse]