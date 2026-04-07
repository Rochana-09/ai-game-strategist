def grader(output):
    score = 0
    keywords = ["attack", "defend", "strategy"]

    for k in keywords:
        if k in output.lower():
            score += 1/3

    return score