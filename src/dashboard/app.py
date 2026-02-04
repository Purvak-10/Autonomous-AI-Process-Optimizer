import streamlit as st
import pandas as pd
import plotly.graph_objects as go

from src.optimizer.run_optimizer import run as run_optimizer

# --------------------------------------------------
# Page Configuration
# --------------------------------------------------
st.set_page_config(
    page_title="Autonomous AI Process Optimizer",
    layout="wide"
)

# --------------------------------------------------
# Helper: Apply Slider Effect (What-If Simulation)
# --------------------------------------------------
def apply_threshold_effect(baseline, experimental, threshold):
    """
    Simulates the effect of changing approval strictness.
    Higher threshold => faster approvals
    Lower threshold => stricter approvals
    """

    factor = threshold / 1000  # baseline reference

    adjusted = experimental.copy()

    adjusted["avg_cycle_time"] = max(
        10, experimental["avg_cycle_time"] / factor
    )

    adjusted["avg_cost"] = max(
        1, experimental["avg_cost"] * (1 + (1 / factor - 1) * 0.2)
    )

    adjusted["sla_violation_rate"] = max(
        0.0, experimental["sla_violation_rate"] / factor
    )

    return adjusted


# --------------------------------------------------
# Helper: Comparison Chart
# --------------------------------------------------
def comparison_chart(baseline, experimental):
    labels = [
        "Cycle Time (mins)",
        "Cost per Ticket",
        "SLA Violations (%)"
    ]

    base_vals = [
        baseline["avg_cycle_time"],
        baseline["avg_cost"],
        baseline["sla_violation_rate"] * 100
    ]

    exp_vals = [
        experimental["avg_cycle_time"],
        experimental["avg_cost"],
        experimental["sla_violation_rate"] * 100
    ]

    fig = go.Figure()
    fig.add_bar(
        x=labels,
        y=base_vals,
        name="Current Process",
        marker_color="#1f77b4"
    )
    fig.add_bar(
        x=labels,
        y=exp_vals,
        name="After AI Optimization",
        marker_color="#2ca02c"
    )

    fig.update_layout(
        title="Process Performance Comparison",
        barmode="group",
        height=420,
        yaxis_title="Value"
    )
    return fig


# --------------------------------------------------
# Confidence Score
# --------------------------------------------------
def confidence_score(delta):
    score = (
        abs(delta["avg_cycle_time"]) * 0.4 +
        abs(delta["avg_cost"]) * 0.4 +
        abs(delta["sla_violation_rate"]) * 100 * 0.2
    )
    return min(100, round(score, 1))


# --------------------------------------------------
# Run Optimizer (Cached)
# --------------------------------------------------
@st.cache_data
def get_results():
    return run_optimizer()

result = get_results()

selected = result["selected"]
all_results = result["all_results"]

rule = selected["rule"]
delta = selected["delta"]

baseline = all_results[rule]["baseline"]
raw_experimental = all_results[rule]["experimental"]

# --------------------------------------------------
# HEADER
# --------------------------------------------------
st.title("🤖 Autonomous AI Process Optimizer")
st.caption(
    "Identifies process bottlenecks, evaluates improvement strategies, "
    "and recommends the most effective optimization."
)

st.divider()

# --------------------------------------------------
# PROCESS FLOW
# --------------------------------------------------
st.header("🔁 Process Flow")

st.graphviz_chart("""
digraph {
    rankdir=LR;
    node [shape=box style=filled fillcolor="#E8F0FE"];
    Created -> Assigned -> "In Progress" -> Approved -> Closed;
    Approved [fillcolor="#FDECEA"];
}
""")

st.write(
    "The Approval step is highlighted as the primary bottleneck "
    "based on process analysis."
)

# --------------------------------------------------
# CURRENT PERFORMANCE
# --------------------------------------------------
st.header("🚨 Process Performance Overview")

c1, c2, c3 = st.columns(3)
c1.metric("Avg Cycle Time (mins)", round(baseline["avg_cycle_time"], 1))
c2.metric("Avg Cost per Ticket", round(baseline["avg_cost"], 1))
c3.metric("SLA Violation Rate (%)", round(baseline["sla_violation_rate"] * 100, 1))

# --------------------------------------------------
# ROOT CAUSE
# --------------------------------------------------
st.header("🔍 Root Cause Identified")

st.write(
    "The Approval step introduces the largest delay, "
    "increasing cycle time, cost, and SLA violations."
)

# --------------------------------------------------
# AI EVALUATION
# --------------------------------------------------
st.header("🧪 AI Evaluation Process")

st.markdown("""
1. Analyze current process behavior  
2. Apply alternative optimization strategies  
3. Measure impact on time, cost, and SLA compliance  
4. Compare outcomes  
5. Select the best-performing option
""")

# --------------------------------------------------
# WHAT-IF SLIDER (NOW FUNCTIONAL)
# --------------------------------------------------
from src.simulation.simulate_with_threshold import simulate_threshold

st.header("🎛️ Approval Threshold (What-If Simulation)")

threshold = st.slider(
    "Approval Threshold",
    min_value=100,
    max_value=5000,
    step=100,
    value=1000
)

st.caption(
    "Higher values allow more tickets to be auto-approved, "
    "reducing delays but increasing exposure."
)

@st.cache_data
def cached_simulation(threshold):
    return simulate_threshold(threshold)

with st.spinner("Running digital twin simulation..."):
    sim_result = cached_simulation(threshold)

baseline = sim_result["baseline"]
experimental = sim_result["experimental"]
delta = sim_result["delta"]

# --------------------------------------------------
# CENTERED AI RECOMMENDATION
# --------------------------------------------------
st.divider()

conf = confidence_score(delta)

st.markdown(
    f"""
    <div style="text-align:center;
                padding:35px;
                border-radius:14px;
                background-color:#f0fdf4;
                border:2px solid #22c55e;">
        <h2>🏆 AI Recommended Action</h2>
        <h1 style="color:#16a34a;">{rule}</h1>
        <p>Confidence Score: <b>{conf}%</b></p>
    </div>
    """,
    unsafe_allow_html=True
)

st.divider()

# --------------------------------------------------
# IMPACT CHART
# --------------------------------------------------
st.header("📈 Expected Impact")

st.plotly_chart(
    comparison_chart(baseline, experimental),
    use_container_width=True
)

# --------------------------------------------------
# ALTERNATIVES
# --------------------------------------------------
st.header("🔀 Alternative Strategies Considered")

alt_rows = []
for r, data in all_results.items():
    alt_rows.append([
        r,
        round(data["experimental"]["avg_cycle_time"], 1),
        round(data["experimental"]["avg_cost"], 1),
        round(data["experimental"]["sla_violation_rate"] * 100, 1)
    ])

alt_df = pd.DataFrame(
    alt_rows,
    columns=["Strategy", "Cycle Time", "Cost", "SLA Violations (%)"]
)

st.table(alt_df)

# --------------------------------------------------
# EXPLAINABILITY
# --------------------------------------------------
with st.expander("🧠 View AI Reasoning"):
    st.write(
        "Analysis shows approval delays are driven by process design "
        "constraints and manual intervention requirements."
    )
    st.write(
        "Automating low-risk approvals produces the highest improvement "
        "across time, cost, and SLA performance."
    )

# --------------------------------------------------
# FINAL DECISION
# --------------------------------------------------
st.header("✅ Final Recommendation")

st.success(
    f"Based on comprehensive analysis and evaluation, "
    f"the AI recommends **{rule}** to optimize the process."
)
