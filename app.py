import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="📈 Vijay Stock Guru", layout="wide")
st.title("📊 Vijay Stock Guru - Fundamental + Technical Analysis")

symbol = st.text_input("Enter NSE Symbol (e.g. RELIANCE.NS, TCS.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")

        if data.empty:
            st.warning("⚠️ No data found. Please check symbol.")
        else:
            st.subheader("📈 Technical Chart")

            # Moving Averages
            data['SMA20'] = data['Close'].rolling(window=20).mean()
            data['SMA50'] = data['Close'].rolling(window=50).mean()

            # Plotly Chart
            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))
            fig.add_trace(go.Scatter(
                x=data.index, y=data['SMA20'],
                line=dict(color='orange', width=1.5),
                name='SMA 20'
            ))
            fig.add_trace(go.Scatter(
                x=data.index, y=data['SMA50'],
                line=dict(color='blue', width=1.5),
                name='SMA 50'
            ))

            fig.update_layout(
                title=f"{symbol} Price Chart",
                xaxis_rangeslider_visible=False,
                height=500
            )

            st.plotly_chart(fig, use_container_width=True)

            # Signal
            sma20 = data['SMA20'].iloc[-1]
            sma50 = data['SMA50'].iloc[-1]

            if sma20 > sma50:
                st.success("🚀 Bullish crossover - Possible Uptrend")
            elif sma20 < sma50:
                st.error("🔻 Bearish crossover - Possible Downtrend")
            else:
                st.info("➖ Neutral signal")

            # ------------------------
            # 📊 Fundamental Analysis
            # ------------------------
            st.subheader("💼 Fundamental Analysis")

            info = yf.Ticker(symbol).info

            fundamentals = {
                "Company Name": info.get("longName", "N/A"),
                "Sector": info.get("sector", "N/A"),
                "Market Cap": f"{info.get('marketCap', 0)/1e7:.2f} Cr",
                "PE Ratio": info.get("trailingPE", "N/A"),
                "EPS (TTM)": info.get("trailingEps", "N/A"),
                "ROE (approx)": f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get("returnOnEquity") else "N/A",
                "Book Value": info.get("bookValue", "N/A"),
                "Debt to Equity": info.get("debtToEquity", "N/A"),
                "Profit Margin": f"{info.get('profitMargins', 0)*100:.2f}%" if info.get("profitMargins") else "N/A",
                "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get("dividendYield") else "N/A"
            }

            df = pd.DataFrame(list(fundamentals.items()), columns=["Metric", "Value"])
            st.table(df)

    except Exception as e:
        st.error(f"Error: {e}")

else:
    st.info("Enter stock symbol to begin analysis.")
