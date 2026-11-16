import base64

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st

from components.notifications import render_notifications

# =====================================================
# 0. QUICK SWITCHES
# =====================================================

SHOW_MACHINE_IMAGE = True   # False = side panel / popup me machine ki illustration hat jayegi
MAP_HEIGHT = 345            # Balanced factory map height

# =====================================================
# 1. PAGE CONFIG
# =====================================================

try:
    st.set_page_config(
        page_title="ANOMATRIX | Machine Explorer",
        page_icon="⚙️",
        layout="wide",
        initial_sidebar_state="expanded",
    )
except Exception:
    pass

NOW = pd.Timestamp.now().floor("h")

# =====================================================
# 2. SIDEBAR LOGO
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

st.logo(
    "data:image/svg+xml;base64," + base64.b64encode(LOGO_SVG.encode("utf-8")).decode("utf-8"),
    size="large",
)

# =====================================================
# 3. CSS (LARGER DASHBOARD-STYLE HEADINGS ONLY)
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
[data-testid="stHeader"] { background: transparent; height: 2.2rem; }
footer { visibility: hidden; }
.block-container { max-width: 1560px; padding-top: 0.6rem !important; padding-bottom: 1rem !important; }
html, [data-testid="stMain"], section.main { scroll-behavior: smooth; }
#machine-profile { scroll-margin-top: 48px; }

/* ---------- SIDEBAR ---------- */
[data-testid="stSidebar"] { background: #EDEAE4; border-right: 1px solid #DDD8D0; }
[data-testid="stSidebarLogo"], [data-testid="stLogo"], [data-testid="stSidebarHeader"] img {
    height: 4.8rem !important; width: auto !important;
    max-width: 100% !important; object-fit: contain;
}
[data-testid="stSidebarHeader"] {
    height: auto; padding-top: 1.1rem; padding-bottom: 0.9rem;
    border-bottom: 1px solid #DDD8D0;
}
[data-testid="stSidebarContent"] { display: flex; flex-direction: column; }
[data-testid="stSidebarUserContent"] { margin-top: auto; padding-bottom: 1rem; padding-top: 0; }
[data-testid="stSidebarUserContent"] [data-testid="stElementContainer"]:not(:has(.user-card)):not(:has(.stButton)) {
    display: none !important;
}
[data-testid="stSidebar"] .stButton > button {
    background: #FFFFFF; color: #183B5B; border: 1px solid #D9D4CB;
    border-radius: 12px; font-weight: 650; height: 2.6rem; font-size: 14px;
}
[data-testid="stSidebar"] .stButton > button:hover {
    border-color: #328BC5; color: #17628D; background: #F4FAFE;
}
.user-card {
    display: flex; gap: 12px; align-items: center;
    background: #E4E0D8; border-radius: 14px; padding: 12px; margin-bottom: 10px;
}
.user-avatar {
    width: 38px; height: 38px; border-radius: 50%;
    background: #D3E8F6; color: #17628D; font-weight: 800; font-size: 13px;
    display: flex; align-items: center; justify-content: center; flex-shrink: 0;
}
.user-name { font-weight: 700; font-size: 14px; color: #183B5B; }
.user-role { font-size: 12px; color: #6F7C86; }

/* ---------- HEADINGS (ENLARGED TO MATCH DASHBOARD) ---------- */
.eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 11.5px;
    letter-spacing: 3px; color: #6F8496; text-transform: uppercase; font-weight: 600; }
.page-title { font-size: 40px; font-weight: 800; color: #14273A; margin: 3px 0 5px;
    line-height: 1.08; letter-spacing: -0.02em; }
.page-sub { color: #5B6F7E; font-size: 14px; max-width: 780px; }
.divider { border: none; border-top: 1px solid #C9D6E0; margin: 10px 0 10px; }

.count-pill {
    display: flex; justify-content: space-around; gap: 6px;
    background: #FFFFFF; border: 1px solid #E1E5EB;
    border-radius: 16px; padding: 8px 10px; box-shadow: 0 6px 18px rgba(20,39,58,0.07);
    margin-bottom: 6px;
}
.count-pill .n { font-size: 22px; font-weight: 800; line-height: 1; text-align: center; }
.count-pill .l { font-family: 'JetBrains Mono', monospace; font-size: 9.5px; letter-spacing: 1.8px;
    color: #6F7C86; margin-top: 4px; text-align: center; }

.section-label { font-family: 'JetBrains Mono', monospace; letter-spacing: 3px;
    font-size: 11.5px; color: #6F8496; margin-top: 14px; text-transform: uppercase; font-weight: 600; }
.section-title { font-size: 25px; font-weight: 800; color: #14273A; margin: 2px 0 8px;
    line-height: 1.15; letter-spacing: -0.015em; }

/* ---------- PANELS (white cards) ---------- */
[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF; border-radius: 18px; border: 1px solid #E1E5EB;
    box-shadow: 0 6px 20px rgba(20,39,58,0.07);
    padding: 0.85rem !important;
}
.panel-title { font-size: 18px; font-weight: 800; color: #14273A; margin-bottom: 8px; letter-spacing: -0.01em; }
.panel-sub { font-size: 12.5px; color: #7A8791; margin: -4px 0 8px; }

/* inputs */
[data-baseweb="select"] > div { background: #FFFFFF !important; border-radius: 12px !important;
    border-color: #D5DCE4 !important; }
[data-testid="stRadio"] label p { font-size: 13px; }
.stTabs [data-baseweb="tab-list"] { gap: 6px; }
.stTabs [data-baseweb="tab"] { font-weight: 650; font-size: 13.5px; }

/* map legend */
.legend-row { display: flex; flex-wrap: wrap; gap: 14px; align-items: center;
    font-size: 12.5px; color: #4B5E6D; margin: 0; }
.lg-dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 6px; vertical-align: 0; }
.lg-line { display: inline-block; width: 22px; border-top: 2.5px dotted var(--c); margin-right: 6px; vertical-align: 3px; }
.lg-hint { margin-left: auto; font-family: 'JetBrains Mono', monospace; font-size: 10.5px;
    letter-spacing: 1.5px; color: #6F8496; }

/* selected machine panel */
.mx-panel { background: #FFFFFF; border: 1px solid #E1E5EB; border-radius: 18px;
    padding: 14px; box-shadow: 0 6px 20px rgba(20,39,58,0.07); }
.mx-img { width: 100%; max-height: 125px; object-fit: contain; display: block; border-radius: 12px; }
.mx-head { display: flex; justify-content: space-between; align-items: flex-start; gap: 8px; margin-top: 8px; }
.mx-id { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; letter-spacing: 2px; color: #6F8496; }
.mx-name { font-size: 21px; font-weight: 800; color: #14273A; margin-top: 2px; line-height: 1.15; }
.status-chip { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; letter-spacing: 1.5px;
    font-weight: 700; padding: 5px 11px; border-radius: 999px; white-space: nowrap; }
.status-chip.crit { animation: pulse 1.8s ease-in-out infinite; }
@keyframes pulse { 0%,100% { box-shadow: 0 0 0 0 rgba(230,93,112,.45); } 50% { box-shadow: 0 0 0 7px rgba(230,93,112,0); } }
.mx-bar-label { display: flex; justify-content: space-between; font-size: 12.5px; color: #6F7C86; margin: 8px 0 4px; }
.bar { height: 7px; border-radius: 7px; background: #ECEEF2; overflow: hidden; }
.bar > div { height: 100%; border-radius: 7px; }
.mx-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; margin-top: 9px; }
.mx-tile { background: #F7F8FA; border: 1px solid #E8EBF0; border-radius: 12px; padding: 7px 11px; }
.mx-tile .l { font-family: 'JetBrains Mono', monospace; font-size: 9.5px; letter-spacing: 1.6px; color: #7A8791; }
.mx-tile .v { font-size: 18px; font-weight: 800; margin-top: 2px; }
.mx-tile .u { font-size: 11px; font-weight: 600; color: #7A8791; margin-left: 3px; }
.mx-foot { display: flex; justify-content: space-between; font-size: 12.5px; color: #5B6F7E; margin-top: 9px; }
.mx-link { display: block; text-align: center; margin-top: 9px; padding: 8px; border-radius: 12px;
    background: #183B5B; color: #FFFFFF !important; font-weight: 650; font-size: 13.5px;
    text-decoration: none !important; transition: all .2s ease; }
.mx-link:hover { background: #17628D; }

/* key-value tables */
.kv { width: 100%; border-collapse: collapse; }
.kv td { padding: 6px 8px; border-bottom: 1px solid #EEF0F3; font-size: 13px; }
.kv tr:nth-child(even) td { background: #FAFBFC; }
.kv tr:last-child td { border-bottom: none; }
.kv td:first-child { color: #6F7C86; width: 44%; }
.kv td:last-child { color: #14273A; font-weight: 600; }

/* sensor table */
.stbl { width: 100%; border-collapse: collapse; font-size: 13px; margin-bottom: 6px; }
.stbl th { text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1.6px;
    color: #6F7C86; font-weight: 500; padding: 7px 8px; background: #F4F6F9; }
.stbl th:first-child { border-radius: 10px 0 0 10px; }
.stbl th:last-child { border-radius: 0 10px 10px 0; }
.stbl td { padding: 7px 8px; border-bottom: 1px solid #EEF0F3; color: #263746; }
.stbl tr:last-child td { border-bottom: none; }
.stbl td:first-child { font-weight: 700; color: #14273A; }
.state-pill { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 999px; }

/* mini stats above timelines */
.ms-row { display: flex; gap: 8px; margin: 4px 0 4px; flex-wrap: wrap; }
.ms { flex: 1; min-width: 90px; background: #F7F8FA; border: 1px solid #E8EBF0; border-radius: 12px; padding: 6px 10px; }
.ms .l { font-family: 'JetBrains Mono', monospace; font-size: 9.5px; letter-spacing: 1.6px; color: #7A8791; }
.ms .v { font-size: 17px; font-weight: 800; color: #14273A; margin-top: 2px; }

/* outlook tiles / risk-queue cards / alerts / diagnosis */
.ol-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 8px; }
.ol { background: #F7F8FA; border: 1px solid #E8EBF0; border-radius: 12px; padding: 7px 10px; }
.ol .l { font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 1.5px; color: #7A8791; }
.ol .v { font-size: 16px; font-weight: 800; color: #14273A; margin-top: 2px; }

.rq-top { display: flex; justify-content: space-between; align-items: center; }
.rq-name { font-size: 15.5px; font-weight: 800; color: #14273A; margin-top: 4px; }
.rq-id { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1.6px; color: #7A8791; }
.rq-meta { display: flex; justify-content: space-between; font-size: 12.5px; color: #6F7C86; margin: 6px 0 4px; }

.al-row { display: flex; gap: 10px; align-items: center; padding: 7px 4px; border-bottom: 1px solid #EEF0F3; font-size: 13px; }
.al-row:last-child { border-bottom: none; }
.al-row b { color: #14273A; }

.dx { display: flex; gap: 10px; padding: 9px 12px; border-radius: 12px; background: #F7F8FA;
    border: 1px solid #E8EBF0; border-left: 5px solid var(--c); margin-bottom: 7px; }
.dx .ic { font-size: 20px; line-height: 1.2; }
.dx .t { font-weight: 800; color: #14273A; font-size: 14px; }
.dx .d { color: #5B6F7E; font-size: 13px; margin-top: 2px; line-height: 1.35; }
.act { display: flex; gap: 10px; align-items: flex-start; padding: 5px 2px; font-size: 13.5px; color: #263746; }
.act .n { width: 21px; height: 21px; border-radius: 50%; background: #183B5B; color: #fff; font-size: 11px;
    font-weight: 700; display: flex; align-items: center; justify-content: center; flex-shrink: 0; margin-top: 1px; }

/* subsystem health bars */
.sub-row { margin-bottom: 9px; }
.sub-lbl { display: flex; justify-content: space-between; font-size: 13px; font-weight: 600; color: #34495A; margin-bottom: 4px; }

/* comparison table */
.cmp { width: 100%; border-collapse: collapse; }
.cmp th { font-size: 13px; font-weight: 800; color: #14273A; text-align: left; padding: 8px 10px;
    background: #F4F6F9; }
.cmp th:first-child { border-radius: 10px 0 0 10px; }
.cmp th:last-child { border-radius: 0 10px 10px 0; }
.cmp td { padding: 7px 10px; border-bottom: 1px solid #EEF0F3; font-size: 13.5px; color: #263746; }
.cmp td:first-child { color: #6F7C86; }
.cmp td.good { color: #16865D; font-weight: 800; background: #EAF7F1; }
.cmp td.bad { color: #C23A4F; font-weight: 800; background: #FDEEF0; }
.cmp td.dl { color: #6F7C86; font-family: 'JetBrains Mono', monospace; font-size: 12.5px; }
.verdict { margin-top: 9px; padding: 9px 14px; border-radius: 12px; background: #FFF8EA;
    border: 1px solid #F3E3BF; border-left: 5px solid #E5A04B; font-size: 13.5px; color: #34495A; }
.dot { display: inline-block; width: 10px; height: 10px; border-radius: 50%; margin-right: 7px; }

/* popup dialog */
div[role="dialog"] { border-radius: 20px !important; background: #FFFFFF !important; }
hr { border-color: #D5E0E9; margin: 10px 0; }
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
    if st.button("⇦  Log out", use_container_width=True, key="logout_btn_mi"):
        st.session_state["logged_in"] = False
        st.rerun()

# =====================================================
# 5. MOCK DATA
# =====================================================

STATUS_COLOR = {"Healthy": "#20A77A", "Warning": "#E5A04B", "Critical": "#E65D70"}
STATUS_BG = {"Healthy": "#E0F4EA", "Warning": "#FDF0D9", "Critical": "#FDE3E7"}
STATE_COLOR = {"OK": "#14273A", "Watch": "#C77F1F", "Alert": "#C23A4F"}
STATE_BG = {"OK": "#E0F4EA", "Watch": "#FDF0D9", "Alert": "#FDE3E7"}

ZONES = [
    ("📦  RECEIVING & PACKAGING", 1, 37, 31, 61, "#E3F0FA"),
    ("⚙️  MACHINING BAY", 33, 37, 66, 61, "#E6F3EC"),
    ("🔨  PRESS & MOLDING", 68, 37, 99, 61, "#F6EFE5"),
    ("🎨  FABRICATION & PAINT", 1, 1, 31, 26, "#ECE9F6"),
    ("🔋  UTILITY YARD", 33, 1, 99, 26, "#E4F1F4"),
]

ICON = dict(compressor="🌬️", press="🔨", molder="🏭", cnc="⚙️", lathe="🔩", laser="⚡",
            robot="🦾", conveyor="➡️", packaging="📦", cooling="❄️", pump="💧", fan="🌀")


def M(id_, name, type_, zone, x, y, status, health, temp, vib, press, rpm, risk, limit,
      mfr, model, serial, install, hours, last, nxt, specs):
    return dict(id=id_, name=name, type=type_, zone=zone, x=x, y=y, status=status, health=health,
                temp=temp, vib=vib, press=press, rpm=rpm, risk=risk, limit=limit, mfr=mfr,
                model=model, serial=serial, install=install, hours=hours, last=last, next=nxt,
                specs=specs)


MACHINES = [
    M("M-01", "Packaging Line", "packaging", "Receiving & Packaging", 12, 50, "Healthy", 94, 61, 2.4, 6.8, 1450, 14, "Safe",
      "Norvik Packaging", "NP-420 Line", "NP420-1187", "03 Feb 2020", 31200, "02 Oct 2026", "02 Jan 2027",
      [("Throughput", "120 packs / min"), ("Drive power", "11 kW"), ("Format range", "100 – 450 mm"), ("Air supply", "6 bar")]),
    M("M-02", "Hydraulic Press", "press", "Press & Molding", 76, 52, "Healthy", 92, 58, 2.1, 7.0, 1480, 22, "Safe",
      "Brandt Hydraulics", "BH-250T", "BH250-0932", "21 Aug 2018", 44800, "18 Sep 2026", "18 Dec 2026",
      [("Press force", "250 tonnes"), ("Stroke", "600 mm"), ("Pump power", "45 kW"), ("Working pressure", "280 bar")]),
    M("M-03", "Injection Molder", "molder", "Press & Molding", 90, 46, "Healthy", 90, 64, 2.8, 6.9, 1460, 18, "Safe",
      "Kestrel Molding", "KM-180i", "KM180-2204", "09 Nov 2019", 38900, "25 Sep 2026", "25 Dec 2026",
      [("Clamp force", "180 tonnes"), ("Shot volume", "420 cm³"), ("Barrel heating", "18 kW"), ("Cycle time", "22 s")]),
    M("M-04", "CNC Mill", "cnc", "Machining Bay", 42, 52, "Warning", 76, 72, 5.4, 6.9, 8000, 64, "6 days",
      "Tessen Machining", "TX-5 Vertical Mill", "TX5-3345", "12 Jun 2021", 26400, "30 Aug 2026", "Day 2",
      [("Spindle speed", "up to 10,000 rpm"), ("Spindle power", "22 kW"), ("Axis travel", "800 × 500 × 500 mm"), ("Tool magazine", "30 tools")]),
    M("M-05", "Welding Robot", "robot", "Fabrication & Paint", 10, 14, "Healthy", 93, 66, 2.6, 6.7, 3000, 16, "Safe",
      "Arcwright Robotics", "AR-6 Weld Cell", "AR6-0718", "17 Mar 2022", 19800, "05 Oct 2026", "05 Jan 2027",
      [("Payload", "12 kg"), ("Reach", "1,440 mm"), ("Axes", "6"), ("Repeatability", "± 0.05 mm")]),
    M("M-06", "Lathe", "lathe", "Machining Bay", 52, 44, "Healthy", 89, 59, 2.2, 6.6, 1800, 20, "Safe",
      "Tessen Machining", "TL-280 Lathe", "TL280-2261", "28 Jan 2020", 35100, "11 Sep 2026", "11 Dec 2026",
      [("Max swing", "280 mm"), ("Spindle power", "15 kW"), ("Max speed", "3,500 rpm"), ("Centre distance", "650 mm")]),
    M("M-07", "Air Compressor", "compressor", "Utility Yard", 45, 14, "Critical", 58, 87, 8.2, 7.8, 2950, 92, "2.5 days",
      "Helios Compressors", "HC-75 Screw", "HC75-4410", "05 May 2017", 52600, "14 Jun 2026", "Day 1 (urgent)",
      [("Rated power", "75 kW"), ("Max pressure", "10 bar"), ("Free air delivery", "12.5 m³ / min"), ("Drive", "Direct-coupled, 2,950 rpm")]),
    M("M-08", "Cooling System", "cooling", "Utility Yard", 63, 10, "Healthy", 91, 65, 3.2, 6.5, 1450, 35, "12 days",
      "Cryon Thermal", "CT-300 Chiller", "CT300-0586", "30 Sep 2018", 47300, "20 Sep 2026", "Day 5",
      [("Cooling capacity", "300 kW"), ("Coolant flow", "55 m³ / h"), ("Pump power", "18.5 kW"), ("Setpoint", "18 °C")]),
    M("M-09", "Boiler Feed Pump", "pump", "Utility Yard", 85, 16, "Healthy", 88, 70, 3.0, 7.1, 2900, 24, "Safe",
      "Vantor Pumps", "VP-BF40", "VPBF-7782", "11 Dec 2019", 40200, "08 Sep 2026", "08 Dec 2026",
      [("Flow", "40 m³ / h"), ("Head", "180 m"), ("Motor power", "37 kW"), ("Stages", "8")]),
    M("M-10", "Conveyor", "conveyor", "Main Conveyor Aisle", 50, 31, "Warning", 79, 79, 6.1, 7.2, 1450, 58, "9 days",
      "Norvik Conveyors", "NC-Belt 12M", "NCB-1290", "19 Apr 2019", 41700, "22 Aug 2026", "Day 3",
      [("Belt length", "92 m"), ("Belt speed", "1.2 m / s"), ("Drive power", "22 kW"), ("Load capacity", "180 kg / m")]),
    M("M-11", "Paint Booth Fan", "fan", "Fabrication & Paint", 22, 8, "Healthy", 92, 55, 2.3, 6.4, 1750, 15, "Safe",
      "Aerofil Systems", "AF-900 Booth Fan", "AF900-3019", "02 Jul 2021", 23600, "29 Sep 2026", "29 Dec 2026",
      [("Airflow", "18,000 m³ / h"), ("Motor power", "15 kW"), ("Static pressure", "1,200 Pa"), ("Filtration", "G4 + F7")]),
    M("M-12", "Laser Cutter", "laser", "Machining Bay", 60, 54, "Healthy", 90, 62, 2.5, 6.8, 3000, 19, "Safe",
      "Lumen Photonics", "LP-3015 Fiber", "LP3015-5521", "14 Oct 2022", 15400, "13 Oct 2026", "13 Jan 2027",
      [("Laser power", "6 kW fiber"), ("Bed size", "3,000 × 1,500 mm"), ("Max sheet thickness", "25 mm steel"), ("Assist gas", "N₂ / O₂")]),
]
BY_ID = {m["id"]: m for m in MACHINES}
IDS = [m["id"] for m in MACHINES]
MARK_CURVE = 5

AIR_LINES = [("M-07", "M-04"), ("M-07", "M-02"), ("M-07", "M-05")]
COOL_LINES = [("M-08", "M-03"), ("M-08", "M-12"), ("M-08", "M-07")]
AIR_COLOR, COOL_COLOR = "#3B8FD0", "#1FB5A0"

SENSOR_MOUNTS = {
    "compressor": ("Bearing housing", "Motor DE bearing", "Discharge line"),
    "press": ("Hydraulic tank", "Pump housing", "Pump outlet"),
    "molder": ("Barrel zone 2", "Clamp frame", "Hydraulic manifold"),
    "cnc": ("Spindle housing", "Spindle nose", "Coolant line"),
    "lathe": ("Headstock", "Spindle bearing", "Coolant line"),
    "laser": ("Resonator", "Gantry axis", "Assist-gas line"),
    "robot": ("Joint 2 motor", "Wrist joint", "Pneumatic line"),
    "conveyor": ("Drive motor", "Gearbox", "Tensioner circuit"),
    "packaging": ("Seal bar", "Drive gearbox", "Air supply"),
    "cooling": ("Return water line", "Pump housing", "Loop header"),
    "pump": ("Motor winding", "Pump bearing", "Discharge line"),
    "fan": ("Motor housing", "Fan bearing", "Duct static"),
}

LIMITS = {
    "temp": dict(warn=75, alert=85),
    "vib": dict(warn=5.0, alert=7.1),
    "press": dict(low=5.5, high=8.0, watch=7.6),
}


def uptime(m):
    return round(99.6 - (100 - m["health"]) * 0.32, 1)


def sensor_state(m, key):
    v = m[key]
    if key in ("temp", "vib"):
        lim = LIMITS[key]
        return "Alert" if v >= lim["alert"] else "Watch" if v >= lim["warn"] else "OK"
    if key == "press":
        lim = LIMITS["press"]
        if v > lim["high"] or v < lim["low"]:
            return "Alert"
        return "Watch" if v >= lim["watch"] else "OK"
    return "OK"


def status_chip(status):
    extra = " crit" if status == "Critical" else ""
    return (f'<span class="status-chip{extra}" style="color:{STATUS_COLOR[status]};'
            f'background:{STATUS_BG[status]};">● {status.upper()}</span>')


def tiles_html(m):
    tiles = ""
    for key, label, unit in [("temp", "TEMPERATURE", "°C"), ("vib", "VIBRATION", "mm/s"),
                             ("press", "PRESSURE", "bar"), ("rpm", "SPEED", "rpm")]:
        val = f"{m[key]:,}" if key == "rpm" else f"{m[key]}"
        tiles += (f'<div class="mx-tile"><div class="l">{label}</div><div class="v" '
                  f'style="color:{STATE_COLOR[sensor_state(m, key)]}">{val}<span class="u">{unit}</span></div></div>')
    return f'<div class="mx-grid">{tiles}</div>'


def head_html(m):
    hc = STATUS_COLOR[m["status"]]
    return f"""
        <div class="mx-head">
            <div>
                <div class="mx-id">{m['id']} · {m['zone'].upper()}</div>
                <div class="mx-name">{ICON[m['type']]} {m['name']}</div>
            </div>
            {status_chip(m['status'])}
        </div>
        <div class="mx-bar-label"><span>Machine health</span><b style="color:{hc}">{m['health']}%</b></div>
        <div class="bar"><div style="width:{m['health']}%;background:{hc};"></div></div>
    """


def active_alerts():
    out = []
    for m in MACHINES:
        for k, lab, u in [("temp", "Temperature", "°C"), ("vib", "Vibration", "mm/s"), ("press", "Pressure", "bar")]:
            s = sensor_state(m, k)
            if s != "OK":
                out.append((m, lab, m[k], u, s))
    return sorted(out, key=lambda a: (a[4] != "Alert", -a[0]["risk"]))


def diagnose(m):
    t, v, p = (sensor_state(m, k) for k in ("temp", "vib", "press"))
    f = []
    if v != "OK" and t != "OK":
        f.append(("🔧", "Probable bearing / lubrication fault",
                  f"Vibration {m['vib']} mm/s and temperature {m['temp']} °C are elevated — bearing-wear signature.",
                  v if v == "Alert" else t))
    elif v != "OK":
        f.append(("📳", "Rising vibration", f"{m['vib']} mm/s above watch limit. Check alignment.", v))
    elif t != "OK":
        f.append(("🌡️", "Running hot", f"{m['temp']} °C above watch limit. Check cooling and load.", t))
    if p != "OK":
        f.append(("💨", "Pressure near upper limit",
                  f"{m['press']} bar vs {LIMITS['press']['high']} bar limit. Inspect valves.", p))
    if not f:
        f.append(("✅", "No anomalies detected", "All sensors inside normal operating bands.", "OK"))
    actions = {
        "Critical": ["Stop non-essential load & inspect within 24 h",
                     "Check bearing lubrication & replace worn parts",
                     "Keep standby unit ready to avoid stoppage"],
        "Warning": ["Plan inspection at next service window",
                    "Re-check sensor trends every shift",
                    "Verify lubrication and shaft alignment"],
        "Healthy": ["No immediate action needed", "Continue planned service schedule"],
    }[m["status"]]
    return f, actions


def diag_html(m):
    f, _ = diagnose(m)
    return "".join(
        f'<div class="dx" style="--c:{STATE_COLOR[s] if s != "OK" else "#20A77A"}"><div class="ic">{ic}</div>'
        f'<div><div class="t">{t}</div><div class="d">{d}</div></div></div>'
        for ic, t, d, s in f
    )


def actions_html(m):
    _, a = diagnose(m)
    return "".join(f'<div class="act"><div class="n">{i}</div><div>{x}</div></div>' for i, x in enumerate(a, 1))


def rul_text(m):
    return "30+ days" if m["limit"] == "Safe" else m["limit"]


# =====================================================
# 6. MACHINE ILLUSTRATIONS
# =====================================================

def _compressor(c, n, s, l, m):
    return f"""
    <rect x="86" y="164" width="14" height="10" fill="{n}"/><rect x="200" y="164" width="14" height="10" fill="{n}"/>
    <rect x="70" y="100" width="170" height="66" rx="33" fill="{s}"/>
    <rect x="80" y="106" width="150" height="14" rx="7" fill="#FFFFFF" opacity=".28"/>
    <rect x="112" y="58" width="76" height="42" rx="8" fill="{n}"/>
    <rect x="124" y="46" width="52" height="14" rx="4" fill="{m}"/>
    <rect x="242" y="92" width="52" height="74" rx="10" fill="{n}"/>
    <rect x="250" y="102" width="36" height="6" fill="{m}"/><rect x="250" y="114" width="36" height="6" fill="{m}"/>
    <rect x="250" y="126" width="36" height="6" fill="{m}"/>
    <path d="M188 80 H242" stroke="{n}" stroke-width="6"/>
    <circle cx="92" cy="78" r="14" fill="#FFFFFF" stroke="{n}" stroke-width="3"/>
    <path d="M92 78 L99 70" stroke="{c}" stroke-width="3" stroke-linecap="round"/>"""


def _press(c, n, s, l, m):
    return f"""
    <rect x="92" y="38" width="20" height="132" fill="{n}"/><rect x="208" y="38" width="20" height="132" fill="{n}"/>
    <rect x="92" y="38" width="136" height="26" rx="6" fill="{m}"/>
    <rect x="148" y="64" width="24" height="38" fill="{s}"/>
    <rect x="155" y="102" width="10" height="30" fill="{l}"/>
    <rect x="122" y="132" width="76" height="12" rx="3" fill="{n}"/>
    <rect x="100" y="144" width="120" height="26" rx="4" fill="{s}"/>
    <circle cx="258" cy="72" r="14" fill="#FFFFFF" stroke="{n}" stroke-width="3"/>
    <path d="M258 72 L264 64" stroke="{c}" stroke-width="3" stroke-linecap="round"/>
    <path d="M228 72 H244" stroke="{n}" stroke-width="4"/>"""


def _molder(c, n, s, l, m):
    return f"""
    <rect x="50" y="128" width="230" height="42" rx="6" fill="{n}"/>
    <path d="M70 66 L124 66 L110 100 L84 100 Z" fill="{s}"/>
    <rect x="62" y="100" width="118" height="26" rx="6" fill="{m}"/>
    <rect x="186" y="78" width="14" height="50" fill="{s}"/><rect x="236" y="78" width="14" height="50" fill="{s}"/>
    <rect x="200" y="92" width="36" height="24" fill="{l}"/>
    <rect x="250" y="94" width="30" height="34" rx="4" fill="{m}"/>
    <rect x="172" y="106" width="14" height="10" fill="{n}"/>"""


def _cnc(c, n, s, l, m):
    return f"""
    <rect x="70" y="56" width="190" height="114" rx="10" fill="{m}"/>
    <rect x="86" y="72" width="108" height="66" rx="6" fill="{l}"/>
    <rect x="132" y="76" width="14" height="30" fill="{n}"/><rect x="136" y="106" width="6" height="14" fill="{s}"/>
    <rect x="100" y="126" width="80" height="8" fill="{s}"/>
    <rect x="204" y="72" width="44" height="66" rx="6" fill="{n}"/>
    <rect x="210" y="80" width="32" height="18" rx="3" fill="{c}" opacity=".85"/>
    <circle cx="219" cy="116" r="4" fill="{s}"/><circle cx="233" cy="116" r="4" fill="{s}"/>
    <rect x="86" y="146" width="60" height="6" rx="3" fill="{l}" opacity=".7"/>"""


def _lathe(c, n, s, l, m):
    return f"""
    <rect x="60" y="136" width="210" height="34" rx="6" fill="{n}"/>
    <rect x="60" y="88" width="64" height="48" rx="6" fill="{m}"/>
    <circle cx="128" cy="114" r="18" fill="{s}"/><circle cx="128" cy="114" r="7" fill="{n}"/>
    <rect x="134" y="108" width="86" height="12" fill="{l}"/>
    <rect x="224" y="100" width="38" height="36" rx="5" fill="{m}"/>
    <rect x="150" y="92" width="22" height="16" fill="{c}" opacity=".85"/>
    <rect x="72" y="72" width="40" height="16" rx="4" fill="{n}"/>"""


def _laser(c, n, s, l, m):
    return f"""
    <rect x="60" y="120" width="200" height="50" rx="6" fill="{m}"/>
    <rect x="76" y="128" width="168" height="10" fill="{l}"/>
    <rect x="60" y="88" width="14" height="36" fill="{n}"/><rect x="246" y="88" width="14" height="36" fill="{n}"/>
    <rect x="60" y="82" width="200" height="12" rx="4" fill="{n}"/>
    <rect x="148" y="94" width="26" height="22" rx="4" fill="{s}"/>
    <path d="M161 116 V130" stroke="{c}" stroke-width="3"/><circle cx="161" cy="131" r="4" fill="{c}"/>
    <rect x="196" y="48" width="52" height="30" rx="6" fill="{s}"/><rect x="204" y="56" width="22" height="14" rx="3" fill="{l}"/>"""


def _robot(c, n, s, l, m):
    return f"""
    <rect x="112" y="152" width="96" height="18" rx="5" fill="{n}"/>
    <rect x="140" y="132" width="40" height="22" rx="6" fill="{m}"/>
    <path d="M160 134 L128 92" stroke="{s}" stroke-width="18" stroke-linecap="round"/>
    <path d="M128 92 L196 66" stroke="{s}" stroke-width="15" stroke-linecap="round"/>
    <path d="M196 66 L236 84" stroke="{n}" stroke-width="10" stroke-linecap="round"/>
    <circle cx="160" cy="134" r="11" fill="{n}"/><circle cx="128" cy="92" r="10" fill="{n}"/>
    <circle cx="196" cy="66" r="8" fill="{n}"/>
    <path d="M236 84 L246 100" stroke="{c}" stroke-width="4" stroke-linecap="round"/>
    <circle cx="248" cy="104" r="5" fill="{c}" opacity=".7"/>"""


def _conveyor(c, n, s, l, m):
    rollers = "".join(f'<circle cx="{x}" cy="139" r="5" fill="{s}"/>' for x in range(54, 270, 28))
    return f"""
    <rect x="70" y="150" width="8" height="20" fill="{m}"/><rect x="160" y="150" width="8" height="20" fill="{m}"/>
    <rect x="250" y="150" width="8" height="20" fill="{m}"/>
    <rect x="40" y="128" width="240" height="22" rx="11" fill="{n}"/>
    {rollers}
    <rect x="80" y="100" width="36" height="28" rx="3" fill="{l}" stroke="{n}" stroke-width="2"/>
    <rect x="150" y="108" width="30" height="20" rx="3" fill="{l}" stroke="{n}" stroke-width="2"/>
    <rect x="215" y="96" width="40" height="32" rx="3" fill="{l}" stroke="{n}" stroke-width="2"/>
    <rect x="282" y="122" width="26" height="34" rx="6" fill="{m}"/>"""


def _packaging(c, n, s, l, m):
    return _conveyor(c, n, s, l, m) + f"""
    <rect x="124" y="56" width="82" height="72" rx="8" fill="{m}" opacity=".95"/>
    <rect x="136" y="70" width="58" height="34" rx="4" fill="{l}"/>
    <rect x="148" y="108" width="34" height="6" rx="3" fill="{c}" opacity=".85"/>"""


def _cooling(c, n, s, l, m):
    slats = "".join(f'<rect x="108" y="{88 + i * 12}" width="104" height="5" rx="2" fill="{l}" opacity=".85"/>' for i in range(6))
    return f"""
    <rect x="96" y="76" width="128" height="94" rx="8" fill="{m}"/>
    {slats}
    <rect x="110" y="56" width="100" height="20" rx="6" fill="{n}"/>
    <ellipse cx="160" cy="54" rx="42" ry="8" fill="{s}"/>
    <rect x="224" y="128" width="54" height="10" fill="{s}"/><rect x="42" y="128" width="54" height="10" fill="{s}"/>"""


def _pump(c, n, s, l, m):
    fins = "".join(f'<rect x="{186 + i * 14}" y="108" width="6" height="34" fill="{m}"/>' for i in range(5))
    return f"""
    <rect x="84" y="160" width="204" height="10" rx="3" fill="{n}"/>
    <rect x="124" y="56" width="32" height="40" fill="{n}"/>
    <circle cx="140" cy="122" r="36" fill="{s}"/><circle cx="140" cy="122" r="18" fill="{m}"/>
    <circle cx="140" cy="122" r="6" fill="{l}"/>
    <rect x="176" y="104" width="94" height="42" rx="10" fill="{n}"/>
    {fins}
    <rect x="166" y="116" width="12" height="14" fill="{s}"/>"""


def _fan(c, n, s, l, m):
    blades = "".join(f'<ellipse cx="150" cy="78" rx="9" ry="22" fill="{s}" transform="rotate({a} 150 100)"/>' for a in range(0, 360, 60))
    return f"""
    <rect x="112" y="150" width="76" height="20" rx="4" fill="{n}"/><rect x="144" y="140" width="12" height="12" fill="{n}"/>
    <circle cx="150" cy="100" r="58" fill="{m}"/><circle cx="150" cy="100" r="48" fill="{l}"/>
    {blades}
    <circle cx="150" cy="100" r="9" fill="{n}"/>
    <rect x="206" y="80" width="82" height="40" rx="6" fill="{s}"/><rect x="206" y="80" width="82" height="10" rx="4" fill="{m}"/>"""


ILLUS = dict(compressor=_compressor, press=_press, molder=_molder, cnc=_cnc, lathe=_lathe, laser=_laser,
             robot=_robot, conveyor=_conveyor, packaging=_packaging, cooling=_cooling, pump=_pump, fan=_fan)


def machine_img_uri(m):
    c = STATUS_COLOR[m["status"]]
    body = ILLUS[m["type"]](c, "#183B5B", "#9DB3C6", "#DCEBF7", "#5E7F9B")
    svg = f"""
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 320 200" width="640" height="400">
      <defs><linearGradient id="bg" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0" stop-color="#F6FAFE"/><stop offset="1" stop-color="#D9E8F4"/></linearGradient></defs>
      <rect width="320" height="200" rx="18" fill="url(#bg)"/>
      <rect x="0" y="170" width="320" height="30" fill="#C6D7E5" opacity=".6"/>
      <ellipse cx="160" cy="172" rx="128" ry="6" fill="#183B5B" opacity=".13"/>
      {body}
      <circle cx="292" cy="26" r="13" fill="{c}" opacity=".22"/><circle cx="292" cy="26" r="7" fill="{c}"/>
      <text x="14" y="190" font-family="Consolas, Menlo, monospace" font-size="8" letter-spacing="1.5"
            fill="#6F8496">ILLUSTRATION · {m['id']}</text>
    </svg>"""
    return "data:image/svg+xml;base64," + base64.b64encode(svg.encode("utf-8")).decode("utf-8")


def img_html(m):
    return f'<img class="mx-img" src="{machine_img_uri(m)}"/>' if SHOW_MACHINE_IMAGE else ""


# =====================================================
# 7. FACTORY MAP
# =====================================================

SCALE_GOOD_HIGH = [[0, "#E65D70"], [0.5, "#E5A04B"], [1, "#20A77A"]]
SCALE_BAD_HIGH = [[0, "#20A77A"], [0.5, "#E5A04B"], [1, "#E65D70"]]
MODE_CFG = {
    "Status": None,
    "Health": ("health", 50, 100, SCALE_GOOD_HIGH, "%"),
    "Temperature": ("temp", 55, 90, SCALE_BAD_HIGH, "°C"),
    "Vibration": ("vib", 2, 8.5, SCALE_BAD_HIGH, "mm/s"),
    "Risk": ("risk", 10, 95, SCALE_BAD_HIGH, "/100"),
}


def rrect(x0, y0, x1, y1, r):
    return (f"M {x0 + r},{y0} L {x1 - r},{y0} Q {x1},{y0} {x1},{y0 + r} L {x1},{y1 - r} "
            f"Q {x1},{y1} {x1 - r},{y1} L {x0 + r},{y1} Q {x0},{y1} {x0},{y1 - r} "
            f"L {x0},{y0 + r} Q {x0},{y0} {x0 + r},{y0} Z")


def pipe_path(a, b):
    (xa, ya), (xb, yb) = a, b
    if (ya < 28) == (yb < 28):
        return [(xa, ya), (xb, ya), (xb, yb)]
    return [(xa, ya), (xa, 27.2), (xb, 27.2), (xb, yb)]


def build_map(sel_id, mode="Status"):
    fig = go.Figure()
    pos = {m["id"]: (m["x"], m["y"]) for m in MACHINES}

    def line_xy(pairs):
        xs, ys = [], []
        for a, b in pairs:
            pts = pipe_path(pos[a], pos[b])
            xs += [p[0] for p in pts] + [None]
            ys += [p[1] for p in pts] + [None]
        return xs, ys

    ax, ay = line_xy(AIR_LINES)
    fig.add_trace(go.Scatter(x=ax, y=ay, mode="lines", line=dict(color=AIR_COLOR, width=2.2, dash="dot"),
                             hoverinfo="skip"))
    cx, cy = line_xy(COOL_LINES)
    fig.add_trace(go.Scatter(x=cx, y=cy, mode="lines", line=dict(color=COOL_COLOR, width=2.2, dash="dot"),
                             hoverinfo="skip"))

    hx, hy, hs, hc = [], [], [], []
    for m in MACHINES:
        if m["status"] != "Healthy":
            hx.append(m["x"])
            hy.append(m["y"])
            hs.append(52 if m["status"] == "Critical" else 42)
            hc.append("rgba(230,93,112,0.26)" if m["status"] == "Critical" else "rgba(229,160,75,0.26)")
    fig.add_trace(go.Scatter(x=hx, y=hy, mode="markers", marker=dict(size=hs, color=hc), hoverinfo="skip"))

    s = BY_ID[sel_id]
    fig.add_trace(go.Scatter(x=[s["x"]], y=[s["y"]], mode="markers", hoverinfo="skip",
                             marker=dict(size=44, color="rgba(0,0,0,0)", line=dict(color="#183B5B", width=3))))

    cfg = MODE_CFG[mode]
    chev = [14, 26, 38, 62, 74, 86]

    def sub(m):
        return f"{m['id']} · {m['health']}%" if cfg is None else f"{m[cfg[0]]} {cfg[4]}"

    fig.add_trace(go.Scatter(
        x=[m["x"] for m in MACHINES] + chev,
        y=[m["y"] - 6.8 for m in MACHINES] + [31] * len(chev),
        mode="text",
        text=[f"<b>{m['name']}</b><br>{sub(m)}" for m in MACHINES] + ["›››"] * len(chev),
        textfont=dict(size=10, color="#34495A"),
        hoverinfo="skip",
    ))

    if cfg is None:
        mcolor, extra = [STATUS_COLOR[m["status"]] for m in MACHINES], {}
    else:
        mcolor = [m[cfg[0]] for m in MACHINES]
        extra = dict(colorscale=cfg[3], cmin=cfg[1], cmax=cfg[2], showscale=True,
                     colorbar=dict(title=dict(text=cfg[4], font=dict(size=10)), thickness=8, len=0.5,
                                   x=1.0, xanchor="left", tickfont=dict(size=9)))
    fig.add_trace(go.Scatter(
        x=[m["x"] for m in MACHINES],
        y=[m["y"] for m in MACHINES],
        mode="markers+text",
        text=[ICON[m["type"]] for m in MACHINES],
        textfont=dict(size=14),
        textposition="middle center",
        marker=dict(size=[34 if m["status"] == "Critical" else 30 for m in MACHINES],
                    color=mcolor, line=dict(color="white", width=2.5), **extra),
        customdata=[[m["id"], m["name"], m["status"], m["health"], m["temp"], m["vib"], m["risk"]] for m in MACHINES],
        hovertemplate=("<b>%{customdata[0]} · %{customdata[1]}</b><br>Status: %{customdata[2]}"
                       "<br>Health: %{customdata[3]}% · Risk: %{customdata[6]}/100"
                       "<br>Temp: %{customdata[4]} °C · Vib: %{customdata[5]} mm/s"
                       "<br><i>Click to open details</i><extra></extra>"),
        selected=dict(marker=dict(opacity=1)),
        unselected=dict(marker=dict(opacity=1)),
    ))

    shapes = [dict(type="path", path=rrect(x0, y0, x1, y1, 2.2), fillcolor=fill,
                   line=dict(color="#C3D3E0", width=1.5), layer="below")
              for _, x0, y0, x1, y1, fill in ZONES]
    shapes.append(dict(type="path", path=rrect(3, 28.4, 97, 33.6, 2.6), fillcolor="#D2DFEA",
                       line=dict(color="#B6C8D8", width=1.2), layer="below"))
    annotations = [dict(x=x0 + 1.6, y=y1 - 2.6, text=f"<b>{label}</b>", showarrow=False, xanchor="left",
                        font=dict(size=9.5, color="#587086", family="JetBrains Mono, Consolas, monospace"))
                   for label, x0, y0, x1, y1, _ in ZONES]
    annotations += [
        dict(x=98, y=35.2, text="MAIN CONVEYOR AISLE", showarrow=False, xanchor="right",
             font=dict(size=8.5, color="#8AA0B3", family="JetBrains Mono, Consolas, monospace")),
        dict(x=5.5, y=31, text="<b>RAW IN ▶</b>", showarrow=False,
             font=dict(size=8.5, color="#587086", family="JetBrains Mono, Consolas, monospace")),
        dict(x=94.5, y=31, text="<b>DISPATCH ▶</b>", showarrow=False,
             font=dict(size=8.5, color="#587086", family="JetBrains Mono, Consolas, monospace")),
    ]

    fig.update_layout(
        height=MAP_HEIGHT, margin=dict(l=0, r=60 if cfg else 0, t=2, b=0),
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        showlegend=False, dragmode="pan", shapes=shapes, annotations=annotations,
        hoverlabel=dict(bgcolor="white", bordercolor="#C9D9E7", font=dict(color="#183B5B", size=12)),
        xaxis=dict(visible=False, range=[0, 100], fixedrange=True),
        yaxis=dict(visible=False, range=[0, 62], fixedrange=True),
    )
    return fig


def read_map_click():
    ev = st.session_state.get("factory_map")
    if not ev:
        return None
    try:
        pts = ev["selection"]["points"]
    except Exception:
        return None
    for p in pts:
        if p.get("curve_number") == MARK_CURVE:
            return MACHINES[p["point_index"]]["id"]
    return None


# =====================================================
# 8. TIMELINES / HISTORY / COMPARISON HELPERS
# =====================================================

TL = {
    "temp": dict(title="Temperature", unit="°C", hours=24, step=15, fmt="%.1f"),
    "vib": dict(title="Vibration", unit="mm/s", hours=168, step=60, fmt="%.2f"),
    "press": dict(title="Pressure", unit="bar", hours=24, step=15, fmt="%.2f"),
    "rpm": dict(title="Speed (RPM)", unit="rpm", hours=168, step=60, fmt="%.0f"),
}
DRIFT = {
    "temp": {"Critical": 0.16, "Warning": 0.07, "Healthy": 0.0},
    "vib": {"Critical": 0.45, "Warning": 0.20, "Healthy": 0.0},
    "press": {"Critical": 0.05, "Warning": 0.02, "Healthy": 0.0},
    "rpm": {"Critical": 0.012, "Warning": 0.006, "Healthy": 0.0},
}
NOISE = {"Critical": 0.016, "Warning": 0.012, "Healthy": 0.008}


def series(m, key):
    cfg = TL[key]
    n = int(cfg["hours"] * 60 / cfg["step"])
    rng = np.random.default_rng(int(m["id"][2:]) * 1000 + list(TL).index(key) + 1)
    t = np.linspace(0, 1, n)
    base = m[key]
    drift = base * DRIFT[key][m["status"]] * (t ** 2 - 1)
    cycle = base * 0.018 * np.sin(2 * np.pi * (cfg["hours"] / 24) * t)
    noise = rng.normal(0, base * NOISE[m["status"]] * (0.25 if key == "rpm" else 1), n)
    y = base + drift + cycle + noise
    x = pd.date_range(end=NOW, periods=n, freq=f"{cfg['step']}min")
    return x, y


def window_series(m, key, hours=None):
    x, y = series(m, key)
    if hours:
        mask = np.asarray(x >= NOW - pd.Timedelta(hours=hours))
        if mask.sum() >= 3:
            x, y = x[mask], y[mask]
    return x, y


def style_fig(fig, height=235, legend=False):
    fig.update_layout(
        height=height, margin=dict(l=54, r=20, t=44 if legend else 18, b=38),
        paper_bgcolor="white", plot_bgcolor="white", font=dict(color="#52677A", size=12),
        hovermode="x unified", showlegend=legend,
    )
    fig.update_xaxes(gridcolor="#EEF1F5", automargin=True, title_standoff=6)
    fig.update_yaxes(gridcolor="#EEF1F5", automargin=True, title_standoff=6)
    return fig


def timeline_fig(m, key, height=225, hours=None, limits=True):
    cfg = TL[key]
    x, y = window_series(m, key, hours)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=x, y=y, mode="lines", name=cfg["title"], line=dict(color="#328BC5", width=2.4),
                             hovertemplate="%{y:.2f} " + cfg["unit"] + "<extra></extra>"))
    if key in ("temp", "vib"):
        lim = LIMITS[key]
        mask = y >= lim["warn"]
        if mask.any():
            fig.add_trace(go.Scatter(x=x[mask], y=y[mask], mode="markers", marker=dict(size=4.5, color="#E65D70"),
                                     hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[x[-1]], y=[y[-1]], mode="markers", marker=dict(size=9, color="#328BC5",
                             line=dict(color="white", width=2)), hoverinfo="skip"))
    if limits:
        if key in ("temp", "vib"):
            lim = LIMITS[key]
            fig.add_hline(y=lim["warn"], line_dash="dot", line_color="#E5A04B",
                          annotation_text=f"Watch {lim['warn']}", annotation_position="top left")
            fig.add_hline(y=lim["alert"], line_dash="dot", line_color="#E65D70",
                          annotation_text=f"Alert {lim['alert']}", annotation_position="top left")
            top = max(float(y.max()), lim["alert"])
            lo = float(y.min()) - (5 if key == "temp" else 0)
            fig.update_yaxes(range=[max(lo, 0), top * 1.12])
        elif key == "press":
            lim = LIMITS["press"]
            fig.add_hrect(y0=lim["low"], y1=lim["high"], fillcolor="rgba(32,167,122,0.10)", line_width=0,
                          annotation_text="Normal", annotation_position="bottom left")
            fig.update_yaxes(range=[min(float(y.min()), lim["low"]) - 0.4, max(float(y.max()), lim["high"]) + 0.4])
        else:
            r = m["rpm"]
            fig.add_hrect(y0=r * 0.96, y1=r * 1.04, fillcolor="rgba(32,167,122,0.10)", line_width=0,
                          annotation_text="Rated ±4%", annotation_position="bottom left")
            fig.update_yaxes(range=[r * 0.9, r * 1.1])
    span = (x[-1] - x[0]).total_seconds() / 3600
    fig.update_xaxes(tickformat="%H:%M" if span <= 24 else "%a %d")
    fig.update_yaxes(title_text=f"{cfg['unit']}")
    return style_fig(fig, height), y


def history_fig(m, height=230):
    months = pd.date_range(end=NOW, periods=12, freq="MS")
    rng = np.random.default_rng(int(m["id"][2:]) * 77)
    t = np.linspace(0, 1, 12)
    start = min(97.5, m["health"] + {"Critical": 38, "Warning": 17, "Healthy": 4}[m["status"]])
    health = start - (start - m["health"]) * t ** 2.2 + rng.normal(0, 0.6, 12)
    health[-1] = m["health"]
    up_now = uptime(m)
    up = 99.2 - (99.2 - up_now) * t ** 2.2 + rng.normal(0, 0.2, 12)
    up[-1] = up_now
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=months, y=health, name="Health", mode="lines+markers", fill="tozeroy",
                             fillcolor="rgba(50,139,197,0.12)", line=dict(color="#328BC5", width=2.6),
                             hovertemplate="%{y:.1f}%<extra>Health</extra>"))
    fig.add_trace(go.Scatter(x=months, y=up, name="Uptime", mode="lines+markers",
                             line=dict(color="#20A77A", width=2.2, dash="dash"),
                             hovertemplate="%{y:.1f}%<extra>Uptime</extra>"))
    fig.update_xaxes(tickformat="%b %y")
    fig.update_yaxes(range=[min(40, float(health.min()) - 5), 101], ticksuffix="%")
    fig.update_layout(legend=dict(orientation="h", y=1.18, x=0))
    return style_fig(fig, height, legend=True)


def gauge_fig(m):
    col = STATUS_COLOR[m["status"]]
    fig = go.Figure(go.Indicator(
        mode="gauge+number", value=m["health"],
        number=dict(suffix="%", font=dict(size=32, color="#14273A")),
        gauge=dict(axis=dict(range=[0, 100], tickwidth=1, tickcolor="#9AAAB8"),
                   bar=dict(color=col, thickness=0.28), bgcolor="white", borderwidth=0,
                   steps=[dict(range=[0, 60], color="#FDE3E7"), dict(range=[60, 80], color="#FDF0D9"),
                          dict(range=[80, 100], color="#E0F4EA")]),
    ))
    fig.update_layout(height=155, margin=dict(l=20, r=20, t=12, b=0), paper_bgcolor="white")
    return fig


def radar_scores(m):
    return {
        "Health": m["health"],
        "Reliability": 100 - m["risk"],
        "Thermal": float(np.clip((95 - m["temp"]) / 50 * 100, 0, 100)),
        "Vibration": float(np.clip((10 - m["vib"]) / 8.5 * 100, 0, 100)),
        "Uptime": float(np.clip((uptime(m) - 80) / 20 * 100, 0, 100)),
    }


def subsystem_bars_html(m):
    scores = radar_scores(m)
    items = [
        ("Bearing & Drive Health", int(scores["Vibration"])),
        ("Thermal Dissipation", int(scores["Thermal"])),
        ("Operational Reliability", int(scores["Reliability"])),
        ("30-Day Availability", int(uptime(m))),
    ]
    out = '<div style="margin-top:12px;border-top:1px solid #EEF0F3;padding-top:12px;">'
    out += '<div class="panel-title" style="margin-bottom:10px;">Subsystem Integrity</div>'
    for label, val in items:
        c = "#20A77A" if val >= 80 else "#E5A04B" if val >= 60 else "#E65D70"
        out += f"""
        <div class="sub-row">
            <div class="sub-lbl"><span>{label}</span><span style="color:{c};font-weight:700;">{val}%</span></div>
            <div class="bar"><div style="width:{val}%;background:{c};"></div></div>
        </div>
        """
    out += "</div>"
    return out


# =====================================================
# 8b. POPUP DIALOG
# =====================================================

_dialog = getattr(st, "dialog", None) or getattr(st, "experimental_dialog", None)


def popup(title):
    def deco(fn):
        if _dialog is not None:
            try:
                return _dialog(title, width="large")(fn)
            except TypeError:
                return _dialog(title)(fn)

        def fallback(*a, **k):
            with st.expander(title, expanded=True):
                fn(*a, **k)
        return fallback
    return deco


def queue_select(mid, open_popup=False):
    st.session_state["pending_sel"] = mid
    if open_popup:
        st.session_state["popup_request"] = mid


WINDOW_OPTIONS = [6, 12, 24, 72, 168]


@popup("🔎 Machine quick view")
def machine_popup(mid):
    m = BY_ID[mid]
    if SHOW_MACHINE_IMAGE:
        c1, c2 = st.columns([1, 1.25], gap="medium")
        with c1:
            st.html(img_html(m))
        with c2:
            st.html(head_html(m) + tiles_html(m))
    else:
        st.html(head_html(m) + tiles_html(m))
    st.html(f'<div class="mx-foot"><span>Risk score <b>{m["risk"]} / 100</b></span>'
            f'<span>Time to limit: <b>{rul_text(m)}</b></span></div>')

    t1, t2, t3, t4, t5 = st.tabs(["📈 Live trend", "🧠 AI diagnosis", "🔀 Compare", "ℹ️ Details", "🛠️ Work order"])

    with t1:
        o1, o2, o3 = st.columns([1.5, 1.5, 0.8])
        metric = o1.radio("Sensor", list(TL), format_func=lambda k: TL[k]["title"], horizontal=True,
                          key=f"pm_metric_{mid}")
        win = o2.select_slider("Time window", options=WINDOW_OPTIONS, value=24,
                               format_func=lambda h: f"{h} h" if h < 72 else f"{h // 24} d",
                               key=f"pm_win_{mid}")
        show_lim = o3.checkbox("Limits", value=True, key=f"pm_lim_{mid}")
        fig, y = timeline_fig(m, metric, 250, hours=win, limits=show_lim)
        u = TL[metric]["unit"]
        k1, k2, k3, k4 = st.columns(4)
        k1.metric("Current", f"{y[-1]:.2f} {u}", delta=f"{y[-1] - y.mean():+.2f} vs avg", delta_color="inverse")
        k2.metric("Average", f"{y.mean():.2f} {u}")
        k3.metric("Peak", f"{y.max():.2f} {u}")
        k4.metric("State", sensor_state(m, metric))
        st.plotly_chart(fig, use_container_width=True, theme=None, key=f"pop_chart_{mid}",
                        config={"displayModeBar": False})

    with t2:
        d1, d2 = st.columns([1.2, 1])
        with d1:
            st.html('<div class="panel-title">Findings</div>' + diag_html(m))
        with d2:
            st.html('<div class="panel-title">Action checklist</div>')
            _, acts = diagnose(m)
            done = 0
            for i, a in enumerate(acts):
                if st.checkbox(a, key=f"act_{mid}_{i}"):
                    done += 1
            st.progress(done / len(acts), text=f"{done} of {len(acts)} completed")

    with t3:
        other = st.selectbox("Compare with", [i for i in IDS if i != mid], key=f"pm_cmp_{mid}",
                             format_func=lambda i: f"{i} · {BY_ID[i]['name']}")
        o = BY_ID[other]
        q = st.columns(4)
        q[0].metric("Health", f"{m['health']}%", delta=f"{m['health'] - o['health']:+d} vs {o['id']}")
        q[1].metric("Risk", f"{m['risk']}/100", delta=f"{m['risk'] - o['risk']:+d} vs {o['id']}", delta_color="inverse")
        q[2].metric("Temp", f"{m['temp']} °C", delta=f"{m['temp'] - o['temp']:+d} vs {o['id']}", delta_color="inverse")
        q[3].metric("Vibration", f"{m['vib']} mm/s", delta=f"{m['vib'] - o['vib']:+.1f} vs {o['id']}", delta_color="inverse")
        sa, sb = radar_scores(m), radar_scores(o)
        bar = go.Figure()
        bar.add_trace(go.Bar(x=list(sa.keys()), y=list(sa.values()), name=m["name"], marker_color="#328BC5"))
        bar.add_trace(go.Bar(x=list(sb.keys()), y=list(sb.values()), name=o["name"], marker_color="#8A80C5"))
        bar.update_layout(barmode="group", yaxis=dict(range=[0, 100]))
        st.plotly_chart(style_fig(bar, 230, legend=True), use_container_width=True, theme=None,
                        key=f"pop_cmp_{mid}", config={"displayModeBar": False})

    with t4:
        rows = [("Manufacturer", m["mfr"]), ("Model", m["model"]), ("Serial", m["serial"]),
                ("Installed", m["install"]), ("Operating hours", f"{m['hours']:,} h"),
                ("Last service", m["last"]), ("Next service", m["next"])] + m["specs"]
        st.html('<table class="kv">' + "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows) + "</table>")
        dkey = st.selectbox("Export readings", list(TL), format_func=lambda k: TL[k]["title"],
                            key=f"pm_dl_{mid}")
        dx, dy = window_series(m, dkey)
        csv = pd.DataFrame({"time": dx, f"{dkey}_{TL[dkey]['unit']}": dy}).to_csv(index=False)
        st.download_button("⬇️ Download CSV", csv, file_name=f"{mid}_{dkey}.csv", mime="text/csv",
                           key=f"dl_{mid}", use_container_width=True)

    with t5:
        default = {"Critical": "Inspect bearings and replace worn parts",
                   "Warning": "Preventive inspection at next window",
                   "Healthy": "Routine service check"}[m["status"]]
        with st.form(f"wo_form_{mid}", clear_on_submit=True):
            f1, f2 = st.columns(2)
            pr = f1.selectbox("Priority", ["Low", "Medium", "High", "Urgent"],
                              index=3 if m["status"] == "Critical" else 1 if m["status"] == "Warning" else 0)
            due = f2.date_input("Due date", value=(NOW + pd.Timedelta(days=1)).date())
            task = st.text_input("Task", value=default)
            ok = st.form_submit_button("Create work order", use_container_width=True)
        if ok:
            st.session_state["work_orders"].append(
                dict(Machine=f"{m['id']} · {m['name']}", Priority=pr, Task=task, Due=str(due), Status="Open"))
            st.toast(f"Work order created for {m['id']}", icon="🛠️")
        mine = [w for w in st.session_state["work_orders"] if w["Machine"].startswith(m["id"])]
        if mine:
            st.dataframe(pd.DataFrame(mine), use_container_width=True, hide_index=True)

    if st.button("📌  Show in digital profile below", use_container_width=True, key=f"pin_{mid}"):
        st.session_state["pending_sel"] = mid
        st.rerun()


# =====================================================
# 9. NOTIFICATIONS & HEADER
# =====================================================

render_notifications()

counts = {s: sum(1 for m in MACHINES if m["status"] == s) for s in STATUS_COLOR}
alerts = active_alerts()

h_left, h_right = st.columns([3.4, 1.3])
with h_left:
    st.html(
        """
        <div class="eyebrow">ANOMATRIX · MACHINE INTELLIGENCE</div>
        <div class="page-title">Machine Explorer</div>
        <div class="page-sub">Click any machine on the map for instant diagnostics, sensor telemetry, and side-by-side comparison.</div>
        """
    )
with h_right:
    st.html(
        f"""
        <div class="count-pill">
            <div><div class="n" style="color:#20A77A">{counts['Healthy']}</div><div class="l">HEALTHY</div></div>
            <div><div class="n" style="color:#E5A04B">{counts['Warning']}</div><div class="l">WARNING</div></div>
            <div><div class="n" style="color:#E65D70">{counts['Critical']}</div><div class="l">CRITICAL</div></div>
        </div>
        """
    )
    _pop = getattr(st, "popover", None)
    _ctx = (_pop(f"🔔  Active alerts ({len(alerts)})", use_container_width=True) if _pop
            else st.expander(f"🔔  Active alerts ({len(alerts)})"))
    with _ctx:
        st.html("".join(
            f'<div class="al-row"><span class="state-pill" style="color:{STATE_COLOR[s]};background:{STATE_BG[s]};">{s}</span>'
            f'<span><b>{m["id"]} {m["name"]}</b> · {lab} {v} {u}</span></div>'
            for m, lab, v, u, s in alerts) or "No active alerts")
st.html('<hr class="divider">')

# =====================================================
# 10. A. INTERACTIVE FACTORY MAP & PRIORITY QUEUE
# =====================================================

st.session_state.setdefault("sel_machine", "M-07")
st.session_state.setdefault("work_orders", [])

if "pending_sel" in st.session_state:
    st.session_state["sel_machine"] = st.session_state.pop("pending_sel")

clicked = read_map_click()
if clicked != st.session_state.get("_map_sig"):
    st.session_state["_map_sig"] = clicked
    if clicked:
        st.session_state["sel_machine"] = clicked
        st.session_state["popup_request"] = clicked

sel = BY_ID[st.session_state["sel_machine"]]

st.html('<div class="section-label">FACTORY FLOOR</div>'
        '<div class="section-title">Interactive factory map</div>')

col_map, col_side = st.columns([2.4, 1], gap="medium")

with col_map:
    with st.container(border=True):
        mode = st.radio("Colour map by", list(MODE_CFG), horizontal=True, key="map_mode",
                        label_visibility="collapsed")
        st.html(
            f"""
            <div class="legend-row">
                <span><span class="lg-dot" style="background:#20A77A"></span>Healthy ({counts['Healthy']})</span>
                <span><span class="lg-dot" style="background:#E5A04B"></span>Warning ({counts['Warning']})</span>
                <span><span class="lg-dot" style="background:#E65D70"></span>Critical ({counts['Critical']})</span>
                <span><span class="lg-line" style="--c:{AIR_COLOR}"></span>Compressed air</span>
                <span><span class="lg-line" style="--c:{COOL_COLOR}"></span>Coolant</span>
                <span class="lg-hint">CLICK A MACHINE ▸</span>
            </div>
            """
        )
        try:
            st.plotly_chart(
                build_map(sel["id"], mode), use_container_width=True, key="factory_map",
                on_select="rerun", selection_mode="points", theme=None,
                config={"displayModeBar": False},
            )
        except TypeError:
            st.plotly_chart(build_map(sel["id"], mode), use_container_width=True, theme=None,
                            config={"displayModeBar": False})

    top3 = sorted(MACHINES, key=lambda m: -m["risk"])[:3]
    for col, m in zip(st.columns(3, gap="small"), top3):
        with col:
            with st.container(border=True):
                hc = STATUS_COLOR[m["status"]]
                st.html(
                    f"""
                    <div class="rq-top"><span class="rq-id">{m['id']}</span>{status_chip(m['status'])}</div>
                    <div class="rq-name">{ICON[m['type']]} {m['name']}</div>
                    <div class="rq-meta"><span>Risk <b>{m['risk']}/100</b></span><span>Limit <b>{m['limit']}</b></span></div>
                    <div class="bar"><div style="width:{m['risk']}%;background:{hc};"></div></div>
                    """
                )
                st.button("Inspect", key=f"insp_{m['id']}", on_click=queue_select, args=(m["id"], True),
                          use_container_width=True)

with col_side:
    st.html(
        f"""
        <div class="mx-panel">
            {img_html(sel)}
            {head_html(sel)}
            {tiles_html(sel)}
            <div class="mx-foot"><span>Risk score <b>{sel['risk']} / 100</b></span><span>Limit: <b>{sel['limit']}</b></span></div>
            <a class="mx-link" href="#machine-profile" target="_self">Open full digital profile ↓</a>
        </div>
        """
    )
    st.button("🔎  Open quick-view popup", key="open_popup_btn", on_click=queue_select,
              args=(sel["id"], True), use_container_width=True)

_req = st.session_state.pop("popup_request", None)
if _req:
    machine_popup(_req)

# =====================================================
# 11. B. UNIFIED DIGITAL PROFILE & AI DIAGNOSIS
# =====================================================

st.html('<div id="machine-profile"></div>')
hdr_c1, hdr_c2 = st.columns([2.5, 1])
with hdr_c1:
    st.html('<div class="section-label">DIGITAL PROFILE & DIAGNOSTICS</div>'
            '<div class="section-title">Machine digital profile</div>')
with hdr_c2:
    st.selectbox(
        "Selected machine", IDS, key="sel_machine", label_visibility="collapsed",
        format_func=lambda i: f"Selected: {i} · {BY_ID[i]['name']}",
    )
sel = BY_ID[st.session_state["sel_machine"]]

p1, p2, p3 = st.columns([1.05, 1.05, 1.25], gap="small")

with p1:
    with st.container(border=True):
        rows = [
            ("Machine ID", sel["id"]), ("Manufacturer", sel["mfr"]), ("Model", sel["model"]),
            ("Serial number", sel["serial"]), ("Installed", sel["install"]),
            ("Operating hours", f"{sel['hours']:,} h ({sel['hours'] / 8760:.1f} yr)"),
            ("Floor zone", sel["zone"]), ("Last / Next service", f"{sel['last']} → {sel['next']}"),
        ]
        body = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
        st.html(f'<div class="panel-title">Identity &amp; service</div><table class="kv">{body}</table>')

with p2:
    with st.container(border=True):
        rows = sel["specs"] + [("Rated speed", f"{sel['rpm']:,} rpm"), ("Operating status", sel["status"])]
        body = "".join(f"<tr><td>{a}</td><td>{b}</td></tr>" for a, b in rows)
        st.html(
            f'<div class="panel-title">Specifications &amp; outlook</div><table class="kv">{body}</table>'
            f"""
            <div class="ol-grid">
                <div class="ol"><div class="l">TIME TO LIMIT</div><div class="v">{rul_text(sel)}</div></div>
                <div class="ol"><div class="l">14D FAIL RISK</div><div class="v">{round(sel['risk'] * 0.85)}%</div></div>
                <div class="ol"><div class="l">UPTIME (30D)</div><div class="v">{uptime(sel)}%</div></div>
            </div>
            """
        )

with p3:
    with st.container(border=True):
        st.html('<div class="panel-title">AI diagnosis &amp; recommended actions</div>'
                + diag_html(sel)
                + '<div style="margin-top:8px;border-top:1px solid #EEF0F3;padding-top:8px;">'
                + actions_html(sel) + '</div>')

# =====================================================
# 12. C. SENSOR MONITORING & BALANCED RIGHT COLUMN
# =====================================================

st.html('<div class="section-label">REAL-TIME TELEMETRY</div>'
        '<div class="section-title">Sensor monitoring</div>')

s_left, s_right = st.columns([1.65, 1], gap="small")

with s_left:
    with st.container(border=True):
        mt, mv, mp = SENSOR_MOUNTS[sel["type"]]
        rpm_max = int(round(sel["rpm"] * 1.25, -2))
        cfg_rows = [
            ("Temperature", "RTD PT100", mt, "0 – 120 °C", "1 s", sensor_state(sel, "temp")),
            ("Vibration", "Triaxial accel.", mv, "0 – 15 mm/s", "10 kHz", sensor_state(sel, "vib")),
            ("Pressure", "Piezo transducer", mp, "0 – 10 bar", "1 s", sensor_state(sel, "press")),
            ("Speed", "Hall tachometer", "Drive shaft", f"0 – {rpm_max:,} rpm", "1 s", "OK"),
            ("Motor current", "Clamp CT", "Drive cabinet", "0 – 150 A", "1 s", "OK"),
        ]
        body = "".join(
            f'<tr><td>{a}</td><td>{b}</td><td>{c}</td><td>{d}</td><td>{e}</td>'
            f'<td><span class="state-pill" style="color:{STATE_COLOR[f]};background:{STATE_BG[f]};">{f}</span></td></tr>'
            for a, b, c, d, e, f in cfg_rows
        )
        st.html(
            f'<div class="panel-title">Sensor configuration &amp; trends · {sel["name"]}</div>'
            '<table class="stbl"><thead><tr><th>SENSOR</th><th>TYPE</th><th>MOUNTED AT</th>'
            f'<th>RANGE</th><th>RATE</th><th>STATE</th></tr></thead><tbody>{body}</tbody></table>'
        )

        tab_labels = ["Temperature · 24 h", "Vibration · 7 d", "Pressure · 24 h", "RPM · 7 d"]
        for tab, key in zip(st.tabs(tab_labels), ["temp", "vib", "press", "rpm"]):
            with tab:
                fig, y = timeline_fig(sel, key, 225)
                u = TL[key]["unit"]
                f = TL[key]["fmt"]
                stat = sensor_state(sel, key)
                st.html(
                    f"""
                    <div class="ms-row">
                        <div class="ms"><div class="l">CURRENT</div><div class="v">{f % y[-1]} {u}</div></div>
                        <div class="ms"><div class="l">AVERAGE</div><div class="v">{f % y.mean()} {u}</div></div>
                        <div class="ms"><div class="l">PEAK</div><div class="v">{f % y.max()} {u}</div></div>
                        <div class="ms"><div class="l">LOWEST</div><div class="v">{f % y.min()} {u}</div></div>
                        <div class="ms"><div class="l">STATE</div><div class="v" style="color:{STATE_COLOR[stat]}">{stat}</div></div>
                    </div>
                    """
                )
                st.plotly_chart(fig, use_container_width=True, theme=None, key=f"tl_{key}",
                                config={"displayModeBar": False})

with s_right:
    with st.container(border=True):
        st.html('<div class="panel-title">Health index &amp; 12-month trend</div>')
        st.plotly_chart(gauge_fig(sel), use_container_width=True, theme=None, key="gauge_main",
                        config={"displayModeBar": False})
        st.plotly_chart(history_fig(sel, 230), use_container_width=True, theme=None, key="history_main",
                        config={"displayModeBar": False})
        st.html(subsystem_bars_html(sel))

# =====================================================
# 13. D. MACHINE COMPARISON
# =====================================================

st.html('<div class="section-label">BENCHMARKING</div>'
        '<div class="section-title">Machine comparison</div>')

ca, cb = st.columns(2, gap="small")
with ca:
    id_a = st.selectbox("Machine A", IDS, index=IDS.index("M-07"), key="cmp_a", label_visibility="collapsed",
                        format_func=lambda i: f"Machine A: {i} · {BY_ID[i]['name']}")
with cb:
    id_b = st.selectbox("Machine B", IDS, index=IDS.index("M-02"), key="cmp_b", label_visibility="collapsed",
                        format_func=lambda i: f"Machine B: {i} · {BY_ID[i]['name']}")
A, B = BY_ID[id_a], BY_ID[id_b]
COL_A, COL_B = "#328BC5", "#8A80C5"

cmp_rows = [
    ("Temperature", A["temp"], B["temp"], "low", "{:.0f}", " °C"),
    ("Vibration", A["vib"], B["vib"], "low", "{:.1f}", " mm/s"),
    ("Pressure", A["press"], B["press"], None, "{:.1f}", " bar"),
    ("Speed", A["rpm"], B["rpm"], None, "{:,.0f}", " rpm"),
    ("Health", A["health"], B["health"], "high", "{:.0f}", "%"),
    ("Risk score", A["risk"], B["risk"], "low", "{:.0f}", " / 100"),
    ("Uptime (30 d)", uptime(A), uptime(B), "high", "{:.1f}", "%"),
    ("Operating hours", A["hours"], B["hours"], None, "{:,.0f}", " h"),
]

body = ""
for label, va, vb, better, fmt, suf in cmp_rows:
    cls_a = cls_b = ""
    if better and va != vb:
        a_good = (va < vb) if better == "low" else (va > vb)
        cls_a, cls_b = ("good", "bad") if a_good else ("bad", "good")
    d = vb - va
    arrow = "▲" if d > 0 else "▼" if d < 0 else "–"
    delta = f"{arrow} {fmt.format(abs(d))}" if d != 0 else "–"
    body += (f'<tr><td>{label}</td><td class="{cls_a}">{fmt.format(va)}{suf}</td>'
             f'<td class="{cls_b}">{fmt.format(vb)}{suf}</td><td class="dl">{delta}</td></tr>')
body += f'<tr><td>Time to limit</td><td>{A["limit"]}</td><td>{B["limit"]}</td><td class="dl">–</td></tr>'

if id_a == id_b:
    verdict = "Select two different machines to see a meaningful comparison."
else:
    hi, lo = (A, B) if A["risk"] > B["risk"] else (B, A)
    if A["risk"] == B["risk"]:
        verdict = "Both machines carry the same risk score."
    else:
        verdict = (f"<b>{hi['id']} {hi['name']}</b> carries the higher risk ({hi['risk']} vs {lo['risk']}) "
                   f"and a health gap of {abs(A['health'] - B['health'])} points — prioritise it for inspection.")

cl, cr = st.columns([1.35, 1], gap="small")
with cl:
    with st.container(border=True):
        st.html(
            f"""
            <table class="cmp">
              <thead><tr>
                <th>Parameter</th>
                <th><span class="dot" style="background:{COL_A}"></span>{A['id']} · {A['name']}</th>
                <th><span class="dot" style="background:{COL_B}"></span>{B['id']} · {B['name']}</th>
                <th>Δ (B − A)</th>
              </tr></thead>
              <tbody>{body}</tbody>
            </table>
            <div class="verdict">{verdict}</div>
            """
        )
with cr:
    with st.container(border=True):
        st.html('<div class="panel-title">Performance profile</div>')
        sa, sb = radar_scores(A), radar_scores(B)
        cats = list(sa)
        radar = go.Figure()
        for name, sc, col, fill in [(A["name"], sa, COL_A, "rgba(50,139,197,0.18)"),
                                    (B["name"], sb, COL_B, "rgba(138,128,197,0.18)")]:
            radar.add_trace(go.Scatterpolar(r=[sc[c] for c in cats] + [sc[cats[0]]], theta=cats + [cats[0]],
                                            name=name, fill="toself", fillcolor=fill,
                                            line=dict(color=col, width=2.5)))
        radar.update_layout(
            height=315, margin=dict(l=60, r=60, t=15, b=45), paper_bgcolor="white",
            font=dict(color="#52677A", size=12), legend=dict(orientation="h", y=-0.12, x=0.5, xanchor="center"),
            polar=dict(bgcolor="white", domain=dict(x=[0, 1], y=[0, 1]),
                       radialaxis=dict(range=[0, 100], gridcolor="#E4ECF3", tickfont=dict(size=9), angle=90,
                                       tickangle=90),
                       angularaxis=dict(gridcolor="#E4ECF3", tickfont=dict(size=12))),
        )
        st.plotly_chart(radar, use_container_width=True, theme=None, key="radar_cmp",
                        config={"displayModeBar": False})

# =====================================================
# 14. WORK ORDERS RAISED FROM THE POPUP
# =====================================================

if st.session_state["work_orders"]:
    st.html('<div class="section-label">MAINTENANCE</div>'
            '<div class="section-title">Work orders raised</div>')
    with st.container(border=True):
        st.dataframe(pd.DataFrame(st.session_state["work_orders"]), use_container_width=True, hide_index=True)

st.caption("Prototype v1.2 · Illustrative mock data · Not live sensor data")