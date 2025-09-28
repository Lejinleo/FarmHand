# agri_bot.py

import os
import json
import time
from typing import List
import streamlit as st
from dotenv import load_dotenv

from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage

from unified_tools import query_knowledge_base, google_search, search_wikipedia

# ---------------------------
# Helper & Agent Logic (unchanged)
# ---------------------------

TOOLS = [
    {
        "type": "function",
        "function": {
            "name": "query_knowledge_base",
            "description": "Searches the local vector database for specific, trusted information about Kerala agriculture.",
            "parameters": {
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "The user's question about Kerala farming."
                    }
                },
                "required": ["query"],
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "google_search",
            "description": "Performs a Google search for current events, news, or general information.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            },
        },
    },
    {
        "type": "function",
        "function": {
            "name": "search_wikipedia",
            "description": "Searches Wikipedia for factual, historical, or encyclopedic information.",
            "parameters": {
                "type": "object",
                "properties": {"query": {"type": "string"}},
                "required": ["query"]
            },
        },
    },
]

TOOL_FUNCTIONS = {
    "query_knowledge_base": query_knowledge_base,
    "google_search": google_search,
    "search_wikipedia": search_wikipedia,
}


def init_client() -> MistralClient:
    load_dotenv()
    api_key = os.getenv("MISTRAL_API_KEY")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY not found in .env")
    return MistralClient(api_key=api_key)


def agent_respond(client: MistralClient, model: str, user_query: str, messages: List[ChatMessage]) -> str:
    messages.append(ChatMessage(role="user", content=user_query))
    try:
        chat_response = client.chat(model=model, messages=messages, tools=TOOLS)
    except Exception as e:
        return f"(Error) Failed to contact model: {e}"

    response_message = chat_response.choices[0].message

    if getattr(response_message, "tool_calls", None):
        tool_call = response_message.tool_calls[0]
        func_name = tool_call.function.name
        try:
            func_args = json.loads(tool_call.function.arguments)
        except Exception:
            func_args = {}

        try:
            tool_result = TOOL_FUNCTIONS[func_name](**func_args)
        except Exception as e:
            tool_result = f"(Error executing tool {func_name}: {e})"

        messages.append(response_message)
        messages.append(ChatMessage(role="tool", name=func_name, content=str(tool_result)))

        try:
            final_response = client.chat(model=model, messages=messages)
            final_answer = final_response.choices[0].message.content
        except Exception as e:
            final_answer = f"(Error) Failed to get final model response: {e}"
    else:
        final_answer = response_message.content

    messages.append(ChatMessage(role="assistant", content=final_answer))
    return final_answer

# ---------------------------
# STREAMLIT PAGE WRAPPED LIKE `show_page()`
# ---------------------------

def show_page():
    st.header("🌾 Kerala Agri-Bot — Chat Assistant")

    if "messages" not in st.session_state:
        st.session_state.messages = [ChatMessage(role="system", content="You are an expert agricultural assistant for farmers in Kerala.")]
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []

    # CSS for chat bubbles (original colors)
    st.markdown("""
        <style>
        .chat-bubble-user {
            background-color: #014225;  /* user bubble color */
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 75%;
            float: right;
            clear: both;
        }
        .chat-bubble-bot {
            background-color: #014225;  /* bot bubble color */
            padding: 10px 15px;
            border-radius: 10px;
            margin: 5px 0;
            max-width: 75%;
            float: left;
            clear: both;
        }
        </style>
    """, unsafe_allow_html=True)

    # Chat container
    chat_container = st.container()
    with chat_container:
        for speaker, text in st.session_state.chat_history:
            if speaker == "You":
                st.markdown(f"<div class='chat-bubble-user'>{text}</div>", unsafe_allow_html=True)
            else:
                st.markdown(f"<div class='chat-bubble-bot'>{text}</div>", unsafe_allow_html=True)

    # Input form
    with st.form(key="user_input_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type your question here:", key="chat_input")
        submitted = st.form_submit_button("Send")

    if submitted and user_input:
        try:
            client = init_client()
            with st.spinner("Agri-Bot is thinking..."):
                answer = agent_respond(client, "mistral-small", user_input, st.session_state.messages)

            # Append new messages
            st.session_state.chat_history.append(("You", user_input))
            st.session_state.chat_history.append(("Agri-Bot", answer))

            # Streamlit auto-refreshes the container automatically
        except Exception as e:
            st.error(f"Error: {e}")

    # Auto-scroll to latest message
    st.markdown("""
        <script>
            const chatDiv = document.querySelector('.main');
            if(chatDiv) { chatDiv.scrollTop = chatDiv.scrollHeight; }
        </script>
    """, unsafe_allow_html=True)
