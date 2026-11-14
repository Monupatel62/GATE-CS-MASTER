"""Seed reference rows from the reviewed paper-code registry.

Unknown historical offerings remain NOT_RESEARCHED; they are not asserted to
have existed in those years.
"""
from __future__ import annotations

import csv
import sqlite3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "research" / "paper-code-registry.csv"


def optional_int(value: str) -> int | None:
    value = (value or "").strip()
    return int(value) if value else None


def seed(conn: sqlite3.Connection) -> None:
    with REGISTRY.open(newline="", encoding="utf-8") as handle:
        rows = list(csv.DictReader(handle))

    for year in range(1983, 2028):
        conn.execute(
            "INSERT OR IGNORE INTO examinations(year,historical_status) VALUES(?,?)",
            (year, "NOT_RESEARCHED"),
        )

    for row in rows:
        code = row["paper_code"].strip().upper()
        first_year = optional_int(row.get("first_official_listing_year", ""))
        last_year = optional_int(row.get("last_official_listing_year", ""))
        conn.execute(
            """INSERT OR IGNORE INTO paper_codes
               (paper_code,paper_name,first_official_listing_year,
                last_official_listing_year,introduction_status,notes)
               VALUES(?,?,?,?,?,?)""",
            (
                code,
                row["paper_name"].strip(),
                first_year,
                last_year,
                row.get("introduction_status", "UNVERIFIED").strip(),
                row.get("notes", "").strip(),
            ),
        )

        start = first_year if first_year is not None else 1983
        end = last_year if last_year is not None else 2026
        for year in range(max(1983, start), min(2027, end + 1)):
            conn.execute(
                """INSERT OR IGNORE INTO exam_paper_offerings
                   (offering_id,year,paper_code,offering_status,evidence_notes)
                   VALUES(?,?,?,?,?)""",
                (
                    f"{year}-{code}",
                    year,
                    code,
                    "NOT_RESEARCHED",
                    "Inventory placeholder only; paper offering must be established from year-specific evidence.",
                ),
            )


if __name__ == "__main__":
    from scripts.init_database import DB_PATH

    with sqlite3.connect(DB_PATH) as connection:
        connection.execute("PRAGMA foreign_keys = ON")
        seed(connection)
        connection.commit()
