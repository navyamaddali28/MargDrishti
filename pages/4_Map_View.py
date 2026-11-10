
import streamlit as st
import pandas as pd
import pydeck as pdk
from components.supabase_client import supabase

st.set_page_config(
    page_title="MargDrishti | Map View",
    page_icon="📍",
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
div[data-testid="stMetric"] {
    background: #F0EBE2;
    border: 1px solid #E5DDD0;
    padding: 15px;
    border-radius: 12px;
}
div[data-testid="stMetricValue"] {
    color: #665747;
}
</style>
""", unsafe_allow_html=True)

st.title("📍 Pothole Map View")
st.write("Explore pothole detections across reported road locations.")

st.divider()

if st.button("🔄 Refresh Map"):
    st.rerun()

try:
    response = (
        supabase.table("pothole_detections")
        .select("*")
        .order("detected_at", desc=True)
        .execute()
    )

    reports = response.data or []

    if not reports:
        st.info("No pothole detections available yet.")
        st.stop()

    df = pd.DataFrame(reports)

    required_columns = [
        "id", "detected_at", "latitude", "longitude",
        "location", "severity", "status", "source",
        "confidence", "image_url"
    ]

    for column in required_columns:
        if column not in df.columns:
            df[column] = None

    df["latitude"] = pd.to_numeric(
        df["latitude"], errors="coerce"
    )
    df["longitude"] = pd.to_numeric(
        df["longitude"], errors="coerce"
    )

    valid_coordinates = (
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    )

    map_df = df[valid_coordinates].copy()
    missing_df = df[~valid_coordinates].copy()

    total_reports = len(df)
    mapped_reports = len(map_df)
    missing_coordinates = len(missing_df)

    st.subheader("Location Overview")

    c1, c2, c3 = st.columns(3)

    c1.metric("Total Detections", total_reports)
    c2.metric("Mapped Detections", mapped_reports)
    c3.metric("Missing GPS Data", missing_coordinates)

    st.divider()

    st.subheader("Explore Detection Locations")

    filter1, filter2 = st.columns(2)

    severity_values = sorted(
        df["severity"].fillna("Unclassified").astype(str).unique()
    )

    status_values = sorted(
        df["status"].fillna("Unknown").astype(str).unique()
    )

    with filter1:
        selected_severity = st.selectbox(
            "Filter by Severity",
            ["All"] + severity_values
        )

    with filter2:
        selected_status = st.selectbox(
            "Filter by Status",
            ["All"] + status_values
        )

    filtered_df = df.copy()

    if selected_severity != "All":
        filtered_df = filtered_df[
            filtered_df["severity"].fillna("Unclassified").astype(str)
            == selected_severity
        ]

    if selected_status != "All":
        filtered_df = filtered_df[
            filtered_df["status"].fillna("Unknown").astype(str)
            == selected_status
        ]

    filtered_map = filtered_df.dropna(
        subset=["latitude", "longitude"]
    ).copy()

    if not filtered_map.empty:

        severity_colors = {
            "Low": [46, 160, 90, 220],
            "Medium": [245, 190, 55, 230],
            "High": [225, 75, 65, 230],
            "Critical": [130, 25, 45, 240]
        }

        filtered_map["marker_color"] = filtered_map[
            "severity"
        ].apply(
            lambda value: severity_colors.get(
                str(value).title(),
                [110, 110, 110, 220]
            )
        )

        latitude_center = float(filtered_map["latitude"].mean())
        longitude_center = float(filtered_map["longitude"].mean())

        layer = pdk.Layer(
            "ScatterplotLayer",
            data=filtered_map,
            get_position="[longitude, latitude]",
            get_fill_color="marker_color",
            get_line_color=[255, 255, 255, 220],
            get_radius=110,
            radius_min_pixels=6,
            radius_max_pixels=18,
            pickable=True,
            auto_highlight=True
        )

        view_state = pdk.ViewState(
            latitude=latitude_center,
            longitude=longitude_center,
            zoom=11,
            pitch=30
        )

        deck = pdk.Deck(
            layers=[layer],
            initial_view_state=view_state,
            tooltip={
                "html": """
                <b>Location:</b> {location}<br/>
                <b>Severity:</b> {severity}<br/>
                <b>Status:</b> {status}<br/>
                <b>Confidence:</b> {confidence}
                """,
                "style": {
                    "backgroundColor": "#665747",
                    "color": "white"
                }
            }
        )

        st.pydeck_chart(deck, use_container_width=True)

        st.success(
            f"{len(filtered_map)} detections displayed on the map."
        )

        st.markdown("""
        **Marker legend**

        🟢 Low &nbsp;&nbsp; 🟡 Medium &nbsp;&nbsp;
        🔴 High &nbsp;&nbsp; 🟥 Critical
        """)

    else:
        st.warning(
            "No GPS-based locations are available for these filters."
        )

    st.divider()

    st.subheader("Detection Location Details")

    if not filtered_df.empty:

        display_columns = [
            "id", "location", "severity", "status",
            "latitude", "longitude", "confidence",
            "detected_at", "source"
        ]

        details = filtered_df[display_columns].copy()

        details.columns = [
            "Detection ID", "Location", "Severity", "Status",
            "Latitude", "Longitude", "Confidence",
            "Detected At", "Source"
        ]

        details["Location"] = details["Location"].fillna("Not available")
        details["Severity"] = details["Severity"].fillna("Unclassified")
        details["Status"] = details["Status"].fillna("Unknown")
        details["Source"] = details["Source"].fillna("Unknown")

        st.dataframe(
            details,
            use_container_width=True,
            hide_index=True
        )

        st.subheader("View Individual Detection")

        options = filtered_df.to_dict("records")

        selected_index = st.selectbox(
            "Choose a detection",
            range(len(options)),
            format_func=lambda i: (
                f'{options[i].get("location") or "Unknown location"}'
                f' — {options[i].get("severity") or "Unclassified"}'
                f' — ID: {options[i].get("id")}'
            )
        )

        selected = options[selected_index]

        d1, d2 = st.columns(2)

        with d1:
            st.write("**Location:**", selected.get("location") or "Not available")
            st.write("**Severity:**", selected.get("severity") or "Unknown")
            st.write("**Status:**", selected.get("status") or "Unknown")

        with d2:
            confidence = selected.get("confidence")

            if confidence is not None:
                st.write("**Confidence:**", f"{float(confidence) * 100:.1f}%")
            else:
                st.write("**Confidence:** Not available")

            st.write("**Latitude:**", selected.get("latitude"))
            st.write("**Longitude:**", selected.get("longitude"))
            st.write("**Detected at:**", selected.get("detected_at") or "Unknown")

        image_url = selected.get("image_url")

        if image_url:
            st.image(
                image_url,
                caption="Pothole detection image",
                use_container_width=True
            )
        else:
            st.info("No image is available for this detection.")

    else:
        st.info("No detections match the selected filters.")

    st.divider()

    st.subheader("Detections Without GPS Coordinates")

    if not missing_df.empty:
        st.info(
            f"{len(missing_df)} detections cannot be plotted because "
            "their GPS coordinates are missing or invalid."
        )

        missing_details = missing_df[
            ["id", "location", "severity", "status", "detected_at"]
        ].copy()

        missing_details.columns = [
            "Detection ID", "Location", "Severity",
            "Status", "Detected At"
        ]

        st.dataframe(
            missing_details,
            use_container_width=True,
            hide_index=True
        )
    else:
        st.success("All detections have valid GPS coordinates.")

except Exception as error:
    st.error("Unable to load map data from Supabase.")
    st.exception(error)
