# GATE Master Research Database

A source-traceable research database for GATE examination papers and questions from 1983 through 2026.

## Scope
- All GATE paper codes, not CS alone.
- CS/IT is the first pilot dataset.
- Every year, paper, session, set and optional section is a separate record.
- Historical introduction and retirement years are researched, not guessed.
- Primary store: SQLite. Exports: CSV and JSONL.
- Question text, official key, independent solution and verification evidence remain separate.

## Research integrity
- GATE beginning in 1983 does not prove every modern paper code existed in 1983.
- Never fabricate missing papers, questions, answer keys, solutions, marks, codes or source URLs.
- Third-party indexes are discovery leads; verify against original documents.
- Preserve historical labels such as CS and IT exactly as printed.
- Do not apply current syllabus or marking rules retrospectively.
- Track optional sections and paper-specific question structures.
- Do not claim completion until inventory and validation reports support it.

## Repository layout
- `research/`: historical inventory, source register, pattern and syllabus history.
- `database/`: SQLite schema and generated database.
- `papers/`: source PDFs and organized paper collections (subject to source terms).
- `solutions/`: reviewed solutions.
- `analytics/`: frequency, repetition and syllabus analysis.
- `reports/`: extraction, verification and missing-data reports.
- `tests/`: database, extraction and mock-test checks.

## Current status
The project is in the source-inventory and schema stage. No full historical corpus is claimed. See `PROJECT_STATUS.md`.

Start with `research/official-sources.md` and `research/source-register.csv`.
