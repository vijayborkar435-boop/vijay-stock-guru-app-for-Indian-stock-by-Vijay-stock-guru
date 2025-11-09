import streamlit as st
import yfinance as yf
import plotly.graph_objects as go

st.set_page_config(page_title="Vijay Stock Guru", layout="wide")
st.title("📈 Vijay Stock Guru - NSE Stock Chart")

symbol = st.text_input("Enter NSE Stock Symbol (e.g., RELIANCE.NS, TCS.NS, HDFCBANK.NS):")

if symbol:
    try:
        # Fetch data
        data = yf.download(symbol, period="6mo", interval="1d", progress=False)
        
        if data is None or data.empty:
            st.error("❌ No data found! Please check the symbol name (e.g., RELIANCE.NS)")
        else:
            st.success(f"✅ Data loaded successfully for {symbol}")
            
            # Convert index to column (Date)
            data.reset_index(inplace=True)
            
            # Check data head (for debugging)
            st.write("Preview:", data.head())
            
            # Plot candlestick
            fig = go.Figure(data=[
                go.Candlestick(
                    x=data['Date'],
                    open=data['Open'],
                    high=data['High'],
                    low=data['Low'],
                    close=data['Close'],
                    name='Candlestick'
                )
            ])
            
            fig.update_layout(
                title=f"{symbol} - Candlestick Chart (6 Months)",
                xaxis_title="Date",
                yaxis_title="Price (INR)",
                xaxis_rangeslider_visible=True,
                template="plotly_dark",
                height=600
            )
            
            st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error(f"⚠️ Error fetching or plotting data: {e}")
else:
    st.info("Please enter a stock symbol to load the chart.")
