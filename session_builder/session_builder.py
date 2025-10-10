import random

def build_session(weak, review, new, total=10):
    session = []
    session += random.sample(weak, min(int(0.3 * total), len(weak)))
    session += random.sample(review, min(int(0.3 * total), len(review)))
    session += random.sample(new, min(int(0.4 * total), len(new)))
    random.shuffle(session)
    return session
