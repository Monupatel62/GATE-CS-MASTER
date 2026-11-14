"""Tests for question-candidate extraction audit summaries."""
import unittest

from scripts.audit_question_candidates import audit_rows


class AuditQuestionCandidatesTests(unittest.TestCase):
    def test_reports_missing_and_duplicate_question_numbers(self):
        rows = [
            {"paper_id": "GATE-2026-CS1", "question_number": "1", "verification_status": "PENDING"},
            {"paper_id": "GATE-2026-CS1", "question_number": "2", "verification_status": "PENDING"},
            {"paper_id": "GATE-2026-CS1", "question_number": "2", "verification_status": "PENDING"},
            {"paper_id": "GATE-2026-CS1", "question_number": "66", "verification_status": "PENDING"},
        ]
        report = audit_rows(rows, expected_questions=3)[0]
        self.assertEqual(report["candidate_records"], 4)
        self.assertEqual(report["unique_question_numbers"], 3)
        self.assertEqual(report["missing_question_numbers"], "3")
        self.assertEqual(report["duplicate_question_numbers"], "2")
        self.assertEqual(report["out_of_range_question_numbers"], "66")
        self.assertEqual(report["pending_review_records"], 4)

    def test_keeps_papers_separate(self):
        rows = [
            {"paper_id": "2025-CS1", "question_number": "1", "verification_status": "PENDING"},
            {"paper_id": "2025-CS2", "question_number": "1", "verification_status": "PENDING"},
        ]
        reports = audit_rows(rows, expected_questions=1)
        self.assertEqual([r["paper_id"] for r in reports], ["2025-CS1", "2025-CS2"])
        self.assertTrue(all(r["missing_question_numbers"] == "" for r in reports))


if __name__ == "__main__":
    unittest.main()
