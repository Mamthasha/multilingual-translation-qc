import re
import json

PATTERNS = [
    ("URL", re.compile(r'https?://\S+')),
    ("HASHTAG", re.compile(r'#\w+')),
    ("MENTION", re.compile(r'@\w+')),
    ("NUMBER", re.compile(r'\b\d+(\.\d+)?\b')),
]

NUM_WORDS = ["ZERO", "ONE", "TWO", "THREE", "FOUR", "FIVE", "SIX", "SEVEN",
             "EIGHT", "NINE", "TEN", "ELEVEN", "TWELVE", "THIRTEEN",
             "FOURTEEN", "FIFTEEN"]


def make_placeholder(counter):
    """Generates placeholder tokens that survive subword tokenization better
    than underscore/digit-heavy tokens like __ENT_0__."""
    word = NUM_WORDS[counter] if counter < len(NUM_WORDS) else f"NUM{counter}"
    return f"XxEntity{word}xX"


def load_glossary(path="configs/glossary.json"):
    """Loads a list of terms that must never be translated (names, brands, etc.)"""
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def protect_entities(text, glossary=None):
    """
    Replaces glossary terms, URLs, hashtags, mentions, and numbers
    with placeholder tokens.

    Returns:
        protected_text: the text with entities replaced
        entity_map: dict mapping placeholder -> original value
    """
    entity_map = {}
    counter = 0
    protected_text = text

    # Protect glossary terms first (longest match first, avoids partial overlaps)
    if glossary:
        for term in sorted(glossary, key=len, reverse=True):
            pattern = re.compile(r'\b' + re.escape(term) + r'\b')
            matches = list(pattern.finditer(protected_text))
            for match in reversed(matches):
                placeholder = make_placeholder(counter)
                entity_map[placeholder] = match.group(0)
                start, end = match.span()
                protected_text = protected_text[:start] + placeholder + protected_text[end:]
                counter += 1

    # Then protect URLs, hashtags, mentions, numbers
    for label, pattern in PATTERNS:
        matches = list(pattern.finditer(protected_text))
        for match in reversed(matches):
            placeholder = make_placeholder(counter)
            entity_map[placeholder] = match.group(0)
            start, end = match.span()
            protected_text = protected_text[:start] + placeholder + protected_text[end:]
            counter += 1

    return protected_text, entity_map


def restore_entities(translated_text, entity_map):
    """Puts the original values back in place of the placeholder tokens."""
    restored_text = translated_text
    for placeholder, original_value in entity_map.items():
        restored_text = restored_text.replace(placeholder, original_value)
    return restored_text


if __name__ == "__main__":
    sample = "Hello, my name is Mamthasha and I study at SASTRA University. Visit https://sastra.edu or call 12345, #placement2027"
    glossary = ["Mamthasha", "SASTRA", "SASTRA University"]

    protected, mapping = protect_entities(sample, glossary=glossary)
    print("Original: ", sample)
    print("Protected:", protected)
    print("Mapping:  ", mapping)

    restored = restore_entities(protected, mapping)
    print("Restored: ", restored)
    print("Match original?", restored == sample)