from typing import Dict, List

from langchain_openai import ChatOpenAI, OpenAIEmbeddings
from langchain_core.output_parsers import StrOutputParser

from config.settings import settings
from services.prompt_template import get_prompt
from services.retriever import MultiNamespaceRetriever


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
        )
        self.prompt = get_prompt()
        self.parser = StrOutputParser()

    def _format_docs(self, docs: List) -> str:
        if not docs:
            return "No relevant information found."
        return "\n\n---\n\n".join(
            [
                f"[Source: {doc.metadata.get('source_namespace', 'unknown')}]\n{doc.page_content}"
                for doc in docs
            ]
        )

    async def query(self, query: str, namespace: str = "default", top_k: int = 5) -> Dict:
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
        answer = await chain.ainvoke({})
        sources = [
            {
                "id": getattr(doc, "id", None),
                "namespace": doc.metadata.get("source_namespace", namespace),
                "metadata": doc.metadata,
            }
            for doc in docs
        ]
        return {"answer": answer, "sources": sources, "namespace": namespace}

