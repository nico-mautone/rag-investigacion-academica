import os
from dotenv import load_dotenv

load_dotenv(override=True) # Load environment variables

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
INDEX_NAME = "academic-papers" # Adjust if needed

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in environment variables.")
if not OPEN_AI_KEY:
    raise ValueError("OPEN_AI_KEY not found in environment variables.")
