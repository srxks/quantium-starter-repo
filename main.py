import pandas as pd
from dash import Dash, html, dcc
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

# Create chart
fig = px.line(
    df,
    x="date",
    y="sales",
    color="region",
    title="Sales vs Date by Region",
    markers=True
)

# Dash app
app = Dash(__name__)

app.layout = html.Div([
    html.H1("Sales Dashboard"),

    dcc.Graph(
        figure=fig
    )
])

if __name__ == "__main__":
    app.run(debug=True)