 import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="Vijay Stock Guru - Pro", layout="wide")

st.title("🚀 Vijay Stock Guru - All in One (Fundamental + Technical + Breakout)")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS):", "TCS.NS")

if symbol:
    try:
        stock = yf.Ticker(symbol)
        df = stock.history(period="6mo", interval="1d")

        if df.empty:
            st.error("⚠️ No data found for this stock.")
        else:
            st.success(f"✅ Data loaded for {symbol}")

            # ---------------- FUNDAMENTAL ----------------
            info = stock.info
            st.subheader("🏦 Fundamental Summary")

            fundamentals = {
                "Company Name": info.get("shortName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Market Cap (₹ Cr)": round(info.get("marketCap", 0) / 1e7, 2),
                "P/E Ratio": info.get("trailingPE", "N/A"),
                "P/B Ratio": info.get("priceToBook", "N/A"),
                "EPS (₹)": info.get("trailingEps", "N/A"),
                "Dividend Yield (%)": info.get("dividendYield", 0) * 100 if info.get("dividendYield") else "N/A",
                "52 Week High": info.get("fiftyTwoWeekHigh", "N/A"),
                "52 Week Low": info.get("fiftyTwoWeekLow", "N/A"),
                "Book Value (₹)": info.get("bookValue", "N/A"),
            }

            st.table(pd.DataFrame(list(fundamentals.items()), columns=["Metric", "Value"]))

            # ---------------- TECHNICAL ----------------
            df["MA20"] = df["Close"].rolling(window=20).mean()
            df["MA50"] = df["Close"].rolling(window=50).mean()

            delta = df["Close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
            rs = gain / loss
            df["RSI"] = 100 - (100 / (1 + rs))

            st.subheader("📈 Technical Summary")
            latest = df.iloc[-1]
            summary = pd.DataFrame({
                "MA20": [round(latest["MA20"], 2)],
                "MA50": [round(latest["MA50"], 2)],
                "RSI": [round(latest["RSI"], 2)]
            })
            st.table(summary)

            # ---------------- BREAKOUT SECTION ----------------
            st.subheader("⚡ Breakout & Volume Alert")

            condition_rsi = latest["RSI"] > 60
            condition_ma = latest["MA20"] > latest["MA50"]
            condition_vol = df["Volume"].iloc[-1] > df["Volume"].rolling(20).mean().iloc[-1]

            if condition_rsi and condition_ma and condition_vol:
                st.success("🚀 Breakout Signal! Stock showing strength (RSI>60, MA20>MA50, High Volume)")
            else:
                st.warning("⚠️ No breakout yet. Stock still consolidating or weak.")

            # ---------------- CHART ----------------
            st.subheader("📉 Stock Price Chart with MA20 & MA50")

            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=df.index,
                open=df["Open"], high=df["High"],
                low=df["Low"], close=df["Close"],
                name="Candlestick"
            ))
            fig.add_trace(go.Scatter(x=df.index, y=df["MA20"], name="MA20", line=dict(color="cyan", width=1.5)))
            fig.add_trace(go.Scatter(x=df.index, y=df["MA50"], name="MA50", line=dict(color="orange", width=1.5)))

            fig.update_layout(
                template="plotly_dark",
                xaxis_title="Date", yaxis_title="Price (INR)",
                width=950, height=500,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"❌ Error: {e}")       
