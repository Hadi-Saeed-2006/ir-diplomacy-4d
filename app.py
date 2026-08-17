import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(page_title="DIPLOMATIQ 4D", page_icon="🌐", layout="wide", initial_sidebar_state="expanded")
DATA_FILE = Path(__file__).parent / "data" / "diplomatic_events.csv"
REQUIRED = {"date", "country", "partner", "region", "lat", "lon", "category", "severity", "impact", "event"}

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    missing = REQUIRED - set(df.columns)
    if missing:
        raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    numeric = ["lat", "lon", "severity", "impact"]
    for col in numeric:
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["date", "country", "partner", "lat", "lon", "severity", "impact"])
    return df.sort_values("date")

try:
    df = load_data()
except Exception as exc:
    st.error("The dashboard could not load its dataset.")
    st.exception(exc)
    st.stop()

st.title("🌐 DIPLOMATIQ 4D")
st.caption("Global Relations & Diplomacy Intelligence • geospatial + temporal + relationship analytics")

with st.sidebar:
    st.header("Control Room")
    min_date, max_date = df.date.min().date(), df.date.max().date()
    selected_dates = st.date_input("Time window", (min_date, max_date), min_value=min_date, max_value=max_date)
    regions = ["All"] + sorted(df.region.unique().tolist())
    region = st.selectbox("Region", regions)
    categories = ["All"] + sorted(df.category.unique().tolist())
    category = st.selectbox("Event type", categories)
    severity = st.slider("Minimum severity", 1, 5, 1)
    st.divider()
    st.caption("Analytical indicator • not an official sovereign-risk rating")

if isinstance(selected_dates, (tuple, list)) and len(selected_dates) == 2:
    start, end = pd.Timestamp(selected_dates[0]), pd.Timestamp(selected_dates[1])
else:
    start = end = pd.Timestamp(selected_dates)

filtered = df[(df.date >= start) & (df.date <= end) & (df.severity >= severity)].copy()
if region != "All": filtered = filtered[filtered.region == region]
if category != "All": filtered = filtered[filtered.category == category]

k1, k2, k3, k4, k5 = st.columns(5)
k1.metric("Events", f"{len(filtered):,}")
k2.metric("Countries", f"{filtered.country.nunique():,}")
k3.metric("Partners", f"{filtered.partner.nunique():,}")
k4.metric("Avg severity", f"{filtered.severity.mean():.2f}" if len(filtered) else "—")
k5.metric("Total impact", f"{filtered.impact.sum():,.0f}")

if filtered.empty:
    st.warning("No events match the current filters. Broaden the time window or reduce the severity filter.")
    st.stop()

st.success(f"Analysis window: {start.date()} → {end.date()} • {len(filtered):,} matching events")

tab1, tab2, tab3, tab4 = st.tabs(["🛰️ 4D Globe", "🤝 Diplomatic Network", "📈 Risk & Trends", "🧠 Analyst Brief"])

with tab1:
    globe = px.scatter_geo(filtered, lat="lat", lon="lon", color="severity", size="impact", hover_name="event",
        hover_data={"country": True, "partner": True, "category": True, "date": True, "severity": True, "impact": True, "lat": False, "lon": False},
        projection="orthographic", title="Global diplomatic event field")
    globe.update_geos(showland=True, showcountries=True, showocean=True)
    globe.update_layout(height=620, margin=dict(l=0, r=0, t=55, b=0))
    st.plotly_chart(globe, use_container_width=True)
    st.caption("4D = geographic space represented on the globe + time represented through the selected event window.")
    st.dataframe(filtered.sort_values("date", ascending=False)[["date", "country", "partner", "region", "category", "severity", "impact", "event"]].head(25), hide_index=True, use_container_width=True)

with tab2:
    edges = (filtered.groupby(["country", "partner"], as_index=False).agg(weight=("impact", "sum"), events=("event", "count"))
             .sort_values("weight", ascending=False).head(25))
    if edges.empty:
        st.info("No relationships match the current filters.")
    else:
        nodes = pd.unique(pd.concat([edges.country, edges.partner], ignore_index=True))
        angles = np.linspace(0, 2 * np.pi, len(nodes), endpoint=False)
        positions = {name: (np.cos(angle), np.sin(angle)) for name, angle in zip(nodes, angles)}
        fig = go.Figure()
        for _, row in edges.iterrows():
            x0, y0 = positions[row.country]; x1, y1 = positions[row.partner]
            fig.add_trace(go.Scatter(x=[x0, x1, None], y=[y0, y1, None], mode="lines",
                line=dict(width=max(1, min(7, float(row.weight) / 20))), opacity=0.35, hoverinfo="skip"))
        fig.add_trace(go.Scatter(x=[positions[n][0] for n in nodes], y=[positions[n][1] for n in nodes],
            mode="markers+text", text=nodes, textposition="top center", marker=dict(size=16), hovertext=nodes, hoverinfo="text"))
        fig.update_layout(title="Diplomatic interaction network", showlegend=False, xaxis=dict(visible=False), yaxis=dict(visible=False), height=620, margin=dict(l=0, r=0, t=55, b=0))
        st.plotly_chart(fig, use_container_width=True)
        st.caption("Edge width reflects aggregate event impact in the selected sample; it does not imply political alignment.")
        st.dataframe(edges, hide_index=True, use_container_width=True)

with tab3:
    trend = (filtered.assign(month=filtered.date.dt.to_period("M").astype(str)).groupby("month", as_index=False)
             .agg(events=("event", "count"), impact=("impact", "sum"), severity=("severity", "mean")))
    c1, c2 = st.columns(2)
    with c1:
        fig = px.line(trend, x="month", y=["events", "impact"], markers=True, title="Event volume and impact")
        st.plotly_chart(fig, use_container_width=True)
    with c2:
        country = filtered.groupby("country", as_index=False).agg(events=("event", "count"), severity=("severity", "mean"), impact=("impact", "sum"))
        max_impact = max(float(country.impact.max()), 1.0); max_events = max(float(country.events.max()), 1.0)
        country["pressure_score"] = np.round(100 * (0.45 * country.severity / 5 + 0.35 * country.impact / max_impact + 0.20 * country.events / max_events), 1)
        country = country.sort_values("pressure_score", ascending=False).head(12)
        fig = px.bar(country.sort_values("pressure_score"), x="pressure_score", y="country", orientation="h", title="Relative geopolitical pressure score")
        st.plotly_chart(fig, use_container_width=True)
    st.caption("Pressure score is a transparent portfolio indicator calculated from severity, aggregate impact and event frequency within the selected sample.")

with tab4:
    country = filtered.groupby("country").agg(events=("event", "count"), impact=("impact", "sum")).sort_values("impact", ascending=False)
    latest = filtered.sort_values("date").iloc[-1]
    st.subheader("Executive intelligence brief")
    st.markdown(f"**Window:** {start.date()} → {end.date()}  \n**Signal volume:** {len(filtered):,} events across {filtered.country.nunique()} countries  \n**Highest aggregate impact:** **{country.index[0]}**  \n**Latest recorded signal:** **{latest.event}** on {latest.date.date()}")
    st.markdown("### Analyst workflow\n1. **Detect** clusters and unusual event concentrations.\n2. **Connect** actors through the diplomatic interaction network.\n3. **Quantify** severity, impact and event frequency.\n4. **Formulate** a testable strategic hypothesis.\n5. **Validate** against authoritative primary sources before drawing conclusions.")
    st.download_button("⬇️ Export filtered events (CSV)", filtered.to_csv(index=False).encode("utf-8"), "diplomatiq_filtered_events.csv", "text/csv")

st.divider()
st.caption("DIPLOMATIQ 4D • Portfolio project by Hadi Shaikh • Decision-support prototype, not intelligence or foreign-policy advice")