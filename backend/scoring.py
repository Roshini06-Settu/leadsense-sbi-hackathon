# scoring.py
# Simple weighted scoring formula for lead prioritization.
# In production, this can be replaced with a trained ML model (e.g., scikit-learn).

def calculate_score(events):
    """
    events: dict with visitor activity data, e.g.
    {
        "pages_visited": 3,
        "time_on_site_seconds": 120,
        "used_calculator": True,
        "started_application": True,
        "completed_application": False,
        "revisits": 2
    }
    Returns: score (0-100), reason (string)
    """
    score = 0
    reasons = []

    pages = events.get("pages_visited", 0)
    score += min(pages * 8, 24)
    if pages >= 2:
        reasons.append(f"Visited {pages} pages")

    time_spent = events.get("time_on_site_seconds", 0)
    time_score = min((time_spent / 60) * 5, 20)
    score += time_score
    if time_spent >= 60:
        reasons.append(f"Spent {round(time_spent/60,1)} min on site")

    if events.get("used_calculator"):
        score += 15
        reasons.append("Used EMI/loan calculator")

    if events.get("started_application") and not events.get("completed_application"):
        score += 25
        reasons.append("Started but did not complete application")
    elif events.get("completed_application"):
        score += 30
        reasons.append("Completed application")

    revisits = events.get("revisits", 0)
    score += min(revisits * 6, 18)
    if revisits >= 1:
        reasons.append(f"Returned to site {revisits} time(s)")

    score = min(round(score), 100)

    if score >= 70:
        label = "Hot"
    elif score >= 40:
        label = "Warm"
    else:
        label = "Cold"

    reason_text = ", ".join(reasons) if reasons else "Low engagement"

    return {
        "score": score,
        "label": label,
        "reason": reason_text
    }
