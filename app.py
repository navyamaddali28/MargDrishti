
import streamlit as st
from components.supabase_client import (
    create_auth_client,
    get_authenticated_client
)

st.set_page_config(
    page_title="MargDrishti",
    page_icon="🛣️",
    layout="wide"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

html, body, [class*="css"] {
    font-family: 'Inter', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #07111f, #0c1b2e, #101d31);
    color: #e8f1fa;
}

.block-container {
    padding: 2rem 3rem;
    max-width: 1500px;
}

section[data-testid="stSidebar"] {
    background: rgba(12, 27, 46, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

section[data-testid="stSidebar"] * {
    color: #e8f1fa;
}

h1, h2, h3 {
    color: #f4f8ff !important;
    font-weight: 700 !important;
}

p, label {
    color: #aebfd2;
}

.glass-card {
    background: rgba(255,255,255,0.055);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 20px;
    padding: 25px;
    backdrop-filter: blur(16px);
    min-height: 145px;
}

.glass-card h3 {
    font-size: 19px;
    margin-bottom: 12px;
}

.glass-card p {
    font-size: 14px;
    line-height: 1.7;
}

.hero {
    background: linear-gradient(120deg, rgba(17,190,190,0.16), rgba(50,110,180,0.10));
    border: 1px solid rgba(65,220,220,0.20);
    border-radius: 24px;
    padding: 35px;
    margin: 15px 0 25px 0;
}

.hero-label {
    color: #42d6d0;
    letter-spacing: 3px;
    font-size: 12px;
    font-weight: 700;
}

.hero-title {
    font-size: 38px;
    font-weight: 800;
    color: #f4f8ff;
    margin: 12px 0;
}

.hero-text {
    color: #afc1d4;
    font-size: 15px;
    line-height: 1.8;
}

div.stButton > button {
    background: linear-gradient(90deg, #12b8b5, #268bd2);
    color: white;
    border: none;
    border-radius: 12px;
    padding: 10px 22px;
    font-weight: 600;
}

div.stButton > button:hover {
    border: 1px solid #4ce4df;
    color: white;
}

div[data-testid="stForm"] {
    background: rgba(255,255,255,0.045);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 25px;
}

input {
    background: #14263b !important;
    color: white !important;
}

hr {
    border-color: rgba(255,255,255,0.10);
}
</style>
""", unsafe_allow_html=True)

if "admin_access_token" not in st.session_state:
    st.session_state.admin_access_token = None

if "admin_refresh_token" not in st.session_state:
    st.session_state.admin_refresh_token = None

if "admin_email" not in st.session_state:
    st.session_state.admin_email = None

if st.session_state.admin_access_token:
    try:
        admin_client = get_authenticated_client(
            st.session_state.admin_access_token,
            st.session_state.admin_refresh_token
        )

        user = admin_client.auth.get_user()
        user_id = user.user.id

        result = (
            admin_client.table("staff_members")
            .select("role")
            .eq("user_id", user_id)
            .limit(1)
            .execute()
        )

        if result.data and result.data[0]["role"] == "admin":
            st.session_state.admin_role = "admin"

            st.success(
                f"Logged in as Admin: {st.session_state.admin_email}"
            )

            if st.button("Logout"):
                st.session_state.admin_access_token = None
                st.session_state.admin_refresh_token = None
                st.session_state.admin_email = None
                st.session_state.admin_role = None
                st.rerun()

        else:
            st.error("This account does not have Admin access.")
            st.session_state.admin_access_token = None
            st.session_state.admin_refresh_token = None
            st.session_state.admin_email = None
            st.rerun()

    except Exception:
        st.session_state.admin_access_token = None
        st.session_state.admin_refresh_token = None
        st.session_state.admin_email = None
        st.session_state.admin_role = None
        st.warning("Your session expired. Please log in again.")

st.markdown("""
<div class="hero">
    <div class="hero-label">SMART ROAD INFRASTRUCTURE</div>
    <div class="hero-title">🛣️ MargDrishti</div>
    <div class="hero-text">
        AI-Powered Road Monitoring and Pothole Detection System.
        Monitor road conditions, identify potholes and support
        smarter infrastructure management.
    </div>
</div>
""", unsafe_allow_html=True)

if not st.session_state.admin_access_token:
    st.markdown("## 🔐 Admin Login")
    st.caption("Sign in with your authorized administrator account.")

    with st.form("admin_login_form"):
        email = st.text_input("Admin Email")
        password = st.text_input("Password", type="password")
        login_button = st.form_submit_button("Login")

    if login_button:
        if not email or not password:
            st.warning("Please enter both email and password.")
        else:
            try:
                auth_client = create_auth_client()

                response = auth_client.auth.sign_in_with_password({
                    "email": email,
                    "password": password
                })

                if response.session and response.user:
                    user_id = response.user.id

                    result = (
                        auth_client.table("staff_members")
                        .select("role")
                        .eq("user_id", user_id)
                        .limit(1)
                        .execute()
                    )

                    if result.data and result.data[0]["role"] == "admin":
                        st.session_state.admin_access_token = (
                            response.session.access_token
                        )
                        st.session_state.admin_refresh_token = (
                            response.session.refresh_token
                        )
                        st.session_state.admin_email = response.user.email
                        st.session_state.admin_role = "admin"

                        st.success("Admin login successful!")
                        st.rerun()
                    else:
                        auth_client.auth.sign_out()
                        st.error("This account is not registered as an Admin.")

            except Exception as e:
                st.error("Login failed. Check your email and password.")

st.markdown("## Platform Modules")

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="glass-card">
        <h3>🚧 Pothole Detection</h3>
        <p>Detect road damage using AI-powered YOLO technology.</p>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="glass-card">
        <h3>📍 Road Monitoring</h3>
        <p>View reported potholes and their geographical locations.</p>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="glass-card">
        <h3>📊 Road Analytics</h3>
        <p>Understand road conditions through detection statistics.</p>
    </div>
    """, unsafe_allow_html=True)

st.divider()

st.caption("MargDrishti | AI-Powered Smart Road Monitoring")
