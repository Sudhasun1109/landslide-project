import pandas as pd
import folium
from folium.plugins import MarkerCluster


# =========================
# 1. Load predictions
# =========================

INPUT_FILE = "landslide_risk_predictions.csv"

df = pd.read_csv(INPUT_FILE)

print("Prediction data loaded!")
print("Records:", len(df))


# =========================
# 2. Meghalaya map center
# =========================

center_lat = df["Latitude"].mean()
center_lon = df["Longitude"].mean()

m = folium.Map(
    location=[center_lat, center_lon],
    zoom_start=8,
    tiles="OpenStreetMap"
)


# =========================
# 3. Risk colors
# =========================

risk_colors = {
    "Low": "green",
    "Medium": "yellow",
    "High": "orange",
    "Very High": "red"
}


# =========================
# 4. Marker cluster
# =========================

cluster = MarkerCluster().add_to(m)


# =========================
# 5. Add points
# =========================

for _, row in df.iterrows():

    risk = row["Risk_Level"]
    color = risk_colors.get(risk, "blue")

    popup_text = f"""
    <b>Landslide Risk Assessment</b><br><br>

    <b>Latitude:</b> {row['Latitude']:.6f}<br>
    <b>Longitude:</b> {row['Longitude']:.6f}<br>

    <b>Elevation:</b> {row['Elevation_m']:.1f} m<br>
    <b>Slope:</b> {row['Slope_deg']:.2f}°<br>

    <b>Risk Score:</b> {row['Risk_Score']:.1f}%<br>
    <b>Risk Level:</b> {risk}
    """

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=5,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.7,
        popup=folium.Popup(
            popup_text,
            max_width=300
        )
    ).add_to(cluster)


# =========================
# 6. Add legend
# =========================

legend = """
<div style="
position: fixed;
bottom: 30px;
left: 30px;
width: 180px;
background-color: white;
border:2px solid grey;
z-index:9999;
padding:10px;
font-size:14px;
">

<b>Landslide Risk</b><br><br>

<span style="color:green;">●</span> Low<br>
<span style="color:#d4aa00;">●</span> Medium<br>
<span style="color:orange;">●</span> High<br>
<span style="color:red;">●</span> Very High

</div>
"""

m.get_root().html.add_child(
    folium.Element(legend)
)


# =========================
# 7. Save map
# =========================

OUTPUT_FILE = "risk_map.html"

m.save(OUTPUT_FILE)

print("\nSUCCESS!")
print("Risk map saved as:", OUTPUT_FILE)