import re
import string
import json

STOPWORDS = {
    "a", "an", "the", "and", "or", "in", "on", "to", "for", "of", "is", "are",
    "was", "were", "be", "this", "that", "it", "with", "as", "by"
}

def normalize_text(text: str) -> str:
    text = text.lower()
    #print(text)
    text = re.sub(f"[{re.escape(string.punctuation)}]", " ", text)
    text = re.sub(r"\s+", " ", text).strip()
    return text

def tokenize(text: str):
    return text.split()

def remove_stopwords(tokens):
    return [t for t in tokens if t not in STOPWORDS]

def clean_text(text: str) -> str:
    #print(text)
    text = normalize_text(text)
    tokens = tokenize(text)
    tokens = remove_stopwords(tokens)
    return " ".join(tokens)
