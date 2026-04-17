# Project configuration for the document extraction pipeline.

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

# Demo input and output locations.
INPUT_DIR = BASE_DIR / "sample_inputs"
OUTPUT_DIR = BASE_DIR / "output"
OUTPUT_CSV = OUTPUT_DIR / "extracted_results.csv"

# Supported file types for the current version. More can be added later.
SUPPORTED_FILE_TYPES = [".txt", ".pdf"]

# Fields currently extracted with simple rule-based logic.
EXTRACTED_FIELDS = [
    "Name",
    "Date",
    "Document_Type",
    "Record_Number",
]

# Display defaults.
NOT_FOUND_VALUE = "Not Found"
TEXT_PREVIEW_LENGTH = 180
