def compute_proficiency(topic_data):
    scores = {}
    for topic, stats in topic_data.items():
        accuracy = stats["correct"] / stats["total"] if stats["total"] > 0 else 0
        score = (accuracy * 100) - (stats["avg_time"] / 10)
        scores[topic] = max(0, min(100, round(score, 2)))
    return scores
