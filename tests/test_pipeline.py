"""Simple automated tests for the AI Document Data Extraction project."""

import unittest

from config import INPUT_DIR, OUTPUT_CSV
from export_results import export_results_to_csv
from extract_fields import extract_fields
from extract_text import extract_text_from_file
from main import discover_input_files, run_pipeline


class TestDocumentExtractionPipeline(unittest.TestCase):
    """Verify the basic project workflow remains runnable."""

    def test_discover_input_files_finds_sample_documents(self):
        files, missing_targets, unsupported_targets = discover_input_files([])
        self.assertGreaterEqual(len(files), 3)
        self.assertEqual(missing_targets, [])
        self.assertEqual(unsupported_targets, [])

    def test_extract_text_from_text_file(self):
        sample_path = INPUT_DIR / "invoice_record.txt"
        result = extract_text_from_file(sample_path)
        self.assertTrue(result["success"])
        self.assertIn("Jordan Smith", result["text"])

    def test_extract_fields_returns_expected_values(self):
        sample_text = (INPUT_DIR / "application_record.txt").read_text(encoding="utf-8")
        fields = extract_fields(sample_text)
        self.assertEqual(fields["Name"], "Luis Martinez")
        self.assertEqual(fields["Date"], "2026-04-22")
        self.assertEqual(fields["Document_Type"], "Application")
        self.assertEqual(fields["Record_Number"], "APP-2026-778")
        self.assertEqual(fields["Amount"], "$75.00")
        self.assertEqual(fields["Status"], "Pending")

    def test_export_results_creates_csv(self):
        results = [
            {
                "Source_File": "sample.txt",
                "Source_Path": "sample.txt",
                "Extraction_Status": "Success",
                "Text_Method": "plain_text",
                "Text_Characters": 20,
                "Name": "Test User",
                "Date": "2026-04-29",
                "Document_Type": "Record",
                "Record_Number": "REC-100",
                "Amount": "$10.00",
                "Organization": "Test Org",
                "Status": "Open",
                "Notes": "Example note",
            }
        ]

        created_path = export_results_to_csv(results, OUTPUT_CSV)
        self.assertTrue(created_path.exists())

    def test_run_pipeline_returns_results_for_sample_file(self):
        sample_path = INPUT_DIR / "student_record.txt"
        results = run_pipeline([sample_path], skip_export=True)
        self.assertEqual(len(results), 1)
        self.assertEqual(results[0]["Source_File"], "student_record.txt")
        self.assertEqual(results[0]["Extraction_Status"], "Success")


if __name__ == "__main__":
    unittest.main()
