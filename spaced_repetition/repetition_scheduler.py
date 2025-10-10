from datetime import datetime, timedelta

def schedule_reviews(history):
    today = datetime.now().date()
    due = []
    for qid, record in history.items():
        base_interval = 1
        interval = base_interval * (record["correct"] + 1) / (record["incorrect"] + 1)
        next_due = record["last_seen"] + timedelta(days=interval)
        if next_due <= today:
            due.append(qid)
    return due
