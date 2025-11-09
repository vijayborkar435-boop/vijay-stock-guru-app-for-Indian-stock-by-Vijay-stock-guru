import yfinance as yf
import pandas as pd
import numpy as np

def analyze_stock(symbol):
    try:
        stock = yf.Ticker(symbol)

        # Get history safely
        data = stock.history(period="6mo")
        if data.empty:
            print(f"⚠️ No price data available for {symbol}")
            return

        info = stock.fast_info  # fast, safer version

        # Fundamental Data (safe extraction)
        fundamentals = {
            "Company": symbol,
            "Current Price (₹)": round(info.get("last_price", 0), 2),
            "52 Week High": info.get("year_high"),
            "52 Week Low": info.get("year_low"),
            "Market Cap (Cr)": round(info.get("market_cap", 0) / 1e7, 2),
            "Previous Close": info.get("previous_close")
        }

        # Technical Indicators
        data["MA20"] = data["Close"].rolling(window=20).mean()
        data["MA50"] = data["Close"].rolling(window=50).mean()

        # RSI Calculation
        delta = data["Close"].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        rs = gain / loss
        data["RSI"] = 100 - (100 / (1 + rs))

        # MACD
        data["EMA12"] = data["Close"].ewm(span=12, adjust=False).mean()
        data["EMA26"] = data["Close"].ewm(span=26, adjust=False).mean()
        data["MACD"] = data["EMA12"] - data["EMA26"]
        data["Signal"] = data["MACD"].ewm(span=9, adjust=False).mean()

        # Breakout Check
        last = data.iloc[-1]
        past_high = data["High"].tail(20).max()
        avg_vol = data["Volume"].tail(20).mean()
        breakout = last["Close"] > past_high and last["Volume"] > avg_vol * 1.5

        technicals = {
            "MA20": round(last["MA20"], 2),
            "MA50": round(last["MA50"], 2),
            "RSI": round(last["RSI"], 2),
            "MACD": round(last["MACD"], 2),
            "Signal": round(last["Signal"], 2),
            "Volume": int(last["Volume"]),
            "Avg Vol": int(avg_vol),
            "Breakout": "✅ YES" if breakout else "❌ NO"
        }

        # Print Report
        print(f"\n📊 ANALYSIS REPORT for {symbol}\n")
        print("===== FUNDAMENTAL DATA =====")
        for k, v in fundamentals.items():
            print(f"{k:25}: {v}")

        print("\n===== TECHNICAL DATA =====")
        for k, v in technicals.items():
            print(f"{k:25}: {v}")

        print("--------------------------------------")

    except Exception as e:
        print(f"❌ Error fetching {symbol}: {e}")


# Example use
stocks = ["RELIANCE.NS", "TCS.NS", "INFY.NS", "HDFCBANK.NS"]

for s in stocks:
    analyze_stock(s)        
