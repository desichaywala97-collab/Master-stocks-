import streamlit as st
import yfinance as yf
import pandas_ta as ta
import plotly.graph_objects as go
from datetime import datetime

# --- Page Config ---
st.set_page_config(page_title="My Stock AI Pro", layout="wide")

# --- Custom Styling ---
st.markdown("""
    <style>
    .stMetric { background-color: #1e2130; padding: 15px; border-radius: 10px; }
    </style>
    """, unsafe_allow_html=True)

# --- Sidebar ---
st.sidebar.header("🛠️ Control Panel")
# Aap yahan koi bhi Indian stock likh sakte hain (e.g. TCS.NS, ZOMATO.NS)
symbol = st.sidebar.text_input("Stock Ticker", value="RELIANCE.NS").upper()
time_range = st.sidebar.select_slider("Select Timeframe", options=['1mo', '3mo', '6mo', '1y', '5y'])

# --- Data Engine ---
@st.cache_data(ttl=600) # 10 min cache
def load_data(ticker, period):
    try:
        data = yf.download(ticker, period=period, interval="1d")
        return data
    except:
        return None

data = load_data(symbol, time_range)

# --- App Layout ---
st.title(f"🚀 {symbol} Live Intelligence")
st.caption(f"Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M')}")

if data is not None and not data.empty:
    # Indicators Calculation
    data['RSI'] = ta.rsi(data['Close'], length=14)
    
    # --- Row 1: Metrics (Safe Version) ---
    m1, m2, m3, m4 = st.columns(4)
    
    # Prices and Change
    curr_p = float(data['Close'].iloc[-1])
    prev_p = float(data['Close'].iloc[-2])
    change = ((curr_p - prev_p) / prev_p) * 100
    
    # Displaying Metrics
    m1.metric("Current Price", f"₹{curr_p:,.2f}", f"{change:.2f}%")
    
    rsi_val = data['RSI'].iloc[-1]
    m2.metric("RSI (Momentum)", f"{rsi_val:.1f}" if not pd.isna(rsi_val) else "Wait..")
    
    m3.metric("Highest (Period)", f"₹{data['High'].max():,.0f}")
    m4.metric("Lowest (Period)", f"₹{data['Low'].min():,.0f}")

    # --- Row 2: Live Candlestick Chart ---
    st.subheader("🕯️ Market Trend")
    fig = go.Figure(data=[go.Candlestick(x=data.index,
                    open=data['Open'], high=data['High'],
                    low=data['Low'], close=data['Close'], name='Price')])
    fig.update_layout(template="plotly_dark", margin=dict(l=10, r=10, t=10, b=10))
    st.plotly_chart(fig, use_container_width=True)

    # --- Row 3: AI Verdict ---
    st.divider()
    st.subheader("🧠 AI Investment Verdict")
    
    if not pd.isna(rsi_val):
        if rsi_val < 35:
            st.success(f"🔥 **BUY SIGNAL:** {symbol} is Oversold. High probability of bounce back!")
        elif rsi_val > 65:
            st.error(f"⚠️ **SELL SIGNAL:** {symbol} is Overbought. Price might fall soon!")
        else:
            st.info(f"⚖️ **NEUTRAL:** {symbol} is in stable zone. Hold and Watch.")
    else:
        st.warning("Collecting more data for RSI...")

else:
    st.error("Error: Stock symbol galat hai ya data nahi mil raha. Please check (e.g. RELIANCE.NS)")

# Footer
st.markdown("---")
st.write("Built with ❤️ for Indian Traders")
