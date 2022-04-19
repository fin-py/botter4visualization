import dash
from dash import html

app = dash.Dash(__name__)

app.layout = html.Div(
    [
        html.Div(
            [html.H1("見出し1")],
            id="inner1",
        ),
        html.Div(
            [
                html.H2("見出し2", style={"display": "inline-block"}),
                html.Img(
                    src="https://www.asakura.co.jp/user_data/product_image/12258/1.jpg",
                    style={"display": "inline-block"},
                ),
            ],
            id="inner2",
        ),
    ],
    id="outer",
)

if __name__ == "__main__":
    app.run_server(debug=True)
