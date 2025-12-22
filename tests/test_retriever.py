import os

import pytest
from langchain_openai import OpenAIEmbeddings

from services.retriever import MultiNamespaceRetriever


pytestmark = pytest.mark.skipif(
    not os.getenv("PINECONE_API_KEY") or not os.getenv("OPENAI_API_KEY"),
    reason="Integration test requires Pinecone and OpenAI credentials",
)


def test_retriever_builds_vectorstores():
    embeddings = OpenAIEmbeddings()
    retriever = MultiNamespaceRetriever(["default"], embeddings)
    assert "default" in retriever.vectorstores

