# plagiarism.py
from __future__ import annotations
import hashlib
from typing import Dict, Optional, Tuple, List
import numpy as np
from typing import Any

try:
    import faiss
    FAISS_AVAILABLE = True
except Exception:
    FAISS_AVAILABLE = False

try:
    from sentence_transformers import SentenceTransformer
    ST_AVAILABLE = True
except Exception:
    ST_AVAILABLE = False

class PlagiarismChecker:
    """
    Fast semantic duplicate detection.
    - If FAISS + SentenceTransformer available uses them.
    - Otherwise falls back to CPU brute force using simple embeddings or text hashes.
    """

    def __init__(self, db_client: Optional[Any] = None, model_name: str = "all-MiniLM-L6-v2"):
        self.db = db_client
        self.model = None
        self.index = None
        self.id_to_hash = {}  # mapping local id -> post_hash
        self.embeddings = []  # list of numpy arrays
        self.ids = []         # list of question ids
        if ST_AVAILABLE:
            try:
                self.model = SentenceTransformer(model_name)
            except Exception:
                self.model = None

        if FAISS_AVAILABLE:
            self.index = None  # will init on first add

    def _hash(self, text: str) -> str:
        return hashlib.sha256(text.strip().lower().encode()).hexdigest()

    def add_question(self, qid: int, text: str):
        """Register question with id and embedding for future comparisons."""
        h = self._hash(text)
        self.id_to_hash[qid] = h
        if self.model:
            emb = self.model.encode(text, convert_to_numpy=True)
            emb = emb.astype('float32')
            self.embeddings.append(emb)
            self.ids.append(qid)
            if FAISS_AVAILABLE:
                dim = emb.shape[0]
                if self.index is None:
                    self.index = faiss.IndexFlatIP(dim)
                    self.index.add(np.stack(self.embeddings).astype('float32'))
                else:
                    self.index.add(np.expand_dims(emb, axis=0))
        else:
            # no embedding model: store only hash
            pass

    def is_plagiarized(self, new_text: str, threshold: float = 0.85) -> Tuple[bool, Optional[int]]:
        """Returns (is_plagiarized, similar_qid)"""
        new_hash = self._hash(new_text)
        # Exact match quick check
        for qid, h in self.id_to_hash.items():
            if h == new_hash:
                return True, qid

        # Embedding similarity check
        if self.model and (FAISS_AVAILABLE and self.index is not None or self.embeddings):
            new_emb = self.model.encode(new_text, convert_to_numpy=True).astype('float32')
            if FAISS_AVAILABLE and self.index is not None:
                k = min(5, len(self.ids))
                D, I = self.index.search(np.expand_dims(new_emb, axis=0), k)
                sims = D[0]
                idxs = I[0]
                for sim, idx in zip(sims, idxs):
                    if sim >= threshold:
                        return True, self.ids[idx]
            else:
                # brute-force CPU
                norms = np.linalg.norm(np.stack(self.embeddings), axis=1) * (np.linalg.norm(new_emb) + 1e-12)
                dots = np.dot(np.stack(self.embeddings), new_emb)
                sims = dots / norms
                best_idx = int(np.argmax(sims))
                if sims[best_idx] >= threshold:
                    return True, self.ids[best_idx]

        return False, None
