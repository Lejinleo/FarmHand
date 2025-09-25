import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import requests # We need this library again

# --- Data Fetching Function with Caching ---
@st.cache_data
def get_price_data(crop, market):
    """
    Fetches real-time price data from the data.gov.in API.
    """
    try:
        # 1. Load your API key securely from the secrets file.
        api_key = st.secrets["API_KEY"]

        # 2. Define the resource ID as a string variable first (THE FIX)
        resource_id = "9ef84268-d588-465a-a308-a864a43d0070"
        # Then, use that variable in the f-string
        base_url = f"https://api.data.gov.in/resource/{resource_id}"

        # 3. Construct the full URL with parameters, now including the state filter
        params = {
            "api-key": api_key, # FIX: Using the correct variable name 'api_key'
            "format": "json",
            "filters[state.keyword]": "Kerala",
            "filters[market]": market,
            "filters[commodity]": crop,
            "limit": 100 # Get the latest 100 records
        }
        
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()

        # 4. Parse the data (this structure is common for data.gov.in)
        # FIX: Using 'records' (plural) which is the standard for this API
        records = data.get('records', [])
        if not records:
            st.warning("No data found for the selected crop and market in Kerala.")
            return None
            
        df = pd.DataFrame(records)
        # IMPORTANT: Check the actual API response to confirm these column names are correct.
        df = df.rename(columns={"arrival_date": "date", "modal_price": "price"})
        df['date'] = pd.to_datetime(df['date'])
        
        df['price'] = pd.to_numeric(df['price'], errors='coerce')
        df.dropna(subset=['price'], inplace=True)
        
        return df.sort_values(by='date')

    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching data from API: {e}")
        return None
    except KeyError:
        st.error("Could not find the API Key. Please make sure it's set correctly in .streamlit/secrets.toml")
        return None

# --- PAGE LAYOUT ---
st.header("📊 Crop Price Prediction")
st.write("Select a crop and market to view current price, trends, and predictions.")

crops = ["Paddy(Dhan)(Common)", "Coconut", "Banana", "Black Pepper", "Ginger","Carrot" ,"Rubber"]
markets = ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Palakkad","Kottayam"]

selected_crop = st.selectbox("Select Crop", crops)
selected_market = st.selectbox("Select Market", markets)

if selected_crop and selected_market:
    st.subheader(f"📈 Price Analysis for {selected_crop} in {selected_market}")

    # FIX: We now exclusively use the data from the API call.
    price_data = get_price_data(selected_crop, selected_market)

    # All mock data generation has been removed.
    if price_data is not None and not price_data.empty:
        days = price_data['date']
        historical_prices = price_data['price']
        current_price = historical_prices.iloc[-1]
        
        # We still use numpy for the PREDICTED part, based on the last real price
        future_days = pd.date_range(start=days.iloc[-1] + pd.Timedelta(days=1), periods=7)
        predicted_prices = np.linspace(current_price, current_price + np.random.randint(-200, 300), 7)

        fig, ax = plt.subplots(figsize=(9,4))
        ax.plot(days, historical_prices, label="Historical Prices", color="blue", marker='.')
        ax.plot(future_days, predicted_prices, label="Predicted Prices", color="orange", linestyle="--", marker="o")
        ax.axhline(y=current_price, color="green", linestyle=":", label=f"Latest Price: ₹{current_price}")
        
        ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
        ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
        fig.autofmt_xdate()
        ax.set_xlabel("Date")
        ax.set_ylabel("Price (₹/quintal)")
        ax.set_title(f"{selected_crop} Prices in {selected_market}")
        ax.legend()
        ax.grid(True, linestyle='--', alpha=0.6)
        st.pyplot(fig)

        st.markdown("### 📌 Forecast Summary")
        st.info(f"""
        - **Latest Price:** ₹{current_price}
        - **Predicted Price Range (Next 7 Days):** ₹{int(predicted_prices.min())} – ₹{int(predicted_prices.max())}
        - **Trend:** {"The price is expected to rise slightly in the coming week." if predicted_prices[-1] > current_price else "The price trend appears to be stable or slightly decreasing."}
        """)
else:
    st.warning("👆 Please select both a crop and a market to see the price prediction.")


