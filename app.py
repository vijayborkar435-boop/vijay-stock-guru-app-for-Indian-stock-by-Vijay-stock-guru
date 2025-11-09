import streamlit as st
import pandas as pd
import yfinance as yf
import plotly.graph_objs as go

st.set_page_config(page_title="Vijay Stock Guru", layout="wide")

st.title("📈 Vijay Stock Guru - Breakout & Volume Analysis")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d")
        
        if data.empty:
            st.error("⚠️ No data found for this symbol! Please check the symbol name (e.g., RELIANCE.NS, TCS.NS).")
        else:
            data.dropna(inplace=True)
            st.subheader(f"Stock Data for {symbol}")
            st.dataframe(data.tail())

            # Plot candlestick chart
            fig = go.Figure(data=[go.Candlestick(
                x=data.index,
                open=data['Open'],
                high=data['High'],
                low=data['Low'],
                close=data['Close'],
                name='Candlestick'
            )])

            fig.update_layout(title=f"{symbol} - Last 6 Months Chart", xaxis_rangeslider_visible=False)
            st.plotly_chart(fig, use_container_width=True)

            # Breakout detection
            data['Prev_High'] = data['High'].shift(1)
            data['Prev_Low'] = data['Low'].shift(1)

            latest_close = data['Close'].iloc[-1]
            latest_high = data['High'].iloc[-1]
            prev_high = data['Prev_High'].iloc[-1]

            if pd.notna(latest_high) and pd.notna(prev_high):
                if (latest_high > prev_high) and (latest_close > prev_high):
                    st.success("🚀 Bullish Breakout detected!")
                else:
                    st.info("📊 No breakout yet, keep watching.")
            else:
                st.warning("Not enough data to check breakout.")

            # Volume analysis
            avg_volume = data['Volume'].mean()
            latest_volume = data['Volume'].iloc[-1]

            if latest_volume > 1.5 * avg_volume:
                st.warning("💥 High volume detected today!")
            else:
                st.info("📈 Normal volume activity.")

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")

else:
    st.info("Please enter a stock symbol to start analysis.")
