# Failure Log — Track 04

## F001 — Proper noun corrupted during translation
**Date:** 2026-09-06
**Model:** Helsinki-NLP/opus-mt-en-hi
**Direction:** en -> hi
**Input:** "Hello, my name is Mamthasha and I study at SASTRA University."
**Output:** "हैलो, मेरा नाम मामाशा है और मैं SeeeTA यूनिवर्सिटी में अध्ययन करते हैं।"
**Problem:** The proper noun "SASTRA" was mistranslated/corrupted into "SeeeTA" instead of being preserved as-is.
**Root cause:** No entity/placeholder protection was applied before translation — the model treated "SASTRA" as translatable text rather than a name to preserve.
**Status:** Motivates the entity-protection module (src/entity_protect.py) — planned fix.

## F002 — Overly broad proper-noun heuristic
**Date:** 2026-09-06
**Problem:** Initial regex `[A-Z][A-Za-z]{2,}` matched ordinary capitalized words ("Hello", "Visit", "University") as if they were proper nouns, wrongly locking them from translation.
**Root cause:** Capitalization alone can't distinguish a name from a sentence-starting word.
**Fix:** Replaced heuristic with a controlled glossary (configs/glossary.json) — the assignment's own "do-not-translate terms" concept, applied here for entity protection.
**Status:** Resolved.

## F003 — Placeholder corrupted during model translation
**Date:** 2026-09-06
**Problem:** __ENT_0__ style placeholders were fragmented into subword pieces by the
MarianMT tokenizer and not reliably reconstructed by the decoder, producing garbage
like "(_n)____BAR_" instead of the placeholder.
**Root cause:** Seq2seq translation models have no hard copy mechanism for
out-of-vocabulary strings; underscores and digits get split into multiple subword
tokens that the decoder regenerates imperfectly.
**Fix:** (1) switch placeholder format to reduce fragmentation, (2) add a post-
translation validation step that detects missing/corrupted placeholders and routes
the segment to a review queue instead of silently failing.
**Status:** In progress — this also satisfies the assignment's required
"entity/number preservation" QC check and human-review queue.

## F004 — Placeholder corruption persists across formats
**Date:** 2026-09-06
**Problem:** Even after switching to a word-based placeholder format, MarianMT
corrupted 2/2 placeholders in both Hindi and Tamil outputs.
**Root cause:** Small MarianMT models have no guaranteed copy mechanism for
out-of-vocabulary tokens; this is a model-class limitation, not a formatting bug.
**Decision:** Stop trying to achieve 100% placeholder survival. Instead, treat
corruption as an expected failure mode: detect it (already working) and route
affected segments to review_queue.json rather than silently returning bad output.
This directly satisfies the assignment's "safe failure handling" and QC
review-queue requirements.
**Status:** Resolved by design change.

## F005 — Assumed model naming pattern didn't hold for Bengali
**Date:** 2026-09-06
**Problem:** Assumed a direct Helsinki-NLP/opus-mt-en-bn model existed by pattern-
matching other languages (en-hi, en-mr). It doesn't — only the reverse direction
(bn-en) was published standalone.
**Root cause:** Not every language pair has a dedicated model; Bengali is only
covered via the broader en-inc (Indic languages) group model with a language tag.
**Fix:** Route Bengali through Helsinki-NLP/opus-mt-en-inc with >>ben<< tag,
same pattern already used for Tamil/Telugu via the Dravidian group model.
**Status:** Resolved.

## F006 — Poor translation quality for Marathi (not just placeholder corruption)
**Date:** 2026-09-06
**Problem:** Marathi output "माझं नाव इ. स. पू." bears no resemblance to the
source sentence — the model produced "BC" (a date-era term) instead of a
meaningful translation, unrelated to placeholder corruption.
**Root cause:** Small distilled OPUS-MT models vary significantly in quality
across languages depending on how much training data existed for that pair;
Marathi appears notably weaker than Hindi/Spanish/German in this test.
**Status:** Documented as a known limitation. Not fixed — flagged for the
report's "trade-offs" section as evidence that lightweight CPU models have
uneven quality, which the review-queue/QC layer is partly designed to catch.
**Note:** This also affects whether Marathi output should be trusted even when
review_status shows "ok" — worth mentioning as a QC gap for future work.

## F007 — Corruption rate scales with placeholder count per sentence
**Date:** 2026-09-06
**Observation:** Across the 5-input test batch (Hindi), the only input with
zero protected entities (T001) translated cleanly. All 4 inputs with 2+
placeholders in the same sentence (T002-T005) were flagged for corruption.
**Insight:** The small OPUS-MT model's ability to correctly pass through an
unknown token appears to degrade as more such tokens appear in one sentence,
likely because attention/copy behavior for rare tokens gets less reliable
with more competing rare tokens present.
**Implication:** This is strong evidence that review-queue-based QC is not
optional polish but a necessary safety net for this model class — supports
the "Exceptional" tier's explicit requirement that "the production translation
model may not grade itself."
**Status:** Documented for report; no further fix attempted given time
constraints (Baseline scope).

## Addition — Batch resume support
**Date:** 2026-09-06
**Context:** Required test matrix item #4 ("interrupted batch/resume test") was
not yet implemented after Baseline functionality was working.
**Implementation:** cli.py now writes output incrementally after each item
(not just at the end) and checks for already-completed IDs in an existing
output file before starting, skipping them on re-run.
**Test plan:** Start a batch, interrupt with Ctrl+C after 2-3 items complete,
re-run the same command, confirm completed items are skipped and only
remaining items are processed.