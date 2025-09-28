# price_comparison.py

import streamlit as st
import pandas as pd
import requests

# --- Data Fetching Function ---
@st.cache_data
def get_price_data(crop, market):
    """
    Fetches price data from the data.gov.in API for a specific crop and market.
    """
    try:
        api_key = st.secrets["API_KEY"]
        resource_id = "9ef84268-d588-465a-a308-a864a43d0070"
        base_url = f"https://api.data.gov.in/resource/{resource_id}"
        params = {
            "api-key": api_key,
            "format": "json",
            "filters[state.keyword]": "Kerala",
            "filters[market]": market,
            "filters[commodity]": crop,
            "limit": 1 # Only most recent price
        }
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
        records = data.get('records', [])
        if not records:
            return None
        return records[0]
    except (requests.exceptions.RequestException, KeyError):
        return None

# --- Function to get prices from all markets ---
def get_all_market_prices(crop, markets_list):
    price_data = []
    for market in markets_list:
        record = get_price_data(crop, market)
        if record:
            price_data.append({
                "Market": record.get('market'),
                "Price": pd.to_numeric(record.get('modal_price'), errors='coerce')
            })

    if not price_data:
        return None

    df = pd.DataFrame(price_data)
    df.dropna(inplace=True)
    return df.set_index('Market')

# --- SHOW PAGE FUNCTION ---
def show_page():
    st.header("📊 Daily Market Price Comparison")
    st.write("Select a crop to see today's prices across major markets in Kerala.")

    crops = ["Rice", "Coconut", "Banana", "Black Pepper", "Ginger", "Rubber"]
    markets = ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Palakkad"]

    selected_crop = st.selectbox("Select Crop", crops)

    if selected_crop:
        st.subheader(f"📍 Today's Prices for {selected_crop} in Kerala")

        market_prices_df = get_all_market_prices(selected_crop, markets)

        if market_prices_df is not None and not market_prices_df.empty:
            st.bar_chart(market_prices_df, height=400)

            st.markdown("### 🏷️ Price Summary (per quintal)")
            st.dataframe(market_prices_df.sort_values(by="Price", ascending=False))

            best_market = market_prices_df['Price'].idxmax()
            best_price = market_prices_df['Price'].max()
            st.success(f"**Best Market:** You can get the highest price for {selected_crop} today in **{best_market}** at **₹{best_price:,.2f}** per quintal.")
        else:
            st.warning(f"Could not retrieve price data for {selected_crop} today. Please try again later.")
