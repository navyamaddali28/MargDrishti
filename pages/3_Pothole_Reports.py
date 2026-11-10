
import streamlit as st
import pandas as pd
from components.supabase_client import supabase

st.set_page_config(
    page_title="MargDrishti | Pothole Reports",
    page_icon="🛣️",
    layout="wide"
)

st.markdown("""
<style>
.stApp {
    background-color: #F8F5EF;
}

h1, h2, h3 {
    color: #665747;
}

.report-card {
    background: #EFE9DF;
    padding: 18px;
    border-radius: 12px;
    margin-bottom: 12px;
}

div[data-testid="stMetric"] {
    background: #F0EBE2;
    border: 1px solid #E5DDD0;
    padding: 15px;
    border-radius: 12px;
}

div[data-testid="stMetricValue"] {
    color: #665747;
}

.stButton button {
    border-radius: 8px;
}
</style>
""", unsafe_allow_html=True)

st.title("🛣️ Pothole Reports")
st.write("Monitor, search and review pothole detections recorded in MargDrishti.")

st.divider()

if st.button("🔄 Refresh Reports"):
    st.rerun()

try:
    response = (
        supabase
        .table("pothole_detections")
        .select("*")
        .order("detected_at", desc=True)
        .execute()
    )

    reports = response.data or []

    if not reports:
        st.info("No pothole reports available yet.")
        st.stop()

    df = pd.DataFrame(reports)

    required_columns = [
        "id", "detected_at", "location", "severity",
        "confidence", "status", "source", "image_url",
        "latitude", "longitude"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df["severity_display"] = (
        df["severity"]
        .fillna("Unclassified")
        .astype(str)
        .str.strip()
        .replace("", "Unclassified")
    )

    df["status_display"] = (
        df["status"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    df["source_display"] = (
        df["source"]
        .fillna("Unknown")
        .astype(str)
        .str.strip()
        .replace("", "Unknown")
    )

    total = len(df)
    critical = (df["severity_display"].str.lower() == "critical").sum()
    high = (df["severity_display"].str.lower() == "high").sum()
    medium = (df["severity_display"].str.lower() == "medium").sum()
    low = (df["severity_display"].str.lower() == "low").sum()
    unclassified = total - critical - high - medium - low

    st.subheader("Road Damage Overview")

    c1, c2, c3 = st.columns(3)
    c1.metric("Total Reports", total)
    c2.metric("Critical Severity", critical)
    c3.metric("High Severity", high)

    c4, c5, c6 = st.columns(3)
    c4.metric("Medium Severity", medium)
    c5.metric("Low Severity", low)
    c6.metric("Unclassified", unclassified)

    st.divider()

    st.subheader("Search and Filter Reports")

    search = st.text_input(
        "Search by detection ID or location",
        placeholder="Enter an ID or location..."
    )

    f1, f2, f3 = st.columns(3)

    with f1:
        severity_options = ["All"] + sorted(
            df["severity_display"].unique().tolist()
        )
        selected_severity = st.selectbox(
            "Severity",
            severity_options
        )

    with f2:
        status_options = ["All"] + sorted(
            df["status_display"].unique().tolist()
        )
        selected_status = st.selectbox(
            "Status",
            status_options
        )

    with f3:
        source_options = ["All"] + sorted(
            df["source_display"].unique().tolist()
        )
        selected_source = st.selectbox(
            "Detection Source",
            source_options
        )

    filtered_df = df.copy()

    if selected_severity != "All":
        filtered_df = filtered_df[
            filtered_df["severity_display"] == selected_severity
        ]

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["status_display"] == selected_status
        ]

    if selected_source != "All":
        filtered_df = filtered_df[
            filtered_df["source_display"] == selected_source
        ]

    if search.strip():
        search_text = search.strip().lower()

        filtered_df = filtered_df[
            filtered_df["id"].astype(str).str.contains(
                search_text, case=False, na=False
            )
            |
            filtered_df["location"].fillna("").astype(str).str.contains(
                search_text, case=False, na=False
            )
        ]

    st.write(f"**{len(filtered_df)} reports found**")

    st.subheader("Detection Records")

    display_df = filtered_df[
        [
            "id",
            "detected_at",
            "location",
            "severity_display",
            "confidence",
            "status_display",
            "source_display"
        ]
    ].copy()

    display_df.columns = [
        "Detection ID",
        "Detected At",
        "Location",
        "Severity",
        "Confidence",
        "Status",
        "Source"
    ]

    display_df["Confidence"] = display_df["Confidence"].apply(
        lambda x: f"{float(x) * 100:.1f}%" if pd.notna(x) else "N/A"
    )

    st.dataframe(
        display_df,
        use_container_width=True,
        hide_index=True
    )

    csv_data = display_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="⬇️ Download Reports as CSV",
        data=csv_data,
        file_name="margdrishti_pothole_reports.csv",
        mime="text/csv"
    )

    st.divider()

    st.subheader("Detailed Detection Reports")

    if filtered_df.empty:
        st.info("No reports match your selected filters.")

    else:
        for _, report in filtered_df.iterrows():

            detection_id = report["id"]
            severity = report["severity_display"]

            with st.expander(
                f"Detection #{detection_id}  |  {severity} Severity"
            ):

                left, right = st.columns(2)

                with left:
                    st.write("**Detection ID:**", detection_id)
                    st.write(
                        "**Location:**",
                        report["location"] or "Not available"
                    )
                    st.write("**Severity:**", severity)
                    st.write("**Status:**", report["status_display"])

                with right:
                    confidence = report["confidence"]

                    if pd.notna(confidence):
                        st.write(
                            "**AI Confidence:**",
                            f"{float(confidence) * 100:.2f}%"
                        )
                    else:
                        st.write("**AI Confidence:** Not available")

                    st.write("**Source:**", report["source_display"])
                    st.write(
                        "**Detected At:**",
                        report["detected_at"] or "Not available"
                    )

                latitude = report["latitude"]
                longitude = report["longitude"]

                if pd.notna(latitude) and pd.notna(longitude):
                    st.write("**Latitude:**", latitude)
                    st.write("**Longitude:**", longitude)
                else:
                    st.write("**GPS Coordinates:** Not available")

                image_url = report["image_url"]

                if pd.notna(image_url) and str(image_url).strip():
                    st.image(
                        image_url,
                        caption=f"Pothole Detection #{detection_id}",
                        width=400
                    )
                else:
                    st.info("No image is available for this detection.")

except Exception as e:
    st.error("Unable to load pothole reports from Supabase.")
    st.exception(e)
