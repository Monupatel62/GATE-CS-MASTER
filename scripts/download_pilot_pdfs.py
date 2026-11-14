"""Download the four official CS pilot question papers and answer keys locally.

The PDFs are working copies for extraction and review. They are intentionally ignored
by Git; only source URLs, sizes, hashes and review metadata belong in the repository.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import os
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import fitz
import requests

ROOT = Path(__file__).resolve().parents[1]
OFFICIAL_HOST = "gate2026.iitg.ac.in"
SOURCES = [
    {"year": 2025, "paper_code": "CS", "session": "1", "kind": "QUESTION_PAPER",
     "url": "https://gate2026.iitg.ac.in/doc/download/2025/CS12025.pdf",
     "filename": "GATE-2025-CS1-question-paper.pdf"},
    {"year": 2025, "paper_code": "CS", "session": "2", "kind": "QUESTION_PAPER",
     "url": "https://gate2026.iitg.ac.in/doc/download/2025/CS22025.pdf",
     "filename": "GATE-2025-CS2-question-paper.pdf"},
    {"year": 2026, "paper_code": "CS", "session": "1", "kind": "QUESTION_PAPER",
     "url": "https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS1.pdf",
     "filename": "GATE-2026-CS1-question-paper.pdf"},
    {"year": 2026, "paper_code": "CS", "session": "2", "kind": "QUESTION_PAPER",
     "url": "https://gate2026.iitg.ac.in/doc/download/2026/QPs/CS2.pdf",
     "filename": "GATE-2026-CS2-question-paper.pdf"},
    {"year": 2025, "paper_code": "CS", "session": "1", "kind": "ANSWER_KEY",
     "url": "https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf",
     "filename": "GATE-2025-CS1-answer-key.pdf"},
    {"year": 2025, "paper_code": "CS", "session": "2", "kind": "ANSWER_KEY",
     "url": "https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf",
     "filename": "GATE-2025-CS2-answer-key.pdf"},
    {"year": 2026, "paper_code": "CS", "session": "1", "kind": "ANSWER_KEY",
     "url": "https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf",
     "filename": "GATE-2026-CS1-answer-key.pdf"},
    {"year": 2026, "paper_code": "CS", "session": "2", "kind": "ANSWER_KEY",
     "url": "https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf",
     "filename": "GATE-2026-CS2-answer-key.pdf"},
]


def is_official_url(url: str) -> bool:
    parsed = urlparse(url)
    return parsed.scheme == "https" and parsed.hostname == OFFICIAL_HOST


def is_pdf_payload(payload: bytes) -> bool:
    return payload.startswith(b"%PDF-")


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def download_source(source: dict, output_dir: Path, timeout: int = 45) -> dict:
    url = source["url"]
    if not is_official_url(url):
        raise ValueError(f"Refusing non-official source URL: {url}")

    response = requests.get(
        url,
        timeout=timeout,
        headers={"User-Agent": "GATE-CS-MASTER-research/1.0"},
    )
    response.raise_for_status()
    payload = response.content
    if not is_pdf_payload(payload):
        raise ValueError(f"Response is not a PDF: {url}")
    if not payload:
        raise ValueError(f"Empty PDF response: {url}")

    output_dir.mkdir(parents=True, exist_ok=True)
    destination = output_dir / source["filename"]
    temporary = destination.with_suffix(destination.suffix + ".part")
    temporary.write_bytes(payload)
    os.replace(temporary, destination)

    with fitz.open(destination) as document:
        page_count = document.page_count

    return {
        "year": source["year"],
        "paper_code": source["paper_code"],
        "session": source["session"],
        "document_type": source["kind"],
        "source_url": url,
        "local_path": str(destination.relative_to(ROOT)),
        "size_bytes": len(payload),
        "page_count": page_count,
        "sha256": sha256_bytes(payload),
        "retrieved_at_utc": datetime.now(timezone.utc).isoformat(),
        "download_status": "DOWNLOADED_HASHED",
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", default="papers/raw")
    parser.add_argument("--manifest", default="reports/pilot-source-downloads.csv")
    parser.add_argument("--timeout", type=int, default=45)
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    if not output_dir.is_absolute():
        output_dir = ROOT / output_dir
    manifest = Path(args.manifest)
    if not manifest.is_absolute():
        manifest = ROOT / manifest

    rows = []
    failures = []
    for source in SOURCES:
        try:
            row = download_source(source, output_dir, args.timeout)
            rows.append(row)
            print(f"OK {source['year']} {source['kind']} CS-{source['session']}: {row['size_bytes']} bytes, {row['page_count']} pages")
        except (requests.RequestException, OSError, ValueError) as exc:
            failures.append((source["filename"], str(exc)))
            print(f"FAILED {source['filename']}: {exc}")

    manifest.parent.mkdir(parents=True, exist_ok=True)
    fields = [
        "year", "paper_code", "session", "document_type", "source_url",
        "local_path", "size_bytes", "page_count", "sha256",
        "retrieved_at_utc", "download_status",
    ]
    with manifest.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)

    print(f"Downloaded and hashed {len(rows)}/{len(SOURCES)} official PDFs.")
    print(f"Manifest: {manifest}")
    if failures:
        raise SystemExit(f"{len(failures)} download(s) failed; see messages above.")


if __name__ == "__main__":
    main()
