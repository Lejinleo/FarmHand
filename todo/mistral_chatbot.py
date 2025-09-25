import os
import json
from mistralai.client import MistralClient
from mistralai.models.chat_completion import ChatMessage
from dotenv import load_dotenv

# Import our existing tool functions
from unified_tools import query_knowledge_base, google_search, search_wikipedia

# --- 1. SETUP ---
load_dotenv()
try:
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_api_key:
        raise ValueError("MISTRAL_API_KEY is missing from .env")
    
    client = MistralClient(api_key=mistral_api_key)
    model = "mistral-small"
    print(f"Mistral client initialized using model: {model}")

except Exception as e:
    print(f"Error during setup: {e}")
    exit()

# --- 2. TOOL DEFINITION & MAPPING ---
tools = [
    {"type": "function", "function": {
        "name": "query_knowledge_base",
        "description": "Searches the local vector database for specific, trusted information about Kerala agriculture.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The user's question about Kerala farming."}}, "required": ["query"]},
    }},
    {"type": "function", "function": {
        "name": "google_search",
        "description": "Performs a Google search for current events, news, or general information.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The search query."}}, "required": ["query"]},
    }},
    {"type": "function", "function": {
        "name": "search_wikipedia",
        "description": "Searches Wikipedia for factual, historical, or encyclopedic information.",
        "parameters": {"type": "object", "properties": {"query": {"type": "string", "description": "The topic to search on Wikipedia."}}, "required": ["query"]},
    }}
]
tool_functions = {
    "query_knowledge_base": query_knowledge_base,
    "google_search": google_search,
    "search_wikipedia": search_wikipedia,
}

# --- 3. HANDLER FUNCTION ---
def handle_text_query(user_query: str, messages: list):
    """Handles text queries by letting the Mistral model choose the best tool."""
    print(f"\nThinking about your request...")
    messages.append(ChatMessage(role="user", content=user_query))
    
    chat_response = client.chat(model=model, messages=messages, tools=tools)
    response_message = chat_response.choices[0].message
    
    if response_message.tool_calls:
        tool_call = response_message.tool_calls[0]
        func_name = tool_call.function.name
        func_args = json.loads(tool_call.function.arguments)

        tool_result = tool_functions[func_name](**func_args)

        messages.append(response_message)
        messages.append(ChatMessage(role="tool", name=func_name, content=tool_result))

        # Second call to get the final answer from the tool result
        final_response = client.chat(model=model, messages=messages)
        final_answer = final_response.choices[0].message.content
    else:
        # The model answered directly
        final_answer = response_message.content

    messages.append(ChatMessage(role="assistant", content=final_answer))

    # The final formatting step for Malayalam is now removed.
    print("\n--- Agri-Bot Response ---")
    print(final_answer)

# --- 4. MAIN CHAT LOOP ---
def main():
    # MODIFIED: All user-facing text is now in English.
    print("\n--- Agri-Bot (Mistral Edition v0.4.2) ---")
    print("I can help with your farming questions.")
    print("Note: Photo analysis is not available in this version.")
    print("Type 'quit' to exit.")
    print("\nExample questions:")
    print(" -> 'How do I manage the Rhinoceros beetle pest?'")
    print(" -> 'Tell me about the farmer's welfare fund board scheme'")
    print("-----------------------------------------------------")

    # The system message sets the bot's persona. It's already in English.
    messages = [ChatMessage(role="system", content="You are an expert agricultural assistant for farmers in Kerala.")]

    while True:
        user_input = input("\nYou: ")
        if user_input.lower() == 'quit':
            print("Thank you!")
            break
        
        if "photo" in user_input.lower() or "analyze" in user_input.lower():
            print("\nSorry, this version of the chatbot cannot analyze images.")
        else:
            handle_text_query(user_input, messages)

if __name__ == "__main__":
    main()