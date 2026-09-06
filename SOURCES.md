# Sources, Models, and Licences

## Translation models (Helsinki-NLP / OPUS-MT, via Hugging Face)
| Language | Model | Licence | Commercial use |
|---|---|---|---|
| Hindi | Helsinki-NLP/opus-mt-en-hi | Apache-2.0 | Yes |
| Tamil, Telugu | Helsinki-NLP/opus-mt-en-dra | Apache-2.0 | Yes |
| Bengali | Helsinki-NLP/opus-mt-en-inc | Apache-2.0 | Yes |
| Marathi | Helsinki-NLP/opus-mt-en-mr | Apache-2.0 | Yes |
| Spanish | Helsinki-NLP/opus-mt-en-es | Apache-2.0 | Yes |
| French | Helsinki-NLP/opus-mt-en-fr | Apache-2.0 | Yes |
| German | Helsinki-NLP/opus-mt-en-de | Apache-2.0 | Yes |
| Indonesian | Helsinki-NLP/opus-mt-en-id | Apache-2.0 | Yes |
| Portuguese | Helsinki-NLP/opus-mt-tc-big-en-pt | CC-BY-4.0 | [verify: check licence terms before final submission] |

All models: Language Technology Research Group, University of Helsinki (Helsinki-NLP), hosted on Hugging Face Hub. Retrieved via the `transformers` library's `from_pretrained()`, no manual download or modification of weights.

## Libraries
| Library | Version | Licence |
|---|---|---|
| transformers | 5.16.1 | Apache-2.0 |
| torch | 2.14.0+cpu | Apache-2.0 / BSD-3-Clause (mixed; see PyTorch's own licence file) |
| sentencepiece | 0.2.2 | Apache-2.0 |
| sacremoses | 0.2.0 | MIT |

## Data
- No external training or evaluation datasets used. All test inputs are original example sentences written for this assessment.

## Compute
- All development and execution performed locally on candidate's own CPU laptop (non-GPU).
- No hosted/free compute (Colab, Kaggle, etc.) used for the submitted default workflow.

## Attribution and notes
- No payment, subscription, or paid API used at any point.
- No candidate account tokens, credentials, or secrets are included in this repository.
- Portuguese model licence marked for final verification before submission — flagged, not yet confirmed as of this draft.