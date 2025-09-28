import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- Data Fetching Function (MODIFIED to use Sample Data) ---
@st.cache_data
def get_price_data(crop, market):
    seed_value = (hash(crop) + hash(market)) % (2**32)
    np.random.seed(seed_value)

    today = pd.Timestamp.today()
    dates = pd.date_range(end=today, periods=30, freq='D')
    
    base_price = np.random.randint(2000, 5000)
    price_fluctuations = np.random.randint(-150, 155, size=30).cumsum()
    prices = base_price + price_fluctuations

    df = pd.DataFrame({'date': dates, 'price': prices})
    return df


# ✅ WRAP EVERYTHING IN show_page() FUNCTION
def show_page():
    st.header("📊 Crop Price Prediction")
    st.write("Select a crop and market to view current price, trends, and predictions.")

    crops = ["Paddy(Dhan)(Common)", "Coconut", "Banana", "Black Pepper", "Ginger","Carrot" ,"Rubber"]
    markets = ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur", "Palakkad","Kottayam"]

    selected_crop = st.selectbox("Select Crop", crops)
    selected_market = st.selectbox("Select Market", markets)

    if selected_crop and selected_market:
        st.subheader(f"📈 Price Analysis for {selected_crop} in {selected_market}")

        price_data = get_price_data(selected_crop, selected_market)

        if price_data is not None and not price_data.empty:
            days = price_data['date']
            historical_prices = price_data['price']
            current_price = historical_prices.iloc[-1]
            
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
