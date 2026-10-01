import os
from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from core.vector_store import build_vecotr_store, load_vector_store, get_retriever
from langchain_core.runnables import RunnableLambda, RunnablePassthrough

load_dotenv()


def get_llm():
    api_key = os.getenv("MISTRAL_API_KEY") or os.getenv("mistral_api_key")
    if not api_key:
        raise RuntimeError("MISTRAL_API_KEY is not set")
    return ChatMistralAI(
        model="mistral-small-latest",
        api_key=api_key,
        temperature=0.3,
    )


def format_docs(docs) -> str:
    return "\n\n".join(doc.page_content for doc in docs)


def build_rag_chain(transcript: str):
    vector_store = build_vecotr_store(transcript)
    retriever = get_retriever(vector_store, k=4)
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        (
            "system",
            "Answer using only this meeting transcript context. If the answer "
            "is not found, say you could not find it in the transcript.\n\n"
            "Context:\n{context}",
        ),
        ("human", "{question}"),
    ])
    return (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def load_rag_chain():
    vector_store = load_vector_store()
    retriever = get_retriever(vector_store)
    llm = get_llm()
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Answer only from this meeting context:\n{context}"),
        ("human", "{question}"),
    ])
    return (
        {
            "context": retriever | RunnableLambda(format_docs),
            "question": RunnablePassthrough(),
        }
        | prompt
        | llm
        | StrOutputParser()
    )


def ask_question(rag_chain, question: str) -> str:
    answer = rag_chain.invoke(question)
    print(f"Answer: {answer}")
    return answer

    