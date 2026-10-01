import os
import time

from dotenv import load_dotenv
from langchain_mistralai import ChatMistralAI
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_text_splitters import RecursiveCharacterTextSplitter

load_dotenv()


def get_llm():
   """Create the configured Mistral chat model."""
   api_key = os.getenv("MISTRAL_API_KEY") or os.getenv("mistral_api_key")
   if not api_key:
      raise RuntimeError("MISTRAL_API_KEY is not set")
   return ChatMistralAI(
      model="mistral-small-latest",
      api_key=api_key,
      temperature=0.3,
      max_retries=3,
   )


def _invoke_with_retry(chain, values: dict[str, str]) -> str:
   """Retry temporary failures, but do not repeat an exhausted quota request."""
   for attempt in range(3):
      try:
         return chain.invoke(values)
      except Exception as error:
         if "429" in str(error):
            raise RuntimeError(
               "Mistral API rate limit reached. Local fallback used."
            ) from error
         if attempt == 2:
            raise
         time.sleep(10 * (attempt + 1))
   raise RuntimeError("The Mistral request could not be completed")


def split_transcript(transcript: str) -> list[str]:
   """Split a transcript into overlapping chunks for summarization."""
   splitter = RecursiveCharacterTextSplitter(
      chunk_size=3000,
      chunk_overlap=200,
   )
   return splitter.split_text(transcript)


def summarize(transcript: str) -> str:
   """Return a concise, professional summary of a meeting transcript."""
   llm = get_llm()
   prompt = ChatPromptTemplate.from_messages([
      (
         "system",
         "Summarize this meeting transcript using concise professional "
         "bullet points. Include decisions, important topics, and next steps.",
      ),
      ("human", "{text}"),
   ])
   chain = prompt | llm | StrOutputParser()
   return _invoke_with_retry(chain, {"text": transcript})


def generate_title(transcript: str) -> str:
   """Generate a short professional title from a meeting transcript."""
   title_prompt = ChatPromptTemplate.from_messages([
      (
         "system",
         "Based on the meeting transcript, generate a short professional "
         "meeting title (maximum 8 words). Return only the title.",
      ),
      ("human", "{text}"),
   ])
   title_chain = title_prompt | get_llm() | StrOutputParser()
   return _invoke_with_retry(title_chain, {"text": transcript[:2000]}).strip()
