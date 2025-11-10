import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="📈 Vijay Stock Guru", layout="wide")
st.title("📊 Vijay Stock Guru - Fundamental + Technical Analysis")

symbol = st.text_input("Enter NSE Symbol (e.g. RELIANCE.NS, TCS.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        if data.empty:
            st.warning("⚠️ No data found. Please check symbol.")
        else:
            st.subheader("📈 Technical Chart")

            # Calculate Moving Averages
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()

            # Plotly chart (tested version)
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))
            fig.add_trace(go.Scatter(
                x=data.index, y=data['SMA20'],
                line=dict(color='orange', width=1.5),
                name='SMA 20'
            ))
            fig.add_trace(go.Scatter(
                x=data.index, y=data['SMA50'],
                line=dict(color='blue', width=1.5),
                name='SMA 50'
            ))

            fig.update_layout(
                title=f"{symbol} Price Chart",
                xaxis_rangeslider_visible=False,
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # Basic Signals
            latest_close = data['Close'].iloc[-1]
            sma20 = data['SMA20'].iloc[-1]
            sma50 = data['SMA50'].iloc[-1]

            if sma20 > sma50:
                st.success("🚀 Bullish Crossover - Uptrend Signal")
            elif sma20 < sma50:
                st.error("🔻 Bearish Crossover - Downtrend Signal")
            else:
                st.info("➖ Neutral Signal")

    except Exception as e:
        st.error(f"Error: {e}")
else:
    st.info("Enter stock symbol to begin analysis.")
