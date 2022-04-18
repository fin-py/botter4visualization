# streamlitによる可視化

streamlitを使うと解析のコードを簡単にweb appにすることができます

## jupyterコードそのままでweb appに

例えばpandasによる可視化のソースコードを次のようにするとweb appにします

```{literalinclude} ./code/streamlit_01.py
:language: python
```

次のように実行します。

```
streamlit run streamlit_01.py
```

```{figure} ./resources/streamlit_01.png
:name: streamlit01
:width: 450px

web browserで見える画面
```

streamlitでweb appにする際にjupyter notebookのコードに加える変更ポイント下記の通りです

- streamlitの読み込み

```{literalinclude} ./code/streamlit_01.py
:language: python
:lines: 1
```

- pandasグラフをstreamlitで表示するようにしていする

```
df_ohlc_btc_eur["close"].plot()
```

を次のように書き換えます

```
fig = df_ohlc_btc_eur["close"].plot()
st.pyplot(fig=fig.figure)
```

## インターラクティブにしてみる

jupyterの結果をwebに表示しただけでは嬉しくないですよね。すこしインターラクティブにしてみましょう。

上のコードではデータのサンプルを設定してました

```
rule = "15min"
```

これを次のようにスライドバーで動かして操作できるようにしましょう

```
interval = st.slider('resample interval(minutes):', 1, 60*24, 15, 1)
rule = '{}min'.format(int(interval))
```

ソースコードは次のようになります

```{literalinclude} ./code/streamlit_02.py
:language: python
```

```{figure} ./resources/streamlit_02.png
:name: streamlit02
:width: 450px

スライドバーの画面
```

スライドバーを動かして、異なる時間スケールで価格をみることができます。

## streamlitの基本

- streamlitの関数を呼び出すことで画面にコンポーネントを配置する。ユーザ入力の値は戻り値として受け取れるので、その値で次の処理を変えることができるので気軽にインターラクティブなものを作れる。
- 書いた順番に実行される

とても手軽である反面、高度なカスタマイズができません。簡単なログインを付けられるが、ごく簡易的なものになります。

概念の検証やツール作成に最適です。

次の課題に対する工夫をすれば強力なものを短期間で作成できます。

- コード実行の順番と画面に表示するものの順番が違う場合に`st.empty()`を使って制御できる。
    - 例：グラフの下にスライドバーを配置し、それを動かすとグラフを変更したい場合
- 画面で何かを動かす度に全部実行されるため、パフォーマンスの問題がある
    - @st.cacheを使って処理を一度しか実行しないようにできる
    - ラジオボタンを設置し、その選択に応じて実行する処理を切り分ける（ページ分けをするイメージ）

詳細については過去の勉強会資料を参照していただきたいです。

[streamlit勉強会](https://fin-py.connpass.com/event/201708/)

## 他の機能など

タイトル、文章、HTMLはそれぞれ次のように配置できます

```
st.title('streamlitによる可視化')
st.markdown('# streamlitによる可視化')
st.components.v1.html('<h1>streamlitによる可視化</h1>')
```

他にボタン、ラジオボタン、セレクト枠、テキスト入力枠、カレンダー入力などのコンポーネントが提供されています。
詳細の使い方は公式ドキュメントがわかりやすいです。

[streamlit document](https://docs.streamlit.io/library/get-started)

## 実践編：ツール化してみる

最後にstreamlitを使って解析ツールを作ってみます

```{figure} ./resources/streamlit_03.png
:name: streamlit03
:width: 450px

解析ツール
```

### ページ分け

様々な可視化を使いたいが、それを一度に全部を表示すると時間がかかってしまうので、
これを複数の画面に分けて、サイドバーで切り替えるようにします。

具体的にはまず各々の処理を関数にまとめ、ユーザ選択に応じて呼び出します。

```
pages = {
    '価格': viz_price,
    '価格＋指標': viz_2nd_axe,
    '出来高': viz_volume
}

page = st.sidebar.radio('画面：', list(pages.keys()))
pages[page]()
```

ここでは価格データを可視化するコードは`viz_price`という関数にまとめています。

### 前処理は一度だけ実行する

関数のまえに次のように書くとその関数は一度だけ呼び出されます。

```
@st.cache
```

注意点：関数内で使用したオブジェクトを書換えないように注意しましょう。データ処理して新しいカラムなどを作成して使う場合にはコピーされたDataframeを使うといいでしょう。

## まとめ

コード
```{literalinclude} ./code/streamlit_03.py
:language: python
```
