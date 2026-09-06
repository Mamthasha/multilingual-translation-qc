# Component, Model and Licence Manifest

| Component / asset | Version | Role | Source URL | Code licence | Weights/data licence | Commercial use | Execution | Size (MB) | Verified date |
|---|---|---|---|---|---|---|---|---|---|
| transformers | 5.16.1 | Model loading/inference framework | https://github.com/huggingface/transformers | Apache-2.0 | N/A | Yes | Local CPU | ~500 | 2026-09-06 |
| torch | 2.14.0+cpu | Tensor computation backend | https://pytorch.org | Apache-2.0/BSD-3 | N/A | Yes | Local CPU | ~200 | 2026-09-06 |
| sentencepiece | 0.2.2 | Tokenization | https://github.com/google/sentencepiece | Apache-2.0 | N/A | Yes | Local CPU | ~1 | 2026-09-06 |
| sacremoses | 0.2.0 | Text normalization for MarianMT | https://github.com/hplt-project/sacremoses | MIT | N/A | Yes | Local CPU | ~1 | 2026-09-06 |
| opus-mt-en-hi | - | English→Hindi translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-hi | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | 2026-09-06 |
| opus-mt-en-dra | - | English→Tamil/Telugu translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-dra | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | 2026-09-06 |
| opus-mt-en-inc | - | English→Bengali translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-inc | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | 2026-09-06 |
| opus-mt-en-mr | - | English→Marathi translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-mr | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | [pending] |
| opus-mt-en-es | - | English→Spanish translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-es | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | [pending] |
| opus-mt-en-fr | - | English→French translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-fr | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | [pending] |
| opus-mt-en-de | - | English→German translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-de | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | [pending] |
| opus-mt-en-id | - | English→Indonesian translation | https://huggingface.co/Helsinki-NLP/opus-mt-en-id | Apache-2.0 | Apache-2.0 | Yes | Local CPU | ~300 | [pending] |
| opus-mt-tc-big-en-pt | - | English→Portuguese translation | https://huggingface.co/Helsinki-NLP/opus-mt-tc-big-en-pt | Apache-2.0 | CC-BY-4.0 [verify] | [verify] | Local CPU | ~900 | [pending] |

## Product recommendation (draft — expand later)
- Preferred commercially reusable stack: all Helsinki-NLP OPUS-MT models used are Apache-2.0, safe for commercial reuse, except Portuguese's CC-BY-4.0 model which needs attribution.
- Unresolved licence question: exact commercial-use terms of opus-mt-tc-big-en-pt need final confirmation before any product use.
- No privacy/consent concerns — no personal data used, only static example sentences.
- Before product use: would need proper error handling for API rate limits, retry logic, and likely a larger/better multilingual model for production translation quality (OPUS-MT models are lightweight, not state-of-the-art).