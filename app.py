"""Streamlit dashboard for monitoring ROV operations."""
from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime, timedelta

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objs as go
import streamlit as st


st.set_page_config(
    page_title="ROV Operations Dashboard",
    page_icon="🤿",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _generate_sample_data(num_records: int = 120) -> pd.DataFrame:
    """Create synthetic telemetry data for demonstration purposes."""
    now = datetime.utcnow()
    timestamps = [now - timedelta(minutes=5 * i) for i in range(num_records)][::-1]
    base_depth = np.linspace(100, 350, num_records) + np.random.normal(0, 8, num_records)
    base_temperature = 4 + 0.005 * np.array(range(num_records)) + np.random.normal(0, 0.2, num_records)
    base_pressure = 1.3 * base_depth + np.random.normal(0, 5, num_records)

    df = pd.DataFrame(
        {
            "timestamp": timestamps,
            "depth_m": base_depth,
            "temperature_c": base_temperature,
            "pressure_kpa": base_pressure,
            "power_pct": np.clip(75 + np.random.normal(0, 4, num_records), 60, 95),
            "heading_deg": (180 + np.cumsum(np.random.normal(0, 1.5, num_records))) % 360,
            "speed_knots": np.clip(2.5 + np.random.normal(0, 0.3, num_records), 1.0, 3.5),
        }
    )
    return df


@dataclass
class MissionStatus:
    mission_name: str
    objective: str
    location: str
    pilot: str
    supervisor: str
    start_time: datetime
    status: str
    notes: str


MISSION = MissionStatus(
    mission_name="Poseidon-7 Survey",
    objective="Map subsea pipeline integrity and capture HD imagery",
    location="North Sea Block 15",
    pilot="Casey Morgan",
    supervisor="Lt. Priya Desai",
    start_time=datetime.utcnow() - timedelta(hours=3, minutes=27),
    status="Active",
    notes="Monitoring cross-current turbulence; maintain depth < 350m.",
)

telemetry_df = _generate_sample_data()


def sidebar_filters(df: pd.DataFrame) -> pd.DataFrame:
    st.sidebar.header("Filters")
    time_options = {
        "Last 30 minutes": 30,
        "Last 1 hour": 60,
        "Last 3 hours": 180,
        "Last 6 hours": 360,
        "All data": None,
    }
    selection = st.sidebar.radio("Time range", list(time_options.keys()), index=2)
    minutes = time_options[selection]
    if minutes is None:
        return df
    cutoff = df["timestamp"].max() - timedelta(minutes=minutes)
    return df[df["timestamp"] >= cutoff]


def mission_overview(status: MissionStatus, df: pd.DataFrame) -> None:
    st.title("ROV Operations Dashboard")
    st.caption("Live operations overview with synthetic telemetry for demonstration.")

    with st.expander("Mission Details", expanded=True):
        cols = st.columns([1, 1, 1, 1])
        cols[0].metric("Mission", status.mission_name)
        cols[1].metric("Status", status.status)
        elapsed = datetime.utcnow() - status.start_time
        cols[2].metric("Elapsed Time", f"{elapsed.seconds // 3600}h {(elapsed.seconds % 3600) // 60}m")
        cols[3].metric("Pilot", status.pilot)

        st.markdown(
            f"""
            **Objective:** {status.objective}

            **Location:** {status.location}  
            **Supervisor:** {status.supervisor}  
            **Notes:** {status.notes}
            """
        )

    metrics_cols = st.columns(4)
    latest = df.iloc[-1]
    metrics_cols[0].metric("Depth", f"{latest.depth_m:,.0f} m", delta=f"{latest.depth_m - df.iloc[-2].depth_m:+.1f} m")
    metrics_cols[1].metric("Temperature", f"{latest.temperature_c:.1f} °C", delta=f"{latest.temperature_c - df.iloc[-2].temperature_c:+.2f} °C")
    metrics_cols[2].metric("Pressure", f"{latest.pressure_kpa:,.0f} kPa")
    metrics_cols[3].metric("Power Reserve", f"{latest.power_pct:.0f}%", delta=f"{latest.power_pct - df.iloc[-2].power_pct:+.1f}%")


def plot_timeseries(df: pd.DataFrame) -> None:
    st.subheader("Telemetry Trends")
    chart_tabs = st.tabs(["Depth", "Temperature", "Pressure"])

    depth_fig = px.line(
        df,
        x="timestamp",
        y="depth_m",
        title="Depth over Time",
        labels={"timestamp": "Timestamp", "depth_m": "Depth (m)"},
        markers=True,
    )
    depth_fig.update_yaxes(autorange="reversed")

    temp_fig = px.line(
        df,
        x="timestamp",
        y="temperature_c",
        title="Temperature over Time",
        labels={"timestamp": "Timestamp", "temperature_c": "Temperature (°C)"},
        markers=True,
        line_shape="spline",
    )

    pressure_fig = px.line(
        df,
        x="timestamp",
        y="pressure_kpa",
        title="Pressure over Time",
        labels={"timestamp": "Timestamp", "pressure_kpa": "Pressure (kPa)"},
        markers=True,
    )

    for fig in (depth_fig, temp_fig, pressure_fig):
        fig.update_layout(margin=dict(l=20, r=20, t=60, b=40), template="plotly_dark")

    chart_tabs[0].plotly_chart(depth_fig, use_container_width=True)
    chart_tabs[1].plotly_chart(temp_fig, use_container_width=True)
    chart_tabs[2].plotly_chart(pressure_fig, use_container_width=True)


def engineering_panel(df: pd.DataFrame) -> None:
    st.subheader("Engineering Snapshot")
    col1, col2 = st.columns(2)

    energy_fig = go.Figure()
    energy_fig.add_trace(
        go.Indicator(
            mode="gauge+number",
            value=df["power_pct"].iloc[-1],
            title={"text": "Power Reserve"},
            gauge={
                "axis": {"range": [0, 100]},
                "bar": {"color": "#33FF99"},
                "steps": [
                    {"range": [0, 40], "color": "#8B0000"},
                    {"range": [40, 70], "color": "#E9967A"},
                    {"range": [70, 100], "color": "#1f77b4"},
                ],
            },
        )
    )
    energy_fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    col1.plotly_chart(energy_fig, use_container_width=True)

    heading_fig = px.scatter_polar(
        df.tail(60),
        r="speed_knots",
        theta="heading_deg",
        color="speed_knots",
        title="Heading & Speed (last 60 samples)",
        color_continuous_scale="Blues",
    )
    heading_fig.update_layout(height=300, margin=dict(l=20, r=20, t=60, b=40))
    col2.plotly_chart(heading_fig, use_container_width=True)


def telemetry_table(df: pd.DataFrame) -> None:
    st.subheader("Telemetry Table")
    formatted_df = df.copy()
    formatted_df["timestamp"] = formatted_df["timestamp"].dt.strftime("%Y-%m-%d %H:%M")
    formatted_df.rename(
        columns={
            "timestamp": "Timestamp",
            "depth_m": "Depth (m)",
            "temperature_c": "Temperature (°C)",
            "pressure_kpa": "Pressure (kPa)",
            "power_pct": "Power (%)",
            "heading_deg": "Heading (°)",
            "speed_knots": "Speed (kn)",
        },
        inplace=True,
    )
    st.dataframe(
        formatted_df.tail(50).iloc[::-1],
        use_container_width=True,
        hide_index=True,
    )


filtered_df = sidebar_filters(telemetry_df)
mission_overview(MISSION, filtered_df)
plot_timeseries(filtered_df)
engineering_panel(filtered_df)
telemetry_table(filtered_df)

st.sidebar.markdown("---")
st.sidebar.write(
    "This dashboard uses synthetic data for demonstration. Replace the data generation "
    "logic with live telemetry integration for production use."
)
