# 🧠 Algorithm Layer — IIT Madras Project

This repository contains all algorithmic modules designed by **Abhishek Rai**
for the **Adaptive Learning System** startup project.

---

## 📘 Algorithms

### 1️⃣ Unique Question Generator
- Generates endless unique practice questions using templates, random variables, and paraphrasing.
- Prevents repetition using SHA256 hashing.
- Produces metadata like topic and difficulty.
- Located in: `unique_question_generator/`

### 2️⃣ Plagiarism Check Algorithm
- Detects duplicate or semantically similar questions.
- Uses hash matching and cosine similarity of sentence embeddings.
- Located in: `plagiarism_check/`

---

## ⚙️ How to Use

```bash
# Install dependencies
pip install sentence-transformers numpy

# Run unique question generator
python -m unique_question_generator.generator

# Run plagiarism checker
python -m palgiarism_check.palgiarism
```
