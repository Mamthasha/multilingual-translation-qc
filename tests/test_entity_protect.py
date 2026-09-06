import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))

from entity_protect import protect_entities, restore_entities, make_placeholder


def test_url_is_protected_and_restored():
    text = "Visit https://sastra.edu for details."
    protected, mapping = protect_entities(text)
    assert "https://sastra.edu" not in protected
    restored = restore_entities(protected, mapping)
    assert restored == text


def test_hashtag_is_protected_and_restored():
    text = "Follow #placement2027 for updates."
    protected, mapping = protect_entities(text)
    assert "#placement2027" not in protected
    restored = restore_entities(protected, mapping)
    assert restored == text


def test_number_is_protected_and_restored():
    text = "The package weighs 12.5 kg and costs 499 rupees."
    protected, mapping = protect_entities(text)
    assert "12.5" not in protected
    assert "499" not in protected
    restored = restore_entities(protected, mapping)
    assert restored == text


def test_glossary_term_is_protected_and_restored():
    text = "I study at SASTRA University."
    glossary = ["SASTRA University"]
    protected, mapping = protect_entities(text, glossary=glossary)
    assert "SASTRA University" not in protected
    restored = restore_entities(protected, mapping)
    assert restored == text


def test_ordinary_capitalized_words_are_not_wrongly_protected():
    # Regression test for F002 — plain capitalized words should NOT
    # be treated as entities when no glossary term matches them
    text = "Hello, Visit our campus soon."
    protected, mapping = protect_entities(text, glossary=[])
    assert "Hello" in protected
    assert "Visit" in protected


def test_multiple_entity_types_together():
    text = "Hello, my name is Mamthasha. Visit https://sastra.edu or call 12345, #placement2027"
    glossary = ["Mamthasha"]
    protected, mapping = protect_entities(text, glossary=glossary)
    restored = restore_entities(protected, mapping)
    assert restored == text
    assert len(mapping) == 4  # Mamthasha, URL, number, hashtag


def test_empty_text_does_not_crash():
    protected, mapping = protect_entities("", glossary=[])
    assert protected == ""
    assert mapping == {}


def test_no_entities_present():
    text = "the quick brown fox"
    protected, mapping = protect_entities(text, glossary=[])
    assert protected == text
    assert mapping == {}


def test_make_placeholder_format():
    placeholder = make_placeholder(0)
    assert placeholder.startswith("XxEntity")
    assert placeholder.endswith("xX")