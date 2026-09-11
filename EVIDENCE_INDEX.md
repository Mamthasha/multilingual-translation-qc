# Evidence Index
Maps every claim in this submission to the file/location where it can be verified.

| Claim | Evidence location |
|---|---|
| All 10 baseline languages translate successfully | data/output_hi.json, data/output_ta.json, data/output_te.json, data/output_bn.json, data/output_mr.json, data/output_es.json, data/output_fr.json, data/output_de.json, data/output_pt.json, data/output_id.json |
| Entity/number/URL preservation is implemented | src/entity_protect.py |
| Entity preservation is tested (unit tests) | tests/test_entity_protect.py (9 tests) |
| System detects and flags entity-preservation failures | src/translate.py (missing-placeholder check), data/review_queue.json (populated flagged entries) |
| Review queue is a real, working mechanism | data/review_queue.json, tests/test_translate.py::test_review_queue_file_is_created_on_corruption |
| CLI works with documented input/output contract | cli.py, README.md ("Running a translation" section), data/output_*.json |
| Output matches required contract (route, review_status, runtime, warnings) | src/translate.py (translate() return value), any data/output_*.json file |
| Unsupported-language request is handled safely | tests/test_translate.py::test_unsupported_language_raises_error, ::test_unsupported_language_via_cli_input |
| Interrupted batch / resume is implemented and verified | cli.py (resume logic), notes/evidence_interrupted_batch_test.md (full before/after proof) |
| End-to-end test (real model load + translation) | tests/test_translate.py::test_hindi_translation_end_to_end |
| Full automated test suite passes | tests/ (17 tests total across 3 files), run via `pytest tests/ -v` |
| Benchmark: runtime, RAM, per-language performance | benchmark.py, data/benchmark_results.json |
| All models, libraries, and licences disclosed | SOURCES.md, data/licence_manifest.md |
| AI tool usage fully disclosed | AI_USE.md |
| No payment/paid API used at any point | AI_USE.md, SOURCES.md, README.md |
| Real failures encountered and resolved (with root causes) | notes/failures.md (8 documented issues, F001-F008) |
| Reproducible setup with exact commands | README.md ("Setup" and "Running" sections) |
| Git repository with real commit history | https://github.com/Mamthasha/multilingual-translation-qc |
| 5+ varied test inputs per language (captions, names, dates, units, URLs) | data/test_inputs.json |
| Demo video plan covering all required elements | notes/demo_script.md |