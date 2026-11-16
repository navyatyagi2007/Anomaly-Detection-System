import base64

import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.notifications import render_notifications

# =====================================================
# 1. PAGE CONFIG
# =====================================================

st.set_page_config(
    page_title="ANOMATRIX | Dashboard",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# =====================================================
# 2. SIDEBAR LOGO (top of sidebar, above navigation)
# =====================================================

LOGO_SVG = """
<svg xmlns="http://www.w3.org/2000/svg" width="310" height="84" viewBox="0 0 310 84">
  <defs>
    <linearGradient id="g" x1="0" y1="0" x2="1" y2="1">
      <stop offset="0" stop-color="#3FA0E0"/>
      <stop offset="1" stop-color="#0F2F4E"/>
    </linearGradient>
  </defs>
  <rect x="2" y="6" width="72" height="72" rx="19" fill="url(#g)"/>
  <circle cx="38" cy="42" r="23" fill="none" stroke="#FFFFFF" stroke-width="8.5"
          stroke-dasharray="7.6 7.6"/>
  <circle cx="38" cy="42" r="16.5" fill="none" stroke="#FFFFFF" stroke-width="4.2"/>
  <circle cx="38" cy="42" r="6.5" fill="#FFFFFF"/>
  <text x="88" y="45" textLength="216" lengthAdjust="spacingAndGlyphs"
        font-family="Inter, Segoe UI, Arial, sans-serif" font-size="33" font-weight="900"
        fill="#0F2A45" stroke="#0F2A45" stroke-width="0.9">ANOMATRIX</text>
  <text x="89" y="65" textLength="214" lengthAdjust="spacing"
        font-family="Consolas, Menlo, monospace" font-size="11" font-weight="700"
        fill="#3F5A72">INDUSTRIAL INTELLIGENCE</text>
</svg>
"""

logo_uri = "data:image/svg+xml;base64," + base64.b64encode(
    LOGO_SVG.encode("utf-8")
).decode("utf-8")

st.logo(logo_uri, size="large")

# =====================================================
# 3. CSS
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
[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

.block-container { max-width: 1500px; padding-top: 1.4rem; padding-bottom: 2rem; }

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
}
.page-title { font-size: 36px; font-weight: 800; color: #14273A; margin: 2px 0 4px; line-height: 1.1; }
.page-sub { color: #5B6F7E; font-size: 14px; max-width: 760px; }

/* Action Planner button (top right) */
[data-testid="stDownloadButton"] button {
    background: rgba(255,255,255,0.92); border: 1px solid #F1D3D8;
    border-radius: 16px; height: 3.8rem;
    box-shadow: 0 8px 22px rgba(190,70,90,0.12);
    transition: all .25s ease;
}
[data-testid="stDownloadButton"] button p {
    font-family: 'JetBrains Mono', monospace; letter-spacing: 2.5px;
    font-weight: 700; font-size: 13px; color: #B03A4E;
}
[data-testid="stDownloadButton"] button:hover {
    transform: translateY(-3px); border-color: #E5536A;
    box-shadow: 0 14px 30px rgba(190,70,90,0.22); background: #FFFFFF;
}

.divider { border: none; border-top: 1px solid #C9D6E0; margin: 14px 0 16px; }

/* ---------- COMPACT ALERT BANNER ---------- */
.alert-banner {
    background: linear-gradient(120deg, #FDE0E4 0%, #FCE9EC 60%, #FDEFF1 100%);
    border: 1px solid #F6D0D6; border-radius: 18px; padding: 15px 22px;
    display: flex; justify-content: space-between; align-items: center; gap: 18px;
    margin-top: 6px;
    box-shadow: 0 10px 24px rgba(190,70,90,0.09);
    transition: all .3s ease;
}
.alert-banner:hover { transform: translateY(-2px); box-shadow: 0 14px 30px rgba(190,70,90,0.15); }
.alert-tag { font-family: 'JetBrains Mono', monospace; letter-spacing: 2.5px;
    font-size: 10px; font-weight: 700; color: #B03A4E; }
.alert-tag .dot { display:inline-block; width:7px; height:7px; border-radius:50%;
    background:#E5536A; margin-right:7px; animation: pulse 1.6s infinite; }
@keyframes pulse { 0%{box-shadow:0 0 0 0 rgba(229,83,106,.55);} 70%{box-shadow:0 0 0 8px rgba(229,83,106,0);} 100%{box-shadow:0 0 0 0 rgba(229,83,106,0);} }
.alert-title { font-size: 19px; font-weight: 800; color: #1F2D3A; margin-top: 4px; line-height: 1.25; }
.alert-desc { color: #6B5A60; font-size: 13px; margin-top: 2px; }
.chip-row { display: flex; flex-wrap: wrap; gap: 8px; margin-top: 9px; }
.chip {
    display: inline-flex; align-items: center; gap: 5px;
    background: #FFFFFF; border-radius: 999px; padding: 5px 11px;
    font-size: 11.5px; font-weight: 500; color: #45535D;
}
.sev-box {
    background: #FFFFFF; border-radius: 14px; padding: 11px 18px; min-width: 118px;
    text-align: left; flex-shrink: 0;
    box-shadow: 0 4px 14px rgba(0,0,0,0.05);
}
.sev-box .l { font-family: 'JetBrains Mono', monospace; letter-spacing: 2px;
    font-size: 9.5px; color: #6F7C86; }
.sev-box .v { font-size: 19px; font-weight: 700; color: #1F2D3A; margin-top: 3px; }
.sev-box .v span { color: #E5536A; margin-right: 6px; font-size: 15px; }

/* ---------- KPI CARDS ---------- */
.section-label { font-family: 'JetBrains Mono', monospace; letter-spacing: 3px;
    font-size: 11px; color: #6F8496; margin-top: 24px; }
.section-title { font-size: 23px; font-weight: 800; color: #14273A; margin: 3px 0 14px; }

.kpi-card {
    position: relative; overflow: hidden;
    background: linear-gradient(145deg, #FFFFFF 0%, #F7FBFF 100%);
    border: 1px solid #DCE7F0; border-radius: 18px;
    padding: 18px 20px 20px; min-height: 146px;
    box-shadow: 0 6px 18px rgba(35,75,110,0.06);
    transition: all .28s ease;
}
.kpi-card::before {
    content: ""; position: absolute; right: -40px; top: -40px;
    width: 140px; height: 140px; border-radius: 50%;
    background: radial-gradient(circle, var(--c) 0%, transparent 70%); opacity: .14;
}
.kpi-card:hover { transform: translateY(-5px); box-shadow: 0 14px 28px rgba(35,75,110,0.15); border-color: var(--c); }
.kpi-label { font-family: 'JetBrains Mono', monospace; font-size: 11px;
    letter-spacing: 2.2px; color: #6F7C86; font-weight: 500; }
.kpi-link { display: block; text-decoration: none !important; color: inherit !important; }
.kpi-more { position: absolute; right: 18px; bottom: 14px; font-size: 12px; font-weight: 600;
    color: var(--c); opacity: 0; transform: translateX(-6px); transition: all .25s ease; }
.kpi-card:hover .kpi-more { opacity: 1; transform: translateX(0); }
html, [data-testid="stMain"], section.main { scroll-behavior: smooth; }
#machine-details { scroll-margin-top: 70px; }
.kpi-value { font-size: 36px; font-weight: 800; color: #14273A; margin-top: 14px; line-height: 1; }
.kpi-desc { font-size: 12.5px; color: #7A8791; margin-top: 7px; }
.kpi-line { position: absolute; left: 20px; bottom: 0; height: 4px; width: 44px;
    border-radius: 4px 4px 0 0; background: var(--c); }

/* ---------- PANELS ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: rgba(255,255,255,0.75); border-radius: 20px; border-color: #D6E1EA;
    box-shadow: 0 6px 18px rgba(35,75,110,0.05); transition: all .25s ease;
}
[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 12px 26px rgba(35,75,110,0.10); border-color: #9CC8E2;
}
.panel-title { font-size: 18px; font-weight: 800; color: #14273A; margin-bottom: 14px; }

.risk-row { margin-bottom: 18px; }
.risk-head { display:flex; justify-content:space-between; align-items:baseline; }
.risk-name { font-weight: 700; color: #1F3547; font-size: 15px; }
.risk-meta { font-size: 12px; color: #7A8791; margin-top: 2px; }
.risk-score { font-weight: 800; font-size: 18px; }
.bar { height: 8px; border-radius: 8px; background: #E6EEF5; margin-top: 8px; overflow: hidden; }
.bar > div { height: 100%; border-radius: 8px; }
.tag { font-family:'JetBrains Mono',monospace; font-size:10px; letter-spacing:1.5px;
    padding: 3px 9px; border-radius: 999px; font-weight: 700; margin-left: 8px; }

hr { border-color: #D5E0E9; }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# 4. SIDEBAR BOTTOM : PROFILE + LOGOUT
# =====================================================

with st.sidebar:
    st.html(
        """
        <div class="user-card">
            <div class="user-avatar">PA</div>
            <div>
                <div class="user-name">Plant Admin</div>
                <div class="user-role">Factory Operations</div>
            </div>
        </div>
        """
    )

    if st.button("⇦  Log out", use_container_width=True, key="logout_btn"):
        st.session_state["logged_in"] = False
        st.session_state.pop("selected_action", None)
        st.rerun()

# =====================================================
# 5. NOTIFICATIONS
# =====================================================

render_notifications()

# =====================================================
# 5b. HEADER
# =====================================================

h_left, h_right = st.columns([4, 1])

with h_left:
    st.html(
        """
        <div class="eyebrow">ANOMATRIX · Command Center</div>
        <div class="page-title">Factory Command Center</div>
        <div class="page-sub">A unified view of machine health, active alerts and
        maintenance risk across the plant — all in one place.</div>
        """
    )

PLAN_ACTIONS = [
    ("M-07 Air Compressor", "HIGH", "Day 1", "Technician A",
     "Inspect bearings and check shaft alignment. Vibration is 2.8x normal; limit expected in ~2.5 days."),
    ("M-04 CNC Mill", "MEDIUM", "Day 2", "Technician B",
     "Vibration check. Reading is drifting upward; limit expected in ~6 days."),
    ("M-10 Conveyor", "MEDIUM", "Day 3", "Technician C",
     "Motor inspection. Temperature spikes observed; limit expected in ~9 days."),
    ("M-08 Cooling System", "LOW", "Day 5", "Technician A",
     "Filter replacement. Temperature fluctuation; limit expected in ~12 days."),
]


def build_action_plan():
    """Build the action plan from the current dashboard data. PDF if reportlab exists, else text."""
    stamp = pd.Timestamp.now().strftime("%d %b %Y, %I:%M %p")
    summary = (
        "12 machines registered | 9 healthy | 3 anomalies flagged | "
        "1 high priority | average health 86%"
    )
    try:
        from io import BytesIO

        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=A4, leftMargin=18 * mm, rightMargin=18 * mm,
                                topMargin=18 * mm, bottomMargin=18 * mm,
                                title="ANOMATRIX Action Plan")
        ss = getSampleStyleSheet()
        h1 = ParagraphStyle("h1", parent=ss["Title"], textColor=colors.HexColor("#183B5B"), alignment=0)
        h2 = ParagraphStyle("h2", parent=ss["Heading2"], textColor=colors.HexColor("#183B5B"))
        cell = ParagraphStyle("cell", parent=ss["BodyText"], fontSize=9, leading=12)
        head = ParagraphStyle("head", parent=cell, textColor=colors.white, fontName="Helvetica-Bold")

        rows = [[Paragraph(t, head) for t in ["#", "Machine", "Priority", "When", "Owner", "Action"]]]
        for i, (m, p, d, o, a) in enumerate(PLAN_ACTIONS, 1):
            rows.append([Paragraph(str(i), cell), Paragraph(f"<b>{m}</b>", cell),
                         Paragraph(p, cell), Paragraph(d, cell), Paragraph(o, cell), Paragraph(a, cell)])

        tbl = Table(rows, colWidths=[8 * mm, 32 * mm, 20 * mm, 15 * mm, 24 * mm, 75 * mm], repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183B5B")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F6FC")]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D9E7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
            ("BACKGROUND", (2, 1), (2, 1), colors.HexColor("#FDE3E7")),
        ]))

        doc.build([
            Paragraph("ANOMATRIX - Maintenance Action Plan", h1),
            Paragraph(f"Generated: {stamp}", ss["Normal"]),
            Spacer(1, 6 * mm),
            Paragraph("Factory summary", h2),
            Paragraph(summary, ss["BodyText"]),
            Spacer(1, 4 * mm),
            Paragraph("Priority actions", h2),
            tbl,
            Spacer(1, 6 * mm),
            Paragraph("Illustrative mock data - not live sensor data.", ss["Italic"]),
        ])
        return buf.getvalue(), "anomatrix_action_plan.pdf", "application/pdf"
    except ImportError:
        lines = ["ANOMATRIX - Maintenance Action Plan", f"Generated: {stamp}", "", summary, ""]
        for i, (m, p, d, o, a) in enumerate(PLAN_ACTIONS, 1):
            lines += [f"{i}. {m} [{p}] - {d} ({o})", f"   {a}", ""]
        lines.append("Illustrative mock data - not live sensor data.")
        return "\n".join(lines).encode("utf-8"), "anomatrix_action_plan.txt", "text/plain"


with h_right:
    plan_bytes, plan_name, plan_mime = build_action_plan()
    st.download_button(
        "ACTION PLANNER  ›",
        data=plan_bytes,
        file_name=plan_name,
        mime=plan_mime,
        key="action_planner_btn",
        use_container_width=True,
        help="Click to generate and download the action plan",
    )

st.html('<hr class="divider">')

# =====================================================
# 6. KPI CARDS (8 Cards First on Screen)
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
        st.write("")

# =====================================================
# 7. COMPACT ACTIVE ALERT BANNER (Below the 8 Cards)
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
# 8. QUICK SNAPSHOT : TOP RISKS + HEALTH SPLIT
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
            height=250,
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
# 9. MACHINE DETAILS (cards above link here)
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

st.caption("Prototype v1.0 · Illustrative mock data · Not live sensor data")