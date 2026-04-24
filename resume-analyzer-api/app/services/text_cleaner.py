import re

def clean_text(text):
    text = text.strip()
    # Normalize line endings
    text = text.replace("\r\n", "\n").replace("\r", "\n")

    # Remove too many blank lines
    text = re.sub(r"\n{3,}", "\n\n", text)

    # Normalize spaces
    text = re.sub(r"[ \t]+", " ", text)

    return text

def limit_text(text: str, max_chars: int = 12000) -> str:
    if len(text) <= max_chars:
        return text

    return text[:max_chars]