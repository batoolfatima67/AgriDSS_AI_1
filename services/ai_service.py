import requests
from core.ndvi_engine import compute_ndvi_value
from core.risk_engine import compute_risk

def get_risk_from_api(ndvi, weather):

    url = "http://127.0.0.1:8000/analyze/"

    payload = {
        "ndvi": ndvi,
        "temp": weather["temp"],
        "humidity": weather["humidity"]
    }

    response = requests.post(url, json=payload)

    return response.json()
    
def generate_ai_report(ndvi, weather, crop):

    ndvi_analysis = compute_ndvi_value(ndvi)
    risk_analysis = compute_risk(ndvi, weather)

    return {
        "crop": crop,
        "ndvi_status": ndvi_analysis["status"],
        "risk_level": risk_analysis["category"],
        "risk_score": risk_analysis["risk_score"]
    }
