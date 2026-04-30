"""Text extraction helpers for the AI Document Data Extraction project."""

from importlib import import_module
from pathlib import Path

from config import DEFAULT_TEXT_ENCODING, SUPPORTED_FILE_TYPES


def extract_text_from_file(file_path):
    """Route each supported file to the correct extraction function."""

    path = Path(file_path)

    if not path.exists():
        return _build_result(
            success=False,
            text="",
            method="missing_file",
            message=f"File not found: {path}",
        )

    file_extension = path.suffix.lower()

    if file_extension == ".txt":
        return _read_text_file(path)

    if file_extension == ".pdf":
        return _read_pdf_file(path)

    supported_types = ", ".join(SUPPORTED_FILE_TYPES)
    return _build_result(
        success=False,
        text="",
        method="unsupported",
        message=(
            f"Unsupported file type '{file_extension}'. "
            f"Supported file types: {supported_types}."
        ),
    )


def _read_text_file(path):
    """Read a plain text file using a small set of common encodings."""

    for encoding in (DEFAULT_TEXT_ENCODING, "utf-8-sig", "cp1252"):
        try:
            text = path.read_text(encoding=encoding)
            cleaned_text = _clean_extracted_text(text)
            return _build_result(
                success=bool(cleaned_text),
                text=cleaned_text,
                method="plain_text",
                message=(
                    f"Loaded text from {path.name} using {encoding}."
                    if cleaned_text
                    else f"{path.name} was read, but it did not contain usable text."
                ),
            )
        except UnicodeDecodeError:
            continue
        except OSError as error:
            return _build_result(
                success=False,
                text="",
                method="plain_text",
                message=f"Could not read file: {error}",
            )

    return _build_result(
        success=False,
        text="",
        method="plain_text",
        message=(
            "The text file could not be decoded with the supported encodings "
            "(utf-8, utf-8-sig, cp1252)."
        ),
    )


def _read_pdf_file(path):
    """Extract text from a text-based PDF document."""

    pdf_reader_class, library_name = _get_pdf_reader()

    if pdf_reader_class is None:
        return _build_result(
            success=False,
            text="",
            method="pdf_unavailable",
            message=(
                "PDF support requires the optional 'pypdf' package from "
                "requirements.txt."
            ),
        )

    try:
        reader = pdf_reader_class(str(path))
        page_text_parts = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            cleaned_page_text = _clean_extracted_text(page_text)
            if cleaned_page_text:
                page_text_parts.append(cleaned_page_text)

        if not page_text_parts:
            return _build_result(
                success=False,
                text="",
                method=f"{library_name}_pdf",
                message=(
                    "The PDF opened successfully, but no selectable text was found. "
                    "Scanned PDFs are not supported without OCR."
                ),
            )

        combined_text = "\n".join(page_text_parts)
        return _build_result(
            success=True,
            text=combined_text,
            method=f"{library_name}_pdf",
            message=(
                f"Extracted text from {path.name} using {library_name} "
                f"across {len(page_text_parts)} page(s) with text."
            ),
        )
    except Exception as error:
        return _build_result(
            success=False,
            text="",
            method=f"{library_name}_pdf",
            message=f"PDF extraction failed: {error}",
        )


def _clean_extracted_text(text):
    """Normalize whitespace while keeping line-based field labels readable."""

    normalized_text = text.replace("\r\n", "\n").replace("\r", "\n")
    cleaned_lines = [line.strip() for line in normalized_text.split("\n")]
    return "\n".join(cleaned_lines).strip()


def _get_pdf_reader():
    """Import the PDF library only when PDF processing is needed."""

    for module_name in ("pypdf", "PyPDF2"):
        try:
            module = import_module(module_name)
            pdf_reader_class = getattr(module, "PdfReader", None)
            if pdf_reader_class is not None:
                return pdf_reader_class, module_name
        except ImportError:
            continue

    return None, None


def _build_result(success, text, method, message):
    """Return extraction metadata in a consistent structure."""

    return {
        "success": success,
        "text": text,
        "method": method,
        "message": message,
    }
