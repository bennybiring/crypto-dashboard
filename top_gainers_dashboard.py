import requests
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Top Gainers Crypto Dashboard", layout="wide")
st.title("Top 10 Gainers - Multi Exchange")

@st.cache_data
def get_binance():
    url = "https://api.binance.com/api/v3/ticker/24hr"
    data = requests.get(url).json()
    coins = [x for x in data if x["symbol"].endswith("USDT")]
    sorted_coins = sorted(coins, key=lambda x: float(x["priceChangePercent"]), reverse=True)
    top10 = sorted_coins[:10]
    return pd.DataFrame([(x["symbol"], float(x["priceChangePercent"])) for x in top10],
                        columns=["Symbol", "Change (%)"])

@st.cache_data
def get_kucoin():
    url = "https://api.kucoin.com/api/v1/market/allTickers"
    data = requests.get(url).json()["data"]["ticker"]
    coins = [x for x in data if x["symbol"].endswith("-USDT")]
    sorted_coins = sorted(coins, key=lambda x: float(x["changeRate"]), reverse=True)
    top10 = sorted_coins[:10]
    return pd.DataFrame([(x["symbol"], float(x["changeRate"]) * 100) for x in top10],
                        columns=["Symbol", "Change (%)"])

@st.cache_data
def get_okx():
    url = "https://www.okx.com/api/v5/market/tickers?instType=SPOT"
    data = requests.get(url).json()["data"]
    coins = [x for x in data if x["instId"].endswith("USDT")]
    sorted_coins = sorted(coins, key=lambda x: float(x["chg"]), reverse=True)
    top10 = sorted_coins[:10]
    return pd.DataFrame([(x["instId"], float(x["chg"]) * 100) for x in top10],
                        columns=["Symbol", "Change (%)"])

# Layout 3 kolom
col1, col2, col3 = st.columns(3)

with col1:
    st.subheader("Binance")
    st.dataframe(get_binance(), use_container_width=True)

with col2:
    st.subheader("KuCoin")
    st.dataframe(get_kucoin(), use_container_width=True)

with col3:
    st.subheader("OKX")
    st.dataframe(get_okx(), use_container_width=True)
