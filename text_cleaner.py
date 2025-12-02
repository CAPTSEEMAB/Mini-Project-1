import spacy

# Load spaCy model once at module level
nlp = spacy.load("en_core_web_sm")


def clean_text(text: str) -> str:
    """Remove stopwords and punctuation using spaCy."""
    doc = nlp(text.lower())
    tokens = [
        token.text for token in doc 
        if not token.is_stop and not token.is_punct and not token.is_space
    ]
    return " ".join(tokens)

