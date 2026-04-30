"""Main CLI entry point for the AI Document Data Extraction project."""

import argparse
from pathlib import Path

from config import EXTRACTED_FIELDS, INPUT_DIR, NOT_FOUND_VALUE, TEXT_PREVIEW_LENGTH
from config import SUPPORTED_FILE_TYPES
from export_results import export_results, print_results
from extract_fields import extract_fields
from extract_text import extract_text_from_file


def parse_arguments():
    """Parse command-line options for the extraction pipeline."""

    parser = argparse.ArgumentParser(
        description="Run the AI Document Data Extraction pipeline."
    )
    parser.add_argument(
        "inputs",
        nargs="*",
        help=(
            "Optional file paths or folders to process. "
            "If omitted, the configured data/input folder is used."
        ),
    )
    parser.add_argument(
        "--skip-export",
        action="store_true",
        help="Run the pipeline without creating CSV or Excel output files.",
    )
    return parser.parse_args()


def discover_input_files(user_inputs):
    """Find supported files from CLI inputs or the configured input folder."""

    search_targets = [Path(value) for value in user_inputs] if user_inputs else [INPUT_DIR]
    discovered_files = []
    missing_targets = []
    unsupported_targets = []

    for target in search_targets:
        if target.is_file():
            if _is_supported_file(target):
                discovered_files.append(target.resolve())
            else:
                unsupported_targets.append(str(target))
        elif target.is_dir():
            discovered_files.extend(_collect_supported_files(target))
        else:
            missing_targets.append(str(target))

    unique_files = sorted(set(discovered_files))
    return unique_files, missing_targets, unsupported_targets


def _collect_supported_files(folder_path):
    """Collect supported files from a folder and its subfolders."""

    folder_path = Path(folder_path)
    if not folder_path.exists():
        return []

    return sorted(
        file_path.resolve()
        for file_path in folder_path.rglob("*")
        if file_path.is_file() and _is_supported_file(file_path)
    )


def _is_supported_file(file_path):
    """Check whether the file extension is supported by the project."""

    return Path(file_path).suffix.lower() in SUPPORTED_FILE_TYPES


def build_result_row(file_path, text_result, field_result):
    """Combine extraction metadata and field values into one export row."""

    return {
        "Source_File": file_path.name,
        "Source_Path": str(file_path),
        "Extraction_Status": "Success" if text_result["success"] else "Failed",
        "Text_Method": text_result["method"],
        "Text_Characters": len(text_result["text"]),
        **field_result,
    }


def create_empty_field_result():
    """Return placeholder values when field extraction cannot run."""

    return {field_name: NOT_FOUND_VALUE for field_name in EXTRACTED_FIELDS}


def run_pipeline(input_files, skip_export=False):
    """Process each input file from text extraction to structured output."""

    results = []
    total_files = len(input_files)

    print(f"[INFO] Starting extraction pipeline for {total_files} file(s).")

    for index, file_path in enumerate(input_files, start=1):
        print(f"\n[{index}/{total_files}] Processing: {file_path.name}")

        text_result = extract_text_from_file(file_path)
        print(f"[INFO] {text_result['message']}")

        if text_result["success"]:
            cleaned_text = " ".join(text_result["text"].split())
            preview = cleaned_text[:TEXT_PREVIEW_LENGTH]
            ellipsis = "..." if len(cleaned_text) > TEXT_PREVIEW_LENGTH else ""
            print(f"[PREVIEW] {preview}{ellipsis}")
            field_result = extract_fields(text_result["text"])
            print("[INFO] Field extraction completed.")
        else:
            field_result = create_empty_field_result()
            print("[WARN] Field extraction skipped because no usable text was available.")

        results.append(build_result_row(file_path, text_result, field_result))

    print_results(results)

    if skip_export:
        print("\n[INFO] Export skipped by request.")
        return results

    exported_paths = export_results(results)
    if exported_paths["csv"]:
        print(f"\n[INFO] CSV output: {exported_paths['csv']}")
    if exported_paths["excel"]:
        print(f"[INFO] Excel output: {exported_paths['excel']}")
    else:
        print("[INFO] Excel output skipped because openpyxl is not installed.")

    return results


def main():
    """Run the CLI pipeline."""

    args = parse_arguments()

    print("=" * 70)
    print("AI Document Data Extraction")
    print("=" * 70)

    input_files, missing_targets, unsupported_targets = discover_input_files(args.inputs)

    for missing_target in missing_targets:
        print(f"[WARN] Missing file or folder skipped: {missing_target}")

    for unsupported_target in unsupported_targets:
        print(f"[WARN] Unsupported file skipped: {unsupported_target}")

    if not input_files:
        print(
            "[ERROR] No supported input files were found. "
            f"Add .txt or .pdf files to {INPUT_DIR} or pass file/folder paths on the command line."
        )
        return 1

    print(f"[INFO] Found {len(input_files)} supported input file(s).")
    run_pipeline(input_files, skip_export=args.skip_export)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
