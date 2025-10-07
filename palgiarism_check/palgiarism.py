import hashlib
import numpy as np
from sentence_transformers import SentenceTransformer

class PlagiarismChecker:
    """Detects duplicate or semantically similar questions."""

    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.question_db = {}  # {hash: {"text": str, "embedding": np.array}}

    def add_question(self, text: str):
        """Adds a question and its embedding to the database."""
        h = hashlib.sha256(text.encode()).hexdigest()
        emb = self.model.encode(text, convert_to_numpy=True)
        self.question_db[h] = {"text": text, "embedding": emb}

    def is_plagiarized(self, new_text: str, threshold: float = 0.85) -> bool:
        """Checks if a new question is plagiarized."""
        new_hash = hashlib.sha256(new_text.encode()).hexdigest()

        # Step 1: Exact match
        if new_hash in self.question_db:
            return True

        # Step 2: Semantic similarity
        new_emb = self.model.encode(new_text, convert_to_numpy=True)
        for q in self.question_db.values():
            sim = np.dot(new_emb, q["embedding"]) / (np.linalg.norm(new_emb) * np.linalg.norm(q["embedding"]))
            if sim >= threshold:
                return True
        return False
