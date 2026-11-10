
import streamlit as st
import pandas as pd
import pydeck as pdk

from components.database import (
    get_pothole_detections,
    get_road_reports
)

st.set_page_config(
    page_title="MargDrishti | Dashboard",
    page_icon="🛣️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp {
        background: #F4F7F8;
    }

    [data-testid="stSidebar"] {
        background: #FFFFFF;
        border-right: 1px solid #E5EAEC;
    }

    .block-container {
        padding-top: 1.8rem;
        padding-bottom: 3rem;
        max-width: 1600px;
    }

    h1, h2, h3 {
        color: #203746;
    }

    p, label, .stCaption {
        color: #71818B;
    }

    [data-testid="stMetric"] {
        background: #FFFFFF;
        border: 1px solid #E5EAEC;
        border-radius: 15px;
        padding: 20px;
        box-shadow: 0 3px 12px rgba(32,55,70,0.04);
    }

    [data-testid="stMetricLabel"] {
        color: #71818B;
        font-size: 13px;
    }

    [data-testid="stMetricValue"] {
        color: #203746;
        font-weight: 700;
    }

    [data-testid="stMetricDelta"] {
        color: #168C80;
    }

    div.stButton > button[kind="primary"] {
        background: #168C80;
        color: white;
        border: none;
        border-radius: 9px;
    }

    div.stButton > button[kind="primary"]:hover {
        background: #11766D;
        color: white;
    }

    [data-testid="stDataFrame"] {
        border: 1px solid #E5EAEC;
        border-radius: 12px;
    }

    .section-label {
        color: #168C80;
        font-size: 12px;
        font-weight: 700;
        letter-spacing: 1.2px;
    }

    .hero {
        background: linear-gradient(110deg, #FFFFFF, #EAF5F3);
        border: 1px solid #DFEBE9;
        padding: 28px 30px;
        border-radius: 18px;
        margin-bottom: 24px;
    }

    .hero-title {
        font-size: 30px;
        font-weight: 750;
        color: #203746;
        margin: 5px 0;
    }

    .hero-subtitle {
        color: #71818B;
        font-size: 15px;
        margin-bottom: 0;
    }

    .panel {
        background: #FFFFFF;
        border: 1px solid #E5EAEC;
        border-radius: 15px;
        padding: 18px;
    }

    hr {
        border-color: #E5EAEC;
    }
</style>
""", unsafe_allow_html=True)


# Fetch Supabase data

try:
    detections = get_pothole_detections() or []
    reports = get_road_reports() or []

    df = pd.DataFrame(detections)
    reports_df = pd.DataFrame(reports)

except Exception as e:
    st.error(f"Unable to load dashboard data: {e}")
    st.stop()


# Prepare detection data

if not df.empty:
    if "severity" not in df.columns:
        df["severity"] = "Unknown"

    if "location" not in df.columns:
        df["location"] = "Not available"

    if "latitude" not in df.columns:
        df["latitude"] = None

    if "longitude" not in df.columns:
        df["longitude"] = None

    if "status" not in df.columns:
        df["status"] = "Pending"

    if "confidence" not in df.columns:
        df["confidence"] = None

    if "detected_at" not in df.columns:
        df["detected_at"] = None

    if "image_url" not in df.columns:
        df["image_url"] = None

    df["latitude"] = pd.to_numeric(df["latitude"], errors="coerce")
    df["longitude"] = pd.to_numeric(df["longitude"], errors="coerce")

    mapped_df = df[
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    ].copy()

else:
    mapped_df = pd.DataFrame()


# Calculate dashboard metrics

total = len(df)

severity = (
    df["severity"].fillna("").astype(str).str.lower()
    if not df.empty else pd.Series(dtype=str)
)

high = (severity == "high").sum()
medium = (severity == "medium").sum()
low = (severity == "low").sum()

mapped = len(mapped_df)

if not reports_df.empty and "status" in reports_df.columns:
    pending_reports = (
        reports_df["status"]
        .fillna("")
        .astype(str)
        .str.lower()
        .isin(["pending", "open"])
        .sum()
    )
else:
    pending_reports = 0


# Header

st.markdown("""
<div class="hero">
    <div class="section-label">SMART ROAD INFRASTRUCTURE</div>
    <div class="hero-title">MargDrishti Dashboard</div>
    <p class="hero-subtitle">
        AI-powered pothole detection and smart road monitoring overview.
    </p>
</div>
""", unsafe_allow_html=True)


# Refresh button

header_left, header_right = st.columns([5, 1])

with header_left:
    st.markdown("### Road Monitoring Overview")
    st.caption("Monitor road conditions, pothole detections and reports.")

with header_right:
    if st.button("↻ Refresh Data", type="primary", use_container_width=True):
        st.rerun()


# KPI cards

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Detections", total)
c2.metric("High Severity", high)
c3.metric("GPS Mapped", mapped)
c4.metric("Pending Reports", pending_reports)

st.write("")


# Main map section

st.markdown("### Geographic Monitoring")
st.caption("Explore pothole detections across mapped road locations.")

map_col, insight_col = st.columns([2.3, 1])

with map_col:

    if not mapped_df.empty:

        map_data = mapped_df.copy()

        map_data["severity_label"] = (
            map_data["severity"].fillna("Unknown").astype(str)
        )

        color_map = {
            "low": [34, 160, 110],
            "medium": [235, 176, 65],
            "high": [224, 91, 76],
            "critical": [145, 45, 55]
        }

        map_data["marker_color"] = map_data["severity_label"].str.lower().map(
            color_map
        ).apply(
            lambda x: x if isinstance(x, list) else [100, 130, 140]
        )

        center_lat = map_data["latitude"].mean()
        center_lon = map_data["longitude"].mean()

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=map_data,
            get_position="[longitude, latitude]",
            get_fill_color="marker_color",
            get_radius=85,
            radius_min_pixels=6,
            radius_max_pixels=16,
            pickable=True,
            auto_highlight=True
        )

        view_state = pdk.ViewState(
            latitude=center_lat,
            longitude=center_lon,
            zoom=12,
            pitch=35
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            map_style="https://basemaps.cartocdn.com/gl/positron-gl-style/style.json",
            tooltip={
                "html": """
                <b>Location:</b> {location}<br/>
                <b>Severity:</b> {severity_label}<br/>
                <b>Status:</b> {status}<br/>
                <b>Confidence:</b> {confidence}
                """,
                "style": {
                    "backgroundColor": "#203746",
                    "color": "white"
                }
            }
        )

        st.pydeck_chart(deck, use_container_width=True)

        st.caption(
            f"Displaying {mapped} detections with valid GPS coordinates."
        )

        st.markdown("""
        🟢 Low &nbsp;&nbsp; 🟡 Medium &nbsp;&nbsp;
        🔴 High &nbsp;&nbsp; 🟥 Critical
        """)

    else:
        st.info(
            "No detections with valid GPS coordinates are available yet."
        )


with insight_col:

    st.markdown("""
    <div class="panel">
        <div class="section-label">DETECTION SUMMARY</div>
        <h3>Severity Overview</h3>
    </div>
    """, unsafe_allow_html=True)

    severity_data = pd.DataFrame({
        "Severity": ["High", "Medium", "Low"],
        "Detections": [high, medium, low]
    })

    st.bar_chart(
        severity_data.set_index("Severity"),
        color="#168C80",
        height=210
    )

    st.markdown("""
    <div class="panel">
        <div class="section-label">GPS COVERAGE</div>
    </div>
    """, unsafe_allow_html=True)

    if total > 0:
        coverage = mapped / total
    else:
        coverage = 0

    st.metric("Mapped Coverage", f"{coverage * 100:.1f}%")
    st.progress(coverage)


st.write("")


# Recent detection

st.markdown("### Latest Detection")
st.caption("Review the most recent pothole detection.")

if not df.empty:

    latest = df.iloc[0]

    image_url = latest.get("image_url")

    image_col, details_col = st.columns([1.2, 1])

    with image_col:

        if pd.notna(image_url) and str(image_url).strip():
            st.image(
                str(image_url).strip(),
                use_container_width=True
            )
        else:
            st.info("No detection image available.")

    with details_col:

        st.markdown("#### Detection Details")

        st.write("**Detection ID:**", latest.get("id", "N/A"))
        st.write("**Severity:**", latest.get("severity", "Unknown"))
        st.write("**Location:**", latest.get("location", "Not available"))
        st.write("**Status:**", latest.get("status", "Not available"))

        confidence = pd.to_numeric(
            pd.Series([latest.get("confidence")]),
            errors="coerce"
        ).iloc[0]

        if pd.notna(confidence):
            if confidence <= 1:
                confidence *= 100

            st.write(f"**Confidence:** {confidence:.1f}%")
        else:
            st.write("**Confidence:** Not available")

        st.write("**Detected At:**", latest.get("detected_at", "N/A"))
        st.write("**Source:**", latest.get("source", "N/A"))

else:
    st.info("No pothole detections available yet.")


st.write("")


# Recent road reports

st.markdown("### Recent Road Reports")
st.caption("Latest road damage reports submitted to MargDrishti.")

if not reports_df.empty:
    st.dataframe(
        reports_df.head(10),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No road reports available yet.")


# Missing GPS records

st.markdown("### GPS Data Quality")

missing_gps = total - mapped

g1, g2 = st.columns(2)

g1.metric("Mapped Records", mapped)
g2.metric("Missing GPS Records", missing_gps)

if missing_gps > 0:
    st.warning(
        f"{missing_gps} records do not have valid GPS coordinates. "
        "They are excluded from the map."
    )
