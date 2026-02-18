import streamlit as st
import requests
import plotly.graph_objects as go
import time
import base64
import os

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Job_Replacement_Detector",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# LOAD LOCAL VIDEO SAFELY
# ===============================

def get_video_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

video_base64 = ""
if os.path.exists("video.mp4"):
    video_base64 = get_video_base64("video.mp4")

# ===============================
# GLOBAL STYLING + VIDEO BACKGROUND
# ===============================

st.markdown(f"""
<style>
.stApp {{
    background: transparent !important;
}}

.video-container {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100vw;
    height: 100vh;
    z-index: -1000;
    overflow: hidden;
}}

.video-container video {{
    position: absolute;
    top: 50%;
    left: 50%;
    min-width: 100%;
    min-height: 100%;
    transform: translate(-50%, -50%);
    object-fit: cover;
    filter: brightness(0.35);
}}

.overlay {{
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: radial-gradient(circle at center,
        rgba(0,0,0,0.6),
        rgba(0,0,0,0.95));
    z-index: -999;
}}

.bento-card {{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(25px);
    border-radius: 20px;
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.15);
}}
</style>

{f'''
<div class="video-container">
    <video autoplay loop muted playsinline>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
</div>
''' if video_base64 else ""}

<div class="overlay"></div>

""", unsafe_allow_html=True)

# ===============================
# SIDEBAR
# ===============================

with st.sidebar:
    st.markdown("## ⚙ CONTROL PANEL")

    roles = [
        'Data Analyst','Accountant','Teacher','Customer Support Rep',
        'Software Engineer','Marketing Specialist','Financial Analyst',
        'HR Manager','Mechanical Engineer','Truck Driver'
    ]

    role = st.selectbox("Job Role", roles)
    sector = st.selectbox("Sector", ["Technology","Finance","Healthcare","Industrial","Other"])

    st.markdown("### Risk Parameters")
    auto = st.slider("Automation Exposure", 0, 100, 60)
    gap = st.slider("Skill Gap Index", 0.0, 10.0, 4.5)
    adoption = st.slider("AI Adoption Level", 0.0, 10.0, 6.0)

    run = st.button("🚀 RUN FORECAST")

# ===============================
# HEADER
# ===============================

st.title("🤖 AI Job Replacement Intelligence Radar")
st.markdown(f"### Analyzing risk for **{role}**")

# ===============================
# BEFORE RUN
# ===============================

if not run:
    st.info("System Ready. Configure parameters and initialize forecast.")

# ===============================
# RUN FORECAST
# ===============================

else:

    payload = {
        "job_role": role,
        "industry": sector,
        "country": "Global",
        "year": 2026,
        "automation_risk_percent": float(auto),
        "skill_gap_index": float(gap),
        "salary_before_usd": 100000,
        "salary_after_usd": 90000,
        "salary_change_percent": -10.0,
        "skill_demand_growth_percent": 15.0,
        "remote_feasibility_score": 7.0,
        "ai_adoption_level": float(adoption),
        "education_requirement_level": 3
    }

    progress = st.progress(0)
    for i in range(100):
        time.sleep(0.01)
        progress.progress(i+1)

    try:
        response = requests.post(
            "https://ai-job-replacement.onrender.com/predict",
            json=payload,
            timeout=30
        )

        if response.status_code != 200:
            st.error(f"API returned error: {response.text}")
            st.stop()

        data = response.json()

        prediction = data["prediction"]
        probabilities = data["class_probabilities"]

        st.success(f"Prediction: {prediction}")
        st.write("Confidence:", f"{max(probabilities.values())*100:.2f}%")

        col1, col2 = st.columns(2)

        with col1:
            fig = go.Figure(data=[go.Pie(
                labels=list(probabilities.keys()),
                values=list(probabilities.values()),
                hole=0.6
            )])
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=[auto, gap*10, adoption*10, 60],
                theta=["Automation","Skill Gap","AI Adoption","Market Flux"],
                fill='toself'
            ))
            st.plotly_chart(radar, use_container_width=True)

    except Exception as e:
        st.error(f"API Connection Error: {e}")
