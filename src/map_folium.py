import os
import pandas as pd
import folium
from folium.plugins import HeatMap
from .config import PROCESSED

def main():
    df = pd.read_parquet(os.path.join(PROCESSED, "bdiff_1973_2024.parquet"))
    df = df[["latitude_centre", "longitude_centre", "Surface parcourue (m2)"]].dropna()
    df = df[df["Surface parcourue (m2)"].between(1, 1e6)]
    m = folium.Map(location=[46.5, 2.5], zoom_start=6, tiles="CartoDB positron")
    HeatMap(df.values.tolist(), radius=7, blur=10, max_zoom=10).add_to(m)
    out = os.path.join(PROCESSED, "heatmap_bdiff_france.html")
    m.save(out)
    print("OK ->", out)

if __name__ == "__main__":
    main()