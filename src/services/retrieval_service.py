from models.chunk import Chunk
from utils.similarity_service import cosine_similarity


def retrieve_relevant_chunks(
    chunks: list[Chunk],
    query_embedding: list[float],
    top_k: int = 3,
) -> list[Chunk]:
    scores = []

    for chunk in chunks:
        score = cosine_similarity(
            chunk.embedding,
            query_embedding,
        )

        scores.append((score, chunk))

    scores.sort(
        key=lambda item: item[0],
        reverse=True,
    )

    return [chunk for _, chunk in scores[:top_k]]