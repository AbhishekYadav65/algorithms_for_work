# generator.py
from __future__ import annotations
import random
import hashlib
import time
from typing import Dict, List, Optional, Set, Any

TEMPLATES = [
    "Write an algorithm to find the {target} in a {structure} of size {n}.",
    "Design a program that computes the {target} within a {structure} containing {n} elements.",
    "How would you determine the {target} from a {structure} having {n} entries?"
]

VARIABLES = {
    "target": ["maximum element", "minimum element", "sum", "frequency of a number"],
    "structure": ["array", "linked list", "binary tree", "graph"],
    "n": [10, 50, 100, 500, 1000]
}


class QuestionExhaustionError(RuntimeError):
    pass


class QuestionGenerator:
    """
    Template + controlled LLM paraphrase based generator.
    Inject `llm` with .paraphrase(text, temperature) -> str for production.
    """

    def __init__(self, db_client: Optional[Any] = None, llm: Optional[Any] = None, used_hashes: Optional[Set[str]] = None):
        self.db = db_client
        self.llm = llm
        self.used_hashes = used_hashes if used_hashes is not None else set()
        self.max_attempts = 12

    def _compose(self) -> str:
        template = random.choice(TEMPLATES)
        filled = template.format(
            target=random.choice(VARIABLES["target"]),
            structure=random.choice(VARIABLES["structure"]),
            n=random.choice(VARIABLES["n"])
        )
        return filled

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.strip().lower().encode()).hexdigest()

    def _llm_paraphrase(self, text: str, difficulty: str = "medium") -> str:
        if self.llm:
            try:
                return self.llm.paraphrase(text, difficulty=difficulty)
            except Exception:
                pass
        # deterministic lightweight paraphrase fallback
        swaps = {"Write": "Design", "Design": "Construct", "How would you determine": "Determine"}
        out = text
        for k, v in swaps.items():
            out = out.replace(k, v)
        return out

    def _exists(self, h: str) -> bool:
        if h in self.used_hashes:
            return True
        if self.db:
            try:
                cur = self.db.cursor()
                cur.execute("SELECT 1 FROM questions WHERE post_hash = %s LIMIT 1", (h,))
                return cur.fetchone() is not None
            except Exception:
                pass
        return False

    def generate_unique_question(self, topic: str, week: int, difficulty: str = "medium", max_attempts: Optional[int] = None) -> Dict:
        attempts = 0
        max_attempts = max_attempts or self.max_attempts
        while attempts < max_attempts:
            attempts += 1
            base = self._compose()
            paraphrased = self._llm_paraphrase(base, difficulty)
            post_hash = self._hash(paraphrased)
            if not self._exists(post_hash):
                self.used_hashes.add(post_hash)
                q = {
                    "question": paraphrased,
                    "template": base,
                    "topic": topic,
                    "week": week,
                    "difficulty": difficulty,
                    "post_hash": post_hash,
                    "created_at": int(time.time())
                }
                return q
        raise QuestionExhaustionError("Unable to generate unique question after attempts.")
