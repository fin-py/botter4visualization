import streamlit as st
import datetime
import pandas as pd
import logging
import ta
import matplotlib.pyplot as plt

logging.basicConfig(level=logging.INFO,
                    format="%(asctime)s %(levelname)s %(message)s",
                    datefmt="%m/%d/%Y %X")
st.set_page_config(layout='wide')


# 前処理を一度だけ実行するようにする
@st.cache(allow_output_mutation=True)
def pre_process():
    logging.info('load data')
    df_eth_eur = pd.read_pickle("../../data/binance_btc-eur_bk.pkl")
    df_btc_eur = pd.read_pickle("../../data/binance_eth-eur_bk.pkl")

    rule = '15min'
    df_ohlc_btc_eur = df_btc_eur["price"].resample(rule, label="right").ohlc()
    df_ohlc_btc_eur["volume"] = df_btc_eur["size"].resample(rule, label="right").sum()
    df_ohlc_btc_eur["RSI14"] = ta.momentum.rsi(df_ohlc_btc_eur["close"], window=14)

    df_ohlc_eth_eur = df_eth_eur["price"].resample(rule, label="right").ohlc()
    df_ohlc_eth_eur["volume"] = df_eth_eur["size"].resample(rule, label="right").sum()
    df_ohlc_eth_eur["RSI14"] = ta.momentum.rsi(df_ohlc_btc_eur["close"], window=14)

    return df_eth_eur, df_btc_eur, df_ohlc_eth_eur, df_ohlc_btc_eur


# 価格の可視化
def viz_price():
    interval = st.slider('interval(minutes):', 1, 60*24, 15, 1)
    # どの銘柄をみるか選べるようにする
    token = st.radio('coin:', ['eth', 'btc'])
    rule = '{}min'.format(int(interval))

    if token == 'btc':
        # 注意点: st.cacheで指定した関数内のオブジェクトは書換えないようにしましましょう。
        # 値を代入したりする場合は元のdataframeをコピーして、それを使う
        df_view = df_btc_eur["price"].resample(rule, label="right").ohlc()
        df_view["volume"] = df_btc_eur["size"].resample(rule, label="right").sum()
    elif token == 'eth':
        df_view = df_eth_eur["price"].resample(rule, label="right").ohlc()
        df_view["volume"] = df_eth_eur["size"].resample(rule, label="right").sum()

    fig = df_view["close"].plot()
    st.pyplot(fig=fig.figure)

    fig = df_view["close"].plot(
        grid=True, # 罫線
        figsize=(30,5),  # 描画サイズ（横、縦）
        title="Close",  # グラフタイトル
        legend=True,  # 凡例
        rot=45,  # xtick の ローテーション
        fontsize=15, # 文字サイズ
        style={"close": "g--"}, # 色と線の種類
    )
    st.pyplot(fig=fig.figure)


def viz_2nd_axe():
    index = st.radio('2nd axe:', ['RSI14', 'volume'])
    if_change_window = st.checkbox('指標算出の窓を変える')

    if not if_change_window:
        figs = df_ohlc_btc_eur[["close", index]].plot(
            grid=True,
            figsize=(30,20),
            title="Close & {}".format(index),
            legend=True,
            subplots=True,
            layout=(2,1), # レイアウト（行,欄）
        )
        st.pyplot(fig=figs[0, 0].figure)
    else:
        window = st.slider('window:', 1, 100, 14, 1)
        window = int(window)
        rule = '{}min'.format(window)
        df_view = df_btc_eur["price"].resample(rule, label="right").ohlc()
        if index == 'volume':
            df_view["volume_flex"] = df_btc_eur["size"].resample(rule, label="right").sum()
        elif index == 'RSI14':
            df_view["RSI14_flex"] = ta.momentum.rsi(df_view["close"], window=window)
        figs = df_view[["close", index + '_flex']].plot(
            grid=True,
            figsize=(30,20),
            title="Close & {}_flex".format(index),
            legend=True,
            subplots=True,
            layout=(2,1), # レイアウト（行,欄）
        )
        st.pyplot(fig=figs[0, 0].figure)
        st.dataframe(df_view)


def viz_volume():
    date_start = st.date_input('start:', datetime.datetime(2022, 3, 1))
    date_end = st.date_input('end:', datetime.datetime(2022, 3, 31))
    df_15min = df_btc_eur["price"].resample("15min", label="right").ohlc()
    df_15min["volume"] = df_btc_eur["size"].resample("15min", label="right").sum()
    df_15min["pricecut"] = pd.cut(df_15min["close"], 30, ).apply(lambda x: x.left)
    df_15min = df_15min.loc[date_start: date_end]
    s_vol_by_price = df_15min.groupby("pricecut")["volume"].sum()
    fig, axes = plt.subplots(1, 2, figsize=(20, 5), constrained_layout = True)
    df_15min["close"].plot(ax=axes[0], yticks=s_vol_by_price.index, grid=True)
    fig = s_vol_by_price.plot(kind="barh",ax=axes[1],sharey=axes[0], grid=True)
    st.pyplot(fig=fig.figure)


df_eth_eur, df_btc_eur, df_ohlc_eth_eur, df_ohlc_btc_eur = pre_process()
st.title('Botterのためのデータ可視化入門、streamlitの巻')

pages = {
    '価格': viz_price,
    '価格＋指標': viz_2nd_axe,
    '出来高': viz_volume
}

page = st.sidebar.radio('画面：', list(pages.keys()))
pages[page]()
