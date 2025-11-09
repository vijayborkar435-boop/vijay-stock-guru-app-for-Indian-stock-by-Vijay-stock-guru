import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(page_title="Vijay Stock Guru", layout="wide")

st.title("📈 Vijay Stock Guru - Breakout & Volume Analysis")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        if data.empty:
            st.warning("⚠️ No data found for this symbol! Please check the symbol name (e.g., RELIANCE.NS)")
        else:
            st.subheader(f"Stock Data for {symbol}")
            st.write(data.tail())

            # Chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))
            fig.update_layout(title=f"{symbol} - Stock Chart", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # Breakout detection
            data['Prev_High'] = data['High'].shift(1)
            data['Prev_Low'] = data['Low'].shift(1)

            latest_close = data['Close'].iloc[-1]
            latest_high = data['High'].iloc[-1]
            prev_high = data['Prev_High'].iloc[-1]

            if (latest_high > prev_high) and (latest_close > prev_high):
                st.success("🚀 Bullish Breakout detected!")
            else:
                st.info("📊 No breakout yet, keep watching...")

            # Volume Analysis
            avg_volume = data['Volume'].mean()
            latest_volume = data['Volume'].iloc[-1]

            if latest_volume > 1.5 * avg_volume:
                st.warning("💥 High Volume detected today!")
            else:
                st.info("📈 Normal Volume.")

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {str(e)}")

else:
    st.info("👉 Please enter a valid NSE stock symbol (e.g., RELIANCE.NS)")
