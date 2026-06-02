from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def home():
    return {"message": "AgriDSS_AI Backend Running"}

@app.post("/analyze/")
def analyze(data: dict):

    ndvi = data.get("ndvi")
    temp = data.get("temp")
    humidity = data.get("humidity")

    risk = 0

    if ndvi < 0.2:
        risk += 50
    elif ndvi < 0.5:
        risk += 25

    if temp > 35:
        risk += 20

    if humidity < 30:
        risk += 15

    return {
        "risk_score": risk,
        "status": "High" if risk > 60 else "Medium" if risk > 30 else "Low"
    }
