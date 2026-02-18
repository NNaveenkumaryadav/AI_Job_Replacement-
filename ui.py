import streamlit as st
import requests
import plotly.graph_objects as go
import time
import base64

# ===============================
# PAGE CONFIG
# ===============================

st.set_page_config(
    page_title="Job_Replacement_Detector",
    page_icon="🤖",
    layout="wide"
)

# ===============================
# LOAD LOCAL VIDEO
# ===============================

def get_video_base64(path):
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode()

video_base64 = get_video_base64("video.mp4")

# ===============================
# GLOBAL STYLING + VIDEO BACKGROUND
# ===============================

st.markdown(f"""
<style>

@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@500;700;900&family=Space+Grotesk:wght@400;600;700&display=swap');

/* Remove default background */
.stApp {{
    background: transparent !important;
}}

.block-container {{
    padding-top: 0rem !important;
    padding-bottom: 0rem !important;
}}

header {{
    background: transparent !important;
}}

[data-testid="stAppViewContainer"] {{
    background: transparent !important;
}}

/* VIDEO BACKGROUND */
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

/* Dark overlay */
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

/* Sidebar */
section[data-testid="stSidebar"] {{
    background: rgba(0,0,0,0.6) !important;
    backdrop-filter: blur(20px);
    border-right: 1px solid rgba(255,255,255,0.1);
}}

/* Hero Title */
.hero-title {{
    font-family: 'Orbitron', sans-serif;
    font-size: 4rem;
    font-weight: 900;
    letter-spacing: 3px;
    background: linear-gradient(90deg, #00f5ff, #ff00c8, #ffffff);
    background-size: 300%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    animation: shine 6s linear infinite;
}}

@keyframes shine {{
    0% {{ background-position: 0% }}
    100% {{ background-position: 300% }}
}}

/* Subtitle */
.hero-subtitle {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 1.1rem;
    font-weight: 500;
    letter-spacing: 1px;
    color: rgba(255,255,255,0.75);
    margin-top: -10px;
}}

/* Status Badge */
.status-badge {{
    font-family: 'Space Grotesk', sans-serif;
    font-size: 0.75rem;
    font-weight: 600;
    letter-spacing: 1px;
    padding: 6px 14px;
    border-radius: 20px;
    background: rgba(0,255,170,0.15);
    color: #00ffaa;
    border: 1px solid rgba(0,255,170,0.4);
    display: inline-block;
}}

/* Glass Cards */
.bento-card {{
    background: rgba(255,255,255,0.06);
    backdrop-filter: blur(25px);
    border-radius: 30px;
    padding: 2rem;
    border: 1px solid rgba(255,255,255,0.15);
    transition: 0.3s;
}}

.bento-card:hover {{
    transform: translateY(-6px);
    box-shadow: 0 0 40px rgba(0,255,255,0.3);
}}

/* Button */
.stButton>button {{
    background: linear-gradient(135deg, #00f5ff, #ff00c8) !important;
    border: none !important;
    color: white !important;
    font-weight: 700 !important;
    border-radius: 16px !important;
    padding: 1rem 2rem !important;
}}

</style>

<div class="video-container">
    <video autoplay loop muted playsinline>
        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
    </video>
</div>

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

col1, col2 = st.columns([5,1])

with col1:
    st.markdown('<div class="hero-title">Intelligence Radar</div>', unsafe_allow_html=True)
    st.markdown(
        f'<div class="hero-subtitle">Scanning displacement vectors for <b>{role}</b></div>',
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        '<div style="margin-top:30px; text-align:right;">'
        '<span class="status-badge">🟢 CORE ONLINE</span>'
        '</div>',
        unsafe_allow_html=True
    )

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
        response = requests.post("http://127.0.0.1:8000/predict", json=payload)
        data = response.json()

        prediction = data["prediction"]
        probabilities = data["class_probabilities"]

        if prediction == "High Risk":
            color = "#ff004c"
        elif prediction == "Moderate Risk":
            color = "#ffae00"
        else:
            color = "#00f5ff"

        k1, k2 = st.columns(2)

        with k1:
            st.markdown(f"""
            <div class="bento-card">
                <h3>Risk Verdict</h3>
                <h1 style="color:{color}; font-size:3rem;">{prediction}</h1>
            </div>
            """, unsafe_allow_html=True)

        with k2:
            st.markdown(f"""
            <div class="bento-card">
                <h3>Confidence</h3>
                <h1>{max(probabilities.values())*100:.1f}%</h1>
            </div>
            """, unsafe_allow_html=True)

        col_chart1, col_chart2 = st.columns(2)

        with col_chart1:
            fig = go.Figure(data=[go.Pie(
                labels=list(probabilities.keys()),
                values=list(probabilities.values()),
                hole=0.75
            )])
            fig.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(fig, use_container_width=True)

        with col_chart2:
            radar = go.Figure()
            radar.add_trace(go.Scatterpolar(
                r=[auto, gap*10, adoption*10, 60],
                theta=["Automation","Skill Gap","AI Adoption","Market Flux"],
                fill='toself'
            ))
            radar.update_layout(template="plotly_dark", paper_bgcolor="rgba(0,0,0,0)")
            st.plotly_chart(radar, use_container_width=True)

    except Exception as e:
        st.error(f"API Error: {e}")
