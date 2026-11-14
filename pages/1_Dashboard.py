
import uuid
from io import BytesIO
from pathlib import Path

import streamlit as st
import pandas as pd
import pydeck as pdk
from PIL import Image

from components.database import (
    get_pothole_detections,
    get_road_reports
)
from components.supabase_client import supabase


# =====================================================
# CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="MargDrishti Dashboard",
    page_icon="🛣️",
    layout="wide"
)

ROOT = Path(__file__).resolve().parents[1]
MODEL_PATH = ROOT / "models" / "best.pt"

IMAGE_BUCKET = "pothole-images"


# =====================================================
# WHITE AND BEIGE THEME
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: #FAF7F2;
    color: #33271F;
}

.block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: #F1E8DE;
    border-right: 1px solid #E5D6C7;
}

section[data-testid="stSidebar"] * {
    color: #594638;
}

h1, h2, h3, h4 {
    color: #33271F !important;
    font-weight: 700 !important;
}

p, label {
    color: #51443A !important;
}

[data-testid="stMetric"] {
    background: #FFFFFF;
    border: 1px solid #E5D6C7;
    border-radius: 18px;
    padding: 20px;
    box-shadow: 0 5px 18px rgba(80,60,40,0.06);
}

[data-testid="stMetricLabel"] {
    color: #594638 !important;
}

[data-testid="stMetricValue"] {
    color: #33271F !important;
    font-weight: 800;
}

div.stButton > button,
div.stFormSubmitButton > button {
    background: linear-gradient(90deg,#159B91,#268BD2);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
}

div.stButton > button:hover {
    background: #11766D;
}

div[data-testid="stForm"] {
    background: #FFFFFF;
    border: 1px solid #E5D6C7;
    border-radius: 18px;
    padding: 20px;
}

.hero {
    background: linear-gradient(120deg,#FFFFFF,#EAF5F3);
    border: 1px solid #D8E9E4;
    padding: 32px;
    border-radius: 22px;
    margin: 12px 0 25px 0;
    box-shadow: 0 8px 25px rgba(70,100,90,0.07);
}

.section-label {
    color: #087F76;
    font-size: 12px;
    font-weight: 800;
    letter-spacing: 1.5px;
}

.hero-title {
    font-size: 34px;
    font-weight: 800;
    color: #33271F !important;
    margin: 8px 0;
}

.hero-subtitle {
    color: #51443A !important;
    font-size: 15px;
}

[data-testid="stImage"] img,
video {
    border-radius: 14px;
}

hr {
    border-color: #E5D6C7;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD YOLO MODEL
# =====================================================

@st.cache_resource
def load_model(model_path):
    from ultralytics import YOLO
    return YOLO(str(model_path))


model = None

if MODEL_PATH.is_file():
    try:
        model = load_model(MODEL_PATH)
        st.success("YOLO model loaded successfully.")
    except Exception as e:
        st.error(f"Model loading failed: {e}")
else:
    st.error(f"Model not found: {MODEL_PATH}")


# =====================================================
# VIDEO SEARCH
# =====================================================

def get_processed_video():

    candidates = [
        ROOT.parent / "results" / "pothole_final_tracking_h264.mp4",
        ROOT.parent / "results" / "pothole_final_tracking.mp4",
        ROOT.parent / "results" / "pothole_detected_video.mp4",
        ROOT / "results" / "pothole_final_tracking_h264.mp4",
        ROOT / "results" / "pothole_final_tracking.mp4",
    ]

    for path in candidates:
        if path.is_file() and path.stat().st_size > 0:
            return path

    return None


# =====================================================
# SUPABASE IMAGE STORAGE
# =====================================================

def upload_processed_image(image_bytes):

    filename = f"dashboard_{uuid.uuid4().hex}.jpg"

    supabase.storage.from_(IMAGE_BUCKET).upload(
        path=filename,
        file=image_bytes,
        file_options={
            "content-type": "image/jpeg"
        }
    )

    public_url = supabase.storage.from_(
        IMAGE_BUCKET
    ).get_public_url(filename)

    if isinstance(public_url, dict):
        public_url = (
            public_url.get("publicUrl")
            or public_url.get("publicURL")
        )

    if not public_url:
        raise RuntimeError("Supabase did not return an image URL.")

    return public_url


# =====================================================
# SAVE DETECTION
# =====================================================

def save_detection_record(
    image_url,
    location,
    severity,
    confidence
):

    record = {
        "image_url": image_url,
        "location": location,
        "severity": severity,
        "confidence": float(confidence)
    }

    supabase.table(
        "pothole_detections"
    ).insert(record).execute()


# =====================================================
# HERO SECTION
# =====================================================

st.markdown("""
<div class="hero">
    <div class="section-label">SMART ROAD INFRASTRUCTURE</div>
    <div class="hero-title">MargDrishti Dashboard</div>
    <p class="hero-subtitle">
        AI-powered pothole detection and smart road monitoring.
    </p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# IMAGE DETECTION
# =====================================================

st.markdown("## 🚧 AI Pothole Detection")

st.caption(
    "Upload a road image and analyse it using your trained YOLO model."
)

with st.container(border=True):

    uploaded_image = st.file_uploader(
        "Upload Road Image",
        type=["jpg", "jpeg", "png", "webp"],
        key="dashboard_image"
    )

    location = st.text_input(
        "Detection Location",
        placeholder="Example: Vijayawada"
    )

    severity = st.selectbox(
        "Severity",
        ["Medium", "Low", "High", "Critical"],
        index=0
    )

    confidence_threshold = st.slider(
        "Detection Confidence Threshold",
        min_value=0.05,
        max_value=0.90,
        value=0.15,
        step=0.05
    )

    detect_button = st.button(
        "🔍 Detect Potholes",
        type="primary",
        use_container_width=True,
        disabled=(uploaded_image is None or model is None)
    )


if detect_button and uploaded_image is not None:

    if not location.strip():

        st.warning("Please enter the detection location.")

    else:

        try:

            original_image = Image.open(
                BytesIO(uploaded_image.getvalue())
            ).convert("RGB")

            with st.spinner("Running YOLO detection..."):

                result = model.predict(
                    source=original_image,
                    conf=confidence_threshold,
                    imgsz=640,
                    verbose=False
                )[0]

            boxes = result.boxes

            st.write("**Model classes:**", model.names)

            if boxes is None or len(boxes) == 0:

                st.warning(
                    "No objects detected. Try a clearer image or check "
                    "whether best.pt was trained with pothole images."
                )

                st.image(
                    original_image,
                    caption="Uploaded image",
                    use_container_width=True
                )

            else:

                annotated_bgr = result.plot()
                annotated_rgb = annotated_bgr[:, :, ::-1]

                st.success(
                    f"Detected {len(boxes)} object(s)."
                )

                st.image(
                    annotated_rgb,
                    caption="YOLO Pothole Detection Result",
                    use_container_width=True
                )

                scores = []
                class_names = []

                for box in boxes:

                    scores.append(
                        float(box.conf[0].item())
                    )

                    class_id = int(box.cls[0].item())

                    if isinstance(model.names, dict):
                        name = model.names.get(
                            class_id,
                            str(class_id)
                        )
                    else:
                        name = model.names[class_id]

                    class_names.append(str(name))

                detection_data = pd.DataFrame({
                    "Detected Object": class_names,
                    "Confidence": [
                        f"{score * 100:.2f}%"
                        for score in scores
                    ],
                    "Severity": [severity] * len(scores)
                })

                st.dataframe(
                    detection_data,
                    use_container_width=True,
                    hide_index=True
                )

                output = BytesIO()

                Image.fromarray(annotated_rgb).save(
                    output,
                    format="JPEG",
                    quality=92
                )

                processed_bytes = output.getvalue()

                with st.spinner("Saving image and detection to Supabase..."):

                    image_url = upload_processed_image(
                        processed_bytes
                    )

                    save_detection_record(
                        image_url=image_url,
                        location=location.strip(),
                        severity=severity,
                        confidence=max(scores)
                    )

                st.success("Detection saved successfully!")

                st.write(f"**Severity:** {severity}")
                st.write(
                    f"**Confidence:** {max(scores) * 100:.2f}%"
                )

                st.cache_data.clear()

        except Exception as e:

            st.error(f"Detection or saving failed: {e}")


# =====================================================
# PROCESSED YOLO VIDEO
# =====================================================

st.divider()

st.markdown("## 🎥 Processed YOLO Pothole Detection Video")

st.caption(
    "Previously processed pothole tracking video."
)

video_path = get_processed_video()

if video_path:

    st.success(
        f"Video loaded: {video_path.name}"
    )

    st.video(str(video_path))

else:

    st.error("Processed video was not found.")

    st.code(
        str(ROOT.parent / "results" / "pothole_final_tracking_h264.mp4")
    )


# =====================================================
# LOAD DATABASE RECORDS
# =====================================================

st.divider()

st.markdown("## 📊 Road Monitoring Overview")

if st.button("↻ Refresh Dashboard"):
    st.rerun()

try:

    detections = get_pothole_detections() or []
    reports = get_road_reports() or []

    df = pd.DataFrame(detections)
    reports_df = pd.DataFrame(reports)

except Exception as e:

    st.error(f"Database loading failed: {e}")
    st.stop()


# =====================================================
# PREPARE DATA
# =====================================================

if not df.empty:

    defaults = {
        "severity": "Unknown",
        "location": "Not available",
        "latitude": None,
        "longitude": None,
        "status": "Pending",
        "confidence": None,
        "detected_at": None,
        "image_url": None
    }

    for column, default in defaults.items():

        if column not in df.columns:
            df[column] = default

    df["latitude"] = pd.to_numeric(
        df["latitude"],
        errors="coerce"
    )

    df["longitude"] = pd.to_numeric(
        df["longitude"],
        errors="coerce"
    )

    df["confidence"] = pd.to_numeric(
        df["confidence"],
        errors="coerce"
    )

    if "detected_at" in df.columns:

        df["detected_at"] = pd.to_datetime(
            df["detected_at"],
            errors="coerce",
            utc=True
        )

        df = df.sort_values(
            "detected_at",
            ascending=False,
            na_position="last"
        )

    mapped_df = df[
        df["latitude"].between(-90, 90)
        & df["longitude"].between(-180, 180)
    ].copy()

else:

    mapped_df = pd.DataFrame()


# =====================================================
# METRICS
# =====================================================

total = len(df)

if not df.empty:

    severity_values = (
        df["severity"]
        .fillna("")
        .astype(str)
        .str.lower()
    )

    critical = int(
        (severity_values == "critical").sum()
    )

    high = int(
        (severity_values == "high").sum()
    )

    medium = int(
        (severity_values == "medium").sum()
    )

    low = int(
        (severity_values == "low").sum()
    )

else:

    critical = high = medium = low = 0


mapped = len(mapped_df)

if not reports_df.empty and "status" in reports_df.columns:

    pending_reports = int(
        reports_df["status"]
        .fillna("")
        .astype(str)
        .str.lower()
        .isin(["pending", "open"])
        .sum()
    )

else:

    pending_reports = 0


# =====================================================
# KPI CARDS
# =====================================================

c1, c2, c3, c4 = st.columns(4)

c1.metric("Total Detections", total)
c2.metric("High Severity", high + critical)
c3.metric("GPS Mapped", mapped)
c4.metric("Pending Reports", pending_reports)


# =====================================================
# SEVERITY CHART
# =====================================================

st.markdown("### Severity Overview")

severity_data = pd.DataFrame({
    "Severity": ["Critical", "High", "Medium", "Low"],
    "Detections": [
        critical,
        high,
        medium,
        low
    ]
})

st.bar_chart(
    severity_data.set_index("Severity"),
    color="#159B91"
)


# =====================================================
# GEOGRAPHIC MONITORING
# =====================================================

st.markdown("### Geographic Monitoring")

if not mapped_df.empty:

    map_data = mapped_df.copy()

    color_map = {
        "low": [34, 160, 110],
        "medium": [235, 176, 65],
        "high": [224, 91, 76],
        "critical": [145, 45, 55]
    }

    map_data["marker_color"] = (
        map_data["severity"]
        .fillna("Unknown")
        .astype(str)
        .str.lower()
        .map(color_map)
        .apply(
            lambda value: value
            if isinstance(value, list)
            else [100, 130, 140]
        )
    )

    layer = pdk.Layer(
        "ScatterplotLayer",
        data=map_data,
        get_position="[longitude, latitude]",
        get_fill_color="marker_color",
        get_radius=85,
        radius_min_pixels=6,
        radius_max_pixels=16,
        pickable=True
    )

    deck = pdk.Deck(
        layers=[layer],
        initial_view_state=pdk.ViewState(
            latitude=map_data["latitude"].mean(),
            longitude=map_data["longitude"].mean(),
            zoom=12,
            pitch=35
        ),
        map_style=(
            "https://basemaps.cartocdn.com/"
            "gl/positron-gl-style/style.json"
        ),
        tooltip={
            "html": """
            <b>Location:</b> {location}<br/>
            <b>Severity:</b> {severity}<br/>
            <b>Status:</b> {status}
            """
        }
    )

    st.pydeck_chart(
        deck,
        use_container_width=True
    )

else:

    st.info("No valid GPS coordinates available yet.")


# =====================================================
# LATEST DETECTION
# =====================================================

st.markdown("### Latest Detection")

if not df.empty:

    latest = df.iloc[0]

    image_url = latest.get("image_url")

    image_col, details_col = st.columns([1.2, 1])

    with image_col:

        if pd.notna(image_url) and str(image_url).strip():

            st.image(
                str(image_url),
                caption="Latest saved detection",
                use_container_width=True
            )

        else:

            st.info("No image available for this record.")

    with details_col:

        st.markdown("#### Detection Details")

        st.write(
            "**Location:**",
            latest.get("location", "N/A")
        )

        st.write(
            "**Severity:**",
            latest.get("severity", "Unknown")
        )

        st.write(
            "**Status:**",
            latest.get("status", "Pending")
        )

        confidence = latest.get("confidence")

        if pd.notna(confidence):

            if confidence <= 1:
                confidence *= 100

            st.write(
                f"**Confidence:** {confidence:.2f}%"
            )

        else:

            st.write("**Confidence:** N/A")

        st.write(
            "**Detected At:**",
            latest.get("detected_at", "N/A")
        )

else:

    st.info("No pothole detections available.")


# =====================================================
# DETECTION GALLERY
# =====================================================

st.markdown("## 🖼️ Pothole Detection Gallery")

st.caption(
    "Images saved with your Supabase detection records."
)

if not df.empty and "image_url" in df.columns:

    gallery = df[
        df["image_url"].notna()
    ].copy()

    gallery = gallery[
        gallery["image_url"]
        .astype(str)
        .str.strip()
        .ne("")
    ].head(12)

    if not gallery.empty:

        columns = st.columns(4)

        for index, (_, record) in enumerate(
            gallery.iterrows()
        ):

            with columns[index % 4]:

                st.image(
                    str(record["image_url"]),
                    use_container_width=True
                )

                st.caption(
                    f"Severity: {record.get('severity', 'Unknown')}"
                )

                confidence = record.get("confidence")

                if pd.notna(confidence):

                    if confidence <= 1:
                        confidence *= 100

                    st.caption(
                        f"Confidence: {confidence:.2f}%"
                    )

                else:

                    st.caption("Confidence: N/A")

                st.caption(
                    f"Location: {record.get('location', 'N/A')}"
                )

    else:

        st.info("No saved detection images found.")

else:

    st.info("No detection image records available.")


# =====================================================
# ROAD REPORTS
# =====================================================

st.markdown("## Recent Road Reports")

if not reports_df.empty:

    st.dataframe(
        reports_df.head(10),
        use_container_width=True,
        hide_index=True
    )

else:

    st.info("No road reports available yet.")


# =====================================================
# GPS QUALITY
# =====================================================

st.markdown("## GPS Data Quality")

missing_gps = total - mapped

g1, g2 = st.columns(2)

g1.metric("Mapped Records", mapped)
g2.metric("Missing GPS Records", missing_gps)

if missing_gps > 0:

    st.warning(
        f"{missing_gps} records do not have valid GPS coordinates."
    )


st.divider()

st.caption(
    "MARGDRISHTI | AI-POWERED SMART ROAD MONITORING"
)
