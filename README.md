# AI Document Data Extraction

This project is a modular Python CLI application for extracting simple structured data from documents. The long-term goal is to build an AI-powered document intelligence pipeline that can accept PDF or image files, extract raw text, identify useful fields, and export the results to spreadsheet output.

The current version is an early prototype. It is intentionally incomplete, but it now demonstrates a real end-to-end pipeline using simple text input and basic rule-based extraction.

## Current Working Features

- Runs from `main.py` as the CLI entry point
- Loads sample input files from `sample_inputs/` by default
- Supports plain `.txt` files reliably
- Includes optional basic support for text-based PDFs if `pypdf` or `PyPDF2` is already installed
- Extracts a small set of fields using simple regex rules:
  - `Name`
  - `Date`
  - `Document_Type`
  - `Record_Number`
- Prints progress messages and structured results to the console
- Exports results to CSV in `output/extracted_results.csv`

## Project Files

- `main.py` - runs the pipeline and coordinates each module
- `extract_text.py` - loads raw text from supported files
- `extract_fields.py` - performs rule-based field extraction
- `export_results.py` - prints results and exports them to CSV
- `config.py` - stores basic project settings

## How To Run

Open a terminal in the project folder and run the program:

```bash
python main.py
```

## Sample Output

When the pipeline runs successfully, it will:

- show progress messages in the terminal
- display the extracted fields for each file
- create `output/extracted_results.csv`

## What Is Still Incomplete

- OCR for scanned PDFs and image files
- More reliable PDF extraction across different document layouts
- More advanced field extraction logic
- Additional export formats such as Excel
- Automated testing and broader sample coverage
- Final cleanup and project polish

## Project Status

This implementation is focused on proving that the project architecture is working in a basic way. The current code demonstrates real progress, but it is not yet a finished document intelligence system.
