import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="FinTech Pro", layout="wide", initial_sidebar_state="expanded")

# --- Custom CSS for Styling ---
st.markdown("""
    <style>
    .main { background-color: #0e1117; color: white; }
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; border: 1px solid #3e4255; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("🛠️ Control Panel")
symbol = st.sidebar.text_input("Stock Ticker", value="RELIANCE.NS")
time_range = st.sidebar.select_slider("Select Timeframe", options=['1mo', '3mo', '6mo', '1y', '5y'])

# --- Data Engine ---
@st.cache_data
def load_data(ticker, period):
    data = yf.download(ticker, period=period)
    return data

data = load_data(symbol, time_range)

# --- App Layout ---
st.title(f"📈 {symbol} Intelligence Dashboard")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if not data.empty:
    # Indicators
    data['RSI'] = ta.rsi(data['Close'], length=14)
    data['EMA_20'] = ta.ema(data['Close'], length=20)
    
    # --- Row 1: Metrics ---
    m1, m2, m3, m4 = st.columns(4)
    current_price = data['Close'].iloc[-1]
    prev_price = data['Close'].iloc[-2]
    change = ((current_price - prev_price) / prev_price) * 100
    
    m1.metric("Current Price", f"₹{current_price:,.2f}", f"{change:.2f}%")
    m2.metric("RSI (Momentum)", f"{data['RSI'].iloc[-1]:.1f}")
    m3.metric("24h High", f"₹{data['High'].iloc[-1]:,.0f}")
    m4.metric("24h Low", f"₹{data['Low'].iloc[-1]:,.0f}")

    # --- Row 2: Charts ---
    tab1, tab2 = st.tabs(["🕯️ Candlestick Chart", "📊 Volume & Indicators"])
    
    with tab1:
        fig = go.Figure(data=[go.Candlestick(x=data.index, open=data['Open'], 
                        high=data['High'], low=data['Low'], close=data['Close'])])
        fig.update_layout(template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        st.bar_chart(data['Volume'])

    # --- Row 3: AI Insights ---
    st.divider()
    st.subheader("🧠 Smart Verdict")
    rsi_val = data['RSI'].iloc[-1]
    
    if rsi_val < 35:
        st.success("🔥 **BUY ALERT:** Stock is highly oversold. Good entry point!")
    elif rsi_val > 65:
        st.error("⚠️ **SELL ALERT:** Overbought zone. Risk of price drop.")
    else:
        st.info("⚖️ **NEUTRAL:** Stock is in a stable range. No immediate action.")

else:
    st.warning("Symbol not found. Please check and try again.")
