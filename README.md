# GATE CS Master Research Database

A source-traceable research project for GATE Computer Science & Information Technology (CS) previous-year papers, questions, answer keys, solutions, syllabus history, and analysis.

## Scope
- Research window: 1983–2026 (availability must be evidenced year by year).
- Paper: GATE CS only.
- Primary store: SQLite.
- Export formats: JSONL and CSV.
- Every question must retain source provenance and an explicit verification state.

## Research integrity
- Do not infer that a CS paper was or was not conducted in a year without evidence.
- Do not invent missing questions, answer keys, question numbering, marks, sessions, or source URLs.
- Preserve original question wording and source page references.
- Keep official answer keys separate from independently derived answers.
- Keep historical syllabus mapping separate from current syllabus mapping.
- Treat third-party archives as discovery sources unless corroborated by primary documents.
- Record missing, ambiguous, low-quality, and disputed records explicitly.

## Current status
This repository has just been initialized. No historical question corpus is claimed to have been extracted or verified yet.

See:
- `PROJECT_STATUS.md`
- `research/source-register.csv`
- `research/paper-availability.csv`
- `database/schema.sql`

## Getting started
```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
python scripts/init_database.py
python scripts/validate_database.py
```
