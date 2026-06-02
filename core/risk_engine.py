def compute_risk(ndvi, weather):

    risk_score = 0

    if ndvi < 0.2:
        risk_score += 50
    elif ndvi < 0.5:
        risk_score += 25

    if weather["temp"] > 35:
        risk_score += 20

    if weather["humidity"] < 30:
        risk_score += 15

    return {
        "risk_score": risk_score,
        "category": "High" if risk_score > 60 else "Medium" if risk_score > 30 else "Low"
    }
