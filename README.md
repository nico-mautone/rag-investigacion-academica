# Academic Research Assistant (RAG Implementation)

An advanced academic research assistant leveraging Retrieval-Augmented Generation (RAG) to provide precise and context-aware answers for researchers. This project integrates OpenAI's language models with Pinecone's vector database to enhance academic queries.

## Project structure

- **`main.py`**: The main entry point of the FastAPI application.
  - Configures the server, sets up middleware for CORS, and includes routes for RAG queries.

- **`rag.py`**: Contains the core logic for processing user queries and retrieving relevant documents.

- **`openai.py`**: Manages interactions with the OpenAI API for generating responses.

- **`pinecone.py`**: Handles document retrieval using Pinecone's vector database.

- **`prompting.py`**: Builds tailored prompts for different stages of query processing.

- **`config.py`**: Loads and validates environment variables, including API keys for OpenAI and Pinecone.

- **`.env.public`**: Example environment file containing placeholders for API keys.

- **`requirements.txt`**: Lists all dependencies required for the project.

- **Notebooks**: 
  - `setting_up_pinecone_database.ipynb`: Guides the setup of Pinecone.
  - `rag_test.ipynb`: Demonstrates the testing of the RAG workflow.

## RAG flow

## API Reference

#### Query endpoint

```http
POST /query
```

| Parameter   | Type     | Description                                             |
| :---------- | :------- | :------------------------------------------------------|
| `query`     | `string` | **Required**. The research question or topic to query. |
| `context`   | `array`  | Optional. Previous conversation context for continuity. |

**Example Request:**
```json
{
  "query": "I’m doing research on reinforcement learning. Tell me which articles I should start with.",
  "context": []
}
```

**Example Response:**
```json
{
  "answer": "I found several articles that are related to your research on reinforcement learning...."
}
```

## Installation

To set up the project locally:

```bash
python -m venv venv
source venv/bin/activate # On Windows: venv\Scripts\activate
```
Then, go to the `rag-api` directory:

```bash
cd rag-api
pip install -r requirements.txt
```

## Deployment

To deploy this project locally:

```bash
fastapi dev main.py
```

