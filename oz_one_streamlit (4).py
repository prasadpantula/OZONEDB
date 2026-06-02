"""
OZ ONE — Jubail & Dammam O₃ Monitoring Dashboard
=================================================
Streamlit + Plotly conversion of the React/TypeScript Power BI-style dashboard.

Run:
    streamlit run oz_one_streamlit.py

Requirements:
    pip install streamlit plotly pandas

Version: 1.0  |  May 2026
"""

import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
import numpy as np

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="OZ ONE | O₃ Monitoring Dashboard",
    page_icon="🌫️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ══════════════════════════════════════════════════════════════════════════════
#  DARK THEME + CUSTOM CSS
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("""
<style>
/* ── Global dark background ── */
html, body, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
    background-color: #0b0e1a !important;
    color: #e2e8f0 !important;
}
[data-testid="stSidebar"] {
    background-color: #0d1020 !important;
    border-right: 1px solid rgba(96,130,255,0.18) !important;
}
[data-testid="stSidebar"] * { color: #c9d1e8 !important; }

/* ── Hide Streamlit header/footer ── */
#MainMenu { visibility: hidden; }
footer    { visibility: hidden; }
header    { visibility: hidden; }

/* ── Metric cards ── */
[data-testid="stMetric"] {
    background: linear-gradient(135deg,#0f1428,#131a30);
    border: 1px solid rgba(96,130,255,0.2);
    border-radius: 12px;
    padding: 14px 16px !important;
}
[data-testid="stMetricLabel"] {
    font-size: 10px !important;
    font-family: 'JetBrains Mono', monospace !important;
    text-transform: uppercase;
    letter-spacing: .1em;
    color: #6b7aaa !important;
}
[data-testid="stMetricValue"] {
    font-size: 22px !important;
    font-weight: 700 !important;
    color: #e2e8f0 !important;
}
[data-testid="stMetricDelta"] { font-size: 11px !important; }

/* ── Tabs ── */
[data-testid="stTabs"] [role="tablist"] {
    background: #0d1020;
    border-radius: 10px;
    border: 1px solid rgba(96,130,255,0.18);
    padding: 4px;
    gap: 4px;
}
[data-testid="stTabs"] [role="tab"] {
    color: #6b7aaa !important;
    font-size: 11px;
    font-family: monospace;
    letter-spacing: .06em;
    border-radius: 7px;
    padding: 6px 14px;
}
[data-testid="stTabs"] [role="tab"][aria-selected="true"] {
    background: rgba(96,130,255,0.2) !important;
    color: #6082ff !important;
    font-weight: 700;
}

/* ── Selectbox / radio ── */
[data-testid="stSelectbox"] > div, [data-testid="stRadio"] > div {
    background: #0f1428 !important;
    border-radius: 8px !important;
}

/* ── Dataframe / tables ── */
[data-testid="stDataFrame"] { border-radius: 10px; overflow: hidden; }

/* ── Section label ── */
.section-label {
    font-family: 'JetBrains Mono', monospace;
    font-size: 9px;
    font-weight: 700;
    letter-spacing: .18em;
    text-transform: uppercase;
    color: #6082ff;
    border-left: 3px solid #6082ff;
    padding-left: 8px;
    margin-bottom: 8px;
}

/* ── Alert cards ── */
.alert-card {
    border-radius: 10px;
    padding: 14px 18px;
    margin-bottom: 10px;
    border-left: 4px solid;
}
.alert-critical { background:rgba(255,79,79,.08); border-color:#ff4f4f; }
.alert-danger    { background:rgba(255,140,66,.08); border-color:#ff8c42; }
.alert-warning   { background:rgba(245,166,35,.08); border-color:#f5a623; }
.alert-info      { background:rgba(96,130,255,.08); border-color:#6082ff; }

/* ── Status badge ── */
.badge {
    display: inline-block;
    font-size: 10px;
    font-weight: 700;
    padding: 2px 8px;
    border-radius: 4px;
    letter-spacing: .06em;
}
.badge-very-high { background:rgba(255,79,79,.15);   color:#ff4f4f; }
.badge-high      { background:rgba(255,140,66,.15);  color:#ff8c42; }
.badge-moderate  { background:rgba(245,166,35,.15);  color:#f5a623; }
.badge-good      { background:rgba(58,240,181,.15);  color:#3af0b5; }

/* ── Breadcrumb ── */
.breadcrumb {
    font-family: monospace;
    font-size: 10px;
    color: #4a5580;
    margin-bottom: 4px;
}
.breadcrumb span { color: #6082ff; }

/* ── Divider ── */
hr { border-color: rgba(96,130,255,0.12) !important; }

/* ── Info box ── */
.info-box {
    background: rgba(96,130,255,0.07);
    border: 1px solid rgba(96,130,255,0.2);
    border-radius: 10px;
    padding: 14px 18px;
    font-size: 13px;
    line-height: 1.7;
    margin-bottom: 16px;
}

/* ── Top header bar ── */
.top-header {
    background: linear-gradient(90deg,#0d1123,#121830);
    border: 1px solid rgba(96,130,255,0.18);
    border-radius: 12px;
    padding: 14px 24px;
    margin-bottom: 18px;
    display: flex;
    align-items: center;
    justify-content: space-between;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  ALL DATA  (mirrored from src/data/index.ts)
# ══════════════════════════════════════════════════════════════════════════════

# ── 24-hour O₃ trend ─────────────────────────────────────────────────────────
HOURS_24 = [f"{i}:00" for i in range(24)]
O3_TODAY = [42,38,35,34,35,48,72,98,122,148,163,174,183,189,185,178,168,155,138,118,95,78,62,52]

df_trend = pd.DataFrame({
    "time":     HOURS_24,
    "jubail":   O3_TODAY,
    "dammam":   [round(v * 0.9) for v in O3_TODAY],
    "standard": [120] * 24,
})

# ── Station data ──────────────────────────────────────────────────────────────
JUBAIL_STATIONS = [
    {"station": "ST-J01", "name": "Industrial Zone",    "current": 183, "region": "Jubail"},
    {"station": "ST-J02", "name": "Petrochemical Hub",  "current": 171, "region": "Jubail"},
    {"station": "ST-J03", "name": "Port Area",          "current": 196, "region": "Jubail"},
    {"station": "ST-J04", "name": "Residential North",  "current": 168, "region": "Jubail"},
    {"station": "ST-J05", "name": "Residential South",  "current": 178, "region": "Jubail"},
]
DAMMAM_STATIONS = [
    {"station": "ST-D01", "name": "Downtown",       "current": 165, "region": "Dammam"},
    {"station": "ST-D02", "name": "Corniche",       "current": 157, "region": "Dammam"},
    {"station": "ST-D03", "name": "Al-Khobar N",    "current": 172, "region": "Dammam"},
    {"station": "ST-D04", "name": "Industrial W",   "current": 160, "region": "Dammam"},
]
ALL_STATIONS = JUBAIL_STATIONS + DAMMAM_STATIONS
for s in ALL_STATIONS:
    s["peak"]   = s["current"] + 8
    s["status"] = "Very High" if s["current"] > 180 else ("High" if s["current"] > 140 else "Moderate")

df_stations = pd.DataFrame(ALL_STATIONS)

# ── NOₓ sources ───────────────────────────────────────────────────────────────
NOX_SOURCES = {
    "Power Plants": 35, "Petrochemical": 28,
    "Refineries": 22,   "Transport": 15,
}
POWER_PLANT_DRILL = {
    "SADARA PP": 14, "SABIC PP": 11, "MARAFIQ": 7, "SWCC Plant": 3,
}

# ── VOC breakdown ─────────────────────────────────────────────────────────────
VOC_BREAKDOWN = {
    "Aromatics": 38, "Alkanes": 27, "Olefins": 21,
    "Oxygenates": 11, "Other": 3,
}

# ── Weekly O₃ ─────────────────────────────────────────────────────────────────
df_weekly = pd.DataFrame([
    {"day": "Sun", "jubail": 152, "dammam": 137},
    {"day": "Mon", "jubail": 148, "dammam": 133},
    {"day": "Tue", "jubail": 155, "dammam": 140},
    {"day": "Wed", "jubail": 159, "dammam": 143},
    {"day": "Thu", "jubail": 162, "dammam": 146},
    {"day": "Fri", "jubail": 178, "dammam": 160},
    {"day": "Sat", "jubail": 183, "dammam": 165},
])

# ── Seasonal chemistry ────────────────────────────────────────────────────────
MONTHS = ["Jan","Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
SEASONAL_O3   = [68,72,85,108,138,162,189,192,175,142,98,74]
SEASONAL_NOX  = [45,42,50,65, 80, 95,110,112,100, 82,58,48]
SEASONAL_TEMP = [18,20,24,30, 36, 40, 44, 44, 40, 34,26,20]

df_seasonal = pd.DataFrame({
    "month": MONTHS,
    "o3":    SEASONAL_O3,
    "nox":   SEASONAL_NOX,
    "temp":  SEASONAL_TEMP,
    "standard": [120] * 12,
})

# ── Long-term analytics ────────────────────────────────────────────────────────
df_longterm = pd.DataFrame({
    "year":        ["2015","2016","2017","2018","2019","2020","2021","2022","2023","2024","2025","2026"],
    "o3":          [88,92,101,118,128,135,142,155,163,171,178,183],
    "exceedances": [22,28,45, 72, 91,105,118,142,158,172,185,189],
})

# ── Mitigation scenarios ──────────────────────────────────────────────────────
df_mitigation = pd.DataFrame([
    {"scenario": "Baseline",  "value": 183, "reduction": 0.0,  "color": "#ff4f4f"},
    {"scenario": "VOC -30%",  "value": 143, "reduction": 21.9, "color": "#6082ff"},
    {"scenario": "NOx -30%",  "value": 168, "reduction": 8.2,  "color": "#f5a623"},
    {"scenario": "Combined",  "value": 127, "reduction": 30.6, "color": "#3af0b5"},
])

# ── Active alerts ──────────────────────────────────────────────────────────────
ALERTS = [
    {"id":"ALT-001","severity":"Critical","location":"Jubail – ST-J03 Port Area",
     "value":196,"threshold":120,"timestamp":"2026-05-02 13:14",
     "message":"O₃ concentration 63% above WHO standard","ack":False},
    {"id":"ALT-002","severity":"Danger","location":"Jubail – ST-J01 Industrial Zone",
     "value":183,"threshold":120,"timestamp":"2026-05-02 13:00",
     "message":"O₃ sustained above 180 µg/m³ for >2 hours","ack":False},
    {"id":"ALT-003","severity":"Warning","location":"Dammam – ST-D03 Al-Khobar N",
     "value":172,"threshold":120,"timestamp":"2026-05-02 12:30",
     "message":"O₃ trending upward, peak risk 14:00–16:00","ack":True},
    {"id":"ALT-004","severity":"Warning","location":"Dammam – ST-D01 Downtown",
     "value":165,"threshold":120,"timestamp":"2026-05-02 11:45",
     "message":"Elevated NOₓ precursor levels detected","ack":True},
    {"id":"ALT-005","severity":"Info","location":"Regional – Wind forecast",
     "value":0,"threshold":0,"timestamp":"2026-05-02 10:00",
     "message":"NW wind shift expected 18:00 – may reduce dispersion","ack":True},
]

# ── KPI definitions ────────────────────────────────────────────────────────────
KPI_CARDS = [
    {"label":"Current O₃ (Jubail)", "value":183, "unit":"µg/m³", "delta":"+4.6%", "status":"very_high"},
    {"label":"Current O₃ (Dammam)", "value":165, "unit":"µg/m³", "delta":"+2.1%", "status":"high"},
    {"label":"Exceedances Today",   "value":8,   "unit":"stations","delta":"+33%","status":"very_high"},
    {"label":"Temperature",         "value":41,  "unit":"°C",     "delta":"+1.2°","status":"moderate"},
    {"label":"Wind Speed",          "value":12,  "unit":"km/h NW","delta":"-8%",  "status":"good"},
    {"label":"Humidity",            "value":28,  "unit":"%",      "delta":"-3%",  "status":"good"},
]

HEALTH_BREAKPOINTS = [
    ("0–60",    "Good",      "No health impact expected",                          "#3af0b5"),
    ("60–100",  "Moderate",  "Unusually sensitive individuals may be affected",    "#a8d8a8"),
    ("100–140", "High",      "Sensitive groups: reduce outdoor exertion",          "#f5a623"),
    ("140–180", "Very High", "Everyone: limit outdoor activity, masks recommended","#ff8c42"),
    ("180+",    "Hazardous", "All outdoor activities contraindicated",             "#ff4f4f"),
]

# ══════════════════════════════════════════════════════════════════════════════
#  HELPERS
# ══════════════════════════════════════════════════════════════════════════════
PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="monospace", size=11, color="#8a9acc"),
    margin=dict(l=10, r=10, t=30, b=10),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(size=10)),
)

_GRID = "rgba(96,130,255,0.07)"

def plo(fig, **kw):
    """Apply dark base layout + chart-specific kwargs without key conflicts.
    kw values take precedence over PLOTLY_LAYOUT defaults (dict merge, not
    double-unpack), so margin/xaxis/yaxis/etc. can all be safely overridden.
    update_xaxes / update_yaxes restore grid styling on every axis."""
    fig.update_layout(**{**PLOTLY_LAYOUT, **kw})
    fig.update_xaxes(gridcolor=_GRID, zeroline=False)
    fig.update_yaxes(gridcolor=_GRID, zeroline=False)
    return fig

STATUS_COLORS = {
    "Very High": "#ff4f4f",
    "High":      "#ff8c42",
    "Moderate":  "#f5a623",
    "Good":      "#3af0b5",
}

def status_color(val: int) -> str:
    if val > 180: return "#ff4f4f"
    if val > 140: return "#ff8c42"
    if val > 100: return "#f5a623"
    return "#3af0b5"

def status_label(val: int) -> str:
    if val > 180: return "Very High"
    if val > 140: return "High"
    if val > 100: return "Moderate"
    return "Good"

def aqi_gauge(value: int, label: str) -> go.Figure:
    """Render a half-arc AQI gauge with Plotly."""
    col = status_color(value)
    max_val = 220
    angle   = 180 * (value / max_val)  # 0–180 degrees
    fig = go.Figure()
    # Background arc
    theta_bg = np.linspace(0, np.pi, 120)
    r = 1
    fig.add_trace(go.Scatter(
        x=np.cos(theta_bg) * r, y=np.sin(theta_bg) * r,
        mode="lines", line=dict(color="rgba(96,130,255,0.12)", width=14),
        hoverinfo="none", showlegend=False,
    ))
    # Filled arc
    theta_fg = np.linspace(0, np.pi * (value / max_val), 120)
    fig.add_trace(go.Scatter(
        x=np.cos(theta_fg) * r, y=np.sin(theta_fg) * r,
        mode="lines", line=dict(color=col, width=14),
        hoverinfo="none", showlegend=False,
    ))
    # Value annotation
    fig.add_annotation(x=0, y=0.3, text=f"<b>{value}</b>",
        font=dict(size=24, color=col, family="monospace"),
        showarrow=False)
    fig.add_annotation(x=0, y=0.05, text=f"µg/m³",
        font=dict(size=10, color="#6b7aaa", family="monospace"),
        showarrow=False)
    fig.add_annotation(x=0, y=-0.2, text=f"<b>{label}</b>",
        font=dict(size=11, color="#c9d1e8", family="monospace"),
        showarrow=False)
    fig.add_annotation(x=0, y=-0.38, text=f"<b>{status_label(value)}</b>",
        font=dict(size=10, color=col, family="monospace"),
        showarrow=False)
    plo(fig,
        margin=dict(l=0, r=0, t=0, b=10),
        height=160, width=200,
        xaxis=dict(visible=False, range=[-1.4, 1.4]),
        yaxis=dict(visible=False, range=[-0.5, 1.2]),
        showlegend=False,
    )
    return fig

def section_label(text: str):
    st.markdown(f'<div class="section-label">{text}</div>', unsafe_allow_html=True)

def breadcrumb(parts: list, sep=" › "):
    html = sep.join(
        f'<span style="color:#6082ff;">{p}</span>' if i == len(parts)-1
        else f'<span style="color:#4a5580;">{p}</span>'
        for i, p in enumerate(parts)
    )
    st.markdown(f'<div class="breadcrumb">📍 {html}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  SESSION STATE INIT
# ══════════════════════════════════════════════════════════════════════════════
defaults = {
    "drill_level":        "overview",    # overview | stations | hourly
    "drill_region":       None,          # "Jubail" | "Dammam"
    "drill_station":      None,          # station dict
    "nox_drill":          False,         # power plants sub-drill
    "selected_voc":       None,
    "selected_week_day":  None,
    "selected_month":     None,
    "selected_year":      None,
    "ack_state":          {a["id"]: a["ack"] for a in ALERTS},
    "alert_severity_filter": "All",
    "selected_mitigation": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v

# ══════════════════════════════════════════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════════════════════════════════════════
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;padding:12px 0 8px;'>
      <div style='font-size:22px;'>🌫️</div>
      <div style='font-family:monospace;font-size:13px;font-weight:700;color:#6082ff;'>OZ ONE</div>
      <div style='font-size:10px;color:#4a5580;margin-top:2px;'>Jubail & Dammam O₃ Monitoring</div>
    </div>
    <hr style='margin:8px 0;'/>
    """, unsafe_allow_html=True)

    region_sel = st.selectbox("Region", ["All Regions", "Jubail Only", "Dammam Only"],
                              key="sidebar_region")
    time_sel   = st.selectbox("Time Range", ["24 Hours", "6 Hours", "12 Hours"],
                              key="sidebar_time")

    st.markdown("---")
    st.markdown('<div style="font-size:10px;color:#4a5580;font-family:monospace;'
                'letter-spacing:.1em;text-transform:uppercase;margin-bottom:6px;">'
                'Navigation</div>', unsafe_allow_html=True)

    page = st.radio("", ["Dashboard","Precursors","Chemistry","Analytics","Alerts"],
                    label_visibility="collapsed", key="nav_page")

    st.markdown("---")
    st.markdown("""
    <div style='font-size:10px;color:#4a5580;line-height:1.8;font-family:monospace;'>
    WHO Standard: 120 µg/m³<br>
    Last updated: 2026-05-02 13:14<br>
    <span style='color:#ff4f4f;'>● LIVE</span>
    </div>
    """, unsafe_allow_html=True)

# Filter helpers based on sidebar region
region_map = {"All Regions": "all", "Jubail Only": "jubail", "Dammam Only": "dammam"}
region_key = region_map[region_sel]

# ══════════════════════════════════════════════════════════════════════════════
#  TOP HEADER BAR
# ══════════════════════════════════════════════════════════════════════════════
st.markdown(f"""
<div class='top-header'>
  <div>
    <span style='font-family:monospace;font-size:16px;font-weight:700;color:#e2e8f0;'>OZ ONE</span>
    <span style='font-size:11px;color:#4a5580;margin-left:10px;font-family:monospace;'>
      Jubail & Dammam O₃ Unified Monitoring System
    </span>
  </div>
  <div style='display:flex;gap:18px;align-items:center;'>
    <span style='font-size:10px;color:#6b7aaa;font-family:monospace;'>Region: {region_sel}</span>
    <span style='font-size:10px;color:#6b7aaa;font-family:monospace;'>{time_sel}</span>
    <span style='background:rgba(255,79,79,.15);color:#ff4f4f;font-size:10px;
                 font-family:monospace;font-weight:700;padding:3px 10px;border-radius:20px;
                 border:1px solid rgba(255,79,79,.3);'>● LIVE</span>
    <span style='background:rgba(255,79,79,.1);color:#ff4f4f;font-size:11px;
                 font-family:monospace;padding:3px 10px;border-radius:6px;'>
      Jubail: 183 µg/m³ | VERY HIGH
    </span>
  </div>
</div>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 1 — DASHBOARD
# ══════════════════════════════════════════════════════════════════════════════
if page == "Dashboard":

    # ── KPI Row ────────────────────────────────────────────────────────────────
    section_label("KEY PERFORMANCE INDICATORS")
    kpi_cols = st.columns(6)
    for col, k in zip(kpi_cols, KPI_CARDS):
        delta_color = "inverse" if k["status"] in ("very_high","high") else "normal"
        col.metric(
            label=f"{k['label']} ({k['unit']})",
            value=k["value"],
            delta=k["delta"],
            delta_color=delta_color,
        )

    st.markdown("---")

    # ── Drill-down state display ────────────────────────────────────────────
    lvl = st.session_state.drill_level
    if lvl == "overview":
        breadcrumb(["Overview"])
    elif lvl == "stations":
        breadcrumb(["Overview", st.session_state.drill_region])
    else:
        breadcrumb(["Overview", st.session_state.drill_region,
                    st.session_state.drill_station["name"]])

    # ── OVERVIEW level ─────────────────────────────────────────────────────
    if lvl == "overview":
        chart_col, gauge_col = st.columns([3, 1])

        with chart_col:
            section_label("O₃ 24-HOUR TREND  ·  Click a region gauge → drill into stations")
            hours = HOURS_24
            if time_sel == "6 Hours":  hours = HOURS_24[18:]
            elif time_sel == "12 Hours": hours = HOURS_24[12:]
            df_t = df_trend[df_trend["time"].isin(hours)]

            fig = go.Figure()
            fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)",
                          line_width=1.5,
                          annotation_text="WHO Std 120 µg/m³",
                          annotation_font_color="#3af0b5",
                          annotation_font_size=9)
            if region_key in ("all","jubail"):
                fig.add_trace(go.Scatter(
                    x=df_t["time"], y=df_t["jubail"], name="Jubail",
                    line=dict(color="#ff4f4f", width=2),
                    mode="lines", hovertemplate="%{y} µg/m³<extra>Jubail</extra>",
                ))
            if region_key in ("all","dammam"):
                fig.add_trace(go.Scatter(
                    x=df_t["time"], y=df_t["dammam"], name="Dammam",
                    line=dict(color="#f5a623", width=1.5, dash="dot"),
                    mode="lines", hovertemplate="%{y} µg/m³<extra>Dammam</extra>",
                ))
            plo(fig, height=230,
                              yaxis=dict(range=[0,220], gridcolor="rgba(96,130,255,0.07)"),
                              title=dict(text="24-Hour O₃ Trend",
                                         font=dict(size=12,color="#8a9acc"),x=0))
            st.plotly_chart(fig, use_container_width=True, key="dash_trend")

        with gauge_col:
            section_label("LIVE AQI GAUGES")
            st.caption("Click a button to drill into stations →")
            if st.button("🔍  Jubail  183 µg/m³  VERY HIGH",
                         key="drill_jubail",
                         help="Drill into Jubail station breakdown"):
                st.session_state.drill_level  = "stations"
                st.session_state.drill_region = "Jubail"
                st.rerun()
            st.plotly_chart(aqi_gauge(183, "Jubail"), use_container_width=False, key="g_j")

            st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)
            if st.button("🔍  Dammam  165 µg/m³  HIGH",
                         key="drill_dammam",
                         help="Drill into Dammam station breakdown"):
                st.session_state.drill_level  = "stations"
                st.session_state.drill_region = "Dammam"
                st.rerun()
            st.plotly_chart(aqi_gauge(165, "Dammam"), use_container_width=False, key="g_d")

        # ── Station status table ──────────────────────────────────────────
        st.markdown("---")
        section_label("STATION STATUS TABLE  ·  Click a row button to drill into hourly data")

        df_disp = df_stations.copy()
        if region_key == "jubail":   df_disp = df_disp[df_disp["region"]=="Jubail"]
        elif region_key == "dammam": df_disp = df_disp[df_disp["region"]=="Dammam"]

        hdr = st.columns([1,2,1,1,1,1.2,1])
        for h,txt in zip(hdr,["Station","Location","Region","O₃ µg/m³","Peak","Status","Drill"]):
            h.markdown(f"<div style='font-size:9px;color:#4a5580;text-transform:uppercase;"
                       f"letter-spacing:.1em;font-family:monospace;'>{txt}</div>",
                       unsafe_allow_html=True)
        st.markdown("<hr style='margin:4px 0 8px;'>", unsafe_allow_html=True)

        for _, row in df_disp.iterrows():
            col = status_color(row["current"])
            c1,c2,c3,c4,c5,c6,c7 = st.columns([1,2,1,1,1,1.2,1])
            c1.markdown(f"<span style='color:#6082ff;font-family:monospace;font-size:12px;'>{row['station']}</span>",
                        unsafe_allow_html=True)
            c2.markdown(f"<span style='font-size:12px;'>{row['name']}</span>", unsafe_allow_html=True)
            c3.markdown(f"<span style='font-size:12px;color:#6b7aaa;'>{row['region']}</span>",
                        unsafe_allow_html=True)
            c4.markdown(f"<span style='color:{col};font-weight:700;font-family:monospace;font-size:12px;'>{row['current']}</span>",
                        unsafe_allow_html=True)
            c5.markdown(f"<span style='font-size:12px;color:#6b7aaa;'>{row['peak']}</span>",
                        unsafe_allow_html=True)
            c6.markdown(f"<span class='badge badge-{row['status'].lower().replace(' ','-')}'>"
                        f"{row['status'].upper()}</span>", unsafe_allow_html=True)
            if c7.button("⚡ Drill", key=f"drill_st_{row['station']}"):
                st.session_state.drill_level   = "hourly"
                st.session_state.drill_region  = row["region"]
                st.session_state.drill_station = row.to_dict()
                st.rerun()

    # ── STATIONS level ─────────────────────────────────────────────────────
    elif lvl == "stations":
        region_name = st.session_state.drill_region
        stations    = JUBAIL_STATIONS if region_name == "Jubail" else DAMMAM_STATIONS
        df_reg      = pd.DataFrame(stations)
        df_reg["peak"]   = df_reg["current"] + 8
        df_reg["status"] = df_reg["current"].apply(status_label)
        df_reg["color"]  = df_reg["current"].apply(status_color)

        col1, col2 = st.columns([3,1])
        with col1:
            section_label(f"{region_name.upper()} — STATION BREAKDOWN  ·  Click a bar to drill into hourly")
            fig = go.Figure()
            fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)", line_width=1.5)
            fig.add_trace(go.Bar(
                x=df_reg["name"], y=df_reg["current"],
                marker_color=df_reg["color"].tolist(),
                marker_line_width=0,
                customdata=df_reg["station"],
                hovertemplate="<b>%{x}</b><br>O₃: %{y} µg/m³<extra></extra>",
            ))
            plo(fig, height=260,
                              yaxis=dict(range=[80,215], gridcolor="rgba(96,130,255,0.07)"),
                              title=dict(text=f"{region_name} Stations — Current O₃",
                                         font=dict(size=12,color="#8a9acc"),x=0))
            st.plotly_chart(fig, use_container_width=True, key="stations_bar")

        with col2:
            st.caption("Select a station to drill hourly:")
            for s in stations:
                col = status_color(s["current"])
                if st.button(
                    f"{s['station']}  {s['name']}  {s['current']} µg/m³",
                    key=f"drill_hourly_{s['station']}",
                ):
                    st.session_state.drill_level   = "hourly"
                    st.session_state.drill_station = {**s, "peak": s["current"]+8, "status": status_label(s["current"])}
                    st.rerun()

        if st.button("← Back to Overview", key="back_overview"):
            st.session_state.drill_level  = "overview"
            st.session_state.drill_region = None
            st.rerun()

    # ── HOURLY level ────────────────────────────────────────────────────────
    elif lvl == "hourly" and st.session_state.drill_station:
        stn = st.session_state.drill_station
        base = stn["current"]
        hourly_vals = [round(v * (base / 183)) for v in O3_TODAY]
        df_hourly = pd.DataFrame({"time": HOURS_24, "o3": hourly_vals})

        section_label(f"{stn['station']} — {stn['name'].upper()} HOURLY O₃ PROFILE")

        fig = go.Figure()
        fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)",
                      line_width=1.5, annotation_text="WHO Std",
                      annotation_font_color="#3af0b5", annotation_font_size=9)
        fig.add_trace(go.Scatter(
            x=df_hourly["time"], y=df_hourly["o3"], name="O₃",
            line=dict(color="#6082ff", width=2),
            fill="tozeroy", fillcolor="rgba(96,130,255,0.06)",
            mode="lines+markers", marker=dict(size=4, color="#6082ff"),
            hovertemplate="%{x}: %{y} µg/m³<extra></extra>",
        ))
        plo(fig, height=260,
                          yaxis=dict(range=[0,225], gridcolor="rgba(96,130,255,0.07)"),
                          title=dict(text=f"Station {stn['station']} Hourly — Peak: {base+8} µg/m³",
                                     font=dict(size=12,color="#8a9acc"),x=0))
        st.plotly_chart(fig, use_container_width=True, key="hourly_line")

        c1,c2,c3 = st.columns(3)
        c1.metric("Current O₃", f"{base} µg/m³")
        c2.metric("Daily Peak", f"{base+8} µg/m³")
        c3.metric("Status", status_label(base))

        if st.button("← Back to Stations", key="back_stations"):
            st.session_state.drill_level   = "stations"
            st.session_state.drill_station = None
            st.rerun()

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 2 — PRECURSORS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Precursors":
    section_label("O₃ PRECURSOR ANALYSIS — NOₓ SOURCES & VOC BREAKDOWN")

    top_l, top_r = st.columns([1, 1])

    # ── NOₓ donut with Power Plants drill-down ─────────────────────────────
    with top_l:
        nox_drill = st.session_state.nox_drill
        if not nox_drill:
            breadcrumb(["NOₓ Sources", "Overview"])
            section_label("NOₓ EMISSION SOURCES  ·  Click 'Power Plants' to drill down")
            labels = list(NOX_SOURCES.keys())
            values = list(NOX_SOURCES.values())
            colors = ["#6082ff","#f5a623","#ff4f4f","#3af0b5"]
            fig = go.Figure(go.Pie(
                labels=labels, values=values,
                hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0b0e1a", width=2)),
                textinfo="label+percent",
                textfont=dict(size=11, family="monospace", color="#e2e8f0"),
                hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
            ))
            plo(fig, height=280,
                              title=dict(text="NOₓ by Source  (WHO annual threshold: 40 µg/m³)",
                                         font=dict(size=11,color="#8a9acc"),x=0))
            st.plotly_chart(fig, use_container_width=True, key="nox_donut")
            if st.button("⚡ Drill into Power Plants (35%)", key="nox_drill_btn"):
                st.session_state.nox_drill = True
                st.rerun()
        else:
            breadcrumb(["NOₓ Sources", "Power Plants"])
            section_label("POWER PLANTS NOₓ BREAKDOWN  ·  SADARA · SABIC · MARAFIQ · SWCC")
            labels = list(POWER_PLANT_DRILL.keys())
            values = list(POWER_PLANT_DRILL.values())
            colors = ["#6082ff","#8ba4ff","#b0bfff","#d4dcff"]
            fig = go.Figure(go.Pie(
                labels=labels, values=values, hole=0.55,
                marker=dict(colors=colors, line=dict(color="#0b0e1a", width=2)),
                textinfo="label+percent",
                textfont=dict(size=11, family="monospace", color="#e2e8f0"),
                hovertemplate="<b>%{label}</b><br>%{value}%<extra></extra>",
            ))
            plo(fig, height=280,
                              title=dict(text="Power Plants Sub-breakdown",
                                         font=dict(size=11,color="#8a9acc"),x=0))
            st.plotly_chart(fig, use_container_width=True, key="nox_pp_donut")
            if st.button("← Back to NOₓ Overview", key="nox_back"):
                st.session_state.nox_drill = False
                st.rerun()

    # ── VOC horizontal bar with cross-filter ──────────────────────────────
    with top_r:
        section_label("VOC BREAKDOWN  ·  Click a bar to cross-filter")
        sel_voc = st.session_state.selected_voc
        voc_labels = list(VOC_BREAKDOWN.keys())
        voc_values = list(VOC_BREAKDOWN.values())
        voc_colors = ["#6082ff","#3af0b5","#f5a623","#9b59b6","#4a5580"]
        bar_colors = [
            c if (sel_voc is None or voc_labels[i] == sel_voc) else "rgba(96,130,255,0.2)"
            for i, c in enumerate(voc_colors)
        ]
        fig = go.Figure(go.Bar(
            x=voc_values, y=voc_labels, orientation="h",
            marker=dict(color=bar_colors, line_width=0),
            hovertemplate="<b>%{y}</b>: %{x}%<extra></extra>",
            customdata=voc_labels,
        ))
        plo(fig, height=280,
                          xaxis=dict(range=[0,50], gridcolor="rgba(96,130,255,0.07)"),
                          title=dict(text="VOC Species Breakdown (%)",
                                     font=dict(size=11,color="#8a9acc"),x=0))
        st.plotly_chart(fig, use_container_width=True, key="voc_bar")

        voc_sel_box = st.selectbox(
            "Cross-filter by VOC type:",
            ["All"] + voc_labels, key="voc_select",
            index=0 if sel_voc is None else voc_labels.index(sel_voc)+1,
        )
        st.session_state.selected_voc = None if voc_sel_box == "All" else voc_sel_box
        if sel_voc:
            idx = voc_labels.index(sel_voc)
            st.info(f"**{sel_voc}**: {voc_values[idx]}% of total VOC emissions. "
                    f"Aromatics are strong O₃ precursors; reducing aromatic emissions "
                    f"by 30% is estimated to cut peak O₃ by ~12 µg/m³.")

    st.markdown("---")

    # ── Weekly grouped bar ────────────────────────────────────────────────
    section_label("WEEKLY O₃ PATTERN  ·  Click a day to isolate")
    sel_day = st.session_state.selected_week_day
    w_cols  = ["#ff4f4f","#f5a623"]
    days    = df_weekly["day"].tolist()

    def week_alpha(day, sel, default_color):
        if sel is None or day == sel: return default_color
        r,g,b = int(default_color[1:3],16),int(default_color[3:5],16),int(default_color[5:7],16)
        return f"rgba({r},{g},{b},0.2)"

    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=days, y=df_weekly["jubail"], name="Jubail",
        marker_color=[week_alpha(d, sel_day, "#ff4f4f") for d in days],
        marker_line_width=0,
        hovertemplate="Jubail %{x}: %{y} µg/m³<extra></extra>",
    ))
    fig.add_trace(go.Bar(
        x=days, y=df_weekly["dammam"], name="Dammam",
        marker_color=[week_alpha(d, sel_day, "#f5a623") for d in days],
        marker_line_width=0,
        hovertemplate="Dammam %{x}: %{y} µg/m³<extra></extra>",
    ))
    fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)", line_width=1)
    plo(fig, height=240, barmode="group",
                      title=dict(text="Weekly O₃ Average by Region",
                                 font=dict(size=11,color="#8a9acc"),x=0))
    st.plotly_chart(fig, use_container_width=True, key="weekly_bar")

    day_filter = st.selectbox("Isolate day:", ["All Days"] + days,
                              key="week_day_sel", index=0 if sel_day is None else days.index(sel_day)+1)
    st.session_state.selected_week_day = None if day_filter == "All Days" else day_filter

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 3 — CHEMISTRY
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Chemistry":
    section_label("ATMOSPHERIC CHEMISTRY — SEASONAL PATTERNS & TEMPERATURE CORRELATION")

    sel_month = st.session_state.selected_month
    metric_toggle = st.radio("Y-axis metric:", ["O₃ (µg/m³)", "NOₓ (µg/m³)", "Temperature (°C)"],
                             horizontal=True, key="chem_metric")
    metric_key = {"O₃ (µg/m³)":"o3", "NOₓ (µg/m³)":"nox", "Temperature (°C)":"temp"}[metric_toggle]

    left_col, right_col = st.columns([3, 2])

    with left_col:
        breadcrumb(["Chemistry", "Seasonal", sel_month] if sel_month else ["Chemistry", "Seasonal"])
        section_label("SEASONAL O₃ & NOₓ — DUAL AXIS  ·  Click a month to cross-filter scatter")

        df_s = df_seasonal.copy()
        alpha_fn = lambda m: 1.0 if (sel_month is None or m == sel_month) else 0.2

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=MONTHS, y=SEASONAL_O3, name="O₃ µg/m³",
            line=dict(color="#6082ff", width=2.5),
            mode="lines+markers",
            marker=dict(
                size=8, color="#6082ff",
                opacity=[alpha_fn(m) for m in MONTHS],
            ),
            hovertemplate="%{x}: %{y} µg/m³<extra>O₃</extra>",
        ))
        fig.add_trace(go.Scatter(
            x=MONTHS, y=SEASONAL_TEMP, name="Temp °C",
            line=dict(color="#f5a623", width=1.5, dash="dot"),
            mode="lines+markers", yaxis="y2",
            marker=dict(size=6, color="#f5a623"),
            hovertemplate="%{x}: %{y}°C<extra>Temp</extra>",
        ))
        fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)", line_width=1.5)
        plo(fig, height=270,
            yaxis=dict(title="O₃ µg/m³", range=[0,220], gridcolor="rgba(96,130,255,0.07)"),
            yaxis2=dict(title="Temp °C", range=[0,60], overlaying="y", side="right",
                        showgrid=False, tickfont=dict(color="#f5a623")),
            title=dict(text="Seasonal O₃ & Temperature", font=dict(size=11,color="#8a9acc"),x=0),
        )
        st.plotly_chart(fig, use_container_width=True, key="seasonal_dual")

        month_filter = st.selectbox("Cross-filter by month:", ["All Months"] + MONTHS,
                                    key="month_sel",
                                    index=0 if sel_month is None else MONTHS.index(sel_month)+1)
        st.session_state.selected_month = None if month_filter == "All Months" else month_filter

        # ── Clickable month table ──────────────────────────────────────────
        st.markdown("---")
        section_label("MONTHLY DATA TABLE")
        tbl_df = df_seasonal[["month","o3","nox","temp","standard"]].copy()
        tbl_df.columns = ["Month","O₃ µg/m³","NOₓ µg/m³","Temp °C","Standard"]
        if sel_month:
            tbl_df = tbl_df[tbl_df["Month"] == sel_month]
        st.dataframe(tbl_df, use_container_width=True, hide_index=True)

    with right_col:
        section_label("TEMPERATURE vs O₃ SCATTER  ·  Correlation analysis")
        scatter_df = pd.DataFrame({
            "temp": SEASONAL_TEMP, "o3": SEASONAL_O3, "month": MONTHS,
        })
        scatter_df["highlight"] = scatter_df["month"].apply(
            lambda m: "Selected" if m == sel_month else "All Months"
        )
        # Build scatter manually so we avoid trendline="ols" (requires statsmodels)
        fig = go.Figure()
        pt_colors = (
            ["#ff4f4f" if m == sel_month else "#6082ff" for m in MONTHS]
            if sel_month else ["#6082ff"] * 12
        )
        fig.add_trace(go.Scatter(
            x=scatter_df["temp"], y=scatter_df["o3"],
            mode="markers+text", text=scatter_df["month"],
            textposition="top center",
            textfont=dict(size=9, color="#8a9acc"),
            marker=dict(size=9, color=pt_colors),
            hovertemplate="<b>%{text}</b><br>Temp: %{x}°C<br>O₃: %{y} µg/m³<extra></extra>",
            showlegend=False,
        ))
        # Manual linear trendline via numpy polyfit (no statsmodels required)
        _c = np.polyfit(scatter_df["temp"], scatter_df["o3"], 1)
        _x_line = np.linspace(scatter_df["temp"].min(), scatter_df["temp"].max(), 60)
        _y_line = np.polyval(_c, _x_line)
        fig.add_trace(go.Scatter(
            x=_x_line, y=_y_line,
            mode="lines", name="Linear fit",
            line=dict(color="rgba(96,130,255,0.5)", width=1.5, dash="dot"),
            hoverinfo="skip", showlegend=False,
        ))
        fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)", line_width=1)
        plo(fig, height=320,
                          title=dict(text="O₃ vs Temperature (°C)", font=dict(size=11,color="#8a9acc"),x=0))
        st.plotly_chart(fig, use_container_width=True, key="scatter_chem")
        st.markdown("""
        <div class='info-box'>
        <b>Pearson r ≈ +0.97</b> — strong positive correlation between temperature and O₃.<br>
        Each 5°C increase in peak summer temperature corresponds to ~23 µg/m³ rise in O₃.
        August records the seasonal maximum (192 µg/m³) coinciding with 44°C mean temperature.
        </div>
        """, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 4 — ANALYTICS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Analytics":
    section_label("LONG-TERM ANALYTICS — 2015–2026 TREND & MITIGATION SCENARIOS")

    sel_year    = st.session_state.selected_year
    sel_mit     = st.session_state.selected_mitigation

    a_left, a_right = st.columns([3, 2])

    with a_left:
        breadcrumb(["Analytics", "Long-term Trend", sel_year] if sel_year else ["Analytics","Long-term Trend"])
        section_label("ANNUAL MEAN O₃ & EXCEEDANCES — 2015–2026  ·  Click a year to isolate")

        alpha_y = lambda y: 1.0 if (sel_year is None or y == sel_year) else 0.25

        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=df_longterm["year"], y=df_longterm["o3"], name="Annual Mean O₃",
            line=dict(color="#6082ff", width=2.5),
            mode="lines+markers",
            marker=dict(
                size=9, color="#6082ff",
                opacity=[alpha_y(y) for y in df_longterm["year"]],
                line=dict(color="#0b0e1a", width=1),
            ),
            hovertemplate="<b>%{x}</b><br>O₃: %{y} µg/m³<extra></extra>",
        ))
        fig.add_trace(go.Bar(
            x=df_longterm["year"], y=df_longterm["exceedances"], name="Exceedances",
            yaxis="y2",
            marker_color=[
                f"rgba(255,79,79,{alpha_y(y)})" for y in df_longterm["year"]
            ],
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>Exceedances: %{y}<extra></extra>",
        ))
        fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)", line_width=1.5)
        plo(fig, height=280, barmode="overlay",
            yaxis=dict(title="O₃ µg/m³", range=[0,220], gridcolor="rgba(96,130,255,0.07)"),
            yaxis2=dict(title="Exceedances", range=[0,250], overlaying="y", side="right",
                        showgrid=False, tickfont=dict(color="#ff4f4f")),
            title=dict(text="2015–2026 O₃ Trend  (+108% since 2015)",
                       font=dict(size=11,color="#8a9acc"),x=0),
        )
        st.plotly_chart(fig, use_container_width=True, key="longterm_dual")

        year_filter = st.selectbox(
            "Isolate year:", ["All Years"] + df_longterm["year"].tolist(),
            key="year_sel",
            index=0 if sel_year is None else df_longterm["year"].tolist().index(sel_year)+1,
        )
        st.session_state.selected_year = None if year_filter == "All Years" else year_filter
        if sel_year:
            row = df_longterm[df_longterm["year"]==sel_year].iloc[0]
            c1,c2,c3 = st.columns(3)
            c1.metric(f"{sel_year} Mean O₃", f"{row['o3']} µg/m³")
            c2.metric(f"{sel_year} Exceedances", int(row["exceedances"]))
            c3.metric("vs 2015 Baseline", f"+{row['o3']-88} µg/m³")

    with a_right:
        breadcrumb(["Mitigation Scenarios"])
        section_label("MITIGATION IMPACT  ·  Click a scenario to see details")

        mit_colors = [
            "#ff4f4f" if (sel_mit is None or sel_mit == "Baseline") else "rgba(255,79,79,0.25)",
            "#6082ff" if (sel_mit is None or sel_mit == "VOC -30%") else "rgba(96,130,255,0.25)",
            "#f5a623" if (sel_mit is None or sel_mit == "NOx -30%") else "rgba(245,166,35,0.25)",
            "#3af0b5" if (sel_mit is None or sel_mit == "Combined") else "rgba(58,240,181,0.25)",
        ]
        fig = go.Figure(go.Bar(
            x=df_mitigation["scenario"], y=df_mitigation["value"],
            marker_color=mit_colors,
            marker_line_width=0,
            hovertemplate="<b>%{x}</b><br>O₃: %{y} µg/m³<extra></extra>",
            text=df_mitigation["value"].apply(lambda v: f"{v} µg/m³"),
            textposition="outside", textfont=dict(size=10, color="#c9d1e8"),
        ))
        fig.add_hline(y=120, line_dash="dot", line_color="rgba(58,240,181,0.5)", line_width=1.5,
                      annotation_text="WHO 120", annotation_font_color="#3af0b5", annotation_font_size=9)
        plo(fig, height=240,
                          yaxis=dict(range=[0,220], gridcolor="rgba(96,130,255,0.07)"),
                          title=dict(text="Projected O₃ by Mitigation Scenario",
                                     font=dict(size=11,color="#8a9acc"),x=0))
        st.plotly_chart(fig, use_container_width=True, key="mitigation_bar")

        mit_sel = st.selectbox(
            "Scenario detail:",
            ["Select…"] + df_mitigation["scenario"].tolist(),
            key="mit_sel",
            index=0 if sel_mit is None else df_mitigation["scenario"].tolist().index(sel_mit)+1,
        )
        st.session_state.selected_mitigation = None if mit_sel == "Select…" else mit_sel

        if sel_mit:
            row = df_mitigation[df_mitigation["scenario"]==sel_mit].iloc[0]
            reduction = row["reduction"]
            st.markdown(f"""
            <div class='info-box'>
            <b>{row['scenario']}</b><br>
            Projected O₃: <b>{int(row['value'])} µg/m³</b><br>
            Reduction vs baseline: <b>{reduction:.1f}%</b><br>
            {"WHO standard met." if row['value'] <= 120 else f"Still {int(row['value'])-120} µg/m³ above WHO."}
            </div>
            """, unsafe_allow_html=True)

        # Scenario impact matrix
        st.markdown("---")
        section_label("SCENARIO IMPACT MATRIX")
        matrix_df = df_mitigation[["scenario","value","reduction"]].copy()
        matrix_df.columns = ["Scenario","O₃ µg/m³","Reduction %"]
        st.dataframe(matrix_df, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════════════════════════════════
#  PAGE 5 — ALERTS
# ══════════════════════════════════════════════════════════════════════════════
elif page == "Alerts":
    section_label("ACTIVE ALERTS — SEVERITY QUEUE & ACK WORKFLOW")

    sev_order   = {"Critical":0,"Danger":1,"Warning":2,"Info":3}
    sev_colors  = {"Critical":"#ff4f4f","Danger":"#ff8c42","Warning":"#f5a623","Info":"#6082ff"}
    sev_css_cls = {"Critical":"alert-critical","Danger":"alert-danger",
                   "Warning":"alert-warning","Info":"alert-info"}

    al_left, al_right = st.columns([3, 2])

    with al_left:
        # Severity slicer
        sev_filter = st.radio(
            "Filter by severity:",
            ["All", "Critical", "Danger", "Warning", "Info"],
            horizontal=True, key="sev_radio",
            index=["All","Critical","Danger","Warning","Info"].index(
                st.session_state.alert_severity_filter
            ),
        )
        st.session_state.alert_severity_filter = sev_filter

        unack_counts = {}
        for sev in ["Critical","Danger","Warning","Info"]:
            count = sum(1 for a in ALERTS if a["severity"]==sev and not st.session_state.ack_state[a["id"]])
            if count: unack_counts[sev] = count
        if unack_counts:
            badge_html = " ".join(
                f'<span class="badge" style="background:rgba(255,79,79,.15);color:{sev_colors[s]};">'
                f'{s}: {c} unacked</span>'
                for s,c in unack_counts.items()
            )
            st.markdown(badge_html, unsafe_allow_html=True)

        st.markdown("---")
        filtered = sorted(
            [a for a in ALERTS if sev_filter == "All" or a["severity"] == sev_filter],
            key=lambda a: sev_order.get(a["severity"],99),
        )
        breadcrumb([f"Alerts", f"{len(filtered)} shown"])

        for a in filtered:
            ack = st.session_state.ack_state[a["id"]]
            col = sev_colors[a["severity"]]
            css = sev_css_cls[a["severity"]]
            ack_badge = (
                f'<span style="font-size:9px;color:#3af0b5;background:rgba(58,240,181,.1);'
                f'padding:2px 7px;border-radius:4px;margin-left:8px;">✓ ACK</span>'
                if ack else
                f'<span style="font-size:9px;color:#ff4f4f;background:rgba(255,79,79,.1);'
                f'padding:2px 7px;border-radius:4px;margin-left:8px;">UNACKED</span>'
            )
            st.markdown(f"""
            <div class='alert-card {css}'>
              <div style='display:flex;justify-content:space-between;align-items:flex-start;'>
                <div>
                  <span style='font-size:10px;font-weight:700;color:{col};
                               text-transform:uppercase;letter-spacing:.1em;'>
                    {a['severity']}
                  </span>
                  {ack_badge}
                  <span style='font-size:9px;color:#4a5580;margin-left:10px;font-family:monospace;'>
                    {a['id']} | {a['timestamp']}
                  </span>
                </div>
                {"" if a['value']==0 else
                 f'<span style="color:{col};font-weight:700;font-family:monospace;font-size:13px;">'
                 f'{a["value"]} µg/m³</span>'}
              </div>
              <div style='font-weight:600;margin:6px 0 2px;'>{a['location']}</div>
              <div style='font-size:12px;color:#8a9acc;'>{a['message']}</div>
            </div>
            """, unsafe_allow_html=True)
            if not ack:
                if st.button(f"Acknowledge {a['id']}", key=f"ack_{a['id']}"):
                    st.session_state.ack_state[a["id"]] = True
                    st.rerun()

    with al_right:
        section_label("HEALTH IMPACT GUIDE")
        for rng, label, desc, col in HEALTH_BREAKPOINTS:
            st.markdown(f"""
            <div style='background:rgba(255,255,255,0.02);border:1px solid rgba(96,130,255,0.1);
                        border-left:4px solid {col};border-radius:8px;padding:10px 14px;margin-bottom:8px;'>
              <div style='display:flex;justify-content:space-between;align-items:center;margin-bottom:3px;'>
                <span style='font-weight:700;color:{col};font-size:12px;'>{label}</span>
                <span style='font-family:monospace;font-size:10px;color:#4a5580;'>{rng} µg/m³</span>
              </div>
              <div style='font-size:11px;color:#8a9acc;'>{desc}</div>
            </div>
            """, unsafe_allow_html=True)

        st.markdown("---")
        section_label("ALERT SUMMARY")
        c1,c2 = st.columns(2)
        total     = len(ALERTS)
        unacked   = sum(1 for a in ALERTS if not st.session_state.ack_state[a["id"]])
        critical  = sum(1 for a in ALERTS if a["severity"]=="Critical")
        c1.metric("Total Alerts", total)
        c2.metric("Unacknowledged", unacked, delta=f"-{total-unacked} acked", delta_color="inverse")
        st.metric("Critical/Danger", critical, delta="Immediate action required", delta_color="inverse")

# ══════════════════════════════════════════════════════════════════════════════
#  FOOTER
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("---")
st.markdown("""
<div style='text-align:center;font-family:monospace;font-size:10px;color:#3a4060;padding:8px 0;'>
  OZ ONE v1.0 · Jubail & Dammam O₃ Unified Monitoring System ·
  Streamlit + Plotly · WHO Standard: 120 µg/m³ ·
  Data: 2026-05-02 13:14 KSA
</div>
""", unsafe_allow_html=True)
