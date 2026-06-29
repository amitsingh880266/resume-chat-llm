from models.chunk import Chunk
import json
from dataclasses import asdict
from pathlib import Path

def _get_document_path(document_id: str) -> Path:
    return Path("storage") / f"{document_id}.json"

def save_chunks(document_id:str, chunks: list[Chunk])-> None:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")
    
    if not chunks:
        raise ValueError("Chunks cannot be empty.")

    storage_directory = Path("storage")
    storage_directory.mkdir(exist_ok=True)

    chunk_file_path = _get_document_path(document_id)

    chunk_list = []

    for chunk in chunks:
        chunk_list.append(asdict(chunk))
    
    with chunk_file_path.open("w", encoding="utf-8") as file:
        json.dump(chunk_list, file, indent=4)

def load_chunks(document_id: str)->list[Chunk]:
    if not document_id.strip():
        raise ValueError("Document ID cannot be empty.")

    document_path = _get_document_path(document_id)

    if not document_path.is_file():
        raise FileNotFoundError("Index file does not exist")
    
    chunk_dict_list = []

    with document_path.open("r") as file:
        chunk_dict_list = json.load(file)
    
    chunk_list = []
    for chunk_dict in chunk_dict_list:
        chunk_list.append(Chunk(**chunk_dict))
    
    return chunk_list

def document_exists(document_id: str) -> bool:
    if not document_id.strip():
        raise ValueError("Document ID cannot empty")

    document_path = _get_document_path(document_id)

    return document_path.is_file()        

