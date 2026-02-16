import streamlit as st
import yfinance as yf
import pandas as pd
import numpy as np

# 1. Professional Page Setup
st.set_page_config(page_title="Master Stocks Pro 2026", layout="wide")

# Custom CSS for Professional Design (Dark Mode UI)
st.markdown("""
    <style>
    .main { background-color: #0E1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #4B506D; }
    [data-testid="stMetricValue"] { color: #00FFC2 !important; }
    .buy-signal { color: #00FF7F; font-weight: bold; font-size: 24px; border: 2px solid #00FF7F; padding: 10px; border-radius: 5px; text-align: center; background-color: rgba(0, 255, 127, 0.1); }
    .sell-signal { color: #FF4B4B; font-weight: bold; font-size: 24px; border: 2px solid #FF4B4B; padding: 10px; border-radius: 5px; text-align: center; background-color: rgba(255, 75, 75, 0.1); }
    .neutral-signal { color: #FFA500; font-weight: bold; font-size: 24px; border: 2px solid #FFA500; padding: 10px; border-radius: 5px; text-align: center; background-color: rgba(255, 165, 0, 0.1); }
    </style>
    """, unsafe_allow_html=True)

# 2. RSI Calculation Function
def get_rsi(data, window=14):
    delta = data.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
    rs = gain / loss
    return 100 - (100 / (1 + rs))

# 3. JavaScript Voice Function (No Library Needed)
def speak_text(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance("{text}");
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

st.title("📈 Master Stocks - Professional Terminal")

# Sidebar for Input
with st.sidebar:
    st.header("Control Panel")
    ticker = st.text_input("Stock Ticker", value="RELIANCE.NS")
    period = st.selectbox("Select Duration", ["1mo", "3mo", "6mo", "1y"])
    st.info("Example: RELIANCE.NS, TATAMOTORS.NS, TSLA, AAPL")

# 4. Data Processing & Logic
try:
    df = yf.download(ticker, period=period, interval="1d")
    
    if not df.empty:
        # RSI Calculation
        df['RSI'] = get_rsi(df['Close'])
        latest_price = float(df['Close'].iloc[-1])
        latest_rsi = float(df['RSI'].iloc[-1])
        prev_price = float(df['Close'].iloc[-2])
        price_diff = latest_price - prev_price
        
        # Display Metrics
        col1, col2, col3 = st.columns(3)
        col1.metric("Current Price", f"₹{latest_price:,.2f}", f"{price_diff:,.2f}")
        
        # Safe RSI Display
        rsi_display = f"{latest_rsi:.1f}" if not pd.isna(latest_rsi) else "Loading.."
        col2.metric("RSI Momentum", rsi_display)
        
        # Buy/Sell Logic UI
        with col3:
            st.write("### Market Signal")
            if latest_rsi < 30:
                st.markdown('<div class="buy-signal">STRONG BUY</div>', unsafe_allow_html=True)
                signal_status = "Oversold. This is a strong buy opportunity."
            elif latest_rsi > 70:
                st.markdown('<div class="sell-signal">STRONG SELL</div>', unsafe_allow_html=True)
                signal_status = "Overbought. You should consider selling."
            else:
                st.markdown('<div class="neutral-signal">NEUTRAL</div>', unsafe_allow_html=True)
                signal_status = "in Neutral zone. Wait for a clear trend."

        # Chart
        st.subheader(f"Price Analysis: {ticker}")
        st.line_chart(df['Close'], use_container_width=True)

        # 5. Speak Feature
        if st.button("🔊 Listen to Audio Analysis"):
            speech_msg = f"Analysis for {ticker}. The current price is {latest_price:.1f}. The R.S.I is {rsi_display}. The market is {signal_status}"
            speak_text(speech_msg)

    else:
        st.warning("Please enter a valid stock ticker.")

except Exception as e:
    st.error(f"An error occurred: {e}")

# Footer
st.markdown("---")
st.caption("Powered by Master Stocks AI Terminal 2026")
