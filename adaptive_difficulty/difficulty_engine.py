# difficulty_engine.py
from __future__ import annotations
from typing import Tuple
import math

LEVELS = ["easy", "medium", "hard"]
LEVEL_SCORE = {"easy": 0.25, "medium": 0.5, "hard": 0.85}

def _ema(prev: float, value: float, alpha: float = 0.2) -> float:
    return alpha * value + (1 - alpha) * prev

def normalize_time(time_s: float, baseline: float = 120.0) -> float:
    """Return value in [0,1] where low time -> closer to 1."""
    return 1.0 / (1.0 + math.log1p(time_s / baseline))

def adjust_difficulty(
    accuracy: float,
    avg_time: float,
    hints_used: int,
    current_level: str,
    question_difficulty: str,
    user_ema: float
) -> Tuple[str, float]:
    """
    Returns (new_level, new_ema)
    - Uses EMA for smoothing user_ema.
    - Produces probabilistic move with momentum.
    """
    acc = max(0.0, min(1.0, accuracy))
    tnorm = normalize_time(avg_time)
    hint_pen = max(0.0, min(1.0, hints_used / 10.0))

    raw_score = 0.62 * acc + 0.28 * tnorm - 0.10 * hint_pen
    # fuse with user_ema
    new_ema = _ema(user_ema, raw_score, alpha=0.18)

    # momentum: require delta threshold to change level
    current_score = LEVEL_SCORE.get(current_level, 0.5)
    delta = new_ema - current_score

    if delta > 0.12:
        # increase one level if possible
        new_level = LEVELS[min(LEVELS.index(current_level) + 1, len(LEVELS) - 1)]
    elif delta < -0.12:
        new_level = LEVELS[max(LEVELS.index(current_level) - 1, 0)]
    else:
        new_level = current_level

    return new_level, round(new_ema, 4)
