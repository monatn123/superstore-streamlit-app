import streamlit as st
import joblib
import pandas as pd
label_encoders = joblib.load("label_encoders.pkl")
model = joblib.load("return_model.pkl")
model_columns = joblib.load("model_columns.pkl")
rf_threshold = joblib.load("rf_threshold.pkl")
if "clean_df" not in st.session_state:
    st.warning("Please load and save the dataset first from the Data Collection & Cleaning page.")
    st.stop()
st.markdown("""
<style>
html, body, .stApp, .main {
    background: #ffffff !important;
}

.main {
    background: #ffffff !important;
}

[data-testid="stAppViewContainer"] {
    background: #ffffff !important;
}

.block-container {
    padding-top: 1rem !important;
    padding-left: 0.6rem !important;
    padding-right: 0.6rem !important;
}

.dashboard-title {
    position: absolute;
    top: -95px;
    left: 1px;
    z-index: 9999;
    padding: 10px 40px;
    border: 1px solid #bcd6f0;
    border-radius: 14px;
    background: #e6f0fa !important;
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.dashboard-title h1 {
    margin: 0;
    color: #0c234d !important;
    font-size: 34px;
    font-weight: 800;
}

/* Real Streamlit containers */
.st-key-input_card,
.st-key-result_card {
    background-color: #cfe3f7 !important;
    border: 1px solid #bcd6f0;
    border-radius: 16px;
    padding: 18px 20px 20px 20px;
    box-shadow: 0 4px 12px rgba(12,35,77,0.08);
}

.st-key-input_card {
    min-height: 500px;
}

.st-key-result_card {
    min-height: 330px;
    margin-top: 30px;
}

.st-key-input_card h2,
.st-key-result_card h2 {
    margin-top: 0px !important;
    margin-bottom: 10px !important;
}

.result-title {
    color: #0c234d !important;
    font-size: 28px;
    font-weight: 800;
    margin-top: 12px;
    margin-bottom: 8px;
}

.result-text {
    color: #0c234d !important;
    font-size: 15px;
    line-height: 1.6;
}

p, label, span, h2, h3 {
    color: #0c234d !important;
}

div[data-baseweb="select"] > div,
div[data-testid="stNumberInput"] input {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
    border: 1px solid #d0d7e2 !important;
}

div[data-testid="stNumberInput"] button {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
    border: 1px solid #d0d7e2 !important;
}

div[data-baseweb="select"] span {
    color: #0c234d !important;
}

ul[role="listbox"] {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
}

div[data-testid="stButton"][data-testkey="predict_btn"] > button {
    width: 100%;
    height: 50px;
    border-radius: 14px;
    background-color: #55add8 !important;
    border: 1px solid #4598c4 !important;
    color: #0c234d !important;
    font-weight: 800 !important;
}

div[data-testid="stButton"][data-testkey="predict_btn"] > button:hover {
    background-color: #4aa3cf !important;
    color: #0c234d !important;
}

.stAlert {
    background-color: #e6f0fa !important;
    color: #0c234d !important;
    border-radius: 12px !important;
    border: 1px solid #bcd6f0 !important;
}
/* Dropdown menu background */
ul[role="listbox"] {
    background-color: #ffffff !important;
}

/* Each dropdown option */
li[role="option"] {
    background-color: #ffffff !important;
    color: #0c234d !important;
}

/* Hover effect */
li[role="option"]:hover {
    background-color: #e6f0fa !important;
    color: #0c234d !important;
}

/* Selected option */
li[aria-selected="true"] {
    background-color: #d6eafc !important;
    color: #0c234d !important;
}

.stAlert * {
    color: #0c234d !important;
}
/* Date input field */
div[data-testid="stDateInput"] input {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
    border: 1px solid #d0d7e2 !important;
}

/* Calendar popup background */
div[role="dialog"] {
    background-color: white !important;
}

/* Calendar text */
div[role="dialog"] * {
    color: #0c234d !important;
}

/* Selected date */
div[role="dialog"] button[aria-selected="true"] {
    background-color: #d6eafc !important;
    color: #0c234d !important;
}

/* Hovered dates */
div[role="dialog"] button:hover {
    background-color: #e6f0fa !important;
    color: #0c234d !important;
}
/* ===== DATE PICKER FULL WHITE THEME ===== */

[data-baseweb="calendar"],
[data-baseweb="calendar"] *,
.react-datepicker,
.react-datepicker * {
    background: white !important;
    color: #0c234d !important;
}

/* Calendar popup */
div[role="dialog"],
div[role="dialog"] * {
    background-color: white !important;
    color: #0c234d !important;
}

/* Day buttons */
button[aria-label*="Choose"],
button[tabindex] {
    background: white !important;
    color: #0c234d !important;
}

/* Selected day */
button[aria-selected="true"] {
    background-color: #d6eafc !important;
    color: #0c234d !important;
    border-radius: 8px !important;
}

/* Hover */
button:hover {
    background-color: #e6f0fa !important;
    color: #0c234d !important;
}

/* Month/year header */
[data-baseweb="calendar"] select,
[data-baseweb="calendar"] svg {
    color: #0c234d !important;
    fill: #0c234d !important;
}

</style>

<div class="dashboard-title">
    <h1>Return Prediction</h1>
</div>
""", unsafe_allow_html=True)

st.markdown("<div style='height:35px;'></div>", unsafe_allow_html=True)

left, right = st.columns([1.25, 0.75], gap="large")

# =========================
# 1. ORDER INPUT FORM
# =========================
with left:
    input_card = st.container(key="input_card")

    with input_card:
        st.markdown(
            "<p style='margin-bottom:8px;'>Enter order details to predict if it will be returned.</p>",
            unsafe_allow_html=True
        )

        st.subheader("1. Order Input Form")

        col1, col2 = st.columns(2)

        with col1:
            category = st.selectbox("Category", ["Furniture", "Office Supplies", "Technology"])

            sub_category = st.selectbox(
                "Sub-Category",
                [
                    "Bookcases", "Chairs", "Tables", "Furnishings",
                    "Binders", "Storage", "Art", "Paper", "Supplies",
                    "Phones", "Accessories", "Machines", "Copiers"
                ]
            )

            segment = st.selectbox("Segment", ["Consumer", "Corporate", "Home Office"])
            region = st.selectbox("Region", ["West", "East", "Central", "South"])
            city_options = sorted(
                st.session_state["clean_df"]["City"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            state_options = sorted(
                st.session_state["clean_df"]["State"]
                .dropna()
                .astype(str)
                .unique()
                .tolist()
            )

            city = st.selectbox("City", city_options)

            state = st.selectbox("State", state_options)
        with col2:
            ship_mode = st.selectbox("Ship Mode", ["Standard Class", "Second Class", "First Class", "Same Day"])
            order_date = st.date_input("Order Date")
            expected_ship_date = st.date_input("Expected Ship Date")
            quantity = st.number_input("Quantity", min_value=1, value=1)
            revenue = st.number_input("Total Revenue", min_value=0.0, value=100.0)
            profit = st.number_input("Total Profit", value=10.0)

        profit_ratio = profit / revenue if revenue > 0 else 0
        avg_order_value = revenue / quantity if quantity > 0 else 0
        order_date_num = pd.to_datetime(order_date).value // 10**9
        ship_date_num = pd.to_datetime(expected_ship_date).value // 10**9

        predict_clicked = st.button("Predict Return", key="predict_btn")

# =========================
# 2. PREDICTION OUTCOME CARD
# =========================
with right:
    result_card = st.container(key="result_card")

    with result_card:
        st.subheader("2. Prediction Outcome")

        if predict_clicked:
            input_data = pd.DataFrame({
                "Category": [category],
                "Sub-Category": [sub_category],
                "Segment": [segment],
                "Region": [region],
                "City": [city],
                "State": [state],
                "Ship Mode": [ship_mode],
                "Order Date": [order_date_num],
                "Ship Date": [ship_date_num],
                "Quantity": [quantity],
                "Total Revenue": [revenue],
                "Total Profit": [profit],
                "Profit Ratio": [profit_ratio],
                "Average Order Value": [avg_order_value]
            })
            input_encoded = input_data.copy()

            categorical_cols = [
                "Category",
                "Sub-Category",
                "Segment",
                "Region",
                "City",
                "State",
                "Ship Mode"
            ]

            for col in categorical_cols:
                if col in input_encoded.columns:
                    input_encoded[col] = input_encoded[col].astype("category").cat.codes

            input_encoded = input_encoded.reindex(columns=model_columns, fill_value=0)
 

            prob = model.predict_proba(input_encoded)[0][1]
            prediction = 1 if prob >= rf_threshold else 0

            st.progress(float(prob))

            if prediction == 1:
                st.markdown(
                    f"""
                    <div class="result-title">⚠️ Prediction:Return Expected</div>
                    <div class="result-text">
                        Return Probability: <b>{prob:.2%}</b><br>
                        Threshold Used: <b>{rf_threshold:.2f}</b><br>
                        Profit Ratio: <b>{profit_ratio:.2f}</b><br>
                        Average Order Value: <b>{avg_order_value:.2f}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            else:
                st.markdown(
                    f"""
                    <div class="result-title">✅ Prediction: No Return</div>
                    <div class="result-text">
                        Return Probability: <b>{prob:.2%}</b><br>
                        Threshold Used: <b>{rf_threshold:.2f}</b><br>
                        Profit Ratio: <b>{profit_ratio:.2f}</b><br>
                        Average Order Value: <b>{avg_order_value:.2f}</b>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
                # =========================
                # 3. RISK EXPLANATION (MODEL-BASED)
                # =========================
                st.markdown("---")
                st.subheader("3. Risk Explanation")

                try:
                    feature_importance = pd.Series(
                        model.feature_importances_,
                        index=model_columns
                    ).sort_values(ascending=False)

                    top_features = feature_importance.head(5).index.tolist()

                    explanations = []

                    for feature in top_features:
                        if feature in input_encoded.columns:
                            value = input_encoded[feature].iloc[0]

                            if value > 0:
                                clean_feature = feature.replace("_", " ")
                                explanations.append(
                                    f"{clean_feature} is one of the strongest factors influencing return prediction."
                                )

                    if not explanations:
                        explanations.append(
                            "No major top model factor is strongly active for this order."
                        )

                    for exp in explanations[:3]:
                        st.markdown(
                            f"""
                            <div style="
                                background-color:#e6f0fa;
                                border:1px solid #bcd6f0;
                                border-radius:12px;
                                padding:10px 14px;
                                margin-bottom:8px;
                                color:#0c234d;
                                font-size:14px;
                                font-weight:600;
                            ">
                                • {exp}
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                except:
                    st.info("Risk explanation is not available for this model.")

        else:
            st.markdown(
                """
                <div class="result-title">Model Ready</div>
                <div class="result-text">
                    Fill in the order details and click Predict Return to generate the outcome.
                </div>
                """,
                unsafe_allow_html=True
            )

# =========================
# 4. MODEL EXPLANATION NOTE
# =========================
st.info(
    "This page uses the selected Random Forest model from the ML & Advanced Analytics page. "
    "The prediction applies the optimized threshold from model evaluation instead of the default 0.50 threshold."
)

