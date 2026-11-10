
import streamlit as st
import pandas as pd

from components.database import (
    get_pothole_detections,
    get_road_reports
)

st.set_page_config(
    page_title="MargDrishti | Dashboard",
    page_icon="🛣️",
    layout="wide"
)

st.title("Welcome to MargDrishti")
st.caption("AI-Powered Road Monitoring and Analysis")
st.divider()

detections = get_pothole_detections()
reports = get_road_reports()

df = pd.DataFrame(detections)
reports_df = pd.DataFrame(reports)

total = len(df)

if not df.empty and "severity" in df.columns:
    severity = df["severity"].astype(str).str.lower()
    high = (severity == "high").sum()
    medium = (severity == "medium").sum()
    low = (severity == "low").sum()
else:
    high = medium = low = 0

areas = (
    df["location"].nunique()
    if not df.empty and "location" in df.columns
    else 0
)

st.subheader("Road Monitoring Overview")

c1, c2, c3, c4, c5 = st.columns(5)

c1.metric("Total Potholes", total)
c2.metric("High Severity", high)
c3.metric("Medium Severity", medium)
c4.metric("Low Severity", low)
c5.metric("Areas Reported", areas)

st.divider()

st.subheader("Detection Insights")

left, right = st.columns(2)

with left:
    st.markdown("#### Most Recent Detection")

    if not df.empty:
        st.dataframe(df.head(1), use_container_width=True)
    else:
        st.info("No pothole detections available yet.")

with right:
    st.markdown("#### Potholes by Location")

    if not df.empty and "location" in df.columns:
        location_counts = df["location"].value_counts()
        st.bar_chart(
            location_counts,
            color="#B9A5D6"
        )
    else:
        st.info("Location data will appear here.")

st.divider()

st.subheader("Recent Road Reports")

if not reports_df.empty:
    st.dataframe(
        reports_df.head(10),
        use_container_width=True,
        hide_index=True
    )
else:
    st.info("No road reports available yet.")
