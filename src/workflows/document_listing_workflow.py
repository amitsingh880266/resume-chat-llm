from src.models.document import Document
from src.repositories.document_repository import list_documents as repository_list_documents


def list_documents() -> list[Document]:
    return repository_list_documents()