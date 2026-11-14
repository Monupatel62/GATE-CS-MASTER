from pathlib import Path
import sqlite3
import sys

ROOT = Path(__file__).resolve().parents[1]
DB_PATH = ROOT / "database" / "gate_cs.sqlite"

def main() -> int:
    if not DB_PATH.exists():
        print("Database missing. Run scripts/init_database.py first.")
        return 2
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        integrity = conn.execute("PRAGMA integrity_check").fetchone()[0]
        foreign_key_errors = conn.execute("PRAGMA foreign_key_check").fetchall()
        table_count = conn.execute(
            "SELECT COUNT(*) FROM sqlite_master WHERE type='table'"
        ).fetchone()[0]
    print({
        "integrity": integrity,
        "foreign_key_errors": len(foreign_key_errors),
        "table_count": table_count,
    })
    return 0 if integrity == "ok" and not foreign_key_errors else 1

if __name__ == "__main__":
    sys.exit(main())
