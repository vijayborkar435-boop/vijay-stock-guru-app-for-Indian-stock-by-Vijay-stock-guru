import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objects as go

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Vijay Stock Guru", layout="wide")

st.title("📈 Vijay Stock Guru - Breakout & Volume Analysis")
st.markdown("Made with ❤️ by Vijay Stock Guru")

# -------------------- USER INPUT --------------------
symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        # Download stock data
        data = yf.download(symbol, period="6mo", interval="1d")
        data.dropna(inplace=True)

        # Check if empty
        if data.empty:
            st.error("⚠️ No data found for this symbol! Please check (e.g., RELIANCE.NS, TCS.NS)")
            st.stop()

        # Show latest few rows
        st.subheader(f"📊 Stock Data for {symbol}")
        st.dataframe(data.tail(), use_container_width=True)

        # -------------------- FIXED CHART SECTION --------------------
        data.reset_index(inplace=True)
        data['Date'] = pd.to_datetime(data['Date'])

        fig = go.Figure(data=[go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        )])

        fig.update_layout(
            title=f"{symbol} - Last 6 Months Chart",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            template="plotly_dark",
            xaxis_rangeslider_visible=True,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------- BREAKOUT DETECTION --------------------
        data['Prev_High'] = data['High'].shift(1)
        latest_close = float(data['Close'].iloc[-1])
        latest_high = float(data['High'].iloc[-1])
        prev_high = float(data['Prev_High'].iloc[-1])

        # ✅ FIXED: Explicit comparison (no Series ambiguity)
        if (latest_high > prev_high) and (latest_close > prev_high):
            st.success("🚀 Bullish Breakout detected! Possible upward movement.")
        else:
            st.info("📊 No breakout yet. Keep watching for resistance breakout.")

        # -------------------- VOLUME ANALYSIS --------------------
        avg_volume = data['Volume'].mean()
        latest_volume = data['Volume'].iloc[-1]

        if latest_volume > 1.5 * avg_volume:
            st.warning("💥 High volume detected today! Could be strong move ahead.")
        else:
            st.write("🔸 Normal trading volume today.")

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")
else:
    st.info("👉 Please enter a valid NSE stock symbol (e.g., RELIANCE.NS).")
