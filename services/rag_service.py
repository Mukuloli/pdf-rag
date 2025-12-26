from typing import Dict, List, AsyncIterator
from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser

from config.settings import settings
from services.prompt_template import get_prompt
from services.retriever import MultiNamespaceRetriever
from utils.cache import SimpleCache


class RAGService:
    """Core RAG logic for answering questions."""

    def __init__(self, namespaces: List[str] | None = None):
        self.namespaces = namespaces or ["default"]
        self.embeddings = OpenAIEmbeddings(
            openai_api_key=settings.OPENAI_API_KEY,
            model=settings.EMBEDDING_MODEL,
            dimensions=settings.EMBEDDING_DIM,
        )
        self.retriever = MultiNamespaceRetriever(self.namespaces, self.embeddings)
        self.llm = ChatOpenAI(
            openai_api_key=settings.OPENAI_API_KEY,
            model=settings.LLM_MODEL,
            temperature=0.3,
            streaming=True,  # Enable streaming
        )
        self.prompt = get_prompt()
        self.parser = StrOutputParser()
        self.cache = SimpleCache(max_size=128, ttl_seconds=600)

    def _format_docs(self, docs: List) -> str:
        if not docs:
            return "No relevant information found."
        return "\n\n---\n\n".join(
            [
                f"[Source: {doc.metadata.get('source_namespace', 'unknown')}]\n{doc.page_content}"
                for doc in docs
            ]
        )

    async def query_stream(
        self, query: str, namespace: str = "default", top_k: int = 5
    ) -> AsyncIterator[Dict]:
        """Stream the answer token by token."""
        
        cache_key = f"{namespace}:{query.strip()}"
        cached = self.cache.get(cache_key)
        if cached:
            yield {"type": "sources", "sources": cached["sources"], "namespace": namespace}
            yield {"type": "token", "content": cached["answer"]}
            yield {"type": "complete"}
            return

        # Get documents
        docs = self.retriever.get_documents(query, namespace=namespace, top_k=top_k)
        
        # Prepare sources
        sources = [
            {
                "id": getattr(doc, "id", None),
                "namespace": doc.metadata.get("source_namespace", namespace),
                "metadata": doc.metadata,
            }
            for doc in docs
        ]
        
        # Yield sources first
        yield {"type": "sources", "sources": sources, "namespace": namespace}
        
        # Build chain
        chain = (
            {
                "context": lambda x: self._format_docs(docs),
                "question": lambda x: query,
            }
            | self.prompt
            | self.llm
            | self.parser
        )
        
        full_answer: List[str] = []

        # Stream the answer
        async for chunk in chain.astream({}):
            if chunk:  # Only yield non-empty chunks
                yield {"type": "token", "content": chunk}
                full_answer.append(chunk)
        
        # Yield completion signal
        yield {"type": "complete"}

        # Cache full answer
        self.cache.set(
            cache_key,
            {"answer": "".join(full_answer), "sources": sources},
        )

    async def query(self, query: str, namespace: str = "default", top_k: int = 5) -> Dict:
        """Non-streaming version for backward compatibility."""
        cache_key = f"{namespace}:{query.strip()}"
        cached = self.cache.get(cache_key)
        if cached:
            return {
                "answer": cached["answer"],
                "sources": cached["sources"],
                "namespace": namespace,
            }

        docs = self.retriever.get_documents(query, namespace=namespace, top_k=top_k)
        
        chain = (
            {
                "context": lambda x: self._format_docs(docs),
                "question": lambda x: query,
            }
            | self.prompt
            | self.llm
            | self.parser
        )
        
        # Collect all chunks
        answer = ""
        async for chunk in chain.astream({}):
            answer += chunk
        
        sources = [
            {
                "id": getattr(doc, "id", None),
                "namespace": doc.metadata.get("source_namespace", namespace),
                "metadata": doc.metadata,
            }
            for doc in docs
        ]
        
        # Cache answer
        self.cache.set(cache_key, {"answer": answer, "sources": sources})

        return {"answer": answer, "sources": sources, "namespace": namespace}

        docs = self.retriever.get_documents(query, namespace=namespace, top_k=top_k)
        
        chain = (
            {
                "context": lambda x: self._format_docs(docs),
                "question": lambda x: query,
            }
            | self.prompt
            | self.llm
            | self.parser
        )
        
        # Collect all chunks
        answer = ""
        async for chunk in chain.astream({}):
            answer += chunk
        
        sources = [
            {
                "id": getattr(doc, "id", None),
                "namespace": doc.metadata.get("source_namespace", namespace),
                "metadata": doc.metadata,
            }
            for doc in docs
        ]
        
        # Cache answer
        self.cache.set(cache_key, {"answer": answer, "sources": sources})

        return {"answer": answer, "sources": sources, "namespace": namespace}

        docs = self.retriever.get_documents(query, namespace=namespace, top_k=top_k)
        
        chain = (
            {
                "context": lambda x: self._format_docs(docs),
                "question": lambda x: query,
            }
            | self.prompt
            | self.llm
            | self.parser
        )
        
        # Collect all chunks
        answer = ""
        async for chunk in chain.astream({}):
            answer += chunk
        
        sources = [
            {
                "id": getattr(doc, "id", None),
                "namespace": doc.metadata.get("source_namespace", namespace),
                "metadata": doc.metadata,
            }
            for doc in docs
        ]
        
        # Cache answer
        self.cache.set(cache_key, {"answer": answer, "sources": sources})

        return {"answer": answer, "sources": sources, "namespace": namespace}