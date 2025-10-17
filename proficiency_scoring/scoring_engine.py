# scoring_engine.py
from __future__ import annotations
from typing import Dict
from datetime import datetime, timedelta
import math

def compute_proficiency(topic_data: Dict[str, Dict]) -> Dict[str, float]:
    """
    Bayesian-inspired proficiency score per topic.
    Accounts for:
      - accuracy (correct/total)
      - avg_time (penalty)
      - recency decay (older attempts penalized)
    Returns 0-100 scores.
    """
    out = {}
    now = datetime.now()
    for topic, stats in topic_data.items():
        total = stats.get("total", 0)
        correct = stats.get("correct", 0)
        avg_time = stats.get("avg_time", 0) or 0
        last_attempt = stats.get("last_attempt_date", now)
        if isinstance(last_attempt, str):
            try:
                last_attempt = datetime.fromisoformat(last_attempt)
            except Exception:
                last_attempt = now

        # Bayesian prior: Beta(2,2) -> 0.5 baseline
        alpha = 2 + correct
        beta = 2 + (total - correct)
        mean = alpha / (alpha + beta)  # [0,1]

        # time penalty (log)
        time_pen = 1.0 / (1.0 + math.log1p(avg_time / 60.0))

        # recency decay: half-life 30 days
        days = max(0, (now - last_attempt).days)
        decay = 0.5 ** (days / 30.0)

        raw = mean * 0.7 + time_pen * 0.2 + decay * 0.1
        score = max(0.0, min(1.0, raw))
        out[topic] = round(score * 100, 2)
    return out
