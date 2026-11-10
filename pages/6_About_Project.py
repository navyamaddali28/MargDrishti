import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="MargDrishti | About Project",
    page_icon="🛣️",
    layout="wide",
)

# ------------------------------------------------------------------
# Styling (same beige theme as the rest of the dashboard)
# ------------------------------------------------------------------
st.markdown("""
<style>
.stApp { background-color: #FAF7F2; }
h1, h2, h3, h4 { color: #594638; }
p, li { color: #65584D; }
.info-card {
    background-color: #F1E8DE;
    padding: 22px;
    border-radius: 14px;
    border: 1px solid #E5D6C7;
    margin-bottom: 15px;
}
.info-card h3, .info-card h4 { margin-top: 0; }
.tag {
    display: inline-block;
    background-color: #E5D6C7;
    color: #594638;
    padding: 4px 12px;
    border-radius: 20px;
    margin: 3px 4px 3px 0;
    font-size: 0.85rem;
}
.phase-done    { border-left: 6px solid #5E8C61; }
.phase-pending { border-left: 6px solid #D9A441; }
.phase-notyet  { border-left: 6px solid #B8A898; }
.team-name { font-weight: 600; color: #594638; }
</style>
""", unsafe_allow_html=True)


def card(html: str) -> None:
    """Small helper to show a styled card."""
    st.markdown(f'<div class="info-card">{html}</div>', unsafe_allow_html=True)


# ------------------------------------------------------------------
# Header
# ------------------------------------------------------------------
st.markdown("# 🛣️ About MargDrishti")
st.markdown("### AI-Integrated Smart Dashcam for Real-Time Pothole Detection, "
            "Reporting, and Road Health Monitoring")
st.write("EPICS Project | B.Tech Information Technology | "
         "Department of Information Technology, V R Siddhartha Engineering College")

st.divider()

# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tabs = st.tabs([
    "🌍 Overview",
    "🎯 Objectives",
    "📚 Literature",
    "🗂️ Datasets",
    "🏗️ Architecture",
    "🧠 Algorithms",
    "🚦 Progress",
    "📈 Results",
    "🔖 References",
])

# ==================================================================
# 1. OVERVIEW
# ==================================================================
with tabs[0]:
    st.markdown("## 🌍 Project Overview")
    card("""
    <b>MargDrishti</b> is a smart road monitoring system that detects potholes
    and other road defects using Artificial Intelligence and Computer Vision.
    A dashcam captures road video, an AI model detects defects in real time,
    and each detection is stored with its location, image, time and confidence,
    so that road health can be monitored from one dashboard.
    """)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("### 💡 Motivation")
        card("""
        <ul>
        <li><b>Road defects are a growing concern</b> that affect everyday
        travel and road safety.</li>
        <li><b>Potholes and surface damage</b> can lead to accidents, vehicle
        damage, discomfort and traffic disruption.</li>
        <li><b>Road conditions change continuously</b>, but conventional
        inspection is periodic and cannot capture every new defect.</li>
        <li>The lack of <b>continuous and timely road-condition information</b>
        creates a need for better awareness of road health.</li>
        </ul>
        """)
    with col2:
        st.markdown("### ⚠️ Problem Statement")
        card("""
        <ul>
        <li>Potholes pose significant risks to road safety, vehicle condition
        and smooth transportation.</li>
        <li>Traditional inspections are periodic and manual, so newly formed
        potholes are identified late.</li>
        <li>Drivers and road authorities lack continuous, location-based
        information for hazard awareness, reporting and maintenance.</li>
        <li>AI-based computer vision can enable real-time pothole detection and
        support location-based road monitoring and reporting.</li>
        </ul>
        """)

    st.markdown("### 👥 Project Team")
    t1, t2, t3 = st.columns(3)
    with t1:
        card('<span class="team-name">M.S.D. Navya Sri</span><br>24EU08100')
    with t2:
        card('<span class="team-name">G. Hamsini</span><br>24EU08086')
    with t3:
        card('<span class="team-name">Ch. Adithya</span><br>24EU08073')
    st.write("**Under the guidance of:** Dr. M. Suneetha, Head of the Department")

# ==================================================================
# 2. OBJECTIVES
# ==================================================================
with tabs[1]:
    st.markdown("## 🎯 Objectives")
    col1, col2 = st.columns(2)
    with col1:
        card("""
        <h3>🔍 Real-Time Detection</h3>
        Develop an AI-integrated smart dashcam system that detects road defects
        in real time, with potholes as the major focus, alerts drivers and
        records pothole locations using GPS.
        """)
    with col2:
        card("""
        <h3>☁️ Monitoring &amp; Reporting</h3>
        Monitor road conditions through cloud-based reporting, citizen
        participation and pothole lifecycle tracking to support timely road
        maintenance.
        """)

    st.markdown("## ✅ Expected Outcomes")
    col1, col2 = st.columns(2)
    with col1:
        card("""
        <h3>🚗 For Drivers</h3>
        Real-time pothole alerts that improve road safety and reduce vehicle
        damage through early hazard detection.
        """)
    with col2:
        card("""
        <h3>🏛️ For Road Authorities</h3>
        Monitor pothole status, track repair progress and make data-driven
        maintenance decisions using a centralized dashboard.
        """)

    st.markdown("## ✨ Key Features")
    features = [
        "AI-based pothole and road-defect detection (class, bounding box, confidence)",
        "Road image and video upload",
        "Pothole detection records with image, location, timestamp and confidence",
        "Interactive map for records with GPS coordinates",
        "Severity and status-based filtering (pothole lifecycle tracking)",
        "Analytics and dashboard summaries",
        "Centralized data storage using Supabase",
    ]
    for feature in features:
        st.markdown(f"- {feature}")

# ==================================================================
# 3. LITERATURE
# ==================================================================
with tabs[2]:
    st.markdown("## 📚 Summary of Literature Review")
    literature = pd.DataFrame([
        {
            "Year": 2025,
            "Paper": "Road Perception for Autonomous Driving: Pothole Detection in "
                     "Complex Environments Based on Improved YOLOv8",
            "Algorithm / Model": "Improved YOLOv8, OpenCV, Mosaic Augmentation, "
                                 "CBAM Attention, CIoU Loss",
            "Dataset": "Self-collected, 24,000+ images in different weather and lighting",
            "Result": "Higher mAP and robust detection in complex environments "
                      "than baseline YOLOv8",
            "Limitation": "Only pothole detection; no driver alerts, reporting "
                          "or geospatial visualization",
        },
        {
            "Year": 2025,
            "Paper": "iWatchRoad: Scalable Detection and Geospatial Visualization "
                     "of Potholes for Smart Cities",
            "Algorithm / Model": "YOLO, OCR, OpenStreetMap, Computer Vision",
            "Dataset": "Self-annotated, 7,000+ dashcam frames from Indian roads",
            "Result": "Real-time detection, GPS mapping and web-based visualization",
            "Limitation": "No driver voice alerts, citizen reporting or "
                          "complete pothole lifecycle tracking",
        },
        {
            "Year": 2025,
            "Paper": "Vision-Based Pothole Detection and Reporting System for "
                     "Smart Cities (YOLOv8-Seg and Predictive Maintenance)",
            "Algorithm / Model": "YOLOv8-Seg, MiDaS/DPT depth estimation, OpenCV",
            "Dataset": "Public pothole image datasets",
            "Result": "High-precision segmentation, cloud reporting, "
                      "predictive maintenance support",
            "Limitation": "No driver alerts, road health scoring "
                          "or repair status tracking",
        },
        {
            "Year": 2025,
            "Paper": "Pothole Detection and Analysis System (PoDAS) for Real "
                     "Time Data Using Sensor Networks",
            "Algorithm / Model": "Sensor Fusion, Wireless Sensor Network, Machine Learning",
            "Dataset": "Sensor data collected from vehicles",
            "Result": "Improved localization and road-condition analysis "
                      "through cross-validation of sensors",
            "Limitation": "Sensor-based, not computer vision; no dashcam "
                          "assistance or GIS visualization",
        },
        {
            "Year": 2024,
            "Paper": "Deep Learning-Based Pothole Detection and Classification "
                     "Using YOLOv5",
            "Algorithm / Model": "YOLOv5, OpenCV, CNN",
            "Dataset": "Kaggle pothole dataset and custom road images",
            "Result": "High accuracy and real-time performance",
            "Limitation": "No GPS integration, cloud reporting "
                          "or maintenance management",
        },
    ])
    st.dataframe(literature, hide_index=True, use_container_width=True)

    st.info(
        "**Research gap:** existing work mostly stops at detection. MargDrishti "
        "combines detection with driver alerts, GPS tagging, cloud storage, "
        "a map-based dashboard and repair-status tracking."
    )

# ==================================================================
# 4. DATASETS
# ==================================================================
with tabs[3]:
    st.markdown("## 🗂️ Datasets")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### Dataset 1: N-RDD2024")
        card("""
        <b>Road Damage &amp; Defects Dataset</b> (source: Mendeley Data)
        <ul>
        <li>Original size: 27,360 road images from 8 countries, including India</li>
        <li>Annotations: bounding boxes for road defects</li>
        <li>Our prepared India subset: <b>1,221 images</b>
        (976 training, 245 validation)</li>
        <li>8 selected classes</li>
        </ul>
        """)
        st.markdown("**Classes in the prepared dataset**")
        classes = ["Potholes (major focus)", "Longitudinal cracks",
                   "Transverse cracks", "Alligator cracks", "Manhole covers",
                   "Patchy road sections", "Waterlogged roads", "Obstacles"]
        st.markdown("".join(f'<span class="tag">{c}</span>' for c in classes),
                    unsafe_allow_html=True)

    with col2:
        st.markdown("### Dataset 2: BharatPothole")
        card("""
        <b>Indian Pothole Dataset</b> (source: iWatchRoad research project)
        <ul>
        <li>Forward-facing dashcam frames, <b>7,000+ annotated frames</b></li>
        <li>Coverage: Indian roads</li>
        <li>Annotations: bounding boxes for potholes</li>
        <li>Focus: pothole detection</li>
        </ul>
        """)
        st.markdown("**Environmental conditions**")
        conds = ["Daylight", "Dawn", "Dusk", "Night with street lighting",
                 "Rain / Monsoon", "Dry / Sunny"]
        st.markdown("".join(f'<span class="tag">{c}</span>' for c in conds),
                    unsafe_allow_html=True)
        st.markdown("**Road types**")
        roads = ["Urban", "Rural", "Village", "Unpaved", "National highways"]
        st.markdown("".join(f'<span class="tag">{r}</span>' for r in roads),
                    unsafe_allow_html=True)

    st.markdown("### 🧰 Requirements")
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Software**")
        software = pd.DataFrame([
            ("Python", "Core system development"),
            ("OpenCV", "Camera-frame capture and preprocessing"),
            ("Ultralytics YOLO", "Real-time road-defect detection"),
            ("PyTorch", "Model training and inference"),
            ("VS Code", "Development and testing"),
            ("Streamlit + PyDeck", "Dashboard and map visualization"),
            ("Supabase", "Database and image storage"),
        ], columns=["Software", "Purpose"])
        st.dataframe(software, hide_index=True, use_container_width=True)
    with col2:
        st.markdown("**Hardware**")
        hardware = pd.DataFrame([
            ("Dashcam / Camera", "Captures continuous road video"),
            ("Edge-AI computing device", "Runs the model for real-time detection"),
            ("GPS module", "Records pothole location and timestamp"),
            ("Alert unit", "Real-time audio / visual alerts"),
            ("Storage / Memory", "Stores images and detection records"),
        ], columns=["Hardware", "Purpose"])
        st.dataframe(hardware, hide_index=True, use_container_width=True)

# ==================================================================
# 5. ARCHITECTURE
# ==================================================================
with tabs[4]:
    st.markdown("## 🏗️ System Architecture")
    st.write("From the dashcam to the dashboard, data flows through six stages.")

    dot = """
    digraph G {
        rankdir=LR;
        bgcolor="transparent";
        node [shape=box, style="rounded,filled", fillcolor="#F1E8DE",
              color="#8B7868", fontname="Helvetica", fontcolor="#594638",
              margin="0.2,0.12"];
        edge [color="#8B7868", penwidth=1.5];

        cam   [label="Dashcam / Camera\\nReal-time road video"];
        edge_ [label="Edge-AI Device\\nOpenCV → YOLO\\nframe processing"];
        det   [label="Road Defect Detection\\nPothole (major focus)\\nCracks, Manhole, Patchy,\\nWaterlogging, Others\\n+ Audio / Visual Alert"];
        conn  [label="Data & Connectivity\\nWi-Fi / Mobile hotspot\\nGPS + detection data"];
        db    [label="Cloud & Database\\nImages | Location | Timestamp\\nDefect type | Confidence"];
        dash  [label="Reporting & Monitoring\\nMap dashboard, reports,\\nroad health, maintenance tracking"];

        cam -> edge_ -> det -> conn -> db -> dash;
    }
    """
    st.graphviz_chart(dot, use_container_width=True)

    st.markdown("### Stages explained")
    stages = [
        ("1. Dashcam / Camera", "Captures continuous real-time road video."),
        ("2. Edge-AI Device", "OpenCV captures frames and the YOLO model runs on each one."),
        ("3. Road Defect Detection", "Detects potholes (major focus), cracks, manholes, patchy "
                                     "roads, waterlogging and others, and triggers an audio / visual driver alert."),
        ("4. Data & Connectivity", "GPS location and detection data are sent over Wi-Fi / mobile hotspot."),
        ("5. Cloud & Database", "Detection records (image, location, timestamp, defect type, "
                                "confidence) are stored centrally."),
        ("6. Reporting & Monitoring", "Location mapping, road condition dashboard, pothole reports, "
                                      "road health monitoring and maintenance tracking."),
    ]
    for title, text in stages:
        st.markdown(f"**{title}**: {text}")

    st.caption("Note: the cloud and database layer in this prototype is Supabase "
               "and the map layer uses PyDeck.")

# ==================================================================
# 6. ALGORITHMS
# ==================================================================
with tabs[5]:
    st.markdown("## 🧠 Algorithms")

    st.markdown("### Algorithm 1: YOLO-Based Road Damage Detection")
    card("""
    <b>Detect_Road_Damage</b> detects road damage from input images or video
    frames using the trained YOLO model.<br><br>
    <b>Input:</b> I (road image or video frame), M (trained detection model),
    T (confidence threshold).<br>
    <b>Output:</b> detected road damage with class labels, confidence scores
    and bounding boxes.
    """)
    st.code("""\
1.  Load the trained model M
2.  Read the input road image or video frame I
3.  Preprocess I and resize it to the required input size
4.  Pass the preprocessed image to model M
5.  Generate predicted bounding boxes, class labels and confidence scores
6.  Initialize an empty list D to store valid detections
7.  For each predicted detection d:
8.      If confidence of d >= threshold T:
9.          Add d to detection list D
10. Draw bounding boxes and class labels on I for detections in D
11. Display the annotated image or video frame
12. Return D""", language="text")

    st.markdown("### Algorithm 2: Road Damage Reporting and Road Health Monitoring")
    card("""
    <b>Monitor_Road_Health</b> records detected road damage and uses the
    collected detections to monitor road conditions.<br><br>
    <b>Input:</b> D (detections from Algorithm 1), R (road damage records
    from processed images or frames).<br>
    <b>Output:</b> updated road damage records and a road condition summary.
    """)
    st.code("""\
1.  Initialize the road damage record list R
2.  Receive the detection list D from Algorithm 1
3.  If D is empty:
4.      Record that no road damage was detected in the current frame
5.  Else:
6.      For each detection d in D:
7.          Extract damage class, confidence score and bounding box from d
8.          Create a road damage record with the available information
9.          Add the record to R
10. Analyze the collected records in R
11. Calculate the number of detections for each road damage class
12. Generate a summary of the detected potholes and cracks
13. Display the road damage summary for monitoring
14. Return R and the road condition summary""", language="text")

# ==================================================================
# 7. PROGRESS
# ==================================================================
with tabs[6]:
    st.markdown("## 🚦 Implementation Phases")

    phases = [
        ("01", "Setup", "Completed",
         "Hardware and software setup, camera and environment setup, dataset preparation"),
        ("02", "System Development", "Completed",
         "OpenCV integration, YOLO integration, real-time processing setup"),
        ("03", "Detection Model", "Completed",
         "Pothole detection, real-time detection, bounding box and confidence output"),
        ("04", "Data Storage & Connectivity", "Pending",
         "GPS location and timestamp, detection data storage, cloud / database connectivity"),
        ("05", "Reporting & Road Health Monitoring", "Pending",
         "Dashboard and reports, location mapping, road health monitoring, maintenance tracking"),
        ("06", "Testing & Deployment", "Not Started",
         "System testing, performance evaluation, final deployment"),
    ]
    css_class = {"Completed": "phase-done", "Pending": "phase-pending",
                 "Not Started": "phase-notyet"}
    icon = {"Completed": "✅", "Pending": "⏳", "Not Started": "⚪"}

    completed = sum(1 for p in phases if p[2] == "Completed")
    st.progress(completed / len(phases),
                text=f"{completed} of {len(phases)} phases completed")

    for num, name, status, detail in phases:
        st.markdown(
            f'<div class="info-card {css_class[status]}">'
            f"<b>Phase {num}: {name}</b> &nbsp; {icon[status]} <i>{status}</i><br>"
            f"{detail}</div>",
            unsafe_allow_html=True,
        )

    st.info(
        "MargDrishti is currently a prototype. Live camera integration, automatic "
        "GPS capture and a complete end-to-end detection workflow are the next steps."
    )

    st.markdown("### 🔮 Future Scope")
    st.markdown("""
    - Continuous live detection through a USB webcam / dashcam.
    - GPS integration for automatic location tagging.
    - Automatic saving of verified AI detections.
    - Improved pothole severity classification and road health scoring.
    - Real-time driver alerts and road monitoring.
    - Citizen reporting and integration with mobile devices and road maintenance systems.
    """)

# ==================================================================
# 8. RESULTS
# ==================================================================
with tabs[7]:
    st.markdown("## 📈 Execution of Results & Analysis")

    c1, c2, c3 = st.columns(3)
    c1.metric("Pothole (live webcam)", "0.61")
    c2.metric("Multiple potholes (road image)", "0.13 – 0.57")
    c3.metric("Alligator crack", "0.55")

    col1, col2, col3 = st.columns(3)
    with col1:
        card("""
        <h4>⚙️ Execution</h4>
        <ul>
        <li>Model: YOLO</li>
        <li>Input: road image / dashcam frame</li>
        <li>Output: pothole + confidence score</li>
        </ul>
        """)
    with col2:
        card("""
        <h4>📊 Results</h4>
        <ul>
        <li>Pothole detected (live webcam): 0.61</li>
        <li>Multiple potholes detected (road image): 0.13–0.57</li>
        <li>Alligator crack detected: 0.55</li>
        </ul>
        """)
    with col3:
        card("""
        <h4>🔎 Analysis</h4>
        <ul>
        <li>Detects potholes and cracks in real time</li>
        <li>Multiple potholes detected in a single frame</li>
        <li>Works on live webcam as well as road images</li>
        </ul>
        """)

    # Optional: show your result screenshots (save them in an assets folder)
    # r1, r2, r3 = st.columns(3)
    # r1.image("assets/webcam_result.png", caption="Live webcam detection")
    # r2.image("assets/road_image_result.png", caption="Multiple potholes in one frame")
    # r3.image("assets/alligator_crack.png", caption="Alligator crack detection")

# ==================================================================
# 9. REFERENCES
# ==================================================================
with tabs[8]:
    st.markdown("## 🔖 References")
    refs = [
        "S. Kong, Q. Meng, X. Li, Z. Wang, X. Liu, and B. Li, “Road Perception for "
        "Autonomous Driving: Pothole Detection in Complex Environments Based on "
        "Improved YOLOv8,” *IEEE Access*, vol. 13, pp. 80914–80929, 2025. "
        "DOI: 10.1109/ACCESS.2025.3566944. **(Base paper)**",

        "D. Arya, H. Maeda, S. K. Ghosh, D. Toshniwal, and Y. Sekimoto, “RDD2022: A "
        "Multi-national Image Dataset for Automatic Road Damage Detection,” "
        "*Geoscience Data Journal*, vol. 11, no. 4, pp. 846–862, 2024. "
        "DOI: 10.1002/gdj3.260.",

        "H. Salaudeen and E. Çelebi, “Pothole Detection Using Image Enhancement GAN "
        "and Object Detection Network,” *Electronics*, vol. 11, no. 12, 1882, 2022. "
        "DOI: 10.3390/electronics11121882.",

        "Y. Ma et al., “Pavement Distress Detection and Classification Based on YOLO "
        "Network,” *International Journal of Pavement Engineering*, vol. 22, no. 13, "
        "pp. 1659–1672, 2021. DOI: 10.1080/10298436.2020.1714047.",

        "D. Arya et al., “RDD2020: An Annotated Image Dataset for Automatic Road "
        "Damage Detection Using Deep Learning,” *Data in Brief*, vol. 36, 107133, 2021. "
        "DOI: 10.1016/j.dib.2021.107133.",
    ]
    for i, ref in enumerate(refs, start=1):
        st.markdown(f"**[{i}]** {ref}")

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.divider()
st.markdown(
    "<div style='text-align:center; color:#8B7868;'>"
    "MargDrishti | AI-Powered Road Monitoring<br>"
    "Building smarter and safer roads"
    "</div>",
    unsafe_allow_html=True,
)