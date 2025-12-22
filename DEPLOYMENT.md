# Deployment Guide

## Prerequisites
- Python 3.11+
- Pinecone index created with the namespaces you plan to search.
- OpenAI API key with access to the configured model.

## Environment
1) Copy `.env.example` to `.env` and set secrets.
2) Ensure `PINECONE_API_KEY`, `PINECONE_INDEX_NAME`, and `OPENAI_API_KEY` are set.

## Run Locally
```bash
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Docker
```bash
docker-compose up --build
```

## Production (examples)
- Gunicorn + Uvicorn workers:
```bash
pip install -r requirements.txt
gunicorn main:app -w 4 -k uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```
- Behind Nginx (see `nginx.conf`).

