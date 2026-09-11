import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from translate import translate
from entity_protect import load_glossary


def test_empty_input_produces_safe_output():
    """Injected fault: empty string input should not crash, should return
    a valid (if empty) result rather than garbage or an exception."""
    glossary = load_glossary()
    result = translate("", "hi", glossary=glossary)
    assert "translated_text" in result
    assert result["review_status"] in ["ok", "flagged"]


def test_repeated_text_input_is_handled():
    """Injected fault: heavily repeated text (simulating a corrupted/looping
    upstream source) should still translate without crashing."""
    glossary = load_glossary()
    repeated_text = "test " * 50  # unusual, repetitive input
    result = translate(repeated_text, "hi", glossary=glossary)
    assert "translated_text" in result
    assert len(result["translated_text"]) > 0


def test_wrong_language_code_is_rejected_safely():
    """Injected fault: a target language code that looks plausible but is
    not supported should raise a clear, safe error, not silently
    mistranslate or crash unpredictably."""
    glossary = load_glossary()
    try:
        translate("Hello world", "xx", glossary=glossary)
        assert False, "Expected ValueError for invalid language code"
    except ValueError as e:
        assert "Unsupported target language" in str(e)


def test_entity_corrupted_output_is_detected_and_flagged():
    """Injected fault: a sentence known (from prior testing) to trigger
    placeholder corruption should be correctly detected and routed to
    the review queue, not silently returned as if it were correct."""
    glossary = load_glossary()
    # This exact sentence is known from prior testing to corrupt 2 placeholders
    result = translate(
        "Hello, my name is Mamthasha and I study at SASTRA University.",
        "hi",
        glossary=glossary
    )
    assert result["review_status"] == "flagged"
    assert len(result["warnings"]) > 0


def test_review_queue_captures_all_required_fields():
    """Confirms a flagged entry in review_queue.json contains enough
    information to actually be useful for human review — not just a
    bare flag with no context."""
    import json
    glossary = load_glossary()
    translate("My name is Mamthasha and I study at SASTRA University.", "hi", glossary=glossary)

    with open("data/review_queue.json", "r", encoding="utf-8") as f:
        queue = json.load(f)

    assert len(queue) > 0
    last_entry = queue[-1]
    assert "source_text" in last_entry
    assert "target_lang" in last_entry
    assert "raw_output" in last_entry
    assert "missing_placeholders" in last_entry
    assert "reason" in last_entry