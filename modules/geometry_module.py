def get_geometry(gdf, region_column, selected_region):

    filtered_gdf = gdf[gdf[region_column] == selected_region]

    geometry = filtered_gdf.geometry.iloc[0]

    return filtered_gdf, geometry
