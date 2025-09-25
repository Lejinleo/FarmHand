import streamlit as st
from PIL import Image
import torch
from transformers import AutoImageProcessor, AutoModelForImageClassification

# --- Load Model and Processor from Hugging Face Hub ---
@st.cache_resource
def load_model_and_processor():
    """
    Loads the model and processor from the Hugging Face Hub.
    Using st.cache_resource ensures this is done only once.
    """
    try:
        processor = AutoImageProcessor.from_pretrained("wambugu71/crop_leaf_diseases_vit")
        model = AutoModelForImageClassification.from_pretrained("wambugu71/crop_leaf_diseases_vit")
        return processor, model
    except Exception as e:
        st.error(f"Error loading model from Hugging Face Hub: {e}")
        return None, None

# --- Image Analysis Function ---
def analyze_image_with_model(uploaded_image, processor, model):
    """
    Analyzes an uploaded image using the loaded model.
    """
    if not all([processor, model]):
        return {"error": "Model could not be loaded."}

    with st.spinner('Analyzing the crop leaf... Please wait.'):
        # Ensure image is in RGB format
        image = uploaded_image.convert("RGB")
        
        # Preprocess the image for the model
        inputs = processor(images=image, return_tensors="pt")

        # Make a prediction
        with torch.no_grad():
            outputs = model(**inputs)
            logits = outputs.logits
            
        # Get predicted class index and confidence score
        predicted_class_idx = logits.argmax(-1).item()
        probabilities = torch.nn.functional.softmax(logits, dim=1)[0]
        confidence_score = probabilities[predicted_class_idx].item()
        
        # Get the predicted label from the model's config
        predicted_label = model.config.id2label[predicted_class_idx]
        
        # --- You can add logic here to provide advice based on the disease name ---
        advice = {
            "Rice Blast": "Remove and destroy infected leaves. Improve water drainage. Consult a local farming advisor.",
            "Rice Sheath Blight": "Reduce nitrogen fertilizer. Use a fungicide if necessary. Ensure proper plant spacing.",
            "Rice Brown Spot": "Improve soil fertility, especially with potassium. Use a recommended fungicide.",
            # Add more diseases and their advice as needed
        }
        
        return {
            "disease_name": predicted_label,
            "confidence": f"{confidence_score * 100:.2f}%",
            "first_step_advice": advice.get(predicted_label, "No specific advice available. Consult an expert."),
            "description": f"The model has identified a high probability of **{predicted_label}**."
        }

# --- Streamlit App UI ---
def show_page():
    st.title("🌾 Crop Disease Analyzer")
    st.write("Upload a photo of a crop leaf, and our AI will identify potential diseases and provide immediate advice.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose a leaf image...", type=["jpg", "jpeg", "png"])

    # Load model and processor only once
    processor, model = load_model_and_processor()

    if uploaded_file is not None:
        # Open the image using PIL
        image = Image.open(uploaded_file)
        
        # Display the uploaded image and analysis result in two columns
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption="Uploaded Leaf Image", use_column_width=True)
            
        # Perform analysis on the uploaded image
        analysis_result = analyze_image_with_model(image, processor, model)

        with col2:
            st.subheader("Analysis Result")
            if "error" in analysis_result:
                st.error(analysis_result["error"])
            else:
                st.success(f"**Disease Detected:** {analysis_result['disease_name']}")
                st.info(f"**Confidence:** {analysis_result['confidence']}")
                st.warning(f"**First Step Advice:** {analysis_result['first_step_advice']}")
                st.markdown("---")
                st.info(f"**Description:** {analysis_result['description']}")

if __name__ == "__main__":
    show_page()
