from pathlib import Path
from pypdf import PdfReader
from src.services.text_cleaning_service import clean_text
from src.utils.logger import logger
import time


def read_pdf(path: Path) -> str:
    start = time.perf_counter()
    try:
        if not path.is_file():
            raise FileNotFoundError(f"File {path} does not exist.")

        reader = PdfReader(path)
        text = ""
        page_count = len(reader.pages)
        for page in reader.pages:
            page_text = page.extract_text() or ""
            text += page_text + "\n"

        text = clean_text(text)
        elapsed_ms = (time.perf_counter() - start) * 1000
        logger.info(
            "read_pdf: read %d pages from %s and extracted %d characters in %.2f ms",
            page_count,
            path.name,
            len(text),
            elapsed_ms,
        )

        return text
    except Exception:
        logger.exception("read_pdf: failed to read PDF %s", path)
        raise
