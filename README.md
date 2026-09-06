# Track 04 — Multilingual Translation with Independent Quality Control

Candidate submission for IncuBrix SASTRA 2027 hiring assessment.

## What this does
Translates English text into 10 languages (Hindi, Tamil, Telugu, Bengali,
Marathi, Spanish, French, German, Portuguese, Indonesian) on CPU, while
protecting names/numbers/URLs from being mistranslated, and automatically
flagging translations where that protection fails for human review.

## Requirements
- Python 3.11 (tested on 3.11.9 — newer versions like 3.14 are not yet
  reliably supported by PyTorch as of this writing)
- Windows/Mac/Linux, CPU only, no GPU required
- ~2GB free disk space for models, ~4GB+ RAM recommended

## Setup (exact commands)
```powershell
# 1. Create and activate virtual environment
py -3.11 -m venv venv
venv\Scripts\Activate.ps1        # Windows PowerShell
# source venv/bin/activate       # Mac/Linux

# 2. Install dependencies
pip install --upgrade pip
pip install torch --index-url https://download.pytorch.org/whl/cpu
pip install transformers sentencepiece sacremoses psutil pytest
```

## Running a translation (CLI)
```powershell
python cli.py --input data/test_inputs.json --target hi --output data/output_hi.json
```
Supported `--target` codes: `hi, ta, te, bn, mr, es, fr, de, pt, id`

Output is a JSON file with `translated_text` and `review_status` (`ok` or
`flagged`) per input.

## Running tests
```powershell
pytest tests/ -v
```

## Running the benchmark
```powershell
python benchmark.py
```
Outputs runtime, peak RAM, and status per language to `data/benchmark_results.json`.

## Project structure

incubrix-track04/
├── src/
│ ├── entity_protect.py # glossary-based entity/number/URL protection
│ └── translate.py # model routing + translation + QC detection
├── tests/ # unit and end-to-end tests
├── configs/
│ └── glossary.json # do-not-translate terms
├── data/
│ ├── test_inputs.json # required test matrix inputs
│ └── review_queue.json # flagged translations (created at runtime)
├── notes/
│ ├── failures.md # documented failures and fixes
│ └── demo_script.md # demo video plan
├── cli.py # command-line interface
├── benchmark.py # performance/quality benchmark script
├── SOURCES.md # models, libraries, licences
├── AI_USE.md # AI tool usage disclosure
└── REPORT.md # technical report


## Known limitations (see notes/failures.md for full detail)
- Small OPUS-MT models occasionally corrupt entity placeholders during
  translation; this is detected and routed to `data/review_queue.json`
  rather than silently shipped as incorrect output.
- Bengali, Tamil, and Telugu use shared multi-language group models
  (no dedicated one-to-one model exists for these from Helsinki-NLP).

