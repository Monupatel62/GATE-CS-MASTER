# Project Status

**Scope:** All GATE paper codes, 1983–2026.  
**Pilot:** CS/IT.  
**Stage:** Official source inventory and generalized database schema.  
**Question corpus:** No complete historical question corpus has been extracted.

## Repository
- Repository: `Monupatel62/GATE-CS-MASTER`
- Default branch: `main`
- Active research branch: `research/foundation`
- Research changes have not been merged into main.

## Verified source facts
- IISc's official GATE 2024 archive states that the first GATE examination was in 1983.
- IIT Guwahati's official GATE 2026 downloads page advertises bulk question papers for 2007–2025 and year-wise downloads for 2021–2025.
- GATE 2026 official test-paper page lists 30 papers.
- GATE 2026 official pattern page documents MCQ, MSQ, NAT and current marking rules.
- GATE 2027 official pages state that syllabi have been revised and include RA in the two-paper combinations.
- Direct PDF text inspection now covers GATE 2025 CS-1/CS-2 papers and both official keys, plus GATE 2026 CS-1/CS-2 papers and both official keys. Each 2025 and 2026 answer-key PDF has 65 question rows. Local PDF download, SHA-256 manifest and question-level extraction remain pending.

## Pilot batch update (2026 CS-1)
- [x] Retrieved the complete official 2026 CS-1 question-paper PDF through the PDF text parser (46 pages); text extraction is available for review, but visual questions/figures need page-image review.
- [x] Retrieved the complete official 2026 CS-1 answer-key PDF (2 pages).
- [x] Added all 65 official answer-key rows for 2026 CS-1 to `research/pilot-verified-keys/2026-CS1-answer-key.csv`.
- [x] Added 195 official answer-key rows for 2025 CS-1, 2025 CS-2 and 2026 CS-2 to `research/pilot-verified-keys/2025-CS1-CS2-and-2026-CS2-answer-keys.csv`.
- [x] Total answer-key records transcribed from official PDFs in this pilot: 260 across four CS sessions (Q1–Q65 each).
- [ ] Match all 65 question statements to the key and review PDF extraction errors/figures.
- [ ] Write and independently check detailed solutions and subject/topic tags.

## Progress tracker
| Work item | Status |
|---|---|
| Years researched | 0 full year inventories complete; official archive pages inspected for 2023–2026 and historical archive coverage leads recorded |
| Paper codes discovered | 30 official 2026 codes + RA listed for 2027 + IT historical lead (unverified) |
| Papers discovered | 4 CS session papers and 4 matching keys directly inspected; all-code inventory partial |
| Papers downloaded and hashed | 0 local files confirmed; 2026 CS-1 PDF parsed remotely; local hash manifest pending |
| Questions extracted | 0 fully verified question-text batches; 2026 CS-1 PDF text parsed for pilot review |
| Questions verified | 260 official answer-key rows transcribed across 4 sessions; question-text-to-key matching pending |
| Solutions completed | 0 |
| Missing papers documented | Preliminary only |
| Errors remaining | Not yet measured |

## Tooling and repository layout
- [x] Generalized SQLite schema for all paper codes, sessions, sets and sections.
- [x] Paper-code/year availability matrix (1983–2026) and separate CS pilot leads.
- [x] Local PDF manifest and question-candidate extraction scripts.
- [x] Reference seeding and CSV/JSONL export scripts.
- [x] Paper-code folders, report templates and schema tests added.
- [ ] Execute tests in GitHub Actions; no CI result has been recorded yet.

## Next steps
1. Enumerate official 2026/2025/2024/2023 paper and answer-key links for all codes.
2. Complete CS/IT pilot year/session PDF and key inventory.
3. Validate extraction and database workflow on pilot papers.
4. Extend to all paper codes.
5. Research introduction/retirement years using official year-specific brochures.
6. Build historical pattern and syllabus timelines.
7. Generate CSV/JSONL/SQLite only from source-verified records.

A paper is not verified because an index lists it. A question is not verified until its text is checked against the original paper. An official answer is not verified until matched to the official key for the same paper/session/version.
