
# ============================================================
# GHOSTLOAD | CLOUD RELIABILITY & AI WORKLOAD OBSERVATORY
# Complete application: Streamlit + Pandas + Plotly
# ============================================================

import random
from datetime import datetime

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st


# ============================ CONFIG =========================

st.set_page_config(
    page_title="GHOSTLOAD | Cloud Observatory",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)

CYAN = "#55E6EF"
BLUE = "#7599FF"
PURPLE = "#B69CFF"
PINK = "#FF7BA9"
GREEN = "#65F0B1"
ORANGE = "#FFBF69"
WHITE = "#EDF4FF"


# ============================= CSS ===========================

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080b12;
    --panel: #101621;
    --border: #263348;
    --cyan: #55e6ef;
    --muted: #94a3b8;
    --white: #edf4ff;
}

.stApp {
    background:
        radial-gradient(ellipse at 5% 0%, #14253b 0%, transparent 36%),
        radial-gradient(ellipse at 95% 15%, #112b36 0%, transparent 27%),
        var(--bg);
    color: var(--white);
    font-family: 'Space Grotesk', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(8, 11, 18, .8);
}

[data-testid="stSidebar"] {
    background: #0b101a;
    border-right: 1px solid var(--border);
}

h1, h2, h3, h4, p, label {
    font-family: 'Space Grotesk', sans-serif;
}

h1 {
    letter-spacing: -1.5px;
}

.hero {
    padding: 34px;
    border: 1px solid #294052;
    border-radius: 22px;
    background: linear-gradient(120deg, #182e40, #0c121e 65%, #11242f);
    position: relative;
    overflow: hidden;
    animation: appear .65s ease-out;
    margin-bottom: 22px;
}

.hero:after {
    content: "";
    position: absolute;
    right: -90px;
    top: -130px;
    width: 310px;
    height: 310px;
    border: 1px solid rgba(85,230,239,.25);
    border-radius: 50%;
    box-shadow:
        0 0 0 28px rgba(85,230,239,.025),
        0 0 0 58px rgba(85,230,239,.02),
        0 0 90px rgba(85,230,239,.09);
    pointer-events: none;
}

.eyebrow, .section-label {
    color: var(--cyan);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero-title {
    font-size: clamp(38px, 5vw, 65px);
    font-weight: 700;
    letter-spacing: -3px;
    line-height: 1;
    margin: 16px 0;
}

.hero-title span {
    color: var(--cyan);
}

.hero-subtitle {
    color: #b3c2d6;
    max-width: 700px;
    font-size: 15px;
    line-height: 1.7;
}

.status-pill {
    display: inline-block;
    padding: 6px 11px;
    border-radius: 999px;
    border: 1px solid #315364;
    color: var(--cyan);
    background: rgba(85,230,239,.06);
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
}

.panel {
    background: linear-gradient(145deg, #121b29, #0e1420);
    border: 1px solid var(--border);
    border-radius: 16px;
    padding: 20px;
    margin-bottom: 14px;
    transition: border-color .2s ease, transform .2s ease;
}

.panel:hover {
    border-color: #42627b;
    transform: translateY(-2px);
}

.metric-label {
    color: var(--muted);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 29px;
    color: var(--white);
    margin: 9px 0 4px;
}

.metric-note {
    color: var(--cyan);
    font-size: 11px;
    letter-spacing: .5px;
}

.small-muted {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.65;
}

.node {
    border: 1px solid #2e5066;
    background: #101e2c;
    padding: 14px 8px;
    border-radius: 12px;
    color: #dcecff;
    font-size: 12px;
    text-align: center;
    min-height: 74px;
}

.stButton > button {
    border-radius: 10px;
    border: 1px solid #3a6576;
    background: linear-gradient(110deg, #173849, #142938);
    color: #e9fcff;
    font-weight: 600;
    transition: all .2s ease;
}

.stButton > button:hover {
    border-color: var(--cyan);
    color: white;
    box-shadow: 0 0 18px rgba(85,230,239,.15);
}

.stDownloadButton > button {
    border-radius: 10px;
    background: #13202d;
    border: 1px solid #2f5265;
    color: #e9fcff;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 8px;
    border-bottom: 1px solid var(--border);
}

.stTabs [data-baseweb="tab"] {
    background: transparent;
    border-radius: 9px 9px 0 0;
    color: #a6b4c8;
    padding: 12px 15px;
}

.stTabs [aria-selected="true"] {
    color: var(--cyan) !important;
    border-bottom: 2px solid var(--cyan);
}

div[data-testid="stMetric"] {
    background: #101824;
    border: 1px solid var(--border);
    padding: 14px;
    border-radius: 13px;
}

hr {
    border-color: var(--border);
}

@keyframes appear {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    * { animation: none !important; transition: none !important; }
}
</style>
""", unsafe_allow_html=True)


# ======================== CHART THEME ========================

def style_chart(fig, height=350, title=None):
    fig.update_layout(
        title=dict(
            text=title or "",
            font=dict(size=17, color=WHITE),
            x=0.02,
            xanchor="left",
        ),
        template="plotly_dark",
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(12,18,30,0.35)",
        font=dict(family="Arial, sans-serif", color="#B8C6D9", size=12),
        margin=dict(l=20, r=20, t=65, b=45),
        hoverlabel=dict(
            bgcolor="#101B2A",
            bordercolor=CYAN,
            font=dict(color="#FFFFFF", size=12),
        ),
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=1.02,
            xanchor="right",
            x=1,
        ),
        xaxis=dict(
            showgrid=False,
            zeroline=False,
            linecolor="#263348",
        ),
        yaxis=dict(
            showgrid=True,
            gridcolor="rgba(130,160,190,0.12)",
            zeroline=False,
            linecolor="#263348",
        ),
    )
    return fig


def metric_card(label, value, note="SIMULATED"):
    st.markdown(
        f"""
        <div class="panel">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
            <div class="metric-note">{note}</div>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================= SIMULATION ENGINE ===================

def run_simulation(
    request_count,
    interruption_probability,
    base_latency,
    max_retries,
    idempotency,
    seed,
):
    """Generate synthetic request records; no real network requests are sent."""

    rng = random.Random(seed)
    records = []

    for request_id in range(1, request_count + 1):
        attempts = 0
        duplicate_operations = 0
        response_lost = False
        total_latency = 0
        final_status = "FAILED"
        failure_reason = "Retry limit reached"

        for attempt in range(max_retries + 1):
            attempts += 1

            latency = max(
                5,
                int(rng.gauss(base_latency, max(5, base_latency * 0.18))),
            )
            total_latency += latency

            interrupted = rng.random() < interruption_probability

            if not interrupted:
                final_status = "SUCCESS"
                failure_reason = ""
                break

            # Model whether a server processed the request but its response
            # was lost. This is a simplified scenario.
            server_processed = rng.random() < 0.55

            if server_processed:
                response_lost = True

                if attempt < max_retries:
                    if not idempotency:
                        duplicate_operations += 1
                    continue

                final_status = "UNKNOWN"
                failure_reason = "Response lost; processing uncertain"
                break

            if attempt < max_retries:
                continue

            final_status = "FAILED"
            failure_reason = "Service interruption"

        records.append({
            "Request ID": f"REQ-{request_id:05d}",
            "Attempts": attempts,
            "Latency (ms)": total_latency,
            "Status": final_status,
            "Response Lost": response_lost,
            "Duplicate Operations": duplicate_operations,
            "Idempotency": "ON" if idempotency else "OFF",
            "Failure Reason": failure_reason,
        })

    return pd.DataFrame(records)


def calculate_metrics(data):
    total = len(data)

    if total == 0:
        return {
            "success_rate": 0.0,
            "failure_rate": 0.0,
            "unknown_rate": 0.0,
            "duplicates": 0,
            "avg_latency": 0.0,
            "avg_attempts": 0.0,
        }

    return {
        "success_rate": (data["Status"] == "SUCCESS").mean() * 100,
        "failure_rate": (data["Status"] == "FAILED").mean() * 100,
        "unknown_rate": (data["Status"] == "UNKNOWN").mean() * 100,
        "duplicates": int(data["Duplicate Operations"].sum()),
        "avg_latency": float(data["Latency (ms)"].mean()),
        "avg_attempts": float(data["Attempts"].mean()),
    }


def make_strategy_table(count, interruption, latency, seed):
    strategies = [
        ("No retries", 0, False),
        ("One retry", 1, False),
        ("Two retries", 2, False),
        ("Two retries + idempotency", 2, True),
    ]

    results = []

    for name, retries, idem in strategies:
        result = run_simulation(
            request_count=count,
            interruption_probability=interruption,
            base_latency=latency,
            max_retries=retries,
            idempotency=idem,
            seed=seed,
        )
        m = calculate_metrics(result)

        results.append({
            "Strategy": name,
            "Success rate (%)": round(m["success_rate"], 2),
            "Failure rate (%)": round(m["failure_rate"], 2),
            "Unknown outcomes (%)": round(m["unknown_rate"], 2),
            "Duplicate operations": m["duplicates"],
            "Average latency (ms)": round(m["avg_latency"], 1),
            "Average attempts": round(m["avg_attempts"], 2),
        })

    return pd.DataFrame(results)


# ============================ SIDEBAR ========================

with st.sidebar:
    st.markdown(
        '<div class="eyebrow">GHOSTLOAD / CONTROL DECK</div>',
        unsafe_allow_html=True,
    )
    st.markdown("## Experiment setup")
    st.caption("Configure the simulated test environment.")

    request_count = st.slider(
        "Number of requests",
        100, 5000, 1000, step=100,
    )

    interruption_probability = st.slider(
        "Interruption probability",
        0.0, 0.8, 0.15, step=0.05,
        help="Chance an individual request attempt is interrupted.",
    )

    base_latency = st.slider(
        "Base latency (ms)",
        20, 1000, 120, step=20,
    )

    max_retries = st.selectbox(
        "Retry policy",
        options=[0, 1, 2, 3],
        index=2,
        format_func=lambda n: "No retries" if n == 0 else f"{n} retries",
    )

    idempotency = st.checkbox(
        "Enable idempotency protection",
        value=True,
        help="Models protection against duplicate operation effects.",
    )

    seed = st.number_input(
        "Experiment seed",
        min_value=1,
        max_value=999999,
        value=42,
        step=1,
    )

    if "experiment_seed" not in st.session_state:
        st.session_state["experiment_seed"] = int(seed)

    if st.button("↻ Generate new experiment", use_container_width=True):
        st.session_state["experiment_seed"] += 1
        st.rerun()

    st.divider()

    st.markdown("### Execution mode")
    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Local simulation</div>
            <p class="small-muted">
                Synthetic request and cloud metrics. No real servers or
                payment systems are affected.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )


# ======================= GENERATE DATA =======================

effective_seed = int(st.session_state["experiment_seed"])

data = run_simulation(
    request_count=request_count,
    interruption_probability=interruption_probability,
    base_latency=base_latency,
    max_retries=max_retries,
    idempotency=idempotency,
    seed=effective_seed,
)

metrics = calculate_metrics(data)

strategy_data = make_strategy_table(
    count=min(request_count, 2000),
    interruption=interruption_probability,
    latency=base_latency,
    seed=effective_seed,
)


# ============================= HERO ==========================

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">
            CLOUD RELIABILITY / AI WORKLOADS / RESILIENCE
        </div>
        <div class="hero-title">GHOST<span>LOAD</span></div>
        <div class="hero-subtitle">
            A cloud reliability observatory for exploring service failures,
            request recovery, workload pressure, and retry strategies
            through controlled experiments.
        </div>
        <br>
        <span class="status-pill">● SIMULATION ENGINE ACTIVE</span>
        &nbsp;
        <span class="status-pill">LOCAL EXPERIMENT</span>
    </div>
    """,
    unsafe_allow_html=True,
)

st.markdown(
    f"""
    <div class="small-muted">
        Experiment seed: <b>{effective_seed}</b>
        &nbsp;·&nbsp; Requests: <b>{request_count:,}</b>
        &nbsp;·&nbsp; Generated: <b>{datetime.now().strftime("%d %b %Y, %H:%M:%S")}</b>
    </div>
    """,
    unsafe_allow_html=True,
)

st.write("")


# ============================== TABS =========================

overview, evidence, strategy, cloud, methodology = st.tabs([
    "◈ Overview",
    "▤ Request evidence",
    "⇄ Strategy lab",
    "☁ Cloud lab",
    "ⓘ Methodology",
])


# ============================================================
# TAB 1 — OVERVIEW
# ============================================================

with overview:
    st.markdown("## System overview")
    st.caption("An at-a-glance view of the current reliability experiment.")

    c1, c2, c3, c4 = st.columns(4)

    with c1:
        metric_card("Successful requests", f"{metrics['success_rate']:.1f}%")

    with c2:
        metric_card("Failed requests", f"{metrics['failure_rate']:.1f}%")

    with c3:
        metric_card("Average latency", f"{metrics['avg_latency']:.0f} ms")

    with c4:
        metric_card("Duplicate operations", f"{metrics['duplicates']:,}")

    left, right = st.columns([1, 1.35])

    with left:
        st.markdown("### Request health distribution")

        outcome_counts = (
            data["Status"]
            .value_counts()
            .reindex(["SUCCESS", "FAILED", "UNKNOWN"], fill_value=0)
        )

        donut = go.Figure(
            data=[
                go.Pie(
                    labels=outcome_counts.index,
                    values=outcome_counts.values,
                    hole=0.72,
                    sort=False,
                    marker=dict(
                        colors=[CYAN, PINK, PURPLE],
                        line=dict(color="#0B101A", width=4),
                    ),
                    textinfo="percent",
                    textposition="inside",
                    hovertemplate=(
                        "<b>%{label}</b><br>"
                        "Requests: %{value:,}<br>"
                        "Share: %{percent}<extra></extra>"
                    ),
                )
            ]
        )

        donut.add_annotation(
            text=(
                f"<b>{len(data):,}</b>"
                "<br><span style='font-size:11px'>REQUESTS</span>"
            ),
            x=0.5,
            y=0.5,
            showarrow=False,
            font=dict(size=23, color=WHITE),
        )

        donut.update_layout(showlegend=True)
        style_chart(donut, 350, "Request outcome mix")

        st.plotly_chart(
            donut,
            use_container_width=True,
            key="overview_donut",
        )

    with right:
        st.markdown("### Latency telemetry")

        latency_plot = go.Figure()

        latency_plot.add_trace(
            go.Scatter(
                x=list(range(1, len(data) + 1)),
                y=data["Latency (ms)"],
                mode="lines",
                name="Request latency",
                line=dict(color=CYAN, width=2, shape="spline"),
                fill="tozeroy",
                fillcolor="rgba(85,230,239,0.10)",
                hovertemplate=(
                    "Request #%{x}<br>"
                    "Latency: %{y:.0f} ms<extra></extra>"
                ),
            )
        )

        latency_plot.add_hline(
            y=base_latency,
            line_dash="dash",
            line_color=ORANGE,
            annotation_text="Configured base latency",
            annotation_position="top left",
        )

        latency_plot.update_xaxes(title="Request number")
        latency_plot.update_yaxes(
            title="Total latency (ms)",
            rangemode="tozero",
        )

        style_chart(latency_plot, 350, "Request latency curve")

        st.plotly_chart(
            latency_plot,
            use_container_width=True,
            key="overview_latency",
        )

    st.markdown("### Request processing pipeline")

    pipeline = st.columns(4)

    pipeline_items = [
        ("01", "Request created", "Generate a test request"),
        ("02", "Failure simulated", "Apply interruption probability"),
        ("03", "Retry decision", "Apply configured retry policy"),
        ("04", "Outcome recorded", "Store the final result"),
    ]

    for col, (number, title, description) in zip(pipeline, pipeline_items):
        with col:
            st.markdown(
                f"""
                <div class="node">
                    <div class="section-label">{number}</div>
                    <b>{title}</b>
                    <div class="small-muted">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "These results are simulated. Retries may improve the chance of "
        "success but add latency. Idempotency is modelled as protection "
        "against duplicate effects; no real server is being tested."
    )


# ============================================================
# TAB 2 — REQUEST EVIDENCE
# ============================================================

with evidence:
    st.markdown("## Request-level evidence")
    st.caption("Inspect individual records and export the generated dataset.")

    search_term = st.text_input(
        "Search request ID",
        placeholder="Example: REQ-00025",
    )

    status_filter = st.multiselect(
        "Filter by final status",
        options=["SUCCESS", "FAILED", "UNKNOWN"],
        default=["SUCCESS", "FAILED", "UNKNOWN"],
    )

    filtered = data[data["Status"].isin(status_filter)].copy()

    if search_term.strip():
        filtered = filtered[
            filtered["Request ID"].str.contains(
                search_term.strip(),
                case=False,
                regex=False,
            )
        ]

    st.markdown(f"**Showing {len(filtered):,} of {len(data):,} requests**")

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    st.download_button(
        "⬇ Download filtered evidence (CSV)",
        data=filtered.to_csv(index=False).encode("utf-8"),
        file_name="ghostload_request_evidence.csv",
        mime="text/csv",
        use_container_width=True,
    )

    e1, e2, e3 = st.columns(3)

    with e1:
        st.metric("Requests in view", f"{len(filtered):,}")

    with e2:
        st.metric(
            "Response-loss events",
            int(filtered["Response Lost"].sum()),
        )

    with e3:
        st.metric(
            "Duplicate operations",
            int(filtered["Duplicate Operations"].sum()),
        )

    st.markdown("### Latency distribution")

    if not filtered.empty:
        histogram = px.histogram(
            filtered,
            x="Latency (ms)",
            color="Status",
            color_discrete_map={
                "SUCCESS": CYAN,
                "FAILED": PINK,
                "UNKNOWN": PURPLE,
            },
            nbins=35,
            opacity=0.85,
        )

        histogram.update_layout(bargap=0.08)
        style_chart(histogram, 360, "Distribution of request latency")

        st.plotly_chart(
            histogram,
            use_container_width=True,
            key="evidence_histogram",
        )
    else:
        st.info("No requests match your current filters.")


# ============================================================
# TAB 3 — STRATEGY LAB
# ============================================================

with strategy:
    st.markdown("## Recovery strategy lab")
    st.caption("Compare retry policies under the same simulated settings.")

    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Research question</div>
            <div style="font-size:19px;font-weight:600;">
                How do retries and idempotency affect success,
                latency, and duplicate processing?
            </div>
            <p class="small-muted">
                Each strategy uses the same experiment seed and interruption
                probability for a more consistent comparison.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.dataframe(
        strategy_data,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Success rate comparison")

    colors = [PINK, BLUE, PURPLE, CYAN]

    success_fig = go.Figure()

    success_fig.add_trace(
        go.Bar(
            x=strategy_data["Strategy"],
            y=strategy_data["Success rate (%)"],
            marker=dict(
                color=colors,
                line=dict(color="rgba(255,255,255,0.12)", width=1),
            ),
            text=[
                f"{value:.1f}%"
                for value in strategy_data["Success rate (%)"]
            ],
            textposition="outside",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Success rate: %{y:.2f}%<extra></extra>"
            ),
        )
    )

    success_fig.update_layout(showlegend=False)
    success_fig.update_yaxes(
        title="Successful requests (%)",
        range=[0, 115],
    )

    style_chart(success_fig, 390, "Recovery strategy performance")

    st.plotly_chart(
        success_fig,
        use_container_width=True,
        key="strategy_success",
    )

    st.markdown("### Latency comparison")

    latency_fig = go.Figure()

    latency_fig.add_trace(
        go.Scatter(
            x=strategy_data["Strategy"],
            y=strategy_data["Average latency (ms)"],
            mode="lines+markers",
            line=dict(color=CYAN, width=3, shape="spline"),
            marker=dict(
                size=12,
                color=CYAN,
                line=dict(color=WHITE, width=1),
            ),
            fill="tozeroy",
            fillcolor="rgba(85,230,239,0.08)",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Average latency: %{y:.1f} ms<extra></extra>"
            ),
        )
    )

    latency_fig.update_yaxes(
        title="Average latency (ms)",
        rangemode="tozero",
    )

    style_chart(latency_fig, 370, "Latency cost of recovery")

    st.plotly_chart(
        latency_fig,
        use_container_width=True,
        key="strategy_latency",
    )

    st.markdown("### Duplicate operation comparison")

    duplicate_fig = go.Figure()

    duplicate_fig.add_trace(
        go.Scatter(
            x=strategy_data["Strategy"],
            y=strategy_data["Duplicate operations"],
            mode="lines+markers",
            line=dict(color=PINK, width=3, shape="spline"),
            marker=dict(size=11, color=PINK),
            fill="tozeroy",
            fillcolor="rgba(255,123,169,0.09)",
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Duplicate operations: %{y}<extra></extra>"
            ),
        )
    )

    duplicate_fig.update_yaxes(title="Duplicate operations", rangemode="tozero")
    style_chart(duplicate_fig, 350, "Duplicate processing risk")

    st.plotly_chart(
        duplicate_fig,
        use_container_width=True,
        key="strategy_duplicates",
    )

    st.markdown("### Interpretation")

    st.markdown("""
    - **No retries:** One attempt only; interrupted requests may remain incomplete.
    - **More retries:** Additional attempts may improve completion but add latency.
    - **Idempotency:** Represents a safeguard against repeated operation effects.
    - **Unknown outcomes:** A request may have been processed even when the
      client did not receive a response.
    """)

    st.warning(
        "This is a simplified model, not a guarantee of real-world performance. "
        "Actual retry and idempotency behaviour depends on server implementation."
    )

    st.download_button(
        "⬇ Download strategy comparison (CSV)",
        data=strategy_data.to_csv(index=False).encode("utf-8"),
        file_name="ghostload_strategy_comparison.csv",
        mime="text/csv",
    )


# ============================================================
# TAB 4 — CLOUD COMPUTING LAB
# ============================================================

with cloud:
    st.markdown("## Cloud infrastructure lab")
    st.caption("Explore simulated compute, network, and AI workload metrics.")

    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Cloud environment</div>
            <div style="font-size:23px;font-weight:700;">
                Compute · Network · AI workloads
            </div>
            <p class="small-muted">
                Illustrative telemetry for a future cloud monitoring platform.
                This prototype is not connected to a cloud provider.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    cloud_rng = random.Random(effective_seed + 100)

    cloud_cpu = cloud_rng.randint(25, 95)
    cloud_memory = cloud_rng.randint(35, 90)
    cloud_gpu = cloud_rng.randint(10, 98)
    cloud_availability = round(cloud_rng.uniform(98.2, 99.99), 2)
    cloud_latency = cloud_rng.randint(35, 450)
    queued_jobs = cloud_rng.randint(2, 85)

    st.markdown("### Infrastructure overview")

    availability_col, cpu_col, memory_col = st.columns(3)

    with availability_col:
        metric_card(
            "Service availability",
            f"{cloud_availability}%",
            "SIMULATED",
        )

    with cpu_col:
        metric_card("CPU utilization", f"{cloud_cpu}%", "SIMULATED")

    with memory_col:
        metric_card("Memory utilization", f"{cloud_memory}%", "SIMULATED")

    st.markdown("### Resource utilization gauges")
    st.caption("Circular gauges display generated values, not live measurements.")

    gauge_cols = st.columns(3)

    resource_values = [
        ("CPU", cloud_cpu, CYAN),
        ("Memory", cloud_memory, PURPLE),
        ("GPU", cloud_gpu, PINK),
    ]

    for col, (name, value, accent) in zip(gauge_cols, resource_values):
        with col:
            gauge = go.Figure(
                go.Indicator(
                    mode="gauge+number",
                    value=value,
                    number={
                        "suffix": "%",
                        "font": {"size": 30, "color": WHITE},
                    },
                    title={
                        "text": name,
                        "font": {"size": 15, "color": "#B8C6D9"},
                    },
                    gauge={
                        "shape": "angular",
                        "axis": {
                            "range": [0, 100],
                            "tickwidth": 0,
                            "tickcolor": "#263348",
                        },
                        "bar": {
                            "color": accent,
                            "thickness": 0.25,
                        },
                        "bgcolor": "#101621",
                        "borderwidth": 0,
                        "steps": [
                            {"range": [0, 60], "color": "#182332"},
                            {"range": [60, 85], "color": "#263044"},
                            {"range": [85, 100], "color": "#402331"},
                        ],
                    },
                )
            )

            gauge.update_layout(
                height=245,
                margin=dict(l=20, r=20, t=40, b=10),
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color=WHITE),
            )

            st.plotly_chart(
                gauge,
                use_container_width=True,
                key=f"cloud_gauge_{name}",
            )

    cloud_metrics_col1, cloud_metrics_col2 = st.columns(2)

    with cloud_metrics_col1:
        metric_card("Cloud request latency", f"{cloud_latency} ms", "SIMULATED")

    with cloud_metrics_col2:
        metric_card("AI jobs waiting", str(queued_jobs), "SIMULATED")

    st.markdown("### Cloud workload simulator")

    workload = st.select_slider(
        "Choose workload pressure",
        options=["Low", "Moderate", "High", "Extreme"],
        value="Moderate",
        key="cloud_workload",
    )

    simulate_outage = st.checkbox(
        "Simulate a cloud service interruption",
        value=False,
        key="cloud_outage",
    )

    if st.button("Analyse cloud scenario", type="primary"):
        pressure = {
            "Low": 0.15,
            "Moderate": 0.35,
            "High": 0.65,
            "Extreme": 0.90,
        }[workload]

        estimated_cpu = min(100, int(25 + pressure * 80))
        estimated_latency = int(45 + pressure * 650)
        estimated_queue = int(5 + pressure * 180)

        if simulate_outage:
            estimated_latency = int(estimated_latency * 1.8)

        st.markdown("### Scenario results")

        r1, r2, r3 = st.columns(3)

        with r1:
            st.metric("Modelled CPU pressure", f"{estimated_cpu}%")

        with r2:
            st.metric("Modelled latency", f"{estimated_latency} ms")

        with r3:
            st.metric("Modelled queued jobs", estimated_queue)

        if simulate_outage:
            st.warning(
                "This scenario includes a simulated interruption. "
                "No real cloud service has been interrupted."
            )
        elif pressure >= 0.65:
            st.warning(
                "The model indicates elevated workload pressure. "
                "Real infrastructure measurements would be needed to confirm it."
            )
        else:
            st.success("The model indicates a relatively manageable workload.")

    st.markdown("### Cloud architecture concept")

    architecture = st.columns(5)

    architecture_items = [
        ("01", "Client", "Sends requests"),
        ("02", "Cloud API", "Receives requests"),
        ("03", "Compute", "Processes work"),
        ("04", "Monitor", "Collects metrics"),
        ("05", "Recovery", "Handles failures"),
    ]

    for col, (number, title, description) in zip(
        architecture, architecture_items
    ):
        with col:
            st.markdown(
                f"""
                <div class="node">
                    <div class="section-label">{number}</div>
                    <b>{title}</b>
                    <div class="small-muted">{description}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "This version does not connect to AWS, Azure, Google Cloud, "
        "or real GPU servers. Cloud telemetry is simulated."
    )


# ============================================================
# TAB 5 — METHODOLOGY
# ============================================================

with methodology:
    st.markdown("## Research methodology")
    st.caption("Review the model, assumptions, limitations, and roadmap.")

    st.markdown("### What does GHOSTLOAD investigate?")

    st.markdown("""
    GHOSTLOAD models how an application might behave when requests
    experience connection interruptions. It compares retry policies and
    a simplified idempotency safeguard, measuring final request status,
    latency, attempts, and duplicate-operation counts.
    """)

    st.markdown("### Experiment variables")

    variables = pd.DataFrame([
        {
            "Variable": "Request count",
            "Role": "Input",
            "Description": "Number of simulated requests.",
        },
        {
            "Variable": "Interruption probability",
            "Role": "Input",
            "Description": "Chance an attempt is interrupted.",
        },
        {
            "Variable": "Base latency",
            "Role": "Input",
            "Description": "Starting latency used by the simulation.",
        },
        {
            "Variable": "Retry policy",
            "Role": "Input",
            "Description": "Number of additional attempts allowed.",
        },
        {
            "Variable": "Idempotency setting",
            "Role": "Input",
            "Description": "Whether duplicate effects are modelled as prevented.",
        },
        {
            "Variable": "Final request status",
            "Role": "Output",
            "Description": "Success, failure, or unknown outcome.",
        },
        {
            "Variable": "Latency and duplicates",
            "Role": "Output",
            "Description": "Modelled total time and repeated processing.",
        },
    ])

    st.dataframe(variables, use_container_width=True, hide_index=True)

    st.markdown("### Model assumptions")

    st.markdown("""
    - Each attempt uses the configured interruption probability.
    - Latency is sampled around the configured base latency.
    - An interrupted request may have been processed even if its response
      was lost.
    - Retrying without idempotency protection may create duplicate effects
      in the model.
    - The idempotency setting is illustrative; it does not implement
      a real database constraint or server-side idempotency key.
    - A fixed seed makes the generated experiment reproducible with
      the same settings and software version.
    """)

    st.markdown("### Limitations")

    st.warning(
        "This is a simulation prototype, not a production cloud monitoring system."
    )

    st.markdown("""
    - No real HTTP requests are sent.
    - No real network connections are disrupted.
    - No real cloud provider or GPU is monitored.
    - No AI model analyses logs in this version.
    - The failure and latency distributions are simplified assumptions.
    - Simulated availability must not be interpreted as a real service-level
      availability guarantee.
    """)

    st.markdown("### Development roadmap")

    roadmap = pd.DataFrame([
        {
            "Phase": "1",
            "Feature": "Simulation engine",
            "Goal": "Explore failures, retries, and duplicate effects.",
            "Status": "Current prototype",
        },
        {
            "Phase": "2",
            "Feature": "Controlled local test API",
            "Goal": "Send requests to a test service and record outcomes.",
            "Status": "Planned",
        },
        {
            "Phase": "3",
            "Feature": "Persistent experiment storage",
            "Goal": "Save and compare test runs.",
            "Status": "Planned",
        },
        {
            "Phase": "4",
            "Feature": "Cloud telemetry integration",
            "Goal": "Collect authorised resource and service metrics.",
            "Status": "Planned",
        },
        {
            "Phase": "5",
            "Feature": "AI failure analyst",
            "Goal": "Summarise real logs and propose evidence-based fixes.",
            "Status": "Planned",
        },
    ])

    st.dataframe(roadmap, use_container_width=True, hide_index=True)

    st.markdown("### Export experiment")

    st.download_button(
        "⬇ Download complete experiment (CSV)",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="ghostload_full_experiment.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ============================= FOOTER ========================

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:16px 0 28px;">
        <div class="eyebrow">GHOSTLOAD / RESEARCH PROTOTYPE</div>
        <p class="small-muted">
            Cloud reliability · Failure recovery · AI workload observability
        </p>
        <p class="small-muted">
            All infrastructure and request metrics are simulated in this version.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
