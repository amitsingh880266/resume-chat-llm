from src.models.chunk import Chunk

def build_document_prompt (chunks: list[Chunk], question: str) -> str:
    if not chunks:
        raise ValueError("Chunks cannot be empty")
    
    context = "\n\n".join(
        chunk.text for chunk in chunks
    )

    return f"""
    Answer using ONLY the context.
    Reply with words.

    Context:
    {context}

    Question:
    {question}
    """