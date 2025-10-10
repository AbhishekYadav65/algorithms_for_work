def analyze_weakness(user_history):
    topic_stats = {}
    for topic, result in user_history:
        if topic not in topic_stats:
            topic_stats[topic] = {"correct": 0, "total": 0}
        topic_stats[topic]["total"] += 1
        if not result:
            topic_stats[topic]["correct"] += 0
        else:
            topic_stats[topic]["correct"] += 1

    weakness = {t: 1 - (v["correct"] / v["total"]) for t, v in topic_stats.items()}
    return sorted(weakness.items(), key=lambda x: x[1], reverse=True)
