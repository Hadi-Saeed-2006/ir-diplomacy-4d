import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path
import requests

st.set_page_config(page_title="DIPLOMATIQ 4D", page_icon="🌐", layout="wide", initial_sidebar_state="expanded")
ROOT = Path(__file__).parent
DATA_FILE = ROOT / "data" / "diplomatic_events.csv"
REQUIRED = {"date", "country", "partner", "region", "lat", "lon", "category", "severity", "impact", "event"}
GDELT_API = "https://api.gdeltproject.org/api/v2/doc/doc"
GDELT_QUERY = '(diplomacy OR "foreign relations" OR "strategic dialogue" OR "bilateral relations" OR "international summit")'

@st.cache_data
def load_data():
    df = pd.read_csv(DATA_FILE, parse_dates=["date"])
    missing = REQUIRED - set(df.columns)
    if missing: raise ValueError(f"Dataset is missing columns: {sorted(missing)}")
    for c in ["lat", "lon", "severity", "impact"]: df[c] = pd.to_numeric(df[c], errors="coerce")
    return df.dropna(subset=["date", "country", "partner", "lat", "lon", "severity", "impact"]).sort_values("date")

@st.cache_data(ttl=900)
def fetch_live_news(query=GDELT_QUERY, limit=50):
    params={"query":query,"mode":"artlist","maxrecords":min(max(limit,1),250),"timespan":"7d","sort":"datedesc","format":"json"}
    r=requests.get(GDELT_API,params=params,timeout=15); r.raise_for_status()
    rows=[]
    for a in r.json().get("articles",[]):
        rows.append({"date":a.get("seendate",""),"title":a.get("title",""),"url":a.get("url",""),"domain":a.get("domain",""),"language":a.get("language",""),"source":"GDELT DOC 2.0"})
    return pd.DataFrame(rows)

try: df=load_data()
except Exception as exc:
    st.error("The dashboard could not load its dataset."); st.exception(exc); st.stop()

st.title("🌐 DIPLOMATIQ 4D")
st.caption("Global Relations & Diplomacy Intelligence • geospatial + temporal + relationship analytics")
with st.sidebar:
    st.header("Control Room")
    min_date,max_date=df.date.min().date(),df.date.max().date()
    dates=st.date_input("Time window",(min_date,max_date),min_value=min_date,max_value=max_date)
    region=st.selectbox("Region",["All"]+sorted(df.region.unique().tolist()))
    category=st.selectbox("Event type",["All"]+sorted(df.category.unique().tolist()))
    severity=st.slider("Minimum severity",1,5,1)
    st.divider(); live_news=st.checkbox("Enable live GDELT news",False)
    st.caption("Live news is optional; the core dashboard works offline.")

if isinstance(dates,(tuple,list)) and len(dates)==2: start,end=pd.Timestamp(dates[0]),pd.Timestamp(dates[1])
else: start=end=pd.Timestamp(dates)
filtered=df[(df.date>=start)&(df.date<=end)&(df.severity>=severity)].copy()
if region!="All": filtered=filtered[filtered.region==region]
if category!="All": filtered=filtered[filtered.category==category]

k1,k2,k3,k4,k5=st.columns(5)
k1.metric("Events",f"{len(filtered):,}"); k2.metric("Countries",f"{filtered.country.nunique():,}"); k3.metric("Partners",f"{filtered.partner.nunique():,}"); k4.metric("Avg severity",f"{filtered.severity.mean():.2f}" if len(filtered) else "—"); k5.metric("Total impact",f"{filtered.impact.sum():,.0f}")
if filtered.empty: st.warning("No events match the current filters. Broaden the time window or reduce severity."); st.stop()
st.success(f"Analysis window: {start.date()} → {end.date()} • {len(filtered):,} matching events")

tab1,tab2,tab3,tab4,tab5,tab6=st.tabs(["🛰️ 4D Globe","🤝 Diplomatic Network","📈 Risk & Trends","🧠 Analyst Brief","📰 Live News","🌍 Country Profile"])

with tab1:
    fig=px.scatter_geo(filtered,lat="lat",lon="lon",color="severity",size="impact",hover_name="event",hover_data={"country":True,"partner":True,"category":True,"date":True,"severity":True,"impact":True,"lat":False,"lon":False},projection="orthographic",title="Global diplomatic event field")
    fig.update_geos(showland=True,showcountries=True,showocean=True); fig.update_layout(height=620,margin=dict(l=0,r=0,t=55,b=0)); st.plotly_chart(fig,use_container_width=True)
    st.caption("4D = geographic space represented on the globe + time represented through the selected event window.")
    st.dataframe(filtered.sort_values("date",ascending=False)[["date","country","partner","region","category","severity","impact","event"]].head(25),hide_index=True,use_container_width=True)

with tab2:
    edges=filtered.groupby(["country","partner"],as_index=False).agg(weight=("impact","sum"),events=("event","count")).sort_values("weight",ascending=False).head(25)
    nodes=pd.unique(pd.concat([edges.country,edges.partner],ignore_index=True)); angles=np.linspace(0,2*np.pi,len(nodes),endpoint=False); pos={n:(np.cos(a),np.sin(a)) for n,a in zip(nodes,angles)}
    fig=go.Figure()
    for _,r in edges.iterrows():
        x0,y0=pos[r.country]; x1,y1=pos[r.partner]; fig.add_trace(go.Scatter(x=[x0,x1,None],y=[y0,y1,None],mode="lines",line=dict(width=max(1,min(7,float(r.weight)/20))),opacity=.35,hoverinfo="skip"))
    fig.add_trace(go.Scatter(x=[pos[n][0] for n in nodes],y=[pos[n][1] for n in nodes],mode="markers+text",text=nodes,textposition="top center",marker=dict(size=16),hoverinfo="text"))
    fig.update_layout(title="Diplomatic interaction network",showlegend=False,xaxis=dict(visible=False),yaxis=dict(visible=False),height=620,margin=dict(l=0,r=0,t=55,b=0)); st.plotly_chart(fig,use_container_width=True); st.caption("Edge width reflects aggregate event impact; it does not imply political alignment."); st.dataframe(edges,hide_index=True,use_container_width=True)

with tab3:
    trend=filtered.assign(month=filtered.date.dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(events=("event","count"),impact=("impact","sum"),severity=("severity","mean"))
    c1,c2=st.columns(2)
    with c1: st.plotly_chart(px.line(trend,x="month",y=["events","impact"],markers=True,title="Event volume and impact"),use_container_width=True)
    with c2:
        country=filtered.groupby("country",as_index=False).agg(events=("event","count"),severity=("severity","mean"),impact=("impact","sum")); mi=max(float(country.impact.max()),1); me=max(float(country.events.max()),1); country["pressure_score"]=np.round(100*(.45*country.severity/5+.35*country.impact/mi+.20*country.events/me),1); country=country.sort_values("pressure_score",ascending=False).head(12)
        st.plotly_chart(px.bar(country.sort_values("pressure_score"),x="pressure_score",y="country",orientation="h",title="Relative geopolitical pressure score"),use_container_width=True)
    st.caption("Pressure score is a transparent portfolio indicator, not an official sovereign-risk rating.")

with tab4:
    country=filtered.groupby("country").agg(events=("event","count"),impact=("impact","sum")).sort_values("impact",ascending=False); latest=filtered.sort_values("date").iloc[-1]
    st.subheader("Executive intelligence brief"); st.markdown(f"**Window:** {start.date()} → {end.date()}  \n**Signal volume:** {len(filtered):,} events across {filtered.country.nunique()} countries  \n**Highest aggregate impact:** **{country.index[0]}**  \n**Latest recorded signal:** **{latest.event}** on {latest.date.date()}")
    st.markdown("### Analyst workflow\n1. **Detect** clusters.\n2. **Connect** actors.\n3. **Quantify** severity, impact and frequency.\n4. **Formulate** a testable hypothesis.\n5. **Validate** against authoritative primary sources.")
    st.download_button("⬇️ Export filtered events",filtered.to_csv(index=False).encode(),"diplomatiq_filtered_events.csv","text/csv")

with tab5:
    st.subheader("📰 Live diplomatic news signals")
    if not live_news: st.info("Enable Live GDELT news when you want fresh article signals. It is disabled by default for fast, reliable demos.")
    else:
        try:
            news=fetch_live_news()
            if news.empty: st.warning("No matching articles returned.")
            else:
                st.success(f"Loaded {len(news):,} recent article signals."); st.dataframe(news[["date","title","domain","language"]],hide_index=True,use_container_width=True); st.caption("News coverage is a signal about media attention, not proof of a diplomatic event."); st.download_button("⬇️ Export live news",news.to_csv(index=False).encode(),"gdelt_news.csv","text/csv")
        except (requests.RequestException,ValueError) as exc: st.warning("Live GDELT data is temporarily unavailable. The core dashboard is unaffected."); st.caption(str(exc))

with tab6:
    st.subheader("🌍 Country Intelligence Profile")
    countries=sorted(filtered.country.unique().tolist()); selected=st.selectbox("Select country",countries,key="profile_country")
    cf=filtered[filtered.country==selected].copy(); partners=cf.groupby("partner",as_index=False).agg(events=("event","count"),impact=("impact","sum")).sort_values("impact",ascending=False)
    avg=float(cf.severity.mean()); total=float(cf.impact.sum()); events=len(cf); mi=max(float(filtered.impact.sum()),1); me=max(len(filtered),1)
    score=round(100*(.45*avg/5+.35*total/mi+.20*events/me),1)
    a,b,c,d=st.columns(4); a.metric("Events",f"{events:,}"); b.metric("Avg severity",f"{avg:.2f}"); c.metric("Aggregate impact",f"{total:,.0f}"); d.metric("Pressure score",f"{score:.1f}/100")
    left,right=st.columns(2)
    with left:
        st.markdown("#### Top diplomatic counterparties"); st.dataframe(partners.head(10),hide_index=True,use_container_width=True)
        trend=cf.assign(month=cf.date.dt.to_period("M").astype(str)).groupby("month",as_index=False).agg(events=("event","count"),impact=("impact","sum")); st.plotly_chart(px.line(trend,x="month",y=["events","impact"],markers=True,title=f"{selected} activity trend"),use_container_width=True)
    with right:
        st.markdown("#### Event mix"); mix=cf.category.value_counts().rename_axis("category").reset_index(name="events"); st.plotly_chart(px.pie(mix,names="category",values="events",title=f"{selected} event mix"),use_container_width=True)
        st.markdown("#### Recent signals"); st.dataframe(cf.sort_values("date",ascending=False)[["date","partner","category","severity","impact","event"]].head(8),hide_index=True,use_container_width=True)
    st.info("Interpretation: this profile summarizes the selected event sample. It is not a sovereign rating, intelligence assessment, or prediction.")

st.divider(); st.caption("DIPLOMATIQ 4D • Portfolio project by Hadi Shaikh • Decision-support prototype, not intelligence or foreign-policy advice")