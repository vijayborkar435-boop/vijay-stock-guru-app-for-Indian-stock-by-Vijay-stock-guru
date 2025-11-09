# Vijay Stock Guru - India Edition (Auto Fetch)
# Streamlit app: Auto-fetch NSE stocks via yfinance, plus manual overrides.

import streamlit as st
import yfinance as yf
from math import isnan

st.set_page_config(page_title="Vijay Stock Guru", page_icon="📈", layout="centered")

st.markdown("<h1 style='text-align:center'>Vijay Stock Guru — India Edition</h1>", unsafe_allow_html=True)
st.markdown("<p style='text-align:center;color:gray'>Powered by Chat Bhaiya 🔹 Learning & Analysis Tool</p>", unsafe_allow_html=True)
st.write("---")

with st.expander("ℹ️ Quick Guide / Help"):
    st.markdown("""
    **How to use**
    - Enter NSE symbol like `TCS.NS`, `INFY.NS`, `RELIANCE.NS`, `HDFCBANK.NS`.
    - Click **Fetch Data** to auto-fill values (EPS, Price, P/E, ROE, ROCE, Debt).
    - You can edit any value manually after fetch (for example if you prefer TTM EPS or analyst growth).
    - Enter **Annual Growth Rate (%)** (use 5Y CAGR if you can find it).
    - Click **Analyze Stock** to get Intrinsic Value, Margin of Safety and Strength Score.
    
    **Notes**
    - Intrinsic Value uses a simplified Graham-style formula.
    - This is a screening/learning tool — always do deeper research before investing.
    """)

st.write("## 1) Fetch or Enter Stock Data")

colf1, colf2, colf3 = st.columns([2,1,1])
with colf1:
    symbol = st.text_input("Enter NSE Stock Symbol (e.g. TCS.NS, INFY.NS)", value="TCS.NS").upper().strip()
with colf2:
    if st.button("🔘 Fetch Data"):
        fetch_clicked = True
    else:
        fetch_clicked = False
with colf3:
    st.write("")  # spacing

# Default placeholders
eps = None
pe = None
price = None
roe = None
roce = None
de_ratio = None
book_value = None

if fetch_clicked and symbol:
    try:
        ticker = yf.Ticker(symbol)
        info = ticker.info or {}
        # yfinance keys (may be absent)
        price = info.get("currentPrice") or info.get("regularMarketPrice") or 0
        eps = info.get("trailingEps") or info.get("earningsPerShare") or 0
        pe = info.get("trailingPE") or info.get("forwardPE") or 0
        # returnOnEquity comes as decimal like 0.12
        roe = info.get("returnOnEquity")
        roce = info.get("returnOnAssets")  # approximate if ROCE not present
        debt_to_equity = info.get("debtToEquity")
        book_value = info.get("bookValue")
        # Convert decimals to percent if present
        if roe is not None:
            try:
                roe = float(roe) * 100
            except:
                pass
        if roce is not None:
            try:
                roce = float(roce) * 100
            except:
                pass
        if debt_to_equity is None:
            de_ratio = 0.0
        else:
            de_ratio = float(debt_to_equity)
        # Fallback numeric safe
        price = float(price or 0)
        eps = float(eps or 0)
        pe = float(pe or 0)
        roe = float(roe or 0)
        roce = float(roce or 0)
        de_ratio = float(de_ratio or 0)
        book_value = float(book_value or 0)
        st.success("✅ Data fetched from Yahoo Finance (yfinance). You can edit values below if needed.")
    except Exception as e:
        st.error("⚠️ Fetch error: " + str(e))
        price = eps = pe = roe = roce = de_ratio = book_value = 0.0

st.write("## 2) Edit / Confirm Values (auto-filled values shown, you can change)")

col1, col2, col3 = st.columns(3)
with col1:
    eps = st.number_input("EPS (₹)", min_value=0.0, value=float(eps or 0.0), step=0.01, format="%.4f")
    pe = st.number_input("P/E Ratio (market or fair)", min_value=0.0, value=float(pe or 0.0), step=0.1, format="%.2f")
    market_price = st.number_input("Market Price (₹)", min_value=0.0, value=float(price or 0.0), step=0.01, format="%.2f")
with col2:
    roe = st.number_input("ROE (%)", min_value=-100.0, value=float(roe or 0.0), step=0.1, format="%.2f")
    roce = st.number_input("ROCE (%)", min_value=-100.0, value=float(roce or 0.0), step=0.1, format="%.2f")
    de_ratio = st.number_input("Debt-to-Equity", min_value=0.0, value=float(de_ratio or 0.0), step=0.01, format="%.2f")
with col3:
    book_value = st.number_input("Book Value (₹)", min_value=0.0, value=float(book_value or 0.0), step=0.01, format="%.2f")
    growth_rate = st.number_input("Annual Growth Rate (%) - (enter 5Y CAGR if possible)", value=10.0, step=0.1, format="%.2f")
    st.write("Face value / Dividend info can be checked on Screener/NSE if needed.")

st.write("---")
if st.button("🔍 Analyze Stock"):
    # Intrinsic Value calculation (simplified Graham-style)
    try:
        g = float(growth_rate)  # percent
        intrinsic_value = eps * (8.5 + 2 * g) * 4.4 / 9.0
    except Exception as e:
        st.error("Error calculating intrinsic value: " + str(e))
        intrinsic_value = 0.0

    # Margin of Safety
    try:
        mos = ((intrinsic_value - market_price) / intrinsic_value) * 100 if intrinsic_value != 0 else 0.0
    except:
        mos = 0.0

    # Strength scoring logic
    score = 0
    reasons = []
    # Growth positive?
    if g > 0:
        score += 1
        reasons.append("Growth Positive")
    else:
        reasons.append("Growth Negative or Zero")

    # MOS > 20 ?
    if mos > 20:
        score += 1
        reasons.append("Good Margin of Safety")
    else:
        reasons.append("No meaningful Margin of Safety")

    # ROE check
    if roe > 15:
        score += 1
        reasons.append("ROE Strong (>15%)")
    else:
        reasons.append("ROE Weak / Average")

    # ROCE check
    if roce > 12:
        score += 1
        reasons.append("ROCE Healthy (>12%)")
    else:
        reasons.append("ROCE Weak / Average")

    # Debt check
    if de_ratio < 1:
        score += 1
        reasons.append("Low Debt (D/E < 1)")
    else:
        reasons.append("High Debt (D/E >= 1)")

    # Display results
    st.subheader("📊 Result")
    st.write(f"**Symbol:** {symbol}")
    st.write(f"**Intrinsic Value:** ₹{intrinsic_value:,.2f}")
    st.write(f"**Market Price:** ₹{market_price:,.2f}")
    st.write(f"**Margin of Safety:** {mos:.2f}%")
    st.write(f"**EPS:** ₹{eps:.2f} | **P/E (input):** {pe:.2f}")
    st.write(f"**ROE:** {roe:.2f}% | **ROCE (approx):** {roce:.2f}%")
    st.write(f"**Debt-to-Equity:** {de_ratio:.2f}")
    st.write("---")
    st.subheader("🏁 Strength Score")
    st.write(f"**{score} / 5**")

    if score >= 4:
        st.success("💹 Strong Stock — Good candidate for long-term.")
    elif score == 3:
        st.warning("🟡 Moderate — Study further before buying.")
    else:
        st.error("🔴 Weak Fundamentals — Avoid for now.")

    with st.expander("🔎 Why this verdict?"):
        for r in reasons:
            st.write("- " + r)

    st.write("---")
    st.caption("Tip: This is a fundamentals screening tool. For trading, combine with technical analysis and news checks.")
