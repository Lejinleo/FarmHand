import streamlit as st

# --- Page Configuration ---
# This command should be run only once, in your main app file.
st.set_page_config(
    page_title="Kerala Farming Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Styling ---
# This CSS will apply to all pages in your app.
st.markdown("""
<style>
    .title {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        padding: 20px;
    }
    /* You can add more global styles here */
</style>
""", unsafe_allow_html=True)

# --- Main Page Content ---
st.markdown('<p class="title">🌿 Kerala AI Farming Assistant 🌿</p>', unsafe_allow_html=True)

st.header("Welcome to your AI-Powered Farming Co-Pilot")
st.write("""
Navigate through the features using the sidebar on the left.
- **Crop Disease Analyzer:** Upload a photo of a crop leaf to identify diseases instantly.
- **Farming Advisor Chatbot:** Get answers to your farming questions.
- **Price Prediction:** View market trends and future price predictions for your crops.
""")

