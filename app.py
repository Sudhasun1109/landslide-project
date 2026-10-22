import streamlit as st
import pandas as pd
import numpy as np
import sqlite3
from datetime import datetime
import folium
from streamlit_folium import st_folium


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Landslide Early Warning",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)


# =========================================================
# CUSTOM CSS
# =========================================================

st.markdown("""
<style>

html, body, [class*="css"] {
    font-family: Arial, sans-serif;
}

.stApp {
    background: #f7f9fc;
    color: #172033;
}

/* Main content */

.block-container {
    padding-top: 2rem;
    padding-bottom: 3rem;
    max-width: 1450px;
}

/* Sidebar */

section[data-testid="stSidebar"] {
    background: #ffffff;
    border-right: 1px solid #e5e7eb;
}

section[data-testid="stSidebar"] * {
    color: #85ab90 !important;
}

/* Headings */

h1, h2, h3, h4 {
    color: #111827 !important;
}

/* Normal text */

p, label {
    color: #172033;
}

/* Selectbox */

div[data-baseweb="select"] > div {
    background: #ffffff !important;
    border: 1px solid #d1d5db !important;
    color: #054de8 !important;
}

/* Slider */

div[data-testid="stSlider"] {
    padding-top: 5px;
}

/* Metrics */

div[data-testid="stMetric"] {
    background: white;
    border: 1px solid #e5e7eb;
    padding: 18px;
    border-radius: 14px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.04);
}

div[data-testid="stMetricLabel"] {
    color: #6b7280 !important;
}

div[data-testid="stMetricValue"] {
    color: #111827 !important;
}

/* Buttons */

.stButton > button {
    border-radius: 10px;
    border: 1px solid #2563eb;
    background: #2563eb;
    color: white !important;
    font-weight: 600;
    padding: 0.6rem 1rem;
}

.stButton > button:hover {
    background: #1d4ed8;
    border-color: #1d4ed8;
}

/* Dataframe */

div[data-testid="stDataFrame"] {
    border-radius: 12px;
}

/* Alerts */

div[data-testid="stAlert"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# HELPER FUNCTIONS
# =========================================================

def html_card(title, value, subtitle=""):
    st.html(f"""
    <div style="
        background:#ffffff;
        border:1px solid #e5e7eb;
        border-radius:16px;
        padding:20px;
        margin-bottom:15px;
        box-shadow:0 5px 18px rgba(0,0,0,0.05);
    ">
        <div style="
            font-size:13px;
            color:#6b7280;
            font-weight:600;
            margin-bottom:8px;
        ">
            {title}
        </div>

        <div style="
            font-size:28px;
            color:#111827;
            font-weight:700;
        ">
            {value}
        </div>

        <div style="
            font-size:13px;
            color:#6b7280;
            margin-top:5px;
        ">
            {subtitle}
        </div>
    </div>
    """)


def risk_color(level):

    if level == "Very High":
        return "#dc2626"

    if level == "High":
        return "#ea580c"

    if level == "Medium":
        return "#ca8a04"

    return "#16a34a"


def rainfall_factor(rainfall):

    if rainfall <= 0:
        return 0

    elif rainfall < 10:
        return 20

    elif rainfall < 25:
        return 40

    elif rainfall < 50:
        return 60

    elif rainfall < 75:
        return 80

    else:
        return 100


def get_risk_level(score):

    if score >= 80:
        return "Very High"

    elif score >= 60:
        return "High"

    elif score >= 25:
        return "Medium"

    else:
        return "Low"


def rainfall_condition(rainfall):

    if rainfall <= 0:
        return "No Rainfall"

    elif rainfall < 10:
        return "Light Rainfall"

    elif rainfall < 25:
        return "Moderate Rainfall"

    elif rainfall < 50:
        return "Heavy Rainfall"

    elif rainfall < 75:
        return "Very Heavy Rainfall"

    else:
        return "Extreme Rainfall"


# =========================================================
# DATABASE
# =========================================================

def init_database():

    conn = sqlite3.connect("alert_log.db")

    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            alert_key TEXT UNIQUE,
            latitude REAL,
            longitude REAL,
            risk_level TEXT,
            risk_score REAL,
            rainfall REAL,
            status TEXT,
            message TEXT,
            created_at TEXT
        )
    """)

    conn.commit()
    conn.close()


def alert_already_processed(alert_key):

    conn = sqlite3.connect("alert_log.db")

    cursor = conn.cursor()

    cursor.execute(
        "SELECT id FROM alerts WHERE alert_key = ?",
        (alert_key,)
    )

    result = cursor.fetchone()

    conn.close()

    return result is not None


def save_alert(
    alert_key,
    latitude,
    longitude,
    risk_level,
    risk_score,
    rainfall,
    status,
    message
):

    conn = sqlite3.connect("alert_log.db")

    cursor = conn.cursor()

    cursor.execute("""
        INSERT OR IGNORE INTO alerts
        (
            alert_key,
            latitude,
            longitude,
            risk_level,
            risk_score,
            rainfall,
            status,
            message,
            created_at
        )
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        alert_key,
        latitude,
        longitude,
        risk_level,
        risk_score,
        rainfall,
        status,
        message,
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ))

    conn.commit()
    conn.close()


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    df = pd.read_csv("dynamic_risk_predictions.csv")

    df["Latitude"] = pd.to_numeric(
        df["Latitude"],
        errors="coerce"
    )

    df["Longitude"] = pd.to_numeric(
        df["Longitude"],
        errors="coerce"
    )

    df["Elevation_m"] = pd.to_numeric(
        df["Elevation_m"],
        errors="coerce"
    )

    df["Slope_deg"] = pd.to_numeric(
        df["Slope_deg"],
        errors="coerce"
    )

    df["Risk_Score"] = pd.to_numeric(
        df["Risk_Score"],
        errors="coerce"
    )

    df = df.dropna(
        subset=[
            "Latitude",
            "Longitude",
            "Elevation_m",
            "Slope_deg",
            "Risk_Score"
        ]
    )

    return df


# =========================================================
# LOAD DATA
# =========================================================

try:

    df = load_data()

except Exception as e:

    st.error(
        "Dataset loading failed. Make sure dynamic_risk_predictions.csv "
        "is inside the project folder."
    )

    st.stop()


init_database()


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.markdown("""
    <div style="
        font-size:24px;
        font-weight:800;
        color:#111827;
        margin-bottom:5px;
    ">
        🌍 Landslide AI
    </div>

    <div style="
        font-size:13px;
        color:#305eba;
        margin-bottom:25px;
    ">
        Early Warning & Monitoring
    </div>
    """, unsafe_allow_html=True)

    st.markdown("### 📍 Select Location")

    location_options = [
        f"{row.Latitude:.6f}, {row.Longitude:.6f}"
        for row in df.itertuples()
    ]

    selected_location = st.selectbox(
        "Location",
        location_options
    )

    latitude, longitude = map(
        float,
        selected_location.split(", ")
    )

    selected_rows = df[
        (df["Latitude"].round(6) == round(latitude, 6))
        &
        (df["Longitude"].round(6) == round(longitude, 6))
    ]

    if selected_rows.empty:

        st.error("Selected location was not found.")

        st.stop()

    selected = selected_rows.iloc[0]

    st.markdown("---")

    st.markdown("### 🌧️ Rainfall Simulation")

    rainfall = st.slider(
        "Rainfall (mm)",
        min_value=0,
        max_value=150,
        value=0,
        step=5
    )

    st.caption(
        "Prototype simulation input. "
        "It is not live rainfall."
    )

    st.markdown("---")

    st.markdown("### 📊 System")

    st.write("**ML Model:** Random Forest")
    st.write("**Features:** Elevation + Slope")
    st.write("**Map:** Folium + OpenStreetMap")
    st.write("**Database:** SQLite")
    st.write("**Alert:** Twilio SMS")


# =========================================================
# CALCULATE DYNAMIC RISK
# =========================================================

ml_risk = float(selected["Risk_Score"])

rain_factor = rainfall_factor(rainfall)

dynamic_score = (
    ml_risk * 0.70
    +
    rain_factor * 0.30
)

dynamic_score = min(
    max(dynamic_score, 0),
    100
)

dynamic_level = get_risk_level(dynamic_score)

color = risk_color(dynamic_level)

condition = rainfall_condition(rainfall)


# =========================================================
# HERO
# =========================================================

st.html(f"""
<div style="
    background:linear-gradient(135deg,#ffffff,#eef5ff);
    border:1px solid #dbe5f1;
    border-radius:22px;
    padding:34px;
    margin-bottom:25px;
    box-shadow:0 8px 30px rgba(0,0,0,0.05);
">

    <div style="
        font-size:13px;
        font-weight:700;
        color:#2563eb;
        letter-spacing:1px;
        margin-bottom:10px;
    ">
        AI / ML BASED DISASTER MANAGEMENT
    </div>

    <div style="
        font-size:38px;
        font-weight:800;
        color:#111827;
        line-height:1.2;
    ">
        Landslide Early Warning
        & Monitoring System
    </div>

    <div style="
        font-size:16px;
        color:#6b7280;
        margin-top:12px;
        max-width:850px;
        line-height:1.6;
    ">
        A geospatial AI decision-support system that combines
        terrain-based ML risk estimation with rainfall conditions
        to generate dynamic landslide risk and automatic warnings.
    </div>

</div>
""")


# =========================================================
# TOP METRICS
# =========================================================

st.markdown("## 📊 Current Risk Overview")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Dynamic Risk",
        f"{dynamic_score:.1f}%"
    )

with c2:
    st.metric(
        "Risk Level",
        dynamic_level
    )

with c3:
    st.metric(
        "Rainfall",
        f"{rainfall} mm"
    )

with c4:
    st.metric(
        "ML Risk",
        f"{ml_risk:.1f}%"
    )


# =========================================================
# LOCATION ANALYSIS
# =========================================================

st.markdown("## 📍 Selected Location")

c1, c2, c3, c4 = st.columns(4)

with c1:
    html_card(
        "LATITUDE",
        f"{latitude:.6f}",
        "Selected coordinate"
    )

with c2:
    html_card(
        "LONGITUDE",
        f"{longitude:.6f}",
        "Selected coordinate"
    )

with c3:
    html_card(
        "ELEVATION",
        f"{selected['Elevation_m']:.0f} m",
        "Terrain elevation"
    )

with c4:
    html_card(
        "SLOPE",
        f"{selected['Slope_deg']:.2f}°",
        "Terrain slope"
    )


# =========================================================
# AI ANALYSIS
# =========================================================

st.markdown("## 🤖 AI Risk Analysis")

st.html(f"""
<div style="
    background:#ffffff;
    border:1px solid #e5e7eb;
    border-left:6px solid {color};
    border-radius:16px;
    padding:24px;
    margin-bottom:20px;
    box-shadow:0 5px 18px rgba(0,0,0,0.05);
">

    <div style="
        font-size:14px;
        color:#6b7280;
        font-weight:600;
    ">
        CURRENT AI ASSESSMENT
    </div>

    <div style="
        font-size:32px;
        font-weight:800;
        color:{color};
        margin-top:5px;
    ">
        {dynamic_level}
    </div>

    <div style="
        font-size:18px;
        font-weight:700;
        color:#111827;
        margin-top:8px;
    ">
        Dynamic Risk Score: {dynamic_score:.1f}%
    </div>

    <div style="
        font-size:14px;
        color:#6b7280;
        margin-top:12px;
        line-height:1.6;
    ">
        ML Risk: {ml_risk:.1f}% |
        Rainfall: {rainfall} mm |
        Rainfall Condition: {condition}
    </div>

</div>
""")


# =========================================================
# RAINFALL IMPACT
# =========================================================

st.markdown("## 🌧️ Rainfall Impact")

col1, col2 = st.columns(2)

with col1:

    st.metric(
        "Rainfall Factor",
        f"{rain_factor:.0f}/100"
    )

with col2:

    st.metric(
        "Dynamic Risk",
        f"{dynamic_score:.1f}%"
    )

st.progress(
    int(dynamic_score)
)


# =========================================================
# AUTOMATIC WARNING ENGINE
# =========================================================

st.markdown("## 🚨 Automatic Warning Engine")


if dynamic_score >= 80:

    alert_type = "CRITICAL"

    st.error(
        f"🚨 VERY HIGH RISK — Automatic critical alert triggered."
    )

elif dynamic_score >= 60:

    alert_type = "WARNING"

    st.warning(
        f"⚠️ HIGH RISK — Automatic warning alert triggered."
    )

else:

    alert_type = None

    st.success(
        "✅ Risk is below the automatic alert threshold."
    )


# =========================================================
# AUTOMATIC SMS
# =========================================================

if alert_type is not None:

    # Bucket rainfall so Streamlit reruns do not repeatedly send SMS
    rainfall_bucket = int(rainfall // 10) * 10

    alert_key = (
        f"{latitude:.6f}_"
        f"{longitude:.6f}_"
        f"{alert_type}_"
        f"{rainfall_bucket}"
    )

    sms_message = f"""
LANDSLIDE ALERT 🚨

AI Landslide Early Warning System

Risk Level: {dynamic_level}
Risk Score: {dynamic_score:.1f}%

Location:
Lat: {latitude:.6f}
Lon: {longitude:.6f}

Rainfall: {rainfall} mm
Condition: {condition}

Elevation: {selected['Elevation_m']:.0f} m
Slope: {selected['Slope_deg']:.2f}°

Action:
Inspect the area and prepare emergency response.

This is an AI-based risk estimation.
    """.strip()

    # Only process once for this risk/rainfall combination

    if not alert_already_processed(alert_key):

        try:

            from send_alert import send_sms

            receiver_number = st.secrets.get(
                "ALERT_RECEIVER_NUMBER",
                ""
            )

            if receiver_number == "":

                raise Exception(
                    "ALERT_RECEIVER_NUMBER is not configured"
                )

            message_sid = send_sms(
                sms_message,
                receiver_number
            )

            save_alert(
                alert_key,
                latitude,
                longitude,
                dynamic_level,
                dynamic_score,
                rainfall,
                "SMS_SENT",
                sms_message
            )

            st.success(
                "📱 Automatic SMS alert sent successfully."
            )

            st.caption(
                f"Message SID: {message_sid}"
            )

        except Exception as e:

            # Demo fallback
            save_alert(
                alert_key,
                latitude,
                longitude,
                dynamic_level,
                dynamic_score,
                rainfall,
                "DEMO_ALERT",
                sms_message
            )

            st.info(
                "📱 Automatic alert generated successfully."
            )

            st.warning(
                "Twilio delivery is currently unavailable. "
                "The system has generated the alert in demo mode."
            )

    else:

        st.info(
            "📱 Alert already processed for this "
            "location/risk/rainfall condition."
        )

    st.markdown("### 📩 Alert Message Preview")

    st.code(
        sms_message,
        language="text"
    )


# =========================================================
# MAP
# =========================================================

st.markdown("## 🗺️ Interactive Landslide Risk Map")

map_center = [
    latitude,
    longitude
]

m = folium.Map(
    location=map_center,
    zoom_start=8,
    tiles="OpenStreetMap"
)


# Add risk points

for _, row in df.iterrows():

    score = float(row["Risk_Score"])

    level = get_risk_level(score)

    marker_color = risk_color(level)

    folium.CircleMarker(
        location=[
            row["Latitude"],
            row["Longitude"]
        ],
        radius=4,
        color=marker_color,
        fill=True,
        fill_color=marker_color,
        fill_opacity=0.75,
        popup=folium.Popup(
            f"""
            <b>Risk Level:</b> {level}<br>
            <b>Risk Score:</b> {score:.1f}%<br>
            <b>Elevation:</b> {row['Elevation_m']:.0f} m<br>
            <b>Slope:</b> {row['Slope_deg']:.2f}°
            """,
            max_width=300
        )
    ).add_to(m)


# Selected location marker

folium.Marker(
    location=[
        latitude,
        longitude
    ],
    popup=folium.Popup(
        f"""
        <b>Selected Location</b><br>
        Risk: {dynamic_level}<br>
        Dynamic Score: {dynamic_score:.1f}%<br>
        Rainfall: {rainfall} mm
        """,
        max_width=300
    ),
    tooltip="Selected Location",
    icon=folium.Icon(
        color="blue",
        icon="info-sign"
    )
).add_to(m)


st_folium(
    m,
    width=None,
    height=650,
    returned_objects=[]
)


# =========================================================
# MAP LEGEND
# =========================================================

st.markdown("### Risk Legend")

l1, l2, l3, l4 = st.columns(4)

with l1:
    st.success("🟢 LOW — 0–24")

with l2:
    st.warning("🟡 MEDIUM — 25–59")

with l3:
    st.warning("🟠 HIGH — 60–79")

with l4:
    st.error("🔴 VERY HIGH — 80–100")


# =========================================================
# DATASET INTELLIGENCE
# =========================================================

st.markdown("## 🧠 Dataset Intelligence")

c1, c2, c3, c4 = st.columns(4)

with c1:
    st.metric(
        "Total Records",
        f"{len(df):,}"
    )

with c2:
    st.metric(
        "Positive Samples",
        f"{int((df['Label'] == 1).sum()):,}"
    )

with c3:
    st.metric(
        "Negative Samples",
        f"{int((df['Label'] == 0).sum()):,}"
    )

with c4:
    st.metric(
        "ML Model",
        "Random Forest"
    )


# =========================================================
# RISK DISTRIBUTION
# =========================================================

st.markdown("## 📈 Risk Distribution")

risk_distribution = (
    df["Risk_Level"]
    .value_counts()
    .reindex(
        ["Low", "Medium", "High", "Very High"],
        fill_value=0
    )
)

st.bar_chart(risk_distribution)


# =========================================================
# SELECTED LOCATION DATA
# =========================================================

st.markdown("## 🔎 Selected ML Data")

display_columns = [
    "Latitude",
    "Longitude",
    "Elevation_m",
    "Slope_deg",
    "Risk_Score",
    "Risk_Level"
]

available_columns = [
    col for col in display_columns
    if col in df.columns
]

st.dataframe(
    selected[available_columns].to_frame().T,
    use_container_width=True,
    hide_index=True
)


# =========================================================
# SYSTEM PIPELINE
# =========================================================

st.markdown("## ⚙️ AI System Pipeline")

pipeline = [
    ("01", "Data Collection", "GSI + Terrain Data"),
    ("02", "Feature Engineering", "Elevation + Slope"),
    ("03", "Machine Learning", "Random Forest"),
    ("04", "Risk Estimation", "ML Risk Score"),
    ("05", "Dynamic Analysis", "Rainfall + ML Risk"),
    ("06", "Visualization", "Streamlit + Folium"),
    ("07", "Alert Engine", "Automatic Warning"),
    ("08", "Notification", "Twilio SMS")
]

cols = st.columns(4)

for index, item in enumerate(pipeline):

    number, title, description = item

    with cols[index % 4]:

        st.html(f"""
        <div style="
            background:#ffffff;
            border:1px solid #e5e7eb;
            border-radius:14px;
            padding:18px;
            margin-bottom:18px;
            min-height:130px;
            box-shadow:0 4px 15px rgba(0,0,0,0.04);
        ">

            <div style="
                font-size:12px;
                font-weight:800;
                color:#2563eb;
            ">
                {number}
            </div>

            <div style="
                font-size:17px;
                font-weight:700;
                color:#111827;
                margin-top:6px;
            ">
                {title}
            </div>

            <div style="
                font-size:13px;
                color:#6b7280;
                margin-top:6px;
            ">
                {description}
            </div>

        </div>
        """)


# =========================================================
# FOOTER
# =========================================================

st.markdown("---")

st.html("""
<div style="
    text-align:center;
    padding:20px;
    color:#6b7280;
">

    <div style="
        font-size:15px;
        font-weight:700;
        color:#111827;
    ">
        AI/ML-Based Landslide Early Warning & Monitoring System
    </div>

    <div style="
        font-size:13px;
        margin-top:6px;
    ">
        Decision-support prototype for disaster risk management
    </div>

</div>
""")