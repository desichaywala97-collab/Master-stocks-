import streamlit as st

# --- SABSE PEHLE LIBRARIES CHECK KAREIN ---
try:
    import yfinance as yf
    import pandas as pd
    import numpy as np
except ImportError as e:
    st.error(f"Missing Library: {e}. Please wait 1 minute for installation...")
    st.stop()

# --- DESIGN & LOOK ---
st.set_page_config(page_title="Master Stocks AI", layout="wide")

st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; border: 1px solid #4B506D; padding: 20px; border-radius: 12px; }
    .status-box { padding: 15px; border-radius: 10px; font-weight: bold; text-align: center; border: 1px solid #FFA500; color: #FFA500; background: rgba(255,165,0,0.1); }
    [data-testid="stMetricValue"] { color: #00FFC2 !important; }
    </style>
    """, unsafe_allow_html=True)

# --- RSI LOGIC ---
def get_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# --- UI ---
st.title("📈 Master Stocks AI Terminal")

with st.sidebar:
    symbol = st.text_input("Enter Stock Symbol", "RELIANCE.NS")
    duration = st.selectbox("Duration", ["1mo", "6mo", "1y"])
    speak_btn = st.button("🔊 Listen Analysis")

try:
    df = yf.download(symbol, period=duration)
    
    if not df.empty:
        df['RSI'] = get_rsi(df['Close'])
        lp = float(df['Close'].iloc[-1])
        rv = float(df['RSI'].iloc[-1])

        # METRICS: Live Price | RSI | Status
        c1, c2, c3 = st.columns(3)
        c1.metric("Live Price", f"₹{lp:,.2f}")
        c2.metric("RSI (14D)", f"{rv:.1f}")
        
        with c3:
            st.write("Market Signal")
            if rv < 35:
                st.success("🚀 BUY SIGNAL (Oversold)")
                msg = "Market is Oversold. Buying opportunity."
            elif rv > 65:
                st.error("⚠️ SELL SIGNAL (Overbought)")
                msg = "Market is Overbought. Selling opportunity."
            else:
                st.markdown('<div class="status-box">⚖️ Market is Neutral</div>', unsafe_allow_html=True)
                msg = "Market is Neutral. Stay cautious."

        st.line_chart(df['Close'])

        # VOICE
        if speak_btn:
            full_txt = f"Stock {symbol}. Current price {lp:.1f}. RSI is {rv:.1f}. {msg}"
            st.components.v1.html(f"<script>window.speechSynthesis.speak(new SpeechSynthesisUtterance('{full_txt}'));</script>", height=0)

    else:
        st.warning("Invalid Ticker. Please check the symbol.")

except Exception as e:
    st.error(f"Data Fetch Error: {e}")
