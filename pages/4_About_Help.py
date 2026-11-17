import streamlit as st
from components.login import require_login
from components.sidebar import render_sidebar

require_login()
render_sidebar()

# =====================================================
# 1. CSS (EXACT COMMAND CENTER THEME)
# =====================================================

st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&family=JetBrains+Mono:wght@500;700&display=swap');

html, body, .stApp, [class*="css"] { font-family: 'Inter', sans-serif; }

/* Exact same soft ice-blue canvas as other pages */
.stApp {
    background:
        radial-gradient(900px 420px at 92% -5%, rgba(120,190,235,0.22), transparent 60%),
        radial-gradient(700px 400px at 0% 0%, rgba(190,225,250,0.32), transparent 60%),
        #E6F0F8;
    color: #14273A;
}
[data-testid="stHeader"] { background: transparent; height: 1.75rem; }
footer { visibility: hidden; }
.block-container {
    max-width: 1560px;
    padding-top: 1.45rem !important;
    padding-bottom: 1.8rem !important;
}

[data-testid="stMain"] [data-testid="stVerticalBlock"] {
    gap: 0.85rem !important;
}

/* ---------- HEADINGS (EXACT MATCH WITH PAGES 1, 2 & 3) ---------- */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 3px;
    font-size: 11px;
    color: #6F8496;
    margin-top: 8px;
    text-transform: uppercase;
    font-weight: 600;
}
.section-label.top-label {
    margin-top: 0px;
}
.section-title {
    font-family: 'Inter', sans-serif;
    font-size: 24px;
    font-weight: 800;
    color: #14273A;
    margin: 2px 0 8px;
    line-height: 1.15;
    letter-spacing: -0.02em;
}
.section-title.top-title {
    font-family: 'Inter', sans-serif;
    font-size: 32px;
    font-weight: 800;
    color: #14273A;
    margin: 2px 0 6px;
    line-height: 1.15;
    letter-spacing: -0.02em;
}

/* ---------- PURE WHITE ELEVATED CARDS ---------- */
[data-testid="stVerticalBlockBorderWrapper"],
[data-testid="stVerticalBlockBorderWrapper"] > div,
div[data-testid="stContainer"][border="true"],
[data-testid="stLayoutWrapper"] > div[style*="border"],
div[class*="st-emotion-cache"][style*="border: 1px solid"] {
    background-color: #FFFFFF !important;
    background: #FFFFFF !important;
    border-radius: 18px !important;
    border: 1px solid #FFFFFF !important;
    box-shadow: 0 10px 26px rgba(15, 39, 64, 0.07), 0 2px 6px rgba(15, 39, 64, 0.03) !important;
    padding: 1.05rem 1.25rem !important;
}
[data-testid="stVerticalBlockBorderWrapper"] [data-testid="stVerticalBlock"],
[data-testid="stLayoutWrapper"] > div[style*="border"] > [data-testid="stVerticalBlock"],
[data-testid="stLayoutWrapper"] > div[style*="border"] [data-testid="stHorizontalBlock"] {
    background-color: #FFFFFF !important;
}

.card-tag {
    font-family: 'JetBrains Mono', monospace;
    font-size: 10px;
    letter-spacing: 1.8px;
    color: #328BC5;
    font-weight: 700;
    text-transform: uppercase;
    margin-bottom: 4px;
}
.card-heading {
    font-size: 18px;
    font-weight: 800;
    color: #14273A;
    margin-bottom: 8px;
    letter-spacing: -0.01em;
}
.card-text {
    font-size: 14px;
    color: #3D5265;
    line-height: 1.65;
    margin: 0;
}

/* Simple clean list for motive points */
.motive-list {
    margin: 10px 0 0 0;
    padding-left: 18px;
    color: #3D5265;
    font-size: 13.5px;
    line-height: 1.7;
}
.motive-list li {
    margin-bottom: 4px;
}

/* User roles grid */
.role-box {
    background: #F8FBFD;
    border: 1px solid #E4EDF5;
    border-radius: 12px;
    padding: 12px 14px;
    height: 100%;
}
.role-title {
    font-size: 14.5px;
    font-weight: 700;
    color: #14273A;
    margin-bottom: 4px;
}
.role-desc {
    font-size: 13px;
    color: #5B6F7E;
    line-height: 1.5;
    margin: 0;
}

/* Minimal, low-attention Help & Support footer strip */
.help-minimal {
    margin-top: 14px;
    padding: 10px 14px;
    border-radius: 10px;
    background: rgba(255, 255, 255, 0.45);
    border: 1px solid #D8E4EE;
    display: flex;
    justify-content: space-between;
    align-items: center;
    flex-wrap: wrap;
    gap: 8px;
    font-size: 12.5px;
    color: #7A8D9E;
}
.help-minimal span.hm-label {
    font-weight: 600;
    color: #677B8D;
}
.help-minimal span.hm-status {
    font-family: 'JetBrains Mono', monospace;
    font-size: 11px;
    color: #8799A8;
}
</style>
""",
    unsafe_allow_html=True,
)

# =====================================================
# 2. TOP HEADER (PLATFORM OVERVIEW)
# =====================================================

st.html(
    """
    <div class="section-label top-label">ABOUT &amp; HELP</div>
    <div class="section-title top-title">Platform Overview</div>
    """
)

# =====================================================
# 3. ABOUT SECTION (OUR MOTIVE & WHO CAN USE IT)
# =====================================================

col_motive, col_users = st.columns([1.05, 1.35], gap="medium")

with col_motive:
    with st.container(border=True):
        st.html(
            """
            <div class="card-tag">OUR MOTIVE</div>
            <div class="card-heading">Why We Built This Platform</div>
            <p class="card-text">
                Industrial floors often suffer from unexpected equipment breakdowns, delayed fault detection, 
                and scattered sensor records. The motive behind this platform is to bring all critical floor 
                telemetry into one unified, easy-to-read command center.
            </p>
            <ul class="motive-list">
                <li>Detect early warning signs in temperature, vibration, and pressure before failure occurs.</li>
                <li>Provide a clear floor-wise overview of machine health and operational risk.</li>
                <li>Help teams transition from reactive repairs to planned, timely maintenance.</li>
            </ul>
            """
        )

with col_users:
    with st.container(border=True):
        st.html(
            """
            <div class="card-tag">TARGET USERS</div>
            <div class="card-heading">Who Can Use This Platform</div>
            """
        )
        r1c1, r1c2 = st.columns(2, gap="small")
        with r1c1:
            st.html(
                """
                <div class="role-box">
                    <div class="role-title">Plant &amp; Operations Managers</div>
                    <p class="role-desc">
                        Monitor overall floor health, track uptime metrics, and prioritize high-risk assets across shifts.
                    </p>
                </div>
                """
            )
        with r1c2:
            st.html(
                """
                <div class="role-box">
                    <div class="role-title">Maintenance Engineers</div>
                    <p class="role-desc">
                        Inspect sensor anomalies, review AI fault diagnostics, and schedule preventive work orders.
                    </p>
                </div>
                """
            )

        st.html('<div style="height:6px;"></div>')
        r2c1, r2c2 = st.columns(2, gap="small")
        with r2c1:
            st.html(
                """
                <div class="role-box">
                    <div class="role-title">Floor Supervisors &amp; Operators</div>
                    <p class="role-desc">
                        Check live machine status on the interactive floor map and respond quickly to active alerts.
                    </p>
                </div>
                """
            )
        with r2c2:
            st.html(
                """
                <div class="role-box">
                    <div class="role-title">Reliability &amp; Quality Analysts</div>
                    <p class="role-desc">
                        Compare machine performance trends, export sensor logs, and evaluate long-term asset wear.
                    </p>
                </div>
                """
            )

# =====================================================
# 4. MINIMAL HELP & SUPPORT FOOTER (WORK UNDER PROGRESS)
# =====================================================

st.html(
    """
    <div class="help-minimal">
        <span><span class="hm-label">Help &amp; Support</span> — Documentation and support guides are currently being set up.</span>
        <span class="hm-status">Work under progress</span>
    </div>
    """
)