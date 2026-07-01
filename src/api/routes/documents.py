from typing import Annotated
from fastapi import APIRouter, File, UploadFile
from uuid import uuid4
from pathlib import Path
import shutil

from src.api.schemas.document_response import DocumentResponse
from src.workflows.indexing_workflow import index_document

router = APIRouter(
    prefix="/documents",
    tags = ["Documents"]
)


@router.post("")
def upload_document( file: Annotated[UploadFile, File(...)],) -> DocumentResponse:
    
    upload_directory = Path("storage/uploads")
    upload_directory.mkdir(parents=True, exist_ok=True)

    temporary_path = (
        upload_directory /
        f"{uuid4()}{Path(file.filename).suffix}"
    )

    with temporary_path.open('wb') as output_file:
        shutil.copyfileobj(file.file, output_file)

    try:
        document_id = index_document(temporary_path)
    finally:
        temporary_path.unlink()
    return DocumentResponse(document_id=document_id)