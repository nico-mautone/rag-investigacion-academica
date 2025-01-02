# rag-investigacion-academica

## Run Frontend

First, go to the `frontend/academic-chatbot` directory:

```bash
cd frontend/academnic-chatbot
```

### Install dependencies

```bash
npm install
```

### Run the project

```bash
npm run dev
```

## Run Backend

First, go to the `rag-api` directory:

```bash
cd rag-api
```

### Install dependencies

```bash
pip install -r requirements.txt
```

### Add environment variables

Create a `.env` file in the root of the `rag-api` folder with the following content:

```bash
PINECONE_API_KEY=...
OPEN_AI_KEY=...
```

### Run the project

```bash
fastapi dev main.py
```