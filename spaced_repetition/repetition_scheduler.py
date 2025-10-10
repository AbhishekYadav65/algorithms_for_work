from datetime import datetime, timedelta

class SpacedRepetitionScheduler:
    """
    Smart spaced repetition engine:
    - Uses adaptive intervals based on user performance.
    - Mimics human forgetting curve.
    """

    def __init__(self):
        # Stores all question review records
        self.history = {}  # {qid: {last_seen, interval, ease_factor, next_due}}

    def add_question(self, qid: str):
        """Add a new question to the scheduler."""
        self.history[qid] = {
            "last_seen": datetime.now().date(),
            "interval": 1,        # 1 day for new questions
            "ease_factor": 2.5,   # baseline ease (Anki-like)
            "next_due": datetime.now().date() + timedelta(days=1)
        }

    def update_review(self, qid: str, correct: bool):
        """Update next review based on performance."""
        if qid not in self.history:
            self.add_question(qid)

        q = self.history[qid]
        today = datetime.now().date()

        # If user answered correctly
        if correct:
            # Increase ease slightly
            q["ease_factor"] = min(q["ease_factor"] + 0.1, 3.0)
            # Increase interval exponentially
            q["interval"] = int(q["interval"] * q["ease_factor"])
        else:
            # If wrong, reduce interval drastically (relearn sooner)
            q["ease_factor"] = max(q["ease_factor"] - 0.2, 1.3)
            q["interval"] = 1  # reset

        q["last_seen"] = today
        q["next_due"] = today + timedelta(days=q["interval"])
        self.history[qid] = q

    def get_due_today(self):
        """Return all questions that are due for review today."""
        today = datetime.now().date()
        due = [qid for qid, q in self.history.items() if q["next_due"] <= today]
        return due

    def summary(self):
        """Returns an overview of the spaced repetition schedule."""
        return {
            qid: {
                "interval_days": q["interval"],
                "ease_factor": round(q["ease_factor"], 2),
                "next_due": str(q["next_due"])
            }
            for qid, q in self.history.items()
        }
