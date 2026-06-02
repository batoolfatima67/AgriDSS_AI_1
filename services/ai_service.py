from core.ndvi_engine import compute_ndvi_value
from core.risk_engine import compute_risk


def generate_ai_report(ndvi, weather, crop):

    ndvi_analysis = compute_ndvi_value(ndvi)
    risk_analysis = compute_risk(ndvi, weather)

    return {
        "crop": crop,
        "ndvi_status": ndvi_analysis["status"],
        "risk_level": risk_analysis["category"],
        "risk_score": risk_analysis["risk_score"]
    }
