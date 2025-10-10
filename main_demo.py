from spaced_repetition.repetition_scheduler import SpacedRepetitionScheduler

print("\n=== SPACED REPETITION ===")
sr = SpacedRepetitionScheduler()

# Add 3 sample questions
sr.add_question("Q1")
sr.add_question("Q2")
sr.add_question("Q3")

# Simulate reviews
sr.update_review("Q1", correct=True)
sr.update_review("Q2", correct=False)
sr.update_review("Q3", correct=True)

print("Due Today:", sr.get_due_today())
print("Scheduler Summary:")
for qid, data in sr.summary().items():
    print(f"  {qid}: {data}")
