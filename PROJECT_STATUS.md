# Project Status

**Scope:** All GATE paper codes, 1983–2026.  
**Pilot:** CS-1 and CS-2 sessions for 2025 and 2026.  
**Stage:** Official pilot answer-key audit complete; remote question-PDF extraction coverage audited; local extraction and question-to-key matching remain pending.

## Repository
- Repository: Monupatel62/GATE-CS-MASTER
- Default branch: main
- Active research branch: research/foundation
- Research changes have not been merged into main.

## Verified source facts
- IISc's official GATE 2024 archive states that the first GATE examination was in 1983. This does not establish when any particular paper code began.
- IIT Guwahati's official GATE 2026 downloads page advertises bulk question papers for 2007–2025 and year-wise downloads for 2021–2025.
- GATE 2026 official test-paper page lists 30 papers.
- GATE 2026 official pattern page documents MCQ, MSQ, NAT and current marking rules.
- GATE 2027 official pages state that syllabi were revised and include RA in the two-paper combinations.
- Four pilot question-paper PDFs and their four matching official answer-key PDFs have been inspected through remote PDF text parsing. These remote parses are not local downloads and do not have local SHA-256 hashes.

## Pilot answer-key audit
- [x] Transcribed 65 rows for 2025 CS-1 (session 1).
- [x] Transcribed 65 rows for 2025 CS-2 (session 2).
- [x] Transcribed 65 rows for 2026 CS-1 (session 3).
- [x] Transcribed 65 rows for 2026 CS-2 (session 4).
- [x] Compared all 260 CSV records against the corresponding official answer-key PDF rows: question number, session, type, section, answer/key range and marks.
- [x] Corrected 19 incorrect answer values found in the 2026 CS-2 transcription; standardized its NAT values to the official PDF's printed ranges.
- [x] Repeated the full comparison after correction: 260 official rows checked, 0 remaining field mismatches.
- [x] Run a remote PDF-to-Markdown extraction coverage audit for all four pilot papers; publish metadata-only report.
- [ ] Match the 260 key rows to the question text from the corresponding official question papers.
- [ ] Review question-paper extraction errors, diagrams, tables and page layout manually.
- [ ] Write and independently check detailed solutions and subject/topic tags.

**Important status distinction:** 260 answer-key records are now KEY_VERIFIED against official key PDFs. Zero question-text records have yet reached QUESTION_AND_KEY_VERIFIED.

## Progress tracker
| Work item | Status |
|---|---|
| Years researched | 0 full year inventories complete; official archive pages inspected for 2023–2026 and historical archive leads recorded |
| Paper codes discovered | 30 official 2026 codes + RA listed for 2027 + IT historical lead (unverified) |
| Papers discovered | 4 CS session papers and 4 matching official keys directly inspected |
| Papers downloaded and hashed | 0 local files confirmed; remote PDF parsing only; local SHA-256 manifest pending |
| Questions extracted | 0 reviewed question-text batches; remote parser detected 65/65 labels in 2025 CS-1, 65/65 in 2025 CS-2, 53/65 in 2026 CS-1 and 49/65 in 2026 CS-2; this is label coverage only |
| Answer-key rows verified | 260 / 260 against official PDFs; 0 remaining field mismatches |
| Question text matched to keys | 0 |
| Solutions completed | 0 |
| Topic mappings completed | 0 |
| Database question records | 0 verified question records |
| CSV / JSONL question exports | Header-only / empty; not complete exports |
| Missing papers documented | Preliminary only |
| Errors remaining | Question extraction and visual review errors not yet measured |

## Tooling and repository layout
- [x] Generalized SQLite schema for all paper codes, sessions, sets and sections.
- [x] Paper-code/year availability matrix (1983–2026) and separate CS pilot leads.
- [x] Local PDF manifest and question-candidate extraction scripts.
- [x] Reference seeding and CSV/JSONL export scripts.
- [x] Paper-code folders, report templates and schema tests added.
- [x] Automated tests added for the four pilot answer-key CSVs.
- [x] Added a reusable local JSONL candidate-coverage audit script and tests.
- [x] Added an official-host-only downloader for the four pilot question PDFs and four answer-key PDFs; it verifies the PDF signature and writes SHA-256/page-count metadata.
- [x] Added a metadata-only remote extraction coverage report; no question text copied into the report.
- [ ] Confirm the latest answer-key, candidate-audit and database tests pass in GitHub Actions.
- [ ] Run the new downloader locally; no PDFs or local SHA-256 manifest have been produced yet.

## Next steps
1. Download permitted pilot source PDFs locally and create the SHA-256 manifest.
2. Build a page-aware extraction workflow and review every question against its original PDF, including diagrams and tables.
3. Match the extracted question records to the already audited official keys.
4. Independently solve questions and map them to year-specific syllabi.
5. Populate SQLite and generate reproducible exports only from reviewed records.
6. Complete the historical CS/IT inventory, then expand to all paper codes.
7. Research introduction/retirement years using official year-specific brochures.

A paper is not verified because an index lists it. An answer key is verified only against its official key PDF. A question is not QUESTION_AND_KEY_VERIFIED until its text and matching official answer are both checked.
