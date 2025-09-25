import streamlit as st
import time

# --- MOCK Chatbot Function (Replace with your actual Gemini API call) ---
def get_gemini_chat_response(prompt, chat_history):
    """
    This is a MOCK function.
    In your real app, this function will send the user's prompt
    and the chat history to the Gemini Text API.
    """
    with st.spinner("Thinking..."):
        time.sleep(2)
    if "rice leaf blast" in prompt.lower():
        return "Of course. For Rice Leaf Blast, you can use a fungicide containing Tricyclazole. For an organic approach, a spray made from neem oil can be effective. Apply every 7-10 days. Would you like to know about government subsidies for fungicides?"
    elif "hello" in prompt.lower():
        return "Hello! I am Kēraḷa Mitra, your AI farming assistant. How can I help you today? You can ask me about crop diseases, treatment plans, or government schemes."
    else:
        return "I can help with questions about common Kerala crops like rice, banana, and coconut. For example, you can ask me: 'What is the best way to treat banana bunchy top virus?'"

# --- Page Layout ---
st.header("💬 Farming Advisor Chatbot")
st.write("Ask me about crop health, treatments, or government schemes.")

# Initialize chat history in session state if it doesn't exist
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display past messages from history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Accept user input
if prompt := st.chat_input("What is your question?"):
    # Add user message to chat history and display it
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Get and display the assistant's response
    with st.chat_message("assistant"):
        response = get_gemini_chat_response(prompt, st.session_state.messages)
        st.markdown(response)

    # Add assistant's response to chat history
    st.session_state.messages.append({"role": "assistant", "content": response})
