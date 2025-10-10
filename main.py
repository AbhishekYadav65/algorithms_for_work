# main.py
# main_demo.py
from unique_question_generator.generator import generate_unique_question
from plagiarism_check.plagiarism import PlagiarismChecker
from adaptive_difficulty.difficulty_engine import adjust_difficulty
from spaced_repetition.repetition_scheduler import schedule_reviews
from brain_memory.memory_context import analyze_weakness
from agent_guidance.hint_filter import filter_hint
from proficiency_scoring.scoring_engine import compute_proficiency
from session_builder.session_builder import build_session
from datetime import datetime

print("\n=== UNIQUE QUESTION GENERATOR ===")
q = generate_unique_question()
print("Generated Question:", q["question"])

print("\n=== PLAGIARISM CHECK ===")
checker = PlagiarismChecker()
checker.add_question(q["question"])
print("Duplicate?", checker.is_plagiarized(q["question"]))

print("\n=== ADAPTIVE DIFFICULTY ===")
level = adjust_difficulty(accuracy=0.8, avg_time=25, hints_used=1, current_level="medium")
print("Next Difficulty Level:", level)

print("\n=== SPACED REPETITION ===")
history = {"Q1": {"last_seen": datetime.now(), "correct": 2, "incorrect": 0}}
print("Due for Review:", schedule_reviews(history))

print("\n=== BRAIN MEMORY CONTEXT ===")
user_history = [("Arrays", True), ("Trees", False), ("Trees", False), ("Graphs", True)]
print("Weak Topics:", analyze_weakness(user_history))

print("\n=== AGENT GUIDANCE FILTER ===")
hint = "Use a for loop to iterate the array."
print("Filtered Hint:", filter_hint(hint))

print("\n=== PROFICIENCY SCORING ===")
topics = {
    "Arrays": {"correct": 8, "total": 10, "avg_time": 18},
    "Trees": {"correct": 4, "total": 10, "avg_time": 40}
}
print("Scores:", compute_proficiency(topics))

print("\n=== SESSION BUILDER ===")
session = build_session(["Q1","Q2","Q3"], ["Q4","Q5"], ["Q6","Q7","Q8","Q9"])
print("Final Session:", session)
