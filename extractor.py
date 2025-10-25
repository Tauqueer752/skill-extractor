import re
from fuzzywuzzy import fuzz

# Load skills list
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
    """Extract technical skills using synonym + fuzzy matching."""
    text = normalize_text(text)
    found = set()

    for skill in SKILLS:
        if re.search(r'\b' + re.escape(skill) + r'\b', text):
            found.add(skill)
        else:
            for word in text.split():
                if fuzz.ratio(word, skill) > 90:
                    found.add(skill)

    return sorted(found)

