"""Inspect local GATE PDFs and write a provenance manifest.

This tool does not download papers. Place permitted working copies under papers/
and retain each original source URL in the source register.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
from datetime import datetime, timezone
from pathlib import Path

import fitz

ROOT = Path(__file__).resolve().parents[1]


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def inspect(path: Path) -> dict[str, str | int]:
    doc = fitz.open(path)
    first_page = doc[0].get_text("text")[:1200] if doc.page_count else ""
    return {
        "relative_path": str(path.relative_to(ROOT)),
        "filename": path.name,
        "size_bytes": path.stat().st_size,
        "page_count": doc.page_count,
        "sha256": sha256_file(path),
        "first_page_text_preview": " ".join(first_page.split()),
        "inspected_at_utc": datetime.now(timezone.utc).isoformat(),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", default="papers")
    parser.add_argument("--output", default="reports/pdf-manifest.csv")
    args = parser.parse_args()

    directory = (ROOT / args.directory).resolve()
    output = (ROOT / args.output).resolve()
    rows = [inspect(path) for path in sorted(directory.rglob("*.pdf"))]
    output.parent.mkdir(parents=True, exist_ok=True)
    fields = list(rows[0].keys()) if rows else [
        "relative_path", "filename", "size_bytes", "page_count",
        "sha256", "first_page_text_preview", "inspected_at_utc"
    ]
    with output.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Inspected {len(rows)} PDF(s); manifest: {output}")


if __name__ == "__main__":
    main()
