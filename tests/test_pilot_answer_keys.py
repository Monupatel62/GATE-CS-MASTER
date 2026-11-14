"""Integrity checks for the transcribed official pilot answer-key rows."""
from __future__ import annotations

import csv
from collections import defaultdict
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parents[1]
KEY_DIR = ROOT / "research" / "pilot-verified-keys"
KEY_FILES = (
    KEY_DIR / "2026-CS1-answer-key.csv",
    KEY_DIR / "2025-CS1-CS2-and-2026-CS2-answer-keys.csv",
)
EXPECTED_SESSIONS = {
    ("2025", "CS-1", "1"),
    ("2025", "CS-2", "2"),
    ("2026", "CS-1", "3"),
    ("2026", "CS-2", "4"),
}
EXPECTED_FIELDS = {
    "year", "paper_code", "session", "question_no", "question_type",
    "section", "official_key_or_range", "marks", "source_url",
    "verification_status",
}


class PilotAnswerKeyTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.rows = []
        for path in KEY_FILES:
            with path.open(newline="", encoding="utf-8") as handle:
                reader = csv.DictReader(handle)
                if not EXPECTED_FIELDS.issubset(set(reader.fieldnames or [])):
                    raise AssertionError(f"{path.name}: missing required CSV columns")
                cls.rows.extend(reader)

    def test_exactly_four_pilot_sessions_and_260_rows(self):
        self.assertEqual(len(self.rows), 260)
        sessions = {
            (row["year"], row["paper_code"], row["session"])
            for row in self.rows
        }
        self.assertEqual(sessions, EXPECTED_SESSIONS)

    def test_each_session_has_questions_1_through_65_once(self):
        grouped = defaultdict(list)
        for row in self.rows:
            key = (row["year"], row["paper_code"], row["session"])
            grouped[key].append(int(row["question_no"]))
        for key in EXPECTED_SESSIONS:
            self.assertEqual(sorted(grouped[key]), list(range(1, 66)), key)

    def test_rows_have_valid_types_marks_and_official_source(self):
        for row in self.rows:
            with self.subTest(session=(row["year"], row["paper_code"]), q=row["question_no"]):
                self.assertIn(row["question_type"], {"MCQ", "MSQ", "NAT"})
                self.assertIn(row["marks"], {"1", "2"})
                self.assertIn(row["section"], {"GA", "CS-1", "CS-2"})
                self.assertTrue(row["official_key_or_range"].strip())
                self.assertEqual(row["verification_status"], "KEY_VERIFIED")
                self.assertTrue(row["source_url"].startswith("https://gate2026.iitg.ac.in/"))

    def test_session_has_one_consistent_official_key_url(self):
        grouped = defaultdict(set)
        for row in self.rows:
            key = (row["year"], row["paper_code"], row["session"])
            grouped[key].add(row["source_url"])
        self.assertEqual(len(grouped), 4)
        self.assertTrue(all(len(urls) == 1 for urls in grouped.values()))


if __name__ == "__main__":
    unittest.main()
