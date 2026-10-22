"""Small offline checks: run `python -m unittest test_collection_pipeline` in src/."""

import json
import tempfile
import unittest
from pathlib import Path

from collection_pipeline import build_dataset, label_requests, load_month, process_month


def request(key, closed_date=None, status="Closed"):
    return {"unique_key": key, "created_date": "2025-01-01T00:00:00.000",
            "closed_date": closed_date, "agency": "DOT",
            "complaint_type": "Street Condition", "status": status}


class CollectionChecks(unittest.TestCase):
    def test_target_boundary_missing_outcomes_and_negative_duration(self):
        records = [request("1", "2025-01-01T00:00:00.000"),
                   request("2", "2025-01-03T00:00:00.000"),
                   request("3", "2025-01-03T00:00:01.000"),
                   request("4", status="Pending"), request("5", status="Open"),
                   request("6", status="Unspecified"),
                   request("7", "2024-12-31T23:59:59.000"),
                   request("8", "2025-01-01T01:00:00.000", status="Pending")]
        clean, checks = process_month(records, 2025, 1)
        labeled = label_requests(clean).set_index("unique_key")
        self.assertEqual(checks["negative_excluded"], 1)
        self.assertEqual(checks["missing_closure"], 3)
        self.assertEqual(labeled["closed_48h"].to_dict(),
                         {"1": 1, "2": 1, "3": 0, "4": 0, "5": 0, "8": 1})
        self.assertEqual(len(labeled.columns), 37)  # ID is now the index.

    def test_duplicate_ids_stop_processing(self):
        with self.assertRaisesRegex(ValueError, "duplicate"):
            process_month([request("1"), request("1")], 2025, 1)

    def test_wrong_month_stops_processing(self):
        with self.assertRaisesRegex(ValueError, "outside 2025-02"):
            process_month([request("1")], 2025, 2)

    def test_unpadded_filename_and_ambiguous_inputs(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            (root / "street_conditions_2025_2_raw.json").write_text(json.dumps([request("1")]))
            self.assertEqual(load_month(root, 2025, 2)[0]["unique_key"], "1")
            (root / "street_conditions_2025_02_raw.json").write_text(json.dumps([request("2")]))
            with self.assertRaisesRegex(ValueError, "Multiple raw inputs"):
                load_month(root, 2025, 2)

    def test_source_folder_cannot_be_output_folder(self):
        with tempfile.TemporaryDirectory() as folder:
            with self.assertRaisesRegex(ValueError, "Do not overwrite"):
                build_dataset(folder, folder)


if __name__ == "__main__":
    unittest.main()
