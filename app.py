import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Vijay Stock Guru", layout="wide")
st.title("📈 Vijay Stock Guru - NSE Stocks Chart")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        data = yf.download(symbol, period="6mo", interval="1d", progress=False)

        if data.empty:
            st.error("❌ No data found! Please check the symbol name (e.g., RELIANCE.NS)")
        else:
            st.success(f"✅ Data loaded successfully for {symbol}")

            fig = go.Figure(
                data=[go.Candlestick(
                    x=data.index,
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close']
                )]
            )

            fig.update_layout(
                title=f"{symbol} - Candlestick Chart",
                xaxis_title="Date",
                yaxis_title="Price (INR)",
                xaxis_rangeslider_visible=False,
                template="plotly_white",
                height=600
            )

            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")

else:
    st.info("Enter a stock symbol above to see the chart.")           
