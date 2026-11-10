
import streamlit as st
import pandas as pd
import plotly.express as px
from components.supabase_client import supabase

st.set_page_config(
    page_title="MargDrishti | Analytics",
    page_icon="📊",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #FAF7F2;
}
h1, h2, h3 {
    color: #594638;
}
.metric-card {
    background-color: #F1E8DE;
    padding: 20px;
    border-radius: 14px;
    border: 1px solid #E5D6C7;
}
</style>
""", unsafe_allow_html=True)

st.title("📊 MargDrishti Analytics")
st.caption("SMART ROAD INFRASTRUCTURE | Pothole Detection Insights")

if st.button("🔄 Refresh Analytics"):
    st.rerun()

@st.cache_data(ttl=30)
def load_data():
    response = (
        supabase.table("pothole_detections")
        .select("*")
        .order("detected_at", desc=True)
        .execute()
    )
    return pd.DataFrame(response.data)

try:
    df = load_data()

    if df.empty:
        st.info("No pothole detection records are available yet.")
        st.stop()

    df["severity"] = df["severity"].fillna("Unknown").astype(str).str.title()
    df["status"] = df["status"].fillna("Pending").astype(str).str.title()
    df["location"] = df["location"].fillna("Unknown").astype(str)

    df["detected_at"] = pd.to_datetime(
        df["detected_at"], errors="coerce", utc=True
    )

    df["confidence"] = pd.to_numeric(
        df["confidence"], errors="coerce"
    )

    st.markdown("## Detection Overview")

    total = len(df)
    high = (df["severity"] == "High").sum()
    medium = (df["severity"] == "Medium").sum()
    low = (df["severity"] == "Low").sum()

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Total Detections", total)
    c2.metric("High Severity", int(high))
    c3.metric("Medium Severity", int(medium))
    c4.metric("Low Severity", int(low))

    st.divider()

    st.markdown("## Severity Distribution")

    left, right = st.columns(2)

    severity_counts = (
        df["severity"]
        .value_counts()
        .rename_axis("Severity")
        .reset_index(name="Count")
    )

    with left:
        fig = px.pie(
            severity_counts,
            names="Severity",
            values="Count",
            hole=0.45,
            title="Potholes by Severity",
            color="Severity",
            color_discrete_map={
                "Low": "#8DAA91",
                "Medium": "#E8C47C",
                "High": "#D98272",
                "Critical": "#9B4D4D",
                "Unknown": "#B8ADA2"
            }
        )
        st.plotly_chart(fig, use_container_width=True)

    with right:
        status_counts = (
            df["status"]
            .value_counts()
            .rename_axis("Status")
            .reset_index(name="Count")
        )

        fig = px.bar(
            status_counts,
            x="Status",
            y="Count",
            title="Detection Status",
            color="Status",
            color_discrete_sequence=["#B99A83"]
        )
        st.plotly_chart(fig, use_container_width=True)

    st.divider()

    st.markdown("## Detection Trends")

    trend_df = df.dropna(subset=["detected_at"]).copy()

    if not trend_df.empty:
        trend_df["Date"] = (
            trend_df["detected_at"].dt.strftime("%Y-%m-%d")
        )

        daily = (
            trend_df.groupby("Date")
            .size()
            .reset_index(name="Detections")
            .sort_values("Date")
        )

        fig = px.line(
            daily,
            x="Date",
            y="Detections",
            markers=True,
            title="Daily Pothole Detection Trend"
        )
        fig.update_traces(line_color="#B58B70")
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No valid detection timestamps are available.")

    st.divider()

    st.markdown("## Location Analysis")

    location_df = df[
        (df["location"] != "Unknown") &
        (df["location"].str.strip() != "")
    ]

    if not location_df.empty:
        location_counts = (
            location_df["location"]
            .value_counts()
            .head(10)
            .reset_index()
        )
        location_counts.columns = ["Location", "Detections"]

        fig = px.bar(
            location_counts,
            x="Detections",
            y="Location",
            orientation="h",
            title="Top 10 Locations by Detections",
            color_discrete_sequence=["#A9B7A0"]
        )
        fig.update_layout(yaxis={"categoryorder": "total ascending"})
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No location information is available.")

    st.divider()

    st.markdown("## Detection Records")

    display_columns = [
        col for col in [
            "id", "detected_at", "location",
            "severity", "confidence", "status", "source"
        ] if col in df.columns
    ]

    st.dataframe(
        df[display_columns],
        use_container_width=True,
        hide_index=True
    )

    st.download_button(
        "⬇️ Download Analytics Data",
        data=df.to_csv(index=False).encode("utf-8"),
        file_name="margdrishti_analytics.csv",
        mime="text/csv"
    )

except Exception as e:
    st.error("Unable to load analytics from Supabase.")
    st.code(str(e))
    st.info("Check your Supabase connection and table configuration.")

