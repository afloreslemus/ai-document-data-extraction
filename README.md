# AI Document Data Extraction

## Project Description

AI Document Data Extraction is a command-line Python project that reads simple administrative documents, extracts useful structured fields, and exports the results to spreadsheet-friendly output files. The project is designed to show a complete end-to-end data extraction workflow using modular Python code.

## Problem Statement

Organizations often receive documents such as invoices, student records, and application forms that contain important information in plain text. Manually reviewing each file is slow and repetitive. This project demonstrates how Python can automate part of that work by:

- reading supported document files
- extracting raw text
- identifying key fields with rule-based logic
- exporting the extracted results for review

## Features

- CLI-based workflow starting from `main.py`
- Automatically discovers supported files in `data/input/`
- Accepts custom file paths or folders from the command line
- Supports `.txt` files and text-based `.pdf` files
- Extracts these fields:
  - `Name`
  - `Date`
  - `Document_Type`
  - `Record_Number`
  - `Amount`
  - `Organization`
  - `Status`
  - `Notes`
- Uses regex and simple validation rules
- Returns `Not Found` when data is missing
- Prints clear progress and result summaries in the terminal
- Exports results to CSV
- Exports results to Excel when `openpyxl` is installed
- Includes sample input files for testing
- Includes a beginner-friendly automated test script

## Libraries Used

- Python standard library
  - `argparse`
  - `csv`
  - `datetime`
  - `pathlib`
  - `re`
  - `unittest`
- `pypdf` for text-based PDF extraction
- `openpyxl` for optional Excel export

## Folder Structure

```text
ai-document-data-extraction/
├── config.py
├── export_results.py
├── extract_fields.py
├── extract_text.py
├── main.py
├── README.md
├── requirements.txt
├── data/
│   └── input/
│       ├── application_record.txt
│       ├── invoice_record.txt
│       └── student_record.txt
├── output/
│   ├── extracted_results.csv
│   └── extracted_results.xlsx
└── tests/
    └── test_pipeline.py
```

## Dataset / Sample Input Files

The sample dataset is stored in `data/input/`. These are simple fake documents created for project testing:

- `invoice_record.txt` - invoice-style sample with amount and payment status
- `student_record.txt` - student record sample with institution and notes
- `application_record.txt` - application sample with status and fee amount

The sample data uses `.txt` files so the project can be tested immediately after download. PDF support is included for text-based PDFs, but sample PDFs are not required to run the project.

## Installation Instructions

1. Open a terminal in the project folder.
2. Create a virtual environment if desired:

```bash
python -m venv .venv
```

3. Activate the virtual environment.

Windows PowerShell:

```powershell
.venv\Scripts\Activate.ps1
```

4. Install the project dependencies:

```bash
pip install -r requirements.txt
```

## How to Run the Project

Run the default sample dataset:

```bash
python main.py
```

Run a specific file:

```bash
python main.py data/input/invoice_record.txt
```

Run a custom folder:

```bash
python main.py data/input
```

Run without creating output files:

```bash
python main.py --skip-export
```

## Expected Output

When the program runs successfully, it will:

- display a project title banner
- show how many input files were found
- process each file one by one
- print a text extraction message and text preview
- display the extracted structured fields
- create output files in the `output/` folder

Expected exported files:

- `output/extracted_results.csv`
- `output/extracted_results.xlsx` if `openpyxl` is installed

## Testing

Run the beginner-friendly automated tests with:

```bash
python -m unittest discover -s tests -v
```

The tests check:

- sample files are discovered correctly
- text extraction works for `.txt` files
- field extraction returns expected values
- CSV export is created successfully
- the pipeline runs end-to-end on a sample input

## Known Limitations

- OCR is not implemented, so scanned PDFs and image files are not supported
- PDF extraction only works for text-based PDFs
- Field extraction uses regex and keyword rules, so unusual document layouts may reduce accuracy
- The project is designed for small sample datasets, not high-volume production processing
- Excel export depends on `openpyxl`

## References / External Resources

- [pypdf documentation](https://pypdf.readthedocs.io/)
- [openpyxl documentation](https://openpyxl.readthedocs.io/)
- Python Standard Library documentation: https://docs.python.org/3/library/
