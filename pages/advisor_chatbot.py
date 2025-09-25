import streamlit as st
import time

# --- MOCK Chatbot Function ---
def get_gemini_chat_response(prompt, chat_history):
    with st.spinner("Thinking..."):
        time.sleep(2)
    if "rice leaf blast" in prompt.lower():
        return "For Rice Leaf Blast, use Tricyclazole fungicide or neem oil spray every 7-10 days."
    elif "hello" in prompt.lower():
        return "Hello! I am Kēraḷa Mitra, your AI farming assistant."
    else:
        return "I can help with Kerala crops like rice, banana, and coconut. Try asking about 'banana bunchy top virus'."

# --- Page Function ---
def show_page():
    st.header("💬 Farming Advisor Chatbot")
    st.write("Ask me about crop health, treatments, or government schemes.")

    if "messages" not in st.session_state:
        st.session_state.messages = []

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    if prompt := st.chat_input("What is your question?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        response = get_gemini_chat_response(prompt, st.session_state.messages)
        with st.chat_message("assistant"):
            st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})
