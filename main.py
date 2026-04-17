# Main entry point for the AI Document Data Extraction project.

import argparse
from pathlib import Path

from config import (
    EXTRACTED_FIELDS,
    INPUT_DIR,
    NOT_FOUND_VALUE,
    OUTPUT_CSV,
    SUPPORTED_FILE_TYPES,
    TEXT_PREVIEW_LENGTH,
)
from export_results import export_results_to_csv, print_results
from extract_fields import extract_fields
from extract_text import extract_text_from_file


def parse_arguments():
    # Parse simple CLI arguments for the demo pipeline.

    parser = argparse.ArgumentParser(
        description="Run the document extraction pipeline."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help="Optional file paths or folders to process. If omitted, the sample_inputs folder is used.",
    )
    parser.add_argument(
        "--skip-export",
        action="store_true",
        help="Run the pipeline without writing the CSV output file.",
    )
    return parser.parse_args()


def discover_input_files(user_inputs):
    # Find supported files from CLI inputs or the default sample input folder.

    if not user_inputs:
        return _collect_supported_files(INPUT_DIR)

    discovered_files = []

    for raw_input in user_inputs:
        path = Path(raw_input)

        if path.is_file() and path.suffix.lower() in SUPPORTED_FILE_TYPES:
            discovered_files.append(path)
        elif path.is_dir():
            discovered_files.extend(_collect_supported_files(path))
        else:
            print(f"[WARN] Skipping unsupported or missing input: {raw_input}")

    # Remove duplicates while keeping output predictable.
    return sorted(set(discovered_files))


def _collect_supported_files(folder_path):
    # Return supported files from a folder if it exists.

    folder_path = Path(folder_path)
    if not folder_path.exists():
        return []

    return sorted(
        file_path
        for file_path in folder_path.iterdir()
        if file_path.is_file() and file_path.suffix.lower() in SUPPORTED_FILE_TYPES
    )


def build_result_row(file_path, text_result, field_result):
    # Combine text extraction and field extraction into one export row.

    return {
        "Source_File": file_path.name,
        "Extraction_Status": "Success" if text_result["success"] else "Failed",
        "Text_Method": text_result["method"],
        "Text_Characters": len(text_result["text"]),
        **field_result,
    }


def create_empty_field_result():
    # Return placeholder values when extraction fails.

    return {field_name: NOT_FOUND_VALUE for field_name in EXTRACTED_FIELDS}


def run_pipeline(input_files, skip_export=False):
    # Process each input file from raw text extraction to structured output.

    results = []

    for index, file_path in enumerate(input_files, start=1):
        print(f"\n[STEP {index}] Processing: {file_path.name}")

        text_result = extract_text_from_file(file_path)
        print(f"[INFO] {text_result['message']}")

        if text_result["success"]:
            cleaned_text = " ".join(text_result["text"].split())
            preview = cleaned_text[:TEXT_PREVIEW_LENGTH]
            if cleaned_text:
                ellipsis = "..." if len(cleaned_text) > TEXT_PREVIEW_LENGTH else ""
                print(f"[PREVIEW] {preview}{ellipsis}")

            field_result = extract_fields(text_result["text"])
            print("[INFO] Basic field extraction completed.")
        else:
            field_result = create_empty_field_result()
            print("[INFO] Field extraction skipped because no usable text was available.")

        results.append(build_result_row(file_path, text_result, field_result))

    print_results(results)

    if not skip_export and results:
        output_path = export_results_to_csv(results, OUTPUT_CSV)
        print(f"\n[INFO] Results exported to: {output_path}")
    elif skip_export:
        print("\n[INFO] CSV export was skipped by request.")

    print("\n[NOTE] This version is intentionally limited.")
    print("[TODO] Add OCR, stronger PDF handling, more fields, and broader testing later.")

    return results


def main():
    # Run the document extraction demo from the command line.

    args = parse_arguments()

    print("=" * 60)
    print("AI Document Data Extraction")
    print("=" * 60)

    input_files = discover_input_files(args.inputs)

    if not input_files:
        print(
            "[ERROR] No supported input files were found. "
            "Add a .txt file to sample_inputs or pass a file path to main.py."
        )
        return 1

    print(f"[INFO] Found {len(input_files)} supported file(s).")
    run_pipeline(input_files, skip_export=args.skip_export)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
