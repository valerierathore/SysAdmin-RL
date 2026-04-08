def normalize(x):
    if x <= 0:
        return 0.01
    if x >= 1:
        return 0.99
    return x


def easy_grader(output=None, **kwargs):
    try:
        r = output.get("reward", 0.1)
        return normalize(float(r))
    except:
        return 0.5


def medium_grader(output=None, **kwargs):
    try:
        r = output.get("reward", 0.1)
        return normalize(float(r))
    except:
        return 0.5


def hard_grader(output=None, **kwargs):
    try:
        r = output.get("reward", 0.1)
        return normalize(float(r))
    except:
        return 0.5
