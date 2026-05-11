import streamlit as st

st.set_page_config(
    page_title="SuperStore Analytics App",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# REGISTER PAGES
# =========================
about = st.Page("About.py", title="About")
data = st.Page("Data_Collection_&_Cleaning.py", title="Data Collection & Cleaning")
executive = st.Page("Executive_Overview.py", title="Executive Sales Overview")
product = st.Page("Product_&_Operations_Insights.py", title="Products & Operations Insights")
ml = st.Page("ML_Analytics.py", title="ML & Advanced Analytics")
return_prediction_page = st.Page("Return_Prediction.py", title="Return Prediction")

# =========================
# NAVIGATION
# =========================
pg = st.navigation(
    [about, data, executive, product, ml, return_prediction_page],
    position="hidden"
)

# =========================
# STYLING
# =========================
st.markdown(
    """
    <style>
    /* ── Global background ── */
    html, body,
    [data-testid="stAppViewContainer"],
    [data-testid="stMain"],
    .main {
        background-color: #ffffff !important;
        color: #1a1a2e !important;
    }

    .block-container {
        padding-top: 1rem;
        padding-left: 1.2rem;
        padding-right: 1.2rem;
        padding-bottom: 0.8rem;
        background-color: #ffffff !important;
    }

    header[data-testid="stHeader"] {
        display: none !important;
    }

    [data-testid="stToolbar"] {
        display: none !important;
    }

    [data-testid="stDecoration"] {
        display: none !important;
    }

    [data-testid="stStatusWidget"] {
        display: none !important;
    }

    [data-testid="stAppViewContainer"] {
        margin-top: -1.2rem;
    }

    .filter-wrap {
        margin-top: -1.2rem;
        margin-bottom: -1.2rem;
        transform: translateY(8px);
    }
    div[data-baseweb="select"] > div {
        background-color: #dbeeff !important;
        border-color: #93c5e8 !important;
        color: #0a1f44 !important;   /* ← navy */
    }

    div[data-testid="stSelectbox"] {
        transform: translateY(8px) !important;
    }

    .filter-wrap div[data-baseweb="select"] {
        width: 70% !important;
        min-width: 70% !important;
        max-width: 70% !important;
    }

    /* ── Selectbox / dropdown styling ── */
    div[data-baseweb="select"] > div {
        background-color: #dbeeff !important;
        border-color: #93c5e8 !important;
        color: #1a1a2e !important;
    }

    div[data-baseweb="select"] svg {
        fill: #1a1a2e !important;
    }

    /* ── Top nav buttons ── */
    div.stButton > button {
        width: 100%;
        min-height: 58px;
        height: 58px;

        border-radius: 12px;
        border: 1px solid #93c5e8;
        background-color: #dbeeff;
        color: #0a1f44;

        font-size: 10.5px;
        font-weight: 500;
        line-height: 1.15;

        padding: 0px 10px;

        display: flex !important;
        align-items: center !important;
        justify-content: center !important;
        text-align: center !important;

        white-space: normal;
        overflow-wrap: anywhere;
    }

    div.stButton > button:hover {
        border-color: #5aaede;
        background-color: #c2e0f8;
        color: #0a1f44;
        transform: none !important;
        margin-top: 0px !important;
        top: 0px !important;
    }

    div.stButton > button:focus {
        outline: none !important;
        box-shadow: none !important;
        color: #1a1a2e !important;
    }
    /* ── Containers: very light blue ── */
    [data-testid="stMetric"],
    .section-card,
    .info-card,
    .glass-card,
    .pipeline-box {
        background-color: #eaf4ff !important;   /* very light blue */
        border: 1px solid #cfe5fb !important;
        color: #0a1f44 !important;  /* navy text */
    }
    /* ── All text navy ── */
    h1, h2, h3, h4, h5, h6,
    p, span, div, label {
       color: #0a1f44 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# TOP NAV
# =========================
left_space, nav_group = st.columns([2.75, 4.25])

with left_space:
    st.empty()

with nav_group:
    nav1, nav2, nav3, nav4, nav5, nav6 = st.columns(
        [0.95, 1.80, 1.80, 2.05, 1.75, 1.65],
        gap="small"
    )

    def nav_button(label, page_file, is_active, key):
        clicked = st.button(label, key=key)

        if is_active:
            st.markdown(
                f"""
                <style>
                .st-key-{key} button {{
                    background-color: #5aaede !important;
                    border: 1px solid #2e8fbf !important;
                    color: #ffffff !important;
                    font-weight: 600 !important;
                    padding: 0px 10px !important;
                    height: 58px !important;
                    min-height: 58px !important;
                    transform: none !important;
                    margin-top: 0px !important;
                    top: 0px !important;
                }}
                </style>
                """,
                unsafe_allow_html=True
            )

        if clicked:
            st.switch_page(page_file)

    with nav1:
        nav_button("About", "About.py", pg.title == "About", "nav_about")

    with nav2:
        nav_button(
            "Data Collection & Cleaning",
            "Data_Collection_&_Cleaning.py",
            pg.title == "Data Collection & Cleaning",
            "nav_data"
        )

    with nav3:
        nav_button(
            "Executive Sales Overview",
            "Executive_Overview.py",
            pg.title == "Executive Sales Overview",
            "nav_exec"
        )

    with nav4:
        nav_button(
            "Products & Operations Insights",
            "Product_&_Operations_Insights.py",
            pg.title == "Products & Operations Insights",
            "nav_product"
        )

    with nav5:
        nav_button(
            "ML & Advanced Analytics",
            "ML_Analytics.py",
            pg.title == "ML & Advanced Analytics",
            "nav_ml"
        )

    with nav6:
        nav_button(
            "Return Prediction",
            "Return_Prediction.py",
            pg.title == "Return Prediction",
            "nav_return"
        )

# =========================
# FILTERS UNDER NAV
# =========================
if pg.title not in [
    "About",
    "Data Collection & Cleaning",
    "ML & Advanced Analytics",
    "Return Prediction"
]:
    st.markdown('<div class="filter-wrap">', unsafe_allow_html=True)

    left_filter_space, filters_group = st.columns([2.2, 3.8])

    with left_filter_space:
        st.empty()

    with filters_group:
        left_space, f1, f2, f3 = st.columns([0.8, 1, 1, 1], gap="small")

        with f1:
            st.selectbox(
                "Region",
                ["All", "Central", "East", "South", "West"],
                key="global_region"
            )

        with f2:
            st.selectbox(
                "Category",
                ["All", "Furniture", "Office Supplies", "Technology"],
                key="global_category"
            )

        with f3:
            st.selectbox(
                "Segment",
                ["All", "Consumer", "Corporate", "Home Office"],
                key="global_segment"
            )

    st.markdown("</div>", unsafe_allow_html=True)

if pg.title == "ML & Advanced Analytics":
    st.markdown("<div style='height: 55px;'></div>", unsafe_allow_html=True)

# =========================
# RUN PAGE
# =========================
pg.run()
