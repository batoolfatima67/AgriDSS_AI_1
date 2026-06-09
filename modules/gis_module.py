import geopandas as gpd
import streamlit as st


# -----------------------------
# LOAD SHAPEFILE SAFELY
# -----------------------------
def load_shapefile(path):

    try:
        gdf = gpd.read_file(path)
        return gdf

    except Exception as e:
        st.error(f"Error loading shapefile: {path}")
        st.error(str(e))
        return None


# -----------------------------
# GET ADMIN COLUMN SAFELY
# -----------------------------
def detect_column(gdf, possible_names):

    for col in possible_names:
        if col in gdf.columns:
            return col

    return None


# -----------------------------
# GET FILTERED GEOMETRY
# -----------------------------
def get_geometry(gdf, column, value):

    if gdf is None:
        return None, None

    if column not in gdf.columns:
        return None, None

    filtered = gdf[gdf[column] == value]

    if filtered.empty:
        return None, None

    geometry = filtered.geometry.iloc[0]

    return filtered, geometry
