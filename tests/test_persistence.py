import tempfile
import unittest
from pathlib import Path

import DataManipulation


class TestAssessmentPersistence(unittest.TestCase):
    def test_first_assessment_creates_client_history(self):
        assessment = {
            "timestamp": "2026-08-24T18:30:00",
            "results": {
                "body_fat_percent": 17.95,
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "assessment_results.json"

            DataManipulation.add_assessment(
                "client_001",
                assessment,
                filename,
            )

            data = DataManipulation.load_from_file(filename)

            self.assertEqual(
                data["clients"]["client_001"]["assessments"],
                [assessment],
            )

    def test_existing_client_appends_new_assessment(self):
        assessment_a = {
            "timestamp": "2026-08-24T18:30:00",
            "results": {
                "body_fat_percent": 17.95,
            },
        }

        assessment_b = {
            "timestamp": "2026-09-24T18:30:00",
            "results": {
                "body_fat_percent": 17.10,
            },
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "assessment_results.json"

            DataManipulation.add_assessment(
                "client_001",
                assessment_a,
                filename,
            )

            DataManipulation.add_assessment(
                "client_001",
                assessment_b,
                filename,
            )

            data = DataManipulation.load_from_file(filename)

            assessments = (
                data["clients"]["client_001"]["assessments"]
            )

            self.assertEqual(
                assessments,
                [assessment_a, assessment_b],
            )

    def test_different_clients_have_independent_histories(self):
        assessment_a = {
            "timestamp": "2026-08-24T18:30:00",
        }

        assessment_b = {
            "timestamp": "2026-08-24T19:00:00",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "assessment_results.json"

            DataManipulation.add_assessment(
                "client_001",
                assessment_a,
                filename,
            )

            DataManipulation.add_assessment(
                "client_002",
                assessment_b,
                filename,
            )

            data = DataManipulation.load_from_file(filename)

            self.assertEqual(
                data["clients"]["client_001"]["assessments"],
                [assessment_a],
            )

            self.assertEqual(
                data["clients"]["client_002"]["assessments"],
                [assessment_b],
            )

    def test_invalid_client_id_raises_value_error(self):
        assessment = {
            "timestamp": "2026-08-24T18:30:00",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "assessment_results.json"

            for client_id in ("", "   "):
                with self.subTest(client_id=client_id):
                    with self.assertRaises(ValueError):
                        DataManipulation.add_assessment(
                            client_id,
                            assessment,
                            filename,
                        )

    def test_non_string_client_id_raises_type_error(self):
        assessment = {
            "timestamp": "2026-08-24T18:30:00",
        }

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = Path(temp_dir) / "assessment_results.json"

            for client_id in (123, None):
                with self.subTest(client_id=client_id):
                    with self.assertRaises(TypeError):
                        DataManipulation.add_assessment(
                            client_id,
                            assessment,
                            filename,
                        )


if __name__ == "__main__":
    unittest.main()
