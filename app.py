import streamlit as st

# --- Page Configuration ---
st.set_page_config(
    page_title="Kerala Farming Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS ---
st.markdown("""
<style>
    .title {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32;
        text-align: center;
        padding: 20px;
    }
    .st-emotion-cache-16txtl3 {
        background-color: #E8F5E9;
    }
</style>
""", unsafe_allow_html=True)

# --- Sidebar Navigation ---
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a feature", ["Crop Disease Analyzer", "Farming Advisor Chatbot", "Price Prediction"])

st.markdown('<p class="title">🌿 Kerala AI Farming Assistant 🌿</p>', unsafe_allow_html=True)

# --- Import Pages ---
if page == "Crop Disease Analyzer":
    import disease_analyzer
    disease_analyzer.show_page()

elif page == "Farming Advisor Chatbot":
    import advisor_chatbot
    advisor_chatbot.show_page()

elif page == "Price Prediction":
    import price_prediction
    price_prediction.show_page()
