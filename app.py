import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go
import numpy as np

# App title and layout
st.set_page_config(page_title="Vijay Stock Guru - Trend Indicators", layout="wide")

st.title("📈 Vijay Stock Guru - Trend Analysis Dashboard")

# User input
symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        if data.empty:
            st.warning("⚠️ No data found! Please check the stock symbol.")
        else:
            # Moving Averages
            data['EMA20'] = data['Close'].ewm(span=20, adjust=False).mean()
            data['EMA50'] = data['Close'].ewm(span=50, adjust=False).mean()
            data['EMA200'] = data['Close'].ewm(span=200, adjust=False).mean()

            # MACD Calculation
            shortEMA = data['Close'].ewm(span=12, adjust=False).mean()
            longEMA = data['Close'].ewm(span=26, adjust=False).mean()
            data['MACD'] = shortEMA - longEMA
            data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()

            # Candlestick chart
            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))

            # Add EMAs
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA20'], line=dict(color='blue', width=1.5), name='EMA 20'))
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA50'], line=dict(color='orange', width=1.5), name='EMA 50'))
            fig.add_trace(go.Scatter(x=data.index, y=data['EMA200'], line=dict(color='green', width=1.5), name='EMA 200'))

            fig.update_layout(
                title=f"{symbol} Trend Chart with EMAs",
                xaxis_rangeslider_visible=False,
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

            # MACD Chart
            macd_fig = go.Figure()
            macd_fig.add_trace(go.Scatter(x=data.index, y=data['MACD'], line=dict(color='purple', width=1.5), name='MACD'))
            macd_fig.add_trace(go.Scatter(x=data.index, y=data['Signal_Line'], line=dict(color='red', width=1.5), name='Signal Line'))

            macd_fig.update_layout(title="MACD Indicator", height=300)
            st.plotly_chart(macd_fig, use_container_width=True)

            # Volume Chart
            vol_fig = go.Figure()
            vol_fig.add_trace(go.Bar(x=data.index, y=data['Volume'], name='Volume'))
            vol_fig.update_layout(title="Volume Chart", height=250)
            st.plotly_chart(vol_fig, use_container_width=True)

            # Trend Detection Message
            st.subheader("📊 Trend Summary:")
            if data['EMA20'].iloc[-1] > data['EMA50'].iloc[-1] > data['EMA200'].iloc[-1]:
                st.success("🚀 Strong Uptrend detected (Bullish Market).")
            elif data['EMA20'].iloc[-1] < data['EMA50'].iloc[-1] < data['EMA200'].iloc[-1]:
                st.error("🔻 Strong Downtrend detected (Bearish Market).")
            else:
                st.info("⚖️ Mixed or Sideways Trend. Wait for confirmation.")

    except Exception as e:
        st.error(f"Error fetching or plotting data: {e}")

else:
    st.info("👉 Please enter a valid stock symbol to begin analysis.")
