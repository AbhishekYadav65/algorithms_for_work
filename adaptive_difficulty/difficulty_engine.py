def adjust_difficulty(accuracy, avg_time, hints_used, current_level):
    weights = {"accuracy": 0.6, "time": 0.3, "hints": 0.1}
    score = (accuracy * weights["accuracy"]) - (avg_time * weights["time"] / 60) - (hints_used * weights["hints"])

    if score > 0.7:
        return "hard" if current_level == "medium" else "medium"
    elif score < 0.4:
        return "easy" if current_level == "medium" else "medium"
    return current_level
