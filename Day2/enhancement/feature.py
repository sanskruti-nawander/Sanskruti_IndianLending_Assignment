# Day2/enhancement/feature.py
def compute_ews(dpd, cibil, outstanding, past_bounces):
    """
    Simple Early Warning Score (EWS) example.
    Returns a score between 0 and 100.
    """
    score = 0
    score += dpd * 2
    score += max(0, (650 - cibil) / 10)
    score += past_bounces * 5
    score += outstanding / 50000.0
    # clamp 0..100
    if score < 0:
        score = 0
    if score > 100:
        score = 100
    return round(score, 2)
