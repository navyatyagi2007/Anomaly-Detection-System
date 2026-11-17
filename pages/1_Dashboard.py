import base64

import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from components.login import require_login
from components.sidebar import render_sidebar

require_login()
render_sidebar()

from components.notifications import render_notifications

# =====================================================
# 1. CSS
# =====================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif; }

.stApp {
    background:
        radial-gradient(900px 420px at 92% -5%, rgba(120,190,235,0.30), transparent 60%),
        radial-gradient(700px 400px at 0% 0%, rgba(190,225,250,0.40), transparent 60%),
        #EAF3FB;
    color: #263746;
}

/* Top bar aur main container ka extra space hatane ke liye */
[data-testid="stHeader"] { display: none !important; }
footer { visibility: hidden; }

[data-testid="stMainBlockContainer"],
.block-container {
    max-width: 1500px;
    padding-top: 0rem !important;
    margin-top: -1.8rem !important;
    padding-bottom: 1.5rem;
}

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] {
    background: #EDEAE4;
    border-right: 1px solid #DDD8D0;
}
[data-testid="stSidebarLogo"], [data-testid="stLogo"],
[data-testid="stSidebarHeader"] img {
    height: 4.8rem !important; width: auto !important;
    max-width: 100% !important; object-fit: contain;
}
[data-testid="stSidebarHeader"] {
    height: auto; padding-top: 1.2rem; padding-bottom: 1rem;
    border-bottom: 1px solid #DDD8D0;
}
[data-testid="stSidebarContent"] { display: flex; flex-direction: column; }
[data-testid="stSidebarUserContent"] {
    margin-top: auto; padding-bottom: 1.2rem; padding-top: 0;
}
[data-testid="stSidebarUserContent"] [data-testid="stElementContainer"]:not(:has(.user-card)):not(:has(.stButton)) {
    display: none !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF; color: #183B5B; border: 1px solid #D9D4CB;
    border-radius: 12px; font-weight: 650; height: 2.7rem;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #328BC5; color: #17628D; background: #F4FAFE;
}

.user-card {
    display: flex; gap: 12px; align-items: center;
    background: #E4E0D8; border-radius: 14px; padding: 12px;
    margin-bottom: 10px;
}
.user-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: #D3E8F6; color: #17628D; font-weight: 800; font-size: 13px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.user-name { font-weight: 700; font-size: 14px; color: #183B5B; }
.user-role { font-size: 12px; color: #6F7C86; }

/* ---------- HEADER ---------- */
.eyebrow {
    font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 3px; color: #6F8496; text-transform: uppercase;
    margin-top: 0;
}
.page-title { font-size: 34px; font-weight: 800; color: #14273A; margin: 1px 0 3px; line-height: 1.1; }
.page-sub { color: #5B6F7E; font-size: 13.5px; max-width: 780px; }

/* Action Planner button (top right - main area only) */
[data-testid="stMain"] .stButton > button {
    background: rgba(255,255,255,0.92); border: 1px solid #F1D3D8;
    border-radius: 16px; height: 3.5rem;
    box-shadow: 0 8px 22px rgba(190,70,90,0.12);
    transition: all .25s ease;
}
[data-testid="stMain"] .stButton > button p {
    font-family: 'JetBrains Mono', monospace; letter-spacing: 2.5px;
    font-weight: 700; font-size: 13px; color: #B03A4E;
}
[data-testid="stMain"] .stButton > button:hover {
    transform: translateY(-3px); border-color: #E5536A;
    box-shadow: 0 14px 30px rgba(190,70,90,0.22); background: #FFFFFF;
}

.divider { border: none; border-top: 1px solid #C9D6E0; margin: 8px 0 12px; }

/* ---------- COMPACT ALERT BANNER ---------- */
.alert-banner {
    background: linear-gradient(120deg, #FDE0E4 0%, #FCE9EC 60%, #FDEFF1 100%);
    border: 1px solid #F6D0D6; border-radius: 18px; padding: 14px 20px;
    display: flex; justify-content: space-between; align-items: center; gap: 18px;
    margin-top: 10px;
    box-shadow: 0 10px 24px rgba(190,70,90,0.09);
    transition: all .3s ease;
}
.alert-banner:hover { transform: translateY(-2px); box-shadow: 0 14px 30px rgba(190,70,90,0.15); }
.alert-tag { font-family: 'JetBrains Mono', monospace; letter-spacing: 2.5px;
    font-size: 10px; font-weight: 700; color: #B03A4E; }
.alert-tag .dot { display:inline-block; width:7px; height:7px; border-radius:50%;
    background:#E5536A; margin-right:7px; animation: pulse 1.6s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(229,83,106,.55);} 70%{box-shadow:0 0 0 8px rgba(229,83,106,0);} 100%{box-shadow:0 0 0 0 rgba(229,83,106,0);} }
.alert-title { font-size: 18.5px; font-weight: 800; color: #1F2D3A; margin-top: 3px; line-height: 1.25; }
.alert-desc { color: #6B5A60; font-size: 13px; margin-top: 2px; }
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 8px; }
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #FFFFFF; border-radius: 999px; padding: 5px 11px;
    font-size: 11.5px; font-weight: 500; color: #45535D;
}
.sev-box {
    background: #FFFFFF; border-radius: 14px; padding: 10px 18px; min-width: 115px;
    text-align: left; flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.sev-box .l { font-family: 'JetBrains Mono', monospace; letter-spacing: 2px;
    font-size: 9.5px; color: #6F7C86; }
.sev-box .v { font-size: 18px; font-weight: 700; color: #1F2D3A; margin-top: 2px; }
.sev-box .v span { color: #E5536A; margin-right: 6px; font-size: 14px; }

/* ---------- KPI CARDS ---------- */
.section-label { font-family: 'JetBrains Mono', monospace; letter-spacing: 3px;
    font-size: 10.5px; color: #6F8496; margin-top: 18px; }
.section-title { font-size: 21px; font-weight: 800; color: #14273A; margin: 2px 0 10px; }

.kpi-card {
    position: relative; overflow: hidden;
    background: linear-gradient(145deg, #FFFFFF 0%, #F7FBFF 100%);
    border: 1px solid #DCE7F0; border-radius: 18px;
    padding: 16px 18px 18px; min-height: 136px;
    box-shadow: 0 6px 18px rgba(35,75,110,0.06);
    transition: all .28s ease;
}
.kpi-card::before {
    content: ""; position: absolute; right: -40px; top: -40px;
    width: 140px; height: 140px; border-radius: 50%;
    background: radial-gradient(circle, var(--c) 0%, transparent 70%); opacity: .14;
}
.kpi-card:hover { transform: translateY(-4px); box-shadow: 0 14px 28px rgba(35,75,110,0.15); border-color: var(--c); }
.kpi-label { font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
    letter-spacing: 2px; color: #6F7C86; font-weight: 500; }
.kpi-link { display: block; text-decoration: none !important; color: inherit !important; }
.kpi-more { position: absolute; right: 16px; bottom: 12px; font-size: 11.5px; font-weight: 600;
    color: var(--c); opacity: 0; transform: translateX(-6px); transition: all .25s ease; }
.kpi-card:hover .kpi-more { opacity: 1; transform: translateX(0); }
html, [data-testid="stMain"], section.main { scroll-behavior: smooth; }
#machine-details { scroll-margin-top: 30px; }
.kpi-value { font-size: 34px; font-weight: 800; color: #14273A; margin-top: 12px; line-height: 1; }
.kpi-desc { font-size: 12px; color: #7A8791; margin-top: 6px; }
.kpi-line { position: absolute; left: 18px; bottom: 0; height: 4px; width: 42px;
    border-radius: 4px 4px 0 0; background: var(--c); }

/* ---------- PANELS ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.75); border-radius: 20px; border-color: #D6E1EA;
    box-shadow: 0 6px 18px rgba(35,75,110,0.05); transition: all .25s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 12px 26px rgba(35,75,110,0.10); border-color: #9CC8E2;
}
.panel-title { font-size: 17px; font-weight: 800; color: #14273A; margin-bottom: 12px; }

.risk-row { margin-bottom: 15px; }
.risk-head { display:flex; justify-content:space-between; align-items:baseline; }
.risk-name { font-weight: 700; color: #1F3547; font-size: 14.5px; }
.risk-meta { font-size: 12px; color: #7A8791; margin-top: 2px; }
.risk-score { font-weight: 800; font-size: 17px; }
.bar { height: 8px; border-radius: 8px; background: #E6EEF5; margin-top: 7px; overflow: hidden; }
.bar > div { height: 100%; border-radius: 8px; }
.tag { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:1.5px;
    padding: 3px 9px; border-radius: 999px; font-weight: 700; margin-left: 8px; }

hr { border-color: #D5E0E9; }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# 2. NOTIFICATIONS
# =====================================================

render_notifications()

# =====================================================
# 3. HEADER & ACTION PLANNER REDIRECT
# =====================================================

h_left, h_right = st.columns([4, 1], vertical_alignment="center")

with h_left:
    st.html(
        """
        <div class="eyebrow">ANOMATRIX · Command Center</div>
        <div class="page-title">Factory Command Center</div>
        <div class="page-sub">A unified view of machine health, active alerts and
        maintenance risk across the plant — all in one place.</div>
        """
    )

with h_right:
    if st.button(
        "ACTION PLANNER  ›",
        key="action_planner_nav_btn",
        use_container_width=True,
        help="Open Action Planner in Maintenance & Reports",
    ):
        st.session_state["focus_action_planner"] = True
        st.switch_page("pages/3_Maintenance_Reports.py")

st.html('<hr class="divider">')

# =====================================================
# 4. KPI CARDS (8 Cards First on Screen)
# =====================================================

st.html(
    '<div class="section-label" style="margin-top: 0;">SITUATION OVERVIEW</div>'
    '<div class="section-title">Factory health at a glance</div>'
)

kpis = [
    ("TOTAL MACHINES", "12", "Registered equipment", "#328BC5"),
    ("HEALTHY MACHINES", "09", "Operating normally", "#20A77A"),
    ("ANOMALIES FLAGGED", "03", "Require attention", "#E5A04B"),
    ("HIGH PRIORITY", "01", "Critical risk detected", "#E65D70"),
    ("AVERAGE HEALTH", "86%", "Overall machine health", "#328BC5"),
    ("PRODUCTION EFFICIENCY", "90%", "Weekly average", "#20A77A"),
    ("ESTIMATED DOWNTIME", "4.5 hrs", "Weekly downtime", "#E5A04B"),
    ("MAINTENANCE DUE", "04", "Upcoming tasks", "#8A80C5"),
]

for start in range(0, len(kpis), 4):
    cols = st.columns(4)
    for col, (label, value, desc, color) in zip(cols, kpis[start:start + 4]):
        with col:
            st.html(
                f"""
                <a class="kpi-link" href="#machine-details" target="_self">
                    <div class="kpi-card" style="--c:{color};">
                        <div class="kpi-label">{label}</div>
                        <div class="kpi-value">{value}</div>
                        <div class="kpi-desc">{desc}</div>
                        <div class="kpi-more">View details →</div>
                        <div class="kpi-line"></div>
                    </div>
                </a>
                """
            )
    if start == 0:
        st.html('<div style="height: 8px;"></div>')

# =====================================================
# 5. COMPACT ACTIVE ALERT BANNER (Below the 8 Cards)
# =====================================================

ICON = {
    "pin": '<path d="M12 21s-7-6.2-7-11a7 7 0 0114 0c0 4.8-7 11-7 11z"/><circle cx="12" cy="10" r="2.5"/>',
    "clock": '<circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/>',
    "alert": '<path d="M10.3 3.9L2 18a2 2 0 001.7 3h16.6A2 2 0 0022 18L13.7 3.9a2 2 0 00-3.4 0z"/><path d="M12 9v4M12 17h.01"/>',
}


def icon(name, size=14, color="#45535D"):
    svg = (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 24 24" '
        f'fill="none" stroke="{color}" stroke-width="2" stroke-linecap="round" '
        f'stroke-linejoin="round">{ICON[name]}</svg>'
    )
    uri = "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("utf-8")
    return f'<img src="{uri}" width="{size}" height="{size}" style="display:block"/>'


st.html(
    f"""
    <div class="alert-banner">
        <div>
            <div class="alert-tag"><span class="dot"></span>ACTIVE MACHINE ALERT</div>
            <div class="alert-title">M-07 Air Compressor — Bearing Wear Detected</div>
            <div class="alert-desc">Abnormal vibration (2.8x normal) and rising bearing temperature.</div>
            <div class="chip-row">
                <span class="chip">{icon("pin", 13)} Compressor Bay · Line 2</span>
                <span class="chip">{icon("clock", 13)} 2.5 days to limit</span>
                <span class="chip">{icon("alert", 13)} Risk score 92 / 100</span>
            </div>
        </div>
        <div class="sev-box">
            <div class="l">PRIORITY</div>
            <div class="v"><span>●</span>High</div>
        </div>
    </div>
    """
)

# =====================================================
# 6. QUICK SNAPSHOT : TOP RISKS + HEALTH SPLIT
# =====================================================

st.html(
    '<div class="section-label">QUICK SNAPSHOT</div>'
    '<div class="section-title">Where to look first</div>'
)

top_risks = pd.DataFrame(
    {
        "Machine": ["M-07 Air Compressor", "M-04 CNC Mill", "M-10 Conveyor"],
        "Pattern": [
            "Bearing wear · vibration 2.8x normal",
            "Vibration drifting upward",
            "Motor temperature spikes",
        ],
        "Score": [92, 64, 58],
        "Limit": ["2.5 days", "6 days", "9 days"],
        "Priority": ["HIGH", "MEDIUM", "MEDIUM"],
    }
)

PRIORITY_STYLE = {
    "HIGH": ("#E65D70", "#FDE3E7"),
    "MEDIUM": ("#C77F1F", "#FDF0D9"),
}

col_a, col_b = st.columns([1.5, 1])

with col_a:
    with st.container(border=True):
        rows = ""
        for _, r in top_risks.iterrows():
            fg, bg = PRIORITY_STYLE[r["Priority"]]
            rows += f"""
            <div class="risk-row">
                <div class="risk-head">
                    <div>
                        <span class="risk-name">{r['Machine']}</span>
                        <span class="tag" style="color:{fg};background:{bg};">{r['Priority']}</span>
                        <div class="risk-meta">{r['Pattern']} · limit in {r['Limit']}</div>
                    </div>
                    <div class="risk-score" style="color:{fg};">{r['Score']}</div>
                </div>
                <div class="bar"><div style="width:{r['Score']}%;background:{fg};"></div></div>
            </div>
            """
        st.html(f'<div class="panel-title">Top machines at risk</div>{rows}')

with col_b:
    with st.container(border=True):
        st.html('<div class="panel-title">Machine health split</div>')

        fig = go.Figure(
            go.Pie(
                labels=["Healthy", "Warning", "Critical"],
                values=[9, 2, 1],
                hole=0.68,
                marker=dict(colors=["#20A77A", "#E5A04B", "#E65D70"]),
                textinfo="label+value",
                sort=False,
            )
        )
        fig.update_layout(
            height=240,
            margin=dict(t=5, b=5, l=5, r=5),
            paper_bgcolor="rgba(0,0,0,0)",
            showlegend=False,
            font=dict(color="#52677A"),
            annotations=[
                dict(text="<b>86%</b><br>health", x=0.5, y=0.5,
                     font=dict(size=18, color="#14273A"), showarrow=False)
            ],
        )
        st.plotly_chart(fig, use_container_width=True)

# =====================================================
# 7. MACHINE DETAILS (Fit-in Table)
# =====================================================

st.html(
    '<div id="machine-details"></div>'
    '<div class="section-label">MACHINE DETAILS</div>'
    '<div class="section-title">All machines — complete status</div>'
)

machine_details = pd.DataFrame(
    {
        "ID": [f"M-{i:02d}" for i in range(1, 13)],
        "Machine": [
            "Packaging Line", "Hydraulic Press", "Injection Molder", "CNC Mill",
            "Welding Robot", "Lathe", "Air Compressor", "Cooling System",
            "Boiler Feed Pump", "Conveyor", "Paint Booth Fan", "Laser Cutter",
        ],
        "Status": [
            "Healthy", "Healthy", "Healthy", "Warning", "Healthy", "Healthy",
            "Critical", "Healthy", "Healthy", "Warning", "Healthy", "Healthy",
        ],
        "Health %": [94, 92, 90, 76, 93, 89, 58, 91, 88, 79, 92, 90],
        "Temp (°C)": [61, 58, 64, 72, 66, 59, 87, 65, 70, 79, 55, 62],
        "Vibration (mm/s)": [2.4, 2.1, 2.8, 5.4, 2.6, 2.2, 8.2, 3.2, 3.0, 6.1, 2.3, 2.5],
        "Pressure (bar)": [6.8, 7.0, 6.9, 6.9, 6.7, 6.6, 7.8, 6.5, 7.1, 7.2, 6.4, 6.8],
        "Risk Score": [14, 22, 18, 64, 16, 20, 92, 35, 24, 58, 15, 19],
        "Time to Limit": [
            "Safe", "Safe", "Safe", "6 days", "Safe", "Safe",
            "2.5 days", "12 days", "Safe", "9 days", "Safe", "Safe",
        ],
        "Status Note": [
            "Operating normally", "Normal operating condition", "Operating normally",
            "Vibration drifting upward", "Operating normally", "Operating normally",
            "Bearing wear: vibration 2.8x normal", "Temperature fluctuation",
            "Operating normally", "Motor temperature spikes", "Operating normally",
            "Operating normally",
        ],
    }
)

view = st.radio(
    "Show",
    ["All machines", "Healthy", "Needs attention", "High priority"],
    horizontal=True,
    key="details_filter",
    label_visibility="collapsed",
)

if view == "Healthy":
    shown = machine_details[machine_details["Status"] == "Healthy"]
elif view == "Needs attention":
    shown = machine_details[machine_details["Status"] != "Healthy"]
elif view == "High priority":
    shown = machine_details[machine_details["Risk Score"] >= 80]
else:
    shown = machine_details

with st.container(border=True):
    st.dataframe(
        shown.sort_values("Risk Score", ascending=False),
        use_container_width=True,
        hide_index=True,
        height=min(470, 40 + 35 * len(shown)),
        column_config={
            "ID": st.column_config.TextColumn("ID", width="small"),
            "Machine": st.column_config.TextColumn("Machine", width="medium"),
            "Status": st.column_config.TextColumn("Status", width="small"),
            "Health %": st.column_config.ProgressColumn(
                "Health", min_value=0, max_value=100, format="%d%%", width="small"
            ),
            "Temp (°C)": st.column_config.NumberColumn("Temp", format="%d°C", width="small"),
            "Vibration (mm/s)": st.column_config.NumberColumn("Vib.", format="%.1f mm/s", width="small"),
            "Pressure (bar)": st.column_config.NumberColumn("Press.", format="%.1f bar", width="small"),
            "Risk Score": st.column_config.ProgressColumn(
                "Risk", min_value=0, max_value=100, format="%d", width="small"
            ),
            "Time to Limit": st.column_config.TextColumn("Limit", width="small"),
            "Status Note": st.column_config.TextColumn("Status Note", width="medium"),
        },
    )