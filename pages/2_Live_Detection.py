
from datetime import datetime
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image, ImageOps


# =====================================================
# CONFIGURATION
# =====================================================

ROOT = Path(__file__).resolve().parents[1]

MODEL_PATH = ROOT / "models" / "best.pt"
RESULTS_DIR = ROOT / "results" / "live_detections"

RESULTS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="MargDrishti | Live Detection",
    page_icon="🚧",
    layout="wide"
)


# =====================================================
# CUSTOM DESIGN
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: Inter, sans-serif;
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
}

section[data-testid="stSidebar"] * {
    color: #594638;
}

h1, h2, h3 {
    color: #33271F !important;
}

div.stButton > button {
    background: linear-gradient(90deg,#159B91,#268BD2);
    color: white !important;
    border: none;
    border-radius: 12px;
    font-weight: 600;
    padding: 10px 20px;
}

[data-testid="stMetric"] {
    background: white;
    border: 1px solid #E5D6C7;
    border-radius: 16px;
    padding: 18px;
}

.hero {
    background: linear-gradient(120deg,#FFFFFF,#EAF5F3);
    border: 1px solid #D8E9E4;
    border-radius: 22px;
    padding: 28px;
    margin-bottom: 24px;
}

.hero-title {
    font-size: 32px;
    font-weight: 800;
    color: #33271F;
}

.hero-text {
    color: #51443A;
    font-size: 15px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# LOAD YOLO MODEL
# =====================================================

@st.cache_resource
def load_yolo_model(model_path):

    from ultralytics import YOLO

    return YOLO(str(model_path))


# =====================================================
# PAGE HEADER
# =====================================================

st.markdown("""
<div class="hero">
    <div class="hero-title">🚧 Live Pothole Detection</div>
    <div class="hero-text">
        Upload a road image and identify potholes using
        the trained YOLO11s detection model.
    </div>
</div>
""", unsafe_allow_html=True)


# =====================================================
# MODEL VALIDATION
# =====================================================

if not MODEL_PATH.is_file():

    st.error(f"Model file not found: {MODEL_PATH}")
    st.stop()

try:

    model = load_yolo_model(str(MODEL_PATH))

except Exception as error:

    st.error(f"Unable to load YOLO model: {error}")
    st.stop()


with st.expander("View Model Information"):

    st.write("Model:", MODEL_PATH.name)
    st.write("Model path:", str(MODEL_PATH))
    st.write("Model classes:", model.names)


# =====================================================
# IMAGE UPLOAD
# =====================================================

st.markdown("## 1. Upload Road Image")

uploaded_file = st.file_uploader(
    "Choose a road image",
    type=["jpg", "jpeg", "png", "webp"]
)


# =====================================================
# CONFIDENCE SETTINGS
# =====================================================

confidence = st.slider(
    "Detection Confidence Threshold",
    min_value=0.01,
    max_value=0.90,
    value=0.01,
    step=0.01
)


# =====================================================
# IMAGE PROCESSING
# =====================================================

if uploaded_file is not None:

    try:

        original_image = ImageOps.exif_transpose(
            Image.open(
                BytesIO(uploaded_file.getvalue())
            )
        ).convert("RGB")

    except Exception as error:

        st.error(f"Unable to open image: {error}")
        st.stop()

    st.image(
        original_image,
        caption="Uploaded Road Image",
        use_container_width=True
    )

    # =================================================
    # RUN DETECTION
    # =================================================

    if st.button(
        "🔍 Detect Potholes",
        type="primary",
        use_container_width=True
    ):

        try:

            with st.spinner(
                "YOLO is analysing your road image..."
            ):

                results = model.predict(
                    source=np.asarray(original_image),
                    conf=confidence,
                    imgsz=1280,
                    iou=0.45,
                    augment=True,
                    max_det=100,
                    verbose=False
                )

                result = results[0]

            # =================================================
            # RAW DETECTION INFORMATION
            # =================================================

            boxes = result.boxes
            names = model.names

            raw_count = 0 if boxes is None else len(boxes)

            st.divider()

            st.markdown("## 2. Detection Results")

            st.metric(
                "Total Raw YOLO Detections",
                raw_count
            )

            pothole_indices = []
            records = []
            scores = []

            # =================================================
            # FILTER POTHOLE CLASS
            # =================================================

            if boxes is not None and len(boxes) > 0:

                for index, box in enumerate(boxes):

                    class_id = int(box.cls[0].item())

                    if isinstance(names, dict):
                        class_name = names.get(
                            class_id,
                            str(class_id)
                        )
                    else:
                        class_name = names[class_id]

                    score = float(box.conf[0].item())

                    # Display raw detection information
                    st.write(
                        f"Class: {class_name} | "
                        f"Confidence: {score * 100:.2f}%"
                    )

                    if (
                        str(class_name).strip().lower()
                        == "pothole"
                    ):

                        pothole_indices.append(index)
                        scores.append(score)

                        coordinates = box.xyxy[0].tolist()

                        records.append({
                            "Object": "Pothole",
                            "Confidence (%)": round(
                                score * 100, 2
                            ),
                            "X1": round(coordinates[0], 1),
                            "Y1": round(coordinates[1], 1),
                            "X2": round(coordinates[2], 1),
                            "Y2": round(coordinates[3], 1)
                        })

            # =================================================
            # NO DETECTION
            # =================================================

            if len(pothole_indices) == 0:

                st.warning(
                    "No potholes detected by the trained model."
                )

                if raw_count == 0:

                    st.info(
                        "YOLO returned zero bounding boxes. "
                        "The model may need further training "
                        "with similar pothole images."
                    )

                else:

                    st.info(
                        "YOLO detected objects, but none matched "
                        "the pothole class."
                    )

                st.image(
                    original_image,
                    caption="Image analysed by YOLO",
                    use_container_width=True
                )

            # =================================================
            # POTHOLE DETECTED
            # =================================================

            else:

                annotated_image = result.plot()[:, :, ::-1]

                detection_df = pd.DataFrame(records)

                st.success(
                    f"{len(pothole_indices)} pothole(s) detected!"
                )

                # Display images
                col1, col2 = st.columns(2)

                with col1:

                    st.image(
                        original_image,
                        caption="Original Road Image",
                        use_container_width=True
                    )

                with col2:

                    st.image(
                        annotated_image,
                        caption="Detected Potholes",
                        use_container_width=True
                    )

                # =================================================
                # METRICS
                # =================================================

                metric1, metric2, metric3 = st.columns(3)

                metric1.metric(
                    "Potholes Detected",
                    len(pothole_indices)
                )

                metric2.metric(
                    "Average Confidence",
                    f"{np.mean(scores) * 100:.2f}%"
                )

                metric3.metric(
                    "Highest Confidence",
                    f"{max(scores) * 100:.2f}%"
                )

                # =================================================
                # DETECTION DETAILS
                # =================================================

                st.markdown("### Detection Details")

                st.dataframe(
                    detection_df,
                    use_container_width=True,
                    hide_index=True
                )

                # =================================================
                # SAVE RESULTS
                # =================================================

                timestamp = datetime.now().strftime(
                    "%Y%m%d_%H%M%S"
                )

                image_name = (
                    f"pothole_detection_{timestamp}.jpg"
                )

                csv_name = (
                    f"pothole_detection_{timestamp}.csv"
                )

                image_path = RESULTS_DIR / image_name
                csv_path = RESULTS_DIR / csv_name

                Image.fromarray(
                    annotated_image
                ).save(
                    image_path,
                    format="JPEG",
                    quality=95
                )

                detection_df.to_csv(
                    csv_path,
                    index=False
                )

                st.success(
                    "Detection results saved successfully!"
                )

                # =================================================
                # DOWNLOAD IMAGE AND CSV
                # =================================================

                image_buffer = BytesIO()

                Image.fromarray(
                    annotated_image
                ).save(
                    image_buffer,
                    format="JPEG",
                    quality=95
                )

                download_col1, download_col2 = st.columns(2)

                with download_col1:

                    st.download_button(
                        "⬇️ Download Annotated Image",
                        data=image_buffer.getvalue(),
                        file_name=image_name,
                        mime="image/jpeg",
                        use_container_width=True
                    )

                with download_col2:

                    st.download_button(
                        "⬇️ Download Detection Report",
                        data=detection_df.to_csv(
                            index=False
                        ).encode("utf-8"),
                        file_name=csv_name,
                        mime="text/csv",
                        use_container_width=True
                    )

        except Exception as error:

            st.error(
                f"Detection failed: {error}"
            )


# =====================================================
# SAVED DETECTION GALLERY
# =====================================================

st.divider()

st.markdown("## 🖼️ Saved Detection Gallery")

saved_images = sorted(
    RESULTS_DIR.glob("pothole_detection_*.jpg"),
    key=lambda path: path.stat().st_mtime,
    reverse=True
)

if saved_images:

    columns = st.columns(3)

    for index, image_path in enumerate(saved_images[:9]):

        with columns[index % 3]:

            st.image(
                str(image_path),
                use_container_width=True
            )

            st.caption(image_path.name)

else:

    st.info(
        "Your detected pothole images will appear here."
    )


# =====================================================
# FOOTER
# =====================================================

st.divider()

st.caption(
    "MARGDRISHTI | YOLO11s-BASED POTHOLE DETECTION"
)
