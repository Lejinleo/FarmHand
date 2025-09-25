import os
import chromadb
import google.generativeai as genai
from dotenv import load_dotenv

print("Starting the process to build the knowledge base...")

# --- SETUP ---
load_dotenv()
try:
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not found in .env file")
    genai.configure(api_key=api_key)
except Exception as e:
    print(f"Error configuring API: {e}")
    exit()

# --- DATA PREPARATION ---
DOCUMENTS_PATH = "knowledge_documents"
documents = []
for filename in os.listdir(DOCUMENTS_PATH):
    if filename.endswith(".txt"):
        filepath = os.path.join(DOCUMENTS_PATH, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            documents.append(f.read())
print(f"Found and read {len(documents)} documents.")

# --- DATABASE SETUP ---
client = chromadb.PersistentClient(path="agri_db")
collection_name = "kerala_agri_knowledge"
collection = client.get_or_create_collection(name=collection_name)
print(f"ChromaDB collection '{collection_name}' is ready.")

# --- EMBEDDING AND STORING ---
print("Embedding documents and storing them in the database...")
result = genai.embed_content(
    model="models/embedding-001",
    content=documents,
    task_type="retrieval_document"
)
collection.add(
    embeddings=result['embedding'],
    documents=documents,
    ids=[f"doc_{i}" for i in range(len(documents))]
)

print(f"\nSuccessfully built the database. The 'agri_db' folder is now ready.")