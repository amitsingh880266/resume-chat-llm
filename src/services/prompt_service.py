from src.models.chunk import Chunk


def build_document_prompt(chunks: list[Chunk], question: str) -> str:
    if not chunks:
        raise ValueError("Chunks cannot be empty")

    context = "\n\n".join(
        f"Context {index}:\n{chunk.text}"
        for index, chunk in enumerate(chunks, start=1)
    )

    return f"""
    You are a helpful AI assistant.

    Answer the question using ONLY the provided context.

    Whenever you use information from a context section, cite it using
    [Context X], where X is the context number.

    If the answer cannot be determined from the provided context, say:
    "I couldn't find the answer in the provided documents."

    {context}

    Question:
    {question}

    Answer:
    """