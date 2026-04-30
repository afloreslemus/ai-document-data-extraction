"""Output helpers for displaying and exporting extracted results."""

import csv
from pathlib import Path

from config import (
    OUTPUT_CSV,
    OUTPUT_EXCEL,
    RESULT_FIELDS,
)


def print_results(results):
    """Print a structured summary of extraction results to the console."""

    if not results:
        print("\n[INFO] No results are available to display.")
        return

    successful_count = sum(
        1 for result in results if result["Extraction_Status"] == "Success"
    )
    failed_count = len(results) - successful_count

    print("\n" + "=" * 70)
    print("Extraction Summary")
    print("=" * 70)
    print(f"Files processed: {len(results)}")
    print(f"Successful text extractions: {successful_count}")
    print(f"Failed text extractions: {failed_count}")

    for index, result in enumerate(results, start=1):
        print("\n" + "-" * 70)
        print(f"Document {index}: {result['Source_File']}")
        print("-" * 70)
        print(f"Status: {result['Extraction_Status']}")
        print(f"Text Method: {result['Text_Method']}")
        print(f"Text Characters: {result['Text_Characters']}")
        print(f"Name: {result['Name']}")
        print(f"Date: {result['Date']}")
        print(f"Document Type: {result['Document_Type']}")
        print(f"Record Number: {result['Record_Number']}")
        print(f"Amount: {result['Amount']}")
        print(f"Organization: {result['Organization']}")
        print(f"Status Field: {result['Status']}")
        print(f"Notes: {result['Notes']}")


def export_results(results, csv_path=OUTPUT_CSV, excel_path=OUTPUT_EXCEL):
    """Export results to CSV and, when possible, to Excel."""

    exported_paths = {"csv": None, "excel": None}

    if not results:
        return exported_paths

    exported_paths["csv"] = export_results_to_csv(results, csv_path)
    exported_paths["excel"] = export_results_to_excel(results, excel_path)
    return exported_paths


def export_results_to_csv(results, output_path, fieldnames=RESULT_FIELDS):
    """Export extracted results to CSV."""

    output_path = Path(output_path)
    rows = [{field: result.get(field, "") for field in fieldnames} for result in results]
    return _write_csv(output_path, fieldnames, rows)


def export_results_to_excel(results, output_path, fieldnames=RESULT_FIELDS):
    """Export extracted results to Excel when openpyxl is installed."""

    try:
        from openpyxl import Workbook
    except ImportError:
        return None

    output_path = Path(output_path)
    rows = [[result.get(field, "") for field in fieldnames] for result in results]
    return _write_excel(output_path, fieldnames, rows, Workbook)


def _write_csv(output_path, fieldnames, rows):
    """Write CSV data to a specific path."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)

    return output_path


def _write_excel(output_path, fieldnames, rows, workbook_class):
    """Write Excel data to a specific path."""

    output_path.parent.mkdir(parents=True, exist_ok=True)

    workbook = workbook_class()
    worksheet = workbook.active
    worksheet.title = "Extracted Results"
    worksheet.append(list(fieldnames))

    for row in rows:
        worksheet.append(row)

    for column_cells in worksheet.columns:
        max_length = max(len(str(cell.value or "")) for cell in column_cells)
        worksheet.column_dimensions[column_cells[0].column_letter].width = min(
            max_length + 2, 40
        )

    workbook.save(output_path)
    return output_path
