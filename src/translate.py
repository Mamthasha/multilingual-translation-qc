import json
import os
import time
from langdetect import detect, LangDetectException

try:
    from src.entity_protect import protect_entities, restore_entities, load_glossary
except ImportError:
    from entity_protect import protect_entities, restore_entities, load_glossary

from transformers import MarianMTModel, MarianTokenizer

DIRECT_MODELS = {
    "hi": "Helsinki-NLP/opus-mt-en-hi",
    "mr": "Helsinki-NLP/opus-mt-en-mr",
    "es": "Helsinki-NLP/opus-mt-en-es",
    "fr": "Helsinki-NLP/opus-mt-en-fr",
    "de": "Helsinki-NLP/opus-mt-en-de",
    "id": "Helsinki-NLP/opus-mt-en-id",
    "pt": "Helsinki-NLP/opus-mt-tc-big-en-pt",
}

DRAVIDIAN_MODEL = "Helsinki-NLP/opus-mt-en-dra"
DRAVIDIAN_TAGS = {
    "ta": ">>tam<<",
    "te": ">>tel<<",
}

INDIC_MODEL = "Helsinki-NLP/opus-mt-en-inc"
INDIC_TAGS = {
    "bn": ">>ben<<",
}

REVIEW_QUEUE_PATH = "data/review_queue.json"

_model_cache = {}


def _load_model(model_name):
    if model_name not in _model_cache:
        tokenizer = MarianTokenizer.from_pretrained(model_name)
        model = MarianMTModel.from_pretrained(model_name, use_safetensors=True)
        _model_cache[model_name] = (tokenizer, model)
    return _model_cache[model_name]


def _add_to_review_queue(entry):
    os.makedirs("data", exist_ok=True)
    queue = []
    if os.path.exists(REVIEW_QUEUE_PATH):
        with open(REVIEW_QUEUE_PATH, "r", encoding="utf-8") as f:
            queue = json.load(f)

    queue.append(entry)

    with open(REVIEW_QUEUE_PATH, "w", encoding="utf-8") as f:
        json.dump(queue, f, ensure_ascii=False, indent=2)


def translate(text, target_lang, glossary=None):
    """
    Translates English text into the target language.
    target_lang: one of "hi","bn","mr","es","fr","de","id","pt","ta","te"

    Returns a dict matching the required output contract:
    {
        "translated_text": str,
        "route": str,
        "review_status": "ok" | "flagged",
        "runtime_sec": float,
        "warnings": list[str],
    }
    """
    start_time = time.time()
    warnings_list = []

    # Validate target language before doing any model work.
    supported_languages = (
        set(DIRECT_MODELS.keys())
        | set(DRAVIDIAN_TAGS.keys())
        | set(INDIC_TAGS.keys())
    )

    if target_lang not in supported_languages:
        raise ValueError(f"Unsupported target language: {target_lang}")

    # Safely handle empty input without loading a translation model.
    if not text or not text.strip():
        return {
            "translated_text": "",
            "route": "none",
            "review_status": "ok",
            "runtime_sec": round(time.time() - start_time, 3),
            "warnings": ["Empty input"],
        }

    protected_text, entity_map = protect_entities(text, glossary=glossary)

    if target_lang in DRAVIDIAN_TAGS:
        tokenizer, model = _load_model(DRAVIDIAN_MODEL)
        input_text = f"{DRAVIDIAN_TAGS[target_lang]} {protected_text}"
        route = DRAVIDIAN_MODEL

    elif target_lang in INDIC_TAGS:
        tokenizer, model = _load_model(INDIC_MODEL)
        input_text = f"{INDIC_TAGS[target_lang]} {protected_text}"
        route = INDIC_MODEL

    elif target_lang in DIRECT_MODELS:
        tokenizer, model = _load_model(DIRECT_MODELS[target_lang])
        input_text = protected_text
        route = DIRECT_MODELS[target_lang]

    inputs = tokenizer(input_text, return_tensors="pt", padding=True)
    translated_tokens = model.generate(**inputs, max_length=200)
    raw_output = tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

    # QC Check #1: Entity/number/URL preservation
    missing = [p for p in entity_map if p not in raw_output]
    entity_check_failed = len(missing) > 0

    # QC Check #2: Language-ID verification — independent of the translation
    # model, since langdetect uses its own statistical classifier.
    lang_check_failed = False
    detected_lang = None

    try:
        detected_lang = detect(raw_output)

        expected_lang_map = {
            "hi": "hi",
            "ta": "ta",
            "te": "te",
            "bn": "bn",
            "mr": "mr",
            "es": "es",
            "fr": "fr",
            "de": "de",
            "pt": "pt",
            "id": "id",
        }

        expected = expected_lang_map.get(target_lang)

        if expected and detected_lang != expected:
            lang_check_failed = True

    except LangDetectException:
        detected_lang = "undetermined"

    review_status = "ok"

    if entity_check_failed or lang_check_failed:
        review_status = "flagged"

        if entity_check_failed:
            warning_msg = (
                f"{len(missing)} placeholder(s) corrupted during translation"
            )
            warnings_list.append(warning_msg)
            print(f"WARNING: {warning_msg} — flagged for review")

        if lang_check_failed:
            warning_msg = (
                f"Language-ID check failed: expected '{target_lang}', "
                f"detected '{detected_lang}'"
            )
            warnings_list.append(warning_msg)
            print(f"WARNING: {warning_msg} — flagged for review")

        _add_to_review_queue({
            "source_text": text,
            "target_lang": target_lang,
            "raw_output": raw_output,
            "missing_placeholders": missing,
            "detected_language": detected_lang,
            "entity_check_failed": entity_check_failed,
            "language_id_check_failed": lang_check_failed,
            "reason": (
                "entity_preservation_failure"
                if entity_check_failed
                else "language_id_mismatch"
            ),
        })

    final_output = restore_entities(raw_output, entity_map)
    runtime_sec = round(time.time() - start_time, 3)

    return {
        "translated_text": final_output,
        "route": route,
        "review_status": review_status,
        "runtime_sec": runtime_sec,
        "warnings": warnings_list,
    }


if __name__ == "__main__":
    glossary = load_glossary()
    text = "Hello, my name is Mamthasha and I study at SASTRA University."

    all_targets = [
        "hi",
        "ta",
        "te",
        "bn",
        "mr",
        "es",
        "fr",
        "de",
        "pt",
        "id",
    ]

    for lang in all_targets:
        result = translate(text, lang, glossary=glossary)
        print(
            f"[{lang}] {result['translated_text']}  "
            f"(status: {result['review_status']})"
        )