# Final Submission Form — Answers

## Code repository URL
https://github.com/Mamthasha/multilingual-translation-qc

## Repository access
The repository is publicly accessible. (check this box — no need to
separately grant admin@incubrix.com access since it's public)

## Technical-demonstration video URL
[Add after recording tomorrow — upload to YouTube as "Unlisted" or Google
Drive with link-sharing enabled, then paste link here]

## Highest requirement level completed
**Basic requirement completed** (this maps to "Baseline" in the assessment's
own terminology — this is the honest, accurate choice given we deliberately
scoped to Baseline for reliability within the timeline)

## Track-specific outcome summary (PS04)

Draft:
"Implemented a CPU-only translation pipeline supporting English-to-target
translation across all 10 required languages (Hindi, Tamil, Telugu, Bengali,
Marathi, Spanish, French, German, Portuguese, Indonesian) using open-source
Helsinki-NLP OPUS-MT models, routed appropriately across direct bilingual
models and shared language-family group models (Dravidian for Tamil/Telugu,
Indic for Bengali) where dedicated models were unavailable. Built a
deterministic entity/number/URL preservation system using placeholder
substitution with a configurable glossary, combined with automated
corruption detection that flags failed preservations into a structured
review_queue.json for human review — since the production translation
model cannot reliably validate its own entity-preservation output. All 10
languages were benchmarked for runtime and peak memory on the development
hardware (Intel Celeron N4120, 4GB RAM); results and full evidence are
documented in REPORT.md and data/benchmark_results.json. The system
includes a CLI with a documented JSON input/output contract, batch
processing with resume-on-interrupt support (verified with real
interrupted-batch evidence), and 17 automated tests covering unit,
end-to-end, and regression scenarios."

## Known limitations or unsuccessful approaches

Draft (pulled honestly from notes/failures.md):
"1) Entity-preservation placeholders are corrupted by the underlying
MarianMT models in a meaningful proportion of cases, especially in
sentences containing 2+ protected entities — this is a limitation of the
small model class's subword tokenization, not fixable through placeholder
formatting alone (documented as failures F001, F003, F004, F007). This was
addressed by building corruption detection and a review-queue mechanism
rather than attempting to force 100% placeholder survival, which is not
realistic with this model class.
2) Marathi translation quality was noticeably poor in testing — one test
input produced an unrelated, nonsensical output despite no entity
corruption being detected, indicating a language-quality limitation
independent of the entity-preservation system (F006).
3) No direct English-to-Bengali model exists from Helsinki-NLP; Bengali is
routed through a broader Indic-languages group model, which was only
discovered after an initial incorrect assumption about model naming
patterns (F005).
4) Given hardware constraints (4GB RAM, no GPU), Strong-tier features
(20 non-English direction pairs, multi-model comparison/routing) and
Exceptional-tier QC (3 independent checks) were not attempted; this
submission deliberately targets a complete, well-tested Baseline rather
than a partial, less-verified Strong/Exceptional attempt."

## Submission declaration checkboxes
All should be checked truthfully:
- [x] Own individual work — Yes, disclosed AI assistance in AI_USE.md
- [x] Problem statement matches assigned (Track 04 / PS04) — Yes
- [x] Correct workbook for assigned problem statement — Yes
- [x] Repository contains code, reproducible via provided instructions —
      Yes, README.md has exact setup/run commands
- [x] All files/links complete and accessible — Yes (verify GitHub repo is
      public before final submission)
- [x] Used open-source software/models as much as reasonably possible —
      Yes, 100% open-source, no exceptions
- [x] Did not use paid commercial model/API/service — Yes, confirmed true
      throughout AI_USE.md and SOURCES.md
- [x] Disclosed all material AI assistance, models, datasets, tools, free
      credits, hosted compute, paid services, manual work — Yes, AI_USE.md
      and SOURCES.md cover this
- [x] All inputs/media public, synthetic, consented, or licensed — Yes, all
      test inputs are original example sentences
- [x] Identifiable person consent — N/A, no voice/image/likeness used
- [x] Evidence includes failed/rejected/degraded cases, not just successes
      — Yes, notes/failures.md documents 9 real issues honestly, including
      F006 (poor Marathi quality) and F007 (corruption patterns) which are
      genuine limitations, not cherry-picked wins
- [x] Reported runtimes/metrics come from actual executions — Yes, all
      benchmark numbers are from real `python benchmark.py` runs, not
      estimated
- [x] No fabrication of code/outputs/evidence/metrics — Yes, true
- [x] Understand IncuBrix may audit/rerun/live-test — Acknowledge
- [x] Understand results are provisional — Acknowledge
- [x] Understand submission doesn't guarantee interview/selection/offer —
      Acknowledge