import streamlit as st
import pandas as pd
import numpy as np

# Error handling for missing libraries
try:
    import yfinance as yf
except ImportError:
    st.error("Missing Library: Please run 'pip install yfinance' in your terminal.")
    st.stop()

# 1. Page Config & Professional Styling
st.set_page_config(page_title="Master Stocks AI", layout="wide", initial_sidebar_state="expanded")

st.markdown("""
    <style>
    .main { background-color: #0E1117; }
    .metric-card { background-color: #1e2130; padding: 20px; border-radius: 12px; border: 1px solid #3e445e; text-align: center; }
    .signal-box { padding: 15px; border-radius: 8px; font-weight: bold; font-size: 20px; margin-top: 10px; text-align: center; }
    .buy { background-color: rgba(0, 255, 127, 0.2); color: #00FF7F; border: 1px solid #00FF7F; }
    .sell { background-color: rgba(255, 75, 75, 0.2); color: #FF4B4B; border: 1px solid #FF4B4B; }
    .hold { background-color: rgba(255, 165, 0, 0.2); color: #FFA500; border: 1px solid #FFA500; }
    </style>
    """, unsafe_allow_html=True)

# 2. Advanced Functions (RSI & MACD)
def calculate_indicators(data):
    # RSI
    delta = data['Close'].diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
    rs = gain / loss
    data['RSI'] = 100 - (100 / (1 + rs))
    
    # MACD
    exp1 = data['Close'].ewm(span=12, adjust=False).mean()
    exp2 = data['Close'].ewm(span=26, adjust=False).mean()
    data['MACD'] = exp1 - exp2
    data['Signal_Line'] = data['MACD'].ewm(span=9, adjust=False).mean()
    return data

# 3. JavaScript Speak Function
def speak_analysis(text):
    js_code = f"""<script>var m = new SpeechSynthesisUtterance("{text}");window.speechSynthesis.speak(m);</script>"""
    st.components.v1.html(js_code, height=0)

# 4. App Header
st.title("🛡️ Master Stocks AI Terminal")
st.subheader("Smart Analysis for 2026 Trading")

# Sidebar
with st.sidebar:
    st.header("Search Parameters")
    symbol = st.text_input("Enter Ticker (e.g. AAPL, BTC-USD)", "RELIANCE.NS")
    timeframe = st.selectbox("Interval", ["1mo", "6mo", "1y", "5y"])
    analyze_btn = st.button("🚀 Run AI Analysis")

# 5. Main Logic
try:
    df = yf.download(symbol, period=timeframe)
    if not df.empty:
        df = calculate_indicators(df)
        last_price = float(df['Close'].iloc[-1])
        last_rsi = float(df['RSI'].iloc[-1])
        last_macd = float(df['MACD'].iloc[-1])
        last_sig = float(df['Signal_Line'].iloc[-1])
        
        # Display Row 1
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric("Live Price", f"₹{last_price:,.2f}")
        with c2:
            st.metric("RSI (14)", f"{last_rsi:.1f}")
        with c3:
            # Signal Logic
            if last_rsi < 35 and last_macd > last_sig:
                st.markdown('<div class="signal-box buy">🚀 STRONG BUY</div>', unsafe_allow_html=True)
                advice = "Stock is oversold with a bullish crossover. Good time to buy."
            elif last_rsi > 65 and last_macd < last_sig:
                st.markdown('<div class="signal-box sell">⚠️ SELL NOW</div>', unsafe_allow_html=True)
                advice = "Stock is overbought. Book your profits now."
            else:
                st.markdown('<div class="signal-box hold">⚖️ HOLD / NEUTRAL</div>', unsafe_allow_html=True)
                advice = "Market is stable. Wait for a clear RSI or MACD breakout."

        # Chart
        st.line_chart(df['Close'])

        # Speak Logic
        if analyze_btn:
            speech_text = f"Master Stocks Analysis for {symbol}. Current price is {last_price:.1f}. RSI is {last_rsi:.1f}. Our recommendation is {advice}"
            speak_analysis(speech_text)
            
    else:
        st.warning("No data found for this symbol.")
except Exception as e:
    st.error(f"Connect Error: {e}")

st.divider()
st.caption("Master Stocks Pro | AI Driven Financial Insights")
