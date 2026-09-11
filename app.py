import streamlit as st
import pandas as pd

# Page settings
st.set_page_config(
    page_title="DAU Dashboard",
    page_icon="📊",
    layout="wide"
)

# Google Sheet details
sheet_id = "1Oh_hbZB5OFwJ_ff56KKUm5sjxq0SZy37kmQ7IQcIt7k"
gid = "0"

csv_url = (
    f"https://docs.google.com/spreadsheets/d/{sheet_id}"
    f"/export?format=csv&gid={gid}"
)

# Load Google Sheet data
@st.cache_data(ttl=60)
def load_data():
    df = pd.read_csv(csv_url)

    # Convert Date
    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

    # Convert numbers
    for col in ["Web DAU", "App DAU", "Direct DAU"]:
        df[col] = pd.to_numeric(
            df[col].astype(str).str.replace(",", ""),
            errors="coerce"
        )

    # Remove invalid dates
    df = df.dropna(subset=["Date"])

    return df


df = load_data()

# Title
st.title("Daily Active Users Dashboard")

st.write("Data source: Google Sheets")

# Latest data
latest = df.iloc[-1]

# KPI cards
col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Web DAU",
        f"{latest['Web DAU']:,.0f}"
    )

with col2:
    st.metric(
        "App DAU",
        f"{latest['App DAU']:,.0f}"
    )

with col3:
    st.metric(
        "Direct DAU",
        f"{latest['Direct DAU']:,.0f}"
    )

# Chart
st.subheader("📈 DAU Trend")

st.line_chart(
    df,
    x="Date",
    y=["Web DAU", "App DAU", "Direct DAU"]
)

# Data table
st.subheader("📋 Data")

st.dataframe(
    df,
    use_container_width=True
)

# Refresh button
if st.button("🔄 Refresh Data"):
    st.cache_data.clear()
    st.rerun()
