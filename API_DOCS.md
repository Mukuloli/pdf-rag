# API Documentation

## Endpoints
- `POST /query` — run a RAG query.
- `GET /health` — health probe.

## Request/Response
`POST /query`
```json
{
  "query": "What is binary search?",
  "namespace": "default",
  "top_k": 5
}
```

Response:
```json
{
  "answer": "...",
  "sources": [
    {"id": "doc-id", "namespace": "networking-pdf", "metadata": {...}}
  ],
  "namespace": "default"
}
```

## Notes
- Set `namespace` to a specific namespace to scope search; omit to search all configured namespaces.
- Rate limiting is in-memory; tune `RATE_LIMIT_REQUESTS` and `RATE_LIMIT_WINDOW` in `.env`.

