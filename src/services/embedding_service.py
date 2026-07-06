import time
from sentence_transformers import SentenceTransformer
from src.config import settings
from src.utils.logger import logger

_model = SentenceTransformer(settings.embedding_model)
logger.info("Loaded embedding model %s", settings.embedding_model)


def generate_embedding(text: str) -> list[float]:
    start = time.perf_counter()
    try:
        embedding = _model.encode(text)
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.debug(
            "generate_embedding: encoded text length=%d in %.2f ms",
            len(text),
            elapsed_ms,
        )
        return embedding.tolist()
    except Exception:
        logger.exception("generate_embedding: failed to generate embedding")
        raise