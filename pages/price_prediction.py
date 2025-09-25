import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# --- PAGE LAYOUT ---
st.header("📊 Crop Price Prediction")
st.write("Select a crop and market to view current price, trends, and predictions.")

# --- Dropdown Selections ---
# Using more relevant crops for Kerala
crops = ["Rice", "Coconut", "Banana", "Black Pepper", "Ginger"]
markets = ["Thiruvananthapuram", "Kochi", "Kozhikode", "Thrissur"]

selected_crop = st.selectbox("Select Crop", ["-- Select Crop --"] + crops)
selected_market = st.selectbox("Select Market", ["-- Select Market --"] + markets)

# --- Show results only if both are selected ---
if selected_crop in crops and selected_market in markets:
    st.subheader(f"📈 Price Analysis for {selected_crop} in {selected_market}")

    # --- Mock Current Price ---
    # In a real app, this data would come from an API or a database
    np.random.seed(hash(selected_crop) + hash(selected_market))
    current_price = np.random.randint(2500, 5000)  # random current price in ₹/quintal

    # --- Mock Historical Prices ---
    days = pd.date_range(end=pd.Timestamp.today(), periods=30)
    historical_prices = current_price + np.random.randint(-500, 500, size=30)

    # --- Mock Predicted Prices (Next 7 Days) ---
    future_days = pd.date_range(start=pd.Timestamp.today() + pd.Timedelta(days=1), periods=7)
    predicted_prices = np.linspace(historical_prices[-1], historical_prices[-1] + np.random.randint(-200, 300), 7)

    # --- Plot Historical + Predicted ---
    fig, ax = plt.subplots(figsize=(9,4))
    ax.plot(days, historical_prices, label="Historical Prices", color="blue", marker='.')
    ax.plot(future_days, predicted_prices, label="Predicted Prices", color="orange", linestyle="--", marker="o")
    ax.axhline(y=current_price, color="green", linestyle=":", label=f"Current Market Price: ₹{current_price}")

    # Format x-axis for better readability
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%b %d"))
    ax.xaxis.set_major_locator(mdates.AutoDateLocator(maxticks=10))
    fig.autofmt_xdate() # Auto-rotate dates

    ax.set_xlabel("Date")
    ax.set_ylabel("Price (₹/quintal)")
    ax.set_title(f"{selected_crop} Prices in {selected_market}")
    ax.legend()
    ax.grid(True, linestyle='--', alpha=0.6)
    st.pyplot(fig)

    # --- Forecast Summary ---
    st.markdown("### 📌 Forecast Summary")
    st.info(f"""
    - **Current Price:** ₹{current_price}
    - **Predicted Price Range (Next 7 Days):** ₹{int(predicted_prices.min())} – ₹{int(predicted_prices.max())}
    - **Trend:** {"The price is expected to rise slightly in the coming week." if predicted_prices[-1] > historical_prices[-1] else "The price trend appears to be stable or slightly decreasing."}
    """)
else:
    st.warning("👆 Please select both a crop and a market to see the price prediction.")