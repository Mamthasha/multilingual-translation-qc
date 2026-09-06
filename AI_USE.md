# AI Use Disclosure

## Tools used
- Claude (Anthropic) — used as a coding assistant throughout development

## Where AI was used
- Environment setup guidance (Python version selection, venv, dependency installation)
- Debugging disk-space and memory errors during model downloads
- Initial structure/logic for entity-protection module (src/entity_protect.py)
- Initial structure/logic for translation module (src/translate.py)
- Identifying correct Helsinki-NLP model names for each target language
- [Add more as we build: CLI, tests, benchmark script, etc.]

## What I did myself
- Ran all code, verified outputs, debugged real errors as they occurred
- Made the decision to switch from a regex-based proper-noun heuristic to a
  glossary-based approach after observing over-matching (see notes/failures.md, F002)
- Made the decision to treat placeholder corruption as an expected failure mode
  requiring detection + review-queue routing, rather than chasing a "perfect"
  placeholder format (see notes/failures.md, F004)
- [Add more as the project progresses]

## How I reviewed AI-generated code
- Ran every script personally and observed actual output/errors, not just accepted code as correct
- Traced and logged real failures (see notes/failures.md) rather than hiding them
- Can explain and modify every function in src/entity_protect.py and src/translate.py

## Declaration
I remain responsible for the correctness of this submission and can explain,
trace, and modify the core implementation live.

## Model selection research
- Used AI assistance to identify correct Helsinki-NLP model names/routing for
  each target language, including discovering that some languages (Bengali)
  required a broader group model with a language tag rather than a dedicated
  one-to-one model — verified against actual Hugging Face model pages before
  use, not taken on faith.