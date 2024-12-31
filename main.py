import os
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# Pinecone
from pinecone import Pinecone

# OpenAI
from openai import OpenAI

from dotenv import load_dotenv
# ---------------------------------------------------------------------
# 1. Load environment variables
# ---------------------------------------------------------------------
load_dotenv(override=True)

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPEN_AI_KEY = os.getenv("OPEN_AI_KEY")
PINECONE_ENV = "us-east-1-aws"  # Adjust if needed
INDEX_NAME = "academic-papers"  # Example index name

if not PINECONE_API_KEY:
    raise ValueError("PINECONE_API_KEY not found in environment variables.")
if not OPEN_AI_KEY:
    raise ValueError("OPEN_AI_KEY not found in environment variables.")

# ---------------------------------------------------------------------
# 2. Initialize Pinecone and OpenAI
# ---------------------------------------------------------------------
openai_client = OpenAI(api_key=os.environ['OPEN_AI_KEY'])
pinecone_client = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))

# Ensure index exists
if not pinecone_client.has_index(INDEX_NAME):
    print("Pinecone Index not found.")

index = pinecone_client.Index(INDEX_NAME)

# ---------------------------------------------------------------------
# 3. FastAPI App
# ---------------------------------------------------------------------
app = FastAPI(title="Simple RAG API", version="1.0")

# ---------------------------------------------------------------------
# 4. Request/Response Models
# ---------------------------------------------------------------------
class QueryRequest(BaseModel):
    query: str

class QueryResponseModel(BaseModel):
    answer: str

# ---------------------------------------------------------------------
# 5. Utilities: Embedding & Prompt
# ---------------------------------------------------------------------
def get_embedding(text: str) -> list[float]:
    """Get embedding for a single text using pinecone's embedding endpoint."""
    response = pinecone_client.inference.embed(
        model="multilingual-e5-large",
        inputs=[text],
        parameters={
            "input_type": "query"
        }
    )
    return response[0].values

def build_prompt(query: str, contexts: list[dict]) -> str:
    """
    Build a prompt that includes top-3 (title, abstract) contexts and the user query.
    Returns a single string to send to the LLM.
    """
    # You can adapt this prompt template to your notebook's version:
    prompt_template = """
    You are an assistant helping a researcher find relevant academic papers.

    You have these top-3 relevant papers with titles and abstracts:
    1) Title: {title1}
       Abstract: {abstract1}
    2) Title: {title2}
       Abstract: {abstract2}
    3) Title: {title3}
       Abstract: {abstract3}

    The researcher asks: "{query}"

    Your tasks:
    - Analyze the abstracts and see how they relate to the research topic (the query).
    - Summarize the key similarities or differences to the topic.
    - If none are relevant, say "I didn't find any relevant information to this topic".

    If any are relevant, respond with this template:
    "I have found relevant information about your research topic in the following papers:
        - Title: ...
        - Similarities: ...
        - Differences: ...
    "
    """
    # Just fill in the placeholders with the 3 context items we have
    # If there are fewer than 3 matches, fill them with empty placeholders
    titles = []
    abstracts = []
    for i in range(3):
        if i < len(contexts):
            titles.append(contexts[i].get("title", ""))
            abstracts.append(contexts[i].get("abstract", ""))
        else:
            titles.append("")
            abstracts.append("")

    prompt = prompt_template.format(
        title1=titles[0],
        abstract1=abstracts[0],
        title2=titles[1],
        abstract2=abstracts[1],
        title3=titles[2],
        abstract3=abstracts[2],
        query=query,
    )
    return prompt.strip()

def query_pinecone(query: str, top_k: int = 3) -> list[dict]:
    """
    1) Embed the query
    2) Query Pinecone
    3) Return top-k metadata items (title, abstract, etc.)
    """
    # 1) Embed
    query_vector = get_embedding(query)

    # 2) Query the index
    response = index.query(
        vector=query_vector,
        top_k=top_k,
        include_values=False,
        include_metadata=True
    )

    # 3) Gather results
    results = []
    for match in response.matches:
        meta = match.metadata
        results.append({
            "title": meta.get("title", ""),
            "abstract": meta.get("abstract", ""),
            "score": match.score  # optionally keep track of similarity score
        })
    return results

# ---------------------------------------------------------------------
# 6. Chat Completion with OpenAI
# ---------------------------------------------------------------------
def get_llm_answer(prompt: str) -> str:
    """
    Uses an OpenAI ChatCompletion call with the provided prompt.
    Returns the LLM's final answer as a string.
    """
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt},
    ]

    try:
        completion = openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=messages,
            temperature=0.7, # Adjust temperature for more or less randomness
            max_tokens=800, # Adjust max tokens for longer or shorter answers
        )
        return completion.choices[0].message.content.strip()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"OpenAI API error: {str(e)}")

# ---------------------------------------------------------------------
# 7. Single Route: POST /query
# ---------------------------------------------------------------------
@app.post("/query")
def query_endpoint(payload: QueryRequest):
    """
    Receives a JSON payload with 'query', returns the final LLM answer.
    Example payload:
      { "query": "I'm researching active learning in NLP. What papers can help?" }
    """
    user_query = payload.query
    # Retrieve top-3 relevant contexts
    top_contexts = query_pinecone(user_query, top_k=3)

    # Build the prompt with these contexts
    prompt = build_prompt(user_query, top_contexts)

    # Get the final LLM answer
    answer = get_llm_answer(prompt)

    # Return it
    return QueryResponseModel(answer=answer)

# ---------------------------------------------------------------------
# 8. How to Run
# ---------------------------------------------------------------------
# 1) pip install -r requirements.txt
# 2) fastapi dev main.py
# 3) Send a POST request to localhost:8000/query with JSON:
#    {
#       "query": "I am doing a research about active learning in NLP ..."
#    }
