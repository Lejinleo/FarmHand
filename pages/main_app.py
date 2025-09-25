import streamlit as st

def run_app():
    # --- Page Config ---
    st.set_page_config(page_title="Kerala Farming Assistant", page_icon="🌿", layout="wide")

    # --- Sidebar ---
    with st.sidebar:
        st.header(f"👋 Welcome, {st.session_state.username}")
        if st.button("Logout"):
            logout()
        st.markdown("---")
        st.header("Navigation")
        page = st.radio("Choose a feature", ["Crop Disease Analyzer", "Farming Advisor Chatbot", "Price Prediction"])

    # --- Main Title ---
    st.markdown('<h1 style="text-align:center;color:#2E7D32;">🌿 Kerala AI Farming Assistant 🌿</h1>', unsafe_allow_html=True)

    # --- Load Selected Page ---
    if page == "Crop Disease Analyzer":
        import disease_analyzer
        disease_analyzer.show_page()

    elif page == "Farming Advisor Chatbot":
        import advisor_chatbot
        advisor_chatbot.show_page()

    elif page == "Price Prediction":
        import price_prediction
        price_prediction.show_page()
    elif page == "Market Best Prices":
        import marketbest
        marketbest.show_page()

# --- Logout Function ---
def logout():
    st.session_state.logged_in = False
    st.session_state.username = ""
    # Reload login page automatically
    st.experimental_rerun()  # This should work in updated Streamlit versions


