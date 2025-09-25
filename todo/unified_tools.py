import os
import random
import chromadb
import wikipediaapi
import google.generativeai as genai
from googleapiclient.discovery import build

def query_knowledge_base(query: str) -> str:
    print("DEBUG: Attempting to query the knowledge base...")
    try:
        print("DEBUG: Connecting to ChromaDB at './agri_db'...")
        client = chromadb.PersistentClient(path="agri_db")
        collection = client.get_collection(name="kerala_agri_knowledge")
        print("DEBUG: Connection to ChromaDB successful.")

        print("DEBUG: Creating embedding for query using Gemini API...")
        query_embedding_result = genai.embed_content(
            model="models/embedding-001", content=query, task_type="retrieval_query"
        )
        print("DEBUG: Embedding created successfully.")

        results = collection.query(
            query_embeddings=[query_embedding_result['embedding']], n_results=2
        )
        print("DEBUG: Knowledge base query successful.")
        return "\n---\n".join(results['documents'][0])
    except Exception as e:
        print(f"!!! ERROR in query_knowledge_base: {e}")
        return f"Error accessing the local knowledge base: {e}"

def google_search(query: str) -> str:
    print("DEBUG: Attempting to perform Google search...")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        if not api_key or not search_engine_id:
            raise ValueError("GOOGLE_API_KEY or SEARCH_ENGINE_ID not found in .env")
        
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=search_engine_id, num=1).execute()
        print("DEBUG: Google search successful.")
        if 'items' not in res:
            return "No results found."
        item = res['items'][0]
        return f"Title: {item['title']}\nSnippet: {item['snippet']}"
    except Exception as e:
        print(f"!!! ERROR in google_search: {e}")
        return f"Error during Google search: {e}"

def get_weather(location: str) -> str:
    print(f"DEBUG: Getting simulated weather for {location}...")
    if "thiruvananthapuram" in location.lower():
        return "Forecast for Thiruvananthapuram: 29°C, humid, with a high chance of afternoon showers."
    else:
        return f"Forecast for {location.title()}: {random.randint(26, 32)}°C, partly cloudy."

# Wikipedia function is less likely to fail, so it's omitted for brevity