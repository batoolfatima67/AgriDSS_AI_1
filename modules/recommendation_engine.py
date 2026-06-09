import streamlit as st


def generate_recommendation(ndvi, weather, crop):

    rec = {
        "status": "",
        "irrigation": "",
        "fertilizer": ""
    }

    if ndvi < 0.2:
        rec["status"] = "Severe Stress"
        rec["irrigation"] = "Immediate irrigation required"
        rec["fertilizer"] = "High nitrogen fertilizer needed"

    elif ndvi < 0.5:
        rec["status"] = "Moderate Stress"
        rec["irrigation"] = "Schedule irrigation soon"
        rec["fertilizer"] = "Balanced fertilizer recommended"

    else:
        rec["status"] = "Healthy Crop"
        rec["irrigation"] = "Normal irrigation"
        rec["fertilizer"] = "No fertilizer needed"

    if weather and weather.get("temp", 0) > 35:
        rec["irrigation"] += " (Heat stress risk)"

    return rec
