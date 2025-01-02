from fastapi import APIRouter
from pydantic import BaseModel

from services.openai import openai_service
from services.pinecone import pinecone_service
from services.prompting import build_prompt

rag_router = APIRouter()

class QueryRequest(BaseModel):
  query: str
  context: list[dict]


class QueryResponse(BaseModel):
    answer: str

@rag_router.post("/", response_model=QueryResponse)
def rag_query(payload: QueryRequest):
  """
  Receives a JSON payload with 'query' and 'context'.
  First, embed the user query using Pinecone, in order to find similar documents in the documents index.
  Then, build a prompt that includes the user query, the top-3 relevant documents to the query, and the user context.
  Finally, use OpenAI ChatCompletion to generate a response to the user query.
  
  Example:
    POST /query
    {
    "query": "I am doing research about active learning in NLP. Can you help?",
    "context": "Some additional context here"
    }
  """
  user_query = payload.query
  user_context = payload.context

  # 1) Embed the user query using Pinecone
  query_vector = pinecone_service.get_embedding(user_query)
  
  # 2) Query Pinecone with this embedding
  top_contexts = pinecone_service.get_similar_documents(query_vector, top_k=3)
  
  # 3) Build the prompt
  prompt = build_prompt(user_query, top_contexts, user_context)
  
  # 4) Use OpenAI ChatCompletion to get final answer
  answer = openai_service.get_chat_completion(prompt)
  
  return QueryResponse(answer=answer)
