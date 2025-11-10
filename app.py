 import streamlit as st
import yfinance as yf
import pandas as pd

# ---------------------------------
# 📊 App Title
st.title("📈 Vijay Stock Guru - Fundamental + Technical Analysis")

# ---------------------------------
# 🧠 User Input
stock_symbol = st.text_input("Enter Stock Symbol (e.g. TCS.NS, RELIANCE.NS):", "RELIANCE.NS")

# ---------------------------------
# 📥 Fetch Data
try:
    stock = yf.Ticker(stock_symbol)
    info = stock.info
    hist = stock.history(period="6mo")

    # Fundamental Info
    st.subheader("🏢 Company Fundamentals")
    st.write(f"**Company Name:** {info.get('longName', 'N/A')}")
    st.write(f"**Sector:** {info.get('sector', 'N/A')}")
    st.write(f"**Market Cap:** {info.get('marketCap', 'N/A')}")
    st.write(f"**PE Ratio:** {info.get('trailingPE', 'N/A')}")
    st.write(f"**EPS:** {info.get('trailingEps', 'N/A')}")
    st.write(f"**52 Week High:** {info.get('fiftyTwoWeekHigh', 'N/A')}")
    st.write(f"**52 Week Low:** {info.get('fiftyTwoWeekLow', 'N/A')}")

    # Technical Indicators
    st.subheader("📉 Technical Indicators")

    # SMA and RSI Calculation
    hist['SMA20'] = hist['Close'].rolling(window=20).mean()
    hist['SMA50'] = hist['Close'].rolling(window=50).mean()
    delta = hist['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    hist['RSI'] = 100 - (100 / (1 + rs))

    # Display SMA & RSI Table
    st.write(hist[['Close', 'SMA20', 'SMA50', 'RSI']].tail(10))

    # Price Trend
    st.subheader("📈 Price Trend (Close vs SMA)")
    st.line_chart(hist[['Close', 'SMA20', 'SMA50']])

except Exception as e:
    st.error(f"Error loading data: {e}")            
