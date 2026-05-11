import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

CHART_BG = "#f5f7fa"
NAVY = "#0c234d"

st.markdown("""
<style>
html, body, .stApp, .main {
    background: #ffffff !important;
}

.main {
    background: linear-gradient(
        135deg,
        #ffffff 0%,
        #f5f7fa 45%,
        #eef3f9 100%
    ) !important;
}

[data-testid="stAppViewContainer"] {
    background: transparent !important;
}

.block-container {
    padding-top: 2rem !important;
    padding-left: 0.35rem !important;
    padding-right: 0.35rem !important;
    padding-bottom: 0rem !important;
    max-width: 100% !important;
}

.dashboard-title {
    position: absolute;
    top: -170px;
    left: 1px;
    z-index: 9999;
    padding: 8px 22px;
    border-radius: 14px;
    border: 1px solid #bcd6f0;
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
    margin-bottom: 0.2rem !important;
    color: #0c234d !important;
}

[data-testid="stMetric"] {
    background-color: #cfe3f7 !important;
    border: 1px solid #bcd6f0;
    border-radius: 14px;
    padding: 18px 10px;
    min-height: 95px;
    display: flex;
    flex-direction: column;
    justify-content: center;
    align-items: center;
}

[data-testid="stMetricLabel"],
[data-testid="stMetricLabel"] *,
[data-testid="stMetricValue"],
[data-testid="stMetricValue"] * {
    font-weight: 900 !important;
    color: #0c234d !important;
}

div[data-baseweb="select"] > div {
    background-color: #f5f7fa !important;
    border: 1px solid #d0d7e2 !important;
    color: #0c234d !important;
}

div[data-baseweb="select"] span {
    color: #0c234d !important;
}

ul[role="listbox"] {
    background-color: #f5f7fa !important;
    border: 1px solid #d0d7e2 !important;
}

li[role="option"] {
    background-color: #f5f7fa !important;
    color: #0c234d !important;
}

li[role="option"]:hover {
    background-color: #e6f0fa !important;
    color: #0c234d !important;
}

li[aria-selected="true"] {
    background-color: #dbeafe !important;
    color: #0c234d !important;
}

.st-key-body_up {
    margin-top: -35px !important;
}

.st-key-scorecards_left {
    margin-left: -59px !important;
}

.st-key-profit_sub_up {
    margin-top: -100px !important;
    transform: translateX(5px) !important;
}

.st-key-segment_up {
    margin-top: -270px !important;
}

.st-key-ship_up {
    margin-top: -4px !important;
    transform: translateX(5px) !important;
}

.st-key-customers_up {
    margin-top: -360px !important;
}

div[data-testid="stHorizontalBlock"]:has(button) {
    margin-top: -6px !important;
}

.st-key-global_region,
.st-key-global_category,
.st-key-global_segment {
    margin-top: -35px !important;
}

.st-key-scorecards_left > div {
    margin-top: -45px !important;
}

/* FULL center everything inside scorecards */
[data-testid="stMetric"] {
    display: flex !important;
    flex-direction: column;
    justify-content: center;
    align-items: center !important;
    text-align: center !important;
}

/* Force ALL inner text to center */
[data-testid="stMetric"] * {
    text-align: center !important;
    justify-content: center !important;
}

/* Fix label specifically (Streamlit wraps it weirdly) */
[data-testid="stMetricLabel"] {
    width: 100% !important;
    display: block !important;
}

/* Fix delta alignment */
[data-testid="stMetricDelta"] {
    width: 100% !important;
    display: flex !important;
    justify-content: center !important;
}
.st-key-map_right {
    transform: translateX(5px) !important;
}

</style>

<div class="dashboard-title">
    <h1>Products & Operations Insights</h1>
</div>
""", unsafe_allow_html=True)

if "orders_raw_df" not in st.session_state:
    st.warning("Please load data first from the Data Collection & Cleaning page.")
    st.stop()

orders_raw_df = st.session_state["orders_raw_df"].copy()

st.session_state["region_options"] = ["All"] + sorted(orders_raw_df["Region"].dropna().unique().tolist())
st.session_state["category_options"] = ["All"] + sorted(orders_raw_df["Category"].dropna().unique().tolist())
st.session_state["segment_options"] = ["All"] + sorted(orders_raw_df["Segment"].dropna().unique().tolist())

selected_region = st.session_state.get("global_region", "All")
selected_category = st.session_state.get("global_category", "All")
selected_segment = st.session_state.get("global_segment", "All")

filtered_df = orders_raw_df.copy()

if selected_region != "All":
    filtered_df = filtered_df[filtered_df["Region"] == selected_region]

if selected_category != "All":
    filtered_df = filtered_df[filtered_df["Category"] == selected_category]

if selected_segment != "All":
    filtered_df = filtered_df[filtered_df["Segment"] == selected_segment]

if filtered_df.empty:
    st.warning("No data matches the selected filters.")
    st.stop()

body_up = st.container(key="body_up")

with body_up:
    left_margin, main_area, right_margin = st.columns([0.01, 0.98, 0.01])

    with main_area:
        highest_product_revenue = filtered_df.groupby("Product Name")["Total Revenue"].sum().max()
        average_order_value = filtered_df.groupby("Order ID")["Total Revenue"].sum().mean()
        total_units_sold = filtered_df["Quantity"].sum()

        left_space, cards_area, right_space = st.columns([0.01, 0.45, 0.40])

        with cards_area:
            scorecards_box = st.container(key="scorecards_left")

            with scorecards_box:
                left_pad, c1, c2, c3, right_pad = st.columns(
                    [0.01, 1.6, 1.6, 1.6, 0.08],
                    gap="small"
                )

                filtered_df["Order Date"] = pd.to_datetime(filtered_df["Order Date"], errors="coerce")
                filtered_df["Year"] = filtered_df["Order Date"].dt.year

                current_year = filtered_df["Year"].max()
                previous_year = current_year - 1

                current_df = filtered_df[filtered_df["Year"] == current_year]
                previous_df = filtered_df[filtered_df["Year"] == previous_year]

                def yoy_change(current_value, previous_value):
                    if previous_value == 0 or pd.isna(previous_value):
                        return "N/A"
                    change = ((current_value - previous_value) / previous_value) * 100
                    sign = "+" if change >= 0 else ""
                    return f"{sign}{change:.1f}% vs previous year"

                current_highest_product_revenue = current_df.groupby("Product Name")["Total Revenue"].sum().max()
                previous_highest_product_revenue = previous_df.groupby("Product Name")["Total Revenue"].sum().max()
                current_average_order_value = current_df.groupby("Order ID")["Total Revenue"].sum().mean()
                previous_average_order_value = previous_df.groupby("Order ID")["Total Revenue"].sum().mean()
                current_total_units_sold = current_df["Quantity"].sum()
                previous_total_units_sold = previous_df["Quantity"].sum()

                c1.metric(
                    "Highest Product Revenue",
                    f"${highest_product_revenue:,.0f}",
                    delta=yoy_change(current_highest_product_revenue, previous_highest_product_revenue)
                )

                c2.metric(
                    "Average Order Value",
                    f"${average_order_value:,.0f}",
                    delta=yoy_change(current_average_order_value, previous_average_order_value)
                )

                c3.metric(
                    "Total Units Sold",
                    f"{total_units_sold:,.0f}",
                    delta=yoy_change(current_total_units_sold, previous_total_units_sold)
                )

    row1_col1, row1_col2 = st.columns(2, gap="small", vertical_alignment="top")
    row2_col1, row2_col2 = st.columns(2, gap="small")

    with row2_col1:
        segment_box = st.container(key="segment_up")

        with segment_box:
            st.subheader("Orders per Segment by Category (%)")

            stack_df = (
                filtered_df.groupby(["Segment", "Category"])["Order ID"]
                .nunique()
                .reset_index(name="Orders")
            )

            stack_df["Pct"] = stack_df.groupby("Segment")["Orders"].transform(
                lambda x: x / x.sum() * 100
            )

            fig_segment = px.bar(
                stack_df,
                x="Segment",
                y="Orders",
                color="Category",
                text=stack_df["Pct"].round(1).astype(str) + "%",
                template="plotly_white",
                color_discrete_map={
                    "Office Supplies": "#c7b7e8",   # LIGHTEST
                    "Furniture": "#9f95d8",         # medium
                    "Technology": "#6f78bd"         # darkest
                }
            )

            fig_segment.update_traces(
                textposition="outside",
                textfont=dict(color=NAVY, size=10),
                cliponaxis=False
            )

            fig_segment.update_layout(
                barmode="stack",
                height=230,
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                xaxis_title="",
                yaxis_title="",
                legend_title_text="Category",
                legend=dict(
                    font=dict(color=NAVY),
                    title_font=dict(color=NAVY)
                ),
                margin=dict(l=5, r=5, t=25, b=0)
            )

            fig_segment.update_xaxes(showgrid=False, zeroline=False, tickfont=dict(color=NAVY))
            fig_segment.update_yaxes(showgrid=False, zeroline=False, showticklabels=False)

            st.plotly_chart(fig_segment, use_container_width=True)

    with row1_col2:
        profit_box = st.container(key="profit_sub_up")

        with profit_box:
            st.subheader("Most and Least Profitable Sub-Categories")

            profit_sub = (
                filtered_df.groupby("Sub-Category")["Total Profit"]
                .sum()
                .reset_index()
                .sort_values("Total Profit", ascending=True)
            )

            bottom5 = profit_sub.head(5)
            top5 = profit_sub.tail(5)

            profit_focus = pd.concat([bottom5, top5]).sort_values("Total Profit", ascending=True)

            profit_focus["Status"] = profit_focus["Total Profit"].apply(
                lambda x: "Loss" if x < 0 else "Profit"
            )

            fig_profit_sub = px.bar(
                profit_focus,
                x="Total Profit",
                y="Sub-Category",
                orientation="h",
                color="Status",
                text="Total Profit",
                template="plotly_white",
                color_discrete_map={
                    "Profit": "#3b82f6",
                    "Loss": "#ef4444"
                }
            )

            fig_profit_sub.update_traces(
                texttemplate="$%{text:,.0f}",
                textposition="outside",
                textfont=dict(color=NAVY, size=10),
                cliponaxis=False
            )

            fig_profit_sub.update_layout(
                height=285,
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                xaxis_title="",
                yaxis_title="",
                legend_title_text="Status",
                legend=dict(
                    font=dict(color=NAVY),
                    title_font=dict(color=NAVY)
                ),
                margin=dict(l=5, r=75, t=5, b=0)
            )

            fig_profit_sub.update_xaxes(showgrid=False, zeroline=False, showticklabels=False)
            fig_profit_sub.update_yaxes(
                showgrid=False,
                zeroline=False,
                automargin=True,
                tickfont=dict(color=NAVY)
            )

            st.plotly_chart(fig_profit_sub, use_container_width=True)

    with row2_col2:
        ship_box = st.container(key="ship_up")

        with ship_box:
            donut_col, map_col = st.columns([0.48, 0.52], gap="small")

            with donut_col:
                st.subheader("Ship Mode Share of Total Sales (%)")

                ship_sales = (
                    filtered_df.groupby("Ship Mode")["Total Revenue"]
                    .sum()
                    .reset_index()
                )

                fig_ship = px.pie(
                    ship_sales,
                    names="Ship Mode",
                    values="Total Revenue",
                    hole=0.60,
                    template="plotly_white",
                    color="Ship Mode",
                    color_discrete_map={
                        "Standard Class": "#bfa14a",   # deep muted mustard
                        "Second Class": "#d4b75c",     # classic mustard
                        "First Class": "#e3c97a",      # soft light mustard
                        "Same Day": "#f0dca3"          # very soft pale mustard
                    }
                )

                fig_ship.update_traces(
                    textinfo="percent",
                    textposition="inside",
                    textfont=dict(color=NAVY, size=13),
                    hovertemplate="<b>%{label}</b><extra></extra>"
                )

                fig_ship.update_layout(
                    height=310,
                    width=350,
                    autosize=False,
                    paper_bgcolor=CHART_BG,
                    plot_bgcolor=CHART_BG,
                    font=dict(color=NAVY, size=10),
                    margin=dict(l=0, r=0, t=5, b=5),
                    showlegend=True,
                    legend=dict(
                        orientation="h",
                        yanchor="top",
                        y=-0.05,
                        xanchor="center",
                        x=0.5,
                        title="",
                        font=dict(color=NAVY, size=10),
                        title_font=dict(color=NAVY)
                    )
                )

                fig_ship.update_traces(domain=dict(x=[0.05, 0.95], y=[0.05, 1]))

                st.plotly_chart(fig_ship, use_container_width=False)

            with map_col:
                map_box = st.container(key="map_right")

                with map_box:
                    st.subheader("Sales by State")

                    state_sales = (
                        filtered_df.groupby("State")["Total Revenue"]
                        .sum()
                        .reset_index()
                        .sort_values("Total Revenue", ascending=False)
                    )

                    state_abbrev = {
                        "Alabama": "AL", "Arizona": "AZ", "Arkansas": "AR", "California": "CA",
                        "Colorado": "CO", "Connecticut": "CT", "Delaware": "DE", "Florida": "FL",
                        "Georgia": "GA", "Idaho": "ID", "Illinois": "IL", "Indiana": "IN",
                        "Iowa": "IA", "Kansas": "KS", "Kentucky": "KY", "Louisiana": "LA",
                        "Maine": "ME", "Maryland": "MD", "Massachusetts": "MA", "Michigan": "MI",
                        "Minnesota": "MN", "Mississippi": "MS", "Missouri": "MO", "Montana": "MT",
                        "Nebraska": "NE", "Nevada": "NV", "New Hampshire": "NH", "New Jersey": "NJ",
                        "New Mexico": "NM", "New York": "NY", "North Carolina": "NC",
                        "North Dakota": "ND", "Ohio": "OH", "Oklahoma": "OK", "Oregon": "OR",
                        "Pennsylvania": "PA", "Rhode Island": "RI", "South Carolina": "SC",
                        "South Dakota": "SD", "Tennessee": "TN", "Texas": "TX", "Utah": "UT",
                        "Vermont": "VT", "Virginia": "VA", "Washington": "WA",
                        "West Virginia": "WV", "Wisconsin": "WI", "Wyoming": "WY",
                        "District of Columbia": "DC"
                    }

                    state_sales["Code"] = state_sales["State"].map(state_abbrev)

                    state_sales["Sales %"] = (
                        state_sales["Total Revenue"] / state_sales["Total Revenue"].sum() * 100
                    )

                    top5_states = state_sales.head(5).copy()

                    fig_state = px.choropleth(
                        state_sales,
                        locations="Code",
                        locationmode="USA-states",
                        color="Sales %",
                        scope="usa",
                        template="plotly_white",
                        color_continuous_scale=[
                            [0.0, "#e8f3ec"],   # very light green (almost white)
                            [0.25, "#c8e2d1"],  # soft pastel green
                            [0.50, "#9fceb5"],  # muted sage
                            [0.75, "#6fb394"],  # medium muted green
                            [1.0, "#3f8f6e"]    # deeper sage green (still soft)
                        ],
                        hover_name="State",
                        hover_data={
                            "Sales %": ":.1f",
                            "Total Revenue": False,
                            "Code": False
                        }
                    )

                    fig_state.add_trace(go.Scattergeo(
                        locations=top5_states["Code"],
                        locationmode="USA-states",
                        text=top5_states["Sales %"].round(1).astype(str) + "%",
                        mode="text",
                        textfont=dict(color=NAVY, size=11),
                        showlegend=False
                    ))

                    fig_state.update_traces(
                        hovertemplate="<b>%{hovertext}</b><br>Sales Share: %{z:.1f}%<extra></extra>"
                    )

                    fig_state.update_layout(
                        height=310,
                        paper_bgcolor=CHART_BG,
                        plot_bgcolor=CHART_BG,
                        font=dict(color=NAVY, size=10),
                        margin=dict(l=0, r=0, t=5, b=0),
                        coloraxis_showscale=False,
                        geo=dict(
                            bgcolor=CHART_BG,
                            lakecolor=CHART_BG
                        )
                    )

                    st.plotly_chart(fig_state, use_container_width=True)

    row3_col1, row3_col2 = st.columns([1.0, 1.0], gap="small")

    with row3_col1:
        customers_box = st.container(key="customers_up")

        with customers_box:
            st.subheader("Top 5 Customers by Selected Metric")

            metric_choice = st.selectbox(
                "Choose Metric",
                ["Sales", "Profit", "Profit Ratio"]
            )

            customer_summary = filtered_df.groupby(
                ["Customer Name", "Segment"]
            ).agg({
                "Total Revenue": "sum",
                "Total Profit": "sum"
            }).reset_index()

            customer_summary["Profit Ratio"] = (
                customer_summary["Total Profit"] /
                customer_summary["Total Revenue"].replace(0, 1)
            )

            if metric_choice == "Sales":
                metric_col = "Total Revenue"
            elif metric_choice == "Profit":
                metric_col = "Total Profit"
            else:
                metric_col = "Profit Ratio"

            top5_customers = customer_summary.sort_values(
                metric_col, ascending=False
            ).head(5).copy()

            if top5_customers.empty:
                st.warning("No customer data available for this view.")
                st.stop()

            if metric_choice == "Profit Ratio":
                top5_customers["Label"] = top5_customers[metric_col].apply(
                    lambda x: f"{x:.1%}"
                )
                x_max = top5_customers[metric_col].max() * 1.20
            else:
                top5_customers["Label"] = top5_customers[metric_col].apply(
                    lambda x: f"${x:,.0f}"
                )
                x_max = top5_customers[metric_col].max() * 1.25

            segment_colors = {
                "Consumer": "#e08a4e",      # soft burnt orange
                "Corporate": "#f2a65a",     # warm orange
                "Home Office": "#f7c08a"    # light peachy orange
            }
            top5_customers["Bar Color"] = top5_customers["Segment"].map(
                segment_colors
            ).fillna("#3b82f6")

            fig_customers = go.Figure()

            fig_customers.add_trace(go.Bar(
                x=top5_customers[metric_col],
                y=top5_customers["Customer Name"],
                orientation="h",
                text=top5_customers["Label"],
                textposition="outside",
                marker_color=top5_customers["Bar Color"],
                width=0.55,
                textfont=dict(color=NAVY, size=10),
                cliponaxis=False,
                showlegend=False
            ))

            fig_customers.add_trace(go.Scatter(
                x=[None], y=[None],
                mode="markers",
                marker=dict(size=10, color="#c9783a"),  # Consumer
                name="Consumer",
                showlegend=True
            ))

            fig_customers.add_trace(go.Scatter(
                x=[None], y=[None],
                mode="markers",
                marker=dict(size=10, color="#e09a5f"),  # Corporate
                name="Corporate",
                showlegend=True
            ))

            fig_customers.add_trace(go.Scatter(
                x=[None], y=[None],
                mode="markers",
                marker=dict(size=10, color="#f2c9a0"),  # Home Office
                name="Home Office",
                showlegend=True
            ))

            fig_customers.update_layout(
                height=223,
                paper_bgcolor=CHART_BG,
                plot_bgcolor=CHART_BG,
                font=dict(color=NAVY, size=10),
                xaxis_title="",
                yaxis_title="",
                legend_title_text="Segment",
                legend=dict(
                    font=dict(color=NAVY),
                    title_font=dict(color=NAVY)
                ),
                margin=dict(l=5, r=120, t=5, b=0)
            )

            fig_customers.update_yaxes(
                categoryorder="array",
                categoryarray=top5_customers["Customer Name"][::-1],
                automargin=True,
                showgrid=False,
                zeroline=False,
                tickfont=dict(color=NAVY)
            )

            fig_customers.update_xaxes(
                range=[0, x_max],
                showgrid=False,
                zeroline=False,
                showticklabels=False
            )

            st.plotly_chart(fig_customers, use_container_width=True)
