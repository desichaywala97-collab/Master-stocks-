import streamlit as st
import pandas as pd
import numpy as np

# Error Handling agar library install na ho
try:
    import yfinance as yf
except ImportError:
    st.error("🔄 Libraries install ho rahi hain... Kripya 1 minute baad Reboot karein.")
    st.stop()

st.set_page_config(page_title="Master Stocks AI", layout="wide")

# CSS for Neutral/Buy/Sell looks
st.markdown("""
    <style>
    [data-testid="stMetric"] { background-color: #1e2130; border: 1px solid #4B506D; padding: 20px; border-radius: 12px; }
    .neutral-box { color: #FFA500; font-weight: bold; border: 1px solid #FFA500; padding: 10px; border-radius: 8px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

st.title("📈 Master Stocks AI Terminal")

# Input Section
col_in1, col_in2 = st.columns(2)
with col_in1:
    symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")
with col_in2:
    duration = st.selectbox("Duration", ["1mo", "6mo", "1y"])

try:
    df = yf.download(symbol, period=duration)
    if not df.empty:
        # RSI Calculation logic
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(14).mean()
        df['RSI'] = 100 - (100 / (1 + (gain/loss)))
        
        latest_price = float(df['Close'].iloc[-1])
        latest_rsi = float(df['RSI'].iloc[-1])

        # Your requested Clean Layout
        m1, m2, m3 = st.columns(3)
        m1.metric("Live Price", f"₹{latest_price:,.2f}")
        m2.metric("RSI (14D)", f"{latest_rsi:.1f}")
        
        with m3:
            st.write("Market Status")
            if latest_rsi < 30:
                st.success("🚀 BUY SIGNAL")
            elif latest_rsi > 70:
                st.error("⚠️ SELL SIGNAL")
            else:
                st.markdown('<div class="neutral-box">⚖️ Market is Neutral</div>', unsafe_allow_html=True)

        st.line_chart(df['Close'])

        if st.button("🔊 Listen Audio Analysis"):
            msg = f"The price is {latest_price:.1f} and R.S.I is {latest_rsi:.1f}. Market is neutral."
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{msg}'));</script>", height=0)
except Exception as e:
    st.info("Searching for stock data...")
