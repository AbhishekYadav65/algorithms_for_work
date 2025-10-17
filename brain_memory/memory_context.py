# memory_context.py
from __future__ import annotations
from typing import List, Tuple, Dict, Optional, Any
from collections import deque, defaultdict
import numpy as np

SHORT_TERM_LIMIT = 10

class MemoryContext:
    """
    Short-term and long-term memory manager.
    - short_term: last N attempts
    - long_term: per-topic stats and vector (optional embedding)
    """

    def __init__(self, embedding_model: Optional[Any] = None):
        self.short_term = deque(maxlen=SHORT_TERM_LIMIT)  # list of (topic, correct, meta)
        self.topic_stats = defaultdict(lambda: {"correct": 0, "total": 0})
        self.embedding_model = embedding_model
        self.topic_vectors: Dict[str, np.ndarray] = {}

    def record_attempt(self, topic: str, correct: bool, metadata: Optional[Dict] = None):
        self.short_term.append((topic, correct, metadata or {}))
        s = self.topic_stats[topic]
        s["total"] += 1
        s["correct"] += 1 if correct else 0
        self.topic_stats[topic] = s

    def analyze_weakness(self, top_k: int = 5) -> List[Tuple[str, float]]:
        """Return topics sorted by weakness score (higher = weaker)"""
        weakness = {}
        for t, v in self.topic_stats.items():
            if v["total"] == 0:
                continue
            acc = v["correct"] / v["total"]
            score = 1.0 - acc  # simple weakness
            weakness[t] = score
        sorted_w = sorted(weakness.items(), key=lambda x: x[1], reverse=True)
        return sorted_w[:top_k]

    def topic_vector(self, topic: str, refresh: bool = False) -> Optional[np.ndarray]:
        """Compute or return cached topic embedding if model provided."""
        if topic in self.topic_vectors and not refresh:
            return self.topic_vectors[topic]
        if self.embedding_model:
            vec = self.embedding_model.encode(topic, convert_to_numpy=True)
            self.topic_vectors[topic] = vec
            return vec
        return None

    def recent_pattern(self) -> Dict[str, int]:
        """Count recent failures per topic"""
        counts = defaultdict(int)
        for topic, correct, _ in self.short_term:
            if not correct:
                counts[topic] += 1
        return dict(counts)
