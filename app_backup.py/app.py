
import streamlit as st
import pandas as pd
import plotly.express as px

# ---------------- PAGE CONFIGURATION ----------------
st.set_page_config(
    page_title="ANOMATRIX | Machine Intelligence",
    page_icon="⚙️",
    layout="wide"
)

# ---------------- CUSTOM DESIGN ----------------
st.markdown("""
<style>
.stApp {
    background-color: #0b1120;
    color: #ffffff;
}
[data-testid="stSidebar"] {
    background-color: #111c30;
}
.metric-card {
    background-color: #17243a;
    padding: 20px;
    border-radius: 12px;
    border: 1px solid #263957;
}
.metric-label {
    color: #a8b6cc;
    font-size: 14px;
}
.metric-value {
    color: #ffffff;
    font-size: 30px;
    font-weight: bold;
}
.metric-note {
    color: #8da3c0;
    font-size: 12px;
}
h1, h2, h3 {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)

# ---------------- SIDEBAR ----------------
st.sidebar.title("⚙️ ANOMATRIX")
st.sidebar.caption("AI-Powered Industrial Monitoring")
st.sidebar.divider()

page = st.sidebar.radio(
    "NAVIGATION",
    ["Dashboard", "Machines", "Alerts", "Predictions", "Maintenance"]
)

st.sidebar.divider()
st.sidebar.caption("System Status")
st.sidebar.success("Monitoring Active")

# ---------------- SAMPLE DATA ----------------
machines = pd.DataFrame({
    "Machine": ["M-01", "M-02", "M-03", "M-04", "M-05",
                "M-06", "M-07", "M-08", "M-09", "M-10",
                "M-11", "M-12"],
    "Type": ["Motor", "Pump", "Turbine", "CNC Mill", "Motor",
             "Pump", "Air Compressor", "Turbine", "Motor",
             "Conveyor", "Pump", "Motor"],
    "Risk Score": [15, 12, 20, 64, 18, 10, 92, 14, 22, 58, 16, 11],
    "Status": ["Normal", "Normal", "Normal", "Warning",
               "Normal", "Normal", "Critical", "Normal",
               "Normal", "Warning", "Normal", "Normal"]
})

# ---------------- DASHBOARD ----------------
if page == "Dashboard":

    st.title("ANOMATRIX Dashboard")
    st.caption("Detect Early. Predict Failures. Prevent Downtime.")
    st.divider()

    st.subheader("Machine Health Overview")

    col1, col2, col3, col4 = st.columns(4)

    metrics = [
        (col1, "Total Machines", "12", "Machines monitored"),
        (col2, "Normal Machines", "9", "Operating normally"),
        (col3, "Anomalies Detected", "3", "Require attention"),
        (col4, "High Priority", "1", "Immediate inspection")
    ]

    for col, label, value, note in metrics:
        with col:
            st.markdown(f"""
            <div class="metric-card">
                <div class="metric-label">{label}</div>
                <div class="metric-value">{value}</div>
                <div class="metric-note">{note}</div>
            </div>
            """, unsafe_allow_html=True)

    st.write("")
    left, right = st.columns([1.4, 1])

    with left:
        st.subheader("Machine Risk Analysis")

        fig = px.bar(
            machines,
            x="Machine",
            y="Risk Score",
            color="Status",
            color_discrete_map={
                "Normal": "#16a085",
                "Warning": "#f39c12",
                "Critical": "#e74c3c"
            },
            range_y=[0, 100]
        )

        fig.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            plot_bgcolor="#0b1120",
            margin=dict(l=10, r=10, t=20, b=10),
            yaxis_title="Risk Score (0-100)",
            xaxis_title="Machine ID"
        )

        st.plotly_chart(fig, use_container_width=True)

    with right:
        st.subheader("Machine Status")

        status_data = machines["Status"].value_counts().reset_index()
        status_data.columns = ["Status", "Count"]

        fig2 = px.pie(
            status_data,
            names="Status",
            values="Count",
            hole=0.55,
            color="Status",
            color_discrete_map={
                "Normal": "#16a085",
                "Warning": "#f39c12",
                "Critical": "#e74c3c"
            }
        )

        fig2.update_layout(
            template="plotly_dark",
            paper_bgcolor="#0b1120",
            margin=dict(l=10, r=10, t=20, b=10)
        )

        st.plotly_chart(fig2, use_container_width=True)

    st.subheader("Priority Machines")

    priority = machines[machines["Risk Score"] >= 50].sort_values(
        "Risk Score", ascending=False
    )

    st.dataframe(
        priority,
        use_container_width=True,
        hide_index=True
    )

# ---------------- MACHINES PAGE ----------------
elif page == "Machines":

    st.title("Machine Directory")
    st.caption("Overview of all monitored industrial machines.")

    st.dataframe(
        machines,
        use_container_width=True,
        hide_index=True
    )

# ---------------- ALERTS PAGE ----------------
elif page == "Alerts":

    st.title("Alerts & Anomalies")

    critical = machines[machines["Status"] == "Critical"]
    warning = machines[machines["Status"] == "Warning"]

    st.error(f"Critical alerts: {len(critical)}")
    st.warning(f"Warning alerts: {len(warning)}")

    st.dataframe(
        machines[machines["Status"] != "Normal"],
        use_container_width=True,
        hide_index=True
    )

# ---------------- PREDICTIONS PAGE ----------------
elif page == "Predictions":

    st.title("Failure Predictions")
    st.info("Predictive maintenance module will be connected to the forecasting model in the next development stage.")

    st.write("Example prediction from the ANOMATRIX project:")
    st.metric("M-07 Air Compressor", "2.5 days", "Estimated time to limit")

# ---------------- MAINTENANCE PAGE ----------------
elif page == "Maintenance":

    st.title("Maintenance Recommendations")

    st.warning("M-07 Air Compressor — High Priority")

    st.write("Recommended actions:")
    st.write("- Inspect bearings.")
    st.write("- Check shaft alignment.")
    st.write("- Schedule inspection within 24 hours.")

    st.divider()

    st.info("M-04 CNC Mill — Medium Priority")
    st.write("Inspect the machine and monitor its operating condition.")

st.sidebar.divider()
st.sidebar.caption("ANOMATRIX | Prototype v1.0")
