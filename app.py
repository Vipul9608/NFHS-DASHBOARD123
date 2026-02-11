import streamlit as st
import pandas as pd
import plotly.express as px

# -------------------------
# Page Config
# -------------------------
st.set_page_config(
    page_title="NFHS India Dashboard",
    layout="wide"
)

st.title("📊 National Family Health Survey (NFHS) Dashboard")

# -------------------------
# Load Data
# -------------------------
@st.cache_data
def load_data():
    df = pd.read_excel("All India National Family Health Survey.xlsx")
    return df

df = load_data()

# -------------------------
# Sidebar Filters
# -------------------------
st.sidebar.header("🔎 Filters")

state = st.sidebar.selectbox(
    "Select State",
    df["India/States/UTs"].unique()
)

survey = st.sidebar.selectbox(
    "Select Survey",
    df["Survey"].unique()
)

area = st.sidebar.selectbox(
    "Select Area",
    df["Area"].unique()
)

filtered_df = df[
    (df["India/States/UTs"] == state) &
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

# -------------------------
# Indicator Selection
# -------------------------
numeric_columns = df.select_dtypes(include='number').columns

indicator = st.selectbox(
    "📌 Select Indicator",
    numeric_columns
)

# -------------------------
# KPI Section
# -------------------------
st.subheader("📌 Key Indicator Value")

if not filtered_df.empty:
    value = filtered_df[indicator].values[0]
    st.metric(label=indicator, value=round(value, 2))
else:
    st.warning("No data available for selected filters")

# -------------------------
# Comparison Across States
# -------------------------
st.subheader("📊 State-wise Comparison")

compare_df = df[
    (df["Survey"] == survey) &
    (df["Area"] == area)
]

fig = px.bar(
    compare_df,
    x="India/States/UTs",
    y=indicator,
    title=f"{indicator} - {survey} ({area})",
)

fig.update_layout(height=500)

st.plotly_chart(fig, use_container_width=True)

# -------------------------
# Survey Trend Comparison
# -------------------------
st.subheader("📈 Survey Trend Comparison")

trend_df = df[
    (df["India/States/UTs"] == state) &
    (df["Area"] == area)
]

fig2 = px.line(
    trend_df,
    x="Survey",
    y=indicator,
    markers=True,
    title=f"{indicator} Trend - {state}"
)

st.plotly_chart(fig2, use_container_width=True)

# -------------------------
# Raw Data Section
# -------------------------
st.subheader("📄 Raw Data Preview")
st.dataframe(filtered_df)
