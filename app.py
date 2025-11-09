import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# -----------------------------------------------------------
# App Configuration
# -----------------------------------------------------------
st.set_page_config(page_title="Vijay Stock Guru", layout="wide")
st.title("📈 Vijay Stock Guru - Breakout & Volume Analysis")

# -----------------------------------------------------------
# Input Section
# -----------------------------------------------------------
symbol = st.text_input(
    "Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):",
    "RELIANCE.NS"
)

# -----------------------------------------------------------
# Main Logic
# -----------------------------------------------------------
if symbol:
    try:
        # Download stock data
        data = yf.download(symbol, period="6mo", interval="1d")

        if data is None or data.empty:
            st.error("❌ No data found! Please check the stock symbol.")
        else:
            # Show data
            st.subheader(f"📊 Latest Stock Data for {symbol}")
            st.dataframe(data.tail())

            # -----------------------------------------------------------
            # Candlestick Chart
            # -----------------------------------------------------------
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data["Open"],
                high=data["High"],
                low=data["Low"],
                close=data["Close"],
                name="Candlestick"
            )])
            fig.update_layout(
                title=f"{symbol} - 6 Month Candlestick Chart",
                xaxis_rangeslider_visible=False,
                template="plotly_dark"
            )
            st.plotly_chart(fig, use_container_width=True)

            # -----------------------------------------------------------
            # Breakout Detection
            # -----------------------------------------------------------
            if len(data) >= 2:
                latest_high = float(data["High"].iloc[-1])
                latest_close = float(data["Close"].iloc[-1])
                prev_high = float(data["High"].iloc[-2])

                if (latest_high > prev_high) and (latest_close > prev_high):
                    st.success("🚀 Bullish Breakout Detected!")
                else:
                    st.info("📊 No breakout yet, keep watching.")
            else:
                st.warning("⚠️ Not enough data for breakout detection.")

            # -----------------------------------------------------------
            # Volume Analysis
            # -----------------------------------------------------------
            avg_volume = float(data["Volume"].mean())
            latest_volume = float(data["Volume"].iloc[-1])

            if latest_volume > 1.5 * avg_volume:
                st.warning("💥 High volume detected today!")
            else:
                st.info("📈 Normal trading volume today.")

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {str(e)}")

else:
    st.info("Please enter a stock symbol to start analysis.")
