import dash
from dash import dcc, html
import plotly.express as px

fig = px.line(x=[1, 2, 3], y=[3, 5, 2], width=400, height=400)
text = """
#### この部分はMarkdown記法で記述しています

- リスト1
- リスト2

---

```
app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [html.H1("見出し1")],
            id="inner1",
        ),
        html.Div(
            [
                dcc.Markdown(text, style={"display": "inline-block"}),
                dcc.Graph(figure=fig, style={"display": "inline-block"}),
            ],
            id="inner2",
        ),
    ],
    id="outer",
)

if __name__ == "__main__":
    app.run_server(debug=True)
```

"""

app = dash.Dash(__name__)
app.layout = html.Div(
    [
        html.Div(
            [html.H1("Markdownとグラフ")],
            id="inner1",
        ),
        html.Div(
            [
                dcc.Markdown(text, style={"display": "inline-block"}),
                dcc.Graph(figure=fig, style={"display": "inline-block"}),
            ],
            id="inner2",
        ),
    ],
    id="outer",
)

if __name__ == "__main__":
    app.run_server(debug=True)
