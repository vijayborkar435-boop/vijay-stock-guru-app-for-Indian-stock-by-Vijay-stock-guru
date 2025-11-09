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

        # If no data
        if data.empty:
            st.error("⚠️ No data found for this symbol! Check spelling (e.g., RELIANCE.NS, TCS.NS)")
            st.stop()

        # Show data
        st.subheader(f"📊 Latest Stock Data for {symbol}")
        st.dataframe(data.tail(), use_container_width=True)

        # -------------------- CANDLESTICK CHART --------------------
        data = data.reset_index()
        fig = go.Figure(data=[go.Candlestick(
            x=data['Date'],
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Price'
        )])

        fig.update_layout(
            title=f"{symbol} - 6 Months Chart",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            template="plotly_white",
            xaxis_rangeslider_visible=False,
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------- BREAKOUT DETECTION --------------------
        data['Prev_High'] = data['High'].shift(1)

        latest_row = data.iloc[-1]
        prev_row = data.iloc[-2]

        latest_close = float(latest_row['Close'])
        latest_high = float(latest_row['High'])
        prev_high = float(prev_row['High'])

        if (latest_high > prev_high) and (latest_close > prev_high):
            st.success("🚀 Bullish Breakout detected! Possible upward movement.")
        else:
            st.info("📊 No breakout yet. Keep watching the stock.")

        # -------------------- VOLUME ANALYSIS --------------------
        avg_volume = data['Volume'].mean()
        latest_volume = float(latest_row['Volume'])

        if latest_volume > 1.5 * avg_volume:
            st.warning("💥 High trading volume today! Watch for big move.")
        else:
            st.write("🔸 Normal trading volume.")

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")

else:
    st.info("👉 Please enter a valid NSE stock symbol (like RELIANCE.NS or TCS.NS).")
