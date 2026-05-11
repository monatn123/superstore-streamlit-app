import streamlit as st
import base64
from pathlib import Path

st.set_page_config(page_title="About", layout="wide")

# =========================
# LOAD LOGO
# =========================
def get_base64_image(image_path):
    path = Path(image_path)
    if path.exists():
        with open(path, "rb") as img_file:
            return base64.b64encode(img_file.read()).decode()
    return None

logo_base64 = get_base64_image("lau-logo.jpg")

# =========================
# PRO MINIMAL SVG ICONS
# =========================
def icon(name):
    icons = {
        "institution": "M3 21h18M5 21V9l7-5 7 5v12M9 21v-6h6v6",
        "program": "M4 6l8-4 8 4-8 4-8-4zM4 12l8 4 8-4M4 18l8 4 8-4",
        "course": "M4 19.5A2.5 2.5 0 0 1 6.5 17H20M4 4.5A2.5 2.5 0 0 1 6.5 2H20v20H6.5A2.5 2.5 0 0 1 4 19.5z",
        "dataset": "M4 6c0-2 16-2 16 0v12c0 2-16 2-16 0V6zM4 6c0 2 16 2 16 0M4 12c0 2 16 2 16 0",
        "download": "M12 3v12M7 10l5 5 5-5M5 21h14",
        "clean": "M3 21l6-6M14 4l6 6-9 9H5v-6l9-9z",
        "analysis": "M4 19V5M4 19h16M8 16v-5M12 16V8M16 16v-9",
        "ml": "M9 3h6v3h3v6h3v6h-3v3h-6v-3H6v-6H3V6h6V3z",
        "insights": "M12 3v3M12 18v3M4.2 4.2l2.1 2.1M17.7 17.7l2.1 2.1M3 12h3M18 12h3M4.2 19.8l2.1-2.1M17.7 6.3l2.1-2.1",
        "geo": "M12 21s7-5.2 7-12a7 7 0 0 0-14 0c0 6.8 7 12 7 12zM12 11a2 2 0 1 0 0-4 2 2 0 0 0 0 4z",
        "revenue": "M12 1v22M17 5H9.5a3.5 3.5 0 0 0 0 7H14a3.5 3.5 0 0 1 0 7H6",
        "profit": "M4 19l6-6 4 4 6-10M16 7h4v4"
    }

    return f'<svg class="minimal-icon" viewBox="0 0 24 24" fill="none"><path d="{icons[name]}" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>'

# =========================
# CUSTOM CSS
# =========================
st.markdown("""
<style>
html, body, .stApp, .main {
    background: #ffffff !important;
    color: #0a1f44 !important;
}

.main {
    background: #ffffff !important;
}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 1.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
    max-width: 1450px;
}

.about-title {
    font-size: 2.2rem;
    font-weight: 800;
    color: white;
    margin-bottom: 0.25rem;
}

.about-subtitle {
    color: #b9c7d8;
    font-size: 1rem;
    margin-bottom: 1.2rem;
}

.glass-card {
    background: rgba(5, 18, 35, 0.72);
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 22px;
    padding: 14px 14px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.20);
    height: 205px;
    display: flex;
    flex-direction: column;
    align-items: center;
    justify-content: flex-start;
    text-align: center;
}

.glass-card h4 {
    font-size: 0.78rem;
    margin-bottom: 6px;
}

.glass-card h2 {
    font-size: 1.05rem;
    margin-bottom: 4px;
    line-height: 1.2;
    min-height: 38px;
}

.glass-card p {
    font-size: 0.82rem;
    margin-top: 2px;
    margin-bottom: 0;
}

.glass-icon {
    margin-bottom: 8px;
    width: 100%;
    display: flex;
    justify-content: flex-start;   /* 👈 move left */
    padding-left: 128px;             /* 👈 control how much */
    color: #0a1f44;
}

.minimal-icon {
    width: 24px;
    height: 24px;
    color: #0a1f44;
    display: inline-block;
    vertical-align: middle;
}

.section-card {
    background: rgba(5, 18, 35, 0.72);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 16px 16px;
    margin-top: 10px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.22);
}

.section-title {
    color: white;
    font-size: 1.8rem;
    font-weight: 800;
    margin-bottom: 20px;
}

.section-title .minimal-icon {
    width: 24px;
    height: 24px;
    margin-right: 8px;
    vertical-align: -3px;
}

.pipeline-wrap {
    display: flex;
    align-items: center;
    justify-content: space-between;
    gap: 10px;
    flex-wrap: wrap;
}

.pipeline-box {
    flex: 1;
    min-width: 0;
    background: linear-gradient(
        135deg,
        rgba(210, 230, 250, 0.85),
        rgba(180, 215, 245, 0.85)
    );    
    border: 1px solid rgba(255,255,255,0.10);
    border-radius: 18px;
    padding: 10px 8px;
    text-align: center;
    color: white;
    min-height: 88px;
}

.pipeline-box .emoji {
    margin-bottom: 8px;
    color: #8fd4ff;
}

.pipeline-box .emoji .minimal-icon {
    width: 24px;
    height: 24px;
}

.pipeline-box .title {
    font-size: 0.95rem;
    font-weight: 800;
    margin-bottom: 2px;
}

.pipeline-box .desc {
    font-size: 0.95rem;
    color: #d6e2ef;
}

.arrow {
    color: #68a8ff;
    font-size: 2rem;
    font-weight: 800;
    text-align: center;
}

.info-card {
    background: rgba(5, 18, 35, 0.72);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 24px;
    padding: 18px 18px;
    margin-top: 14px;
    min-height: 400px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.22);
}

.info-title {
    color: white;
    font-size: 1.35rem;
    font-weight: 800;
    margin-bottom: 12px;
}

.info-text {
    color: #d2deea;
    font-size: 0.95rem;
    line-height: 1.6;
    margin-bottom: 12px;
}

.mini-grid {
    display: grid;
    grid-template-columns: 1fr 1fr;
    gap: 14px;
}

.mini-card {
    padding: 12px 12px;
    border-radius: 16px;
}

.mini-card-title {
    color: #8fd4ff;
    font-size: 1rem;
    font-weight: 800;
    margin-bottom: 6px;
}

.mini-card-title .minimal-icon {
    width: 17px;
    height: 17px;
    margin-right: 6px;
    vertical-align: -3px;
}

.mini-card-text {
    color: #d5e0ea;
    font-size: 0.95rem;
}

.highlight-list {
    display: flex;
    flex-direction: column;
    gap: 8px;
    margin-top: 6px;
}

.highlight-item {
    background: linear-gradient(
        135deg,
        rgba(220, 240, 255, 0.9),
        rgba(200, 225, 250, 0.9)
    );
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 16px;
    padding: 10px 14px;
    color: #e6eef7;
    font-size: 0.88rem;
    font-weight: 600;
}

.logo-wrap {
    display: flex;
    justify-content: flex-start;
    margin-bottom: 6px;
    margin-top: -110px;
}

.logo-wrap img {
    max-height: 100px;
    width: 200px;
    border-radius: 0px;
}

.highlights-card {
    min-height: 400px;
    padding: 18px 18px;
}

@media (max-width: 900px) {
    .pipeline-wrap {
        flex-direction: column;
    }
    .arrow {
        transform: rotate(90deg);
    }
}
</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================
if logo_base64:
    st.markdown(f'<div class="logo-wrap"><img src="data:image/png;base64,{logo_base64}"></div>', unsafe_allow_html=True)

st.markdown('<div class="about-title">SuperStore Analytics App</div>', unsafe_allow_html=True)
st.markdown('<div class="about-subtitle">A KDD-based retail analytics application for descriptive, diagnostic, and advanced analytics using the Superstore Sales dataset.</div>', unsafe_allow_html=True)

# =========================
# TOP CARDS
# =========================
c1, c2, c3, c4 = st.columns(4)

with c1:
    st.markdown(f'<div class="glass-card"><div class="glass-icon">{icon("institution")}</div><h4>Institution</h4><h2>Lebanese American University</h2><p>Adnan Kassar School of Business</p></div>', unsafe_allow_html=True)

with c2:
    st.markdown(f'<div class="glass-card"><div class="glass-icon">{icon("program")}</div><h4>Program</h4><h2>MSDA</h2><p>Master of Science in Data Analytics</p></div>', unsafe_allow_html=True)

with c3:
    st.markdown(f'<div class="glass-card"><div class="glass-icon">{icon("course")}</div><h4>Course</h4><h2>DAN614</h2><p>Advanced Data Visualization</p></div>', unsafe_allow_html=True)

with c4:
    st.markdown(f'<div class="glass-card"><div class="glass-icon">{icon("dataset")}</div><h4>Dataset</h4><h2>Superstore Sales</h2><p>~10,000 transactional records</p></div>', unsafe_allow_html=True)

# =========================
# KDD PIPELINE
# =========================
st.markdown(
f'<div class="section-card">'
f'<div class="section-title">{icon("analysis")}KDD Pipeline Overview</div>'
f'<div class="pipeline-wrap">'
f'<div class="pipeline-box"><div class="emoji">{icon("download")}</div><div class="title">Data Collection</div><div class="desc">File Upload · Google Sheets</div></div>'
f'<div class="arrow">→</div>'
f'<div class="pipeline-box"><div class="emoji">{icon("clean")}</div><div class="title">Data Cleaning</div><div class="desc">Impute · Outliers · Validate</div></div>'
f'<div class="arrow">→</div>'
f'<div class="pipeline-box"><div class="emoji">{icon("analysis")}</div><div class="title">Analysis</div><div class="desc">Sales · Profit · Quantity</div></div>'
f'<div class="arrow">→</div>'
f'<div class="pipeline-box"><div class="emoji">{icon("ml")}</div><div class="title">ML Modeling</div><div class="desc">Supervised · Unsupervised</div></div>'
f'<div class="arrow">→</div>'
f'<div class="pipeline-box"><div class="emoji">{icon("insights")}</div><div class="title">Insights</div><div class="desc">Visual · Interactive</div></div>'
f'</div></div>',
unsafe_allow_html=True
)

# =========================
# BOTTOM CARDS
# =========================
left, right = st.columns([1.75, 0.85])

with left:
    st.markdown(
    f'<div class="info-card">'
    f'<div class="info-title">About the Dataset</div>'
    f'<div class="info-text">The <b>Superstore Sales Dataset</b> is a retail analytics benchmark containing roughly <b>10,000 transactional records</b> spanning customer orders, product details, geographic data, and financial metrics such as revenue, profit, and quantity sold.</div>'
    f'<div class="mini-grid">'
    f'<div class="mini-card"><div class="mini-card-title">{icon("dataset")}Sheets</div><div class="mini-card-text">Orders, People, and Returns tables are integrated for full business analysis.</div></div>'
    f'<div class="mini-card"><div class="mini-card-title">{icon("geo")}Geography</div><div class="mini-card-text">Regional and state-level information supports location-based insights.</div></div>'
    f'<div class="mini-card"><div class="mini-card-title">{icon("revenue")}Revenue</div><div class="mini-card-text">Sales values help evaluate category, customer, and product performance.</div></div>'
    f'<div class="mini-card"><div class="mini-card-title">{icon("profit")}Profitability</div><div class="mini-card-text">Profit measures highlight operational efficiency and business value.</div></div>'
    f'</div></div>',
    unsafe_allow_html=True
    )

with right:
    st.markdown(
    '<div class="info-card highlights-card">'
    '<div class="info-title"> App Highlights</div>'
    '<div class="highlight-list">'
    '<div class="highlight-item"> Google Sheets live connection</div>'
    '<div class="highlight-item"> Interactive data cleaning pipeline</div>'
    '<div class="highlight-item"> Executive sales dashboards</div>'
    '<div class="highlight-item"> Products & operations insights</div>'
    '<div class="highlight-item"> Supervised machine learning models</div>'
    '<div class="highlight-item"> PCA and advanced analytics</div>'
    '</div></div>',
    unsafe_allow_html=True
    )
