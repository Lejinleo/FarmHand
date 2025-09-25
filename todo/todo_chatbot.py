import os
import datetime
from mistralai.client import MistralClient
from dotenv import load_dotenv

# Import our knowledge base and NEW weather tool
from unified_tools import query_knowledge_base, get_weather, google_search

# --- 1. SETUP ---
print("DEBUG: Starting script setup...")
load_dotenv()
try:
    mistral_api_key = os.getenv("MISTRAL_API_KEY")
    if not mistral_api_key:
        raise ValueError("MISTRAL_API_KEY is missing from .env")
    
    client = MistralClient(api_key=mistral_api_key)
    model = "mistral-small-latest" 
    print(f"DEBUG: Mistral client initialized successfully with model: {model}")

except Exception as e:
    print(f"!!! ERROR during setup: {e}")
    exit()

# --- 2. THE SMART TO-DO LIST FUNCTION ---
def get_daily_todo_list() -> str:
    print("DEBUG: Inside get_daily_todo_list function...")
    current_month_name = datetime.date.today().strftime("%B")
    
    print("DEBUG: Step A1 - Gathering seasonal tasks from knowledge base...")
    kb_query = f"Key farming tasks in Kerala during {current_month_name} for rice and coconut."
    seasonal_tasks_info = query_knowledge_base(kb_query)
    
    print("DEBUG: Step A2 - Gathering live weather data...")
    weather_info = get_weather(location="Thiruvananthapuram")
    
    print("DEBUG: Step A3 - Gathering live price data...")
    price_info = google_search(query="current price of coconut in Thiruvananthapuram market")

    print("DEBUG: Step B - Synthesizing final notification with Mistral AI...")
    prompt = f"""
    You are an expert farm advisor... (prompt content is the same)
    
    **Seasonal Focus Information:**
    {seasonal_tasks_info}

    **Live Weather Data:**
    {weather_info}

    **Live Market Price Data:**
    {price_info}

    Generate the compact notification now.
    """
    
    messages = [{"role": "user", "content": prompt}]
    chat_response = client.chat(model=model, messages=messages)
    print("DEBUG: Synthesis successful.")
    
    return chat_response.choices[0].message.content

# --- 3. MAIN SCRIPT ---
def main():
    print("DEBUG: Starting main function...")
    print("\n--- Farmer's Smart Notification ---")
    
    daily_tasks = get_daily_todo_list()
    
    print("\n🔔 Here is your smart to-do list for today:")
    print("----------------------------------------")
    print(daily_tasks)
    print("----------------------------------------")

if __name__ == "__main__":
    main()