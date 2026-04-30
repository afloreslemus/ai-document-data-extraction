"""Rule-based field extraction for the AI Document Data Extraction project."""

import re
from datetime import datetime

from config import DATE_INPUT_FORMATS, EXTRACTED_FIELDS, NOT_FOUND_VALUE


def extract_fields(text):
    """Extract configured fields from raw document text."""

    if not text or not text.strip():
        return {field_name: NOT_FOUND_VALUE for field_name in EXTRACTED_FIELDS}

    return {
        "Name": extract_name(text),
        "Date": extract_date(text),
        "Document_Type": extract_document_type(text),
        "Record_Number": extract_record_number(text),
        "Amount": extract_amount(text),
        "Organization": extract_organization(text),
        "Status": extract_status(text),
        "Notes": extract_notes(text),
    }


def extract_name(text):
    """Find a labeled person name using line-based patterns."""

    # The project focuses on documents with explicit labels, so the first pass
    # checks common name field names rather than guessing from any capitalized text.
    patterns = [
        r"(?im)^(?:name|full name|customer name|client name|patient name|student name|applicant name)\s*[:\-]\s*([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+){1,3})\s*$",
        r"(?im)^(?:prepared for|submitted by|issued to)\s*[:\-]\s*([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+){1,3})\s*$",
    ]
    return _search_patterns(patterns, text)


def extract_date(text):
    """Extract a date and normalize it to YYYY-MM-DD when possible."""

    # These patterns capture the most common labeled formats first, then allow
    # a fallback search for an unlabeled date elsewhere in the document.
    patterns = [
        r"(?im)^(?:date|document date|service date|application date|invoice date|record date)\s*[:\-]\s*([^\n]+?)\s*$",
        r"\b([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\b",
        r"\b([0-9]{1,2}-[0-9]{1,2}-[0-9]{4})\b",
        r"\b([0-9]{4}-[0-9]{2}-[0-9]{2})\b",
        r"\b([A-Za-z]{3,9}\s+[0-9]{1,2},\s+[0-9]{4})\b",
    ]

    raw_date = _search_patterns(patterns, text)
    if raw_date == NOT_FOUND_VALUE:
        return NOT_FOUND_VALUE

    normalized_date = _normalize_date(raw_date)
    return normalized_date if normalized_date else NOT_FOUND_VALUE


def extract_document_type(text):
    """Find a labeled document type or infer one from document keywords."""

    labeled_type = _search_patterns(
        [
            r"(?im)^(?:document type|type)\s*[:\-]\s*([A-Za-z][A-Za-z /-]+)\s*$",
        ],
        text,
    )
    if labeled_type != NOT_FOUND_VALUE:
        return _normalize_spaces(labeled_type).title()

    keyword_map = {
        "invoice": "Invoice",
        "student record": "Student Record",
        "application": "Application",
        "receipt": "Receipt",
        "report": "Report",
        "administrative record": "Administrative Record",
        "record": "Record",
    }
    return _infer_keyword_value(text, keyword_map)


def extract_record_number(text):
    """Find a record identifier such as an invoice or application number."""

    # Identifiers are usually labeled, but the fallback pattern still catches
    # codes such as INV-2026-104 when the label is missing.
    patterns = [
        r"(?im)^(?:record number|record no\.?|invoice number|invoice no\.?|document id|application id|student id|case number|reference number|account number|id)\s*[:#\- ]+\s*([A-Za-z0-9/_-]{3,})\s*$",
        r"\b([A-Z]{2,}(?:-[A-Z0-9]{2,})+)\b",
    ]
    return _search_patterns(patterns, text)


def extract_amount(text):
    """Extract a labeled currency amount and normalize it when possible."""

    patterns = [
        r"(?im)^(?:amount|amount due|total|total amount|balance|payment amount|tuition balance)\s*[:\-]\s*(\$?\s*[0-9][0-9,]*(?:\.[0-9]{2})?)\s*$",
        r"(?im)\btotal\s+(?:due|paid)?\s*[:\-]?\s*(\$?\s*[0-9][0-9,]*(?:\.[0-9]{2})?)\b",
    ]

    raw_amount = _search_patterns(patterns, text)
    if raw_amount == NOT_FOUND_VALUE:
        return NOT_FOUND_VALUE

    return _normalize_amount(raw_amount)


def extract_organization(text):
    """Extract an organization or institution name from labeled lines."""

    patterns = [
        r"(?im)^(?:organization|company|vendor|institution|department|office|issued by|prepared by|from)\s*[:\-]\s*(.+?)\s*$",
    ]
    return _search_patterns(patterns, text)


def extract_status(text):
    """Extract a labeled status or infer one from common workflow words."""

    labeled_status = _search_patterns(
        [
            r"(?im)^(?:status|application status|payment status)\s*[:\-]\s*([A-Za-z ]+)\s*$",
        ],
        text,
    )
    if labeled_status != NOT_FOUND_VALUE:
        return _normalize_spaces(labeled_status).title()

    keyword_map = {
        "approved": "Approved",
        "pending": "Pending",
        "paid": "Paid",
        "completed": "Completed",
        "active": "Active",
        "denied": "Denied",
        "rejected": "Rejected",
        "closed": "Closed",
        "open": "Open",
    }
    return _infer_keyword_value(text, keyword_map)


def extract_notes(text):
    """Extract a simple notes or comments line when it is labeled."""

    patterns = [
        r"(?im)^(?:notes|comments|remark|remarks|reason|summary)\s*[:\-]\s*(.+?)\s*$",
    ]
    return _search_patterns(patterns, text)


def _search_patterns(patterns, text):
    """Try each regex pattern and return the first cleaned match."""

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            cleaned_value = _normalize_spaces(match.group(1))
            return cleaned_value if cleaned_value else NOT_FOUND_VALUE
    return NOT_FOUND_VALUE


def _normalize_spaces(value):
    """Collapse repeated whitespace into single spaces."""

    return " ".join(value.split()).strip()


def _normalize_date(value):
    """Validate a matched date and return a consistent ISO-style format."""

    cleaned_value = _normalize_spaces(value).replace(".", "")
    for date_format in DATE_INPUT_FORMATS:
        try:
            parsed_date = datetime.strptime(cleaned_value, date_format)
            return parsed_date.strftime("%Y-%m-%d")
        except ValueError:
            continue
    return None


def _normalize_amount(value):
    """Standardize a currency string to a readable dollar format."""

    cleaned_value = value.replace("$", "").replace(",", "").strip()
    try:
        amount = float(cleaned_value)
        return f"${amount:,.2f}"
    except ValueError:
        return _normalize_spaces(value)


def _infer_keyword_value(text, keyword_map):
    """Infer a field value from keywords when a labeled field is missing."""

    lowered_text = text.lower()
    for keyword, label in keyword_map.items():
        if keyword in lowered_text:
            return label
    return NOT_FOUND_VALUE
