import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Vijay Stock Guru", layout="wide")
st.title("📈 Vijay Stock Guru - Unified Stock Analysis Dashboard")

# --- Input ---
symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        # --- Fetch Data ---
        data = yf.download(symbol, period="6mo", interval="1d")
        if data.empty:
            st.warning("⚠️ No data found! Please check the symbol name.")
        else:
            data.dropna(inplace=True)

            # --- Tabs Layout ---
            tab1, tab2, tab3, tab4 = st.tabs([
                "📊 Price Chart",
                "🚀 Breakout & Volume",
                "📉 Technical Indicators",
                "ℹ️ About"
            ])

            # --- TAB 1: Chart ---
            with tab1:
                st.subheader(f"Stock Data for {symbol}")
                st.dataframe(data.tail())

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
                    title=f"{symbol} - Price Chart",
                    xaxis_rangeslider_visible=False,
                    template="plotly_dark"
                )
                st.plotly_chart(fig, use_container_width=True)

            # --- TAB 2: Breakout & Volume ---
            with tab2:
                st.subheader("🚀 Breakout & Volume Analysis")

                data['Prev_High'] = data['High'].shift(1)
                data['Prev_Low'] = data['Low'].shift(1)

                latest_close = data['Close'].iloc[-1]
                latest_high = data['High'].iloc[-1]
                prev_high = data['Prev_High'].iloc[-1]

                breakout = latest_high > prev_high and latest_close > prev_high
                if breakout:
                    st.success("✅ Bullish Breakout detected! 🚀")
                else:
                    st.info("📊 No breakout yet. Keep watching!")

                avg_volume = data['Volume'].mean()
                latest_volume = data['Volume'].iloc[-1]
                if latest_volume > 1.5 * avg_volume:
                    st.warning("💥 High trading volume detected today!")

                st.write(f"📅 Last Close: ₹{latest_close:.2f}")
                st.write(f"📊 Average Volume: {avg_volume:,.0f}")
                st.write(f"📈 Latest Volume: {latest_volume:,.0f}")

            # --- TAB 3: Indicators ---
            with tab3:
                st.subheader("📉 Technical Indicators")

                # Moving Averages
                data['SMA20'] = data['Close'].rolling(window=20).mean()
                data['SMA50'] = data['Close'].rolling(window=50).mean()

                # RSI Calculation
                delta = data['Close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
                RS = gain / loss
                data['RSI'] = 100 - (100 / (1 + RS))

                # MACD Calculation
                exp1 = data['Close'].ewm(span=12, adjust=False).mean()
                exp2 = data['Close'].ewm(span=26, adjust=False).mean()
                data['MACD'] = exp1 - exp2
                data['Signal'] = data['MACD'].ewm(span=9, adjust=False).mean()

                # --- Charts ---
                st.line_chart(data[['Close', 'SMA20', 'SMA50']])
                st.line_chart(data['RSI'])
                st.line_chart(data[['MACD', 'Signal']])

                st.caption("📘 Indicators: SMA20, SMA50, RSI, MACD & Signal Line")

            # --- TAB 4: About ---
            with tab4:
                st.markdown("""
                ### 💡 Vijay Stock Guru
                - Real-time NSE data via Yahoo Finance  
                - Detects **Breakouts** with **Volume Confirmation**  
                - Shows key **Technical Indicators**  
                - Designed & conceptualized by *Vijay Stock Guru*  
                ---
                ⚙️ Built with: Streamlit + Plotly + Python
                """)

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")

else:
    st.info("Please enter a valid NSE stock symbol above.")
