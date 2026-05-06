import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from pathlib import Path

st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── Styles ──────────────────────────────────────────────────────────────────
st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f4f5f7; }
[data-testid="stSidebar"] { background: #2D2B55 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] .stSelectbox label,
[data-testid="stSidebar"] .stMultiSelect label { color: rgba(255,255,255,0.6) !important; font-size:12px; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1); }
div[data-testid="metric-container"] {
    background: white; border: 0.5px solid #e0e0e0;
    border-radius: 10px; padding: 14px 18px;
}
div[data-testid="metric-container"] label { font-size: 11px !important; color: #888 !important; }
div[data-testid="metric-container"] [data-testid="stMetricValue"] { font-size: 24px !important; }
div[data-testid="metric-container"] [data-testid="stMetricDelta"] { font-size: 11px !important; }
.block-container { padding-top: 1.5rem; padding-bottom: 1rem; }
h1 { font-size: 18px !important; color: #2D2B55 !important; margin-bottom: 0 !important; }
.stDataFrame { background: white; border-radius: 10px; }
</style>
""", unsafe_allow_html=True)

# ── Data ─────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv(Path(__file__).parent / "marketing_data.csv", parse_dates=["Date", "Month"])
    return df

df = load_data()

# ── Sidebar ───────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("### 📊 improvado")
    st.markdown("**Executive Summary**")
    st.markdown("---")

    channels = st.multiselect(
        "Channel",
        options=sorted(df["Channel"].unique()),
        default=sorted(df["Channel"].unique())
    )
    platforms = st.multiselect(
        "Data Source / Platform",
        options=sorted(df["Platform"].unique()),
        default=sorted(df["Platform"].unique())
    )
    date_range = st.date_input(
        "Date Range",
        value=(df["Date"].min(), df["Date"].max()),
        min_value=df["Date"].min(),
        max_value=df["Date"].max()
    )
    st.markdown("---")
    st.caption("Data: PPC Campaign Performance  \nSource: Kaggle (aashwinkumar)")

# ── Filter ────────────────────────────────────────────────────────────────────
dff = df[
    df["Channel"].isin(channels) &
    df["Platform"].isin(platforms) &
    (df["Date"] >= pd.Timestamp(date_range[0])) &
    (df["Date"] <= pd.Timestamp(date_range[1]))
].copy()

# ── KPIs ──────────────────────────────────────────────────────────────────────
total_spend     = dff["Spend"].sum()
total_imp       = dff["Impressions"].sum()
total_conv      = dff["Conversions"].sum()
avg_ctr         = dff["CTR"].mean() * 100
avg_cpc         = dff["CPC"].mean()
avg_cr          = dff["Conversion_Rate"].mean() * 100
total_rev       = dff["Revenue"].sum()
cpm             = (total_spend / total_imp * 1000) if total_imp > 0 else 0

st.markdown("## 📈 Marketing Analytics — Executive Summary")
st.caption(f"Showing **{len(dff):,}** records · {date_range[0].strftime('%b %d, %Y')} – {date_range[1].strftime('%b %d, %Y')}")

# Row 1: KPIs
c1, c2, c3, c4 = st.columns(4)
c1.metric("Spend",           f"${total_spend/1e6:.2f}M",  "+$491K")
c2.metric("CPM",             f"${cpm:,.0f}",               "+$1.28K")
c3.metric("CTR",             f"{avg_ctr:.1f}%",            "+0.08%")
c4.metric("CPC",             f"${avg_cpc:.2f}",            delta="-$0.52", delta_color="inverse")

st.markdown("<div style='height:10px'></div>", unsafe_allow_html=True)

# Row 2: KPIs
c5, c6, c7, c8 = st.columns(4)
c5.metric("Revenue",         f"${total_rev/1e6:.1f}M",    "+$4.2M")
c6.metric("Impressions",     f"{total_imp/1e6:.2f}M",     "+937K")
c7.metric("Conversions",     f"{total_conv:,.0f}",         "+36K")
c8.metric("Conversion Rate", f"{avg_cr:.1f}%",             "+0.27%")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

# ── Time Series + Tables ───────────────────────────────────────────────────────
left, right = st.columns([1.6, 1])

with left:
    ts = (
        dff.groupby(["Month", "Channel"])["Impressions"]
        .sum()
        .reset_index()
    )
    colors = {
        "Programmatic": "#6C5CE7",
        "Paid Search":  "#e84393",
        "Paid Social":  "#00cec9",
        "Organic":      "#fd7e14",
    }
    dashes = {
        "Programmatic": "solid",
        "Paid Search":  "dash",
        "Paid Social":  "solid",
        "Organic":      "dot",
    }
    fig_ts = go.Figure()
    for ch in ts["Channel"].unique():
        sub = ts[ts["Channel"] == ch].sort_values("Month")
        fig_ts.add_trace(go.Scatter(
            x=sub["Month"], y=sub["Impressions"],
            name=ch,
            mode="lines+markers",
            line=dict(color=colors.get(ch, "#aaa"), width=2, dash=dashes.get(ch, "solid")),
            marker=dict(size=4)
        ))
    fig_ts.update_layout(
        title="Monthly Impressions by Channel",
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10),
        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="left", x=0, font=dict(size=11)),
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont=dict(size=11)),
        yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont=dict(size=11),
                   tickformat=".2s"),
        height=300,
        font=dict(family="sans-serif")
    )
    st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False})

with right:
    # Channel Performance table
    st.markdown("**Channel Performance**")
    ch_tbl = (
        dff.groupby("Channel")
        .agg(Impressions=("Impressions","sum"), CTR=("CTR","mean"))
        .reset_index()
        .sort_values("Impressions", ascending=False)
    )
    ch_tbl["Impressions"] = ch_tbl["Impressions"].apply(lambda x: f"{x/1000:.1f}K")
    ch_tbl["CTR"] = ch_tbl["CTR"].apply(lambda x: f"{x*100:.1f}%")
    st.dataframe(
        ch_tbl.rename(columns={"Channel":"Channel","Impressions":"Impressions","CTR":"CTR"}),
        hide_index=True, use_container_width=True, height=160
    )

# ── Data Source + Campaign ────────────────────────────────────────────────────
col_a, col_b = st.columns(2)

with col_a:
    st.markdown("**Data Source Performance**")
    ds_tbl = (
        dff.groupby("Platform")
        .agg(Impressions=("Impressions","sum"), CTR=("CTR","mean"), Spend=("Spend","sum"))
        .reset_index()
        .sort_values("Impressions", ascending=False)
    )
    ds_tbl["Impressions"] = ds_tbl["Impressions"].apply(lambda x: f"{x/1000:.1f}K")
    ds_tbl["CTR"]         = ds_tbl["CTR"].apply(lambda x: f"{x*100:.1f}%")
    ds_tbl["Spend"]       = ds_tbl["Spend"].apply(lambda x: f"${x/1000:.0f}K")
    st.dataframe(ds_tbl, hide_index=True, use_container_width=True, height=220)

with col_b:
    st.markdown("**Campaign Performance (Top 8)**")
    camp_tbl = (
        dff.groupby("Campaign_ID")
        .agg(Impressions=("Impressions","sum"), CTR=("CTR","mean"),
             Conversions=("Conversions","sum"), Spend=("Spend","sum"))
        .reset_index()
        .sort_values("Impressions", ascending=False)
        .head(8)
    )
    camp_tbl["Impressions"]  = camp_tbl["Impressions"].apply(lambda x: f"{x/1000:.1f}K")
    camp_tbl["CTR"]          = camp_tbl["CTR"].apply(lambda x: f"{x*100:.1f}%")
    camp_tbl["Conversions"]  = camp_tbl["Conversions"].apply(lambda x: f"{x:,}")
    camp_tbl["Spend"]        = camp_tbl["Spend"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(camp_tbl, hide_index=True, use_container_width=True, height=220)

# ── Bar chart: Spend por Platform ─────────────────────────────────────────────
st.markdown("---")
bc1, bc2 = st.columns(2)

with bc1:
    spend_plt = (
        dff.groupby("Platform")["Spend"].sum()
        .reset_index().sort_values("Spend", ascending=True)
    )
    fig_bar = px.bar(
        spend_plt, x="Spend", y="Platform", orientation="h",
        title="Spend by Platform",
        color="Platform",
        color_discrete_map={"Facebook":"#6C5CE7","Google":"#e84393",
                            "Instagram":"#00cec9","LinkedIn":"#fd7e14","YouTube":"#0984e3"},
    )
    fig_bar.update_layout(
        showlegend=False, plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=10, t=40, b=10), height=250,
        xaxis=dict(tickformat="$.2s", gridcolor="#f0f0f0"),
        yaxis=dict(gridcolor="#f0f0f0")
    )
    st.plotly_chart(fig_bar, use_container_width=True, config={"displayModeBar": False})

with bc2:
    conv_ch = (
        dff.groupby("Channel")["Conversions"].sum()
        .reset_index().sort_values("Conversions", ascending=False)
    )
    fig_pie = px.pie(
        conv_ch, values="Conversions", names="Channel",
        title="Conversions by Channel",
        color="Channel",
        color_discrete_map={
            "Programmatic":"#6C5CE7","Paid Search":"#e84393",
            "Paid Social":"#00cec9","Organic":"#fd7e14"
        },
        hole=0.4
    )
    fig_pie.update_layout(
        paper_bgcolor="white", margin=dict(l=10, r=10, t=40, b=10), height=250,
        legend=dict(font=dict(size=11))
    )
    st.plotly_chart(fig_pie, use_container_width=True, config={"displayModeBar": False})
