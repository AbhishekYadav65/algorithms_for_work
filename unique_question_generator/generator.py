import random
import hashlib
from typing import Dict

# --- Template Bank ---
TEMPLATES = [
    "Write an algorithm to find the {target} in a {structure} of size {n}.",
    "Design a program that computes the {target} within a {structure} containing {n} elements.",
    "How would you determine the {target} from a {structure} having {n} entries?"
]

# --- Variable Pools ---
VARIABLES = {
    "target": ["maximum element", "minimum element", "sum", "frequency of a number"],
    "structure": ["array", "linked list", "binary tree", "graph"],
    "n": [10, 50, 100, 500, 1000]
}

# --- In-memory database (for demo use only) ---
used_hashes = set()

def generate_unique_question() -> Dict:
    """Generates a new unique question by combining templates and random variables."""
    while True:
        # 1. Select a random template
        template = random.choice(TEMPLATES)

        # 2. Replace placeholders
        filled = template.format(
            target=random.choice(VARIABLES["target"]),
            structure=random.choice(VARIABLES["structure"]),
            n=random.choice(VARIABLES["n"])
        )

        # 3. Paraphrasing (simple placeholder)
        paraphrased = filled.replace("Write", "Design") if "Write" in filled else filled

        # 4. Compute hash
        h = hashlib.sha256(paraphrased.encode()).hexdigest()

        # 5. Check uniqueness
        if h not in used_hashes:
            used_hashes.add(h)
            return {
                "question": paraphrased,
                "hash": h,
                "metadata": {
                    "difficulty": random.choice(["easy", "medium", "hard"]),
                    "topic": random.choice(["DSA", "DBMS", "OOP", "Math"])
                }
            }
