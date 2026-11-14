"""Export verified question records from SQLite to CSV and JSONL."""
from __future__ import annotations

import argparse
import csv
import json
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "questions.sqlite"
FIELDS = [
    "question_id", "year", "paper_code", "session_label", "set_label",
    "section_code", "section_name", "question_number", "subject_name",
    "topic_name", "subtopic_name", "question_type", "marks",
    "original_question_text", "official_answer_text",
    "independently_derived_answer", "difficulty", "source_page_start",
    "source_page_end", "paper_source_url", "answer_key_source_url",
    "extraction_confidence", "verification_status",
]


def rows(conn: sqlite3.Connection):
    query = """
    SELECT
      q.question_id, e.year, o.paper_code, s.session_label, p.set_label,
      sec.section_code, sec.section_name, q.question_number,
      subj.subject_name, t.topic_name, st.subtopic_name, q.question_type,
      q.marks, q.original_question_text, q.official_answer_text,
      q.independently_derived_answer, q.difficulty, q.source_page_start,
      q.source_page_end, paper_src.source_url, key_src.source_url,
      q.extraction_confidence, q.verification_status
    FROM questions q
    JOIN paper_sets p ON p.paper_id = q.paper_id
    JOIN paper_sessions s ON s.session_id = p.session_id
    JOIN exam_paper_offerings o ON o.offering_id = s.offering_id
    JOIN examinations e ON e.year = o.year
    LEFT JOIN paper_sections sec ON sec.section_id = q.section_id
    LEFT JOIN source_documents paper_src ON paper_src.source_id = p.paper_source_id
    LEFT JOIN source_documents key_src ON key_src.source_id = p.answer_key_source_id
    LEFT JOIN subjects subj ON subj.subject_id = q.subject_id
    LEFT JOIN topics t ON t.topic_id = q.topic_id
    LEFT JOIN subtopics st ON st.subtopic_id = q.subtopic_id
    ORDER BY e.year, o.paper_code, s.session_label, p.set_label, q.question_number
    """
    cursor = conn.execute(query)
    for row in cursor:
        yield dict(zip(FIELDS, row))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--csv", default="database/all-questions.csv")
    parser.add_argument("--jsonl", default="database/all-questions.jsonl")
    args = parser.parse_args()

    if not DB_PATH.exists():
        raise SystemExit("Database not found. Run scripts/init_database.py first.")

    csv_path = ROOT / args.csv
    jsonl_path = ROOT / args.jsonl
    csv_path.parent.mkdir(parents=True, exist_ok=True)
    jsonl_path.parent.mkdir(parents=True, exist_ok=True)

    with sqlite3.connect(DB_PATH) as conn:
        records = list(rows(conn))

    with csv_path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELDS)
        writer.writeheader()
        writer.writerows(records)

    with jsonl_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")

    print(f"Exported {len(records)} question record(s) to CSV and JSONL.")


if __name__ == "__main__":
    main()
