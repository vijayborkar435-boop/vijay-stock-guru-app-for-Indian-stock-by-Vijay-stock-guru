import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# ==============================
# FUNDAMENTAL + TECHNICAL COMBO
# ==============================

def analyze_stock(symbol):
    try:
        stock = yf.Ticker(symbol)
        info = stock.info

        # ============= FUNDAMENTAL DATA =============
        fundamentals = {
            "Company": info.get("shortName"),
            "Market Cap (Cr)": round(info.get("marketCap", 0) / 1e7, 2),
            "P/E Ratio": info.get("trailingPE"),
            "EPS (₹)": info.get("trailingEps"),
            "ROE (%)": info.get("returnOnEquity", 0) * 100 if info.get("returnOnEquity") else None,
            "Debt to Equity": info.get("debtToEquity"),
            "Profit Margin (%)": info.get("profitMargins", 0) * 100 if info.get("profitMargins") else None,
            "52 Week High": info.get("fiftyTwoWeekHigh"),
            "52 Week Low": info.get("fiftyTwoWeekLow"),
        }

        # ============= TECHNICAL DATA =============
        data = stock.history(period="6mo")
        data["MA20"] = data["Close"].rolling(window=20).mean()
        data["MA50"] = data["Close"].rolling(window=50).mean()

        # RSI Calculation
        delta = data["Close"].diff()
        gain = np.where(delta > 0, delta, 0)
        loss = np.where(delta < 0, -delta, 0)
        avg_gain = pd.Series(gain).rolling(window=14).mean()
        avg_loss = pd.Series(loss).rolling(window=14).mean()
        rs = avg_gain / avg_loss
        data["RSI"] = 100 - (100 / (1 + rs))

        # MACD Calculation
        data["EMA12"] = data["Close"].ewm(span=12, adjust=False).mean()
        data["EMA26"] = data["Close"].ewm(span=26, adjust=False).mean()
        data["MACD"] = data["EMA12"] - data["EMA26"]
        data["Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

        # Breakout Detection
        recent = data.iloc[-1]
        past_high = data["High"].tail(20).max()
        avg_vol = data["Volume"].tail(20).mean()
        breakout = recent["Close"] > past_high and recent["Volume"] > avg_vol * 1.5

        technicals = {
            "Current Price (₹)": round(recent["Close"], 2),
            "20-Day MA": round(recent["MA20"], 2),
            "50-Day MA": round(recent["MA50"], 2),
            "RSI": round(recent["RSI"], 2),
            "MACD": round(recent["MACD"], 2),
            "Signal": round(recent["Signal"], 2),
            "Volume": int(recent["Volume"]),
            "Avg Volume": int(avg_vol),
            "Breakout": "✅ YES" if breakout else "❌ NO"
        }

        print(f"\n📊 ANALYSIS REPORT for {symbol}\n")
        print("===== FUNDAMENTAL ANALYSIS =====")
        for k, v in fundamentals.items():
            print(f"{k:25}: {v}")

        print("\n===== TECHNICAL ANALYSIS =====")
        for k, v in technicals.items():
            print(f"{k:25}: {v}")

        print("\n------------------------------------------")

    except Exception as e:
        print(f"❌ Error fetching data for {symbol}: {e}")


# =============================
# Example: Analyze Multiple Stocks
# =============================
stocks = ["RELIANCE.NS", "TCS.NS", "HDFCBANK.NS", "INFY.NS"]

for s in stocks:
    analyze_stock(s)
