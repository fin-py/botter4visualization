import streamlit as st
import pandas as pd

df_eth_eur = pd.read_pickle("../../data/binance_btc-eur.pkl")
df_btc_eur = pd.read_pickle("../../data/binance_eth-eur.pkl")

df_btc_eur.head()

st.write(df_btc_eur.info())

rule = "15min"
df_ohlc_btc_eur = df_btc_eur["price"].resample(rule, label="right").ohlc()
df_ohlc_btc_eur["volume"] = df_btc_eur["size"].resample(rule, label="right").sum()

df_ohlc_eth_eur = df_eth_eur["price"].resample(rule, label="right").ohlc()
df_ohlc_eth_eur["volume"] = df_eth_eur["size"].resample(rule, label="right").sum()

df_ohlc_btc_eur.head()

fig = df_ohlc_btc_eur["close"].plot()
st.pyplot(fig=fig.figure)


fig = df_ohlc_btc_eur["close"].plot(
    grid=True, # 罫線
    figsize=(30,5),  # 描画サイズ（横、縦）
    title="Close",  # グラフタイトル
    legend=True,  # 凡例
    rot=45,  # xtick の ローテーション
    fontsize=15, # 文字サイズ
    style={"close": "g--"}, # 色と線の種類
)
st.pyplot(fig=fig.figure)

