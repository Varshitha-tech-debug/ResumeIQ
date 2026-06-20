"""PDF text extraction and cleaning."""

import logging
import re

from fastapi import HTTPException
from PyPDF2 import PdfReader

from resumeiq.constants import SECTION_HEADERS

logger = logging.getLogger("resumeiq.pdf")


def _fix_hyphenation(text: str) -> str:
    """Join words split across lines: 'Py-\\nthon' -> 'Python'."""
    return re.sub(r"(\w)-\s*\n\s*(\w)", r"\1\2", text)


def _normalize_whitespace(text: str) -> str:
    text = text.replace("\r\n", "\n").replace("\r", "\n")
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def _fix_missing_spaces(text: str) -> str:
    """Insert spaces where PDF extraction drops them between words."""
    text = re.sub(r"([a-z])([A-Z])", r"\1 \2", text)
    text = re.sub(r"(\w)([,;:])(?=\w)", r"\1\2 ", text)
    text = re.sub(r"\.([A-Z])", r". \1", text)
    return text


def clean_pdf_text(raw: str) -> str:
    """Clean extracted PDF text for reliable keyword and evidence matching."""
    if not raw:
        return ""

    text = _fix_hyphenation(raw)
    text = _normalize_whitespace(text)
    text = _fix_missing_spaces(text)
    return text


def split_sections(text: str) -> dict[str, str]:
    """
    Split resume text into named sections using common ATS headings.
    Returns a dict mapping section name -> content.
    """
    header_pattern = "|".join(re.escape(h) for h in sorted(SECTION_HEADERS, key=len, reverse=True))
    pattern = re.compile(rf"(?i)^\s*({header_pattern})\s*$", re.MULTILINE)

    sections: dict[str, str] = {"full": text}
    matches = list(pattern.finditer(text))

    if not matches:
        return sections

    for idx, match in enumerate(matches):
        name = match.group(1).lower().strip()
        start = match.end()
        end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
        content = text[start:end].strip()
        if content:
            sections[name] = content

    return sections


def extract_text_from_pdf(file_path: str) -> str:
    """
    Extract and clean text from a PDF file.
    Raises HTTPException on read failure or empty/scanned PDFs.
    """
    try:
        reader = PdfReader(file_path)
        pages: list[str] = []
        for page in reader.pages:
            page_text = page.extract_text()
            if page_text:
                pages.append(page_text)
        raw = "\n".join(pages)
    except Exception as exc:
        logger.error("PDF extraction error: %s", exc)
        raise HTTPException(
            status_code=400,
            detail=(
                "Failed to read the PDF. "
                "Please ensure it is a valid, text-based PDF (not a scanned image)."
            ),
        ) from exc

    text = clean_pdf_text(raw)
    if not text or len(text.strip()) < 50:
        raise HTTPException(
            status_code=400,
            detail=(
                "No readable text found in the PDF. "
                "The file may be scanned/image-based or empty. "
                "Upload a text-based PDF resume."
            ),
        )

    return text
