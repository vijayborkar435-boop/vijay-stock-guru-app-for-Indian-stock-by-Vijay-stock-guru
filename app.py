import yfinance as yf
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Vijay Stock Guru", layout="wide")

st.title("📊 Vijay Stock Guru - NSE Analysis")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS):", "TCS.NS")

if symbol:
    try:
        data = yf.download(symbol, period="6mo")
        if data.empty:
            st.warning("⚠️ No data found for this symbol. Try again.")
        else:
            st.success(f"✅ Data loaded for {symbol}")

            # Basic stats
            st.write("### Latest Data")
            st.dataframe(data.tail())

            # Moving averages
            data["MA20"] = data["Close"].rolling(window=20).mean()
            data["MA50"] = data["Close"].rolling(window=50).mean()

            # RSI
            delta = data["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
            rs = gain / loss
            data["RSI"] = 100 - (100 / (1 + rs))

            # Display technicals summary
            st.write("### 📈 Technical Summary")
            last = data.iloc[-1]
            st.write({
                "MA20": round(last["MA20"], 2),
                "MA50": round(last["MA50"], 2),
                "RSI": round(last["RSI"], 2)
            })

            # Plot without crashing
            st.line_chart(data[["Close", "MA20", "MA50"]])

    except Exception as e:
        st.error(f"❌ Error fetching data: {e}")
