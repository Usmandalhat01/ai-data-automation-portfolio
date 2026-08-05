from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Operations Dashboard", layout="wide")
st.title("Business Operations Dashboard")
st.caption("A simple dashboard for reviewing sales, orders, and customer activity.")

uploaded_file = st.file_uploader("Upload an operations CSV", type=["csv"])
default_file = Path(__file__).with_name("sample_operations.csv")

if uploaded_file is not None:
    data = pd.read_csv(uploaded_file)
elif default_file.exists():
    data = pd.read_csv(default_file)
else:
    st.info("Upload a CSV to begin.")
    st.stop()

required = {"date", "customer", "region", "product", "quantity", "unit_price", "status"}
missing = required.difference(data.columns)
if missing:
    st.error(f"Missing columns: {', '.join(sorted(missing))}")
    st.stop()

data["date"] = pd.to_datetime(data["date"], errors="coerce")
data["quantity"] = pd.to_numeric(data["quantity"], errors="coerce").fillna(0)
data["unit_price"] = pd.to_numeric(data["unit_price"], errors="coerce").fillna(0)
data["revenue"] = data["quantity"] * data["unit_price"]

regions = sorted(data["region"].dropna().unique())
selected_regions = st.sidebar.multiselect("Region", regions, default=regions)
statuses = sorted(data["status"].dropna().unique())
selected_statuses = st.sidebar.multiselect("Order status", statuses, default=statuses)

filtered = data[data["region"].isin(selected_regions) & data["status"].isin(selected_statuses)]

col1, col2, col3, col4 = st.columns(4)
col1.metric("Orders", len(filtered))
col2.metric("Revenue", f"₦{filtered['revenue'].sum():,.0f}")
col3.metric("Customers", filtered["customer"].nunique())
col4.metric("Completed", int((filtered["status"].str.lower() == "completed").sum()))

st.subheader("Revenue over time")
daily = filtered.dropna(subset=["date"]).groupby("date", as_index=False)["revenue"].sum()
st.line_chart(daily, x="date", y="revenue")

left, right = st.columns(2)
with left:
    st.subheader("Revenue by product")
    product_summary = filtered.groupby("product")["revenue"].sum().sort_values(ascending=False)
    st.bar_chart(product_summary)
with right:
    st.subheader("Orders by region")
    region_summary = filtered["region"].value_counts()
    st.bar_chart(region_summary)

st.subheader("Filtered records")
st.dataframe(filtered.sort_values("date", ascending=False), use_container_width=True)
