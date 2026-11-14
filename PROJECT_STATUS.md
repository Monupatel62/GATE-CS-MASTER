# Project Status

**Stage:** Source-backed research foundation initialized.  
**Question corpus:** No question records extracted or verified yet.

## Repository
- Repository: `Monupatel62/GATE-CS-MASTER`
- Default branch: `main`
- Research branch: `research/foundation`
- No research branch changes have been merged into main.

## Inspected findings (2026-11-14)
- IIT Guwahati's official 2026 master-paper/key page lists CS-1 (Forenoon) and CS-2 (Afternoon).
- The 2026 official downloads page advertises bulk papers for 2007–2025 and year-wise papers for 2021–2025.
- IIT Roorkee's official 2025 page provides master paper/key listings and explains key ordering and question-type rules.
- IIT Kanpur's official 2023 papers/keys page lists CS.
- PreviousYearPapers.in lists CS PDFs 1991–2015 and two 2016 session files (third-party lead).
- GATE Overflow lists historical CSE materials from 1987 onward and labels some older IT items separately (community lead).
- NPTEL has a paper mapping page for further discovery.

See `research/INITIAL_FINDINGS.md` and `research/source-register.csv`.

## Completed
- [x] Repository and write access checked.
- [x] README and research method created.
- [x] SQLite schema and subject taxonomy created.
- [x] Year inventory initialized conservatively.
- [x] Official pages for 2023, 2025 and 2026 inspected.
- [x] Historical discovery indexes inspected.

## Pending
- [ ] Extract direct official PDF/key links from every archive.
- [ ] Enumerate every CS year/session/set.
- [ ] Inspect historical original PDFs (especially 1987–2006 leads).
- [ ] Establish earliest actual CS-paper year with evidence.
- [ ] Resolve legacy CS vs IT labels.
- [ ] Download permitted originals and record SHA-256/page counts.
- [ ] Extract questions and check against PDF pages.
- [ ] Verify official key versions and solutions.
- [ ] Map historical syllabus versions.
- [ ] Populate SQLite and produce matching CSV/JSONL exports.
- [ ] Run provenance, integrity, duplicate and completeness tests.

## Status vocabulary
- NOT_ESTABLISHED
- PAPER_CONDUCTED_EVIDENCE_FOUND
- PAPER_NOT_CONDUCTED_EVIDENCE_FOUND
- PAPER_LISTED_SOURCE_UNVERIFIED
- ORIGINAL_PDF_VERIFIED
- EXTRACTED_PENDING_REVIEW
- QUESTION_TEXT_VERIFIED
- OFFICIAL_KEY_VERIFIED
- INDEPENDENT_SOLUTION_CHECKED

No year/session or question count is claimed complete without evidence.
