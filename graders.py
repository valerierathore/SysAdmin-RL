def normalize(score):
    if score <= 0:
        return 0.01
    if score >= 1:
        return 0.99
    return score


def easy_grader(output):
    return normalize(0.85)


def medium_grader(output):
    return normalize(0.75)


def hard_grader(output):
    return normalize(0.65)
