from fastapi import FastAPI
from app.routes.rag import rag_router

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    app = FastAPI(title="Simple RAG API", version="1.0")

    # Include your RAG router (the query endpoint)
    app.include_router(rag_router, prefix="/query", tags=["RAG Queries"])

    return app

app = create_app()

# Run locally: uvicorn main:app --reload
# ---------------------------------------------------------------------
# 1) pip install -r requirements.txt
# 2) fastapi dev main.py
# 3) Send a POST request to localhost:8000/query with JSON:
#    {
#       "query": "I am doing a research about active learning in NLP ..."
#    }
