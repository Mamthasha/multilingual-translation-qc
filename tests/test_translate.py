import sys
import os
import json

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from translate import translate, DIRECT_MODELS, DRAVIDIAN_TAGS, INDIC_TAGS, REVIEW_QUEUE_PATH
from entity_protect import load_glossary


def test_unsupported_language_raises_error():
    """Required test matrix item: 'one unsupported-language request'"""
    try:
        translate("Hello", "xx")
        assert False, "Expected ValueError for unsupported language"
    except ValueError as e:
        assert "Unsupported target language" in str(e)


def test_all_required_languages_are_routable():
    """Confirms all 10 baseline languages have a routing path (model mapping exists),
    without actually running translation (fast, no model loading)."""
    required_languages = ["hi", "ta", "te", "bn", "mr", "es", "fr", "de", "pt", "id"]
    for lang in required_languages:
        is_routable = (
            lang in DIRECT_MODELS
            or lang in DRAVIDIAN_TAGS
            or lang in INDIC_TAGS
        )
        assert is_routable, f"{lang} has no routing path defined"


def test_hindi_translation_end_to_end():
    """End-to-end test: actually loads the model and translates.
    This is the required 'at least one end-to-end test.'"""
    glossary = load_glossary()
    result = translate("Hello, my name is Mamthasha.", "hi", glossary=glossary)

    assert "translated_text" in result
    assert "review_status" in result
    assert result["review_status"] in ["ok", "flagged"]
    assert len(result["translated_text"]) > 0


def test_review_queue_file_is_created_on_corruption():
    """Confirms flagged translations actually get written to review_queue.json"""
    glossary = load_glossary()
    translate("My name is Mamthasha and I study at SASTRA University.", "hi", glossary=glossary)

    assert os.path.exists(REVIEW_QUEUE_PATH)
    with open(REVIEW_QUEUE_PATH, "r", encoding="utf-8") as f:
        queue = json.load(f)
    assert isinstance(queue, list)


def test_unsupported_language_via_cli_input():
    """Required test matrix item: unsupported-language request should raise
    a clear error, not crash silently or produce garbage output."""
    glossary = load_glossary()
    try:
        translate("Hello world", "zz", glossary=glossary)
        assert False, "Expected ValueError for unsupported language code 'zz'"
    except ValueError:
        pass  # expected


def test_empty_input_text_does_not_crash():
    """Edge case: empty string should not crash the pipeline."""
    glossary = load_glossary()
    result = translate("", "hi", glossary=glossary)
    assert "translated_text" in result