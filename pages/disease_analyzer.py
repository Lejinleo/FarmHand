import streamlit as st
from PIL import Image
import time

# --- MOCK API FUNCTION ---
def analyze_image_with_gemini(uploaded_image):
    with st.spinner('Analyzing the crop leaf... Please wait.'):
        time.sleep(3)
    return {
        "disease_name": "Rice Leaf Blast",
        "confidence": "High",
        "description": "Rice Blast is a fungal disease with diamond-shaped lesions on leaves.",
        "first_step_advice": "Remove and destroy infected leaves. Improve water drainage.",
        "detailed_plan": "For a detailed treatment plan, ask our Farming Advisor."
    }

# --- Page Function ---
def show_page():
    st.header("📸 Crop Disease Analyzer")
    st.write("Upload a crop leaf photo, and AI will identify diseases.")

    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Leaf Image", use_column_width=True)

        analysis_result = analyze_image_with_gemini(image)

        with col2:
            st.subheader("Analysis Result")
            st.success(f"**Disease Name:** {analysis_result['disease_name']}")
            st.warning(f"**Confidence:** {analysis_result['confidence']}")
            st.info(f"**Description:** {analysis_result['description']}")
            st.error(f"**Immediate Advice:** {analysis_result['first_step_advice']}")
            st.write("---")
            st.info(f"**Next Step:** {analysis_result['detailed_plan']}")
