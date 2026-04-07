def grader(output):
    score = 0
    if "attack" in output.lower():
        score += 0.5
    if "explain" in output.lower():
        score += 0.5
    return score