# streamlitでインターラクティブ可視化

# まずはjupyter notebookのコードをそのままweb appにしてみよう

コード
```{literalinclude} ./code/streamlit_static.py
:language: python
```

jupyter notebookからの変更点

- streamlitを読み込む

```{literalinclude} ./code/streamlit_static.py
:language: python
:lines: 1
```

- グラフをstreamlitに表示するおまじない

```
df_ohlc_btc_eur["close"].plot()
```

を次のように書き換える

```
fig = df_ohlc_btc_eur["close"].plot()
st.pyplot(fig=fig.figure)
```


