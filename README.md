# RAG API (Pinecone + OpenAI)

FastAPI-based Retrieval-Augmented Generation API with multi-namespace Pinecone search and no external cache/Redis dependencies.

## Project Layout
See `API_DOCS.md` and `DEPLOYMENT.md` for endpoint and deploy details.

```
rag-api/
├── main.py
├── config/
├── services/
├── middleware/
├── utils/
├── tests/
├── logs/
├── requirements.txt
├── Dockerfile
└── docker-compose.yml
```

## Quickstart
```bash
python -m venv venv
venv\Scripts\activate  # Windows
pip install -r requirements.txt
copy .env.example .env  # fill secrets
python main.py
```

### Docker
```bash
docker-compose up --build
```

### Tests
```bash
pytest tests/
```

