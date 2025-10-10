import re

def filter_hint(text: str) -> str:
    code_patterns = [r"def ", r"class ", r"\{.*\}", r"<.*>", r"import ", r"\bfor\b", r"\bwhile\b"]
    for pattern in code_patterns:
        if re.search(pattern, text):
            return "Hint removed: contains code. Use conceptual explanation only."
    return text
