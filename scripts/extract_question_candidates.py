"""Create reviewable question candidates from local PDF text.

The output is a working file, not a verified question bank. Page images, diagrams,
equations, tables, split questions and OCR errors require human review.
"""
from __future__ import annotations

import argparse
import json
import re
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]
QUESTION_MARKER = re.compile(r"(?m)^\s*Q\.?\s*(\d{1,3})\s*[.)]?")


def extract_pages(pdf_path: Path) -> list[dict]:
    doc = fitz.open(pdf_path)
    return [
        {"page_number": index + 1, "text": page.get_text("text")}
        for index, page in enumerate(doc)
    ]


def candidates_from_pages(pages: list[dict], paper_id: str) -> list[dict]:
    candidates: list[dict] = []
    current = None
    for page in pages:
        text = page["text"]
        matches = list(QUESTION_MARKER.finditer(text))
        if not matches:
            if current is not None:
                current["text"] += "\n" + text
                current["source_page_end"] = page["page_number"]
            continue
        prefix = text[:matches[0].start()].strip()
        if current is not None and prefix:
            current["text"] += "\n" + prefix
            current["source_page_end"] = page["page_number"]
        for index, match in enumerate(matches):
            if current is not None:
                candidates.append(current)
            end = matches[index + 1].start() if index + 1 < len(matches) else len(text)
            current = {
                "paper_id": paper_id,
                "question_number": match.group(1),
                "source_page_start": page["page_number"],
                "source_page_end": page["page_number"],
                "text": text[match.start():end].strip(),
                "verification_status": "EXTRACTED_PENDING_REVIEW",
                "question_type": "UNKNOWN",
            }
    if current is not None:
        candidates.append(current)
    return candidates


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("pdf", help="Path to a local paper PDF")
    parser.add_argument("--paper-id", required=True)
    parser.add_argument("--output", default="reports/question-candidates.jsonl")
    args = parser.parse_args()

    pdf_path = Path(args.pdf).resolve()
    output = (ROOT / args.output).resolve()
    pages = extract_pages(pdf_path)
    candidates = candidates_from_pages(pages, args.paper_id)
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for row in candidates:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")
    print(f"Created {len(candidates)} candidate record(s). Manual PDF review is required.")


if __name__ == "__main__":
    main()
