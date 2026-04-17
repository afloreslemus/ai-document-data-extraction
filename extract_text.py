# Text extraction helpers for the AI Document Data Extraction project.

from importlib import import_module
from pathlib import Path


def extract_text_from_file(file_path):
    # Send each file to the correct extraction function.
    path = Path(file_path)
    file_extension = path.suffix.lower()

    if file_extension == ".txt":
        return _read_text_file(path)

    if file_extension == ".pdf":
        return _read_pdf_file(path)

    return _build_result(
        success=False,
        text="",
        method="unsupported",
        message=f"File type '{file_extension}' is not supported yet.",
    )


def _read_text_file(path):
    # Plain text files are the most reliable format in the current version.
    try:
        text = path.read_text(encoding="utf-8")
        return _build_result(
            success=True,
            text=text,
            method="plain_text",
            message=f"Loaded text from {path.name}.",
        )
    except UnicodeDecodeError:
        return _build_result(
            success=False,
            text="",
            method="plain_text",
            message=(
                "The text file could not be decoded with UTF-8. "
                "Additional file handling may be needed later."
            ),
        )
    except OSError as error:
        return _build_result(
            success=False,
            text="",
            method="plain_text",
            message=f"Could not read file: {error}",
        )


def _read_pdf_file(path):
    # PDF support is basic for now and only targets text-based PDFs.
    # TODO: Add OCR support for scanned PDFs and image files later.
    pdf_reader_class, library_name = _get_pdf_reader()

    if pdf_reader_class is None:
        return _build_result(
            success=False,
            text="",
            method="pdf_unavailable",
            message=(
                "PDF support requires the optional 'pypdf' package. "
                "Text files will still work without it."
            ),
        )

    try:
        reader = pdf_reader_class(str(path))
        page_text_parts = []

        for page in reader.pages:
            page_text = page.extract_text()
            if page_text and page_text.strip():
                page_text_parts.append(page_text.strip())

        if not page_text_parts:
            return _build_result(
                success=False,
                text="",
                method=f"{library_name}_pdf",
                message=(
                    "The PDF opened successfully, but no selectable text was found. "
                    "This document may need OCR in a future update."
                ),
            )

        combined_text = "\n".join(page_text_parts)
        return _build_result(
            success=True,
            text=combined_text,
            method=f"{library_name}_pdf",
            message=f"Extracted text from PDF using {library_name}.",
        )
    except Exception as error:
        return _build_result(
            success=False,
            text="",
            method=f"{library_name}_pdf",
            message=f"PDF extraction failed: {error}",
        )


def _get_pdf_reader():
    # Import the PDF library only when it is actually needed.
    # This keeps PDF support optional for the project.
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
    # Keep every extraction result in the same format.
    return {
        "success": success,
        "text": text,
        "method": method,
        "message": message,
    }
