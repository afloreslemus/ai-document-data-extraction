"""Project configuration for the document extraction pipeline."""

from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
INPUT_DIR = DATA_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"

CSV_OUTPUT_FILENAME = "extracted_results.csv"
EXCEL_OUTPUT_FILENAME = "extracted_results.xlsx"
OUTPUT_CSV = OUTPUT_DIR / CSV_OUTPUT_FILENAME
OUTPUT_EXCEL = OUTPUT_DIR / EXCEL_OUTPUT_FILENAME

# Supported document types for the beginner-friendly extraction pipeline.
SUPPORTED_FILE_TYPES = (".txt", ".pdf")
DEFAULT_TEXT_ENCODING = "utf-8"

# Fields extracted from each document.
EXTRACTED_FIELDS = [
    "Name",
    "Date",
    "Document_Type",
    "Record_Number",
    "Amount",
    "Organization",
    "Status",
    "Notes",
]

# Fields written to exported output files.
RESULT_FIELDS = [
    "Source_File",
    "Source_Path",
    "Extraction_Status",
    "Text_Method",
    "Text_Characters",
    *EXTRACTED_FIELDS,
]

# Known input date formats. Parsed dates are normalized to YYYY-MM-DD.
DATE_INPUT_FORMATS = (
    "%m/%d/%Y",
    "%m-%d-%Y",
    "%Y-%m-%d",
    "%B %d, %Y",
    "%b %d, %Y",
)

NOT_FOUND_VALUE = "Not Found"
TEXT_PREVIEW_LENGTH = 160
