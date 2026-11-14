from pathlib import Path
import sqlite3
import unittest

ROOT = Path(__file__).resolve().parents[1]
SCHEMA = ROOT / "database" / "schema.sql"


class SchemaTests(unittest.TestCase):
    def setUp(self):
        self.db = sqlite3.connect(":memory:")
        self.db.execute("PRAGMA foreign_keys = ON")
        self.db.executescript(SCHEMA.read_text(encoding="utf-8"))

    def tearDown(self):
        self.db.close()

    def test_schema_integrity_and_expected_tables(self):
        self.assertEqual(self.db.execute("PRAGMA integrity_check").fetchone()[0], "ok")
        names = {
            row[0] for row in self.db.execute(
                "SELECT name FROM sqlite_master WHERE type='table'"
            )
        }
        expected = {
            "paper_codes", "examinations", "source_documents",
            "exam_paper_offerings", "paper_sessions", "paper_sets",
            "paper_sections", "questions", "question_options",
            "question_assets", "answer_key_items", "solutions",
            "syllabus_versions", "syllabus_topics",
            "question_syllabus_mapping", "similarity_groups",
            "similarity_members", "verification_events", "extraction_batches",
        }
        self.assertTrue(expected.issubset(names))

    def test_question_identity_is_scoped_to_paper(self):
        self.db.execute(
            "INSERT INTO paper_codes(paper_code,paper_name) VALUES('CS','Computer Science')"
        )
        self.db.execute("INSERT INTO examinations(year) VALUES(2026)")
        self.db.execute(
            "INSERT INTO exam_paper_offerings(offering_id,year,paper_code,offering_status) "
            "VALUES('CS26',2026,'CS','EVIDENCE_FOUND')"
        )
        self.db.execute(
            "INSERT INTO paper_sessions(session_id,offering_id,session_label) "
            "VALUES('CS26-1','CS26','CS-1')"
        )
        self.db.execute(
            "INSERT INTO paper_sets(paper_id,session_id,set_label) "
            "VALUES('CS26-1-MASTER','CS26-1','MASTER')"
        )
        self.db.execute(
            "INSERT INTO questions(question_id,paper_id,question_number,original_question_text) "
            "VALUES('CS26-1-Q1','CS26-1-MASTER','1','sample question')"
        )
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO questions(question_id,paper_id,question_number,original_question_text) "
                "VALUES('CS26-1-Q1-DUP','CS26-1-MASTER','1','duplicate number')"
            )
        self.assertEqual(
            self.db.execute("SELECT COUNT(*) FROM questions").fetchone()[0], 1
        )

    def test_foreign_keys_are_enforced(self):
        with self.assertRaises(sqlite3.IntegrityError):
            self.db.execute(
                "INSERT INTO exam_paper_offerings(offering_id,year,paper_code) "
                "VALUES('BAD',2099,'MISSING')"
            )


if __name__ == "__main__":
    unittest.main()
