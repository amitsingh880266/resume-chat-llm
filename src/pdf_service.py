from pathlib import Path
from pypdf import PdfReader

def read_pdf(path: Path) -> str:
    if not path.is_file():
        raise FileNotFoundError(f"File {path} does not exist.")
    
    reader = PdfReader(path)
    text = ""
    for page in reader.pages:
        text += page.extract_text() + "\n"
    return text
