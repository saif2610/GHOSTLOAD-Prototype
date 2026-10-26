import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="GHOSTLOAD | Reliability Lab",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------- Theme ----------
st.markdown("""
<style>
:root { color-scheme: dark; }
.stApp {
    background:
      radial-gradient(circle at 12% 0%, rgba(24, 80, 125, .22), transparent 30%),
      radial-gradient(circle at 95% 10%, rgba(35, 110, 105, .13), transparent 28%),
      #080d16;
    color: #e8eef7;
}
.block-container { padding-top: 1.7rem; max-width: 1450px; }
.hero {
    border: 1px solid rgba(125, 170, 220, .22);
    background: linear-gradient(120deg, rgba(20, 38, 62, .92), rgba(10, 20, 34, .85));
    padding: 1.5rem 1.6rem; border-radius: 20px; margin-bottom: 1.1rem;
}
.eyebrow { color: #67d8d0; text-transform: uppercase; letter-spacing: .16em; font-size: .75rem; font-weight: 700; }
.hero h1 { font-size: 2.55rem; margin: .35rem 0 .25rem; color: #f4f8ff; }
.hero p { color: #b8c7da; font-size: 1.02rem; margin: 0; }
.small-note { color: #93a6bd; font-size: .83rem; }
.panel {
    border: 1px solid rgba(125, 170, 220, .17);
    background: rgba(17, 27, 42, .72);
    padding: 1rem 1.1rem; border-radius: 15px; min-height: 108px;
}
.panel-label { color: #91a6bf; font-size: .8rem; margin-bottom: .45rem; }
.panel-value { color: #f3f7ff; font-size: 1.75rem; font-weight: 750; }
.panel-help { color: #94a7bc; font-size: .76rem; margin-top: .2rem; }
div[data-testid="stMetric"] {
    background: rgba(17, 27, 42, .72);
    border: 1px solid rgba(125, 170, 220, .17);
    padding: 14px 16px; border-radius: 14px;
}
div[data-testid="stMetricLabel"] { color: #9fb2c9; }
div[data-testid="stMetricValue"] { color: #f3f7ff; }
.stButton button[kind="primary"] {
    background: #5de0d2; color: #07131d; border: 0; font-weight: 800;
    border-radius: 10px; min-height: 2.8rem;
}
.stButton button[kind="secondary"] { border-radius: 10px; }
section[data-testid="stSidebar"] { background: #0b1320; border-right: 1px solid #1b2b40; }
hr { border-color: rgba(125,170,220,.16); }
</style>
""", unsafe_allow_html=True)

# ---------- Simulation engine ----------
def simulate_run(
    order_count: int,
    traffic_level: str,
    outage_probability: float,
    latency_ms: int,
    retry_mode: str,
    idempotency: bool,
    seed: int,
):
    """Deterministic demo simulation. Does not send traffic to any real service."""
    rng = random.Random(seed)
    traffic_factor = {"Low": 0.75, "Moderate": 1.0, "High": 1.55}[traffic_level]
    rows = []
    for i in range(1, order_count + 1):
        base_latency = max(30, int(rng.gauss(230 * traffic_factor, 75 * traffic_factor)))
        network_latency = latency_ms
        outage = rng.random() < outage_probability
        timeout = outage or rng.random() < min(0.55, max(0.0, (base_latency + network_latency - 700) / 2200))
        retries = 0
        attempts = 1

        if timeout:
            if retry_mode == "No retries":
                attempts = 1
            elif retry_mode == "One retry":
                attempts = 2
                retries = 1
            else:
                attempts = 3
                retries = 2

        # Approximate the chance a retry succeeds after a transient fault.
        recovered = (not timeout) or (timeout and rng.random() < (0.25 if retry_mode == "No retries" else 0.70 if retry_mode == "One retry" else 0.86))
        final_latency = base_latency + network_latency + (retries * rng.randint(180, 450))
        if timeout and not recovered:
