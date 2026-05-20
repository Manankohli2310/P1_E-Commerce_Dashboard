import streamlit as st
import pandas as pd
import plotly.express as px

# =========================================
# PAGE CONFIGURATION
# =========================================

st.set_page_config(
    page_title="E-commerce Dashboard",
    page_icon="📊",
    layout="wide"
)

# =========================================
# GLASSMORPHISM CSS
# =========================================

st.markdown(
    """
    <style>


    /* Main Container */
    .block-container {
        padding-top: 2rem;
        padding-left: 2rem;
        padding-right: 2rem;
    }

    /* KPI Cards */
    div[data-testid="metric-container"] {

        background: rgba(255, 255, 255, 0.08);

        border: 1px solid rgba(255, 255, 255, 0.15);

        padding: 20px;

        border-radius: 18px;

        backdrop-filter: blur(12px);
        -webkit-backdrop-filter: blur(12px);

        box-shadow: 0 8px 32px rgba(0, 0, 0, 0.37);

        transition: 0.3s;
    }

    /* KPI Hover Effect */
    div[data-testid="metric-container"]:hover {
        transform: translateY(-5px);

        border: 1px solid rgba(255,255,255,0.3);
    }

    /* Sidebar */
    section[data-testid="stSidebar"] {

        background: rgba(255, 255, 255, 0.05);

        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
    }

    /* Chart Containers */
    div[data-testid="stPlotlyChart"] {
        height: 400px;

        background: rgba(255, 255, 255, 0.05);

        border-radius: 20px;

        padding: 15px;

        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);

        box-shadow: 0 8px 32px rgba(0,0,0,0.2);

        margin-top: 20px;
    }

    /* Titles */
    h1, h2, h3 {
        color: white;
        font-weight: 700;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# =========================================
# DASHBOARD TITLE
# =========================================

st.title("📊 E-commerce Analytics Dashboard")

st.markdown(
    "Analyze sales performance, customers, and revenue trends."
)

# =========================================
# LOAD DATASET
# =========================================

df = pd.read_csv(
    "data/online_retail.csv",
    encoding="ISO-8859-1"
)

# =========================================
# DATA CLEANING
# =========================================

# Remove missing customer IDs
df = df.dropna(subset=["CustomerID"])

# Remove cancelled orders
df = df[
    ~df["InvoiceNo"]
    .astype(str)
    .str.startswith("C")
]

# Create Revenue column
df["Revenue"] = df["Quantity"] * df["UnitPrice"]

# Convert InvoiceDate
df["InvoiceDate"] = pd.to_datetime(
    df["InvoiceDate"],
    errors="coerce"
)

# Create Month column
df["Month"] = df["InvoiceDate"].dt.strftime("%Y-%m")

# =========================================
# KPI CALCULATIONS
# =========================================

total_revenue = round(df["Revenue"].sum(), 2)

total_customers = df["CustomerID"].nunique()

total_products = df["Description"].nunique()

total_orders = df["InvoiceNo"].nunique()

# =========================================
# KPI CARDS
# =========================================

col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Total Revenue",
    f"${total_revenue:,.2f}"
)

col2.metric(
    "👥 Total Customers",
    total_customers
)

col3.metric(
    "📦 Total Products",
    total_products
)

col4.metric(
    "🧾 Total Orders",
    total_orders
)

# =========================================
# TOP SELLING PRODUCTS
# =========================================

top_products = (
    df.groupby("Description")["Quantity"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_products = px.bar(
    top_products,
    x="Quantity",
    y="Description",
    orientation="h",
    title="🔥 Top Selling Products",
    color="Quantity",
    color_continuous_scale="Tealgrn"
)

fig_products.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_font_size=22
)

st.plotly_chart(
    fig_products,
    use_container_width=True
)

# =========================================
# MONTHLY REVENUE TREND
# =========================================

monthly_revenue = (
    df.groupby("Month")["Revenue"]
    .sum()
    .reset_index()
)

fig_revenue = px.line(
    monthly_revenue,
    x="Month",
    y="Revenue",
    title="📈 Monthly Revenue Trend",
    markers=True
)

fig_revenue.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_font_size=22
)

st.plotly_chart(
    fig_revenue,
    use_container_width=True
)

# =========================================
# TOP CUSTOMERS
# =========================================

top_customers = (
    df.groupby("CustomerID")["Revenue"]
    .sum()
    .sort_values(ascending=False)
    .head(10)
    .reset_index()
)

fig_customers = px.bar(
    top_customers,
    x="CustomerID",
    y="Revenue",
    title="🏆 Top Customers by Revenue",
    color="Revenue",
    color_continuous_scale="Purp"
)

fig_customers.update_layout(
    plot_bgcolor="rgba(0,0,0,0)",
    paper_bgcolor="rgba(0,0,0,0)",
    font_color="white",
    title_font_size=22
)

st.plotly_chart(
    fig_customers,
    use_container_width=True
)