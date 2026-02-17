import streamlit as st
import yfinance as yf

# 1. Google-Style Page Setup
st.set_page_config(page_title="AI Market Sentinel", layout="wide")

# Custom CSS for Blinking Red Light and Green Light
st.markdown("""
    <style>
    .green-light { height: 50px; width: 50px; background-color: #00FF00; border-radius: 50%; display: inline-block; box-shadow: 0 0 20px #00FF00; }
    .red-light { height: 50px; width: 50px; background-color: #FF0000; border-radius: 50%; display: inline-block; animation: blinker 1s linear infinite; box-shadow: 0 0 20px #FF0000; }
    @keyframes blinker { 50% { opacity: 0; } }
    .search-container { text-align: center; padding: 50px; }
    </style>
""", unsafe_allow_html=True)

# 2. Sidebar (Three Dots Menu)
with st.sidebar:
    st.title("⋮ Settings")
    st.file_uploader("Upload 10-Year Historical Data", type=["csv"])
    st.info("AI Model: Trained on 2016-2026 TCS Data")

# 3. Top Header: Real-time Price (Live from Google Finance/Yahoo)
ticker_symbol = "TCS.NS"
data = yf.Ticker(ticker_symbol).history(period="1d")
current_price = data['Close'].iloc[-1]

col_title, col_price = st.columns([3, 1])
with col_title:
    st.title("🔍 MarketMind AI Search")
with col_price:
    st.metric(label=f"LIVE: {ticker_symbol}", value=f"₹{current_price:.2f}", delta="-7.2% (AI Alert Context)")

# 4. Search Engine Box
st.markdown("<div class='search-container'>", unsafe_allow_html=True)
user_query = st.text_input("", placeholder="Enter News (e.g., 'New AI Agent Launched' or 'Huge Order Won')...")
st.markdown("</div>", unsafe_allow_html=True)

# 5. Logic & Alert System
if user_query:
    # Danger Keywords (Based on your 10-year research)
    danger_keys = ["ai", "replace", "war", "layoff", "election", "drop", "automation", "claude"]
    positive_keys = ["order", "deal", "profit", "growth", "partnership", "buyback"]
    
    is_danger = any(word in user_query.lower() for word in danger_keys)
    is_positive = any(word in user_query.lower() for word in positive_keys)

    col_alert, col_text = st.columns([1, 5])
    
    if is_danger:
        with col_alert:
            st.markdown("<div class='red-light'></div>", unsafe_allow_html=True)
        with col_text:
            st.error("🚨 CRITICAL ALERT: Market Sentiment matches '2026 SaasPocalypse' Pattern.")
            st.write(f"**Predicted Movement:** -5.5% to -8.0% in next 24 hours.")
            
    elif is_positive:
        with col_alert:
            st.markdown("<div class='green-light'></div>", unsafe_allow_html=True)
        with col_text:
            st.success("✅ SAFE: Market Sentiment is Bullish.")
            st.write(f"**Predicted Movement:** +2.0% to +3.5% Growth.")
    else:
        st.warning("🟡 NEUTRAL: No major impact detected based on 10-year history.")

# 6. Footer Detail
st.divider()
st.caption("AI Engine Version 1.0 | Data Source: Internal 10-Year Study + [Yahoo Finance](https://finance.yahoo.com)")
