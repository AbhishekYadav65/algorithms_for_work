# session_builder.py
from __future__ import annotations
import random
from typing import List, Dict, Optional

class InsufficientQuestionsError(RuntimeError):
    pass

def _unique_by_id(pool: List[Dict]) -> List[Dict]:
    seen = set()
    out = []
    for q in pool:
        qid = q.get("id")
        if qid in seen:
            continue
        seen.add(qid)
        out.append(q)
    return out

def build_session(
    weak: List[Dict],
    review: List[Dict],
    new: List[Dict],
    week_filter: Optional[List[int]] = None,
    all_questions_pool: Optional[List[Dict]] = None,
    total: int = 10,
    ratios: Optional[Dict[str, float]] = None,
    min_viable: int = 3
) -> List[Dict]:
    """
    Build a session with given pools.
    - ratios default: 60% weak, 30% review, 10% new
    - Backfill from all_questions_pool when pools insufficient.
    """
    ratios = ratios or {"weak": 0.6, "review": 0.3, "new": 0.1}
    weak = _unique_by_id(weak)
    review = _unique_by_id(review)
    new = _unique_by_id(new)
    all_pool = _unique_by_id(all_questions_pool or (weak + review + new))

    if len(all_pool) < min_viable:
        raise InsufficientQuestionsError("Not enough questions available.")

    want_weak = int(total * ratios["weak"])
    want_review = int(total * ratios["review"])
    want_new = total - (want_weak + want_review)

    session = []
    def take(pool, n):
        if not pool or n <= 0:
            return []
        return random.sample(pool, min(n, len(pool)))

    session += take(weak, want_weak)
    session += take(review, want_review)
    session += take(new, want_new)

    # backfill
    if len(session) < total:
        existing_ids = {q["id"] for q in session}
        candidates = [q for q in all_pool if q["id"] not in existing_ids]
        need = total - len(session)
        if not candidates:
            # nothing new; allow sampling from session (shouldn't happen)
            pass
        else:
            session += random.sample(candidates, min(need, len(candidates)))

    # final safety
    session = _unique_by_id(session)
    if len(session) < total:
        # permissive backfill allowing duplicates only if unavoidable
        extra = (weak + review + new + all_pool)
        i = 0
        while len(session) < total and i < len(extra):
            cand = extra[i % len(extra)]
            if cand["id"] not in {q["id"] for q in session}:
                session.append(cand)
            i += 1

    # final shuffle and trim
    random.shuffle(session)
    return session[:total]
