from typing import Dict, List, Optional

from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec

from config.settings import settings


class MultiNamespaceRetriever:
    """Wrapper to search across one or multiple Pinecone namespaces."""

    def __init__(
        self,
        namespaces: List[str],
        embeddings,
    ):
        pc = Pinecone(api_key=settings.PINECONE_API_KEY)
        self.index = pc.Index(settings.PINECONE_INDEX_NAME)
        self.vectorstores: Dict[str, PineconeVectorStore] = {
            ns: PineconeVectorStore(
                index=self.index,
                embedding=embeddings,
                namespace=ns,
            )
            for ns in namespaces
        }

    def get_documents(
        self, query: str, namespace: Optional[str] = None, top_k: int = 5
    ) -> List:
        # If a namespace is provided, search only there when available.
        if namespace and namespace in self.vectorstores:
            return self.vectorstores[namespace].similarity_search(query, k=top_k)

        # Otherwise search across all configured namespaces.
        results: List = []
        for ns, store in self.vectorstores.items():
            docs = store.similarity_search(query, k=top_k)
            for doc in docs:
                doc.metadata["source_namespace"] = ns
            results.extend(docs)
        return results

