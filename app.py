 import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objs as go

# ------------------ PAGE SETTINGS ------------------
st.set_page_config(page_title="📈 Vijay Stock Guru", layout="wide")
st.title("📊 Vijay Stock Guru - Fundamental + Technical Analysis")

# ------------------ USER INPUT ------------------
symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        # Fetch Data
        data = yf.download(symbol, period="6mo", interval="1d")
        info = yf.Ticker(symbol).info

        if data.empty:
            st.warning("⚠️ No data found for this symbol. Please check the name.")
        else:
            # ------------------ FUNDAMENTAL ANALYSIS ------------------
            st.header("🏦 Fundamental Analysis")

            eps = info.get("trailingEps", 0)
            pe = info.get("trailingPE", 0)
            roe = info.get("returnOnEquity", 0)
            book_value = info.get("bookValue", 0)
            market_cap = info.get("marketCap", 0)
            price = info.get("currentPrice", 0)
            growth_rate = info.get("earningsGrowth", 0) or 0.08  # default 8%

            # Intrinsic Value
            intrinsic_value = (eps * (8.5 + 2 * (growth_rate * 100))) * (4.4 / 9)
            if intrinsic_value > 0:
                margin_of_safety = ((intrinsic_value - price) / intrinsic_value) * 100
            else:
                margin_of_safety = 0

            col1, col2, col3 = st.columns(3)
            col1.metric("Market Cap", f"₹ {market_cap/1e7:.2f} Cr")
            col2.metric("Stock P/E", f"{pe}")
            col3.metric("EPS", f"{eps:.2f}")

            col4, col5, col6 = st.columns(3)
            col4.metric("Book Value", f"₹ {book_value}")
            col5.metric("ROE", f"{roe*100:.2f}%")
            col6.metric("Intrinsic Value", f"₹ {intrinsic_value:.2f}")

            st.write(f"🧮 **Margin of Safety:** {margin_of_safety:.2f}%")
            if margin_of_safety > 20:
                st.success("✅ Safe to consider for long-term investment!")
            elif 0 < margin_of_safety <= 20:
                st.info("⚠️ Fairly valued — wait for a dip.")
            else:
                st.error("❌ Overvalued — Avoid for now.")

            # ------------------ TECHNICAL ANALYSIS ------------------
            st.header("📈 Technical Chart & Signals")

            # Simple Moving Averages
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()

            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name="Price"
            ))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='orange', width=1.5), name='SMA 20'))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], line=dict(color='blue', width=1.5), name='SMA 50'))

            fig.update_layout(title=f"{symbol} - Price Chart", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # ------------------ SIGNALS ------------------
            st.subheader("📊 Signals")

            latest_close = data['Close'].iloc[-1]
            sma20 = data['SMA20'].iloc[-1]
            sma50 = data['SMA50'].iloc[-1]

            if sma20 > sma50:
                st.success("🚀 Bullish Crossover (Uptrend)")
            elif sma20 < sma50:
                st.error("🔻 Bearish Crossover (Downtrend)")
            else:
                st.info("➖ Neutral Trend")

            # Volume check
            avg_vol = data['Volume'].mean()
            latest_vol = data['Volume'].iloc[-1]
            if latest_vol > 1.5 * avg_vol:
                st.warning("💥 High Volume Detected!")

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")

else:
    st.info("Please enter a stock symbol to start analysis.")
