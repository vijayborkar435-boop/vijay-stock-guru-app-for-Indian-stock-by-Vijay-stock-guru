 import streamlit as st
import yfinance as yf
import pandas as pd

# -------------------------------------------------------
# 📊 Vijay Stock Guru - Final App v2 (With Volume Breakout)
# -------------------------------------------------------

st.set_page_config(page_title="Vijay Stock Guru", page_icon="📈", layout="wide")

st.title("📈 Vijay Stock Guru - Fundamental + Technical + Volume Breakout")

# User Input
stock_symbol = st.text_input("Enter NSE Stock Symbol (e.g. TCS.NS, RELIANCE.NS):", "RELIANCE.NS")

if stock_symbol:
    try:
        stock = yf.Ticker(stock_symbol)
        info = stock.info
        hist = stock.history(period="6mo")

        if hist.empty:
            st.warning("No historical data found for this stock. Try another symbol.")
        else:
            # ---------------------------------
            # 🧾 Fundamental Data
            st.subheader("🏢 Company Fundamentals")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
                st.write(f"**Sector:** {info.get('sector', 'N/A')}")
                st.write(f"**Market Cap:** ₹{info.get('marketCap', 'N/A')}")
            with col2:
                st.write(f"**PE Ratio:** {info.get('trailingPE', 'N/A')}")
                st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
                st.write(f"**Book Value:** {info.get('bookValue', 'N/A')}")
            with col3:
                st.write(f"**52 Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
                st.write(f"**52 Week Low:** {info.get('fiftyTwoWeekLow', 'N/A')}")
                st.write(f"**Dividend Yield:** {info.get('dividendYield', 'N/A')}")

            # ---------------------------------
            # 📉 Technical Indicators
            st.subheader("📊 Technical Analysis")

            hist['SMA20'] = hist['Close'].rolling(window=20).mean()
            hist['SMA50'] = hist['Close'].rolling(window=50).mean()

            delta = hist['Close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            hist['RSI'] = 100 - (100 / (1 + rs))

            # ---------------------------------
            # 🔍 Volume Breakout Detection
            hist['AvgVol20'] = hist['Volume'].rolling(window=20).mean()
            latest = hist.iloc[-1]
            prev = hist.iloc[-2] if len(hist) > 1 else latest

            breakout = ""
            if (
                latest['Volume'] > 2 * latest['AvgVol20']
                and latest['Close'] > latest['SMA20']
            ):
                breakout = "🚀 High Volume Breakout Detected!"
            elif latest['Volume'] > 1.5 * latest['AvgVol20']:
                breakout = "📊 Volume Rising — Possible Breakout soon."
            else:
                breakout = "📉 No breakout currently."

            # ---------------------------------
            # 🧾 Display Tables
            st.write("### Latest Technical Data")
            st.dataframe(hist[['Close', 'Volume', 'AvgVol20', 'SMA20', 'SMA50', 'RSI']].tail(10))

            # ---------------------------------
            # 📢 Signal Suggestion
            signal = ""
            if latest['RSI'] < 30 and latest['Close'] > latest['SMA20'] > latest['SMA50']:
                signal = "🟢 Strong Buy (Oversold & Above Averages)"
            elif latest['RSI'] < 40 and latest['Close'] > latest['SMA20']:
                signal = "🟢 Buy Signal"
            elif latest['RSI'] > 70 and latest['Close'] < latest['SMA20']:
                signal = "🔴 Sell Signal"
            elif latest['RSI'] > 60 and latest['SMA20'] < latest['SMA50']:
                signal = "🔴 Weak Sell (Trend Weakening)"
            else:
                signal = "🟡 Hold / Neutral"

            st.subheader("📢 Signal Suggestion")
            st.success(signal)

            # ---------------------------------
            # 💥 Breakout Status
            st.subheader("🔥 Breakout Detector")
            if "Breakout" in breakout:
                st.success(breakout)
            elif "Possible" in breakout:
                st.warning(breakout)
            else:
                st.info(breakout)

            # ---------------------------------
            # 📈 Chart
            st.subheader("Stock Price Chart with SMA20 & SMA50")
            st.line_chart(hist[['Close', 'SMA20', 'SMA50']])

    except Exception as e:
        st.error(f"Error loading data: {e}")               
