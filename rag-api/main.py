from fastapi import FastAPI
from routes.rag import rag_router
from fastapi.middleware.cors import CORSMiddleware

def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application instance.
    """
    app = FastAPI(title="Simple RAG API", version="1.0")

    # Include your RAG router (the query endpoint)
    app.include_router(rag_router, prefix="/query", tags=["RAG Queries"])
    
    # CORS settings, allow localhost:3000 for development
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://localhost:8080"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    return app

app = create_app()

# Run locally
# ---------------------------------------------------------------------
# 1) pip install -r requirements.txt
# 2) fastapi dev main.py
# 3) Send a POST request to localhost:8000/query with JSON:
#    {
#       "query": "I am doing a research about active learning in NLP ..."
#    }
