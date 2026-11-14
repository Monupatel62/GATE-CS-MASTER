# Pilot official answer-key audit

This directory contains the answer-key transcription for the first four CS pilot sessions.

| Year | Paper | Session | Rows | Official key |
|---|---|---:|---:|---|
| 2025 | CS-1 | 1 | 65 | [PDF](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS1_Keys.pdf) |
| 2025 | CS-2 | 2 | 65 | [PDF](https://gate2026.iitg.ac.in/doc/download/2025_Key/CS2_Keys.pdf) |
| 2026 | CS-1 | 3 | 65 | [PDF](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS1_Keys.pdf) |
| 2026 | CS-2 | 4 | 65 | [PDF](https://gate2026.iitg.ac.in/doc/download/2026/Keys/CS2_Keys.pdf) |
| **Total** | | | **260** | |

## Audit performed

Every row was compared with the matching official PDF for question number, session, question type, section, official key/accepted NAT range and marks. The 2026 CS-2 transcription initially contained 19 incorrect answer values. Those values were corrected from the official PDF. Its NAT values were also normalized to the range format printed in the key.

A second full comparison after correction found **260 rows checked and zero remaining field mismatches**.

The CSV status KEY_VERIFIED applies only to the official answer-key row. It does not mean that the corresponding question statement has been extracted or matched. No question in this pilot is yet marked QUESTION_AND_KEY_VERIFIED.

## Re-run checks

```bash
python -m unittest discover -s tests -v
```

The source PDFs were inspected through remote PDF text parsing. They have not yet been downloaded locally or SHA-256 hashed. The CSV files contain answer-key data only; full question-paper text and copyrighted paper assets are not included here.
