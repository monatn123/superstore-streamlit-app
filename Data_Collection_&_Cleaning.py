import streamlit as st
import pandas as pd
import datetime
import re
import io
import plotly.graph_objects as go
from sklearn.experimental import enable_iterative_imputer
from sklearn.impute import IterativeImputer

# =========================
# PAGE STYLE
# =========================
st.markdown("""
<style>
html, body, .stApp, .main {
    background: #ffffff !important;
}

.main {
    background: #ffffff !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-bottom: 1.5rem !important;
    padding-left: 0.7rem !important;
    padding-right: 0.7rem !important;
    max-width: 1420px;
}

div[data-testid="stVerticalBlock"] {
    gap: 1rem !important;
}

div[data-testid="stHorizontalBlock"] {
    gap: 1.1rem !important;
}

.dashboard-title {
    margin-top: -0.3rem;
    margin-bottom: 1rem;
    padding: 18px 26px;
    border: 1px solid #b8d4f0;
    border-radius: 22px;
    background: linear-gradient(135deg, #ddeeff, #c8e0f8);
    box-shadow: 0 8px 24px rgba(10,40,100,0.10);
}

.dashboard-title h1 {
    margin: 0;
    color: #0a2550;
    font-size: 34px;
    font-weight: 850;
    letter-spacing: -0.4px;
    line-height: 1.05;
}

.dashboard-title p {
    margin: 8px 0 0 0;
    color: #1a3a70;
    font-size: 15px;
    line-height: 1.45;
}

.section-heading {
    color: #0a2550;
    font-weight: 800;
    font-size: 21px;
    margin: 0 0 0.65rem 0;
    line-height: 1.2;
    font-family: sans-serif;
}

.sub-heading {
    color: #1a3a70;
    font-size: 15px;
    font-weight: 650;
    margin-bottom: 0.6rem;
}

.mini-note {
    background: #eaf3fd;
    border: 1px solid #b8d4f0;
    color: #0a2550;
    border-radius: 14px;
    padding: 12px 14px;
    font-size: 14px;
    line-height: 1.55;
    margin-top: 6px;
    margin-bottom: 10px;
}

.small-sheet-pill {
    display: inline-block;
    background: #d0e8fa;
    border: 1px solid #9ec8ef;
    border-radius: 12px;
    padding: 8px 13px;
    color: #0a2550;
    font-size: 14px;
    font-weight: 650;
    margin-right: 7px;
    margin-top: 6px;
}

.step-pill {
    display: inline-block;
    background: #d0e8fa;
    border: 1px solid #9ec8ef;
    color: #0a2550;
    border-radius: 999px;
    padding: 6px 12px;
    font-size: 13px;
    font-weight: 650;
    margin-bottom: 0.25rem;
}
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #e8f4fd !important;
    border: 1px solid #b8d4f0 !important;
    border-radius: 20px !important;
    box-shadow: 0 6px 18px rgba(10,40,100,0.08) !important;
    padding: 10px !important;
}

.st-key-source_box,
.st-key-validation_box,
.st-key-missing_box,
.st-key-outlier_box,
.st-key-duplicate_box,
.st-key-category_box,
.st-key-format_box,
.st-key-preview_box,
.st-key-final_save_box,
.st-key-outlier_impact_box_0,
.st-key-outlier_impact_box_1 {
    background-color: #e8f4fd !important;
    border-radius: 20px !important;
}
.st-key-outlier_box {
    height: 200px !important;
}
/* Keep normal text navy */
.section-heading,
.sub-heading,
.mini-note,
.step-pill,
label,
p {
    color: #0a2550 !important;
}

/* Upload label only → NAVY */
div[data-testid="stFileUploader"] > label,
div[data-testid="stFileUploader"] > label * {
    color: #0a2550 !important;
}

/* Label "Upload your Superstore file" → NAVY */
div[data-testid="stFileUploader"] label {
    color: #0a2550 !important;
}


/* Tabs */
button[data-baseweb="tab"] {
    background: #d0e8fa !important;
    color: #0a2550 !important;
    border-radius: 14px 14px 0 0 !important;
    padding: 11px 18px !important;
    margin-right: 6px !important;
    border: 1px solid #b8d4f0 !important;
    font-weight: 750 !important;
}
button[data-baseweb="tab"][aria-selected="true"],
button[data-baseweb="tab"][aria-selected="true"] *,
button[data-baseweb="tab"][aria-selected="true"] p,
button[data-baseweb="tab"][aria-selected="true"] span,
button[data-baseweb="tab"][aria-selected="true"] div {
    background: #0a2550 !important;
    color: white !important;
    border-color: #0a2550 !important;
}

/* Alerts */
div[data-testid="stAlert"] {
    padding: 0.62rem 0.9rem !important;
    margin-top: 0.22rem !important;
    margin-bottom: 0.35rem !important;
    border-radius: 14px !important;
}

/* Inputs */
div[data-testid="stRadio"],
div[data-testid="stFileUploader"],
div[data-testid="stSelectbox"],
div[data-testid="stTextInput"] {
    margin-top: 0.25rem !important;
    margin-bottom: 0.5rem !important;
}

label, p, span {
    line-height: 1.42 !important;
}


/* File uploader browse/upload button — white text */
div[data-testid="stFileUploader"] button,
div[data-testid="stFileUploader"] button * {
    color: white !important;
}

/* Uploaded file name + size — white text */
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *,
div[data-testid="stFileUploader"] [class*="uploadedFile"],
div[data-testid="stFileUploader"] [class*="uploadedFile"] *,
div[data-testid="stFileUploader"] [class*="UploadedFile"],
div[data-testid="stFileUploader"] [class*="UploadedFile"] *,
section[data-testid="stFileUploaderDropzone"] ~ div *,
div[data-testid="stFileUploader"] > div > div > div > div,
div[data-testid="stFileUploader"] > div > div > div > div * {
    color: white !important;
}

/* Expander: always light blue background, never black */
[data-testid="stExpander"],
[data-testid="stExpander"] summary,
[data-testid="stExpander"] summary:hover,
[data-testid="stExpander"] summary:focus,
[data-testid="stExpander"] summary:active,
details[data-testid="stExpander"],
details[data-testid="stExpander"] > summary {
    background: #eaf3fd !important;
    background-color: #eaf3fd !important;
    border: 1px solid #b8d4f0 !important;
    border-radius: 15px !important;
}

/* Expander header text — always navy */
[data-testid="stExpander"] summary *,
[data-testid="stExpander"] summary span,
[data-testid="stExpander"] summary p,
[data-testid="stExpander"] summary div,
[data-testid="stExpander"] [data-testid="stExpanderToggleIcon"] {
    color: #0a2550 !important;
}

/* Selectbox */
div[data-baseweb="select"] > div {
    background-color: #eaf3fd !important;
    color: #0a2550 !important;
    border: 1px solid #b8d4f0 !important;
    border-radius: 12px !important;
}
div[data-baseweb="select"] span {
    color: #0a2550 !important;
}
div[data-baseweb="popover"],
div[data-baseweb="popover"] > div,
div[data-baseweb="menu"],
ul[role="listbox"] {
    background-color: #eaf3fd !important;
    border: 1px solid #b8d4f0 !important;
    border-radius: 10px !important;
}
li[role="option"], div[role="option"] {
    background-color: #eaf3fd !important;
    color: #0a2550 !important;
}
li[role="option"] *, div[role="option"] * {
    color: #0a2550 !important;
}
li[role="option"]:hover, div[role="option"]:hover {
    background-color: #c8e0f8 !important;
}
li[aria-selected="true"], div[aria-selected="true"] {
    background-color: #b8d4f0 !important;
}

/* Segmented control */
div[data-baseweb="button-group"] {
    background: #d0e8fa !important;
    border: 1px solid #b8d4f0 !important;
    border-radius: 14px !important;
    padding: 5px !important;
    gap: 6px !important;
}
div[data-baseweb="button-group"] button {
    background: #eaf3fd !important;
    color: #0a2550 !important;
    border: 1px solid #b8d4f0 !important;
    border-radius: 11px !important;
    padding: 9px 17px !important;
    font-weight: 700 !important;
}
div[data-baseweb="button-group"] button[aria-pressed="true"] {
    background: #0a2550 !important;
    color: white !important;
    border: 1px solid #0a2550 !important;
}
div[data-baseweb="button-group"] button[aria-pressed="true"] * {
    color: white !important;
}
div[data-baseweb="button-group"] button:hover {
    background: #c8e0f8 !important;
}
/* Normal text → NAVY */
.section-heading,
.sub-heading,
.mini-note,
.step-pill,
label,
p {
    color: #0a2550 !important;
}

/* Uploaded file name → WHITE (strong override) */
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"],
div[data-testid="stFileUploader"] [data-testid="stFileUploaderFile"] *,
div[data-testid="stFileUploader"] div[class*="uploadedFile"],
div[data-testid="stFileUploader"] div[class*="uploadedFile"] * {
    color: white !important;
}
div[data-testid="stFileUploader"] button {
    background: #eaf3fd !important;   /* light blue */
    border: 1px solid #b8d4f0 !important;
    border-radius: 10px !important;
    color: #0a2550 !important;
}

div[data-testid="stFileUploader"] button:hover {
    background: #d6eafc !important;
}
/* ===== Upload dropzone (big box) → LIGHT GREY ===== */
section[data-testid="stFileUploaderDropzone"],
section[data-testid="stFileUploaderDropzone"] > div,
section[data-testid="stFileUploaderDropzone"] > div > div {
    background: #f5f7fa !important;   /* light grey (same as charts) */
    border: 1px solid #d0d7e2 !important;
    border-radius: 14px !important;
}

/* FORCE upload button text → NAVY */
div[data-testid="stFileUploader"] button,
div[data-testid="stFileUploader"] button * {
    color: #0a2550 !important;
}
/* Upload box light grey */
section[data-testid="stFileUploaderDropzone"] {
    background: #f5f7fa !important;
    border: 1px solid #d0d7e2 !important;
    border-radius: 14px !important;
}

/* Default upload text navy */
section[data-testid="stFileUploaderDropzone"] * {
    color: #0a2550 !important;
}

/* Upload button navy text */
section[data-testid="stFileUploaderDropzone"] button,
section[data-testid="stFileUploaderDropzone"] button * {
    color: #0a2550 !important;
}

/* Uploaded file dark pill text forced white */
section[data-testid="stFileUploaderDropzone"] div[title],
section[data-testid="stFileUploaderDropzone"] div[title] *,
section[data-testid="stFileUploaderDropzone"] div[aria-label],
section[data-testid="stFileUploaderDropzone"] div[aria-label] * {
    color: white !important;
}
/* ===== Uploaded file icons → NAVY ===== */

/* Target all icons inside uploaded file pill */
div[data-testid="stFileUploader"] svg {
    fill: #0a2550 !important;
    stroke: #0a2550 !important;
}

/* Specifically the remove (X) button */
div[data-testid="stFileUploader"] button[aria-label="Remove file"] svg {
    fill: #0a2550 !important;
    stroke: #0a2550 !important;
}

/* Left file icon (document icon) */
div[data-testid="stFileUploader"] div svg {
    fill: #0a2550 !important;
    stroke: #0a2550 !important;
}

/* Optional: make hover slightly darker */
div[data-testid="stFileUploader"] button:hover svg {
    fill: #081b3a !important;
    stroke: #081b3a !important;
}
.st-key-outlier_box div[data-testid="stSelectbox"] {
    margin-top: -12px !important;
}
.st-key-outlier_box div[data-testid="stAlert"] {
    margin-top: -6px !important;
}
.st-key-outlier_box div[data-testid="stPlotlyChart"] {
    margin-top: -6px !important;
}

</style>
""", unsafe_allow_html=True)

# JS to force white text on uploaded file name (Streamlit renders it dynamically)


# =========================
# PAGE TITLE
# =========================
st.markdown(
    """
    <div style="
        transform: translateY(-100px);
        border: 2px solid #b8d4f0;
        border-radius: 14px;
        padding: 14px 28px;
        background: #eaf3fd;
        box-shadow: 0 4px 14px rgba(10,40,100,0.10);
        display: inline-block;
        margin-bottom: 10px;
    ">
        <h1 style="
            margin:0;
            color:#0a2550;
            font-size:34px;
            font-weight:800;
        ">
            Data Collection & Cleaning
        </h1>
    </div>
    """,
    unsafe_allow_html=True
)
# =========================
# HELPERS
# =========================
def validate_sheet(df, required_cols, sheet_name):
    missing_cols = [col for col in required_cols if col not in df.columns]
    if missing_cols:
        st.error(f"{sheet_name} sheet is missing columns: {missing_cols}")
        return False
    return True


def extract_sheet_id(url):
    match = re.search(r"/d/([a-zA-Z0-9-_]+)", url)
    return match.group(1) if match else None


def fix_superstore_dates(df):
    df = df.copy()
    for col in ["Order Date", "Ship Date"]:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors="coerce")
    return df


def save_uploaded_file_to_session(uploaded_file):
    st.session_state["uploaded_file_name"] = uploaded_file.name
    st.session_state["uploaded_file_bytes"] = uploaded_file.getvalue()


def get_uploaded_file_from_session():
    if "uploaded_file_bytes" in st.session_state and "uploaded_file_name" in st.session_state:
        return io.BytesIO(st.session_state["uploaded_file_bytes"]), st.session_state["uploaded_file_name"]
    return None, None


def navy_table(df, height=160, key=None):
    fig = go.Figure(
        data=[
            go.Table(
                header=dict(
                    values=list(df.columns),
                    fill_color="#0a2550",
                    font=dict(color="#ffffff", size=13),
                    align="left",
                    line_color="#b8d4f0",
                    height=30
                ),
                cells=dict(
                    values=[df[col].tolist() for col in df.columns],
                    fill_color="#eaf3fd",
                    font=dict(color="#0a2550", size=13),
                    align="left",
                    line_color="#c8e0f8",
                    height=30
                )
            )
        ]
    )
    fig.update_layout(
        height=height,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)"
    )
    st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False}, key=key)

def render_metadata_sidebar():
    if st.session_state.get("data_ready", False):
        with st.sidebar:
            st.markdown(
                f"""
                <div style="
                    background-color:#eaf3fd;
                    border:1px solid #b8d4f0;
                    border-radius:14px;
                    padding:14px;
                    color:#0a2550;
                    line-height:1.6;
                ">
                    <h4 style="margin-top:0; margin-bottom:10px; color:#0a2550;">Sheet Metadata</h4>
                    <b>Name:</b> {st.session_state.get("loaded_sheet_name", "N/A")}<br>
                    <b>Last Updated:</b> {st.session_state.get("loaded_at", "N/A")}<br>
                    <b>Row Count:</b> {st.session_state.get("loaded_row_count", "N/A")}
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# REQUIRED COLUMNS
# =========================
orders_columns = [
    "Row ID", "Order ID", "Order Date", "Ship Date", "Ship Mode",
    "Customer ID", "Customer Name", "Segment", "Country/Region",
    "City", "State", "Postal Code", "Region", "Product ID",
    "Category", "Sub-Category", "Product Name", "Quantity",
    "Total Revenue", "Total Profit"
]
people_columns = ["Person", "Region"]
returns_columns = ["Returned", "Order ID"]

# =========================
# SESSION DEFAULTS
# =========================
if "data_source_choice" not in st.session_state:
    st.session_state["data_source_choice"] = "Upload File"
if "google_url_value" not in st.session_state:
    st.session_state["google_url_value"] = ""
if "imputation_method" not in st.session_state:
    st.session_state["imputation_method"] = "None"
if "outlier_method" not in st.session_state:
    st.session_state["outlier_method"] = "None"

# =========================
# PAGE INSIDE PAGE TABS
# =========================
tab_source, tab_cleaning, tab_impact = st.tabs([
    "1  Data Source & Validation",
    "2  Cleaning Controls",
    "3  Impact Summary & Preview"
])

# =========================
# TAB 1: DATA SOURCE INPUT
# =========================
with tab_source:
    source_col, validation_col = st.columns([1.05, 0.95], gap="large")

    with source_col:
        with st.container(border=True, key="source_box"):
            st.markdown('<span class="step-pill">Step 1</span>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Select Data Source</div>', unsafe_allow_html=True)
            st.markdown('<div class="sub-heading">Choose how the Superstore dataset should be loaded.</div>', unsafe_allow_html=True)

            data_source = st.segmented_control(
                "Choose input method:",
                options=["Upload File", "Google Sheets"],
                key="data_source_choice",
                label_visibility="collapsed"
            )

            uploaded_file = None
            if data_source == "Upload File":
                uploaded_file = st.file_uploader(
                    "Upload your Superstore file",
                    type=["csv", "xlsx", "xls"],
                    key="superstore_uploader"
                )
                if uploaded_file is not None:
                    save_uploaded_file_to_session(uploaded_file)
            else:
                st.text_input(
                    "Paste Google Sheets link here",
                    key="google_url_value"
                )

            source_status_area = st.empty()
            sheets_area = st.empty()

    with validation_col:
        with st.container(border=True, key="validation_box"):
            st.markdown('<span class="step-pill">Step 2</span>', unsafe_allow_html=True)
            st.markdown('<div class="section-heading">Column Validation</div>', unsafe_allow_html=True)
            st.markdown(
                """
                <div class="mini-note">
                    This step checks whether the required Orders, People, and Returns columns are available before the dataset moves to cleaning.
                </div>
                """,
                unsafe_allow_html=True
            )
            validation_status_area = st.empty()
else_placeholder_uploaded_file = None

# Make variables available outside tab block even after reruns
uploaded_file = locals().get("uploaded_file", None)
data_source = st.session_state.get("data_source_choice", "Upload File")
file_from_session, file_name_from_session = get_uploaded_file_from_session()

should_load_from_upload = (
    data_source == "Upload File"
    and (uploaded_file is not None or file_from_session is not None)
)
should_load_from_google = (
    data_source == "Google Sheets"
    and st.session_state.get("google_url_value", "").strip() != ""
)

# =========================
# LOAD DATA + CLEANING LOGIC
# =========================
if should_load_from_upload or should_load_from_google or st.session_state.get("data_ready", False):
    try:
        people_df = None
        returns_df = None
        excel_sheet_names = []
        file_name = st.session_state.get("loaded_sheet_name", "Uploaded file")

        if st.session_state.get("data_ready", False) and not (should_load_from_upload or should_load_from_google):
            orders_df = st.session_state["orders_raw_df"].copy()
            people_df = st.session_state.get("people_df")
            returns_df = st.session_state.get("returns_df")
            load_message = "Data already loaded ✅"
            excel_sheet_names = ["Orders", "People", "Returns"] if people_df is not None and returns_df is not None else []

        elif data_source == "Upload File":
            if uploaded_file is not None:
                file_obj = io.BytesIO(uploaded_file.getvalue())
                file_name = uploaded_file.name
            else:
                file_obj = io.BytesIO(st.session_state["uploaded_file_bytes"])
                file_name = st.session_state["uploaded_file_name"]

            if file_name.endswith(".csv"):
                orders_df = pd.read_csv(file_obj)
                orders_df.columns = orders_df.columns.str.strip()
                load_message = "CSV file loaded successfully ✅"
                st.session_state["loaded_source_type"] = "Upload File"
            elif file_name.endswith(".xlsx") or file_name.endswith(".xls"):
                excel_file = pd.ExcelFile(file_obj)
                excel_sheet_names = excel_file.sheet_names

                file_obj.seek(0)
                orders_df = pd.read_excel(file_obj, sheet_name="Orders")
                file_obj.seek(0)
                people_df = pd.read_excel(file_obj, sheet_name="People")
                file_obj.seek(0)
                returns_df = pd.read_excel(file_obj, sheet_name="Returns")

                orders_df.columns = orders_df.columns.str.strip()
                people_df.columns = people_df.columns.str.strip()
                returns_df.columns = returns_df.columns.str.strip()

                load_message = "Excel file loaded successfully ✅"
                st.session_state["loaded_source_type"] = "Upload File"
            else:
                st.error("Unsupported file type")
                st.stop()

        elif data_source == "Google Sheets":
            google_url = st.session_state.get("google_url_value", "").strip()
            sheet_id = extract_sheet_id(google_url)
            if not sheet_id:
                st.error("Invalid Google Sheets link ❌")
                st.stop()

            excel_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=xlsx"
            excel_file = pd.ExcelFile(excel_url)

            orders_df = pd.read_excel(excel_file, sheet_name="Orders")
            people_df = pd.read_excel(excel_file, sheet_name="People")
            returns_df = pd.read_excel(excel_file, sheet_name="Returns")

            orders_df.columns = orders_df.columns.str.strip()
            people_df.columns = people_df.columns.str.strip()
            returns_df.columns = returns_df.columns.str.strip()

            excel_sheet_names = ["Orders", "People", "Returns"]
            load_message = "Google Sheets loaded successfully ✅"
            file_name = "Google Sheets - Superstore"
            st.session_state["loaded_source_type"] = "Google Sheets"
            st.session_state["loaded_google_url"] = google_url

        orders_df = fix_superstore_dates(orders_df)

        st.session_state["loaded_sheet_name"] = file_name if data_source == "Upload File" else "Google Sheets - Superstore"
        st.session_state["loaded_row_count"] = orders_df.shape[0]
        st.session_state["loaded_at"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        orders_valid = validate_sheet(orders_df, orders_columns, "Orders")
        if people_df is not None and returns_df is not None:
            people_valid = validate_sheet(people_df, people_columns, "People")
            returns_valid = validate_sheet(returns_df, returns_columns, "Returns")
        else:
            people_valid = True
            returns_valid = True

        if not (orders_valid and people_valid and returns_valid):
            st.stop()

        # Render notifications in Tab 1 placeholders
        with source_status_area.container():
            st.success(load_message)
        with sheets_area.container():
            with st.expander("Available Sheets", expanded=False):
                if excel_sheet_names:
                    for sheet in excel_sheet_names:
                        st.markdown(f'<span class="small-sheet-pill">{sheet}</span>', unsafe_allow_html=True)
                else:
                    st.markdown('<span class="small-sheet-pill">Single-sheet source detected</span>', unsafe_allow_html=True)
        with validation_status_area.container():
            st.success("Orders sheet is valid ✅")
            if people_df is not None and returns_df is not None:
                st.success("People sheet is valid ✅")
                st.success("Returns sheet is valid ✅")
            else:
                st.info("Single-sheet source detected")

        # Prepare data
        missing_values = orders_df.isnull().sum()
        missing_values = missing_values[missing_values > 0]
        df_clean = orders_df.copy()

        # =========================
        # TAB 2: CLEANING CONTROLS
        # =========================
        with tab_cleaning:
            st.markdown('<div class="sub-heading">Each cleaning operation is placed in its own card to make the page easier to read and defend.</div>', unsafe_allow_html=True)

            top_clean_left, top_clean_right = st.columns([1, 1], gap="large")

            with top_clean_left:
                with st.container(border=True, key="missing_box"):
                    st.markdown('<span class="step-pill">Step 3</span>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Missing Values & Imputation</div>', unsafe_allow_html=True)

                    if missing_values.empty:
                        st.success("No missing values found ✅")
                    else:
                        st.warning("Missing values detected ⚠️")
                        missing_df = missing_values.reset_index()
                        missing_df.columns = ["Column", "Missing Count"]
                        navy_table(missing_df, height=30 + len(missing_df) * 20, key="missing_values_table")

                    method = st.selectbox(
                        "Choose imputation method",
                        ["None", "Mean", "Median", "Mode", "MICE"],
                        key="imputation_method"
                    )

                    st.markdown(
                        """
                        <div class="mini-note">
                            MICE is an advanced iterative method for imputing missing numeric values. Mean, median, and mode are simpler rule-based methods.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    if method != "None":
                        if method in ["Mean", "Median", "Mode"]:
                            for col in df_clean.columns:
                                if df_clean[col].isnull().sum() > 0:
                                    if method == "Mean" and pd.api.types.is_numeric_dtype(df_clean[col]):
                                        df_clean[col] = df_clean[col].fillna(df_clean[col].mean())
                                    elif method == "Median" and pd.api.types.is_numeric_dtype(df_clean[col]):
                                        df_clean[col] = df_clean[col].fillna(df_clean[col].median())
                                    elif method == "Mode":
                                        mode_series = df_clean[col].mode()
                                        if not mode_series.empty:
                                            df_clean[col] = df_clean[col].fillna(mode_series[0])
                            st.success(f"Missing values handled using {method} ✅")
                        elif method == "MICE":
                            numeric_cols_mice = df_clean.select_dtypes(include=["number"]).columns.tolist()
                            non_numeric_cols = df_clean.select_dtypes(exclude=["number"]).columns.tolist()

                            for col in non_numeric_cols:
                                if df_clean[col].isnull().sum() > 0:
                                    mode_series = df_clean[col].mode()
                                    if not mode_series.empty:
                                        df_clean[col] = df_clean[col].fillna(mode_series[0])

                            if len(numeric_cols_mice) > 0:
                                imputer = IterativeImputer(random_state=42)
                                df_clean[numeric_cols_mice] = imputer.fit_transform(df_clean[numeric_cols_mice])
                            st.success("Missing values handled using MICE for numeric columns ✅")

            with top_clean_right:
                with st.container(border=True, key="outlier_box"):
                    st.markdown('<span class="step-pill">Step 4</span>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Outlier Handling</div>', unsafe_allow_html=True)
                    detection_method = st.selectbox(
                        "Choose outlier detection method",
                        ["IQR", "Z-Score"],
                        key="detection_method"
                    )
                    outlier_method = st.selectbox(
                        "Choose outlier handling method",
                        ["None", "Flag Only", "Cap at Bounds", "Remove Rows"],
                        key="outlier_method"
                    )

                    base_df = df_clean.copy()
                    outlier_df = base_df.copy()
                    numeric_cols_for_outliers = ["Total Revenue", "Total Profit"]
                    outlier_summary_rows = []

                    if outlier_method == "None":
                        st.info("No outlier treatment selected.")

                    for col in numeric_cols_for_outliers:
                        if col in base_df.columns:
                            if detection_method == "IQR":
                                Q1 = base_df[col].quantile(0.25)
                                Q3 = base_df[col].quantile(0.75)
                                IQR = Q3 - Q1

                                lower_bound = Q1 - 1.5 * IQR
                                upper_bound = Q3 + 1.5 * IQR

                                outlier_mask = (
                                    (base_df[col] < lower_bound) |
                                    (base_df[col] > upper_bound)
                                )

                            elif detection_method == "Z-Score":
                                mean = base_df[col].mean()
                                std = base_df[col].std()

                                z_scores = (base_df[col] - mean) / std

                                lower_bound = -3
                                upper_bound = 3

                                outlier_mask = (
                                    (z_scores < lower_bound) |
                                    (z_scores > upper_bound)
                                )
                            outlier_count = int(outlier_mask.sum())

                            outlier_summary_rows.append({"Column": col, "Affected Rows": outlier_count})

                            if outlier_method == "Flag Only":
                                outlier_df[f"{col}_Outlier"] = ((outlier_df[col] < lower_bound) | (outlier_df[col] > upper_bound))
                            elif outlier_method == "Cap at Bounds":
                                outlier_df[col] = outlier_df[col].clip(lower=lower_bound, upper=upper_bound)
                            elif outlier_method == "Remove Rows":
                                current_mask = (outlier_df[col] < lower_bound) | (outlier_df[col] > upper_bound)
                                outlier_df = outlier_df[~current_mask]

                    if outlier_summary_rows:
                        outlier_summary_df = pd.DataFrame(outlier_summary_rows)
                        navy_table(outlier_summary_df, height=80, key="outlier_summary_table")
                        if outlier_method == "Flag Only":
                            st.info("Outliers were flagged only.")
                        elif outlier_method == "Cap at Bounds":
                            st.success("Outliers were capped at IQR bounds ✅")
                        elif outlier_method == "Remove Rows":
                            st.success("Outlier rows were removed ✅")

            # Duplicates
            duplicates = outlier_df.duplicated().sum()
            if duplicates > 0:
                outlier_df = outlier_df.drop_duplicates()

            duplicate_keys = 0
            if returns_df is not None:
                duplicate_keys = returns_df["Order ID"].duplicated().sum()
                if duplicate_keys > 0:
                    returns_df = returns_df.drop_duplicates(subset=["Order ID"])

            # Category standardization
            outlier_df["Category"] = outlier_df["Category"].astype(str).str.strip().str.title()
            outlier_df["Segment"] = outlier_df["Segment"].astype(str).str.strip().str.title()

            # Format validation
            outlier_df["Order Date"] = pd.to_datetime(outlier_df["Order Date"], errors="coerce")
            outlier_df["Ship Date"] = pd.to_datetime(outlier_df["Ship Date"], errors="coerce")
            invalid_order_dates = outlier_df["Order Date"].isnull().sum()
            invalid_ship_dates = outlier_df["Ship Date"].isnull().sum()

            numeric_cols = ["Quantity", "Total Revenue", "Total Profit"]
            for col in numeric_cols:
                outlier_df[col] = pd.to_numeric(outlier_df[col], errors="coerce")
            invalid_numbers = outlier_df[numeric_cols].isnull().sum()

            bottom_left, bottom_mid, bottom_right = st.columns([0.95, 0.95, 1.1], gap="large")

            with bottom_left:
                with st.container(border=True, key="duplicate_box"):
                    st.markdown('<span class="step-pill">Step 5</span>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Duplicate Check</div>', unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div class="mini-note">
                            Duplicate rows: <b>{duplicates}</b><br>
                            Duplicate Return Order IDs: <b>{duplicate_keys}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    if duplicates > 0:
                        st.success("Duplicates removed ✅")
                    else:
                        st.success("No duplicate rows found ✅")
                    if returns_df is not None:
                        if duplicate_keys > 0:
                            st.success("Duplicate return keys removed before merge ✅")
                        else:
                            st.success("No duplicate return keys found ✅")

            with bottom_mid:
                with st.container(border=True, key="category_box"):
                    st.markdown('<span class="step-pill">Step 6</span>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Category Standardization</div>', unsafe_allow_html=True)
                    st.markdown(
                        """
                        <div class="mini-note">
                            Category and Segment values were cleaned using strip and title case formatting.
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    st.success("Category and Segment standardized ✅")

            with bottom_right:
                with st.container(border=True, key="format_box"):
                    st.markdown('<span class="step-pill">Step 7</span>', unsafe_allow_html=True)
                    st.markdown('<div class="section-heading">Format Validation</div>', unsafe_allow_html=True)
                    st.markdown(
                        f"""
                        <div class="mini-note">
                            Invalid Order Dates: <b>{invalid_order_dates}</b><br>
                            Invalid Ship Dates: <b>{invalid_ship_dates}</b>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )
                    invalid_numbers_df = invalid_numbers.reset_index()
                    invalid_numbers_df.columns = ["Column", "Invalid Count"]
                    navy_table(invalid_numbers_df, height=87, key="format_validation_table")
                    if invalid_order_dates == 0 and invalid_ship_dates == 0 and invalid_numbers.sum() == 0:
                        st.success("All data formats are valid ✅")
                    else:
                        st.warning("Some values were invalid and converted to NaN")

            with st.container(border=True, key="final_save_box"):
                st.markdown('<span class="step-pill">Final Step</span>', unsafe_allow_html=True)
                st.markdown('<div class="section-heading">Save Cleaned Data</div>', unsafe_allow_html=True)
                orders_df["Order Date"] = pd.to_datetime(orders_df["Order Date"], errors="coerce", dayfirst=False)
                orders_df["Ship Date"] = pd.to_datetime(orders_df["Ship Date"], errors="coerce", dayfirst=False)

                st.session_state["orders_raw_df"] = orders_df.copy()
                st.session_state["people_df"] = people_df
                st.session_state["returns_df"] = returns_df
                st.session_state["clean_df"] = outlier_df.copy()
                st.session_state["data_ready"] = True
                st.success("Data saved successfully for the other pages ✅")

        # =========================
        # TAB 3: IMPACT SUMMARY + PREVIEW
        # =========================
        with tab_impact:
            render_metadata_sidebar()

            if "outlier_df" not in locals():
                base_df = st.session_state.get("clean_df", orders_df).copy()
                outlier_df = st.session_state.get("clean_df", orders_df).copy()
                outlier_method = st.session_state.get("outlier_method", "None")

            if outlier_method != "None":
                st.markdown('<div class="section-heading">Outlier Impact Summary</div>', unsafe_allow_html=True)
                sum_left, sum_right = st.columns(2, gap="large")
                target_cols = ["Total Revenue", "Total Profit"]
                target_column_boxes = [sum_left, sum_right]

                for i, col in enumerate(target_cols):
                    if col in base_df.columns:
                        before = base_df[col].dropna()
                        after = outlier_df[col].dropna()

                        Q1 = before.quantile(0.25)
                        Q3 = before.quantile(0.75)
                        IQR = Q3 - Q1
                        low = Q1 - 1.5 * IQR
                        high = Q3 + 1.5 * IQR
                        affected = int(((before < low) | (before > high)).sum())

                        summary = pd.DataFrame({
                            "Metric": ["Affected Rows", "Mean", "Median", "Std Dev", "Min", "Q1", "Q3", "Max"],
                            "Before": [
                                affected,
                                round(before.mean(), 2),
                                round(before.median(), 2),
                                round(before.std(), 2),
                                round(before.min(), 2),
                                round(before.quantile(0.25), 2),
                                round(before.quantile(0.75), 2),
                                round(before.max(), 2)
                            ],
                            "After": [
                                affected,
                                round(after.mean(), 2),
                                round(after.median(), 2),
                                round(after.std(), 2),
                                round(after.min(), 2),
                                round(after.quantile(0.25), 2),
                                round(after.quantile(0.75), 2),
                                round(after.max(), 2)
                            ]
                        })

                        with target_column_boxes[i]:
                            with st.container(border=True, key=f"outlier_impact_box_{i}"):
                                st.markdown(f'<div class="section-heading">🔎 {col}</div>', unsafe_allow_html=True)
                                navy_table(summary, height=285, key=f"outlier_impact_table_{i}")
            else:
                st.info("Select an outlier treatment method in the Cleaning Controls tab to display the impact summary.")

            with st.container(border=True, key="preview_box"):
                st.markdown('<div class="section-heading">Preview of First 10 Rows</div>', unsafe_allow_html=True)
                navy_table(orders_df.head(10), height=230, key="preview_first_10_table")

    except Exception as e:
        st.error(f"Error: {e}")

else:
    with tab_source:
        st.warning("Please upload a file or paste a Google Sheets link")
    with tab_cleaning:
        st.info("Load the dataset first, then return here to apply the cleaning controls.")
    with tab_impact:
        st.info("The impact summary and data preview will appear after the dataset is loaded and cleaned.")
