
import streamlit as st
from textwrap import dedent

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="MargDrishti | Home",
    page_icon="🛣️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM THEME
# =====================================================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif !important;
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
    color: #51443A;
}

.hero {
    background: linear-gradient(120deg, #FFFFFF, #EAF5F3);
    border: 1px solid #D8E9E4;
    border-radius: 24px;
    padding: 38px;
    margin: 14px 0 28px 0;
    box-shadow: 0 8px 25px rgba(70,100,90,0.07);
}

.hero-label {
    color: #087F76;
    letter-spacing: 2px;
    font-size: 12px;
    font-weight: 800;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    color: #33271F;
    margin: 12px 0;
}

.hero-text {
    color: #51443A;
    font-size: 16px;
    line-height: 1.8;
}

.module-card {
    background: #FFFFFF;
    border: 1px solid #E5D6C7;
    border-radius: 20px;
    padding: 25px;
    min-height: 175px;
    box-shadow: 0 5px 18px rgba(80,60,40,0.06);
    transition: all 0.25s ease;
}

.module-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 25px rgba(80,60,40,0.12);
}

.module-card h3 {
    color: #33271F;
    font-size: 20px;
    margin-bottom: 12px;
}

.module-card p {
    color: #51443A;
    line-height: 1.7;
    font-size: 14px;
}

.stButton > button {
    background: linear-gradient(90deg, #159B91, #268BD2);
    color: white !important;
    border: none;
    border-radius: 12px;
    padding: 10px 20px;
    font-weight: 600;
}

hr {
    border-color: #E5D6C7;
}

.footer {
    text-align: center;
    color: #75675B;
    font-size: 13px;
    padding: 20px;
}
</style>
""", unsafe_allow_html=True)


# =====================================================
# HERO SECTION
# =====================================================

hero_html = dedent("""
<div class="hero">
    <div class="hero-label">SMART ROAD INFRASTRUCTURE</div>
    <div class="hero-title">Welcome to MargDrishti</div>
    <div class="hero-text">
        AI-powered pothole detection and smart road monitoring.
        Identify road damage, review saved detections, monitor locations,
        and explore analytics from one place.
    </div>
</div>
""").strip()

st.markdown(hero_html, unsafe_allow_html=True)


# =====================================================
# PLATFORM INTRODUCTION
# =====================================================

st.markdown("## Explore the Platform")

st.write(
    "MargDrishti provides intelligent tools for road monitoring, "
    "pothole detection, reporting and analysis."
)

st.write("")


# =====================================================
# PLATFORM CARDS
# =====================================================

col1, col2 = st.columns(2, gap="large")

with col1:
    st.markdown(dedent("""
    <div class="module-card">
        <h3>📊 Dashboard</h3>
        <p>
            View total pothole detections, severity information,
            GPS-mapped locations, detection images and processed
            YOLO videos.
        </p>
    </div>
    """).strip(), unsafe_allow_html=True)

with col2:
    st.markdown(dedent("""
    <div class="module-card">
        <h3>📷 Live Detection</h3>
        <p>
            Upload road images and use the trained YOLO model
            to identify potholes and review detection confidence.
        </p>
    </div>
    """).strip(), unsafe_allow_html=True)

st.write("")

col3, col4 = st.columns(2, gap="large")

with col3:
    st.markdown(dedent("""
    <div class="module-card">
        <h3>📍 Map View</h3>
        <p>
            Explore pothole reports and their geographic
            locations using available GPS information.
        </p>
    </div>
    """).strip(), unsafe_allow_html=True)

with col4:
    st.markdown(dedent("""
    <div class="module-card">
        <h3>📈 Analytics & Reports</h3>
        <p>
            Review road condition information, detection history,
            severity distribution and report summaries.
        </p>
    </div>
    """).strip(), unsafe_allow_html=True)


# =====================================================
# PROJECT INFORMATION
# =====================================================

st.divider()

st.markdown("## About MargDrishti")

st.write(
    "MargDrishti is an AI-powered smart road monitoring system "
    "designed to identify potholes using computer vision and "
    "YOLO-based object detection."
)

st.write(
    "The platform supports detection review, image records, "
    "geographic monitoring and road condition analysis."
)

st.divider()

st.markdown(
    '<div class="footer">MARGDRISHTI | AI-POWERED SMART ROAD MONITORING</div>',
    unsafe_allow_html=True
)
