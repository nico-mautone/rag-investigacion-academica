from fastapi import APIRouter
from pydantic import BaseModel

from app.services.openai import openai_service
from app.services.pinecone import pinecone_service
from app.services.prompting import build_prompt

rag_router = APIRouter()

# Pydantic request/response models
class QueryRequest(BaseModel):
    query: str

class QueryResponse(BaseModel):
    answer: str

@rag_router.post("/", response_model=QueryResponse)
def rag_query(payload: QueryRequest):
    """
    Receives a JSON payload with 'query', returns the final LLM answer.
    Example:
      POST /query
      {
        "query": "I am doing research about active learning in NLP. Can you help?"
      }
    """
    user_query = payload.query

    # 1) Embed the user query using Pinecone
    query_vector = pinecone_service.get_embedding(user_query)
    
    # 2) Query Pinecone with this embedding
    top_contexts = pinecone_service.get_similar_documents(query_vector, top_k=3)
    
    # 3) Build the prompt
    prompt = build_prompt(user_query, top_contexts)
    
    # 4) Use OpenAI ChatCompletion to get final answer
    answer = openai_service.get_chat_completion(prompt)
    
    return QueryResponse(answer=answer)
