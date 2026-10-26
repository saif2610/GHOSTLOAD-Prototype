
from __future__ import annotations

import random
from datetime import datetime
from typing import Any

import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="GHOSTLOAD | Reliability Lab",
    page_icon="🛰️",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ----------------------------- VISUAL DESIGN -----------------------------
st.markdown(
    """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

.stApp {
    color: #edf4ff;
    background:
        radial-gradient(ellipse at 8% 0%, rgba(40,116,170,.20), transparent 34%),
        radial-gradient(ellipse at 95% 8%, rgba(36,204,178,.12), transparent 30%),
        #070b13;
    font-family: 'Manrope', sans-serif;
}

[data-testid="stHeader"] {
    background: rgba(7,11,19,.78);
}

.block-container {
    max-width: 1480px;
    padding-top: 1.5rem;
    padding-bottom: 3rem;
}

section[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0b1422,#080d16);
    border-right: 1px solid rgba(125,170,220,.15);
}

.hero {
    position: relative;
    overflow: hidden;
    padding: 2.2rem;
    border-radius: 24px;
    border: 1px solid rgba(119,177,224,.24);
    background: linear-gradient(
        115deg,
        rgba(17,34,57,.96),
        rgba(10,19,32,.91) 62%,
        rgba(9,32,39,.88)
    );
    box-shadow: 0 18px 70px rgba(0,0,0,.18);
    margin-bottom: 1.5rem;
    animation: riseIn .75s ease both;
}

.hero:before {
    content: '';
    position: absolute;
    inset: -80% -20%;
    background: conic-gradient(
        from 0deg,
        transparent,
        rgba(84,224,211,.08),
        transparent 28%
    );
    animation: orbitGlow 16s linear infinite;
    pointer-events: none;
}

.hero-content {
    position: relative;
    z-index: 1;
}

.eyebrow {
    color: #67e3d4;
    font: 500 .72rem 'DM Mono', monospace;
    letter-spacing: .2em;
    text-transform: uppercase;
}

.hero h1 {
    font-size: clamp(2.5rem, 6vw, 4.5rem);
    letter-spacing: -.065em;
    line-height: 1.05;
    margin: .5rem 0 .8rem;
    color: #f4f8ff;
    font-weight: 800;
}

.hero h1 span {
    color: #68e1d4;
}

.hero p {
    color: #b5c8dd;
    max-width: 720px;
    font-size: 1rem;
    line-height: 1.8;
}

.hero-meta {
    display: flex;
    gap: .6rem;
    flex-wrap: wrap;
    margin-top: 1.3rem;
}

.pill {
    display: inline-block;
    padding: .4rem .7rem;
    border-radius: 999px;
    border: 1px solid rgba(135,180,220,.2);
    background: rgba(7,15,25,.5);
    color: #c4d5e7;
    font: .72rem 'DM Mono', monospace;
}

.section-kicker {
    color: #68e1d4;
    font: 500 .7rem 'DM Mono', monospace;
    letter-spacing: .16em;
    text-transform: uppercase;
    margin-bottom: .4rem;
}

.glass-card {
    border: 1px solid rgba(130,170,214,.17);
    border-radius: 17px;
    padding: 1rem 1.05rem;
    background: linear-gradient(
        145deg,
        rgba(18,30,47,.88),
        rgba(11,19,31,.8)
    );
    min-height: 125px;
    transition: transform .22s ease, border-color .22s ease;
    animation: riseIn .55s ease both;
}

.glass-card:hover {
    transform: translateY(-3px);
    border-color: rgba(96,225,212,.45);
}

.metric-label {
    color: #8fa8c2;
    font-size: .78rem;
}

.metric-value {
    color: #f4f8ff;
    font-size: 2rem;
    font-weight: 800;
    letter-spacing: -.05em;
    margin: .25rem 0;
}

.metric-foot {
    color: #829bb5;
    font-size: .73rem;
}

.info-card {
    border: 1px solid rgba(130,170,214,.16);
    border-radius: 16px;
    background: rgba(14,24,38,.68);
    padding: 1rem 1.1rem;
}

.stButton button,
.stDownloadButton button {
    border-radius: 11px !important;
    min-height: 2.7rem;
    font-weight: 700 !important;
    transition: transform .18s ease !important;
}

.stButton button:hover,
.stDownloadButton button:hover {
    transform: translateY(-2px);
}

.stButton button[kind="primary"] {
    background: linear-gradient(100deg,#69e5d6,#8cebd6) !important;
    color: #07131b !important;
    border: 0 !important;
}

[data-testid="stMetric"] {
    background: rgba(17,28,44,.72);
    border: 1px solid rgba(130,170,214,.16);
    padding: 13px 16px;
    border-radius: 14px;
}

hr {
    border-color: rgba(130,170,214,.14);
}

footer {
    visibility: hidden;
}

@keyframes riseIn {
    from {
        opacity: 0;
        transform: translateY(12px);
    }
    to {
        opacity: 1;
        transform: translateY(0);
    }
}

@keyframes orbitGlow {
    to {
        transform: rotate(360deg);
    }
}

@media (prefers-reduced-motion: reduce) {
    *, *::before, *::after {
        animation: none !important;
        transition: none !important;
    }
}
</style>
""",
    unsafe_allow_html=True,
)

# ----------------------------- SIMULATION ENGINE -----------------------------
def simulate_run(
    order_count: int,
    traffic_level: str,
    outage_probability: float,
    latency_ms: int,
    retry_mode: str,
    idempotency: bool,
    seed: int,
) -> pd.DataFrame:
    """Generate reproducible synthetic transaction records."""

    rng = random.Random(seed)

    traffic_factors = {
        "Low": 0.75,
        "Moderate": 1.0,
        "High": 1.55,
    }

    retry_limits = {
        "No retries": 0,
        "One retry": 1,
        "Up to 2 retries": 2,
    }

    traffic_factor = traffic_factors[traffic_level]
    retry_limit = retry_limits[retry_mode]
    rows: list[dict[str, Any]] = []

    for i in range(1, order_count + 1):
        base_latency = max(
            35,
            int(rng.gauss(230 * traffic_factor, 65 * traffic_factor)),
        )

        outage = rng.random() < outage_probability

        timeout_chance = min(
            0.70,
            max(0.0, (base_latency + latency_ms - 650) / 2100),
        )

        timeout = outage or rng.random() < timeout_chance

        retries = retry_limit if timeout else 0
        attempts = 1 + retries

        if not timeout:
            recovered = True
        elif retry_limit == 0:
            recovered = False
        else:
            recovery_chance = {1: 0.70, 2: 0.86}[retry_limit]
            recovered = rng.random() < recovery_chance

        status = "Completed" if recovered else "Failed"

        final_latency = (
            base_latency
            + latency_ms
            + sum(rng.randint(150, 420) for _ in range(retries))
        )

        duplicate = False

        if recovered and retries > 0 and not idempotency:
            duplicate_chance = min(
                0.55,
                0.13 * retries + outage_probability * 0.55,
            )
            duplicate = rng.random() < duplicate_chance

        rows.append({
            "Transaction": f"ORD-{i:04d}",
            "Traffic": traffic_level,
            "Simulated latency (ms)": int(final_latency),
            "Connection interruption": "Yes" if outage else "No",
            "Attempts": attempts,
            "Status": status,
            "Duplicate risk": (
                "Detected" if duplicate else "None detected"
            ),
            "Idempotency protection": (
                "On" if idempotency else "Off"
            ),
        })

    return pd.DataFrame(rows)


def metric_card(label: str, value: str, foot: str) -> str:
    return (
        "<div class='glass-card'>"
        f"<div class='metric-label'>{label}</div>"
        f"<div class='metric-value'>{value}</div>"
        f"<div class='metric-foot'>{foot}</div>"
        "</div>"
    )


def get_metrics(frame: pd.DataFrame) -> dict[str, float | int]:
    total = len(frame)

    completed = int((frame["Status"] == "Completed").sum())
    failed = total - completed
    duplicates = int(
        (frame["Duplicate risk"] == "Detected").sum()
    )

    average_latency = (
        float(frame["Simulated latency (ms)"].mean())
        if total else 0.0
    )

    p95_latency = (
        float(frame["Simulated latency (ms)"].quantile(0.95))
        if total else 0.0
    )

    return {
        "total": total,
        "completed": completed,
        "failed": failed,
        "duplicates": duplicates,
        "success_rate": (
            100 * completed / total if total else 0.0
        ),
        "average_latency": average_latency,
        "p95_latency": p95_latency,
    }


# ----------------------------- SIDEBAR CONTROLS -----------------------------
with st.sidebar:
    st.markdown(
        "<div class='eyebrow'>SYSTEM CONTROL</div>",
        unsafe_allow_html=True,
    )

    st.markdown("# 🛰️ GHOSTLOAD")
    st.caption("Workflow resilience • Research prototype")
    st.divider()

    st.markdown("### Configure an experiment")

    order_count = st.slider(
        "Simulated transactions",
        min_value=25,
        max_value=500,
        value=150,
        step=25,
    )

    traffic_level = st.select_slider(
        "Traffic intensity",
        options=["Low", "Moderate", "High"],
        value="Moderate",
    )

    outage_pct = st.slider(
        "Connection interruption chance",
        min_value=0,
        max_value=60,
        value=15,
        step=5,
    )

    latency_ms = st.slider(
        "Added network latency",
        min_value=0,
        max_value=2000,
        value=250,
        step=50,
        help="Synthetic latency added to each simulated request.",
    )

    retry_mode = st.selectbox(
        "Retry policy",
        ["No retries", "One retry", "Up to 2 retries"],
    )

    idempotency = st.toggle(
        "Enable idempotency protection",
        value=True,
        help="Models protection against repeated side effects on retries.",
    )

    seed = st.number_input(
        "Experiment seed",
        min_value=1,
        max_value=99999,
        value=42,
        step=1,
    )

    run_button = st.button(
        "▶ RUN EXPERIMENT",
        type="primary",
        use_container_width=True,
    )

    reset_button = st.button(
        "Reset to default settings",
        use_container_width=True,
    )

    st.divider()

    st.markdown(
        "<span class='pill'>LOCAL SYNTHETIC MODE</span>",
        unsafe_allow_html=True,
    )

    st.caption(
        "No live service is contacted. This prototype does not change "
        "your network or create real transactions."
    )


if reset_button:
    st.session_state.clear()
    st.rerun()


# ----------------------------- HERO HEADER -----------------------------
st.markdown(
    """
<div class="hero">
  <div class="hero-content">
    <div class="eyebrow">RELIABILITY ENGINEERING · PROTOTYPE 0.2</div>
    <h1>GHOST<span>LOAD</span></h1>
    <p>
      Stress the workflow. Expose the weak points. Measure what happens
      when connectivity gets unreliable.
    </p>
    <div class="hero-meta">
      <span class="pill">FAULT SIMULATION</span>
      <span class="pill">RETRY ANALYSIS</span>
      <span class="pill">TRANSACTION INTEGRITY</span>
      <span class="pill">REPRODUCIBLE RUNS</span>
    </div>
  </div>
</div>
""",
    unsafe_allow_html=True,
)


# ----------------------------- RUN EXPERIMENT -----------------------------
if "results" not in st.session_state:
    st.session_state.results = None

if "run_meta" not in st.session_state:
    st.session_state.run_meta = None

if run_button or st.session_state.results is None:
    with st.spinner("Running synthetic fault scenarios..."):
        generated = simulate_run(
            order_count=order_count,
            traffic_level=traffic_level,
            outage_probability=outage_pct / 100.0,
            latency_ms=latency_ms,
            retry_mode=retry_mode,
            idempotency=idempotency,
            seed=int(seed),
        )

        st.session_state.results = generated

        st.session_state.run_meta = {
            "transactions": order_count,
            "traffic": traffic_level,
            "outage": outage_pct,
            "latency": latency_ms,
            "retry": retry_mode,
            "idempotency": idempotency,
            "timestamp": datetime.now().strftime(
                "%Y-%m-%d %H:%M:%S"
            ),
            "seed": int(seed),
        }


df = st.session_state.results
meta = st.session_state.run_meta or {}
metrics = get_metrics(df)


# ----------------------------- WORKSPACE TABS -----------------------------
st.markdown(
    "<div class='section-kicker'>LIVE WORKSPACE</div>",
    unsafe_allow_html=True,
)

tab_overview, tab_evidence, tab_compare, tab_method = st.tabs([
    "◈ Command overview",
    "▤ Transaction evidence",
    "⇄ Strategy comparison",
    "ⓘ Research notes",
])


# ----------------------------- OVERVIEW -----------------------------
with tab_overview:
    st.markdown("### Experiment snapshot")

    st.caption(
        "Synthetic results only. Change controls in the sidebar "
        "and run another experiment to update the results."
    )

    c1, c2, c3, c4 = st.columns(4, gap="medium")

    with c1:
        st.markdown(
            metric_card(
                "COMPLETION RATE",
                f"{metrics['success_rate']:.1f}%",
                f"{metrics['completed']:,} completed",
            ),
            unsafe_allow_html=True,
        )

    with c2:
        st.markdown(
            metric_card(
                "FAILED TRANSACTIONS",
                f"{metrics['failed']:,}",
                f"{100 * metrics['failed'] / metrics['total']:.1f}% "
                "of simulated total",
            ),
            unsafe_allow_html=True,
        )

    with c3:
        st.markdown(
            metric_card(
                "DUPLICATE FLAGS",
                f"{metrics['duplicates']:,}",
                "Potential repeated side effects",
            ),
            unsafe_allow_html=True,
        )

    with c4:
        st.markdown(
            metric_card(
                "AVG. LATENCY",
                f"{metrics['average_latency']:,.0f} ms",
                f"95th percentile: {metrics['p95_latency']:,.0f} ms",
            ),
            unsafe_allow_html=True,
        )

    st.markdown("### Outcome telemetry")

    chart_col, notes_col = st.columns(
        [1.15, 0.85],
        gap="large",
    )

    with chart_col:
        outcome = (
            df["Status"]
            .value_counts()
            .reindex(["Completed", "Failed"], fill_value=0)
            .rename_axis("Outcome")
            .reset_index(name="Transactions")
        )

        st.bar_chart(
            outcome.set_index("Outcome"),
            height=265,
            use_container_width=True,
        )

    with notes_col:
        st.markdown(
            "<div class='info-card'>"
            "<div class='section-kicker'>AUTOMATED OBSERVATIONS</div>",
            unsafe_allow_html=True,
        )

        if metrics["failed"]:
            st.warning(
                f"{metrics['failed']} transaction(s) failed in this "
                "synthetic run. Compare retry policies to study recovery."
            )
        else:
            st.success(
                "All simulated transactions completed in this run. "
                "Try increasing the interruption chance."
            )

        if metrics["duplicates"]:
            st.error(
                f"{metrics['duplicates']} completed transaction(s) "
                "were flagged for possible duplicate side effects."
            )
        elif (
            not bool(meta.get("idempotency", True))
            and meta.get("retry") != "No retries"
        ):
            st.info(
                "No duplicate flags appeared in this sample, but "
                "retries without idempotency can still be risky."
            )
        else:
            st.info(
                "No duplicate side effects were generated in this sample. "
                "This does not prove real-world safety."
            )

        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("### Run configuration")

    if meta:
        a, b, c = st.columns(3)

        a.markdown(
            f"**Transactions:** {meta.get('transactions', '—')}  \n"
            f"**Traffic intensity:** {meta.get('traffic', '—')}  \n"
            f"**Random seed:** `{meta.get('seed', '—')}`"
        )

        b.markdown(
            f"**Interruption chance:** {meta.get('outage', '—')}%  \n"
            f"**Added latency:** {meta.get('latency', '—')} ms"
        )

        c.markdown(
            f"**Retry policy:** {meta.get('retry', '—')}  \n"
            f"**Idempotency:** "
            f"{'Enabled' if meta.get('idempotency') else 'Disabled'}"
        )

        st.caption(
            f"Last experiment: {meta.get('timestamp', '—')}"
        )


# ----------------------------- TRANSACTION EVIDENCE -----------------------------
with tab_evidence:
    st.markdown("### Transaction-level evidence")

    st.write(
        "Inspect generated records, filter potential failure modes, "
        "and export the experiment results."
    )

    f1, f2, f3 = st.columns([1, 1, 1.4])

    with f1:
        selected_status = st.multiselect(
            "Outcome",
            ["Completed", "Failed"],
            default=["Completed", "Failed"],
        )

    with f2:
        duplicate_filter = st.selectbox(
            "Duplicate risk",
            ["All records", "Detected only", "None detected"],
        )

    with f3:
        search_text = st.text_input(
            "Find transaction ID",
            placeholder="e.g. ORD-0012",
        )

    evidence = df[df["Status"].isin(selected_status)]

    if duplicate_filter == "Detected only":
        evidence = evidence[
            evidence["Duplicate risk"] == "Detected"
        ]
    elif duplicate_filter == "None detected":
        evidence = evidence[
            evidence["Duplicate risk"] == "None detected"
        ]

    if search_text.strip():
        evidence = evidence[
            evidence["Transaction"].str.contains(
                search_text.strip(),
                case=False,
                na=False,
            )
        ]

    st.caption(f"Showing {len(evidence):,} of {len(df):,} records")

    st.dataframe(
        evidence,
        use_container_width=True,
        hide_index=True,
        height=360,
    )

    csv_data = df.to_csv(index=False).encode("utf-8")

    st.download_button(
        "⬇ Download full transaction evidence (CSV)",
        data=csv_data,
        file_name="ghostload_simulation_results.csv",
        mime="text/csv",
        use_container_width=True,
    )

    st.markdown("### Latency profile")

    st.line_chart(
        df.set_index("Transaction")[["Simulated latency (ms)"]],
        height=260,
        use_container_width=True,
    )


# ----------------------------- STRATEGY COMPARISON -----------------------------
with tab_compare:
    st.markdown("### Compare retry and integrity strategies")

    st.caption(
        "Each strategy uses the same experiment seed and settings "
        "to make the synthetic comparison reproducible."
    )

    strategies = [
        ("No retries · no guard", "No retries", False),
        ("One retry · no guard", "One retry", False),
        ("Up to 2 retries · no guard", "Up to 2 retries", False),
        ("Up to 2 retries · idempotency", "Up to 2 retries", True),
    ]

    comparison_rows: list[dict[str, Any]] = []

    for label, strategy_retry, strategy_idempotency in strategies:
        strategy_df = simulate_run(
            order_count=int(meta.get("transactions", order_count)),
            traffic_level=str(meta.get("traffic", traffic_level)),
            outage_probability=float(
                meta.get("outage", outage_pct)
            ) / 100.0,
            latency_ms=int(meta.get("latency", latency_ms)),
            retry_mode=strategy_retry,
            idempotency=strategy_idempotency,
            seed=int(meta.get("seed", seed)),
        )

        strategy_metrics = get_metrics(strategy_df)

        comparison_rows.append({
            "Strategy": label,
            "Completion rate (%)": round(
                float(strategy_metrics["success_rate"]), 1
            ),
            "Failed": int(strategy_metrics["failed"]),
            "Duplicate flags": int(strategy_metrics["duplicates"]),
            "Average latency (ms)": round(
                float(strategy_metrics["average_latency"])
            ),
        })

    comparison_df = pd.DataFrame(comparison_rows)

    st.dataframe(
        comparison_df,
        use_container_width=True,
        hide_index=True,
    )

    st.markdown("### Completion rate by strategy")

    st.bar_chart(
        comparison_df.set_index("Strategy")[["Completion rate (%)"]],
        height=280,
        use_container_width=True,
    )

    st.info(
        "This is a simplified model for exploring trade-offs, not a "
        "benchmark of production systems. Real-world testing is required."
    )


# ----------------------------- RESEARCH NOTES -----------------------------
with tab_method:
    st.markdown("### What this prototype does")

    left, right = st.columns(2, gap="large")

    with left:
        st.markdown(
            """
<div class="info-card">
<h4>Included in this version</h4>
<ul>
<li>Reproducible synthetic transaction runs</li>
<li>Configurable interruption probability and added latency</li>
<li>Retry-policy comparison</li>
<li>Potential duplicate-side-effect flags</li>
<li>Transaction evidence and CSV export</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    with right:
        st.markdown(
            """
<div class="info-card">
<h4>Not included yet</h4>
<ul>
<li>No live AI API integration</li>
<li>No real network impairment or packet loss</li>
<li>No persistent transaction database</li>
<li>No validated production-reliability claims</li>
<li>No proof of research novelty</li>
</ul>
</div>
""",
            unsafe_allow_html=True,
        )

    st.markdown("### Proposed research question")

    st.info(
        "How effectively can a controlled failure-testing framework "
        "detect transaction-integrity and recovery failures in AI-assisted "
        "workflows under intermittent network connectivity?"
    )

    st.markdown("### Next engineering milestone")

    st.markdown(
        "Build a local test API and persistent transaction store. "
        "Add controlled request interruption, idempotency keys, and "
        "repeatable tests. Then measure missing or duplicate transactions, "
        "recovery time, median latency, and 95th-percentile latency."
    )

    st.markdown("### Candidate measurements")

    st.markdown(
        "- Transaction completion rate (%)\n"
        "- Missing or duplicate transaction count\n"
        "- Recovery time after an interruption\n"
        "- Median and 95th-percentile response latency\n"
        "- Difference between baseline and improved implementations"
    )


# ----------------------------- FOOTER -----------------------------
st.divider()

st.markdown(
    """
<div style="
    display:flex;
    justify-content:space-between;
    gap:1rem;
    flex-wrap:wrap;
    color:#7f94ad;
    font-size:.75rem;
">
    <span style="font-family:monospace">
        GHOSTLOAD / RELIABILITY LAB / 0.2
    </span>
    <span>
        Synthetic data only · Validate with controlled experiments.
    </span>
</div>
""",
    unsafe_allow_html=True,
)
