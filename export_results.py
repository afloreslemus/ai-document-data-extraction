# Output helpers for displaying and exporting extracted results.

import csv
from pathlib import Path


def print_results(results):
    # Print structured extraction results to the console.
    if not results:
        print("\n[INFO] No results are available to display.")
        return

    print("\n" + "=" * 60)
    print("Structured Extraction Results")
    print("=" * 60)

    for index, result in enumerate(results, start=1):
        print(f"\nResult {index}: {result['Source_File']}")
        print(f"  Status: {result['Extraction_Status']}")
        print(f"  Text Method: {result['Text_Method']}")
        print(f"  Text Characters: {result['Text_Characters']}")
        print(f"  Name: {result['Name']}")
        print(f"  Date: {result['Date']}")
        print(f"  Document Type: {result['Document_Type']}")
        print(f"  Record Number: {result['Record_Number']}")


def export_results_to_csv(results, output_path):
    # Export extracted results to CSV.
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    fieldnames = [
        "Source_File",
        "Extraction_Status",
        "Text_Method",
        "Text_Characters",
        "Name",
        "Date",
        "Document_Type",
        "Record_Number",
    ]

    with output_path.open("w", newline="", encoding="utf-8") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()

        for result in results:
            writer.writerow(result)

    return output_path
