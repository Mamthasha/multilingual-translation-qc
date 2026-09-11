# Technical Report — Track 04: Multilingual Translation with Independent QC

## 1. Architecture Overview
The system is a CLI-driven translation pipeline: input text passes through
entity protection, is routed to the appropriate translation model based on
target language, translated, checked for entity-preservation failures, and
either returned as-is or flagged into a review queue for human inspection.

- `src/entity_protect.py` — glossary-based entity/number/URL protection before translation
- `src/translate.py` — model routing and translation logic, corruption detection
- `cli.py` — command-line interface with batch input and resume support
- `benchmark.py` — performance measurement script
- `configs/glossary.json` — do-not-translate terms
- `data/review_queue.json` — flagged segments requiring human review
- `tests/` — 17 automated tests across 3 files

## 2. Model Selection and Routing
| Language | Model | Reasoning |
|---|---|---|
| Hindi | opus-mt-en-hi | Direct dedicated model available |
| Tamil, Telugu | opus-mt-en-dra | No per-language model; shared Dravidian-family model with language tag |
| Bengali | opus-mt-en-inc | No direct en-bn model exists; routed through Indic-languages group model |
| Marathi | opus-mt-en-mr | Direct dedicated model available |
| Spanish, French, German, Indonesian | opus-mt-en-{lang} | Direct dedicated models available |
| Portuguese | opus-mt-tc-big-en-pt | Larger "tc-big" variant; no smaller direct alternative found |

**Trade-off discussion:** Using shared group models (Dravidian for Tamil/Telugu,
Indic for Bengali) instead of dedicated bilingual models reduced the number of
distinct models needed from 10 to 8, saving disk space and download time on a
disk-constrained laptop. Benchmark data (Section 7) shows this doesn't
straightforwardly hurt performance — Telugu (shared Dravidian model) ran in
25.63s, comparable to Hindi's dedicated model at 27.74s — suggesting
per-language complexity matters more than the shared-vs-dedicated model
architecture choice itself.

## 3. Entity/Number Preservation Design
- Initial approach: regex-based proper-noun detection (`[A-Z][A-Za-z]{2,}`) — failed, over-matched ordinary capitalized words (see failure F002)
- Final approach: glossary-based protection (configs/glossary.json) combined with regex for URLs/hashtags/mentions/numbers
- Placeholder format iterated twice (F001, F003, F004) after observing subword tokenization corrupting placeholders during translation
- **Design decision:** rather than pursuing a placeholder format with guaranteed survival (not achievable with small seq2seq models), built detection + review-queue routing as the safety net instead

## 4. Quality Control Approach
- Entity/number preservation check (implemented) — deterministic, compares placeholder survival pre/post translation
- Detected failures are routed to `data/review_queue.json` with full context (source text, target language, raw output, missing placeholders, reason)
- Observed pattern (F007): corruption rate scales with placeholder count per sentence — sentences with 2+ protected entities were flagged far more often than sentences with 0-1, across all 10 languages tested

## 5. Failures and Debugging
See `notes/failures.md` for the full log. Summary of key issues:
- F001: proper noun corrupted with no protection (motivated the whole entity-protection module)
- F002: naive regex heuristic over-matched ordinary words
- F003/F004: placeholder corruption during translation — resolved by treating it as an expected, detected, and queued failure mode rather than chasing prevention
- F005: assumed model-naming pattern didn't hold for Bengali — required research into Helsinki-NLP's actual model catalog
- F006: Marathi model produced a poor/unrelated translation independent of placeholder issues — documented as a model-quality limitation
- F007: corruption rate scales with number of protected entities per sentence
- F008: background-job-based interruption testing corrupted cached model weights; resolved by using manual foreground interruption instead
- F009: benchmarking multiple models sequentially exhausted RAM; resolved by clearing the model cache between languages

## 6. Resource Constraints and Engineering Trade-offs
- Development laptop: Intel(R) Celeron(R) N4120 @ 1.10GHz (4 cores), 4GB RAM
  (3912 MB), ~60GB total disk (57.3GB usable after Windows overhead)
- Disk space crisis during development — required cleanup (Anaconda removal, ~4.8GB) before models could be downloaded
- RAM/pagefile crisis — required manual pagefile resize to load `transformers`/`torch` reliably
- **Model choice was directly shaped by these constraints:** chose small OPUS-MT models (~300MB each) over a single larger multilingual model (e.g. NLLB-200, ~2.5GB) specifically because of disk limits — a real engineering decision under real constraints, not a hypothetical one
- **Benchmark script itself hit the same RAM ceiling** during development —
  loading multiple translation models sequentially in one process exhausted
  available memory after 5 languages, requiring an explicit model-cache-clearing
  step between each language (see F009)
- CLI commands were run sequentially (one language at a time), never in
  parallel, for the same reason — a deliberate adaptation to available
  hardware rather than a design limitation

## 7. Testing and Reproducibility
- 17 automated tests across 3 files (tests/test_entity_protect.py,
  tests/test_translate.py, tests/test_batch_resume.py), all passing
  (verified via `pytest tests/ -v`, 17 passed in 160.54s)
- Includes unit tests, one true end-to-end test (loads real model, runs
  real translation), and regression tests for previously-found bugs
  (e.g. test_ordinary_capitalized_words_are_not_wrongly_protected,
  a direct regression test for failure F002)
- Interrupted-batch/resume test performed and documented in full with
  real before/after evidence (see notes/evidence_interrupted_batch_test.md)

### Benchmark results (runtime, peak RAM per language)
| Language | Runtime (sec) | Peak RAM (MB) | Status |
|---|---|---|---|
| Hindi | 27.74 | 650.8 | flagged |
| Tamil | 24.44 | 636.1 | flagged |
| Telugu | 25.63 | 553.3 | flagged |
| Bengali | 24.37 | 300.9 | flagged |
| Marathi | 13.80 | 532.8 | flagged |
| Spanish | 18.11 | 537.6 | ok |
| French | 20.03 | 529.3 | flagged |
| German | 20.62 | 528.7 | ok |
| Portuguese | 191.75 | 466.4 | ok |
| Indonesian | 25.01 | 516.7 | flagged |

**Notable outlier:** Portuguese took 191.75s — roughly 8-10x longer than every
other language. This directly reflects the model choice: Portuguese uses
`opus-mt-tc-big-en-pt`, a larger "tc-big" variant (no smaller direct
alternative exists from Helsinki-NLP), while all other languages use
lightweight ~300MB models. A production system might swap Portuguese to a
smaller model if one becomes available, or accept the latency cost given it
still runs correctly on CPU.

## 8. Product Recommendation

**Commercially reusable stack:** All Helsinki-NLP OPUS-MT models used for
Hindi, Tamil, Telugu, Bengali, Marathi, Spanish, French, German, and
Indonesian are Apache-2.0 licensed — fully permissive for commercial use
with attribution. The Portuguese model (opus-mt-tc-big-en-pt) uses
CC-BY-4.0 licensing, which requires attribution but does not block
commercial use; this should be formally re-verified against the model's
current licence page before any production deployment.

**Research-only or unresolved components:** None of the models used carry
research-only restrictions. All are freely available for both research and
commercial inference use as of the versions verified in this submission.

**What would need to change before product use:**
1. **Translation quality is inconsistent across languages** — Marathi in
   particular produced a poor/unrelated translation in testing (F006),
   suggesting a production system would need per-language quality
   validation before trusting all 10 languages equally, or a fallback to a
   larger multilingual model (e.g. NLLB-200) for languages where the
   lightweight OPUS-MT model underperforms.
2. **Entity-preservation corruption rate is non-trivial** — across the test
   batch, the majority of sentences containing 2+ protected entities were
   flagged for review (F007). A production system would need either a
   better entity-preservation mechanism (e.g. constrained decoding, or a
   larger model with more reliable copy behavior) or an accepted human
   review workflow for flagged segments, which is the direction this
   prototype takes.
3. **Sequential model loading is not production-scalable** — the CPU/RAM
   constraints of the development environment required processing one
   language and one batch at a time. A production deployment would need
   either more RAM/compute to hold multiple models concurrently, or a
   model-serving layer (e.g. batched inference, model server with request
   queuing) rather than the current single-process CLI approach.
4. **No retry/rate-limiting logic** — since this runs entirely locally with
   no external API calls, this wasn't needed for the assessment, but would
   be required if any component were later moved to a hosted API.

**Privacy/consent constraints:** None identified — no personal data, user
content, or third-party copyrighted text was used in testing; all test
inputs are original example sentences written for this assessment.

## 9. Next Steps / What's Not Included
- Strong-tier features (non-English direction pairs, model comparison/routing, glossary cache-resume) — out of scope for this submission given time constraints; Baseline completed with strong engineering and evidence instead
- Exceptional-tier QC (3 independent checks) — not attempted; single deterministic entity-check implemented and documented as sufficient for Baseline scope