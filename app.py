import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Vijay Stock Guru - NSE Analysis", layout="wide")

st.title("📈 Vijay Stock Guru - NSE Analysis")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS):", "TCS.NS")

if symbol:
    try:
        df = yf.download(symbol, period="6mo", interval="1d")
        if df.empty:
            st.error("⚠️ No data found for this stock.")
        else:
            st.success(f"✅ Data loaded for {symbol}")

            # Calculate indicators
            df["MA20"] = df["Close"].rolling(window=20).mean()
            df["MA50"] = df["Close"].rolling(window=50).mean()
            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df["RSI"] = 100 - (100 / (1 + rs))

            # Latest summary table
            st.subheader("📊 Latest Data")
            st.dataframe(df.tail().round(2))

            # Technical summary
            st.subheader("⚙️ Technical Summary")
            latest = df.iloc[-1]
            st.table(pd.DataFrame({
                "MA20": [round(latest["MA20"], 2)],
                "MA50": [round(latest["MA50"], 2)],
                "RSI": [round(latest["RSI"], 2)]
            }))

            # Chart (Candlestick + Moving Averages)
            st.subheader("📉 Stock Price Chart with MA20 & MA50")

            fig = go.Figure()

            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                name="Candlestick"
            ))
            fig.add_trace(go.Scatter(x=df.index, y=df["MA20"], name="MA20", line=dict(color="blue", width=1.5)))
            fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], name="MA50", line=dict(color="orange", width=1.5)))

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Date",
                yaxis_title="Price (INR)",
                width=950, height=500
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")
