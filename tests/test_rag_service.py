import os

import pytest

from services.rag_service import RAGService


pytestmark = pytest.mark.skipif(
    not os.getenv("PINECONE_API_KEY") or not os.getenv("OPENAI_API_KEY"),
    reason="Integration test requires Pinecone/OpenAI credentials",
)


def test_rag_service_initialization():
    service = RAGService(namespaces=["default"])
    assert service.namespaces == ["default"]
    assert service.embeddings is not None

