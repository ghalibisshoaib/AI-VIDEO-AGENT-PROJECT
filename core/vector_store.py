import os

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

CHROMA_DIR = "vector_db"
COLLECTION_NAME = "meeting_transcript"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"


def get_embeddings():
    """Create the local embedding model used by the vector store."""
    return HuggingFaceEmbeddings(
        model_name=EMBEDDING_MODEL,
        model_kwargs={"device": "cpu"},
    )


def build_vecotr_store(transcript: str) -> Chroma:
    """Split a transcript, embed it, and persist the resulting vector store."""
    print("Building vector store...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,
        chunk_overlap=50,
    )
    chunks = splitter.split_text(transcript)
    documents = [
        Document(page_content=chunk, metadata={"chunk_index": index})
        for index, chunk in enumerate(chunks)
    ]
    return Chroma.from_documents(
        documents=documents,
        embedding=get_embeddings(),
        collection_name=COLLECTION_NAME,
        persist_directory=CHROMA_DIR,
    )


def load_vector_store() -> Chroma:
    """Load the persisted transcript vector store."""
    return Chroma(
        collection_name=COLLECTION_NAME,
        embedding_function=get_embeddings(),
        persist_directory=CHROMA_DIR,
    )


def get_retriever(vector_store: Chroma, k: int = 4):
    """Create a similarity retriever from a vector store."""
    if k <= 0:
        raise ValueError("k must be greater than zero")
    return vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": k},
    )