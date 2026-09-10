import streamlit as st
import pandas as pd
import folium

from streamlit_folium import st_folium
from send_alert import send_sms


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="AI Landslide Early Warning System",
    page_icon="🌋",
    layout="wide"
)


# =========================================================
# TITLE
# =========================================================

st.title("🌋 AI-Powered Landslide Early Warning & Monitoring System")

st.markdown(
    """
    **AI + Terrain + Rainfall Based Risk Monitoring Dashboard**

    This prototype estimates landslide risk using terrain features
    and simulated rainfall conditions.
    """
)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    return pd.read_csv(
        "dynamic_risk_predictions.csv"
    )


try:

    df = load_data()

except FileNotFoundError:

    st.error(
        "❌ dynamic_risk_predictions.csv not found."
    )

    st.stop()


# =========================================================
# CHECK COLUMNS
# =========================================================

required_columns = [
    "Latitude",
    "Longitude",
    "Elevation_m",
    "Slope_deg",
    "Risk_Score",
    "Rainfall_mm",
    "Dynamic_Risk_Score"
]


missing_columns = [
    col
    for col in required_columns
    if col not in df.columns
]


if missing_columns:

    st.error(
        f"❌ Missing columns: {missing_columns}"
    )

    st.write(
        "Available columns:"
    )

    st.write(
        df.columns.tolist()
    )

    st.stop()


# =========================================================
# RISK LEVEL
# =========================================================

def get_risk_level(score):

    if score >= 80:
        return "Very High"

    elif score >= 60:
        return "High"

    elif score >= 40:
        return "Medium"

    else:
        return "Low"


# =========================================================
# RAINFALL FACTOR
# =========================================================

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


# =========================================================
# SIDEBAR
# =========================================================

st.sidebar.header(
    "⚙️ Risk Simulation"
)


st.sidebar.info(
    """
    Simulate rainfall conditions and
    observe the change in landslide risk.
    """
)


# =========================================================
# LOCATION SELECTION
# =========================================================

location_labels = []


for index, row in df.iterrows():

    label = (
        f"{index} | "
        f"{row['Latitude']:.5f}, "
        f"{row['Longitude']:.5f}"
    )

    location_labels.append(
        label
    )


selected_location = st.sidebar.selectbox(
    "📍 Select Monitoring Location",
    location_labels
)


selected_index = int(
    selected_location.split("|")[0].strip()
)


selected_row = df.iloc[
    selected_index
]


# =========================================================
# LOCATION DATA
# =========================================================

latitude = float(
    selected_row["Latitude"]
)


longitude = float(
    selected_row["Longitude"]
)


elevation = float(
    selected_row["Elevation_m"]
)


slope = float(
    selected_row["Slope_deg"]
)


# IMPORTANT:
# Your CSV column is Risk_Score

base_risk = float(
    selected_row["Risk_Score"]
)


# =========================================================
# RAINFALL SIMULATION
# =========================================================

st.sidebar.subheader(
    "🌧️ Rainfall Simulation"
)


rainfall = st.sidebar.slider(
    "Simulated Rainfall (mm)",
    min_value=0.0,
    max_value=100.0,
    value=10.0,
    step=1.0
)


# =========================================================
# CALCULATE RAINFALL FACTOR
# =========================================================

rain_factor = rainfall_factor(
    rainfall
)


# =========================================================
# DYNAMIC RISK
# =========================================================

dynamic_risk = (
    base_risk * 0.70
    +
    rain_factor * 0.30
)


dynamic_risk = max(
    0,
    min(
        100,
        dynamic_risk
    )
)


# =========================================================
# RISK LEVEL
# =========================================================

risk_level = get_risk_level(
    dynamic_risk
)


# =========================================================
# RAINFALL CONDITION
# =========================================================

if rainfall == 0:

    rainfall_condition = "No Rainfall"

elif rainfall < 10:

    rainfall_condition = "Light Rainfall"

elif rainfall < 25:

    rainfall_condition = "Moderate Rainfall"

elif rainfall < 50:

    rainfall_condition = "Heavy Rainfall"

elif rainfall < 75:

    rainfall_condition = "Very Heavy Rainfall"

else:

    rainfall_condition = "Extreme Rainfall"


# =========================================================
# WARNING MESSAGE
# =========================================================

if risk_level == "Very High":

    warning_message = (
        "🚨 VERY HIGH RISK — Immediate precaution recommended."
    )

    recommended_action = (
        "Evacuate vulnerable areas if advised by authorities "
        "and continuously monitor the location."
    )


elif risk_level == "High":

    warning_message = (
        "⚠️ HIGH RISK — Close monitoring required."
    )

    recommended_action = (
        "Inspect the area and prepare emergency response."
    )


elif risk_level == "Medium":

    warning_message = (
        "🟡 MEDIUM RISK — Continue monitoring."
    )

    recommended_action = (
        "Monitor rainfall and terrain conditions."
    )


else:

    warning_message = (
        "🟢 LOW RISK — Normal monitoring."
    )

    recommended_action = (
        "No immediate action required."
    )


# =========================================================
# DASHBOARD METRICS
# =========================================================

st.subheader(
    "📊 Current Risk Status"
)


col1, col2, col3, col4 = st.columns(
    4
)


with col1:

    st.metric(
        "Risk Score",
        f"{dynamic_risk:.1f}%"
    )


with col2:

    st.metric(
        "Risk Level",
        risk_level
    )


with col3:

    st.metric(
        "Rainfall",
        f"{rainfall:.1f} mm"
    )


with col4:

    st.metric(
        "Slope",
        f"{slope:.1f}°"
    )


# =========================================================
# WARNING STATUS
# =========================================================

st.subheader(
    "🚨 Warning Status"
)


if risk_level == "Very High":

    st.error(
        warning_message
    )


elif risk_level == "High":

    st.warning(
        warning_message
    )


elif risk_level == "Medium":

    st.warning(
        warning_message
    )


else:

    st.success(
        warning_message
    )


st.info(
    f"Recommended Action: {recommended_action}"
)


# =========================================================
# LOCATION DETAILS
# =========================================================

st.subheader(
    "📍 Selected Location"
)


c1, c2, c3 = st.columns(
    3
)


with c1:

    st.metric(
        "Latitude",
        f"{latitude:.6f}"
    )

    st.metric(
        "Elevation",
        f"{elevation:.1f} m"
    )


with c2:

    st.metric(
        "Longitude",
        f"{longitude:.6f}"
    )

    st.metric(
        "Slope",
        f"{slope:.2f}°"
    )


with c3:

    st.metric(
        "Base ML Risk",
        f"{base_risk:.1f}%"
    )

    st.metric(
        "Rainfall Condition",
        rainfall_condition
    )


# =========================================================
# RISK CHANGE
# =========================================================

risk_change = (
    dynamic_risk - base_risk
)


st.subheader(
    "📈 Risk Change"
)


if risk_change > 0:

    st.warning(
        f"⬆️ Risk increased by "
        f"{risk_change:.1f}% due to rainfall."
    )


elif risk_change < 0:

    st.success(
        f"⬇️ Risk decreased by "
        f"{abs(risk_change):.1f}%."
    )


else:

    st.info(
        "➡️ No change in risk."
    )


# =========================================================
# SMS ALERT
# =========================================================

st.subheader(
    "📱 Emergency SMS Alert"
)


receiver_number = st.text_input(
    "Emergency Contact Number",
    placeholder="+91XXXXXXXXXX"
)


if risk_level in [
    "High",
    "Very High"
]:

    st.warning(
        "⚠️ High-risk condition detected. "
        "Emergency SMS can be sent."
    )


else:

    st.info(
        "SMS alert becomes available when "
        "risk reaches High or Very High."
    )


# =========================================================
# SMS MESSAGE
# =========================================================

sms_message = f"""
LANDSLIDE WARNING 🚨

Location:
{latitude:.6f}, {longitude:.6f}

Risk Level:
{risk_level}

Risk Score:
{dynamic_risk:.1f}%

Rainfall:
{rainfall:.1f} mm

Elevation:
{elevation:.1f} m

Slope:
{slope:.2f} degrees

Rainfall Condition:
{rainfall_condition}

Recommended Action:
{recommended_action}

AI Landslide Early Warning System
"""


# =========================================================
# SEND SMS BUTTON
# =========================================================

if st.button(
    "🚨 Send SMS Alert",
    use_container_width=True
):

    if risk_level not in [
        "High",
        "Very High"
    ]:

        st.info(
            "SMS alert is available only for "
            "High or Very High risk."
        )


    elif not receiver_number:

        st.error(
            "❌ Please enter an emergency contact number."
        )


    else:

        # =================================================
        # REAL TWILIO SMS
        # =================================================

        try:

            message_sid = send_sms(
                sms_message,
                receiver_number
            )


            st.success(
                "✅ REAL SMS sent successfully!"
            )


            st.write(
                "Twilio Message SID:"
            )


            st.code(
                message_sid
            )


        # =================================================
        # DEMO FALLBACK
        # =================================================

        except Exception as e:

            st.warning(
                "⚠️ Real SMS could not be sent."
            )


            st.info(
                "🧪 Switching to DEMO SMS mode "
                "for hackathon demonstration."
            )


            st.success(
                "✅ DEMO SMS ALERT GENERATED!"
            )


            st.markdown(
                "### 📱 SMS Preview"
            )


            st.code(
                sms_message
            )


            st.caption(
                "Demo mode: No actual SMS was sent."
            )


            with st.expander(
                "Show Twilio error"
            ):

                st.code(
                    str(e)
                )


# =========================================================
# RISK MAP
# =========================================================

st.subheader(
    "🗺️ Landslide Risk Map"
)


m = folium.Map(
    location=[
        latitude,
        longitude
    ],
    zoom_start=8,
    tiles="OpenStreetMap"
)


# =========================================================
# ADD ALL RISK POINTS
# =========================================================

for _, row in df.iterrows():

    point_lat = float(
        row["Latitude"]
    )


    point_lon = float(
        row["Longitude"]
    )


    point_risk = float(
        row["Dynamic_Risk_Score"]
    )


    point_level = get_risk_level(
        point_risk
    )


    # Risk colour

    if point_level == "Very High":

        color = "red"

    elif point_level == "High":

        color = "orange"

    elif point_level == "Medium":

        color = "yellow"

    else:

        color = "green"


    popup_text = f"""
    <b>Risk Level:</b> {point_level}<br>
    <b>Risk Score:</b> {point_risk:.1f}%<br>
    <b>Latitude:</b> {point_lat:.6f}<br>
    <b>Longitude:</b> {point_lon:.6f}<br>
    <b>Elevation:</b> {float(row['Elevation_m']):.1f} m<br>
    <b>Slope:</b> {float(row['Slope_deg']):.2f}°
    """


    folium.CircleMarker(
        location=[
            point_lat,
            point_lon
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
    ).add_to(m)


# =========================================================
# SELECTED LOCATION MARKER
# =========================================================

folium.Marker(
    location=[
        latitude,
        longitude
    ],
    popup=folium.Popup(
        f"""
        <b>Selected Monitoring Location</b><br><br>

        Risk: {dynamic_risk:.1f}%<br>

        Level: {risk_level}<br>

        Rainfall: {rainfall:.1f} mm<br>

        Elevation: {elevation:.1f} m<br>

        Slope: {slope:.2f}°
        """,
        max_width=300
    ),
    tooltip="Selected Location"
).add_to(m)


# =========================================================
# DISPLAY MAP
# =========================================================

st_folium(
    m,
    width=None,
    height=650
)


# =========================================================
# RISK DISTRIBUTION
# =========================================================

st.subheader(
    "📊 Risk Distribution"
)


risk_distribution = (
    df["Dynamic_Risk_Score"]
    .apply(get_risk_level)
    .value_counts()
)


st.bar_chart(
    risk_distribution
)


# =========================================================
# MONITORING TABLE
# =========================================================

st.subheader(
    "📋 Monitoring Data"
)


display_df = df.copy()


display_df["Risk_Level"] = (
    display_df[
        "Dynamic_Risk_Score"
    ]
    .apply(get_risk_level)
)


st.dataframe(
    display_df[
        [
            "Latitude",
            "Longitude",
            "Elevation_m",
            "Slope_deg",
            "Risk_Score",
            "Rainfall_mm",
            "Dynamic_Risk_Score",
            "Risk_Level"
        ]
    ],
    use_container_width=True
)


# =========================================================
# SYSTEM WORKFLOW
# =========================================================

st.divider()


st.subheader(
    "🔄 System Workflow"
)


st.markdown(
    """
    **Terrain Data**
    
    ↓
    
    **Elevation + Slope**
    
    ↓
    
    **Random Forest ML Model**
    
    ↓
    
    **Base Risk Score**
    
    ↓
    
    **Rainfall Simulation**
    
    ↓
    
    **Dynamic Risk Score**
    
    ↓
    
    **Warning Level**
    
    ↓
    
    **Real SMS / Demo SMS Alert**
    """
)


# =========================================================
# FOOTER
# =========================================================

st.divider()


st.caption(
    "🌋 AI-Powered Landslide Early Warning & Monitoring System | "
    "Hackathon Prototype"
)