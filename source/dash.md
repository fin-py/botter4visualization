# Dash

DashではHTMLのタグをPythonのオブジェクトとして構成できます
## レイアウト

```{literalinclude} ./code/dash_layout.py
:language: python
:caption: dash_layout.py
```

`dash_layout.py` を実行すると、 {numref}`dash_layout` のように描画されます

```{figure} ./resources/dash_layout.png
:name: dash_layout

Dashのレイアウト
```

## Markdown・グラフ

HTMLタグのほか、Markdown記法で書かれたテキストや、Plotlyで記述したグラフをレイアウトできます

```{literalinclude} ./code/dash_figure.py
:language: python
:caption: dash_figure.py
```

`dash_figure.py` を実行すると、 {numref}`md_figure` のように描画されます

```{figure} ./resources/md_figure.png
:name: md_figure

Markdownとグラフ
```