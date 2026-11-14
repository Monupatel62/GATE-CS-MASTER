# Pilot question-paper extraction audit

## Scope

This report records remote PDF-to-Markdown parser output for the four official CS pilot papers. It contains extraction metadata only, not copied question statements.

| Year | Paper | PDF pages | Unique question labels found | Expected | Parser image markers | Result |
|---|---|---:|---:|---:|---:|---|
| 2025 | CS-1 | 64 | 65 | 65 | 6 | All question labels detected; visual review still required |
| 2025 | CS-2 | 48 | 65 | 65 | 0 | All unique labels detected; repeated labels occur in extracted text |
| 2026 | CS-1 | 46 | 53 | 65 | 16 | Incomplete marker extraction |
| 2026 | CS-2 | 42 | 49 | 65 | 6 | Incomplete marker extraction |

## What this does and does not establish

- The two 2025 PDFs yielded all 65 unique question labels in the remote Markdown parse.
- The 2025 CS-2 parse contains repeated question-label occurrences. Repetition may be a parser artifact or cross-reference; it is not counted as an additional question.
- The 2026 parses did not expose all 65 question labels. Missing labels in this report mean the parser did not identify them; they are not proof that questions are absent from the source PDFs.
- Image-marker counts are parser placeholders, not a reliable count of diagrams. A zero count does not prove that a paper contains no visual content.
- Math-block counts are approximate parser markers, not a correctness check.
- None of the four question texts has been manually checked against page images, and none has been matched to its official key row.
- The source PDFs were fetched remotely for parsing. They were not downloaded into the repository, and no local SHA-256 hashes exist.

## Required next work

1. Obtain permitted local working copies of the four official PDFs.
2. Run `scripts/inspect_pdfs.py` to create the local provenance and SHA-256 manifest.
3. Run `scripts/extract_question_candidates.py` separately for each paper.
4. Run `scripts/audit_question_candidates.py` on the resulting JSONL and resolve missing/duplicate labels.
5. Compare every candidate, option, equation and visual asset with the original PDF page.
6. Match the reviewed question to the audited answer key; only then use QUESTION_AND_KEY_VERIFIED.

## Reproducible candidate audit

```bash
python scripts/audit_question_candidates.py reports/question-candidates.jsonl --expected 65
```

This command reports question-number coverage only. It does not certify question wording, diagrams, options or answers.
