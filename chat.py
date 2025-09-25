import streamlit as st
from PIL import Image
import time

# --- Page Configuration ---
# This must be the first Streamlit command in your script.
st.set_page_config(
    page_title="Kerala Farming Assistant",
    page_icon="🌿",
    layout="wide",
    initial_sidebar_state="expanded",
)

# --- Custom CSS for Styling ---
# This function injects custom CSS to style the app.
def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# You would create a style.css file for more complex styling,
# but for a hackathon, embedding it directly is faster.
st.markdown("""
<style>
    /* Main title style */
    .title {
        font-size: 3rem;
        font-weight: bold;
        color: #2E7D32; /* A nice green color */
        text-align: center;
        padding: 20px;
    }
    /* Style for the sidebar */
    .st-emotion-cache-16txtl3 {
        background-color: #E8F5E9; /* Light green background */
    }
</style>
""", unsafe_allow_html=True)


# --- MOCK API FUNCTIONS (Replace with your actual Gemini API calls) ---

def analyze_image_with_gemini(uploaded_image):
    """
    This is a MOCK function.
    In your real app, this function will take the image,
    send it to the Gemini Vision API, and return the response.
    """
    # Show a spinner while "processing"
    with st.spinner('Analyzing the crop leaf... Please wait.'):
        time.sleep(3) # Simulate network latency

    # For demonstration, we return a hardcoded detailed response.
    # Your Gemini prompt should ask for a response in a similar structured format.
    mock_response = {
        "disease_name": "Rice Leaf Blast",
        "confidence": "High",
        "description": "Rice Blast is a common fungal disease that affects all parts of the rice plant. It appears as diamond-shaped lesions with a grayish center on the leaves.",
        "first_step_advice": "Immediately remove and destroy infected leaves to prevent further spread. Ensure proper water drainage in the affected area.",
        "detailed_plan": "For a detailed treatment plan, ask our Farming Advisor about 'Rice Leaf Blast treatment'."
    }
    return mock_response

def get_gemini_chat_response(prompt, chat_history):
    """
    This is a MOCK function.
    In your real app, this function will send the user's prompt
    and the chat history to the Gemini Text API.
    """
    with st.spinner('Thinking...'):
        time.sleep(2)

    # Simple rule-based mock responses for demonstration.
    if "rice leaf blast" in prompt.lower():
        return "Of course. For Rice Leaf Blast, you can use a fungicide containing Tricyclazole. For an organic approach, a spray made from neem oil can be effective. Apply every 7-10 days. Would you like to know about government subsidies for fungicides?"
    elif "hello" in prompt.lower():
        return "Hello! I am Kēraḷa Mitra, your AI farming assistant. How can I help you today? You can ask me about crop diseases, treatment plans, or government schemes."
    else:
        return "I can help with questions about common Kerala crops like rice, banana, and coconut. For example, you can ask me: 'What is the best way to treat banana bunchy top virus?'"


# --- APP LAYOUT ---

# Sidebar for navigation
with st.sidebar:
    st.header("Navigation")
    page = st.radio("Choose a feature", ["Crop Disease Analyzer", "Farming Advisor Chatbot", "Price Prediction"])

# Main title
st.markdown('<p class="title">🌿 Kerala AI Farming Assistant 🌿</p>', unsafe_allow_html=True)


# --- Page 1: Crop Disease Analyzer ---

if page == "Crop Disease Analyzer":
    st.header("📸 Crop Disease Analyzer")
    st.write("Upload a photo of a crop leaf, and our AI will identify any diseases and provide initial advice.")

    # File uploader widget
    uploaded_file = st.file_uploader("Choose an image of a leaf...", type=["jpg", "jpeg", "png"])

    if uploaded_file is not None:
        # Display the uploaded image
        image = Image.open(uploaded_file)
        
        col1, col2 = st.columns(2)
        with col1:
            st.image(image, caption='Uploaded Leaf Image.', use_column_width=True)

        # Call the mock API function to "analyze" the image
        analysis_result = analyze_image_with_gemini(image)

        # Display the analysis result
        with col2:
            st.subheader("Analysis Result")
            st.success(f"**Disease Name:** {analysis_result['disease_name']}")
            st.warning(f"**Confidence:** {analysis_result['confidence']}")
            st.info(f"**Description:** {analysis_result['description']}")
            st.error(f"**Immediate Advice:** {analysis_result['first_step_advice']}")
            st.write("---")
            st.info(f"**Next Step:** {analysis_result['detailed_plan']}")


# --- Page 2: Farming Advisor Chatbot ---

if page == "Farming Advisor Chatbot":
    st.header("💬 Farming Advisor Chatbot")
    st.write("Ask me anything about crop health, treatment plans, or government schemes for farmers in Kerala.")

    # Initialize chat history in session state if it doesn't exist
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display past messages
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Chat input for the user
    if prompt := st.chat_input("What is your question?"):
        # Add user message to chat history and display it
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        # Get and display the assistant's response
        with st.chat_message("assistant"):
            # Call the mock chat function
            response = get_gemini_chat_response(prompt, st.session_state.messages)
            st.markdown(response)
        
        # Add assistant's response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
