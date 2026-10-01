import os
import time

from dotenv import load_dotenv
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_mistralai import ChatMistralAI

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


def build_chain(system_prompt: str):
   """Build a text-in, text-out chain using the supplied system prompt."""
   prompt = ChatPromptTemplate.from_messages([
      ("system", system_prompt),
      ("human", "{text}"),
   ])
   return prompt | get_llm() | StrOutputParser()


def extract_action_items(transcript: str) -> str:
   """Extract tasks and deadlines from a meeting transcript."""
   chain = build_chain(
      "You are an expert meeting analyst. From the meeting transcript, "
      "extract all action items. For each provide:\n"
      "- task description\n"
      "- deadline (if mentioned, otherwise write 'not specified')\n\n"
      "Format the result as a numbered list. If none are found, say "
      "'No action items.'"
   )
   return _invoke_with_retry(chain, {"text": transcript}).strip()

def extract_key_decisions(transcript: str) -> str:
   """Extract decisions made during the meeting."""
   chain = build_chain(
      "Extract the key decisions made in this meeting transcript. "
      "Format them as concise bullet points. If none were made, say "
      "'No key decisions found.'"
   )
   return _invoke_with_retry(chain, {"text": transcript}).strip()

def extract_questions(transcript: str) -> str:
   """Extract unresolved questions from the meeting transcript."""
   chain = build_chain(
      "Extract unresolved or open questions from this meeting transcript. "
      "Format them as concise bullet points. If none were found, say "
      "'No open questions found.'"
   )
   return _invoke_with_retry(chain, {"text": transcript}).strip()

def ectraction(transcript: str) -> str:
   """Backward-compatible alias for action-item extraction."""
   return extract_action_items(transcript)
