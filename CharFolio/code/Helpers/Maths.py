

def ab_mod(score):
    if score < 1:
        raise ValueError("Scores must be >= 1")
    return (score-10)//2