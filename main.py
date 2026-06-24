import pandas as pd
from dash import Dash, html, dcc, Input, Output, callback
import plotly.express as px

# Read CSV
df = pd.read_csv("final.csv")

# Clean data
df["sales"] = (
    df["sales"]
    .str.replace("$", "", regex=False)
    .astype(float)
)

df["date"] = pd.to_datetime(df["date"])

# Color palette per region
REGION_COLORS = {
    "north": "#4FC3F7",
    "east":  "#81C784",
    "south": "#FFB74D",
    "west":  "#CE93D8",
}

# ── App ──────────────────────────────────────────────────────────────────────
app = Dash(__name__)

app.layout = html.Div(
    style={
        "minHeight": "100vh",
        "background": "linear-gradient(135deg, #0f0c29, #302b63, #24243e)",
        "fontFamily": "'Segoe UI', sans-serif",
        "padding": "40px 60px",
    },
    children=[

        # ── Header ──
        html.Div(
            style={
                "textAlign": "center",
                "marginBottom": "36px",
            },
            children=[
                html.H1(
                    "🍬 Soul Foods — Pink Morsels",
                    style={
                        "color": "#f9a8d4",
                        "fontSize": "2.6rem",
                        "fontWeight": "800",
                        "letterSpacing": "1px",
                        "margin": "0 0 6px 0",
                        "textShadow": "0 0 18px rgba(249,168,212,0.55)",
                    },
                ),
                html.P(
                    "Regional Sales Dashboard",
                    style={
                        "color": "#a78bfa",
                        "fontSize": "1.1rem",
                        "margin": 0,
                        "letterSpacing": "2px",
                        "textTransform": "uppercase",
                    },
                ),
            ],
        ),

        # ── Filter card ──
        html.Div(
            style={
                "background": "rgba(255,255,255,0.06)",
                "border": "1px solid rgba(255,255,255,0.12)",
                "borderRadius": "16px",
                "padding": "20px 32px",
                "marginBottom": "28px",
                "display": "flex",
                "alignItems": "center",
                "gap": "24px",
                "backdropFilter": "blur(8px)",
            },
            children=[
                html.Label(
                    "Filter by Region",
                    style={
                        "color": "#e0e7ff",
                        "fontWeight": "600",
                        "fontSize": "0.95rem",
                        "whiteSpace": "nowrap",
                        "letterSpacing": "0.5px",
                    },
                ),
                dcc.RadioItems(
                    id="region-filter",
                    options=[
                        {"label": "🌍  All",   "value": "all"},
                        {"label": "🧊  North", "value": "north"},
                        {"label": "🌿  East",  "value": "east"},
                        {"label": "☀️  South", "value": "south"},
                        {"label": "🌄  West",  "value": "west"},
                    ],
                    value="all",
                    inline=True,
                    inputStyle={
                        "marginRight": "6px",
                        "accentColor": "#f9a8d4",
                        "cursor": "pointer",
                    },
                    labelStyle={
                        "color": "#e0e7ff",
                        "fontSize": "0.95rem",
                        "marginRight": "28px",
                        "cursor": "pointer",
                        "userSelect": "none",
                    },
                ),
            ],
        ),

        # ── Chart card ──
        html.Div(
            style={
                "background": "rgba(255,255,255,0.05)",
                "border": "1px solid rgba(255,255,255,0.10)",
                "borderRadius": "20px",
                "padding": "24px",
                "boxShadow": "0 8px 32px rgba(0,0,0,0.45)",
                "backdropFilter": "blur(8px)",
            },
            children=[
                dcc.Graph(id="sales-chart"),
            ],
        ),

        # ── Footer ──
        html.P(
            "Data refreshed from final.csv  ·  Soul Foods Internal Analytics",
            style={
                "color": "rgba(255,255,255,0.25)",
                "textAlign": "center",
                "marginTop": "28px",
                "fontSize": "0.78rem",
                "letterSpacing": "0.5px",
            },
        ),
    ],
)


@callback(
    Output("sales-chart", "figure"),
    Input("region-filter", "value"),
)
def update_chart(selected_region):
    if selected_region == "all":
        filtered = df
        color_map = REGION_COLORS
    else:
        filtered = df[df["region"] == selected_region]
        color_map = {selected_region: REGION_COLORS.get(selected_region, "#f9a8d4")}

    fig = px.line(
        filtered,
        x="date",
        y="sales",
        color="region",
        color_discrete_map=color_map,
        title=f"Sales Over Time — {selected_region.title()}",
        markers=True,
        labels={"sales": "Sales (USD)", "date": "Date", "region": "Region"},
    )

    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font_color="#e0e7ff",
        title_font_size=18,
        title_font_color="#f9a8d4",
        legend=dict(
            bgcolor="rgba(255,255,255,0.07)",
            bordercolor="rgba(255,255,255,0.15)",
            borderwidth=1,
            font_color="#e0e7ff",
        ),
        xaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            linecolor="rgba(255,255,255,0.15)",
            tickfont_color="#a78bfa",
        ),
        yaxis=dict(
            gridcolor="rgba(255,255,255,0.08)",
            linecolor="rgba(255,255,255,0.15)",
            tickfont_color="#a78bfa",
            tickprefix="$",
        ),
        hovermode="x unified",
        margin=dict(l=20, r=20, t=50, b=20),
    )

    fig.update_traces(
        line=dict(width=2.5),
        marker=dict(size=7),
    )

    return fig


if __name__ == "__main__":
    app.run(debug=True)