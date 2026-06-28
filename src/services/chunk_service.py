def split_into_chunks(text:str, chunk_size: int = 500) -> list[str]:
    chunks = []

    for start in range(0, len(text), chunk_size):
        chunk = text[start:start + chunk_size]
        chunks.append(chunk)
        
    return chunks