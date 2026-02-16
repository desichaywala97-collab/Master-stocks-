
import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np
from streamlit_tts import text_to_speech

# 1. Professional Page Setup
st.set_page_config(page_title="Master Stocks Pro 2026", layout="wide")

# Custom CSS for Professional Design
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4B506D; }
    [data-testid="stMetricValue"] { color: #00FFC2 !important; }
    .buy-signal { color: #00FF7F; font-weight: bold; font-size: 24px; border: 2px solid #00FF7F; padding: 10px; border-radius: 5px; text-align: center; }
    .sell-signal { color: #FF4B4B; font-weight: bold; font-size: 24px; border: 2px solid #FF4B4B; padding: 10px; border-radius: 5px; text-align: center; }
    .neutral-signal { color: #FFA500; font-weight: bold; font-size: 24px; border: 2px solid #FFA500; padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI Logic Function
def get_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

st.title("🚀 Master Stocks - Smart Terminal")

# Sidebar for Input
with st.sidebar:
    st.header("Settings")
    ticker = st.text_input("Stock Ticker", value="RELIANCE.NS")
    period = st.selectbox("Select Duration", ["1mo", "3mo", "6mo", "1y"])
    speak_btn = st.button("🔊 Listen to Analysis")

# 3. Data Processing
try:
    df = yf.download(ticker, period=period, interval="1d")
    if not df.empty:
        df['RSI'] = get_rsi(df['Close'])
        latest_price = float(df['Close'].iloc[-1])
        latest_rsi = float(df['RSI'].iloc[-1])
        prev_price = float(df['Close'].iloc[-2])
        price_diff = latest_price - prev_price
        
        # UI Columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"₹{latest_price:,.2f}", f"{price_diff:,.2f}")
        col2.metric("RSI Momentum", f"{latest_rsi:.1f}")
        
        # Buy/Sell Logic
        with col3:
            st.write("### Market Signal")
            if latest_rsi < 30:
                st.markdown('<div class="buy-signal">STRONG BUY</div>', unsafe_allow_html=True)
                signal_text = "Buy"
            elif latest_rsi > 70:
                st.markdown('<div class="sell-signal">STRONG SELL</div>', unsafe_allow_html=True)
                signal_text = "Sell"
            else:
                st.markdown('<div class="neutral-signal">NEUTRAL</div>', unsafe_allow_html=True)
                signal_text = "Wait"

        # Chart Display
        st.line_chart(df['Close'], use_container_width=True)

        # 4. Speak Command Logic
        if speak_btn:
            msg = f"The price of {ticker} is {latest_price:.1f} rupees. The R.S.I value is {latest_rsi:.1f}. "
            if signal_text == "Buy":
                msg += "Stock is oversold. This might be a good buying opportunity."
            elif signal_text == "Sell":
                msg += "Stock is overbought. You should consider selling or booking profits."
            else:
                msg += "The market is in neutral zone. Please wait for a clear signal."
            text_to_speech(msg, language='en')

    else:
        st.error("Invalid Ticker or No Data Found.")

except Exception as e:
    st.error(f"Error: {e}")
