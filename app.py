
# ============================================================
# GHOSTLOAD — Cloud Reliability & AI Workload Observatory
# Complete Streamlit application
# ============================================================

import random
import time
from datetime import datetime

import pandas as pd
import streamlit as st


# ------------------------- PAGE SETUP -------------------------

st.set_page_config(
    page_title="GHOSTLOAD | Cloud Observatory",
    page_icon="☁️",
    layout="wide",
    initial_sidebar_state="expanded",
)


# ------------------------- DESIGN SYSTEM ---------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Space+Grotesk:wght@400;500;600;700&display=swap');

:root {
    --bg: #080b12;
    --panel: #101621;
    --panel2: #141d2b;
    --border: #263348;
    --cyan: #55e6ef;
    --blue: #7599ff;
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
    background: rgba(8, 11, 18, 0.75);
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
    font-weight: 700;
}

.eyebrow {
    color: var(--cyan);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 2px;
    text-transform: uppercase;
}

.hero {
    padding: 32px;
    border: 1px solid #294052;
    border-radius: 22px;
    background:
        linear-gradient(120deg, rgba(24, 46, 64, .94),
        rgba(12, 18, 30, .97) 60%, rgba(17, 36, 47, .9));
    position: relative;
    overflow: hidden;
    animation: appear .7s ease-out;
    margin-bottom: 24px;
}

.hero:after {
    content: "";
    position: absolute;
    right: -90px;
    top: -130px;
    width: 310px;
    height: 310px;
    border: 1px solid rgba(85, 230, 239, .25);
    border-radius: 50%;
    box-shadow:
        0 0 0 28px rgba(85,230,239,.025),
        0 0 0 58px rgba(85,230,239,.02),
        0 0 90px rgba(85,230,239,.09);
    pointer-events: none;
}

.hero-title {
    font-size: clamp(36px, 5vw, 62px);
    font-weight: 700;
    letter-spacing: -3px;
    line-height: 1;
    margin: 14px 0;
}

.hero-title span {
    color: var(--cyan);
}

.hero-subtitle {
    color: #b3c2d6;
    max-width: 650px;
    font-size: 15px;
    line-height: 1.7;
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
    font-size: 12px;
    text-transform: uppercase;
    letter-spacing: 1px;
}

.metric-value {
    font-family: 'DM Mono', monospace;
    font-size: 29px;
    color: var(--white);
    font-weight: 500;
    margin: 9px 0 4px;
}

.metric-note {
    color: var(--cyan);
    font-size: 12px;
}

.section-label {
    color: var(--cyan);
    font-family: 'DM Mono', monospace;
    font-size: 11px;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 8px;
}

.small-muted {
    color: var(--muted);
    font-size: 13px;
    line-height: 1.65;
}

.status-pill {
    display: inline-block;
    padding: 5px 10px;
    border-radius: 999px;
    border: 1px solid #315364;
    color: var(--cyan);
    background: rgba(85,230,239,.06);
    font-family: 'DM Mono', monospace;
    font-size: 10px;
    letter-spacing: 1px;
}

.node {
    display: inline-block;
    border: 1px solid #2e5066;
    background: #101e2c;
    padding: 10px 13px;
    border-radius: 10px;
    color: #dcecff;
    font-size: 12px;
    text-align: center;
    min-width: 100px;
}

.node-line {
    color: var(--cyan);
    text-align: center;
    font-size: 20px;
    padding: 3px;
}

div[data-testid="stMetric"] {
    background: #101824;
    border: 1px solid var(--border);
    padding: 14px;
    border-radius: 13px;
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
    box-shadow: 0 0 18px rgba(85,230,239,.13);
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

hr {
    border-color: var(--border);
}

@keyframes appear {
    from { opacity: 0; transform: translateY(10px); }
    to { opacity: 1; transform: translateY(0); }
}

@media (prefers-reduced-motion: reduce) {
    * {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""", unsafe_allow_html=True)


# ------------------------- HELPERS ---------------------------

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


def run_simulation(
    request_count,
    interruption_probability,
    base_latency,
    max_retries,
    idempotency,
    seed,
):
    """Simulate request outcomes. This does not send real network requests."""

    rng = random.Random(seed)
    records = []

    for request_id in range(1, request_count + 1):
        attempts = 0
        duplicate_operations = 0
        completed = False
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
                completed = True
                final_status = "SUCCESS"
                failure_reason = ""
                break

            # Sometimes the server processes a request but the response
            # is lost. Retrying can then repeat the operation.
            server_processed = rng.random() < 0.55

            if server_processed:
                response_lost = True

                if attempt < max_retries:
                    if not idempotency:
                        duplicate_operations += 1
                    continue

                # The operation may have happened, but the client
                # never received a successful response.
                final_status = "UNKNOWN"
                failure_reason = "Response lost; processing uncertain"
                break

            # The request did not complete on the server.
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
            "success_rate": 0,
            "failure_rate": 0,
            "unknown_rate": 0,
            "duplicates": 0,
            "avg_latency": 0,
            "avg_attempts": 0,
        }

    successes = int((data["Status"] == "SUCCESS").sum())
    failures = int((data["Status"] == "FAILED").sum())
    unknown = int((data["Status"] == "UNKNOWN").sum())

    return {
        "success_rate": successes / total * 100,
        "failure_rate": failures / total * 100,
        "unknown_rate": unknown / total * 100,
        "duplicates": int(data["Duplicate Operations"].sum()),
        "avg_latency": float(data["Latency (ms)"].mean()),
        "avg_attempts": float(data["Attempts"].mean()),
    }


def make_strategy_table(count, interruption, latency, seed):
    """Compare retry and idempotency strategies using common settings."""

    strategies = [
        ("No retries", 0, False),
        ("One retry", 1, False),
        ("Two retries", 2, False),
        ("Two retries + idempotency", 2, True),
    ]

    results = []

    for name, retries, idem in strategies:
        data = run_simulation(
            request_count=count,
            interruption_probability=interruption,
            base_latency=latency,
            max_retries=retries,
            idempotency=idem,
            seed=seed,
        )

        m = calculate_metrics(data)

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


# ------------------------- SIDEBAR ---------------------------

with st.sidebar:
    st.markdown(
        '<div class="eyebrow">GHOSTLOAD / CONTROL DECK</div>',
        unsafe_allow_html=True,
    )

    st.markdown("## Experiment setup")
    st.caption("Configure the simulated test environment.")

    request_count = st.slider(
        "Number of requests",
        min_value=100,
        max_value=5000,
        value=1000,
        step=100,
    )

    interruption_probability = st.slider(
        "Connection interruption probability",
        min_value=0.0,
        max_value=0.8,
        value=0.15,
        step=0.05,
        format="%.2f",
        help="Probability that an individual request attempt is interrupted.",
    )

    base_latency = st.slider(
        "Base request latency (ms)",
        min_value=20,
        max_value=1000,
        value=120,
        step=20,
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
        help=(
            "Models a safeguard that prevents a retried operation "
            "from being applied more than once."
        ),
    )

    seed = st.number_input(
        "Experiment seed",
        min_value=1,
        max_value=999999,
        value=42,
        step=1,
    )

    st.divider()

    st.markdown("### Test profile")
    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Execution mode</div>
            <div style="font-size:15px;font-weight:600;">
                Local simulation
            </div>
            <p class="small-muted">
                No real requests, payments, or cloud services are affected.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if st.button("↻ Generate new experiment", use_container_width=True):
        st.session_state["experiment_seed"] = (
            int(st.session_state.get("experiment_seed", seed)) + 1
        )
        st.rerun()


# Keep experiment data stable between normal Streamlit reruns.
effective_seed = int(st.session_state.get("experiment_seed", seed))

if st.session_state.get("last_seed") != effective_seed:
    st.session_state["last_seed"] = effective_seed

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


# ------------------------- HEADER ----------------------------

st.markdown(
    """
    <div class="hero">
        <div class="eyebrow">CLOUD RELIABILITY / AI WORKLOADS / RESILIENCE</div>
        <div class="hero-title">GHOST<span>LOAD</span></div>
        <div class="hero-subtitle">
            A cloud reliability observatory for exploring service failures,
            request recovery, workload pressure, and the behaviour of
            retry strategies in controlled experiments.
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


# ------------------------- TABS ------------------------------

overview, evidence, strategy, cloud, methodology = st.tabs([
    "◈  Overview",
    "▤  Request evidence",
    "⇄  Strategy lab",
    "☁  Cloud lab",
    "ⓘ  Methodology",
])


# ============================================================
# TAB 1: OVERVIEW
# ============================================================

with overview:
    st.markdown("## System overview")
    st.caption(
        "A quick view of the current simulated reliability experiment."
    )

    a, b, c, d = st.columns(4)

    with a:
        metric_card(
            "Successful requests",
            f"{metrics['success_rate']:.1f}%",
            "Final status = SUCCESS",
        )

    with b:
        metric_card(
            "Failed requests",
            f"{metrics['failure_rate']:.1f}%",
            "Final status = FAILED",
        )

    with c:
        metric_card(
            "Average latency",
            f"{metrics['avg_latency']:.0f} ms",
            "Total simulated request time",
        )

    with d:
        metric_card(
            "Duplicate operations",
            f"{metrics['duplicates']:,}",
            "Modelled repeated processing",
        )

    st.write("")

    left, right = st.columns([1.35, 1])

    with left:
        st.markdown("### Request outcome distribution")

        outcome_counts = (
            data["Status"]
            .value_counts()
            .reindex(["SUCCESS", "FAILED", "UNKNOWN"], fill_value=0)
        )

        outcome_df = pd.DataFrame({
            "Outcome": outcome_counts.index,
            "Requests": outcome_counts.values,
        }).set_index("Outcome")

        st.bar_chart(outcome_df, height=300)

    with right:
        st.markdown("### Current configuration")

        st.markdown(
            f"""
            <div class="panel">
                <div class="section-label">Network model</div>
                <div class="metric-value" style="font-size:22px;">
                    {interruption_probability * 100:.0f}%
                </div>
                <p class="small-muted">Interruption probability per attempt</p>
                <hr>
                <div class="section-label">Retry policy</div>
                <div style="font-size:18px;font-weight:600;">
                    {max_retries} retries
                </div>
                <hr>
                <div class="section-label">Idempotency protection</div>
                <div style="font-size:18px;font-weight:600;">
                    {"Enabled" if idempotency else "Disabled"}
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown("### Request latency profile")

    latency_df = data[["Request ID", "Latency (ms)"]].copy()
    latency_df["Request number"] = range(1, len(latency_df) + 1)

    st.line_chart(
        latency_df.set_index("Request number")[["Latency (ms)"]],
        height=260,
    )

    st.markdown("### Request processing flow")

    flow1, flow2, flow3, flow4 = st.columns(4)

    with flow1:
        st.markdown(
            '<div class="node">01<br>Request created</div>',
            unsafe_allow_html=True,
        )

    with flow2:
        st.markdown(
            '<div class="node">02<br>Failure simulated</div>',
            unsafe_allow_html=True,
        )

    with flow3:
        st.markdown(
            '<div class="node">03<br>Retry decision</div>',
            unsafe_allow_html=True,
        )

    with flow4:
        st.markdown(
            '<div class="node">04<br>Outcome recorded</div>',
            unsafe_allow_html=True,
        )

    st.info(
        "Interpretation: retries can improve the chance of receiving a "
        "successful response, but can add latency. Idempotency is modelled "
        "as protection against duplicate operations. These are simulated "
        "results, not measurements from a production system."
    )


# ============================================================
# TAB 2: REQUEST EVIDENCE
# ============================================================

with evidence:
    st.markdown("## Request-level evidence")
    st.caption(
        "Inspect individual simulated requests and export the experiment data."
    )

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

    st.markdown(
        f"**Showing {len(filtered):,} of {len(data):,} requests**"
    )

    st.dataframe(
        filtered,
        use_container_width=True,
        hide_index=True,
        height=420,
    )

    csv_data = filtered.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download filtered request evidence (CSV)",
        data=csv_data,
        file_name="ghostload_request_evidence.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("### Evidence summary")

    e1, e2, e3 = st.columns(3)

    with e1:
        st.metric("Requests in view", f"{len(filtered):,}")

    with e2:
        st.metric(
            "Response-loss events",
            int(filtered["Response Lost"].sum()) if len(filtered) else 0,
        )

    with e3:
        st.metric(
            "Duplicate operations",
            int(filtered["Duplicate Operations"].sum()) if len(filtered) else 0,
        )

    st.caption(
        "CSV exports contain generated experiment records only. "
        "They do not contain logs from a real server."
    )


# ============================================================
# TAB 3: STRATEGY LAB
# ============================================================

with strategy:
    st.markdown("## Recovery strategy lab")
    st.caption(
        "Compare retry policies under the same simulated interruption settings."
    )

    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Research question</div>
            <div style="font-size:18px;font-weight:600;">
                How do retries and idempotency affect request success,
                latency, and duplicate processing?
            </div>
            <p class="small-muted">
                All strategies use the same experiment seed and interruption
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

    success_chart = strategy_data[
        ["Strategy", "Success rate (%)"]
    ].set_index("Strategy")

    st.bar_chart(success_chart, height=300)

    st.markdown("### Latency comparison")

    latency_chart = strategy_data[
        ["Strategy", "Average latency (ms)"]
    ].set_index("Strategy")

    st.bar_chart(latency_chart, height=300)

    st.markdown("### Duplicate operation comparison")

    duplicate_chart = strategy_data[
        ["Strategy", "Duplicate operations"]
    ].set_index("Strategy")

    st.bar_chart(duplicate_chart, height=260)

    st.markdown("### How to interpret the results")

    st.markdown("""
    - **No retries:** Requests get one attempt. This avoids retry overhead
      but may leave more requests unsuccessful.
    - **More retries:** Give interrupted requests additional chances, but
      increase the number of attempts and potentially the total latency.
    - **Idempotency:** Models a server-side safeguard that recognises
      repeated operations and prevents duplicate effects.
    - **Unknown outcomes:** A request may have been processed even though
      the client never received its response.
    """)

    st.warning(
        "The comparison is a simplified model. Real systems require careful "
        "testing of timeouts, backoff, server-side idempotency, and actual "
        "service behaviour before drawing operational conclusions."
    )

    strategy_csv = strategy_data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download strategy comparison (CSV)",
        data=strategy_csv,
        file_name="ghostload_strategy_comparison.csv",
        mime="text/csv",
    )


# ============================================================
# TAB 4: CLOUD COMPUTING LAB
# ============================================================

with cloud:
    st.markdown("## Cloud infrastructure lab")
    st.caption(
        "Explore virtual server resources, AI workloads, and service pressure."
    )

    st.markdown(
        """
        <div class="panel">
            <div class="section-label">Cloud environment</div>
            <div style="font-size:23px;font-weight:700;">
                Compute · Network · AI workloads
            </div>
            <p class="small-muted">
                This module demonstrates the metrics a cloud observability
                platform could monitor. Values are generated locally and
                are not collected from cloud infrastructure.
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

    c1, c2, c3 = st.columns(3)

    with c1:
        metric_card("Service availability", f"{cloud_availability}%", "SIMULATED")
        st.progress(min(cloud_availability / 100, 1.0))

    with c2:
        metric_card("CPU utilization", f"{cloud_cpu}%", "SIMULATED")
        st.progress(cloud_cpu / 100)

    with c3:
        metric_card("Memory utilization", f"{cloud_memory}%", "SIMULATED")
        st.progress(cloud_memory / 100)

    c4, c5, c6 = st.columns(3)

    with c4:
        metric_card("GPU utilization", f"{cloud_gpu}%", "SIMULATED")
        st.progress(cloud_gpu / 100)

    with c5:
        metric_card("Cloud request latency", f"{cloud_latency} ms", "SIMULATED")

    with c6:
        metric_card("AI jobs waiting", f"{queued_jobs}", "SIMULATED")

    st.markdown("### Resource utilization")

    resource_df = pd.DataFrame({
        "Resource": ["CPU", "Memory", "GPU"],
        "Utilization (%)": [cloud_cpu, cloud_memory, cloud_gpu],
    }).set_index("Resource")

    st.bar_chart(resource_df, height=260)

    st.markdown("### Cloud workload simulator")

    workload = st.select_slider(
        "Select cloud workload pressure",
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
                "The scenario includes a simulated service interruption. "
                "No actual cloud service has been interrupted."
            )
        elif pressure >= 0.65:
            st.warning(
                "The model indicates elevated workload pressure. "
                "Real infrastructure would need to be measured to confirm it."
            )
        else:
            st.success(
                "The model indicates a relatively manageable workload."
            )

    st.markdown("### Cloud architecture concept")

    architecture = st.columns(5)

    architecture_labels = [
        ("01", "Client", "Sends requests"),
        ("02", "Cloud API", "Receives requests"),
        ("03", "Compute", "Processes work"),
        ("04", "Monitor", "Collects metrics"),
        ("05", "Recovery", "Handles failures"),
    ]

    for col, (number, title, description) in zip(
        architecture, architecture_labels
    ):
        with col:
            st.markdown(
                f"""
                <div class="panel" style="min-height:135px;">
                    <div class="section-label">{number}</div>
                    <div style="font-size:16px;font-weight:600;">
                        {title}
                    </div>
                    <p class="small-muted">{description}</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.info(
        "Cloud integration is a future development step. This prototype "
        "does not connect to AWS, Azure, Google Cloud, or real GPU servers."
    )


# ============================================================
# TAB 5: METHODOLOGY
# ============================================================

with methodology:
    st.markdown("## Research methodology")
    st.caption(
        "Understand the model, its assumptions, and its limitations."
    )

    st.markdown("### 1. What GHOSTLOAD tests")

    st.markdown("""
    GHOSTLOAD models what can happen when an application sends requests
    through an unreliable connection. It compares request outcomes under
    different retry policies and an idempotency-protection setting.
    """)

    st.markdown("### 2. Variables")

    variables = pd.DataFrame([
        {
            "Variable": "Request count",
            "Role": "Input",
            "Description": "Number of simulated requests.",
        },
        {
            "Variable": "Interruption probability",
            "Role": "Input",
            "Description": "Chance an attempt experiences an interruption.",
        },
        {
            "Variable": "Base latency",
            "Role": "Input",
            "Description": "Starting latency used by the simulation.",
        },
        {
            "Variable": "Retry policy",
            "Role": "Input",
            "Description": "Number of additional attempts permitted.",
        },
        {
            "Variable": "Idempotency",
            "Role": "Input",
            "Description": "Whether duplicate effects are modelled as prevented.",
        },
        {
            "Variable": "Success/failure rate",
            "Role": "Output",
            "Description": "Final status distribution of simulated requests.",
        },
        {
            "Variable": "Latency and duplicates",
            "Role": "Output",
            "Description": "Modelled time and repeated processing.",
        },
    ])

    st.dataframe(variables, use_container_width=True, hide_index=True)

    st.markdown("### 3. Model assumptions")

    st.markdown("""
    - Each attempt has an interruption probability selected in the sidebar.
    - Request latency is sampled around the configured base latency.
    - An interrupted request may have been processed even if its response
      is lost.
    - A retry without idempotency protection can create a duplicate effect
      in the model.
    - The idempotency setting represents a simplified safeguard; it is not
      a real database or server-side idempotency implementation.
    - The experiment seed makes the generated results reproducible for the
      same settings and software version.
    """)

    st.markdown("### 4. Limitations")

    st.markdown("""
    **This is a prototype, not a production monitoring platform.**

    - It does not send real HTTP requests.
    - It does not disconnect or modify your internet connection.
    - It does not connect to cloud providers or measure actual server health.
    - It does not run AI models or inspect real GPU workloads.
    - Its latency and failure distributions are simplified assumptions.
    - The reported success rate is a simulation result, not a service-level
      availability guarantee.
    """)

    st.markdown("### 5. Future development roadmap")

    roadmap = pd.DataFrame([
        {
            "Phase": "1",
            "Feature": "Current simulation engine",
            "Goal": "Explore retries, interruptions, and duplicate effects.",
            "Status": "Prototype",
        },
        {
            "Phase": "2",
            "Feature": "Local test API",
            "Goal": "Send test requests to a controlled FastAPI service.",
            "Status": "Planned",
        },
        {
            "Phase": "3",
            "Feature": "Persistent experiment database",
            "Goal": "Store and compare real test runs.",
            "Status": "Planned",
        },
        {
            "Phase": "4",
            "Feature": "Cloud telemetry integration",
            "Goal": "Collect authorised CPU, memory, and service metrics.",
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

    full_csv = data.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download complete experiment (CSV)",
        data=full_csv,
        file_name="ghostload_full_experiment.csv",
        mime="text/csv",
        use_container_width=True,
    )


# ------------------------- FOOTER ----------------------------

st.divider()

st.markdown(
    """
    <div style="text-align:center;padding:14px 0 24px;">
        <div class="eyebrow">GHOSTLOAD / RESEARCH PROTOTYPE</div>
        <p class="small-muted">
            Cloud reliability · Failure recovery · AI workload observability
        </p>
        <p class="small-muted">
            Demonstration software. All displayed infrastructure and request
            metrics are simulated unless a future version explicitly
            connects to a real test environment.
        </p>
    </div>
    """,
    unsafe_allow_html=True,
)
