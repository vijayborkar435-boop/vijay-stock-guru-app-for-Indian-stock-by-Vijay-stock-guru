import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

# -------------------- PAGE CONFIG --------------------
st.set_page_config(page_title="Vijay Stock Guru", layout="wide")

st.title("📈 Vijay Stock Guru - Breakout & Volume Analysis")
st.markdown("Made with ❤️ by Vijay Stock Guru")

# -------------------- USER INPUT --------------------
symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

# -------------------- MAIN APP --------------------
if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        data.dropna(inplace=True)

        # ✅ Check if data is empty
        if data.empty:
            st.error("⚠️ No data found for this symbol! Please check the symbol name (e.g., RELIANCE.NS, TCS.NS).")
            st.stop()

        # -------------------- DISPLAY STOCK DATA --------------------
        st.subheader(f"📊 Stock Data for {symbol}")
        st.dataframe(data.tail(), use_container_width=True)

        # -------------------- PLOTLY CANDLESTICK CHART --------------------
        fig = go.Figure()
        fig.add_trace(go.Candlestick(
            x=data.index,
            open=data['Open'],
            high=data['High'],
            low=data['Low'],
            close=data['Close'],
            name='Candlestick'
        ))

        fig.update_layout(
            title=f"{symbol} - Last 6 Months",
            xaxis_title="Date",
            yaxis_title="Price (₹)",
            xaxis_rangeslider_visible=False,
            template="plotly_dark",
            height=600
        )

        st.plotly_chart(fig, use_container_width=True)

        # -------------------- BREAKOUT DETECTION --------------------
        data['Prev_High'] = data['High'].shift(1)
        data['Prev_Low'] = data['Low'].shift(1)

        # Safely get last 2 rows
        latest_row = data.iloc[-1]
        prev_row = data.iloc[-2] if len(data) > 1 else data.iloc[-1]

        latest_close = latest_row['Close']
        latest_high = latest_row['High']
        prev_high = prev_row['High']

        if (latest_high > prev_high) and (latest_close > prev_high):
            st.success("🚀 Bullish Breakout detected! This stock may be ready for upward movement.")
        else:
            st.info("📊 No breakout yet. Keep watching for strong movement above recent highs.")

        # -------------------- VOLUME ANALYSIS --------------------
        avg_volume = data['Volume'].mean()
        latest_volume = latest_row['Volume']

        if latest_volume > 1.5 * avg_volume:
            st.warning("💥 High volume detected today! (Possible strong move)")
        else:
            st.write("🔸 Normal volume activity today.")

    except Exception as e:
        st.error(f"⚠️ Error fetching data: {e}")

else:
    st.info("👉 Please enter a valid stock symbol to start analysis.")
