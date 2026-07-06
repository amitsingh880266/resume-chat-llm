import time
import nltk
from nltk.tokenize import sent_tokenize

from src.utils.logger import logger

nltk.download("punkt", quiet=True)


def split_into_chunks(
    text: str,
    chunk_size: int = 500,
) -> list[str]:
    start = time.perf_counter()

    try:
        if not text.strip():
            raise ValueError("Text cannot be empty.")

        if chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")

        sentences = sent_tokenize(text)

        chunks: list[str] = []

        current_chunk: list[str] = []
        current_size = 0

        for sentence in sentences:
            sentence_size = len(sentence)

            # If the sentence fits, add it to the current chunk
            if current_size + sentence_size <= chunk_size:
                current_chunk.append(sentence)
                current_size += sentence_size
            else:
                # Save the completed chunk
                if current_chunk:
                    chunks.append(" ".join(current_chunk))

                # Start a new chunk with the current sentence
                current_chunk = [sentence]
                current_size = sentence_size

        # Save the last chunk
        if current_chunk:
            chunks.append(" ".join(current_chunk))

        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "split_into_chunks: produced %d chunks from %d sentences in %.2f ms",
            len(chunks),
            len(sentences),
            elapsed_ms,
        )

        return chunks
    except Exception:
        logger.exception("split_into_chunks: failed to split text into chunks")
        raise