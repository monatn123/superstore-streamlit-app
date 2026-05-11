import streamlit as st
import pandas as pd
import plotly.express as px
import numpy as np
import joblib
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import (
    cross_val_predict,
    train_test_split,
    StratifiedKFold
)
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    roc_auc_score,
    average_precision_score,
    confusion_matrix
)

CHART_BG = "#f5f7fa"
NAVY = "#0c234d"


def fix_plotly_colors(fig):
    fig.update_layout(
        font=dict(color=NAVY),
        legend=dict(font=dict(color=NAVY), title_font=dict(color=NAVY))
    )
    fig.update_xaxes(title_font=dict(color=NAVY), tickfont=dict(color=NAVY), color=NAVY)
    fig.update_yaxes(title_font=dict(color=NAVY), tickfont=dict(color=NAVY), color=NAVY)
    return fig


st.markdown("""
<style>
html, body, .stApp, .main { background: #ffffff !important; }

.main {
    background: linear-gradient(135deg, #ffffff 0%, #f5f7fa 45%, #eef3f9 100%) !important;
}

[data-testid="stAppViewContainer"] { background: transparent !important; }

.block-container {
    padding-top: 2rem !important;
    padding-left: 0.35rem !important;
    padding-right: 0.35rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
}

.dashboard-title {
    position: absolute;
    top: -115px;
    left: 1px;
    z-index: 9999;
    padding: 10px 40px;
    border: 1px solid #bcd6f0;
    border-radius: 14px;
    background: #e6f0fa;
    box-shadow: 0 4px 14px rgba(0,0,0,0.08);
}

.dashboard-title h1 {
    margin: 0;
    color: #0c234d;
    font-size: 34px;
    font-weight: 800;
    line-height: 1;
}

h2, h3 {
    font-size: 20px !important;
    margin-top: 0.15rem !important;
    margin-bottom: 0.25rem !important;
    color: #0c234d !important;
}

p, label, span { color: #0c234d !important; }

.metric-card-custom {
    background-color: #cfe3f7;
    border: 1px solid #bcd6f0;
    border-radius: 14px;
    height: 125px;
    min-height: 125px;
    max-height: 125px;
    padding: 10px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center !important;
    text-align: center !important;
}

.metric-card-custom .metric-label {
    font-size: 13px;
    font-weight: 700;
    color: #0c234d;
    margin-bottom: 5px;
    text-align: center !important;
    width: 100%;
}

.metric-card-custom .metric-value {
    font-size: 34px;
    font-weight: 700;
    color: #0c234d;
    line-height: 1.1;
    margin-bottom: 6px;
    text-align: center !important;
    width: 100%;
}

.metric-card-custom .metric-delta {
    font-size: 11px;
    color: #0c234d;
    line-height: 1.2;
    text-align: center !important;
    width: fit-content;
    margin: 6px auto 0 auto;
    padding: 4px 12px;
    font-weight: 600;
    background: #b9e4d0;
    border: 1px solid #9fd4bb;
    border-radius: 999px;
}

div[data-testid="stVerticalBlock"] { gap: 0.25rem !important; }

[data-testid="stDataFrame"] {
    background-color: #f5f7fa !important;
    border-radius: 12px !important;
    border: 1px solid #d0d7e2 !important;
}

.stAlert {
    background-color: #e6f0fa !important;
    color: #0c234d !important;
    border-radius: 12px !important;
    border: 1px solid #bcd6f0 !important;
}

div[data-baseweb="select"] > div {
    background-color: #f5f7fa !important;
    border: 1px solid rgba(255,255,255,0.10) !important;
    color: #0c234d !important;
}

div[data-baseweb="select"] span { color: #0c234d !important; }
ul[role="listbox"] { background-color: #f5f7fa !important; }

.st-key-body_up { margin-top: -25px !important; }
.st-key-scorecards_left { margin-left: -59px !important; margin-top: -14px !important; }
.st-key-supervised_info_left { margin-left: -40px !important; margin-top: 40px !important; }
.st-key-top_factors_up { margin-left: 21px !important; margin-top: -55px !important; }

.st-key-left_align_section {
    margin-left: -18px !important;
    margin-top: -12px !important;
    transform: scaleX(1.04);
    transform-origin: left;
}

.st-key-cm_components_up {
    margin-top: -10px !important;
    margin-left: -18px !important;
    transform: scaleX(1.04);
    transform-origin: left;
}

[data-testid="column"]:first-child { margin-left: -17px !important; }

.st-key-threshold_up {
    margin-left: 21px !important;
    margin-top: -130px !important;
}

.st-key-imbalance_up {
    margin-top: -120px !important;
    margin-left: 80px !important;
}

.st-key-imbalance_up .stAlert {
    padding-top: 22px !important;
    padding-bottom: 22px !important;
}

details {
    background-color: #f5f7fa !important;
    border: 1px solid #d0d7e2 !important;
    border-radius: 12px !important;
    padding: 6px 10px !important;
}

summary {
    color: #0c234d !important;
    font-weight: 600 !important;
}

[data-testid="stExpander"] {
    background-color: #f5f7fa !important;
    border: 1px solid #d0d7e2 !important;
    border-radius: 12px !important;
    box-shadow: none !important;
}

[data-testid="stExpander"] summary {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
}

[data-testid="stExpander"] summary:hover,
[data-testid="stExpander"] summary:focus,
[data-testid="stExpander"] summary:active {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
    outline: none !important;
}

[data-testid="stExpander"] > div { background-color: #f5f7fa !important; }

[data-testid="stTable"] table { border-collapse: collapse !important; }

[data-testid="stTable"] th,
[data-testid="stTable"] td {
    border: 1px solid #d0d7e2 !important;
}
</style>

<div class="dashboard-title">
    <h1>ML & Advanced Analytics</h1>
</div>
""", unsafe_allow_html=True)


if "clean_df" not in st.session_state:
    st.warning("Please load data first from the Data Collection & Cleaning page.")
    st.stop()

orders_raw_df = st.session_state["clean_df"].copy()
returns_df = st.session_state.get("returns_df")

if returns_df is None:
    st.warning("Returns sheet is required for supervised ML.")
    st.stop()

returns_df = returns_df.drop_duplicates(subset=["Order ID"])

orders_return_df = orders_raw_df.merge(
    returns_df,
    on="Order ID",
    how="left"
)

orders_return_df["Returned"] = orders_return_df["Returned"].fillna("No")

orders_raw_df["Order Date"] = pd.to_datetime(orders_raw_df["Order Date"], errors="coerce")
orders_raw_df["Ship Date"] = pd.to_datetime(orders_raw_df["Ship Date"], errors="coerce")
orders_return_df["Order Date"] = pd.to_datetime(orders_return_df["Order Date"], errors="coerce")
orders_return_df["Ship Date"] = pd.to_datetime(orders_return_df["Ship Date"], errors="coerce")

body_up = st.container(key="body_up")

with body_up:
    with st.spinner("Training models and optimizing thresholds..."):

        ml_df = orders_return_df.copy()

        ml_df["Returned"] = ml_df["Returned"].apply(
            lambda x: 1 if x == "Yes" else 0
        )

        ml_df = ml_df.drop(
            ["Row ID", "Order ID", "Customer ID", "Customer Name", "Product Name"],
            axis=1,
            errors="ignore"
        )


        ml_df["Order Date"] = ml_df["Order Date"].fillna(pd.Timestamp("2000-01-01"))
        ml_df["Ship Date"] = ml_df["Ship Date"].fillna(pd.Timestamp("2000-01-01"))

        ml_df["Order Date"] = ml_df["Order Date"].astype("int64") // 10**9
        ml_df["Ship Date"] = ml_df["Ship Date"].astype("int64") // 10**9

        label_encoders = {}

        for col in ml_df.select_dtypes(include="object").columns:
            le = LabelEncoder()
            ml_df[col] = le.fit_transform(ml_df[col].astype(str))
            label_encoders[col] = le

        ml_df = ml_df.fillna(0)

        X = ml_df.drop("Returned", axis=1)
        y = ml_df["Returned"]

        X_train, X_test, y_train, y_test = train_test_split(
            X, y,
            test_size=0.2,
            random_state=42,
            stratify=y
        )

        rf_model = RandomForestClassifier(random_state=42)

        lr_model = Pipeline([
            ("scaler", StandardScaler()),
            ("lr", LogisticRegression(max_iter=1000))
        ])

        svm_model = Pipeline([
            ("scaler", StandardScaler()),
            ("svm", SVC(probability=True, random_state=42))
        ])

        cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)

        # ── Step 1: get out-of-fold probabilities for every model ──────────────
        # These are the only probabilities used for threshold tuning AND CV metrics,
        # so both are guaranteed to use the exact same threshold logic.
        rf_cv_prob  = cross_val_predict(rf_model,  X_train, y_train, cv=cv, method="predict_proba")[:, 1]
        lr_cv_prob  = cross_val_predict(lr_model,  X_train, y_train, cv=cv, method="predict_proba")[:, 1]
        svm_cv_prob = cross_val_predict(svm_model, X_train, y_train, cv=cv, method="predict_proba")[:, 1]

        # ── Step 2: find the best threshold from CV probabilities ──────────────
        def tune_threshold_from_cv_probs(y_true, y_prob):
            threshold_rows = []

            for threshold in np.arange(0.05, 0.96, 0.01):
                y_pred_temp = (y_prob >= threshold).astype(int)

                precision = precision_score(y_true, y_pred_temp, zero_division=0)
                recall = recall_score(y_true, y_pred_temp, zero_division=0)
                f1 = f1_score(y_true, y_pred_temp, zero_division=0)

                threshold_rows.append({
                    "Threshold": threshold,
                    "Precision": precision,
                    "Recall": recall,
                    "F1": f1
                })

            threshold_df = pd.DataFrame(threshold_rows)

            best_row = threshold_df.sort_values("F1", ascending=False).iloc[0]

            return best_row["Threshold"], threshold_df

        rf_threshold,  rf_threshold_df  = tune_threshold_from_cv_probs(y_train, rf_cv_prob)
        lr_threshold,  lr_threshold_df  = tune_threshold_from_cv_probs(y_train, lr_cv_prob)
        svm_threshold, svm_threshold_df = tune_threshold_from_cv_probs(y_train, svm_cv_prob)

        # ── Step 3: compute CV metrics using the optimised threshold ───────────
        # Applying the threshold to out-of-fold probs means CV and test metrics
        # are evaluated under identical threshold logic — no more default-0.5 mismatch.
        def compute_metrics(y_true, y_prob, threshold):
            y_pred = (y_prob >= threshold).astype(int)
            return {
                "Accuracy":  accuracy_score(y_true, y_pred),
                "Precision": precision_score(y_true, y_pred, zero_division=0),
                "Recall":    recall_score(y_true, y_pred, zero_division=0),
                "F1":        f1_score(y_true, y_pred, zero_division=0),
                "ROC-AUC":   roc_auc_score(y_true, y_prob),
                "PR-AUC":    average_precision_score(y_true, y_prob)
            }

        rf_cv_metrics  = compute_metrics(y_train, rf_cv_prob,  rf_threshold)
        lr_cv_metrics  = compute_metrics(y_train, lr_cv_prob,  lr_threshold)
        svm_cv_metrics = compute_metrics(y_train, svm_cv_prob, svm_threshold)

        # ── Step 4: fit on full training set, evaluate on held-out test set ───
        rf_model.fit(X_train, y_train)
        lr_model.fit(X_train, y_train)
        svm_model.fit(X_train, y_train)
        
        joblib.dump(rf_model, "return_model.pkl")
        joblib.dump(X.columns.tolist(), "model_columns.pkl")
        joblib.dump(rf_threshold, "rf_threshold.pkl")
        joblib.dump(label_encoders, "label_encoders.pkl")

        rf_prob  = rf_model.predict_proba(X_test)[:, 1]
        lr_prob  = lr_model.predict_proba(X_test)[:, 1]
        svm_prob = svm_model.predict_proba(X_test)[:, 1]

        rf_test_metrics  = compute_metrics(y_test, rf_prob,  rf_threshold)
        lr_test_metrics  = compute_metrics(y_test, lr_prob,  lr_threshold)
        svm_test_metrics = compute_metrics(y_test, svm_prob, svm_threshold)

        rf_pred  = (rf_prob  >= rf_threshold).astype(int)
        lr_pred  = (lr_prob  >= lr_threshold).astype(int)
        svm_pred = (svm_prob >= svm_threshold).astype(int)

        rf_cm  = confusion_matrix(y_test, rf_pred)
        lr_cm  = confusion_matrix(y_test, lr_pred)
        svm_cm = confusion_matrix(y_test, svm_pred)

        model_results = pd.DataFrame({
            "Model": ["Random Forest", "Logistic Regression", "SVM"],

            "Optimized Threshold": [rf_threshold, lr_threshold, svm_threshold],

            "CV Accuracy":  [rf_cv_metrics["Accuracy"],  lr_cv_metrics["Accuracy"],  svm_cv_metrics["Accuracy"]],
            "CV Precision": [rf_cv_metrics["Precision"], lr_cv_metrics["Precision"], svm_cv_metrics["Precision"]],
            "CV Recall":    [rf_cv_metrics["Recall"],    lr_cv_metrics["Recall"],    svm_cv_metrics["Recall"]],
            "CV F1":        [rf_cv_metrics["F1"],        lr_cv_metrics["F1"],        svm_cv_metrics["F1"]],
            "CV ROC-AUC":   [rf_cv_metrics["ROC-AUC"],   lr_cv_metrics["ROC-AUC"],   svm_cv_metrics["ROC-AUC"]],
            "CV PR-AUC":    [rf_cv_metrics["PR-AUC"],    lr_cv_metrics["PR-AUC"],    svm_cv_metrics["PR-AUC"]],

            "Test Accuracy":  [rf_test_metrics["Accuracy"],  lr_test_metrics["Accuracy"],  svm_test_metrics["Accuracy"]],
            "Test Precision": [rf_test_metrics["Precision"], lr_test_metrics["Precision"], svm_test_metrics["Precision"]],
            "Test Recall":    [rf_test_metrics["Recall"],    lr_test_metrics["Recall"],    svm_test_metrics["Recall"]],
            "Test F1":        [rf_test_metrics["F1"],        lr_test_metrics["F1"],        svm_test_metrics["F1"]],
            "Test ROC-AUC":   [rf_test_metrics["ROC-AUC"],   lr_test_metrics["ROC-AUC"],   svm_test_metrics["ROC-AUC"]],
            "Test PR-AUC":    [rf_test_metrics["PR-AUC"],    lr_test_metrics["PR-AUC"],    svm_test_metrics["PR-AUC"]]
        })

        model_results = model_results.round(4)

        best_recall_row  = model_results.loc[model_results["Test Recall"].idxmax()]
        best_f1_row      = model_results.loc[model_results["Test F1"].idxmax()]
        best_roc_auc_row = model_results.loc[model_results["Test ROC-AUC"].idxmax()]

left_margin, main_area, right_margin = st.columns([0.01, 0.98, 0.01])

with main_area:
    left_space, cards_area, right_space = st.columns([0.01, 0.55, 0.30])

    with cards_area:
        scorecards_box = st.container(key="scorecards_left")

        with scorecards_box:
            left_pad, c1, c2, c3, c4, right_pad = st.columns(
                [0.04, 1.25, 1.25, 1.25, 1.25, 0.12],
                gap="small"
)

            with c1:
                st.markdown(
                    f"""
                    <div class="metric-card-custom">
                        <div class="metric-label">Highest Test Recall</div>
                        <div class="metric-value">{best_recall_row['Test Recall']:.2%}</div>
                        <div class="metric-delta">{best_recall_row['Model']} | Threshold: {best_recall_row['Optimized Threshold']:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c2:
                st.markdown(
                    f"""
                    <div class="metric-card-custom">
                        <div class="metric-label">Highest Test F1 Score</div>
                        <div class="metric-value">{best_f1_row['Test F1']:.2%}</div>
                        <div class="metric-delta">{best_f1_row['Model']} | Threshold: {best_f1_row['Optimized Threshold']:.2f}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )
            with c3:
                st.markdown(
                    f"""
                    <div class="metric-card-custom">
                        <div class="metric-label">Highest Test ROC-AUC</div>
                        <div class="metric-value">{best_roc_auc_row['Test ROC-AUC']:.3f}</div>
                        <div class="metric-delta">{best_roc_auc_row['Model']}</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                )

            with c4:
                st.markdown(
                    f"""
                    <div class="metric-card-custom">
                        <div class="metric-label">Best Model</div>
                        <div class="metric-value" style="font-size:26px;">Random Forest</div>
                        <div class="metric-delta">Based on F1 Score</div>
                    </div>
                    """,
                    unsafe_allow_html=True
                ) 



    left_space, info_area, imbalance_area = st.columns([0.01, 0.44, 0.36])

    with info_area:
        info_inner, info_empty = st.columns([0.97, 0.03])

        with info_inner:
            info_box = st.container(key="supervised_info_left")

            with info_box:
                st.info(
                    "Models predict whether an order is likely to be returned based on transaction features. "
                    "Thresholds are tuned on out-of-fold CV probabilities, then applied consistently to both "
                    "CV and test metrics for a fair, apples-to-apples comparison."
                )

            st.markdown("</div>", unsafe_allow_html=True)

        with imbalance_area:
            imbalance_box = st.container(key="imbalance_up")

            with imbalance_box:
                imbalance_inner, imbalance_empty = st.columns([0.92, 0.08])  # ⬅️ increased width

                with imbalance_inner:
                    st.markdown(
                        """
                        <div style="
                            background-color:#e6f0fa;
                            height:150px;
                            padding:12px 18px;
                            border-radius:12px;
                            color:#0c234d;
                            line-height:1.4;
                            display:flex;
                            flex-direction:column;
                            justify-content:center;
                            align-items:flex-start;
                            text-align:left;
                            box-sizing:border-box;
                        ">
                            <b style="margin-bottom:6px;">Model Evaluation Focus:</b>
                            <div>
                                • Metric priority: F1-Score → ROC-AUC → Recall → Precision → Accuracy<br>
                                • F1-score was prioritized because it balances recall and precision<br>
                                • Recall was especially important to reduce missed returned orders<br>
                                • Random Forest achieved the strongest overall classification performance
                            </div>
                        """,
                        unsafe_allow_html=True
                    )

    row1_col1, row1_col2 = st.columns(2, gap="small", vertical_alignment="top")

    with row1_col1:
        left_align_section = st.container(key="left_align_section")

        with left_align_section:
            st.subheader("Threshold-Based Model Comparison")

            main_comparison_df = model_results[
                [
                    "Model",
                    "Optimized Threshold",
                    "Test Recall",
                    "Test F1",
                    "Test Accuracy",
                    "Test ROC-AUC"
                ]
            ]

            main_comparison_df = main_comparison_df.rename(
                columns={"Optimized Threshold": "Threshold"}
            )

            main_show = main_comparison_df.copy()
            main_show = main_show.round(3).astype({
                "Threshold": float,
                "Test Recall": float,
                "Test F1": float,
                "Test Accuracy": float,
                "Test ROC-AUC": float
            })

            def highlight_best_columns(data):
                styles = pd.DataFrame("", index=data.index, columns=data.columns)

                for col in ["Test Recall", "Test F1", "Test Accuracy", "Test ROC-AUC"]:
                    styles.loc[data[col] == data[col].max(), col] = (
                        "background-color: #b9e4d0; color: #0c234d; font-weight: bold;"
                    )

                return styles

            styled_df = (
                main_show.style
                .set_properties(**{
                    "background-color": "#f5f7fa",
                    "color": "#0c234d",
                    "text-align": "center"
                })
                .apply(highlight_best_columns, axis=None)
                .set_table_styles([
                    {
                        "selector": "th",
                        "props": [
                            ("background-color", "#f5f7fa"),
                            ("color", "#0c234d"),
                            ("font-weight", "bold"),
                            ("text-align", "center")
                        ]
                    }
                ])
            )

            st.table(
                styled_df.format({
                    "Threshold": "{:.3f}",
                    "Test Recall": "{:.3f}",
                    "Test F1": "{:.3f}",
                    "Test Accuracy": "{:.3f}",
                    "Test ROC-AUC": "{:.3f}"
                })
            )

            with st.expander("Show expanded metrics"):
                expanded_metrics_df = model_results[
                    [
                        "Model",
                        "CV Recall",
                        "CV F1",
                        "CV ROC-AUC",
                        "CV Accuracy",
                        "CV Precision",
                        "Test Precision"
                    ]
                ]
                expanded_show = expanded_metrics_df.copy()

                st.table(
                    expanded_show.style
                    .format({
                        col: "{:.3f}" for col in expanded_show.columns if col != "Model"
                    })
                    .set_properties(**{
                        "background-color": "#f5f7fa",
                        "color": "#0c234d",
                        "text-align": "center"
                    })
                    .set_table_styles([
                        {
                            "selector": "th",
                            "props": [
                                ("background-color", "#f5f7fa"),
                                ("color", "#0c234d"),
                                ("font-weight", "bold"),
                                ("text-align", "center")
                            ]
                        }
                    ])
                )

    with row1_col2:
        threshold_box = st.container(key="threshold_up")

        with threshold_box:
            st.subheader("Threshold Tuning Curve (Random Forest)")

            fig_threshold = px.line(
                rf_threshold_df,
                x="Threshold",
                y=["Recall", "Precision", "F1"],
                template="plotly_white"
            )

            fig_threshold.add_vline(
                x=rf_threshold,
                line_dash="dash",
                line_color="#3f8f6e"
            )

            fig_threshold.update_layout(
                height=260,
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                margin=dict(l=5, r=5, t=5, b=5),
                legend_title_text="Metric",
                legend=dict(
                    font=dict(color=NAVY, size=10),
                    title_font=dict(color=NAVY, size=11)
                )
            )

            fig_threshold.update_xaxes(
                title_text="Threshold",
                title_font=dict(color=NAVY),
                tickfont=dict(color=NAVY),
                color=NAVY,
                showgrid=False,
                zeroline=True,        # ✅ show axis line
                showline=True,        # ✅ force axis line
                ticks="outside",      # ✅ show tick marks
                ticklen=5             # optional: size of ticks
            )

            fig_threshold.update_yaxes(
                title_text="",
                title_font=dict(color=NAVY),
                tickfont=dict(color=NAVY),
                color=NAVY,
                showgrid=False,
                zeroline=False
            )

            st.plotly_chart(
                fig_threshold,
                use_container_width=True,
                key="threshold_tuning_curve_chart"
            )

    row2_col1, row2_col2 = st.columns(2, gap="small", vertical_alignment="top")

    with row2_col1:
        cm_components_box = st.container(key="cm_components_up")

        with cm_components_box:
            st.subheader("Confusion Matrix Components by Model")

            rf_tn,  rf_fp,  rf_fn,  rf_tp  = rf_cm.ravel()
            lr_tn,  lr_fp,  lr_fn,  lr_tp  = lr_cm.ravel()
            svm_tn, svm_fp, svm_fn, svm_tp = svm_cm.ravel()

            cm_components_df = pd.DataFrame({
                "Component": ["TP", "FP", "TN", "FN"] * 3,
                "Count": [
                    rf_tp,  rf_fp,  rf_tn,  rf_fn,
                    lr_tp,  lr_fp,  lr_tn,  lr_fn,
                    svm_tp, svm_fp, svm_tn, svm_fn
                ],
                "Model": (
                    ["Random Forest"] * 4 +
                    ["Logistic Regression"] * 4 +
                    ["SVM"] * 4
                )
            })

            fig_cm_components = px.bar(
                cm_components_df,
                x="Component",
                y="Count",
                color="Model",
                barmode="group",
                text="Count",
                template="plotly_white",
                category_orders={"Component": ["TP", "FP", "TN", "FN"]},
                color_discrete_map={
                    "Random Forest":       "#8fb7e8",
                    "Logistic Regression": "#a8d5c2",
                    "SVM":                 "#c7b7e8"
                }
            )

            fig_cm_components = fix_plotly_colors(fig_cm_components)

            fig_cm_components.update_traces(
                textposition="outside",
                textfont=dict(color=NAVY, size=10)
            )

            fig_cm_components.update_layout(
                height=270,
                xaxis_title="",
                yaxis_title="",
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                legend_title="",
                margin=dict(l=5, r=5, t=5, b=5),
                bargap=0.25,
                bargroupgap=0.08
            )

            fig_cm_components.update_xaxes(showgrid=False, zeroline=False)
            fig_cm_components.update_yaxes(
                showgrid=False, zeroline=False,
                showticklabels=False, ticks="", title=""
            )

            st.plotly_chart(fig_cm_components, use_container_width=True)

    with row2_col2:
        top_factors_box = st.container(key="top_factors_up")

        with top_factors_box:
            st.subheader("Top Factors Affecting Returns")

            feature_importance = pd.Series(
                rf_model.feature_importances_,
                index=X.columns
            )

            top_features = feature_importance.sort_values(ascending=False).head(10)

            fig_imp = px.bar(
                x=top_features.values,
                y=top_features.index,
                orientation="h",
                text=top_features.values,
                template="plotly_white"
            )

            fig_imp = fix_plotly_colors(fig_imp)

            fig_imp.update_traces(
                marker_color="#8fb7e8",
                texttemplate="%{text:.4f}",
                textposition="outside",
                textfont=dict(color=NAVY, size=10)
            )

            fig_imp.update_layout(
                height=320,
                xaxis_title="",
                yaxis_title="",
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                margin=dict(l=5, r=5, t=10, b=10)
            )

            fig_imp.update_xaxes(
                showgrid=False, zeroline=False,
                showticklabels=False, ticks=""
            )

            fig_imp.update_yaxes(
                categoryorder="total ascending",
                showgrid=False, zeroline=False
            )

            st.plotly_chart(fig_imp, use_container_width=True)
