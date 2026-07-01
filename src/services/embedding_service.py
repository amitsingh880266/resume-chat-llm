from sentence_transformers import SentenceTransformer
from src.config import settings

_model = SentenceTransformer(settings.embedding_model)

def generate_embedding(text: str) -> list[float]:
    embedding = _model.encode(text)
    return embedding.tolist()