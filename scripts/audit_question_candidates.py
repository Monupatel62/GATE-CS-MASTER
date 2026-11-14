"""Audit local extracted question-candidate JSONL without publishing question text."""
from __future__ import annotations

import argparse
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def audit_rows(rows: list[dict], expected_questions: int = 65) -> list[dict[str, str | int]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[str(row.get("paper_id", "UNKNOWN"))].append(row)

    reports = []
    expected = set(range(1, expected_questions + 1))
    for paper_id, paper_rows in sorted(grouped.items()):
        numbers = []
        for row in paper_rows:
            try:
                numbers.append(int(str(row["question_number"]).strip()))
            except (KeyError, TypeError, ValueError):
                continue
        counts = Counter(numbers)
        present = set(numbers)
        reports.append({
            "paper_id": paper_id,
            "candidate_records": len(paper_rows),
            "unique_question_numbers": len(present),
            "expected_question_count": expected_questions,
            "missing_question_numbers": ";".join(map(str, sorted(expected - present))),
            "duplicate_question_numbers": ";".join(
                map(str, sorted(number for number, count in counts.items() if count > 1))
            ),
            "out_of_range_question_numbers": ";".join(
                map(str, sorted(number for number in present if number not in expected))
            ),
            "pending_review_records": sum(
                row.get("verification_status") != "QUESTION_AND_KEY_VERIFIED"
                for row in paper_rows
            ),
        })
    return reports


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("input", help="Question-candidate JSONL created by extract_question_candidates.py")
    parser.add_argument("--expected", type=int, default=65)
    parser.add_argument("--output", default="reports/question-extraction-audit.csv")
    args = parser.parse_args()

    source = Path(args.input)
    if not source.is_absolute():
        source = ROOT / source
    rows = []
    with source.open(encoding="utf-8") as handle:
        for line_number, line in enumerate(handle, start=1):
            if not line.strip():
                continue
            try:
                rows.append(json.loads(line))
            except json.JSONDecodeError as exc:
                raise SystemExit(f"Invalid JSON on line {line_number}: {exc}") from exc

    reports = audit_rows(rows, args.expected)
    output = Path(args.output)
    if not output.is_absolute():
        output = ROOT / output
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "paper_id", "candidate_records", "unique_question_numbers",
        "expected_question_count", "missing_question_numbers",
        "duplicate_question_numbers", "out_of_range_question_numbers",
        "pending_review_records",
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(reports)
    print(f"Audited {len(rows)} candidate record(s) across {len(reports)} paper(s).")
    print(f"Report: {output}")


if __name__ == "__main__":
    main()
