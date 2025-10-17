# repetition_scheduler.py
from __future__ import annotations
from datetime import date, timedelta
from typing import Dict, Optional, List, Any
import math

class SpacedRepetitionScheduler:
    """
    Parametric spaced repetition.
    Use persistence layer (db) through optional db_client with expected table `review_schedule`.
    In-memory fallback provided for testing.
    """

    def __init__(self, db_client: Optional[Any] = None, user_id: Optional[int] = None):
        self.db = db_client
        self.user_id = user_id
        self.history: Dict[str, Dict] = {}  # qid -> {last_seen, interval, ease_factor, next_due}
        self.base = 1

    def add_question(self, qid: str, today: Optional[date] = None):
        d = today or date.today()
        self.history[qid] = {
            "last_seen": d,
            "interval": self.base,
            "ease_factor": 2.5,
            "next_due": d + timedelta(days=self.base)
        }

    def update_review(self, qid: str, correct: bool, today: Optional[date] = None):
        if qid not in self.history:
            self.add_question(qid, today)
        today = today or date.today()
        q = self.history[qid]
        if correct:
            q["ease_factor"] = min(3.0, q["ease_factor"] + 0.1)
            # exponential growth controlled by ease_factor
            q["interval"] = max(1, int(q["interval"] * q["ease_factor"]))
        else:
            q["ease_factor"] = max(1.3, q["ease_factor"] - 0.25)
            q["interval"] = 1
        q["last_seen"] = today
        q["next_due"] = today + timedelta(days=q["interval"])
        self.history[qid] = q

    def get_due_today(self, today: Optional[date] = None, limit: Optional[int] = None) -> List[str]:
        today = today or date.today()
        due = [qid for qid, meta in self.history.items() if meta["next_due"] <= today]
        if limit:
            return due[:limit]
        return due

    def summary(self):
        return {
            qid: {
                "interval_days": v["interval"],
                "ease_factor": round(v["ease_factor"], 2),
                "next_due": str(v["next_due"])
            }
            for qid, v in self.history.items()
        }
