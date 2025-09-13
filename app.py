# streamlit_app.py

import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# ---- Demo Dataset ----
np.random.seed(42)  # reproducibility

data = {
    "date": pd.date_range("2025-08-01", periods=30, freq="D"),
    "customer_name": ["Sharma", "Gupta", "Verma", "Patel"] * 7 + ["Sharma", "Gupta"],
    "liters": np.random.randint(1, 5, size=30),
    "rate": [50] * 30,  # Rs/litre fixed
    "session": np.random.choice(["Morning", "Night"], size=30),  # delivery session
    "fat": np.round(np.random.uniform(3.5, 6.5, size=30), 2)  # milk fat %
}
df = pd.DataFrame(data)
df["amount"] = df["liters"] * df["rate"]
df["paid"] = df["amount"] - np.random.choice([0, 10, 20], size=30)  # some pending
df["balance"] = df["amount"] - df["paid"]

# ---- Dashboard UI ----
st.title("📊 Milk Business Dashboard")

# Date filter
date_filter = st.date_input("Select Date Range", [df["date"].min(), df["date"].max()])
start_date, end_date = date_filter
filtered_df = df[(df["date"] >= pd.to_datetime(start_date)) & (df["date"] <= pd.to_datetime(end_date))]

# Summary metrics
col1, col2, col3 = st.columns(3)
col1.metric("Total Liters", f"{filtered_df['liters'].sum()} L")
col2.metric("Total Amount", f"₹{filtered_df['amount'].sum()}")
col3.metric("Pending Balance", f"₹{filtered_df['balance'].sum()}")

# Customer-wise report
st.subheader("📌 Customer Wise Report")
st.dataframe(filtered_df.groupby("customer_name")[["liters", "amount", "paid", "balance"]].sum())

# Graph: Daily liters
st.subheader("📈 Daily Milk Trend")
daily = filtered_df.groupby("date")["liters"].sum()
st.line_chart(daily)

# Pie Chart: Customer-wise liters
st.subheader("🥧 Customer Contribution (Liters)")
customer_share = filtered_df.groupby("customer_name")["liters"].sum()
fig1, ax1 = plt.subplots()
ax1.pie(customer_share, labels=customer_share.index, autopct="%1.1f%%", startangle=90)
ax1.axis("equal")
st.pyplot(fig1)

# Morning vs Night Fat Chart
st.subheader("🌞 Morning vs 🌙 Night Average Fat %")
fat_session = filtered_df.groupby("session")["fat"].mean()
st.bar_chart(fat_session)

# Alerts: Pending Payments
st.subheader("⚠️ Alerts")
alerts = filtered_df[filtered_df["balance"] > 0]
if alerts.empty:
    st.success("No pending payments! ✅")
else:
    for _, row in alerts.iterrows():
        st.error(f"{row['customer_name']} has pending balance ₹{row['balance']} on {row['date'].date()}")
