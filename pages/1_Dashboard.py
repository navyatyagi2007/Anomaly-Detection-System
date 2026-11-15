
import streamlit as st
import pandas as pd

st.title("⚙️ ANOMATRIX Dashboard")

st.markdown(
    "### Detect Early. Predict Failures. Prevent Downtime."
)

st.markdown("---")

# Machine Health Overview
st.subheader("Machine Health Overview")

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Machines", "12")
col2.metric("Normal Machines", "9")
col3.metric("Anomalies Detected", "3")
col4.metric("High Priority", "1")

st.markdown("---")

# Machine Health Chart
st.subheader("Machine Health Overview")

health_data = pd.DataFrame({
    "Machine": [
        "M-01", "M-02", "M-03",
        "M-04", "M-05", "M-06"
    ],
    "Health Score": [95, 88, 92, 65, 98, 72]
})

st.bar_chart(
    health_data,
    x="Machine",
    y="Health Score"
)

st.markdown("---")

# Recent Alerts
st.subheader("Recent Alerts")

alerts = pd.DataFrame({
    "Machine ID": ["M-04", "M-07", "M-10"],
    "Alert": [
        "High Vibration",
        "Temperature Anomaly",
        "Abnormal Operating Pattern"
    ],
    "Severity": ["High", "Medium", "Medium"]
})

st.dataframe(alerts, use_container_width=True)

st.caption("ANOMATRIX | Prototype v1.0")
