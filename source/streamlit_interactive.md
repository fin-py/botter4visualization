# streamlitによる可視化

streamlitを使うと解析のコードを簡単にweb appにすることができます

## まずはjupyter notebookのコードをそのままweb appにしてみまししょう

例えばpandasによる可視化を次のようにするとweb appにします

```{literalinclude} ./code/streamlit_01.py
:language: python
```

実行する時は

```
streamlit run streamlit_01.py
```
のようにします。

jupyter notebookのコードに加える変更ポイント

- streamlitの読み込む

```{literalinclude} ./code/streamlit_01.py
:language: python
:lines: 1
```

- pandasグラフをstreamlitで表示する

```
df_ohlc_btc_eur["close"].plot()
```

を次のように書き換えます

```
fig = df_ohlc_btc_eur["close"].plot()
st.pyplot(fig=fig.figure)
```

## ちょっとだけインターラクティブにしてみる

これだとjupyterの結果を表示しただけなので嬉しくないですよね。すこしインターラクティブにしましょう。

上のコードでデータのサンプルを設定してました

```
rule = "15min"
```

これを次のようにスライドバーで動かして操作できるようにしましょう

```
interval = st.slider('resample interval(minutes):', 1, 60*24, 15, 1)
rule = '{}min'.format(int(interval))
```

