# ROV Operations Dashboard

A Streamlit application for monitoring remotely operated vehicle (ROV) missions using Plotly visualizations. The dashboard ships with synthetic telemetry so you can explore the layout and interactions locally, and it can be adapted to consume live mission data.

## Getting started

1. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the dashboard**

   ```bash
   streamlit run app.py
   ```

   Streamlit will print a local development URL (typically `http://localhost:8501`) that you can open in your browser.

## Customizing the data source

The sample telemetry is generated in `app.py` inside the `_generate_sample_data` helper. Replace this function with your own data ingestion logic (REST endpoint, database query, ROS topic, etc.) and ensure the resulting `pandas.DataFrame` includes the columns used across the charts and tables:

- `timestamp`
- `depth_m`
- `temperature_c`
- `pressure_kpa`
- `power_pct`
- `heading_deg`
- `speed_knots`

Feel free to add or remove fields and extend the visualizations as needed for your mission requirements.
