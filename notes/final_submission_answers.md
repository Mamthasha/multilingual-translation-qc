# Final Submission Form — Answers

## Code repository URL

https://github.com/Mamthasha/multilingual-translation-qc

## Repository access

The repository is publicly accessible.

## Technical-demonstration video URL

[Add after recording — upload the demonstration video as "Unlisted" on YouTube or use a shareable Google Drive link, then paste the link here.]

## Highest requirement level completed

**Basic requirement completed**

This maps to the **Baseline** level in the assessment terminology. The submission deliberately targets a complete and well-tested Baseline implementation rather than claiming partially verified Strong or Exceptional features.

## Track-specific outcome summary (PS04)

Implemented a CPU-only translation pipeline supporting English-to-target translation across all 10 required languages (Hindi, Tamil, Telugu, Bengali, Marathi, Spanish, French, German, Portuguese, Indonesian) using Helsinki-NLP OPUS-MT models, routed across direct bilingual models and shared language-family models where dedicated models were unavailable.

Built entity/number/URL protection using placeholder substitution and automated corruption detection that flags failed preservation into a structured `review_queue.json` for human review.

The system includes a CLI with a documented JSON input/output contract, batch processing with resume-on-interrupt support, and automated tests covering translation, validation, regression, and fault-injection scenarios.

Runtime and memory benchmark evidence, limitations, and implementation details are documented in `REPORT.md` and the associated evidence files.

## Known limitations or unsuccessful approaches

1. Entity-preservation placeholders are corrupted by the underlying MarianMT models in a meaningful proportion of cases, especially in sentences containing 2+ protected entities. This was addressed by building corruption detection and a review-queue mechanism rather than attempting to force 100% placeholder survival. The observed failures are documented in `notes/failures.md`.

2. Marathi translation quality was noticeably poor in testing. One test input produced an unrelated, nonsensical output despite no entity corruption being detected, indicating a language-quality limitation independent of the entity-preservation system.

3. No direct English-to-Bengali model exists from Helsinki-NLP for the required route. Bengali is therefore routed through a broader Indic-languages group model. This routing decision and the initial incorrect model-name assumption are documented in the project evidence.

4. Given hardware constraints (4GB RAM, no GPU), Strong-tier features (20 non-English direction pairs and multi-model comparison/routing) and Exceptional-tier QC (3 independent checks) were not attempted. This submission deliberately targets a complete, well-tested Baseline rather than a partial, less-verified Strong/Exceptional attempt.

## Submission declaration checkboxes

- [x] Own individual work — Yes, with AI assistance disclosed in `AI_USE.md`
- [x] Problem statement matches assigned — Track 04 / PS04
- [x] Correct workbook for assigned problem statement — Yes
- [x] Repository contains code and is reproducible using the provided instructions — Yes, `README.md` contains setup and run instructions
- [x] All files/links complete and accessible — Yes
- [x] Used open-source software/models as much as reasonably possible — Yes
- [x] Did not use paid commercial model/API/service — Yes
- [x] Disclosed material AI assistance, models, datasets, tools, free credits, hosted compute, paid services, and manual work where applicable — Yes, documented in `AI_USE.md` and `SOURCES.md`
- [x] All inputs/media are public, synthetic, consented, or appropriately licensed — Yes, test inputs are original example sentences
- [x] Identifiable person consent — N/A; no voice, image, or likeness was used
- [x] Evidence includes failed, rejected, or degraded cases, not only successful cases — Yes, documented in `notes/failures.md`
- [x] Reported runtimes/metrics come from actual executions — Yes
- [x] No fabrication of code, outputs, evidence, or metrics — Yes
- [x] Understand that IncuBrix may audit, rerun, or live-test the submission — Acknowledge
- [x] Understand that results are provisional — Acknowledge
- [x] Understand that submission does not guarantee an interview, selection, or offer — Acknowledge