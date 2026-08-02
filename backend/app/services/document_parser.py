from pathlib import Path

from docx import Document
from pypdf import PdfReader


def extract_text_from_txt(file_path: Path) -> str:
    """Extract text from a plain text file."""
    return file_path.read_text(encoding="utf-8", errors="ignore")


def extract_text_from_pdf(file_path: Path) -> str:
    """Extract text from a PDF file."""
    reader = PdfReader(str(file_path))

    pages = []

    for page in reader.pages:
        text = page.extract_text()
        if text:
            pages.append(text)

    return "\n".join(pages)


def extract_text_from_docx(file_path: Path) -> str:
    """Extract text from a DOCX file."""
    document = Document(str(file_path))

    paragraphs = [
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    ]

    return "\n".join(paragraphs)


def extract_text(file_path: str | Path) -> str:
    """
    Extract text from a supported document.

    Supported formats:
    - .txt
    - .pdf
    - .docx
    """
    path = Path(file_path)

    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")

    extension = path.suffix.lower()

    if extension == ".txt":
        return extract_text_from_txt(path)

    if extension == ".pdf":
        return extract_text_from_pdf(path)

    if extension == ".docx":
        return extract_text_from_docx(path)

    raise ValueError(
        f"Text extraction is not supported for file type: {extension}"
    )