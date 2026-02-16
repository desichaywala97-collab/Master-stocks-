import streamlit as st
import pandas as pd
import numpy as np

# Error handling: Agar library abhi tak install nahi hui toh user ko guide karega
try:
    import yfinance as yf
except ImportError:
    st.error("⚠️ 'yfinance' library nahi mili. Kripya apni GitHub repo mein 'requirements.txt' file check karein.")
    st.stop()

# 1. Dashboard Style & Setup
st.set_page_config(page_title="Master Stocks AI 2026", layout="wide")

st.markdown("""
    <style>
    .metric-card { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4B506D; }
    .buy-signal { color: #00FF7F; font-size: 22px; font-weight: bold; background: rgba(0,255,127,0.1); padding: 10px; border-radius: 5px; text-align: center; }
    .sell-signal { color: #FF4B4B; font-size: 22px; font-weight: bold; background: rgba(255,75,75,0.1); padding: 10px; border-radius: 5px; text-align: center; }
    </style>
    """, unsafe_allow_html=True)

# 2. Voice Function (No Library Required)
def speak_now(text):
    js_code = f"""<script>var msg = new SpeechSynthesisUtterance("{text}");window.speechSynthesis.speak(msg);</script>"""
    st.components.v1.html(js_code, height=0)

# 3. RSI Calculation
def get_rsi(series, period=14):
    delta = series.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

st.title("📈 Master Stocks AI Terminal")

# Input
symbol = st.sidebar.text_input("Enter Stock Symbol", "RELIANCE.NS")
period = st.sidebar.selectbox("Duration", ["1mo", "6mo", "1y"])

try:
    data = yf.download(symbol, period=period)
    if not data.empty:
        data['RSI'] = get_rsi(data['Close'])
        current_price = float(data['Close'].iloc[-1])
        rsi_val = float(data['RSI'].iloc[-1])
        
        # UI Columns
        col1, col2, col3 = st.columns(3)
        col1.metric("Live Price", f"₹{current_price:,.2f}")
        col2.metric("RSI (14D)", f"{rsi_val:.1f}")
        
        with col3:
            if rsi_val < 30:
                st.markdown('<div class="buy-signal">🚀 BUY SIGNAL</div>', unsafe_allow_html=True)
                rec = "Oversold. Possible trend reversal."
            elif rsi_val > 70:
                st.markdown('<div class="sell-signal">⚠️ SELL SIGNAL</div>', unsafe_allow_html=True)
                rec = "Overbought. Be careful."
            else:
                st.info("Market is Neutral")
                rec = "Holding in neutral range."

        st.line_chart(data['Close'])
        
        if st.button("🔊 Listen Audio Analysis"):
            speak_now(f"The current price of {symbol} is {current_price:.1f}. RSI is {rsi_val:.1f}. Analysis shows {rec}")
            
except Exception as e:
    st.warning("Data fetch karne mein dikkat aa rahi hai. Ticker check karein.")
