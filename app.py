import streamlit as st
import subprocess
import sys
import time

# --- 1. SILENT AUTO-INSTALLER (Yfinance Error Fix) ---
try:
    import yfinance as yf
except ImportError:
    # Agar library nahi hai, toh ye line use install kar degi
    subprocess.check_call([sys.executable, "-m", "pip", "install", "yfinance"])
    import yfinance as yf

import pandas as pd
import numpy as np

# --- 2. PROFESSIONAL DESIGN (Trading Terminal Look) ---
st.set_page_config(page_title="Master Stocks AI", layout="wide")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    div[data-testid="stMetric"] {
        background-color: #1e2130;
        border: 1px solid #4B506D;
        padding: 20px;
        border-radius: 12px;
    }
    .neutral-box {
        color: #FFA500;
        font-weight: bold;
        border: 1px solid #FFA500;
        padding: 12px;
        border-radius: 8px;
        text-align: center;
        background-color: rgba(255, 165, 0, 0.1);
    }
    [data-testid="stMetricValue"] { color: #00FFC2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- 3. RSI LOGIC ---
def get_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- 4. APP INTERFACE ---
st.title("🛡️ Master Stocks AI Terminal")

# Sidebar inputs
with st.sidebar:
    st.header("Search")
    symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")
    duration = st.selectbox("Select Duration", ["1mo", "6mo", "1y"])
    st.divider()
    speak_trigger = st.button("🔊 Listen Audio Analysis")

# --- 5. DATA PROCESSING ---
try:
    # Fetching live data from Yahoo Finance
    df = yf.download(symbol, period=duration)
    
    if not df.empty:
        df['RSI'] = get_rsi(df['Close'])
        latest_price = float(df['Close'].iloc[-1])
        latest_rsi = float(df['RSI'].iloc[-1])
        
        # --- LOOK: LIVE PRICE | RSI | MARKET STATUS ---
        col1, col2, col3 = st.columns(3)
        
        col1.metric("Live Price", f"₹{latest_price:,.2f}")
        col2.metric("RSI (14D)", f"{latest_rsi:.1f}")
        
        with col3:
            st.write("Market Signal")
            if latest_rsi < 30:
                st.success("🚀 BUY SIGNAL")
                msg = "Oversold zone. Market is Bullish."
            elif latest_rsi > 70:
                st.error("⚠️ SELL SIGNAL")
                msg = "Overbought zone. Market is Bearish."
            else:
                st.markdown('<div class="neutral-box">⚖️ Market is Neutral</div>', unsafe_allow_html=True)
                msg = "Market is in neutral range. No clear trend."

        # CHART
        st.line_chart(df['Close'])

        # --- SPEAK COMMAND ---
        if speak_trigger:
            full_speech = f"Analysis for {symbol}. Current price is {latest_price:.1f}. RSI is {latest_rsi:.1f}. {msg}"
            # JavaScript voice engine (Har browser par chalega)
            st.components.v1.html(f"""
                <script>
                var msg = new SpeechSynthesisUtterance('{full_speech}');
                window.speechSynthesis.speak(msg);
                </script>
            """, height=0)
            
    else:
        st.warning("Data fetch nahi ho raha. Symbol sahi likhein (Example: SBIN.NS or AAPL)")

except Exception as e:
    st.info("System is initializing... Please wait 10 seconds.")

st.divider()
st.caption("Master Stocks Pro | Empowering Traders with AI")
