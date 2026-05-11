import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CHART_BG = "#f5f7fa"
NAVY = "#0c234d"
st.markdown("""
<style>
html, body, .stApp, .main {
    background: #081b3a !important;
}

.main {
    background: linear-gradient(
        135deg,
        #081b3a 0%,
        #0c234d 45%,
        #12356b 100%
    ) !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-left: 0.35rem !important;
    padding-right: 0.35rem !important;
    padding-bottom: 0 !important;
    min-height: 100vh;
    max-width: 100% !important;
}

.dashboard-title {
    position: absolute;
    top: -150px;
    left: 1px;
    z-index: 9999;

    padding: 10px 40px;
    border: 1px solid #bcd6f0;
    border-radius: 14px;
    background: #e6f0fa !important;  /* LIGHTER BLUE */
    box-shadow: 0 4px 12px rgba(0,0,0,0.08);
}

.dashboard-title h1 {
    margin: 0;
    color: #0c234d !important;  /* NAVY TEXT */
    font-size: 34px;
    font-weight: 800;
}

h2, h3 {
    font-size: 20px !important;
    margin-top: 0.15rem !important;
    margin-bottom: 0.2rem !important;
}

[data-testid="stMetric"] {
    background-color: #cfe3f7 !important;  /* LIGHT BLUE */
    border: 1px solid #bcd6f0;
    border-radius: 14px;
    padding: 18px 10px;
}

[data-testid="stMetricLabel"] {
    width: 100%;
    text-align: center !important;
    display: block;
    padding-left: 2px !important;
}

[data-testid="stMetricValue"] {
    width: 100%;
    text-align: center !important;
}

div[data-testid="stVerticalBlock"] {
    gap: 0.2rem !important;
}

div[data-baseweb="select"] > div {
    background-color: #f5f7fa !important;   /* SAME AS CHART_BG */
    border: 1px solid #d0d7e2 !important;
    color: #0c234d !important;
}

div[data-baseweb="select"] span {
    color: #0c234d !important;
}

ul[role="listbox"] {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
}

div[data-baseweb="select"] span {
    color: white !important;
}

.st-key-body_up {
    margin-top: -35px !important;
}

.st-key-scorecards_left {
    margin-left: -59px !important;
}

.st-key-top_left_up {
    margin-top: -23px !important;
}

.st-key-top_right_up {
    margin-top: -100px !important;
    transform: translateX(5px) !important;
}

.st-key-row3_up {
    margin-top: -17px !important;
}
/* Make scorecard labels + numbers bold */
[data-testid="stMetric"] [data-testid="stMetricLabel"],
[data-testid="stMetric"] [data-testid="stMetricLabel"] *,
[data-testid="stMetric"] [data-testid="stMetricLabel"] p,
[data-testid="stMetric"] [data-testid="stMetricLabel"] div,
[data-testid="stMetric"] label,
[data-testid="stMetric"] label * {
    font-weight: 900 !important;
    color: #0c234d !important;
}

[data-testid="stMetric"] [data-testid="stMetricValue"],
[data-testid="stMetric"] [data-testid="stMetricValue"] *,
[data-testid="stMetric"] [data-testid="stMetricValue"] div {
    font-weight: 900 !important;
    color: #0c234d !important;
}
[data-testid="stMetricDelta"] {
    margin-left: 15px !important;
}
.st-key-compare_right {
    transform: translateX(5px) !important;
}

</style>

<div class="dashboard-title">
    <h1>Executive Sales Overview</h1>
</div>
""", unsafe_allow_html=True)


if "orders_raw_df" not in st.session_state:
    st.warning("Please load data first from the Data Collection & Cleaning page.")
    st.stop()

orders_raw_df = st.session_state["orders_raw_df"].copy()
returns_df = st.session_state.get("returns_df")
# Extract year safely from both Excel and Google Sheets dates


if returns_df is not None:
    returns_df = returns_df.drop_duplicates(subset=["Order ID"])
    orders_return_df = orders_raw_df.merge(returns_df, on="Order ID", how="left")
    orders_return_df["Returned"] = orders_return_df["Returned"].fillna("No")
else:
    orders_return_df = orders_raw_df.copy()
    orders_return_df["Returned"] = "No"

def parse_superstore_date(series):
    s = series.copy()

    # If already datetime
    if pd.api.types.is_datetime64_any_dtype(s):
        return s

    # Excel serial numbers
    numeric_dates = pd.to_numeric(s, errors="coerce")
    parsed = pd.Series(pd.NaT, index=s.index)

    excel_mask = numeric_dates.notna() & numeric_dates.between(20000, 60000)
    parsed.loc[excel_mask] = pd.to_datetime(
        numeric_dates.loc[excel_mask],
        unit="D",
        origin="1899-12-30",
        errors="coerce"
    )

    # Normal US Superstore dates: MM/DD/YYYY
    remaining_mask = parsed.isna()
    parsed.loc[remaining_mask] = pd.to_datetime(
        s.loc[remaining_mask].astype(str).str.strip(),
        format="%m/%d/%Y",
        errors="coerce"
    )

    # Fallback for ISO dates like 2016-11-08
    remaining_mask = parsed.isna()
    parsed.loc[remaining_mask] = pd.to_datetime(
        s.loc[remaining_mask],
        errors="coerce"
    )

    return parsed


orders_raw_df["Order Date"] = parse_superstore_date(orders_raw_df["Order Date"])
orders_raw_df["Ship Date"] = parse_superstore_date(orders_raw_df["Ship Date"])
orders_return_df["Order Date"] = parse_superstore_date(orders_return_df["Order Date"])
orders_return_df["Ship Date"] = parse_superstore_date(orders_return_df["Ship Date"])

selected_region = st.session_state.get("exec_region", "All")
selected_category = st.session_state.get("exec_category", "All")
selected_segment = st.session_state.get("exec_segment", "All")

def get_index(options, value):
    return options.index(value) if value in options else 0


region_options = ["All"] + sorted(orders_raw_df["Region"].dropna().unique().tolist())
category_options = ["All"] + sorted(orders_raw_df["Category"].dropna().unique().tolist())
segment_options = ["All"] + sorted(orders_raw_df["Segment"].dropna().unique().tolist())

body_up = st.container(key="body_up")

with body_up:
    left_margin, main_area, right_margin = st.columns([0.01, 0.98, 0.01])

    with main_area:
        left_space, cards_area, right_space = st.columns([0.01, 0.45, 0.40])

        with right_space:
            st.markdown("<div style='margin-top:-22px;'></div>", unsafe_allow_html=True)

        filtered_df = orders_raw_df.copy()
        filtered_return_df = orders_return_df.copy()

        if selected_region != "All":
            filtered_df = filtered_df[filtered_df["Region"] == selected_region]
            filtered_return_df = filtered_return_df[filtered_return_df["Region"] == selected_region]

        if selected_category != "All":
            filtered_df = filtered_df[filtered_df["Category"] == selected_category]
            filtered_return_df = filtered_return_df[filtered_return_df["Category"] == selected_category]

        if selected_segment != "All":
            filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]
            filtered_return_df = filtered_return_df[filtered_return_df["Segment"] == selected_segment]


        if filtered_df.empty:
            st.warning("No data matches the selected filters.")
            st.stop()

        total_orders = filtered_df["Order ID"].nunique()
        total_revenue = filtered_df["Total Revenue"].sum()
        total_profit = filtered_df["Total Profit"].sum()

        with cards_area:
            scorecards_box = st.container(key="scorecards_left")

            with scorecards_box:
                left_pad, c1, c2, c3, right_pad = st.columns([0.01, 1.6, 1.6, 1.6, 0.08], gap="small")

            # =========================
            # YEAR-OVER-YEAR CHANGE
            # =========================
            filtered_df["Year"] = filtered_df["Order Date"].dt.year
            available_years = sorted(filtered_df["Year"].dropna().unique())

            current_year = available_years[-1]
            previous_year = available_years[-2] if len(available_years) >= 2 else None
 
            current_df = filtered_df[filtered_df["Year"] == current_year]
            previous_df = filtered_df[filtered_df["Year"] == previous_year]

            def yoy_change(current_value, previous_value):
                if previous_value is None or previous_value == 0 or pd.isna(previous_value):
                    return "N/A"
                change = ((current_value - previous_value) / previous_value) * 100
                sign = "+" if change >= 0 else ""
                return f"{sign}{change:.1f}% vs previous year"

            current_orders = current_df["Order ID"].nunique()
            previous_orders = previous_df["Order ID"].nunique()

            current_revenue = current_df["Total Revenue"].sum()
            previous_revenue = previous_df["Total Revenue"].sum()

            current_profit = current_df["Total Profit"].sum()
            previous_profit = previous_df["Total Profit"].sum()

            c1.metric(
                "Total Orders",
                f"{total_orders:,}",
                delta=yoy_change(current_orders, previous_orders)
            )

            c2.metric(
                "Total Revenue",
                f"${total_revenue:,.0f}",
                delta=yoy_change(current_revenue, previous_revenue)
            )

            c3.metric(
                "Total Profit",
                f"${total_profit:,.0f}",
                delta=yoy_change(current_profit, previous_profit)
            )

    # =========================
    # ROW 1
    # Average Orders by Month now replaces Profit by Region place
    # Profit by Region now replaces Revenue by Category place
    # =========================
    row1_col1, row1_col2 = st.columns(2, gap="small", vertical_alignment="top")

    with row1_col1:
        top_left_box = st.container(key="top_left_up")

        with top_left_box:
            st.subheader("Profit by Region")

            profit_region = (
                filtered_df.groupby("Region")["Total Profit"]
                .sum()
                .reset_index()
                .sort_values("Total Profit", ascending=True)
            )

            fig_profit = px.bar(
                profit_region,
                x="Region",
                y="Total Profit",
                text="Total Profit",
                template="plotly_white",
                color_discrete_sequence=["#5a8fd6"]
            )

            fig_profit.update_traces(
                texttemplate="$%{text:,.0f}",
                textposition="outside",
                textfont=dict(color=NAVY, size=10)
            )

            fig_profit.update_layout(
                height=215,
                xaxis_title="",
                yaxis_title="",
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                margin=dict(l=5, r=5, t=5, b=0)
            )

            fig_profit.update_xaxes(
                showgrid=False,
                zeroline=False,
                tickfont=dict(color=NAVY)
            )
            fig_profit.update_yaxes(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            )

            st.plotly_chart(fig_profit, use_container_width=True)

    with row1_col2:
        top_right_box = st.container(key="top_right_up")

        with top_right_box:
            st.subheader("Average Orders by Month")

            temp_df = filtered_df.copy()
            temp_df["Order Date"] = pd.to_datetime(temp_df["Order Date"], errors="coerce")
            temp_df = temp_df.dropna(subset=["Order Date"])

            temp_df["Month_Num"] = temp_df["Order Date"].dt.month
            temp_df["Month"] = temp_df["Order Date"].dt.strftime("%b")
            temp_df["Year"] = temp_df["Order Date"].dt.year

            monthly_orders = (
                temp_df.groupby(["Year", "Month_Num", "Month"])["Order ID"]
                .count()
                .reset_index(name="Orders")
            )

            avg_monthly_orders = (
                monthly_orders.groupby(["Month_Num", "Month"])["Orders"]
                .mean()
                .reset_index()
                .sort_values("Month_Num")
            )

            min_val = avg_monthly_orders["Orders"].min()
            max_val = avg_monthly_orders["Orders"].max()

            colors = [
                "red" if v == min_val else "green" if v == max_val else "#7EC8FF"
                for v in avg_monthly_orders["Orders"]
            ]

            sizes = [
                8 if v in [min_val, max_val] else 5
                for v in avg_monthly_orders["Orders"]
            ]

            fig_month = go.Figure()

            fig_month.add_trace(go.Scatter(
                x=avg_monthly_orders["Month"],
                y=avg_monthly_orders["Orders"],
                mode="lines+markers+text",
                line=dict(width=2, color="#7EC8FF"),
                marker=dict(size=sizes, color=colors),
                text=[round(v, 1) for v in avg_monthly_orders["Orders"]],
                textposition="top center",
                textfont=dict(color=NAVY, size=10),
                hovertemplate="%{x}<br>Avg Orders: %{y:.1f}<extra></extra>"
            ))

            fig_month.update_layout(
                height=293,
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                xaxis_title="",
                yaxis_title="",
                xaxis=dict(
                    categoryorder="array",
                    categoryarray=[
                        "Jan", "Feb", "Mar", "Apr", "May", "Jun",
                        "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"
                    ]
                ),
                margin=dict(l=5, r=5, t=5, b=0)
            )

            fig_month.update_xaxes(
                showgrid=False,
                zeroline=False,
                tickfont=dict(color=NAVY)
            )
            fig_month.update_yaxes(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            )

            st.plotly_chart(fig_month, use_container_width=True)

    # =========================
    # ROW 2
    # Revenue by Category + Returns Distribution + Orders vs Returns
    # all on the same level
    # =========================
    row3_box = st.container(key="row3_up")

    with row3_box:
        row2_col1, row2_col2, row2_col3 = st.columns([1, 1, 1.15], gap="small", vertical_alignment="top")

        with row2_col1:
            st.subheader("Revenue by Category")

            rev_cat = (
                filtered_df.groupby("Category")["Total Revenue"]
                .sum()
                .reset_index()
                .sort_values("Total Revenue", ascending=False)
            )
            # Sort by revenue (lowest → highest)
            rev_cat = rev_cat.sort_values("Total Revenue")

            # Light → dark palette
            palette = ["#c7b7e8", "#9f95d8", "#6f78bd"]

            # Map colors based on revenue ranking
            color_map = dict(zip(rev_cat["Category"], palette))
            fig_rev = px.bar(
                rev_cat,
                x="Category",
                y="Total Revenue",
                text="Total Revenue",
                color="Category",
                template="plotly_white",
                color_discrete_map=color_map
                
            )

            fig_rev.update_traces(width=0.55)

            fig_rev.update_traces(
                texttemplate="$%{text:,.0f}",
                textposition="outside",
                textfont=dict(color="#0c234d", size=9)
            )

            fig_rev.update_layout(
                height=337,
                xaxis_title="",
                yaxis_title="",
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=9),
                coloraxis_showscale=False,
                margin=dict(l=5, r=5, t=12, b=0),
                bargap=0.6,
                legend=dict(
                    font=dict(color=NAVY),
                    title_font=dict(color=NAVY)
                ),
            )
            fig_rev.update_xaxes(
                showgrid=False,
                zeroline=False,
                showticklabels=True,
                ticks="",
                tickfont=dict(color="#0c234d"),
                color="#0c234d",
                type="category",   # ✅ add this
                categoryorder="array",
                categoryarray=rev_cat["Category"]   # ✅ add this
            )
            fig_rev.update_yaxes(
                showgrid=False,
                zeroline=False,
                showticklabels=False
            )

            st.plotly_chart(fig_rev, use_container_width=True)

        with row2_col2:
            st.subheader("Returns Distribution")
            # Quantity-level returns distribution
            # Order-level returns distribution
            filtered_return_df["Returned"] = filtered_return_df["Returned"].fillna("No")

            order_returns = (
                filtered_return_df.groupby("Order ID")["Returned"]
                .apply(lambda x: "Yes" if "Yes" in x.values else "No")
                .reset_index()
            )

            returns_count = order_returns["Returned"].value_counts().reset_index()
            returns_count.columns = ["Returned", "Count"]

            total_return_orders = returns_count["Count"].sum()
    
            fig_returns = px.pie(
                returns_count,
                names="Returned",
                values="Count",
                hole=0.6,
                template="plotly_white",
                color="Returned",
                color_discrete_map={
                    "No": "#9aaaf2",   # lavender-blue
                    "Yes": "#ff7a7a"   # keep your same red
                }
            )

            fig_returns.update_traces(
                texttemplate="%{value:,.0f}<br><span style='font-size:10px'>%{percent}</span>",
                textposition="inside",
                textfont=dict(color="#0c234d", size=12, family="Arial")
            )

            fig_returns.update_layout(
                height=337,
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=9),

                legend=dict(
                    font=dict(color=NAVY)
                ),

                margin=dict(l=5, r=5, t=12, b=5),

                annotations=[
                    dict(
                        text=f"{total_return_orders:,.0f}<br><span style='font-size:11px'>Total Orders</span>",
                        x=0.5,
                        y=0.5,
                        showarrow=False,
                        font=dict(color=NAVY, size=15, family="Arial")
                    )
                ]
            )
            st.plotly_chart(fig_returns, use_container_width=True)

        with row2_col3:
            compare_box = st.container(key="compare_right")

            with compare_box:
                st.subheader("Orders vs Returns by Category")

                orders_cat = (
                    filtered_df.groupby("Category")["Order ID"]
                    .nunique()
                    .reset_index(name="Orders")
                )

                returns_cat = (
                    filtered_return_df[filtered_return_df["Returned"] == "Yes"]
                    .groupby("Category")["Order ID"]
                    .nunique()
                    .reset_index(name="Returns")
                )

                compare_cat = pd.merge(orders_cat, returns_cat, on="Category", how="left").fillna(0)

                fig_compare = go.Figure()

                fig_compare.add_trace(go.Bar(
                    x=compare_cat["Category"],
                    y=compare_cat["Orders"],
                    name="Orders",
                    marker_color="#6ea8fe",   # lighter blue
                    text=compare_cat["Orders"],
                    textposition="outside",
                    textfont=dict(color=NAVY, size=9)
                ))

                fig_compare.add_trace(go.Bar(
                    x=compare_cat["Category"],
                    y=compare_cat["Returns"],
                    name="Returns",
                    marker_color="#f7b267",   # lighter orange (same tone)
                    text=compare_cat["Returns"],
                    textposition="outside",
                    textfont=dict(color=NAVY, size=9)
                ))

                fig_compare.update_traces(
                    cliponaxis=False
                )

                fig_compare.update_layout(
                    barmode="group",
                    height=337,
                    paper_bgcolor=CHART_BG,
                    plot_bgcolor=CHART_BG,
                    font=dict(color=NAVY, size=9),
                    xaxis_title="",
                    yaxis_title="",
                    legend_title="",
                    margin=dict(l=5, r=5, t=18, b=0),
                    legend=dict(font=dict(color=NAVY))
                )

                fig_compare.update_xaxes(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=True,
                    ticks="",
                    tickfont=dict(color="#0c234d"),
                    color="#0c234d"
                )

                fig_compare.update_yaxes(
                    showgrid=False,
                    zeroline=False,
                    showticklabels=False
                )

                st.plotly_chart(fig_compare, use_container_width=True)
