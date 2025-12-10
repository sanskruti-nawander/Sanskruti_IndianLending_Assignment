# Sample enhancement feature: Early Warning Score
def compute_ews(dpd, cibil, outstanding, past_bounces):
    score = 0
    score += dpd * 2
    score += (650 - cibil) / 10
    score += past_bounces * 5
    score += outstanding / 50000
    return max(0, min(100, score))
from feature import compute_ews
print(compute_ews(90, 620, 150000, 2))

