from fastapi import APIRouter
from pydantic import BaseModel

from services.openai import openai_service
from services.pinecone import pinecone_service
from services.prompting import build_prompt_for_initial_message, build_prompt_to_check_necessity_of_retrieving_documents, build_prompt_for_intermediate_message_with_new_docs, build_prompt_for_intermediate_message_without_new_docs, build_prompt_for_query_refinement

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
  refined_query = openai_service.get_chat_completion(build_prompt_for_query_refinement(user_context,user_query))
  query_vector = pinecone_service.get_embedding(refined_query)
  
  # 2.1) If it is the first query, fetch the top-3 documents from Pinecone sen the prompt without user_context
  if len(user_context) == 0:
    top_contexts = pinecone_service.get_similar_documents(query_vector, top_k=3)
    prompt = build_prompt_for_initial_message(user_query, top_contexts)
    print(prompt)
  else:
    # 2.2) If it is not the first query, check if it is necessary to retrieve new documents
    prompt = build_prompt_to_check_necessity_of_retrieving_documents(user_context, user_query)
    raw_answer = openai_service.get_chat_completion(prompt)
    answer_clean = raw_answer.strip().lower()
    if "true" in answer_clean:
        answer = "True"
    else:
        answer = "False"
    if answer == "True":
      # 2.2.1) If new documents are necessary, fetch the top-3 documents from Pinecone and send the prompt with user_context
      top_contexts = pinecone_service.get_similar_documents(query_vector, top_k=3)
      prompt = build_prompt_for_intermediate_message_with_new_docs(user_context, user_query, top_contexts)
    else:
      # 2.2.2) If new documents are not necessary, send the prompt with user_context
      prompt = build_prompt_for_intermediate_message_without_new_docs(user_context, user_query)
  
  # 3) Use OpenAI ChatCompletion to get final answer
  answer = openai_service.get_chat_completion(prompt)
  
  return QueryResponse(answer=answer)
