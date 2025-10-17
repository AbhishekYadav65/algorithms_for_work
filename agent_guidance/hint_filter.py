# hint_filter.py
from __future__ import annotations
import re
from typing import Optional
from typing import Any

CODE_PATTERNS = [
    r"\bdef\b", r"\bclass\b", r"\bimport\b", r"\bfor\b", r"\bwhile\b",
    r"\{.*\}", r"<.*?>", r"->", r"return\s+", r";\s*$", r"printf\(", r"std::"
]

class HintFilter:
    """
    Ensures hints are conceptual only. Optionally accept a classifier (model)
    with .predict_proba([text]) -> [prob_code].
    """

    def __init__(self, classifier: Optional[Any] = None):
        self.classifier = classifier
        self.patterns = [re.compile(p) for p in CODE_PATTERNS]

    def _contains_code_by_regex(self, text: str) -> bool:
        low = text
        for pat in self.patterns:
            if pat.search(low):
                return True
        return False

    def filter_hint(self, text: str) -> str:
        # 1. quick regex block
        if self._contains_code_by_regex(text):
            return "Hint removed: contains code. Provide conceptual explanation only."

        # 2. classifier if available
        if self.classifier:
            try:
                proba = self.classifier.predict_proba([text])[0]
                # assume classifier returns [prob_non_code, prob_code]
                prob_code = proba[-1]
                if prob_code > 0.35:
                    return "Hint removed: contains code-like content. Use conceptual language."
            except Exception:
                pass

        # 3. sanitize backticks and code fences
        text = re.sub(r"```.*?```", "", text, flags=re.S)
        text = text.replace("`", "")
        return text.strip()
