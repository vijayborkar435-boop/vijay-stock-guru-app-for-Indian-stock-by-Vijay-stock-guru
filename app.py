import streamlit as st
import yfinance as yf
import pandas as pd
import plotly.graph_objects as go

st.set_page_config(page_title="📈 Vijay Stock Guru", layout="wide")
st.title("📊 Vijay Stock Guru - Fundamental + Technical + Valuation")

symbol = st.text_input("Enter NSE Symbol (e.g. RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")

        if data.empty:
            st.warning("⚠️ No data found for this symbol.")
        else:
            # --- 📈 Technical Analysis ---
            st.subheader("📊 Technical Chart")

            data['SMA20'] = data['Close'].rolling(20).mean()
            data['SMA50'] = data['Close'].rolling(50).mean()

            fig = go.Figure()
            fig.add_trace(go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            ))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA20'], line=dict(color='orange', width=1.5), name='SMA 20'))
            fig.add_trace(go.Scatter(x=data.index, y=data['SMA50'], line=dict(color='blue', width=1.5), name='SMA 50'))
            fig.update_layout(title=f"{symbol} Price Chart", xaxis_rangeslider_visible=False, height=500)
            st.plotly_chart(fig, use_container_width=True)

            # Signal
            sma20 = data['SMA20'].iloc[-1]
            sma50 = data['SMA50'].iloc[-1]
            if sma20 > sma50:
                st.success("🚀 Bullish crossover (Uptrend likely)")
            elif sma20 < sma50:
                st.error("🔻 Bearish crossover (Downtrend likely)")
            else:
                st.info("➖ Neutral trend")

            # --- 💼 Fundamental Analysis ---
            st.subheader("💼 Fundamental Analysis")
            ticker = yf.Ticker(symbol)
            info = ticker.info if hasattr(ticker, "info") else {}

            def safe_get(key, default="N/A"):
                value = info.get(key, default)
                if isinstance(value, (int, float)) and abs(value) > 1e9:
                    return f"{value/1e7:.2f} Cr"
                return value

            fundamentals = {
                "Company Name": safe_get("longName"),
                "Sector": safe_get("sector"),
                "Market Cap": safe_get("marketCap"),
                "PE Ratio": safe_get("trailingPE"),
                "EPS (TTM)": safe_get("trailingEps"),
                "ROE": f"{info.get('returnOnEquity', 0)*100:.2f}%" if info.get("returnOnEquity") else "N/A",
                "Book Value": safe_get("bookValue"),
                "Debt to Equity": safe_get("debtToEquity"),
                "Profit Margin": f"{info.get('profitMargins', 0)*100:.2f}%" if info.get("profitMargins") else "N/A",
                "Dividend Yield": f"{info.get('dividendYield', 0)*100:.2f}%" if info.get("dividendYield") else "N/A"
            }

            df = pd.DataFrame(list(fundamentals.items()), columns=["Metric", "Value"])
            st.table(df)

            # --- 💰 Intrinsic Value ---
            st.subheader("💰 Intrinsic Value (DCF Based)")
            eps = info.get("trailingEps", None)
            growth = info.get("earningsQuarterlyGrowth", 0.10)
            discount_rate = 0.12
            current_price = info.get("currentPrice", None)

            if eps and current_price:
                try:
                    intrinsic_value = eps * (1 + growth) / (discount_rate - growth)
                    st.write(f"📍 Intrinsic Value ≈ ₹{intrinsic_value:.2f}")
                    st.write(f"💵 Current Price: ₹{current_price}")
                    if intrinsic_value > current_price:
                        diff = ((intrinsic_value - current_price) / current_price) * 100
                        st.success(f"✅ Undervalued by {diff:.2f}%")
                    else:
                        diff = ((current_price - intrinsic_value) / intrinsic_value) * 100
                        st.error(f"❌ Overvalued by {diff:.2f}%")
                except Exception:
                    st.warning("⚠️ Not enough data for DCF calculation.")
            else:
                st.info("EPS or Price data not available for DCF model.")

    except Exception as e:
        st.error(f"⚠️ Error: {e}")
else:
    st.info("Enter a stock symbol to begin analysis.")
                    
