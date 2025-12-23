from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import PlainTextResponse, StreamingResponse
from pydantic import BaseModel, model_validator
import uvicorn

from config.settings import settings
from services.rag_service import RAGService
from middleware.rate_limit import RateLimitMiddleware
from utils.logger import setup_logger

logger = setup_logger(__name__)
app = FastAPI(title="RAG API", version="1.0.0")

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_origin_regex=".*",
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Rate Limiting
app.add_middleware(RateLimitMiddleware)

# Initialize RAG Service
rag_service = RAGService(namespaces=["computer-networking-pdf", "networking-pdf"])


class QueryRequest(BaseModel):
    # Accept both "query" and "question" for compatibility with frontend
    query: str | None = None
    question: str | None = None
    namespace: str = "default"
    top_k: int = 5
    include_sources: bool = False
    as_text: bool = True  # default to plain-text responses for frontend

    @model_validator(mode="before")
    def fill_query(cls, values):
        if not values.get("query") and values.get("question"):
            values["query"] = values["question"]
        return values

    @model_validator(mode="after")
    def ensure_query(cls, values):
        if not values.query or not values.query.strip():
            raise ValueError("Field 'query' is required.")
        return values


class QueryResponse(BaseModel):
    answer: str
    sources: list | None = None
    namespace: str


@app.post("/query", response_model=QueryResponse)
async def query_rag(request: QueryRequest):
    try:
        result = await rag_service.query(
            query=request.query,
            namespace=request.namespace,
            top_k=request.top_k,
        )
        if not request.include_sources:
            result["sources"] = None
            # hide namespace when returning plain text
            result["namespace"] = None
        if request.as_text or not request.include_sources:
            return PlainTextResponse(result["answer"])
        return result
    except Exception as e:
        logger.error("Query error: %s", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# Streaming, chat-style
@app.post("/ask")
async def ask_stream(request: QueryRequest):
    async def token_generator():
        async for event in rag_service.query_stream(
            query=request.query,
            namespace=request.namespace,
            top_k=request.top_k,
        ):
            if event.get("type") == "token":
                yield event["content"]

    return StreamingResponse(token_generator(), media_type="text/plain")


@app.get("/health")
async def health_check():
    return {"status": "healthy"}


if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host=settings.HOST,
        port=settings.PORT,
        reload=settings.DEBUG,
    )

