import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from pathlib import Path

st.set_page_config(
    page_title="Marketing Analytics Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
[data-testid="stAppViewContainer"] { background: #f4f5f7; }
[data-testid="stSidebar"] { background: #2D2B55 !important; }
[data-testid="stSidebar"] * { color: rgba(255,255,255,0.85) !important; }
[data-testid="stSidebar"] .stMultiSelect label,
[data-testid="stSidebar"] .stDateInput label { color: rgba(255,255,255,0.6) !important; font-size: 12px; }
[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.1); }
.block-container { padding-top: 1.2rem; padding-bottom: 1rem; }
h2, h3 { color: #2D2B55 !important; }
.kpi-label  { font-size: 11px; color: #888; margin-bottom: 1px; font-weight: 400; }
.kpi-value  { font-size: 24px; font-weight: 600; color: #2D2B55; line-height: 1.1; margin-bottom: 2px; }
.delta-up   { font-size: 11px; color: #00b894; }
.delta-down { font-size: 11px; color: #d63031; }
div[data-testid="stVerticalBlock"] div[data-testid="stVerticalBlock"] { background: white; border-radius: 10px; border: 0.5px solid #e5e5e5; padding: 10px 14px 6px; }
</style>
""", unsafe_allow_html=True)

# ── Datos ──────────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    return pd.read_csv(
        Path(__file__).parent / "marketing_data.csv",
        parse_dates=["Date", "Month"]
    )

df = load_data()

# Series mensuales reales Feb–Dic 2024
MONTHS = ["Feb","Mar","Apr","May","Jun","Jul","Aug","Sep","Oct","Nov","Dec"]
MONTHLY = {
    "Spend":       [319011,524689,563206,535933,531609,517916,523226,449068,528310,387299,421192],
    "CPM":         [1025,  1051,  1183,  1165,  1101,  1180,  1234,  1104,   958,  1027,  1083],
    "CTR":         [25.19, 23.33, 29.84, 29.76, 25.40, 29.38, 25.54, 30.36, 22.51, 22.29, 27.89],
    "CPC":         [14.44, 13.61,  9.27,  9.36, 12.80, 11.39, 13.25,  8.53, 12.01,  9.47, 11.55],
    "Revenue":     [3321877,4927968,6413032,5769677,4904379,5116647,5009860,4747832,4988722,4478878,4148418],
    "Impressions": [311261,499315,475986,459894,482623,439094,424083,406671,551379,376950,389087],
    "Conversions": [28443, 40951, 48081, 49207, 41201, 44327, 41453, 40253, 46476, 37469, 36446],
    "CR":          [49.85, 48.99, 49.78, 55.25, 49.83, 52.54, 48.74, 48.95, 52.48, 56.73, 51.94],
}

PURPLE = "#6C5CE7"
COLOR_MAP = {
    "Programmatic": "#6C5CE7",
    "Paid Search":  "#e84393",
    "Paid Social":  "#00cec9",
    "Organic":      "#fd7e14",
}
DASH_MAP = {
    "Programmatic": "solid",
    "Paid Search":  "dash",
    "Paid Social":  "solid",
    "Organic":      "dot",
}
PLATFORM_COLORS = {
    "Facebook":  "#6C5CE7",
    "Google":    "#e84393",
    "Instagram": "#00cec9",
    "LinkedIn":  "#fd7e14",
    "YouTube":   "#0984e3",
}
CONTENT_COLORS = ["#6C5CE7","#e84393","#00cec9","#fd7e14"]

# ── Sparkline helper ────────────────────────────────────────────────────────────
def make_sparkline(key: str) -> go.Figure:
    fig = go.Figure(go.Scatter(
        x=MONTHS, y=MONTHLY[key],
        mode="lines",
        line=dict(color=PURPLE, width=1.8),
        fill="tozeroy",
        fillcolor="rgba(108,92,231,0.07)",
        hovertemplate="%{x}: %{y:,.0f}<extra></extra>"
    ))
    fig.update_layout(
        height=52,
        margin=dict(l=0, r=0, t=0, b=0),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        showlegend=False
    )
    return fig

# ── KPI card helper ─────────────────────────────────────────────────────────────
def kpi_card(col, label: str, value: str, delta: str, up: bool, spark_key: str):
    with col:
        with st.container():
            st.markdown(f"<div class='kpi-label'>{label}</div>", unsafe_allow_html=True)
            st.markdown(f"<div class='kpi-value'>{value}</div>", unsafe_allow_html=True)
            arrow = "↑" if up else "↓"
            css   = "delta-up" if up else "delta-down"
            st.markdown(f"<div class='{css}'>{arrow} {delta}</div>", unsafe_allow_html=True)
            st.plotly_chart(
                make_sparkline(spark_key),
                use_container_width=True,
                config={"displayModeBar": False},
                key=f"sp_{spark_key}"
            )

# ── Sidebar ─────────────────────────────────────────────────────────────────────
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
    content_types = st.multiselect(
        "Content Type",
        options=sorted(df["Content_Type"].unique()),
        default=sorted(df["Content_Type"].unique())
    )
    date_range = st.date_input(
        "Date Range",
        value=(df["Date"].min(), df["Date"].max()),
        min_value=df["Date"].min(),
        max_value=df["Date"].max()
    )
    st.markdown("---")
    st.caption("Data: PPC Campaign Performance\nSource: Kaggle (aashwinkumar)")

# ── Filtro ───────────────────────────────────────────────────────────────────────
dff = df[
    df["Channel"].isin(channels) &
    df["Platform"].isin(platforms) &
    df["Content_Type"].isin(content_types) &
    (df["Date"] >= pd.Timestamp(date_range[0])) &
    (df["Date"] <= pd.Timestamp(date_range[1]))
].copy()

# ── Header ───────────────────────────────────────────────────────────────────────
st.markdown("## 📈 Marketing Analytics — Executive Summary")
st.caption(
    f"Showing **{len(dff):,}** records · "
    f"{date_range[0].strftime('%b %d, %Y')} – {date_range[1].strftime('%b %d, %Y')}"
)

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 1 — KPI Cards con Sparklines
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Key Performance Indicators")

row1 = st.columns(4)
kpi_card(row1[0], "Spend",                      "$5.30M", "$491K vs prev period",  True,  "Spend")
kpi_card(row1[1], "Cost per Mille (CPM)",        "$1,101", "$1.28K vs prev period", True,  "CPM")
kpi_card(row1[2], "Click-through Rate (CTR)",    "26.6%",  "0.08% vs prev period",  True,  "CTR")
kpi_card(row1[3], "Cost per Click (CPC)",        "$11.41", "$0.52 vs prev period",  False, "CPC")

st.markdown("<div style='height:6px'></div>", unsafe_allow_html=True)

row2 = st.columns(4)
kpi_card(row2[0], "Revenue",                     "$53.8M", "$4.2M vs prev period",  True, "Revenue")
kpi_card(row2[1], "Impressions",                 "4.82M",  "937K vs prev period",   True, "Impressions")
kpi_card(row2[2], "Conversions",                 "454K",   "36K vs prev period",    True, "Conversions")
kpi_card(row2[3], "Conversion Rate",             "51.3%",  "0.27% vs prev period",  True, "CR")

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 2 — Time Series por Canal
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Monthly Impressions by Channel")

ts = (
    dff.groupby(["Month", "Channel"])["Impressions"]
    .sum().reset_index().sort_values("Month")
)

fig_ts = go.Figure()
for ch in sorted(ts["Channel"].unique()):
    sub = ts[ts["Channel"] == ch]
    fig_ts.add_trace(go.Scatter(
        x=sub["Month"], y=sub["Impressions"],
        name=ch, mode="lines+markers",
        line=dict(color=COLOR_MAP.get(ch, "#aaa"), width=2.5,
                  dash=DASH_MAP.get(ch, "solid")),
        marker=dict(size=5),
        hovertemplate="<b>%{x|%b %Y}</b><br>Impressions: %{y:,.0f}<extra></extra>"
    ))

fig_ts.update_layout(
    plot_bgcolor="white", paper_bgcolor="white",
    margin=dict(l=10, r=10, t=10, b=10), height=300,
    legend=dict(orientation="h", yanchor="bottom", y=1.02,
                xanchor="left", x=0, font=dict(size=12)),
    xaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont=dict(size=11)),
    yaxis=dict(showgrid=True, gridcolor="#f0f0f0", tickfont=dict(size=11),
               tickformat=".2s"),
    font=dict(family="sans-serif"),
    hovermode="x unified"
)
st.plotly_chart(fig_ts, use_container_width=True, config={"displayModeBar": False})

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 3 — Tablas de Performance
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Performance Tables")
col_ch, col_ds, col_camp = st.columns(3)

with col_ch:
    st.markdown("**Channel Performance**")
    ch_tbl = (
        dff.groupby("Channel")
        .agg(Impressions=("Impressions","sum"), CTR=("CTR","mean"),
             Spend=("Spend","sum"), Conversions=("Conversions","sum"))
        .reset_index().sort_values("Impressions", ascending=False)
    )
    ch_tbl["Impressions"] = ch_tbl["Impressions"].apply(lambda x: f"{x/1000:.1f}K")
    ch_tbl["CTR"]         = ch_tbl["CTR"].apply(lambda x: f"{x*100:.1f}%")
    ch_tbl["Spend"]       = ch_tbl["Spend"].apply(lambda x: f"${x/1000:.0f}K")
    ch_tbl["Conversions"] = ch_tbl["Conversions"].apply(lambda x: f"{x:,}")
    st.dataframe(
        ch_tbl[["Channel","Impressions","CTR","Spend","Conversions"]],
        hide_index=True, use_container_width=True, height=210
    )

with col_ds:
    st.markdown("**Data Source Performance**")
    ds_tbl = (
        dff.groupby("Platform")
        .agg(Impressions=("Impressions","sum"), CTR=("CTR","mean"),
             Spend=("Spend","sum"))
        .reset_index().sort_values("Impressions", ascending=False)
    )
    ds_tbl["Impressions"] = ds_tbl["Impressions"].apply(lambda x: f"{x/1000:.1f}K")
    ds_tbl["CTR"]         = ds_tbl["CTR"].apply(lambda x: f"{x*100:.1f}%")
    ds_tbl["Spend"]       = ds_tbl["Spend"].apply(lambda x: f"${x/1000:.0f}K")
    st.dataframe(ds_tbl, hide_index=True, use_container_width=True, height=245)

with col_camp:
    st.markdown("**Campaign Performance — Top 8**")
    camp_tbl = (
        dff.groupby("Campaign_ID")
        .agg(Impressions=("Impressions","sum"), CTR=("CTR","mean"),
             Conversions=("Conversions","sum"), Spend=("Spend","sum"))
        .reset_index().sort_values("Impressions", ascending=False).head(8)
    )
    camp_tbl["Impressions"]  = camp_tbl["Impressions"].apply(lambda x: f"{x/1000:.1f}K")
    camp_tbl["CTR"]          = camp_tbl["CTR"].apply(lambda x: f"{x*100:.1f}%")
    camp_tbl["Conversions"]  = camp_tbl["Conversions"].apply(lambda x: f"{x:,}")
    camp_tbl["Spend"]        = camp_tbl["Spend"].apply(lambda x: f"${x:,.0f}")
    st.dataframe(camp_tbl, hide_index=True, use_container_width=True, height=340)

st.markdown("---")

# ══════════════════════════════════════════════════════════════════════════════
# SECCIÓN 4 — Platform & Content Analysis
# ══════════════════════════════════════════════════════════════════════════════
st.markdown("### Platform & Content Type Analysis")
col_a, col_b, col_c = st.columns(3)

# — Spend por plataforma (barra horizontal)
with col_a:
    st.markdown("**Spend by Platform**")
    spend_plt = (
        dff.groupby("Platform")["Spend"].sum()
        .reset_index().sort_values("Spend", ascending=True)
    )
    colors_bar = [PLATFORM_COLORS.get(p, "#aaa") for p in spend_plt["Platform"]]
    fig_bar = go.Figure(go.Bar(
        x=spend_plt["Spend"], y=spend_plt["Platform"],
        orientation="h",
        marker=dict(color=colors_bar),
        text=spend_plt["Spend"].apply(lambda x: f"${x/1000:.0f}K"),
        textposition="outside",
        textfont=dict(size=11),
        hovertemplate="<b>%{y}</b><br>Spend: $%{x:,.0f}<extra></extra>"
    ))
    fig_bar.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=60, t=10, b=10), height=280,
        showlegend=False,
        xaxis=dict(showgrid=True, gridcolor="#f0f0f0",
                   tickformat="$,.0f", tickfont=dict(size=10)),
        yaxis=dict(showgrid=False, tickfont=dict(size=11))
    )
    st.plotly_chart(fig_bar, use_container_width=True,
                    config={"displayModeBar": False})

# — Content Type — donut de campañas
with col_b:
    st.markdown("**Content Type Distribution**")
    ct = (
        dff.groupby("Content_Type")
        .agg(Campaigns=("Campaign_ID","count"),
             Conversions=("Conversions","sum"),
             Revenue=("Revenue","sum"),
             CTR=("CTR","mean"))
        .reset_index()
    )
    fig_donut = go.Figure(go.Pie(
        labels=ct["Content_Type"],
        values=ct["Campaigns"],
        hole=0.58,
        marker=dict(
            colors=CONTENT_COLORS,
            line=dict(color="white", width=2)
        ),
        textinfo="label+percent",
        textfont=dict(size=11),
        hovertemplate=(
            "<b>%{label}</b><br>"
            "Campaigns: %{value}<br>"
            "Share: %{percent}<extra></extra>"
        )
    ))
    fig_donut.update_layout(
        paper_bgcolor="white",
        margin=dict(l=10, r=10, t=10, b=10), height=280,
        showlegend=False,
        annotations=[dict(
            text=f"<b>{ct['Campaigns'].sum():,}</b><br>total",
            x=0.5, y=0.5, showarrow=False,
            font=dict(size=13, color="#2D2B55")
        )]
    )
    st.plotly_chart(fig_donut, use_container_width=True,
                    config={"displayModeBar": False})

# — Content Type — CTR vs Revenue (eje dual)
with col_c:
    st.markdown("**Content Type — CTR vs Revenue**")
    ct2 = (
        dff.groupby("Content_Type")
        .agg(CTR=("CTR","mean"), Revenue=("Revenue","sum"))
        .reset_index()
        .sort_values("Revenue", ascending=False)
    )
    fig_dual = go.Figure()
    fig_dual.add_trace(go.Bar(
        name="Revenue ($M)",
        x=ct2["Content_Type"],
        y=ct2["Revenue"] / 1e6,
        marker=dict(color=CONTENT_COLORS),
        yaxis="y1",
        text=ct2["Revenue"].apply(lambda x: f"${x/1e6:.1f}M"),
        textposition="outside",
        textfont=dict(size=10),
        hovertemplate="<b>%{x}</b><br>Revenue: $%{y:.2f}M<extra></extra>"
    ))
    fig_dual.add_trace(go.Scatter(
        name="CTR (%)",
        x=ct2["Content_Type"],
        y=ct2["CTR"] * 100,
        mode="lines+markers",
        line=dict(color="#fd7e14", width=2.5),
        marker=dict(size=8, color="#fd7e14"),
        yaxis="y2",
        hovertemplate="<b>%{x}</b><br>CTR: %{y:.1f}%<extra></extra>"
    ))
    fig_dual.update_layout(
        plot_bgcolor="white", paper_bgcolor="white",
        margin=dict(l=10, r=50, t=10, b=10), height=280,
        legend=dict(orientation="h", yanchor="bottom", y=1.02,
                    xanchor="left", x=0, font=dict(size=10)),
        xaxis=dict(tickfont=dict(size=11), showgrid=False),
        yaxis=dict(title="Revenue ($M)", showgrid=True,
                   gridcolor="#f0f0f0", tickfont=dict(size=10),
                   tickformat=".1f"),
        yaxis2=dict(title="CTR (%)", overlaying="y", side="right",
                    tickfont=dict(size=10), showgrid=False,
                    tickformat=".1f")
    )
    st.plotly_chart(fig_dual, use_container_width=True,
                    config={"displayModeBar": False})

st.markdown("---")
st.caption(
    "Built with Python · Streamlit · Plotly  |  "
    "Data: [Kaggle — PPC Campaign Performance Dataset](https://www.kaggle.com/datasets/aashwinkumar/ppc-campaign-performance-data)"
)
