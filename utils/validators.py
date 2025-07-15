# utils/validators.py

import re

def clean_markdown_wrappers(text: str) -> str:
    """
    Removes markdown code blocks (```language) from GPT output.
    """
    text = re.sub(r'```[\w]*\n?', '', text)
    text = re.sub(r'```', '', text)
    return text.strip()

def is_valid_translation(original: str, translated: str) -> bool:
    """
    Checks if translated text maintains the structure of the original.
    """
    if re.findall(r'<\?php', original) != re.findall(r'<\?php', translated):
        return False
    if re.findall(r'\?>', original) != re.findall(r'\?>', translated):
        return False

    tags = ['<div', '<section', '<header', '<footer', '<main', '<article']
    for tag in tags:
        if original.lower().count(tag) != translated.lower().count(tag):
            return False

    if len(translated.strip()) < len(original.strip()) * 0.3:
        return False

    return True
