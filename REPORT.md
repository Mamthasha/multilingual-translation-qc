# Technical Report — Track 04: Multilingual Translation with Independent QC

## 1. Architecture Overview
[Diagram/description to add: CLI → entity protection → model routing → translation → corruption check → review queue → restore → output]

- `src/entity_protect.py` — glossary-based entity/number/URL protection before translation
- `src/translate.py` — model routing and translation logic
- `configs/glossary.json` — do-not-translate terms
- `data/review_queue.json` — flagged segments requiring human review
- [Add: cli.py, tests/, benchmark script — once built]

## 2. Model Selection and Routing
| Language | Model | Reasoning |
|---|---|---|
| Hindi | opus-mt-en-hi | Direct dedicated model available |
| Tamil, Telugu | opus-mt-en-dra | No per-language model; shared Dravidian-family model with language tag |
| Bengali | opus-mt-en-inc | No direct en-bn model exists; routed through Indic-languages group model |
| Marathi | opus-mt-en-mr | Direct dedicated model available |
| Spanish, French, German, Indonesian | opus-mt-en-{lang} | Direct dedicated models available |
| Portuguese | opus-mt-tc-big-en-pt | Larger "tc-big" variant; no smaller direct alternative found |

**Trade-off discussion:** [Expand later] Using one general group model per language family (Dravidian, Indic) instead of dedicated bilingual models saves engineering effort but may trade off some translation quality — worth benchmarking once all languages are working.

## 3. Entity/Number Preservation Design
- Initial approach: regex-based proper-noun detection (`[A-Z][A-Za-z]{2,}`) — failed, over-matched ordinary capitalized words (see failure F002)
- Final approach: glossary-based protection (configs/glossary.json) combined with regex for URLs/hashtags/mentions/numbers
- Placeholder format iterated twice (F001, F003, F004) after observing subword tokenization corrupting placeholders during translation
- **Design decision:** rather than pursuing a placeholder format with guaranteed survival (not achievable with small seq2seq models), built detection + review-queue routing as the safety net instead

## 4. Quality Control Approach
[Expand once QC section is built]
- Entity/number preservation check (implemented) — deterministic, compares placeholder survival pre/post translation
- [Add: language-ID check, back-translation check if time permits]

## 5. Failures and Debugging
See `notes/failures.md` for the full log. Summary of key issues:
- F001: proper noun corrupted with no protection (motivated the whole entity-protection module)
- F002: naive regex heuristic over-matched ordinary words
- F003/F004: placeholder corruption during translation — resolved by treating it as an expected, detected, and queued failure mode rather than chasing prevention
- F005: assumed model-naming pattern didn't hold for Bengali — required research into Helsinki-NLP's actual model catalog

## 6. Resource Constraints and Engineering Trade-offs
- Development laptop: [fill in specs] CPU, 4GB RAM, ~60GB disk (heavily constrained)
- Disk space crisis during development — required cleanup (Anaconda removal, ~4.8GB) before models could be downloaded
- RAM/pagefile crisis — required manual pagefile resize to load `transformers`/`torch` reliably
- **Model choice was directly shaped by these constraints:** chose small OPUS-MT models (~300MB each) over a single larger multilingual model (e.g. NLLB-200, ~2.5GB) specifically because of disk limits — a real engineering decision under real constraints, not a hypothetical one

## 7. Testing and Reproducibility
[To add once tests/benchmark are built]

## 8. Product Recommendation
[To add: which models are commercially reusable, licence caveats, what would need to change for production use — e.g. Portuguese model licence verification pending]

## 9. Next Steps / What's Not Included
- Strong-tier features (non-English direction pairs, model comparison/routing, glossary cache-resume) — out of scope for this submission given time constraints; Baseline completed with strong engineering and evidence instead
- Exceptional-tier QC (3 independent checks) — not attempted; single deterministic entity-check implemented and documented as sufficient for Baseline scope