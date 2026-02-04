# (Reusable visual blocks)

import plotly.graph_objects as go

def metric_card(title, value, delta=None):
    text = f"{value}"
    if delta is not None:
        text += f" ({delta:+})"

    return f"""
    <div style="padding:15px;border-radius:10px;background:#f5f5f5;margin-bottom:10px">
        <h4>{title}</h4>
        <h2>{text}</h2>
    </div>
    """

def comparison_chart(baseline, experimental):
    labels = ["Cycle Time", "Cost", "SLA Violations"]
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

    fig = go.Figure(data=[
        go.Bar(name="Baseline", x=labels, y=base_vals),
        go.Bar(name="After AI", x=labels, y=exp_vals)
    ])
    fig.update_layout(barmode="group")
    return fig
