# Evidence: Interrupted Batch / Resume Test
(Required Test Matrix item #4)

## Test setup
- Input file: data/test_inputs_resume_demo.json (10 items)
- Command: `python cli.py --input data/test_inputs_resume_demo.json --target hi --output data/output_resume_demo.json`

## Run 1 — Interrupted mid-batch (manual Ctrl+C after 2 items completed)

Warning: You are sending unauthenticated requests to the HF Hub.
Loading weights: 100%|█| 256/256 [00:00<00:00, 1997.41it/s]
WARNING: 2 placeholder(s) corrupted during translation — flagged for review
WARNING: 4 placeholder(s) corrupted during translation — flagged for review
[KeyboardInterrupt raised manually here, mid-processing of item 3 (R003),
inside model.generate() during beam search decoding]


## State after interruption
`data/output_resume_demo.json` contained exactly 2 completed items at this point:
```json
[
  {
    "id": "R001",
    "source_text": "Hello, my name is Mamthasha and I study at SASTRA University.",
    "target_lang": "hi",
    "route": "Helsinki-NLP/opus-mt-en-hi",
    "review_status": "flagged",
    "runtime_sec": 23.226,
    "warnings": ["2 placeholder(s) corrupted during translation"]
  },
  {
    "id": "R002",
    "source_text": "The event starts on 15 September 2026 at 6:30 PM.",
    "target_lang": "hi",
    "route": "Helsinki-NLP/opus-mt-en-hi",
    "review_status": "flagged",
    "runtime_sec": 18.497,
    "warnings": ["4 placeholder(s) corrupted during translation"]
  }
]
```
Confirmed via `type data\output_resume_demo.json` immediately after the interrupt.

## Run 2 — Resumed (same exact command, re-run)

Resuming: 2 item(s) already completed, skipping them.
Warning: You are sending unauthenticated requests to the HF Hub.
Loading weights: 100%|█| 256/256 [00:00<00:00, 1552.09it/s]
WARNING: 2 placeholder(s) corrupted during translation — flagged for review
WARNING: 2 placeholder(s) corrupted during translation — flagged for review
WARNING: 2 placeholder(s) corrupted during translation — flagged for review
WARNING: 4 placeholder(s) corrupted during translation — flagged for review
WARNING: 2 placeholder(s) corrupted during translation — flagged for review
WARNING: 2 placeholder(s) corrupted during translation — flagged for review
Wrote 10 results to data/output_resume_demo.json


Note: exactly 6 WARNING lines printed on resume, but 8 items were processed
(R003-R010) — 2 of those 8 (R005, R010, both "Subscribe for more travel
vlogs...") translated cleanly with `review_status: "ok"` and no warning,
which is consistent with the final file below.

## Final state — all 10 items present, correctly ordered, no duplicates
Final `data/output_resume_demo.json` contains all 10 items (R001–R010):
- R001, R002: from Run 1 (preserved, not redone)
- R003–R010: from Run 2 (newly processed)
- Runtimes for R001-R002 remain unchanged from Run 1 (23.226s, 18.497s),
  confirming these entries were not recomputed
- R005 and R010 (identical source text, "Subscribe for more travel vlogs
  every Friday!") both correctly returned `review_status: "ok"` with no
  entity placeholders, since this sentence contains no protected entities

## Conclusion
The system correctly detects already-completed items by `id` and skips them
on re-run, printing an explicit `"Resuming: N item(s) already completed"`
message. No completed work was redone (confirmed by unchanged runtime values
for R001/R002 across both runs), and the final output file correctly
contains all 10 items with no duplicates or gaps. This satisfies the
required "interrupted batch/resume test" from the assessment's test matrix.

## Note on testing methodology
An earlier attempt using PowerShell's `Start-Job`/`Stop-Job` to simulate
interruption inadvertently corrupted the cached model weights for
`opus-mt-en-hi` (see notes/failures.md, F008) — the model briefly reported
`MISSING` weights and reinitialized randomly. Manual Ctrl+C in a foreground
terminal was used instead, which reliably terminates the process without
corrupting on-disk cache state, and was used for this final, valid test.