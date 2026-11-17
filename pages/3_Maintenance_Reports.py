"""
ANOMATRIX - Page 3: Maintenance Hub & Reports Analytics
Exact Machine Explorer ('Interactive Factory Map') Header Position, Font Style & Size.
3 Sub-Pages via Top Banners:
  01 · Maintenance    (4 white clickable KPI cards + white pop-out quick details & AI Recommendations)
  02 · Action Planner (Center tab — direct redirect from Dashboard, compact full-view color calendar, Action Planner + Plan Review)
  03 · Reports        (White MTBF/MTTR/Availability KPI cards, 3 simple charts, What the numbers say, Reliability Table, Reporting Centre)
"""

import calendar
import html as _html
import json
from datetime import date, timedelta
from io import BytesIO
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import streamlit as st
from components.login import require_login
from components.sidebar import render_sidebar

require_login()
render_sidebar()

# =====================================================
# 0. SWITCHES & CONSTANTS
# =====================================================

PERSIST = True
DATA_FILE = Path(__file__).resolve().parent / "hub_state.json"

TODAY = date.today()
NOW = pd.Timestamp.now().floor("h")
MONTHS = pd.date_range(end=NOW, periods=12, freq="MS")
MONTH_END = MONTHS + pd.offsets.MonthEnd(0)


def esc(s):
    return _html.escape(str(s))


# =====================================================
# 1. CSS (Exact Match with Machine Explorer 'Interactive Factory Map')
# =====================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;600;700&display=swap');

html, body, .stApp, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
}
.stApp {
    background:
        radial-gradient(900px 420px at 92% -5%, rgba(120,190,235,0.22), transparent 60%),
        radial-gradient(700px 400px at 0% 0%, rgba(190,225,250,0.32), transparent 60%),
        #E6F0F8;
    color: #0D1F33;
}
[data-testid="stHeader"] { background: transparent; }
footer { visibility: hidden; }

/* Exact top spacing matching Machine Explorer ('Interactive Factory Map') */
.block-container {
    max-width: 1480px;
    padding-top: 2.1rem !important;
    padding-bottom: 1.6rem !important;
}
div[data-testid="stVerticalBlock"] { gap: 0.6rem !important; }

/* ---------- EXACT MACHINE EXPLORER ('Interactive Factory Map') HEADING ---------- */
.page-eyebrow {
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 11px !important;
    font-weight: 600 !important;
    letter-spacing: 2.8px !important;
    color: #6B7E8F !important;
    text-transform: uppercase !important;
    margin: 10px 0 4px 0 !important;
    line-height: 1.2 !important;
}
.page-main-title {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    font-size: 34px !important;
    font-weight: 700 !important;
    color: #0D1F33 !important;
    letter-spacing: -0.02em !important;
    line-height: 1.15 !important;
    margin: 0 !important;
    padding: 0 !important;
}
.header-divider {
    border: none;
    border-top: 1px solid #D3E0EC;
    margin: 8px 0 8px !important;
}

.section-label {
    font-family: 'JetBrains Mono', monospace !important;
    letter-spacing: 2.8px !important;
    font-size: 10.5px !important;
    color: #6B7E8F !important;
    margin-top: 6px !important;
    text-transform: uppercase !important;
    font-weight: 600 !important;
}
.section-title {
    font-family: 'Inter', sans-serif !important;
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #0D1F33 !important;
    margin: 1px 0 6px !important;
    line-height: 1.18 !important;
    letter-spacing: -0.015em !important;
}
.panel-title {
    font-size: 16.5px;
    font-weight: 700;
    color: #0D1F33;
    margin-bottom: 6px;
    letter-spacing: -0.01em;
}
.panel-sub {
    font-size: 12.5px;
    color: #6F808E;
    margin: -3px 0 6px;
}

/* ---------- PURE WHITE POP-OUT CONTAINERS ---------- */
div[data-testid="stVerticalBlockBorderWrapper"],
div[data-testid="stVerticalBlockBorderWrapper"] > div {
    background-color: #FFFFFF !important;
}
div[data-testid="stVerticalBlockBorderWrapper"] {
    background: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1px solid #DCE7F2 !important;
    box-shadow: 0 12px 30px rgba(15, 39, 64, 0.10), 0 3px 8px rgba(15, 39, 64, 0.04) !important;
    padding: 0.8rem 1rem !important;
    transition: transform .2s ease, box-shadow .2s ease !important;
}
div[data-testid="stVerticalBlockBorderWrapper"]:hover {
    box-shadow: 0 16px 36px rgba(15, 39, 64, 0.14), 0 4px 12px rgba(50, 139, 197, 0.09) !important;
}

/* ---------- COMMAND CENTER STYLE WHITE KPI CARDS ---------- */
.cc-kpi {
    position: relative;
    overflow: hidden;
    background: #FFFFFF;
    border: 1px solid #DCE7F2;
    border-radius: 18px;
    padding: 14px 18px 16px;
    box-shadow: 0 12px 28px rgba(15, 39, 64, 0.09), 0 2px 8px rgba(15, 39, 64, 0.04);
    transition: all .2s ease;
}
.cc-kpi::before {
    content: "";
    position: absolute;
    right: -32px;
    top: -32px;
    width: 115px;
    height: 115px;
    border-radius: 50%;
    background: radial-gradient(circle, var(--c) 0%, transparent 70%);
    opacity: .15;
    pointer-events: none;
}
.cc-kpi.active {
    border: 2px solid var(--c);
    box-shadow: 0 16px 34px rgba(35, 75, 110, 0.16);
}
.cc-kpi .l {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.8px;
    color: #6F7C86;
    font-weight: 600;
    text-transform: uppercase;
}
.cc-kpi .v {
    font-size: 32px;
    font-weight: 800;
    color: #0D1F33;
    margin-top: 6px;
    line-height: 1.05;
}
.cc-kpi .d {
    font-size: 12.5px;
    color: #7A8791;
    margin-top: 5px;
}
.cc-kpi .bar-accent {
    position: absolute;
    left: 18px;
    bottom: 0;
    height: 4px;
    width: 44px;
    border-radius: 4px 4px 0 0;
    background: var(--c);
}

/* ---------- INPUTS, POPOVER & BUTTONS ---------- */
[data-testid="stMain"] [data-baseweb="select"] > div {
    background-color: #FFFFFF !important;
    border-radius: 12px !important;
    border-color: #DCE5EE !important;
}
[data-testid="stMain"] [data-baseweb="input"], [data-testid="stMain"] [data-baseweb="textarea"] {
    border-radius: 12px !important;
    background-color: #FFFFFF !important;
}
[data-testid="stRadio"] label p { font-size: 13px; font-weight: 600; color: #0D1F33; }

[data-testid="stMain"] .stButton > button,
[data-testid="stMain"] [data-testid="stDownloadButton"] button,
[data-testid="stMain"] [data-testid="stFormSubmitButton"] button,
[data-testid="stMain"] [data-testid="stPopover"] > button {
    background-color: #FFFFFF !important;
    border: 1px solid #D6E2EE !important;
    border-radius: 13px !important;
    font-weight: 600 !important;
    font-size: 12.5px !important;
    color: #183B5B !important;
    padding: 0.32rem 0.6rem !important;
    min-height: 34px !important;
    box-shadow: 0 4px 12px rgba(15,39,64,0.06) !important;
    transition: all .18s ease !important;
}
[data-testid="stMain"] .stButton > button:hover,
[data-testid="stMain"] [data-testid="stDownloadButton"] button:hover,
[data-testid="stMain"] [data-testid="stFormSubmitButton"] button:hover,
[data-testid="stMain"] [data-testid="stPopover"] > button:hover {
    background-color: #F4FAFE !important;
    border-color: #328BC5 !important;
    color: #17628D !important;
    transform: translateY(-1px);
    box-shadow: 0 7px 16px rgba(50,139,197,0.15) !important;
}
[data-testid="stMain"] .stButton > button[kind="primary"],
[data-testid="stMain"] [data-testid="stDownloadButton"] button[kind="primary"] {
    background: linear-gradient(135deg, #1E6FA5 0%, #328BC5 100%) !important;
    color: #FFFFFF !important;
    border: 1px solid #1E6FA5 !important;
    box-shadow: 0 7px 16px rgba(30,111,165,0.22) !important;
}

/* ---------- PILLS / CHIPS ---------- */
.pill { font-size: 11px; font-weight: 700; padding: 3px 10px; border-radius: 999px; white-space: nowrap; display: inline-block; }
.status-chip { font-family: 'JetBrains Mono', monospace; font-size: 10.5px; letter-spacing: 1.5px; font-weight: 700;
    padding: 5px 11px; border-radius: 999px; white-space: nowrap; }

/* ---------- ROWS / TILES ---------- */
.al-row { display: flex; gap: 12px; align-items: center; padding: 7px 4px; border-bottom: 1px solid #EEF2F6; font-size: 13px; color: #263746; }
.al-row:last-child { border-bottom: none; }
.al-row b { color: #0D1F33; }
.tile-grid { display: grid; grid-template-columns: repeat(3, 1fr); gap: 8px; margin-top: 8px; }
.tile { background: #F8FBFE; border: 1px solid #E1E8F0; border-radius: 12px; padding: 7px 10px; }
.tile .l { font-family: 'JetBrains Mono', monospace; font-size: 9.5px; letter-spacing: 1.6px; color: #7A8791; }
.tile .v { font-size: 16px; font-weight: 700; color: #0D1F33; margin-top: 2px; }
.ms-row { display: flex; gap: 8px; margin: 2px 0 8px; flex-wrap: wrap; }
.ms { flex: 1; min-width: 105px; background: #F8FBFE; border: 1px solid #E1E8F0; border-radius: 12px; padding: 8px 12px; }
.ms .l { font-family: 'JetBrains Mono', monospace; font-size: 9.5px; letter-spacing: 1.6px; color: #7A8791; }
.ms .v { font-size: 18px; font-weight: 700; color: #0D1F33; margin-top: 2px; }
.bar { height: 7px; border-radius: 7px; background: #ECEEF2; overflow: hidden; }
.bar > div { height: 100%; border-radius: 7px; }
.verdict { margin-top: 8px; padding: 8px 12px; border-radius: 12px; background: #FFFDF7; border: 1px solid #F0DFBA;
    border-left: 5px solid #E5A04B; font-size: 12.5px; color: #34495A; }
.verdict.bad { background: #FFF6F7; border-color: #F6D0D6; border-left-color: #E65D70; }
.verdict.ok { background: #F4FBF7; border-color: #CDEBDD; border-left-color: #20A77A; }

/* ---------- RECOMMENDATION CARDS ---------- */
.rec-top { display: flex; justify-content: space-between; align-items: center; }
.rec-id { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1.6px; color: #7A8791; font-weight: 600; }
.rec-name { font-size: 16px; font-weight: 700; color: #0D1F33; margin-top: 3px; }
.rec-task { font-size: 13.5px; font-weight: 700; color: #17628D; margin-top: 5px; }
.rec-why { font-size: 12.5px; color: #5B6F7E; margin: 4px 0 8px; line-height: 1.4; min-height: 46px; }

/* ---------- TABLES ---------- */
.stbl { width: 100%; border-collapse: collapse; font-size: 13px; }
.stbl th { text-align: left; font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1.6px; color: #6F7C86;
    font-weight: 600; padding: 8px 8px; background: #F6F9FC; border-bottom: 1px solid #E2EAF2; position: sticky; top: 0; z-index: 1; }
.stbl td { padding: 8px 8px; border-bottom: 1px solid #EEF0F3; color: #263746; background: #FFFFFF; }
.stbl tr:hover td { background: #F8FBFE; }
.stbl td:first-child { font-weight: 700; color: #0D1F33; }

/* ---------- PIPELINE ---------- */
.pipe { display: grid; grid-template-columns: 1fr auto 1fr auto 1fr auto 1fr; gap: 8px; align-items: center; margin-bottom: 4px; }
.pipe-box { background: #FFFFFF; border: 1px solid #DCE7F0; border-top: 4px solid var(--c); border-radius: 14px; padding: 9px 13px;
    box-shadow: 0 8px 20px rgba(15,39,64,0.08); }
.pipe-box .l { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 1.8px; color: #6F7C86; }
.pipe-box .v { font-size: 24px; font-weight: 800; color: var(--c); line-height: 1.1; margin-top: 2px; }
.pipe-arrow { color: #9AAAB8; font-size: 19px; font-weight: 700; }

/* ---------- ULTRA-COMPACT FULL-VIEW COLOR CALENDAR ---------- */
.cal-h {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9.5px;
    letter-spacing: 1.4px;
    color: #52687A;
    text-align: center;
    font-weight: 700;
    padding: 3px 0;
    background: #F1F6FB;
    border-radius: 7px;
}
.legend-row {
    display: flex;
    flex-wrap: wrap;
    gap: 9px;
    align-items: center;
    font-size: 11px;
    color: #4B5E6D;
    padding: 4px 10px;
    background: #F8FBFE;
    border-radius: 9px;
    border: 1px solid #E2ECF5;
}
.lg-dot { display: inline-block; width: 8px; height: 8px; border-radius: 3px; margin-right: 4px; }
.cal-dot-bar {
    height: 3.5px;
    border-radius: 3px;
    margin-top: -5px;
    margin-bottom: 1px;
}
.task-card {
    display: flex;
    flex-direction: column;
    gap: 4px;
    padding: 9px 12px;
    border-radius: 12px;
    background: #FFFFFF;
    border: 1px solid #E1E8F0;
    border-left: 5px solid var(--c);
    margin-bottom: 8px;
    box-shadow: 0 4px 12px rgba(15,39,64,0.05);
}
.task-card .t { font-weight: 700; color: #0D1F33; font-size: 14px; }
.task-card .d { color: #5B6F7E; font-size: 12.5px; }
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# 2. DATA & CONSTANTS
# =====================================================

STATUS_COLOR = {"Healthy": "#20A77A", "Warning": "#E5A04B", "Critical": "#E65D70"}
STATUS_BG = {"Healthy": "#E0F4EA", "Warning": "#FDF0D9", "Critical": "#FDE3E7"}

_M = [
    ("M-01", "Packaging Line", "Healthy", 94, 14, "Safe"),
    ("M-02", "Hydraulic Press", "Healthy", 92, 22, "Safe"),
    ("M-03", "Injection Molder", "Healthy", 90, 18, "Safe"),
    ("M-04", "CNC Mill", "Warning", 76, 64, "6 days"),
    ("M-05", "Welding Robot", "Healthy", 93, 16, "Safe"),
    ("M-06", "Lathe", "Healthy", 89, 20, "Safe"),
    ("M-07", "Air Compressor", "Critical", 58, 92, "2.5 days"),
    ("M-08", "Cooling System", "Healthy", 91, 35, "12 days"),
    ("M-09", "Boiler Feed Pump", "Healthy", 88, 24, "Safe"),
    ("M-10", "Conveyor", "Warning", 79, 58, "9 days"),
    ("M-11", "Paint Booth Fan", "Healthy", 92, 15, "Safe"),
    ("M-12", "Laser Cutter", "Healthy", 90, 19, "Safe"),
]
MACHINES = [dict(id=a, name=b, status=c, health=d, risk=e, limit=f) for a, b, c, d, e, f in _M]
BY_ID = {m["id"]: m for m in MACHINES}
IDS = [m["id"] for m in MACHINES]


def label(i):
    return f"{i} · {BY_ID[i]['name']}"


RELI = {
    "M-01": (7900, 2, 3.0), "M-02": (7600, 2, 3.5), "M-03": (7700, 3, 3.0), "M-04": (7500, 5, 4.6),
    "M-05": (7200, 1, 2.5), "M-06": (7800, 2, 3.0), "M-07": (8200, 8, 6.0), "M-08": (8300, 3, 3.5),
    "M-09": (7800, 2, 4.5), "M-10": (8000, 6, 4.5), "M-11": (6900, 1, 2.0), "M-12": (6500, 2, 3.0),
}
FAIL_MODE = {
    "M-01": "Seal bar wear", "M-02": "Hydraulic seal leak", "M-03": "Heater band failure", "M-04": "Spindle vibration",
    "M-05": "Wrist joint backlash", "M-06": "Spindle bearing wear", "M-07": "Bearing wear", "M-08": "Filter clogging",
    "M-09": "Pump seal leak", "M-10": "Drive motor overheating", "M-11": "Fan bearing noise", "M-12": "Optics contamination",
}
ALERT_TEXT = {
    "M-07": "Bearing wear · vibration 2.8x normal", "M-04": "Vibration drifting upward",
    "M-10": "Motor temperature spikes", "M-08": "Temperature fluctuation",
}

PRIORITIES = ["Low", "Medium", "High", "Critical"]
PRIO_STYLE = {"Low": ("#16865D", "#E0F4EA"), "Medium": ("#C77F1F", "#FDF0D9"),
              "High": ("#D9602F", "#FDE8DC"), "Critical": ("#C23A4F", "#FDE3E7")}
PRIO_DAYS = {"Critical": 1, "High": 2, "Medium": 4, "Low": 7}
STAGES = ["Pending", "Assigned", "In Progress", "Completed"]
STAGE_STYLE = {"Pending": ("#6F7C86", "#EEF1F4"), "Assigned": ("#17628D", "#DCEEFA"),
               "In Progress": ("#C77F1F", "#FDF0D9"), "Completed": ("#16865D", "#E0F4EA")}
TEAMS = ["Unassigned", "Maintenance Team A", "Maintenance Team B", "Maintenance Team C", "External Vendor"]

TASK_CATEGORY = {
    "Bearing inspection": "Inspection", "Vibration analysis": "Inspection",
    "Sensor calibration": "Preventive", "Lubrication": "Preventive", "Filter replacement": "Preventive",
    "Coolant top-up": "Preventive", "Motor servicing": "Preventive",
    "Bearing replacement": "Scheduled", "Belt replacement": "Scheduled", "Seal replacement": "Scheduled",
    "Full overhaul": "Scheduled", "Other": "Scheduled",
}
TASKS = list(TASK_CATEGORY)
CAT_STYLE = {"Scheduled": ("#2B84C0", "#DCEEFA"), "Inspection": ("#7A6FBD", "#ECE9F8"),
             "Preventive": ("#1B996B", "#E0F4EA"), "Overdue": ("#D94B5F", "#FDE3E7"), "Completed": ("#7A8794", "#EDF0F3")}
CAT_LABEL = {"Scheduled": "Scheduled", "Inspection": "Inspection", "Preventive": "Preventive",
             "Overdue": "Overdue", "Completed": "Completed"}

PARTS = {
    "SP-101": dict(name="Deep-groove bearing 6310", min=4, unit="pcs", lead=3, start=8),
    "SP-102": dict(name="Compressor bearing NU2214", min=2, unit="pcs", lead=5, start=0),
    "SP-103": dict(name="Hydraulic filter element", min=5, unit="pcs", lead=4, start=3),
    "SP-104": dict(name="Air filter cartridge", min=4, unit="pcs", lead=2, start=9),
    "SP-105": dict(name="Drive belt B-86", min=3, unit="pcs", lead=3, start=5),
    "SP-106": dict(name="Proximity sensor M18", min=3, unit="pcs", lead=6, start=2),
    "SP-107": dict(name="Temperature probe PT100", min=3, unit="pcs", lead=6, start=7),
    "SP-108": dict(name="Motor contactor 32A", min=2, unit="pcs", lead=4, start=4),
    "SP-109": dict(name="Coupling spider", min=2, unit="pcs", lead=3, start=6),
    "SP-110": dict(name="Bearing grease", min=6, unit="kg", lead=2, start=14),
    "SP-111": dict(name="Hydraulic seal kit", min=2, unit="kits", lead=7, start=1),
    "SP-112": dict(name="Coolant concentrate", min=20, unit="L", lead=2, start=40),
}
TASK_PARTS = {
    "Bearing inspection": [("SP-110", 1)], "Sensor calibration": [("SP-106", 1)], "Lubrication": [("SP-110", 2)],
    "Filter replacement": [("SP-103", 1), ("SP-104", 1)], "Coolant top-up": [("SP-112", 10)],
    "Motor servicing": [("SP-108", 1), ("SP-110", 1)], "Belt replacement": [("SP-105", 1)],
    "Seal replacement": [("SP-111", 1)], "Full overhaul": [("SP-101", 2), ("SP-111", 1), ("SP-110", 2)],
    "Vibration analysis": [], "Other": [],
}
RECS = [
    ("M-07", "Bearing replacement", "Critical", "Vibration 2.8x normal; limit in ~2.5 days.",
     "Inspect bearings, align shaft & replace worn parts."),
    ("M-04", "Vibration analysis", "High", "Vibration drifting upward; limit in ~6 days.",
     "Check spindle vibration, tool balance & lube."),
    ("M-10", "Motor servicing", "Medium", "Motor temp spikes; limit in ~9 days.",
     "Inspect drive motor windings, cooling & belt."),
    ("M-08", "Filter replacement", "Low", "Cooling loop temp fluctuation; limit in ~12 days.",
     "Replace coolant filter & check flow stability."),
]


def parts_for(task, mid):
    if task == "Bearing replacement":
        return [("SP-102" if mid == "M-07" else "SP-101", 2), ("SP-110", 1)]
    return TASK_PARTS.get(task, [])


def limit_days(m):
    try:
        return float(m["limit"].split()[0])
    except ValueError:
        return None


# =====================================================
# 3. STATE MANAGEMENT & DIRECT DASHBOARD REDIRECT
# =====================================================

DATE_KEYS = ("due", "created", "completed_on")


def seed_wos():
    d = lambda n: TODAY + timedelta(days=n)
    rows = [
        ("M-07", "Bearing inspection", "High", "Pending", "Unassigned", 1, "Inspect vibration levels and bearing condition."),
        ("M-02", "Sensor calibration", "Medium", "In Progress", "Maintenance Team B", 2, "Recalibrate the pressure transducer."),
        ("M-10", "Motor servicing", "Critical", "Pending", "Unassigned", 1, "Motor temperature spikes - check windings and cooling."),
        ("M-08", "Filter replacement", "Low", "Completed", "Maintenance Team A", -1, "Replaced coolant filter cartridge."),
        ("M-04", "Vibration analysis", "Medium", "Assigned", "Maintenance Team C", 3, "Spindle vibration drifting upward."),
        ("M-01", "Lubrication", "Low", "Pending", "Unassigned", 5, "Routine lubrication round."),
        ("M-09", "Lubrication", "Low", "Assigned", "Maintenance Team A", -2, "Pump bearing lubrication."),
        ("M-06", "Belt replacement", "Medium", "In Progress", "Maintenance Team B", -1, "Replace worn drive belt."),
        ("M-12", "Sensor calibration", "Low", "Pending", "Unassigned", -3, "Calibrate gantry axis sensor."),
        ("M-03", "Filter replacement", "Medium", "Assigned", "Maintenance Team C", 7, "Hydraulic filter change."),
        ("M-05", "Bearing inspection", "Medium", "Pending", "Unassigned", 12, "Check wrist joint backlash."),
        ("M-11", "Motor servicing", "Low", "Completed", "Maintenance Team A", -4, "Fan motor serviced."),
        ("M-03", "Seal replacement", "High", "Assigned", "Maintenance Team B", -5, "Replace leaking clamp seal."),
        ("M-02", "Lubrication", "Low", "Pending", "Unassigned", -6, "Press guide lubrication."),
        ("M-01", "Sensor calibration", "Low", "Completed", "Maintenance Team A", -6, "Seal bar sensor calibrated."),
        ("M-12", "Bearing inspection", "Low", "Completed", "Maintenance Team C", -9, "Gantry bearings OK."),
    ]
    out = []
    for i, (mid, task, prio, status, team, off, notes) in enumerate(rows, 1):
        done = status == "Completed"
        out.append(dict(id=f"WO-{1000 + i}", mid=mid, task=task, priority=prio, status=status, team=team,
                        due=d(off), notes=notes, created=d(off - 5), completed_on=d(off) if done else None,
                        repair_h=round(1.0 + (i % 3) * 0.5, 1) if done else None, source="Seed"))
    return out


def load_state():
    stock_ = {pid: p["start"] for pid, p in PARTS.items()}
    if PERSIST and DATA_FILE.exists():
        try:
            raw = json.loads(DATA_FILE.read_text())
            wos_ = raw["wos"]
            for r in wos_:
                for k in DATE_KEYS:
                    r[k] = date.fromisoformat(r[k]) if r.get(k) else None
            stock_.update({k: int(v) for k, v in raw.get("stock", {}).items() if k in stock_})
            return wos_, stock_
        except Exception:
            pass
    return seed_wos(), stock_


def save_state():
    if not PERSIST:
        return
    try:
        rows = []
        for w in st.session_state["hub_wos"]:
            r = dict(w)
            for k in DATE_KEYS:
                r[k] = r[k].isoformat() if r.get(k) else None
            rows.append(r)
        DATA_FILE.write_text(json.dumps(dict(wos=rows, stock=st.session_state["hub_stock"]), indent=1))
    except OSError:
        pass


def wos():
    return st.session_state["hub_wos"]


def stock(pid):
    return st.session_state["hub_stock"][pid]


def flash(msg):
    st.session_state["flash"] = msg


def new_id():
    nums = [int(w["id"].split("-")[1]) for w in wos()] or [1000]
    return f"WO-{max(nums) + 1}"


def add_wo(mid, task, priority, team, due, notes, source="Planner"):
    wo = dict(id=new_id(), mid=mid, task=task, priority=priority,
              status="Pending" if team == "Unassigned" else "Assigned", team=team, due=due, notes=notes,
              created=TODAY, completed_on=None, repair_h=None, source=source)
    wos().append(wo)
    save_state()
    return wo


def import_explorer_orders():
    legacy = st.session_state.get("work_orders", [])
    done = st.session_state.get("hub_imported", 0)
    for w in legacy[done:]:
        mid = str(w.get("Machine", "")).split(" ")[0]
        if mid not in BY_ID:
            continue
        try:
            due = date.fromisoformat(str(w.get("Due")))
        except ValueError:
            due = TODAY + timedelta(days=1)
        prio = {"Urgent": "Critical"}.get(w.get("Priority", "Medium"), w.get("Priority", "Medium"))
        add_wo(mid, w.get("Task", "Other"), prio if prio in PRIORITIES else "Medium", "Unassigned", due,
               "Raised from Machine Explorer", source="Machine Explorer")
    st.session_state["hub_imported"] = len(legacy)


def set_planner(mid, task, prio, notes, switch_tab=True):
    ss = st.session_state
    prio = "Critical" if prio == "Urgent" else prio
    ss["pl_machine"] = mid if mid in BY_ID else IDS[0]
    ss["pl_task"] = task if task in TASKS else "Other"
    ss["pl_prio"] = prio if prio in PRIORITIES else "Medium"
    ss["pl_team"] = "Maintenance Team A"
    ss["pl_date"] = TODAY + timedelta(days=PRIO_DAYS[ss["pl_prio"]])
    ss["pl_notes"] = notes
    if switch_tab:
        ss["active_subpage"] = "Action Planner"
    flash("Action Planner pre-filled — review and download or save!")


def init_state():
    ss = st.session_state
    if "hub_wos" not in ss:
        ss["hub_wos"], ss["hub_stock"] = load_state()
    ss.setdefault("hub_imported", 0)
    ss.setdefault("active_subpage", "Maintenance")
    ss.setdefault("selected_kpi", "due")
    ss.setdefault("pl_machine", "M-07")
    ss.setdefault("pl_task", "Bearing inspection")
    ss.setdefault("pl_prio", "High")
    ss.setdefault("pl_team", "Maintenance Team A")
    ss.setdefault("pl_date", TODAY + timedelta(days=2))
    ss.setdefault("pl_notes", "Inspect vibration levels and bearing condition.")
    ss.setdefault("cal_date", TODAY)

    # Direct redirect from Dashboard ("ACTION PLANNER >" button)
    for trigger_key in ("focus_action_planner", "open_action_planner", "goto_action_planner"):
        if ss.pop(trigger_key, False):
            ss["active_subpage"] = "Action Planner"

    if ss.get("nav_target") == "Action Planner" or ss.get("subpage") == "Action Planner":
        ss["active_subpage"] = "Action Planner"
        ss.pop("nav_target", None)
        ss.pop("subpage", None)

    req = ss.pop("planner_request", None)
    if req:
        set_planner(req.get("machine", "M-07"), req.get("task", "Other"), req.get("priority", "Medium"), req.get("notes", ""))


init_state()
import_explorer_orders()
_flash = st.session_state.pop("flash", None)
if _flash:
    st.toast(_flash, icon="✅")

# =====================================================
# 4. HELPERS & ANALYTICS
# =====================================================


def pill(text, fg, bg):
    return f'<span class="pill" style="color:{fg};background:{bg};">{esc(text)}</span>'


def status_chip(status):
    return (f'<span class="status-chip" style="color:{STATUS_COLOR[status]};'
            f'background:{STATUS_BG[status]};">● {status.upper()}</span>')


def category(w):
    if w["status"] == "Completed":
        return "Completed"
    if w["due"] < TODAY:
        return "Overdue"
    return TASK_CATEGORY.get(w["task"], "Scheduled")


def wo_date(w):
    return (w["completed_on"] or w["due"]) if w["status"] == "Completed" else w["due"]


def open_wos(mid=None):
    return [w for w in wos() if w["status"] != "Completed" and (mid is None or w["mid"] == mid)]


def part_state(pid, need=0):
    s = stock(pid)
    if s <= 0:
        return "Out of stock"
    if s < need:
        return "Short"
    if s < PARTS[pid]["min"]:
        return "Low stock"
    return "In stock"


INV_STYLE = {"In stock": ("#16865D", "#E0F4EA"), "Low stock": ("#C77F1F", "#FDF0D9"),
             "Short": ("#D9602F", "#FDE8DC"), "Out of stock": ("#C23A4F", "#FDE3E7")}
_SEVERITY = {"In stock": 0, "Low stock": 1, "Short": 2, "Out of stock": 3}


def parts_check(task, mid):
    return [(pid, PARTS[pid]["name"], q, stock(pid), part_state(pid, q)) for pid, q in parts_for(task, mid)]


def worst_state(rows):
    return max((r[4] for r in rows), key=lambda s: _SEVERITY[s], default="In stock")


def demand():
    dem = {pid: 0 for pid in PARTS}
    rows = []
    for w in open_wos():
        for pid, q in parts_for(w["task"], w["mid"]):
            dem[pid] += q
            rows.append((w, pid, q))
    return dem, rows


def style_fig(fig, height=230, legend=False):
    fig.update_layout(
        height=height,
        margin=dict(l=48, r=18, t=40 if legend else 16, b=34),
        paper_bgcolor="#FFFFFF",
        plot_bgcolor="#FFFFFF",
        font=dict(color="#52677A", size=12),
        hovermode="x unified",
        showlegend=legend,
    )
    if legend:
        fig.update_layout(legend=dict(orientation="h", y=1.16, x=0))
    fig.update_xaxes(gridcolor="#EEF1F5", automargin=True)
    fig.update_yaxes(gridcolor="#EEF1F5", automargin=True)
    return fig


def show(fig, key):
    st.plotly_chart(fig, use_container_width=True, theme=None, key=key, config={"displayModeBar": False})


def section(num, lab, title, sub=""):
    st.html(f'<div class="section-label">{num} — {lab}</div>'
            f'<div class="section-title">{title}</div>' + (f'<div class="panel-sub">{sub}</div>' if sub else ""))


@st.cache_data(show_spinner=False)
def build_history(_key):
    rng = np.random.default_rng(42)
    fail, planned, unplanned, health, risk = {}, {}, {}, {}, {}
    t = np.linspace(0, 1, 12)
    for m in MACHINES:
        mid = m["id"]
        _, f, mttr = RELI[mid]
        w = np.linspace(1.0, 1.0 + m["risk"] / 30, 12) * rng.uniform(0.7, 1.3, 12)
        fm = rng.multinomial(f, w / w.sum())
        fail[mid] = fm
        unplanned[mid] = np.round(fm * mttr, 1)
        planned[mid] = np.round(rng.uniform(1.0, 2.6, 12), 1)
        start = min(97.5, m["health"] + {"Critical": 38, "Warning": 17, "Healthy": 4}[m["status"]])
        h = start - (start - m["health"]) * t ** 2.2 + rng.normal(0, 0.6, 12)
        h[-1] = m["health"]
        health[mid] = np.round(np.clip(h, 0, 100), 1)
        r0 = {"Critical": 30, "Warning": 35}.get(m["status"], m["risk"] + int(rng.integers(-4, 5)))
        r = r0 + (m["risk"] - r0) * t ** 2.2 + rng.normal(0, 1.2, 12)
        r[-1] = m["risk"]
        risk[mid] = np.round(np.clip(r, 0, 100), 1)
    mk = lambda d: pd.DataFrame(d, index=MONTHS)
    return dict(fail=mk(fail), planned=mk(planned), unplanned=mk(unplanned), health=mk(health), risk=mk(risk))


@st.cache_data(show_spinner=False)
def seed_history(_key):
    rng = np.random.default_rng(7)
    tasks = [t for t in TASK_CATEGORY if t != "Other"]
    rows = []
    for _ in range(54):
        mid = IDS[int(rng.integers(0, 12))]
        task = tasks[int(rng.integers(0, len(tasks)))]
        done = bool(rng.random() < 0.88)
        rows.append({
            "Date": TODAY - timedelta(days=int(rng.integers(4, 350))), "ID": mid, "Machine": BY_ID[mid]["name"],
            "Task": task, "Type": TASK_CATEGORY[task], "Team": TEAMS[1 + int(rng.integers(0, 3))],
            "Repair h": round(float(rng.uniform(1, 7)), 1) if done else 0.0, "Status": "Completed" if done else "Pending",
        })
    return pd.DataFrame(rows)


H = build_history(NOW.strftime("%Y-%m"))
EFF_NOISE = np.random.default_rng(5).normal(0, 0.5, 12)


def history_df():
    live = [{"Date": wo_date(w), "ID": w["mid"], "Machine": BY_ID[w["mid"]]["name"], "Task": w["task"],
             "Type": TASK_CATEGORY.get(w["task"], "Scheduled"), "Team": w["team"],
             "Repair h": float(w["repair_h"] or 0.0), "Status": "Completed" if w["status"] == "Completed" else "Pending"}
            for w in wos()]
    return pd.concat([seed_history(str(TODAY)), pd.DataFrame(live)], ignore_index=True)


def downtime_frames(ids):
    planned, unplanned = H["planned"][ids].copy(), H["unplanned"][ids].copy()
    for w in wos():
        if w["status"] == "Completed" and w["completed_on"] and w["repair_h"] and w["mid"] in ids:
            ts = pd.Timestamp(w["completed_on"].replace(day=1))
            if ts in planned.index:
                (unplanned if TASK_CATEGORY.get(w["task"]) == "Scheduled" else planned).loc[ts, w["mid"]] += float(w["repair_h"])
    return planned, unplanned


def efficiency(planned, unplanned):
    total = (planned + unplanned).mean(axis=1).values
    return pd.Series(np.clip(96 - 2.2 * total + EFF_NOISE, 70, 99), index=MONTHS)


def reliability(ids, mask=None):
    mask = np.ones(12, bool) if mask is None else mask
    n = int(mask.sum())
    f = H["fail"].loc[mask, ids].sum()
    rep = H["unplanned"].loc[mask, ids].sum()
    rows = []
    for mid in ids:
        hrs = RELI[mid][0] * n / 12
        fl = int(f[mid])
        mtbf = hrs / fl if fl else hrs
        mttr = float(rep[mid]) / fl if fl else 0.0
        av = mtbf / (mtbf + mttr) * 100 if (mtbf + mttr) else 100.0
        rows.append({"ID": mid, "Machine": BY_ID[mid]["name"], "Operating h": round(hrs), "Failures": fl,
                     "MTBF h": round(mtbf, 1), "MTTR h": round(mttr, 2), "Availability %": round(av, 2),
                     "Repair h": round(float(rep[mid]), 1)})
    return pd.DataFrame(rows)


def make_pdf(title, subtitle, lines, df, base):
    try:
        from reportlab.lib import colors
        from reportlab.lib.pagesizes import A4, landscape
        from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
        from reportlab.lib.units import mm
        from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

        buf = BytesIO()
        doc = SimpleDocTemplate(buf, pagesize=landscape(A4), leftMargin=12 * mm, rightMargin=12 * mm,
                                topMargin=12 * mm, bottomMargin=12 * mm, title=title)
        ss = getSampleStyleSheet()
        h1 = ParagraphStyle("h1", parent=ss["Title"], textColor=colors.HexColor("#183B5B"), alignment=0)
        cell = ParagraphStyle("cell", parent=ss["BodyText"], fontSize=8, leading=10)
        head = ParagraphStyle("head", parent=cell, textColor=colors.white, fontName="Helvetica-Bold")
        rows = [[Paragraph(esc(c), head) for c in df.columns]]
        for rec in df.astype(str).values.tolist():
            rows.append([Paragraph(esc(v), cell) for v in rec])
        width = landscape(A4)[0] - 24 * mm
        tbl = Table(rows, colWidths=[width / len(df.columns)] * len(df.columns), repeatRows=1)
        tbl.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#183B5B")),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F1F6FC")]),
            ("GRID", (0, 0), (-1, -1), 0.4, colors.HexColor("#C9D9E7")),
            ("VALIGN", (0, 0), (-1, -1), "TOP"),
        ]))
        story = [Paragraph(esc(title), h1), Paragraph(esc(subtitle), ss["Normal"]), Spacer(1, 3 * mm)]
        story += [Paragraph(esc(x), ss["BodyText"]) for x in lines]
        story += [Spacer(1, 3 * mm), tbl]
        doc.build(story)
        return buf.getvalue(), f"{base}.pdf", "application/pdf"
    except ImportError:
        txt = "\n".join([title, subtitle, ""] + lines + ["", df.to_string(index=False)])
        return txt.encode("utf-8"), f"{base}.txt", "text/plain"


# =====================================================
# 5. SINGLE-ROW HEADER + NOTIFICATION BELL (Exact Machine Explorer Position & Font)
# =====================================================

due_machines = [m for m in MACHINES if m["risk"] >= 35]
overdue_list = [w for w in open_wos() if category(w) == "Overdue"]
total_notifs = len(due_machines) + len(overdue_list)

hdr_left, hdr_right = st.columns([5.3, 1], vertical_alignment="bottom")
with hdr_left:
    st.html(
        """
        <div class="page-eyebrow">ANOMATRIX · MAINTENANCE &amp; REPORTS</div>
        <div class="page-main-title">Maintenance Hub &amp; Reports Analytics</div>
        """
    )
with hdr_right:
    with st.popover(f"🔔  ({total_notifs})", use_container_width=True):
        st.markdown(f"**Active Notifications ({total_notifs})**")
        for m in sorted(due_machines, key=lambda x: -x["risk"]):
            fg, bg = PRIO_STYLE["Critical" if m["risk"] >= 80 else "Medium" if m["risk"] >= 50 else "Low"]
            st.html(
                f'<div class="al-row">{pill(m["status"].upper(), fg, bg)}'
                f'<span style="flex:1;"><b>{m["id"]} {m["name"]}</b> · {ALERT_TEXT[m["id"]]} (limit {m["limit"]})</span></div>'
            )
        for w in overdue_list[:3]:
            st.html(
                f'<div class="al-row">{pill("OVERDUE", "#C23A4F", "#FDE3E7")}'
                f'<span style="flex:1;"><b>{w["id"]} · {w["mid"]}</b> — {esc(w["task"])}</span></div>'
            )

st.html('<hr class="header-divider">')

# 3 Sub-Page Banners: 01 Maintenance | 02 Action Planner (Middle) | 03 Reports
active_page = st.session_state["active_subpage"]
b_col1, b_col2, b_col3 = st.columns(3, gap="small")
BANNERS = [
    ("Maintenance", "🛠️  01 · Maintenance", b_col1),
    ("Action Planner", "🗓️  02 · Action Planner", b_col2),
    ("Reports", "📊  03 · Reports", b_col3),
]
for key_name, btn_label, col in BANNERS:
    with col:
        if st.button(
            btn_label,
            key=f"banner_{key_name}",
            type="primary" if active_page == key_name else "secondary",
            use_container_width=True,
        ):
            st.session_state["active_subpage"] = key_name
            st.rerun()


# =====================================================
# SUB-PAGE 1: MAINTENANCE
# =====================================================

if active_page == "Maintenance":
    section("01", "MAINTENANCE OVERVIEW", "Maintenance at a glance")

    open_list = open_wos()
    done_list = [w for w in wos() if w["status"] == "Completed"]
    compliance_pct = int(round(len(done_list) / max(len(wos()), 1) * 100))

    CARDS = [
        ("due", "MAINTENANCE DUE", f"{len(due_machines):02d}", "Machines requiring service", "#E5A04B"),
        ("open", "OPEN WORK ORDERS", f"{len(open_list):02d}", "Pending maintenance tasks", "#328BC5"),
        ("overdue", "OVERDUE TASKS", f"{len(overdue_list):02d}", "Past scheduled date", "#E65D70"),
        ("compliance", "COMPLIANCE", f"{compliance_pct}%", "Tasks completed on time", "#20A77A"),
    ]

    sel_kpi = st.session_state["selected_kpi"]
    kcols = st.columns(4, gap="small")
    for col, (cid, lab, val, desc, color) in zip(kcols, CARDS):
        with col:
            cls = "cc-kpi active" if sel_kpi == cid else "cc-kpi"
            st.html(
                f'<div class="{cls}" style="--c:{color};">'
                f'<div class="l">{lab}</div>'
                f'<div class="v">{val}</div>'
                f'<div class="d">{desc}</div>'
                f'<div class="bar-accent"></div>'
                f'</div>'
            )
            if st.button("View quick details", key=f"kpi_btn_{cid}", use_container_width=True):
                st.session_state["selected_kpi"] = cid
                st.rerun()

    # Pure White Pop-out Quick Details Card
    sel_kpi = st.session_state["selected_kpi"]
    with st.container(border=True):
        if sel_kpi == "due":
            st.html('<div class="panel-title">Quick Details · Machines Requiring Service</div>')
            rows_html = ""
            for m in sorted(due_machines, key=lambda x: -x["risk"]):
                fg, bg = PRIO_STYLE["Critical" if m["risk"] >= 80 else "Medium" if m["risk"] >= 50 else "Low"]
                ow = open_wos(m["id"])
                wo_txt = f"{ow[0]['id']} ({ow[0]['status']})" if ow else "No WO assigned"
                rows_html += (f'<div class="al-row">{pill(m["status"].upper(), fg, bg)}'
                              f'<span style="flex:1;"><b>{m["id"]} {m["name"]}</b> · {ALERT_TEXT[m["id"]]} · limit in {m["limit"]}</span>'
                              f'<span>{wo_txt} · Risk <b>{m["risk"]}</b></span></div>')
            st.html(rows_html)
        elif sel_kpi == "open":
            st.html('<div class="panel-title">Quick Details · Open Work Orders</div>')
            rows_html = "".join(
                f'<div class="al-row">{pill(w["priority"], *PRIO_STYLE[w["priority"]])}'
                f'<span style="flex:1;"><b>{w["id"]} · {w["mid"]} {BY_ID[w["mid"]]["name"]}</b> — {esc(w["task"])}</span>'
                f'<span>{esc(w["team"])} · Due <b>{w["due"]:%d %b}</b></span></div>'
                for w in sorted(open_list, key=lambda x: x["due"])[:6]
            ) or '<div class="verdict ok">No open work orders.</div>'
            st.html(rows_html)
        elif sel_kpi == "overdue":
            st.html('<div class="panel-title">Quick Details · Overdue Tasks</div>')
            rows_html = "".join(
                f'<div class="al-row">{pill("OVERDUE", "#C23A4F", "#FDE3E7")}'
                f'<span style="flex:1;"><b>{w["id"]} · {w["mid"]} {BY_ID[w["mid"]]["name"]}</b> — {esc(w["task"])}</span>'
                f'<span style="color:#C23A4F;font-weight:700;">Was due {w["due"]:%d %b} ({(TODAY - w["due"]).days}d late)</span></div>'
                for w in sorted(overdue_list, key=lambda x: x["due"])
            ) or '<div class="verdict ok">Zero overdue tasks!</div>'
            st.html(rows_html)
        else:
            st.html('<div class="panel-title">Quick Details · Completed & Compliance Summary</div>')
            rows_html = "".join(
                f'<div class="al-row">{pill("DONE", "#16865D", "#E0F4EA")}'
                f'<span style="flex:1;"><b>{w["id"]} · {w["mid"]} {BY_ID[w["mid"]]["name"]}</b> — {esc(w["task"])}</span>'
                f'<span>{esc(w["team"])} · {w["repair_h"] or 1.5} h</span></div>'
                for w in done_list[:6]
            )
            st.html(rows_html)

    # Pure White Pop-out AI Recommendations Cards
    section("02", "PREDICTIVE MAINTENANCE", "AI recommendations",
            "Click 'Plan in Action Planner' to jump directly to the Action Planner with pre-filled details.")
    for col, (mid, task, prio, why, how) in zip(st.columns(4, gap="small"), RECS):
        m = BY_ID[mid]
        with col:
            with st.container(border=True):
                fg, bg = PRIO_STYLE[prio]
                chk = parts_check(task, mid)
                ws = worst_state(chk)
                pf, pb = INV_STYLE[ws]
                parts_txt = "No parts needed" if not chk else ("Parts available" if ws == "In stock" else f"Parts: {ws.lower()}")
                st.html(
                    f'<div class="rec-top"><span class="rec-id">{mid}</span>{pill(prio.upper(), fg, bg)}</div>'
                    f'<div class="rec-name">{m["name"]}</div><div class="rec-task">🛠 {task}</div>'
                    f'<div class="rec-why">{why}<br><span style="color:#7A8791;">{how}</span></div>'
                    f'{pill(parts_txt, pf, pb)}'
                )
                exists = any(w["task"] == task for w in open_wos(mid))
                st.button(
                    "✔ Work order exists" if exists else "Plan in Action Planner →",
                    key=f"rec_{mid}",
                    disabled=exists,
                    on_click=set_planner,
                    args=(mid, task, prio, f"{how} ({why})", True),
                    use_container_width=True,
                )

    section("03", "WORK ORDER MANAGEMENT", "Create, assign and track maintenance tasks")
    cnt = {s: sum(1 for w in wos() if w["status"] == s) for s in STAGES}
    pipe_cols = {"Pending": "#6F7C86", "Assigned": "#328BC5", "In Progress": "#E5A04B", "Completed": "#20A77A"}
    boxes = [f'<div class="pipe-box" style="--c:{pipe_cols[s]};"><div class="l">{s.upper()}</div><div class="v">{cnt[s]}</div></div>' for s in STAGES]
    st.html('<div class="pipe">' + '<div class="pipe-arrow">→</div>'.join(boxes) + "</div>")

    with st.container(border=True):
        f1, f2, f3, f4 = st.columns([1.4, 1.4, 1.2, 0.8], vertical_alignment="bottom")
        fp = f1.multiselect("Priority", PRIORITIES, default=PRIORITIES, key="f_prio")
        fs = f2.multiselect("Status", STAGES, default=STAGES, key="f_stat")
        fm = f3.selectbox("Machine", ["All machines"] + IDS, key="f_mach", format_func=lambda i: i if i == "All machines" else label(i))
        fo = f4.checkbox("Overdue only", key="f_over")
        rows = [w for w in wos() if w["priority"] in fp and w["status"] in fs
                and (fm == "All machines" or w["mid"] == fm) and (not fo or category(w) == "Overdue")]
        rows.sort(key=lambda w: (w["status"] == "Completed", -PRIORITIES.index(w["priority"]), w["due"]))
        if rows:
            body = ""
            for w in rows:
                over = category(w) == "Overdue"
                due = (f'<span style="color:#C23A4F;font-weight:700;">{w["due"]:%d %b} · overdue</span>' if over
                       else f'{w["due"]:%d %b %Y}')
                body += (f'<tr><td>{w["id"]}</td><td><b>{w["mid"]}</b> {esc(BY_ID[w["mid"]]["name"])}</td><td>{esc(w["task"])}</td>'
                         f'<td>{pill(w["priority"], *PRIO_STYLE[w["priority"]])}</td><td>{pill(w["status"], *STAGE_STYLE[w["status"]])}</td>'
                         f'<td>{esc(w["team"])}</td><td>{due}</td></tr>')
            st.html('<div style="max-height:260px;overflow:auto;"><table class="stbl"><thead><tr><th>ID</th><th>MACHINE</th><th>TASK</th>'
                    f'<th>PRIORITY</th><th>STATUS</th><th>ASSIGNED TO</th><th>DUE</th></tr></thead><tbody>{body}</tbody></table></div>')
        else:
            st.info("No work orders match the filters.")

    section("04", "SPARE PARTS INVENTORY", "Stock and component availability")
    dem, dem_rows = demand()
    states = {pid: part_state(pid, dem[pid]) for pid in PARTS}

    s_left, s_right = st.columns([1.35, 1], gap="small")
    with s_left:
        with st.container(border=True):
            body = ""
            for pid, p in PARTS.items():
                s = stock(pid)
                fg, bg = INV_STYLE[states[pid]]
                pct = min(100, s / max(p["min"] * 2, s, 1) * 100)
                body += (f'<tr><td>{pid}</td><td>{esc(p["name"])}</td><td><b>{s}</b> {p["unit"]}'
                         f'<div class="bar" style="margin-top:4px;"><div style="width:{pct:.0f}%;background:{fg};"></div></div></td>'
                         f'<td>{p["min"]}</td><td>{dem[pid]}</td><td>{pill(states[pid], fg, bg)}</td></tr>')
            st.html('<div class="panel-title">Spare parts availability</div><div style="max-height:280px;overflow:auto;">'
                    '<table class="stbl"><thead><tr><th>ID</th><th>PART</th><th>IN STOCK</th><th>MIN</th><th>NEEDED</th><th>STATUS</th></tr></thead>'
                    f'<tbody>{body}</tbody></table></div>')

    with s_right:
        with st.container(border=True):
            st.html('<div class="panel-title">Parts required for upcoming maintenance</div>')
            pm = st.selectbox("Filter machine", ["All machines"] + IDS, key="inv_machine",
                              format_func=lambda i: i if i == "All machines" else label(i), label_visibility="collapsed")
            pbody = ""
            for w, pid, q in sorted(dem_rows, key=lambda r: r[0]["due"]):
                if pm != "All machines" and w["mid"] != pm:
                    continue
                s = part_state(pid, q)
                fg, bg = INV_STYLE[s]
                act = f'<span style="color:#C23A4F;font-weight:700;">Order ({PARTS[pid]["lead"]}d)</span>' if s in ("Short", "Out of stock") else '<span style="color:#16865D;">Ready</span>'
                pbody += (f'<tr><td><b>{w["mid"]}</b></td><td>{esc(PARTS[pid]["name"])} (×{q})</td>'
                          f'<td>{w["due"]:%d %b}</td><td>{pill(s, fg, bg)}</td><td>{act}</td></tr>')
            if pbody:
                st.html('<div style="max-height:185px;overflow:auto;"><table class="stbl"><thead><tr><th>MACH</th><th>COMPONENT</th><th>DUE</th><th>STATUS</th><th>ACTION</th></tr></thead>'
                        f'<tbody>{pbody}</tbody></table></div>')
            else:
                st.html('<div class="verdict ok">No spare parts required for this selection.</div>')

            r1, r2, r3 = st.columns([2, 0.9, 1.1])
            r_pid = r1.selectbox("Part", list(PARTS), key="rs_part", format_func=lambda p: f"{p} · {PARTS[p]['name']}", label_visibility="collapsed")
            r_qty = r2.number_input("Qty", min_value=1, max_value=500, value=5, key="rs_qty", label_visibility="collapsed")
            if r3.button("+ Receive", key="rs_btn", use_container_width=True):
                st.session_state["hub_stock"][r_pid] += int(r_qty)
                save_state()
                flash(f"+{int(r_qty)} {PARTS[r_pid]['unit']} added to {PARTS[r_pid]['name']}")
                st.rerun()


# =====================================================
# SUB-PAGE 2 (MIDDLE): ACTION PLANNER
# =====================================================

elif active_page == "Action Planner":
    ap_top_l, ap_top_r = st.columns([3.2, 1.3], vertical_alignment="center")
    with ap_top_l:
        section("01", "ACTION PLANNER", "Schedule calendar & maintenance action planner")
    with ap_top_r:
        cur_mid = st.session_state.get("pl_machine", "M-07")
        cur_task = st.session_state.get("pl_task", "Bearing inspection")
        cur_prio = st.session_state.get("pl_prio", "High")
        cur_team = st.session_state.get("pl_team", "Maintenance Team A")
        cur_due = st.session_state.get("pl_date", TODAY + timedelta(days=2))
        cur_notes = st.session_state.get("pl_notes", "")
        cur_parts_str = ", ".join(f"{PARTS[p]['name']} x{q}" for p, q in parts_for(cur_task, cur_mid)) or "None required"

        plan_export_df = pd.DataFrame([{
            "Machine": label(cur_mid),
            "Health & Risk": f"Health {BY_ID[cur_mid]['health']}% | Risk {BY_ID[cur_mid]['risk']}/100 ({BY_ID[cur_mid]['status']})",
            "Maintenance Task": cur_task,
            "Priority": cur_prio,
            "Assigned Team": cur_team,
            "Scheduled Date": f"{cur_due:%d %b %Y}",
            "Required Parts": cur_parts_str,
            "Action Notes": cur_notes or "-",
        }])
        ap_bytes, ap_fname, ap_mime = make_pdf(
            "ANOMATRIX - Maintenance Action Plan",
            f"Generated {pd.Timestamp.now():%d %b %Y, %I:%M %p}",
            [
                f"Target Machine: {label(cur_mid)} | Status: {BY_ID[cur_mid]['status']} | Limit: {BY_ID[cur_mid]['limit']}",
                f"Task: {cur_task} ({cur_prio} Priority) | Team: {cur_team} | Scheduled: {cur_due:%d %b %Y}",
                f"Notes: {cur_notes or 'Standard inspection & service.'}",
            ],
            plan_export_df,
            f"action_plan_{cur_mid}",
        )
        st.download_button(
            "⬇️ Generate Action Plan",
            ap_bytes,
            file_name=ap_fname,
            mime=ap_mime,
            key="top_gen_action_plan",
            type="primary",
            use_container_width=True,
        )

    def render_day_tasks_body(target_d):
        day_items = [w for w in wos() if wo_date(w) == target_d]
        if day_items:
            st.html("".join(
                f'<div class="task-card" style="--c:{CAT_STYLE[category(w)][0]};">'
                f'<div class="t">{w["id"]} · {w["mid"]} {esc(BY_ID[w["mid"]]["name"])}</div>'
                f'<div class="d"><b>Task:</b> {esc(w["task"])} · <b>Team:</b> {esc(w["team"])}</div>'
                f'<div class="d"><b>Notes:</b> {esc(w["notes"] or "-")}</div>'
                f'<div>{pill(CAT_LABEL[category(w)], *CAT_STYLE[category(w)])} '
                f'{pill(w["priority"], *PRIO_STYLE[w["priority"]])} '
                f'{pill(w["status"], *STAGE_STYLE[w["status"]])}</div></div>'
                for w in day_items
            ))
        else:
            st.html('<div class="verdict ok">No maintenance work assigned on this date.</div>')

    if hasattr(st, "dialog"):
        @st.dialog("📅 Assigned Maintenance Tasks")
        def show_calendar_popup(target_d):
            st.markdown(f"#### {target_d:%A, %d %B %Y}")
            render_day_tasks_body(target_d)
            if st.button("Close", use_container_width=True):
                st.session_state.pop("cal_popup_date", None)
                st.rerun()

        if st.session_state.get("cal_popup_date"):
            pop_d = st.session_state.pop("cal_popup_date")
            show_calendar_popup(pop_d)

    def shift_month(delta):
        d = st.session_state["cal_date"]
        mth = d.month - 1 + delta
        y, mth = d.year + mth // 12, mth % 12 + 1
        st.session_state["cal_date"] = date(y, mth, min(d.day, calendar.monthrange(y, mth)[1]))

    # Ultra-Compact Color-Coded Calendar (Fits cleanly on screen without scrolling)
    _, cal_center, _ = st.columns([0.25, 3.5, 0.25])
    with cal_center:
        with st.container(border=True):
            c_top1, c_top2, c_top3, c_top4 = st.columns([0.35, 0.35, 1.7, 3.7], vertical_alignment="center")
            c_top1.button("◀", key="cal_prev", on_click=shift_month, args=(-1,), use_container_width=True)
            c_top2.button("▶", key="cal_next", on_click=shift_month, args=(1,), use_container_width=True)
            sel_d = st.session_state["cal_date"]
            c_top3.html(f'<div style="font-size:16px;font-weight:700;color:#0D1F33;">📅 {sel_d:%B %Y}</div>')
            c_top4.html('<div class="legend-row" style="margin:0;justify-content:flex-end;">' + "".join(
                f'<span><span class="lg-dot" style="background:{CAT_STYLE[k][0]}"></span>{CAT_LABEL[k]}</span>' for k in CAT_STYLE) + "</div>")

            by_day = {}
            for w in wos():
                by_day.setdefault(wo_date(w), []).append(w)

            hcols = st.columns(7, gap="small")
            for hc, dname in zip(hcols, ["MON", "TUE", "WED", "THU", "FRI", "SAT", "SUN"]):
                hc.html(f'<div class="cal-h">{dname}</div>')

            cal_weeks = calendar.Calendar(firstweekday=0).monthdatescalendar(sel_d.year, sel_d.month)
            for wk in cal_weeks:
                wcols = st.columns(7, gap="small")
                for col, d in zip(wcols, wk):
                    with col:
                        items = by_day.get(d, [])
                        if d.month != sel_d.month:
                            btn_txt = f"· {d.day} ·"
                            bar_color = "transparent"
                        elif items:
                            top_cat = category(items[0])
                            bar_color = CAT_STYLE[top_cat][0]
                            mids = ",".join(w["mid"].replace("M-", "") for w in items[:2])
                            btn_txt = f"{d.day} · {mids}"
                        else:
                            btn_txt = f"{d.day}"
                            bar_color = "transparent"

                        is_today_or_sel = (d == TODAY or d == sel_d)
                        if st.button(
                            btn_txt,
                            key=f"cal_btn_{d.isoformat()}",
                            type="primary" if is_today_or_sel else "secondary",
                            use_container_width=True,
                        ):
                            st.session_state["cal_date"] = d
                            st.session_state["cal_popup_date"] = d
                            st.rerun()
                        if bar_color != "transparent":
                            st.html(f'<div class="cal-dot-bar" style="background:{bar_color};"></div>')

    # Maintenance Action Planner + Plan Review (White Pop-out Cards)
    pl_l, pl_r = st.columns([1.35, 1], gap="small")
    with pl_l:
        with st.container(border=True):
            st.html('<div class="panel-title">Maintenance Action Planner</div>')
            c1, c2 = st.columns(2)
            p_mid = c1.selectbox("Machine selection", IDS, key="pl_machine", format_func=label)
            p_task = c2.selectbox("Maintenance task", TASKS, key="pl_task")
            p_prio = st.radio("Priority", PRIORITIES, horizontal=True, key="pl_prio")
            c3, c4 = st.columns(2)
            p_team = c3.selectbox("Assign to", TEAMS, key="pl_team")
            p_due = c4.date_input("Scheduled date", key="pl_date", min_value=TODAY)
            p_notes = st.text_area("Action notes", key="pl_notes", height=75,
                                   placeholder="Inspect vibration levels and bearing condition.")
            if st.button("Save Action Plan", key="pl_go", type="primary", use_container_width=True):
                wo = add_wo(p_mid, p_task, p_prio, p_team, p_due, p_notes.strip(), source="Action Planner")
                st.session_state["last_plan_id"] = wo["id"]
                st.toast(f"{wo['id']} saved for {p_mid}", icon="🛠️")

    with pl_r:
        with st.container(border=True):
            m = BY_ID[p_mid]
            chk = parts_check(p_task, p_mid)
            lim = limit_days(m)
            prow = "".join(
                f'<div class="al-row">{pill(s, *INV_STYLE[s])}<span style="flex:1;"><b>{esc(n)}</b> × {q}</span>'
                f'<span style="color:#7A8791;">stock {st_}</span></div>'
                for _, n, q, st_, s in chk) or '<div class="panel-sub">No spare parts required for this task.</div>'
            notes_html = ""
            if lim is not None and (p_due - TODAY).days > lim:
                notes_html += f'<div class="verdict bad">Scheduled {p_due:%d %b} is after the predicted limit (~{m["limit"]}). Move the date earlier.</div>'
            short = [pid for pid, q in parts_for(p_task, p_mid) if part_state(pid, q) in ("Short", "Out of stock")]
            if short:
                lead = max(PARTS[pid]["lead"] for pid in short)
                notes_html += f'<div class="verdict bad">Parts must be ordered first (lead time ~{lead} days).</div>'
            st.html(
                f'<div class="panel-title">Plan review</div>'
                f'<div style="display:flex;justify-content:space-between;align-items:center;">'
                f'<div><div class="rec-id">{m["id"]}</div><div class="rec-name">{m["name"]}</div></div>'
                f'{status_chip(m["status"])}</div>'
                f'<div class="tile-grid"><div class="tile"><div class="l">HEALTH</div><div class="v">{m["health"]}%</div></div>'
                f'<div class="tile"><div class="l">RISK</div><div class="v">{m["risk"]}/100</div></div>'
                f'<div class="tile"><div class="l">TIME TO LIMIT</div><div class="v">{m["limit"]}</div></div></div>'
                f'<div style="font-weight:700;color:#0D1F33;margin:10px 0 4px;font-size:14px;">Spare parts check</div>{prow}{notes_html}'
            )
            lp = next((w for w in wos() if w["id"] == st.session_state.get("last_plan_id")), None)
            if lp:
                st.html(f'<div class="verdict ok"><b>{lp["id"]}</b> saved · {lp["mid"]} · {esc(lp["task"])} · due {lp["due"]:%d %b %Y}.</div>')


# =====================================================
# SUB-PAGE 3: REPORTS
# =====================================================

elif active_page == "Reports":
    section("01", "RELIABILITY ANALYTICS", "MTBF, MTTR, availability and failure analysis",
            "Last 12 months across all 12 machines.")

    REL = reliability(IDS)
    tot_h, tot_f, tot_rep = REL["Operating h"].sum(), REL["Failures"].sum(), REL["Repair h"].sum()
    f_mtbf = tot_h / tot_f
    f_mttr = tot_rep / tot_f
    f_av = f_mtbf / (f_mtbf + f_mttr) * 100

    FORMULAS = [
        (r"MTBF=\frac{\text{Total Operating Hours}}{\text{Number of Failures}}", "MTBF · MEAN TIME BETWEEN FAILURES",
         f"{f_mtbf:,.0f} h", "Average hours a machine runs without failure", "#328BC5"),
        (r"MTTR=\frac{\text{Total Repair Time}}{\text{Number of Repairs}}", "MTTR · MEAN TIME TO REPAIR",
         f"{f_mttr:.1f} h", "Average time needed to repair a machine", "#8A80C5"),
        (r"A=\frac{MTBF}{MTBF+MTTR}\times 100", "MACHINE AVAILABILITY",
         f"{f_av:.2f}%", "Share of time a machine is able to operate", "#20A77A"),
    ]
    for col, (tex, title, val, desc, color) in zip(st.columns(3, gap="small"), FORMULAS):
        with col:
            st.html(
                f'<div class="cc-kpi" style="--c:{color};">'
                f'<div class="l">{title}</div>'
                f'<div class="v">{val}</div>'
                f'<div class="d">{desc}</div>'
                f'<div class="bar-accent"></div>'
                f'</div>'
            )
            with st.container(border=True):
                st.latex(tex)

    planned_all, unplanned_all = downtime_frames(IDS)
    g1, g2, g3 = st.columns(3, gap="small")

    with g1:
        with st.container(border=True):
            st.html('<div class="panel-title">MTBF vs MTTR comparison</div>')
            fig = go.Figure()
            fig.add_trace(go.Bar(x=REL["ID"], y=REL["MTBF h"], name="MTBF (h)", marker_color="#328BC5",
                                 customdata=REL["Machine"], hovertemplate="%{customdata}<br>MTBF %{y:,.0f} h<extra></extra>"))
            fig.add_trace(go.Scatter(x=REL["ID"], y=REL["MTTR h"], name="MTTR (h)", mode="lines+markers", yaxis="y2",
                                     line=dict(color="#E5A04B", width=2.5), marker=dict(size=7),
                                     hovertemplate="MTTR %{y:.1f} h<extra></extra>"))
            style_fig(fig, 230, legend=True)
            fig.update_layout(margin=dict(l=44, r=44, t=38, b=30),
                              yaxis=dict(title="MTBF (h)"), yaxis2=dict(title="MTTR (h)", overlaying="y", side="right", showgrid=False))
            show(fig, "rep_mtbf_mttr")

    with g2:
        with st.container(border=True):
            st.html('<div class="panel-title">Monthly machine failure trend</div>')
            ft = H["fail"].sum(axis=1)
            fig = go.Figure(go.Scatter(x=MONTHS, y=ft, mode="lines+markers", fill="tozeroy",
                                       fillcolor="rgba(230,93,112,0.12)", line=dict(color="#E65D70", width=2.5),
                                       hovertemplate="%{y} failures<extra></extra>"))
            style_fig(fig, 230)
            fig.update_xaxes(tickformat="%b")
            fig.update_yaxes(title_text="Failures", rangemode="tozero")
            show(fig, "rep_fail_trend")

    with g3:
        with st.container(border=True):
            st.html('<div class="panel-title">Planned vs unplanned downtime</div>')
            fig = go.Figure()
            fig.add_trace(go.Bar(x=MONTHS, y=planned_all.sum(axis=1), name="Planned (h)", marker_color="#328BC5"))
            fig.add_trace(go.Bar(x=MONTHS, y=unplanned_all.sum(axis=1), name="Unplanned (h)", marker_color="#E65D70"))
            style_fig(fig, 230, legend=True)
            fig.update_layout(barmode="stack")
            fig.update_xaxes(tickformat="%b")
            fig.update_yaxes(title_text="Hours")
            show(fig, "rep_downtime")

    w_col, t_col = st.columns([1, 1.85], gap="small")
    with w_col:
        with st.container(border=True):
            worst_av = REL.loc[REL["Availability %"].idxmin()]
            worst_rep = REL.loc[REL["MTTR h"].idxmax()]
            worst_f = REL.loc[REL["Failures"].idxmax()]
            unpl_share = unplanned_all.values.sum() / (unplanned_all.values.sum() + planned_all.values.sum()) * 100
            st.html(
                '<div class="panel-title">What the numbers say</div>'
                f'<div class="al-row"><span style="flex:1;">Lowest availability</span><b>{worst_av["ID"]} · {worst_av["Availability %"]:.2f}%</b></div>'
                f'<div class="al-row"><span style="flex:1;">Slowest to repair</span><b>{worst_rep["ID"]} · {worst_rep["MTTR h"]:.1f} h</b></div>'
                f'<div class="al-row"><span style="flex:1;">Most failures</span><b>{worst_f["ID"]} · {int(worst_f["Failures"])}</b></div>'
                f'<div class="al-row"><span style="flex:1;">Unplanned downtime share</span><b>{unpl_share:.0f}%</b></div>'
                f'<div class="verdict"><b>Takeaway:</b> {worst_f["ID"]} ({esc(worst_f["Machine"])}) combines the most failures with a long repair time — move it to predictive maintenance first.</div>'
            )

    with t_col:
        with st.container(border=True):
            st.html('<div class="panel-title">Machine-wise reliability</div>')
            st.dataframe(
                REL.drop(columns=["Repair h"]),
                use_container_width=True,
                hide_index=True,
                height=255,
                column_config={
                    "ID": st.column_config.TextColumn("ID", width="small"),
                    "Operating h": st.column_config.NumberColumn("Operating h", format="%d"),
                    "Failures": st.column_config.NumberColumn("Failures", format="%d"),
                    "MTBF h": st.column_config.NumberColumn("MTBF (h)", format="%.0f"),
                    "MTTR h": st.column_config.NumberColumn("MTTR (h)", format="%.1f"),
                    "Availability %": st.column_config.ProgressColumn("Availability", min_value=98, max_value=100, format="%.2f%%"),
                },
            )

    section("02", "REPORTS & HISTORICAL INSIGHTS", "Factory-wide history and downloadable reports")
    with st.container(border=True):
        q1, q2 = st.columns([1, 2])
        rng_val = q1.date_input("Date range", value=(MONTHS[0].date(), TODAY), key="rp_range")
        sel_ids = q2.multiselect("Machines", IDS, default=IDS, key="rp_mach", format_func=label)

        if isinstance(rng_val, (tuple, list)) and len(rng_val) == 2 and sel_ids:
            start, end = rng_val
            mask = np.asarray((MONTH_END >= pd.Timestamp(start)) & (MONTHS <= pd.Timestamp(end)))
            if mask.sum() > 0:
                msel = MONTHS[mask]
                planned, unplanned = downtime_frames(sel_ids)
                eff = efficiency(planned, unplanned).loc[mask]
                planned, unplanned = planned.loc[mask], unplanned.loc[mask]
                fail, health = H["fail"].loc[mask, sel_ids], H["health"].loc[mask, sel_ids]

                hist = history_df()
                hist = hist[(hist["Date"] >= start) & (hist["Date"] <= end) & hist["ID"].isin(sel_ids)].copy()
                down_tot = float(planned.values.sum() + unplanned.values.sum())
                done_cnt = int((hist["Status"] == "Completed").sum())
                pend_cnt = int((hist["Status"] == "Pending").sum())

                st.html('<div class="ms-row">'
                        f'<div class="ms"><div class="l">AVG HEALTH</div><div class="v">{health.iloc[-1].mean():.0f}%</div></div>'
                        f'<div class="ms"><div class="l">FAILURES</div><div class="v">{int(fail.values.sum())}</div></div>'
                        f'<div class="ms"><div class="l">TOTAL DOWNTIME</div><div class="v">{down_tot:.0f} h</div></div>'
                        f'<div class="ms"><div class="l">AVG EFFICIENCY</div><div class="v">{eff.mean():.1f}%</div></div>'
                        f'<div class="ms"><div class="l">TASKS COMPLETED</div><div class="v">{done_cnt}</div></div>'
                        f'<div class="ms"><div class="l">TASKS PENDING</div><div class="v">{pend_cnt}</div></div></div>')

                rel_sub = reliability(sel_ids, mask)
                monthly = pd.DataFrame({
                    "Month": msel.strftime("%b %Y"),
                    "Avg Health %": health.mean(axis=1).round(1).values,
                    "Failures": fail.sum(axis=1).values,
                    "Planned Downtime h": planned.sum(axis=1).round(1).values,
                    "Unplanned Downtime h": unplanned.sum(axis=1).round(1).values,
                    "Production Eff. %": eff.round(1).values,
                })
                mh = hist.sort_values("Date", ascending=False).copy()
                mh["Date"] = mh["Date"].map(lambda d: f"{d:%d %b %Y}")
                fa = pd.DataFrame({
                    "ID": rel_sub["ID"], "Machine": rel_sub["Machine"], "Failures": rel_sub["Failures"],
                    "Top Failure Mode": [FAIL_MODE[i] for i in rel_sub["ID"]],
                    "MTBF h": rel_sub["MTBF h"], "MTTR h": rel_sub["MTTR h"], "Availability %": rel_sub["Availability %"],
                })
                TABLES = {
                    "Monthly Factory Performance Report": monthly,
                    "Failure & Anomaly Report": fa,
                    "Maintenance History": mh,
                }

                st.html('<div class="panel-title" style="margin-top:6px;">Reporting centre</div>')
                rc1, rc2, rc3 = st.columns([2, 1, 1], vertical_alignment="bottom")
                rep_name = rc1.selectbox("Report", list(TABLES), key="rp_name", label_visibility="collapsed")
                df_rep = TABLES[rep_name]
                base = rep_name.lower().replace(" & ", "_").replace(" ", "_")
                pdf_bytes, pdf_fname, pdf_mime = make_pdf(
                    f"ANOMATRIX - {rep_name}",
                    f"Period: {start:%d %b %Y} to {end:%d %b %Y} | Machines: {len(sel_ids)} of {len(IDS)}",
                    [f"Failures: {int(fail.values.sum())} | Downtime: {down_tot:.0f} h | Avg production efficiency: {eff.mean():.1f}%"],
                    df_rep,
                    base,
                )
                rc2.download_button(
                    "⬇️ Download Report",
                    pdf_bytes,
                    file_name=pdf_fname,
                    mime=pdf_mime,
                    key="dl_rep_pdf",
                    type="primary",
                    use_container_width=True,
                )
                rc3.download_button(
                    "⬇️ Export CSV Data",
                    df_rep.to_csv(index=False),
                    file_name=f"{base}.csv",
                    mime="text/csv",
                    key="dl_rep_csv",
                    use_container_width=True,
                )
                st.dataframe(df_rep, use_container_width=True, hide_index=True, height=220)
            else:
                st.info("No data in selected date range.")
        else:
            st.info("Select a valid date range and at least one machine.")