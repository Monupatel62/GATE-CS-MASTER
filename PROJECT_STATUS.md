# Project Status

**Stage:** Research foundation initialized.  
**Data status:** No question records have yet been extracted or verified.

## Confirmed repository state
- Repository: `Monupatel62/GATE-CS-MASTER`
- Default branch: `main`
- Research work is being organized separately from `main`.

## Research principles
1. First establish when GATE CS was actually offered; do not assume the CS paper existed in every year beginning in 1983.
2. Inventory every paper/session/set separately.
3. For each paper, record original question-paper source, answer-key source, local file checksum, page count, source type, and verification status.
4. Use official GATE/IIT/IISc sources as primary evidence.
5. Use third-party archives only to discover leads unless their files can be corroborated.
6. Never claim completeness based only on an index or a third-party page listing.
7. Extract in batches; review the source PDF alongside extracted text.
8. Publish only records with clear provenance and confidence/status fields.

## Work completed
- [x] Repository existence, visibility, default branch, and access checked.
- [x] Initial README created.
- [ ] Historical GATE CS year-by-year inventory.
- [ ] Session/set enumeration.
- [ ] Official PDF and answer-key retrieval.
- [ ] Historical syllabus version inventory.
- [ ] Question extraction and source-page verification.
- [ ] Answer-key verification.
- [ ] Detailed solutions.
- [ ] SQLite population and export parity checks.

## Critical status definitions
- `NOT_ESTABLISHED`: no conclusion about whether the CS paper existed.
- `PAPER_CONDUCTED_EVIDENCE_FOUND`: evidence supports that a CS paper was conducted.
- `PAPER_NOT_CONDUCTED_EVIDENCE_FOUND`: evidence supports no CS paper was conducted.
- `PAPER_LISTED_SOURCE_UNVERIFIED`: index/listing found, original PDF not yet checked.
- `ORIGINAL_PDF_VERIFIED`: original paper inspected and identified.
- `EXTRACTED_PENDING_REVIEW`: machine extraction exists but has not been checked.
- `QUESTION_TEXT_VERIFIED`: question text checked against source PDF.
- `OFFICIAL_KEY_VERIFIED`: answer checked against official key.
- `INDEPENDENT_SOLUTION_CHECKED`: solution independently worked and reviewed.

Do not treat a year as missing merely because the first search did not find it.
