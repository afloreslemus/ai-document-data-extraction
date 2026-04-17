# Rule-based field extraction for the current prototype.

import re
from config import NOT_FOUND_VALUE


def extract_fields(text):
    # Extract fields from raw text.

    fields = {
        "Name": extract_name(text),
        "Date": extract_date(text),
        "Document_Type": extract_document_type(text),
        "Record_Number": extract_record_number(text),
    }

    return fields


def extract_name(text):
    # Find a labeled name field.

    patterns = [
        r"(?im)^(?:name|customer name|client name|patient name)\s*[:\-]\s*([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+){0,3})\s*$",
        r"(?im)^prepared for\s*[:\-]\s*([A-Z][A-Za-z'.-]+(?:\s+[A-Z][A-Za-z'.-]+){0,3})\s*$",
    ]

    return _search_patterns(patterns, text)


def extract_date(text):
    # Look for a labeled date or a common date format.

    patterns = [
        r"(?im)^(?:date|document date|service date)\s*[:\-]\s*([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\s*$",
        r"(?im)^(?:date|document date|service date)\s*[:\-]\s*([0-9]{4}-[0-9]{2}-[0-9]{2})\s*$",
        r"(?im)^(?:date|document date|service date)\s*[:\-]\s*([A-Za-z]+\s+[0-9]{1,2},\s+[0-9]{4})\s*$",
        r"\b([0-9]{1,2}/[0-9]{1,2}/[0-9]{4})\b",
        r"\b([0-9]{4}-[0-9]{2}-[0-9]{2})\b",
    ]

    return _search_patterns(patterns, text)


def extract_document_type(text):
    # Find a labeled document type or infer one from keywords.

    labeled_type = _search_patterns(
        [
            r"(?im)^(?:document type|type)\s*[:\-]\s*([A-Za-z][A-Za-z ]+)\s*$",
        ],
        text,
    )

    if labeled_type != NOT_FOUND_VALUE:
        return labeled_type

    keyword_map = {
        "invoice": "Invoice",
        "report": "Report",
        "application": "Application",
        "receipt": "Receipt",
        "record": "Record",
    }

    lowered_text = text.lower()
    for keyword, label in keyword_map.items():
        if keyword in lowered_text:
            return label

    return NOT_FOUND_VALUE


def extract_record_number(text):
    # Find a simple record or document identifier.

    patterns = [
        r"(?im)^(?:record number|record no\.?|invoice number|invoice no\.?|document id|id|account number)\s*[:#\- ]+\s*([A-Z0-9-]+)\s*$",
        r"\b([A-Z]{2,}-[0-9]{2,})\b",
    ]

    return _search_patterns(patterns, text)


def _search_patterns(patterns, text):
    # Try each regex pattern and return the first clean match.

    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1).strip()
    return NOT_FOUND_VALUE
