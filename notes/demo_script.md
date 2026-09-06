# Demo Video Script (target: under 8 minutes)

## Required elements (from assessment): clean run, output, failure/recovery, tests, one code-level decision explained

## Segment 1 — Introduction (30 sec)
- State name, track (Track 04), and what the system does in one sentence
- Show the project folder structure briefly (src/, tests/, configs/, data/, notes/)

## Segment 2 — Clean setup and run (90 sec)
- Show activating the venv from scratch: `venv\Scripts\Activate.ps1`
- Run the CLI on a real input file:
  `python cli.py --input data/test_inputs.json --target hi --output data/output_hi.json`
- Open the output JSON, point out: translated_text, review_status fields present

## Segment 3 — Show a real failure and recovery (90 sec)
- Open notes/failures.md, briefly show F001-F005
- Pick ONE to demo live: e.g. F002 (naive regex over-matched "Hello"/"Visit")
  - Show the old broken regex briefly (can just describe it, don't need old code)
  - Show the current glossary-based fix in entity_protect.py
  - Explain WHY glossary is better than heuristic — a name isn't detectable by
    capitalization alone

## Segment 4 — Review queue / QC in action (60 sec)
- Run a translation that triggers placeholder corruption (Hindi with SASTRA)
- Show the WARNING printed to console
- Open data/review_queue.json, show the flagged entry
- Explain: this is the safety net — corruption gets caught, not silently shipped

## Segment 5 — Tests (60 sec)
- Run: `pytest tests/ -v`
- Show tests passing
- Briefly explain what test_ordinary_capitalized_words_are_not_wrongly_protected
  tests and why it exists (regression test for F002)

## Segment 6 — One code-level decision, explained (90 sec)
Pick the strongest one: the placeholder-corruption design decision.
- Show entity_protect.py's make_placeholder function
- Explain: we tried multiple placeholder formats (F001, F003, F004), all got
  corrupted by the model's subword tokenization
- Explain the actual decision: instead of chasing a perfect format, we detect
  corruption and route to a review queue — this is more realistic engineering
  than pretending a small model can guarantee exact string preservation

## Segment 7 — Wrap-up (30 sec)
- Summarize: 10 languages, entity protection, QC detection, review queue, tests
- Mention SOURCES.md/AI_USE.md are included for full disclosure

## Notes for recording
- Keep it UNEDITED (required) — practice the flow once or twice before recording
  so it's smooth, but no cuts/edits in the final file
- Have all terminal commands ready to paste (don't type live, reduces dead air)
- Record in one take if possible; if not, note that it must still be "unedited"
  per the requirement — so plan for one clean take rather than multiple clips