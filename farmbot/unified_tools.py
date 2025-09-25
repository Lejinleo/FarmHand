import os
import chromadb
import wikipediaapi
import google.generativeai as genai
from googleapiclient.discovery import build

def query_knowledge_base(query: str) -> str:
    """
    Searches the local vector database for specific, trusted information about Kerala agriculture,
    including farming techniques, local schemes, and known pest data.
    Use this for questions about established local practices. For example: 'How do I prepare for the Mundakan season?'
    """
    print(f"--- [Searching internal knowledge base for: {query}] ---")
    try:
        client = chromadb.PersistentClient(path="agri_db")
        collection = client.get_collection(name="kerala_agri_knowledge")
        
        query_embedding_result = genai.embed_content(
            model="models/embedding-001",
            content=query,
            task_type="retrieval_query"
        )
        results = collection.query(
            query_embeddings=[query_embedding_result['embedding']],
            n_results=2
        )
        return "\n---\n".join(results['documents'][0])
    except Exception as e:
        return f"Error accessing the local knowledge base: {e}"

def google_search(query: str) -> str:
    """
    Performs a Google search for a given query.
    Use this for current events, news, market prices, and general information not found in the local knowledge base.
    For example: 'What is the latest news on rubber prices?'
    """
    print(f"--- [Performing Google Search for: {query}] ---")
    try:
        api_key = os.getenv("GOOGLE_API_KEY")
        search_engine_id = os.getenv("SEARCH_ENGINE_ID")
        service = build("customsearch", "v1", developerKey=api_key)
        res = service.cse().list(q=query, cx=search_engine_id, num=3).execute()
        
        if 'items' not in res:
            return "No results found."
        snippets = [f"Title: {item['title']}\nSnippet: {item['snippet']}" for item in res['items']]
        return "\n\n".join(snippets)
    except Exception as e:
        return f"Error during Google search: {e}"

def search_wikipedia(query: str) -> str:
    """
    Searches Wikipedia for a query.
    Use this for factual, historical, or encyclopedic information.
    For example: 'What is the scientific name for Black Pepper?'
    """
    print(f"--- [Searching Wikipedia for: {query}] ---")
    try:
        wiki_wiki = wikipediaapi.Wikipedia(language='en', user_agent='KeralaAgriBot/1.0')
        page = wiki_wiki.page(query)
        if not page.exists():
            return f"Wikipedia page for '{query}' not found."
        return ". ".join(page.summary.split('.')[0:3]) + "."
    except Exception as e:
        return f"Error during Wikipedia search: {e}"