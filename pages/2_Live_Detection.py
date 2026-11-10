import uuid
from io import BytesIO
from pathlib import Path

import streamlit as st
from PIL import Image

from components.supabase_client import supabase


st.set_page_config(
    page_title="MargDrishti | Live Detection",
    page_icon="🛣️",
    layout="wide",
)

st.markdown(
    """
    <div style="
        background:linear-gradient(120deg,#F4E8DE,#F3D5C4);
        padding:28px;
        border-radius:20px;
        margin-bottom:20px;
    ">
        <h1 style="color:#594337;margin:0;">🚧 Live Pothole Detection</h1>
        <p style="color:#765B4C;margin-top:10px;">
            Capture or upload road media for AI review
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)

project_root = Path(__file__).resolve().parent.parent
model_candidates = (
    project_root / "models" / "best.pt",
    project_root / "best.pt",
)
model_path = next((path for path in model_candidates if path.is_file()), None)


@st.cache_resource(show_spinner="Loading your pothole model...")
def load_model(weights_path: str):
    from ultralytics import YOLO

    return YOLO(weights_path)


model = None
if model_path is None:
    st.warning(
        "I couldn't find best.pt. Put it in the project's models folder at "
        "models/best.pt to enable AI detection."
    )
else:
    try:
        model = load_model(str(model_path))
        st.success(f"Loaded model: {model_path.name}")
    except Exception as error:
        st.warning(
            "The model file is present, but it could not be loaded. Install the "
            "Ultralytics package in this project's virtual environment, then restart "
            "Streamlit. If it still fails, ask your friend which YOLO package/version "
            "was used to train best.pt."
        )
        st.code(r".\.venv\Scripts\python.exe -m pip install ultralytics")
        st.code(str(error))

st.caption(
    "Camera mode takes a photo and runs the model on that photo. It does not show a "
    "continuous live-video feed. Uploaded videos can be stored, but video detection "
    "isn't connected on this page yet."
)

st.divider()
st.subheader("Capture or Upload Road Media")

source_choice = st.radio(
    "Choose how to add road media",
    ["Take a photo", "Upload a file"],
    horizontal=True,
)

media = None
if source_choice == "Take a photo":
    media = st.camera_input("Take a road photo")
else:
    media = st.file_uploader(
        "Choose an image or video",
        type=["jpg", "jpeg", "png", "webp", "mp4", "mov", "webm"],
    )

media_type = ""
image_bytes = None
detections = []

confidence_threshold = st.slider(
    "Minimum detection confidence",
    min_value=0.10,
    max_value=0.90,
    value=0.25,
    step=0.05,
    help="Lower this to show more possible potholes; raise it to show fewer, more certain results.",
)

if media is not None:
    media_type = getattr(media, "type", "") or "application/octet-stream"
    image_bytes = media.getvalue()

    if media_type.startswith("image/"):
        original_image = Image.open(BytesIO(image_bytes)).convert("RGB")

        if model is not None:
            try:
                with st.spinner("Checking the image for potholes..."):
                    result = model.predict(
                        source=original_image,
                        conf=confidence_threshold,
                        verbose=False,
                    )[0]

                # Ultralytics returns the plotted image in BGR order; Streamlit
                # expects RGB.
                annotated_bgr = result.plot()
                annotated_rgb = annotated_bgr[:, :, ::-1]
                st.image(
                    annotated_rgb,
                    caption="AI detection result",
                    use_container_width=True,
                )

                if result.boxes is not None:
                    for box in result.boxes:
                        class_id = int(box.cls[0].item())
                        score = float(box.conf[0].item())
                        class_names = result.names
                        if isinstance(class_names, dict):
                            class_name = class_names.get(class_id, str(class_id))
                        else:
                            class_name = class_names[class_id]
                        detections.append(
                            {
                                "Object": str(class_name),
                                "Confidence": f"{score * 100:.1f}%",
                                "confidence_value": score,
                            }
                        )

                if detections:
                    st.success(f"Found {len(detections)} object(s). Review the boxes above.")
                    st.table(
                        [
                            {"Object": item["Object"], "Confidence": item["Confidence"]}
                            for item in detections
                        ]
                    )
                else:
                    st.info("No objects were detected at the current confidence setting.")
            except Exception as error:
                st.error(f"Model prediction failed: {error}")
                st.image(
                    original_image,
                    caption="Original image",
                    use_container_width=True,
                )
        else:
            st.image(
                original_image,
                caption="Selected road image",
                use_container_width=True,
            )
            st.info("The image is ready to upload. AI results need a working model setup.")

    elif media_type.startswith("video/"):
        st.video(media)
        st.info("This video can be uploaded to Storage. YOLO video processing isn't connected yet.")
    else:
        st.error("This file type is not supported. Choose an image or video.")

st.divider()
st.subheader("Save to Supabase")
st.caption(
    "Enter the location and severity after reviewing the image. A database detection "
    "row is attempted only when the model found at least one object in an image."
)

with st.form("save_media_form"):
    location = st.text_input("Location", placeholder="Example: Benz Circle")
    severity = st.selectbox("Severity", ["Low", "Medium", "High", "Critical"])
    save_button = st.form_submit_button(
        "Upload media and save detections",
        type="primary",
        disabled=media is None,
    )

if save_button and media is not None:
    if not location.strip():
        st.warning("Enter the location before saving.")
    elif not image_bytes:
        st.warning("The selected media is empty. Please select it again.")
    else:
        extension = Path(getattr(media, "name", "road-media")).suffix.lower()
        if not extension:
            extension = ".jpg" if media_type.startswith("image/") else ".mp4"
        storage_path = f"{uuid.uuid4()}{extension}"

        try:
            supabase.storage.from_("pothole-images").upload(
                path=storage_path,
                file=image_bytes,
                file_options={"content-type": media_type},
            )
            public_url = supabase.storage.from_("pothole-images").get_public_url(
                storage_path
            )
        except Exception as error:
            st.error(f"Media upload failed: {error}")
        else:
            st.success("Media uploaded to the pothole-images bucket.")
            st.write("Public media URL:")
            st.code(public_url)

            if media_type.startswith("image/") and detections:
                detection_record = {
                    "image_url": public_url,
                    "location": location.strip(),
                    "severity": severity,
                    "confidence": max(
                        item["confidence_value"] for item in detections
                    ),
                }
                try:
                    supabase.table("pothole_detections").insert(
                        detection_record
                    ).execute()
                except Exception as error:
                    st.warning(
                        "The image is uploaded, but Supabase did not accept a row in "
                        "pothole_detections. Check that the table has image_url, "
                        "location, severity, and confidence columns, and that its Row "
                        "Level Security policies allow this app to insert."
                    )
                    st.caption(f"Supabase response: {error}")
                else:
                    st.success("The detected image record was saved to pothole_detections.")
            elif media_type.startswith("image/"):
                st.info(
                    "The image was uploaded. No detection row was created because the "
                    "model did not find any objects."
                )
            else:
                st.info(
                    "The video was uploaded to Storage. No detection row was created "
                    "because video inference isn't connected yet."
                )
