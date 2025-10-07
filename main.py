# main.py
from unique_question_generator.generator import generate_unique_question
from plagiarism_check.plagiarism import PlagiarismChecker

# Initialize the plagiarism checker
checker = PlagiarismChecker()

# Generate two questions
q1 = generate_unique_question()["question"]
q2 = generate_unique_question()["question"]

print("Question 1:", q1)
print("Question 2:", q2)

# Add first question to DB
checker.add_question(q1)

# Check if the second one is plagiarized
print("Is Question 2 plagiarized?", checker.is_plagiarized(q2))
