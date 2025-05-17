import streamlit as st
import plotly.express as px

import pandas as pd
import numpy as np

from sqlalchemy import create_engine, inspect
from sqlalchemy import text

warehouse = "postgresql://exam_streamlit_user:6beiuI3metBtg239sErSxtwEpLiBZ8xx@dpg-d0jugqre5dus73ba6b3g-a.singapore-postgres.render.com/exam_streamlit"
engine = create_engine(warehouse,  client_encoding='utf8')
connection = engine.connect()

@st.cache_data
def load_data():
    query_ext = """
        SELECT "Product", count(*) AS count
        FROM final
        GROUP BY "Product";
    """
    result = connection.execute(text(query_ext))
    return pd.DataFrame(result.mappings().all())

df = load_data()

df = load_data()
df_sorted = df.sort_values(by="count", ascending=False)
total_sales = df["count"].sum()
df["percentage"] = round(df["count"] / total_sales * 100, 2)

# Title
st.title("📊 Sales Dashboard")

# Top Products Table
st.subheader("🏆 Top Products")
st.dataframe(df_sorted, use_container_width=True)

# Pie Chart: % of total sales per product
st.subheader("📈 Percentage of Total Sales by Product")
pie_fig = px.pie(df, names="Product", values="percentage", hole=0.4)
st.plotly_chart(pie_fig, use_container_width=True)

# Least Sold Product
st.subheader("📉 Least Sold Product")
df_sorted = df.sort_values(by="count", ascending=False)
total_sales = df_sorted["count"].sum()

# Calculate percentage column
df_sorted["percentage"] = (df_sorted["count"] / total_sales * 100).round(2)

least_sold = df_sorted.iloc[-1]
st.markdown(f"- **{least_sold['Product']}** with only **{least_sold['count']}** sales (**{least_sold['percentage']}%** of total)")
