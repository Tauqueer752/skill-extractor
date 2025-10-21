import spacy
import re
from fuzzywuzzy import fuzz

import spacy
import subprocess
import sys

# Try load model, agar fail ho to download kar do
try:
    nlp = spacy.load("en_core_web_sm")
except OSError:
    subprocess.run([sys.executable, "-m", "spacy", "download", "en_core_web_sm"])
    nlp = spacy.load("en_core_web_sm")


# Load skills
with open("skills_list.txt", "r", encoding="utf-8") as f:
    SKILLS = [line.strip().lower() for line in f if line.strip()]

# Synonym mapping
SYNONYMS = {
    "js": "javascript",
    "ml": "machine learning",
    "ai": "artificial intelligence",
    "ms excel": "excel",
    "powerbi": "power bi",
    "ppt": "powerpoint",
    "tf": "tensorflow",
    "py": "python",
    "dl": "deep learning",
    "dbms": "sql",
}

def normalize_text(text):
    """Replace synonyms with full skill names."""
    text = text.lower()
    for short, full in SYNONYMS.items():
        text = re.sub(r'\b' + re.escape(short) + r'\b', full, text)
    return text


def extract_skills(text):
    """Extract technical skills using NLP + synonym + fuzzy matching."""
    text = normalize_text(text)
    doc = nlp(text)
    found = set()

    # Keyword matching
    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)

    # Token-based check
    for token in doc:
        token_text = token.text.lower()
        for skill in SKILLS:
            if fuzz.ratio(token_text, skill) > 90:
                found.add(skill)

    return sorted(list(found))
