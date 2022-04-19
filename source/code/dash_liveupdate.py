import dash
import pandas as pd
import plotly.graph_objs as go
from dash import dcc, html
from dash.dependencies import Input, Output

data = pd.read_pickle("../../data/btcusd_2020-07-08.pickle")
data_iter = iter(data.groupby("timestamp"))

app = dash.Dash(__name__)
app.layout = html.Div(
    html.Div(
        [
            html.H4("BTCUSD"),
            html.Div(id="live-update-text"),
            dcc.Graph(id="live-graph", animate=True),
            dcc.Interval(id="interval-component", interval=1000, n_intervals=0),
        ]
    )
)


@app.callback(
    Output("live-update-text", "children"),
    Output("live-graph", "figure"),
    Input("interval-component", "n_intervals"),
)
def update_graph_scatter(n):
    t, df = next(data_iter)
    timestamp = [html.P(f"timestamp: {t}")]

    groupby_side = df.groupby("side")
    bid = groupby_side.get_group("bid")
    ask = groupby_side.get_group("ask")
    fig = go.Figure()
    fig.add_trace(
        go.Bar(x=bid.loc[:, "size"], y=bid.loc[:, "price"], orientation="h", name="bid")
    )
    fig.add_trace(
        go.Bar(x=ask.loc[:, "size"], y=ask.loc[:, "price"], orientation="h", name="ask")
    )
    fig.update_layout(
        width=600,
        height=800,
        xaxis={"range": [0, df.loc[:, "size"].max()]},
        yaxis={"range": [df.loc[:, "price"].min(), df.loc[:, "price"].max()]},
    )
    return timestamp, fig


if __name__ == "__main__":
    app.run_server()
