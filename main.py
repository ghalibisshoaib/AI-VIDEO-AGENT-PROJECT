import argparse
import os
import re

from dotenv import load_dotenv

from core.extractor import (
    extract_action_items,
    extract_key_decisions,
    extract_questions,
)
from core.rag_enging import ask_question, build_rag_chain
from core.summarize import generate_title, summarize
from core.transcriber import transcribe_all
from utils.audio_processor import process_input

load_dotenv()


def _fallback_bullets(transcript: str, limit: int = 8) -> str:
    """Create basic local bullet points when the analysis API is unavailable."""
    sentences = [
        sentence.strip()
        for sentence in re.split(r"(?<=[.!?])\s+", transcript)
        if sentence.strip()
    ]
    if not sentences:
        return "- No summary could be created."
    return "\n".join(f"- {sentence}" for sentence in sentences[:limit])


def _fallback_title(transcript: str) -> str:
    """Return a local title when the title API is unavailable."""
    words = transcript.split()[:8]
    return " ".join(words).strip(".,!?;:") or "Meeting Transcript"


def run_pipeline(
    source: str,
    language: str | None = None,
    translate: bool = False,
    include_rag: bool = False,
    progress_callback=None,
) -> dict[str, object]:
    """Process a local file or URL and return the meeting results."""
    print("Starting AI video assistant")
    if progress_callback:
        progress_callback("Preparing audio source", 10)
    chunks = process_input(source, chunk_minutes=2)
    transcript_path = os.path.join(os.path.dirname(__file__), "transcript.txt")
    transcript = transcribe_all(
        chunks,
        language=language,
        translate=translate,
        output_path=transcript_path,
    )
    if progress_callback:
        progress_callback("Transcription complete", 60)
    if not transcript:
        raise RuntimeError("No transcript was produced from the input")

    print("\n=== Full Transcription ===")
    print(transcript)
    results: dict[str, object] = {"transcript": transcript}

    errors: list[str] = []
    try:
        if progress_callback:
            progress_callback("Generating summary", 70)
        results["summary"] = summarize(transcript)
    except Exception as error:
        results["summary"] = _fallback_bullets(transcript)
        errors.append("Summary used local fallback because the Mistral API limit was reached.")
    try:
        results["title"] = generate_title(transcript)
    except Exception as error:
        results["title"] = _fallback_title(transcript)
        errors.append("Title used local fallback because the Mistral API limit was reached.")
    for key, function, fallback in (
        ("action_items", extract_action_items, "No action items found."),
        ("key_decisions", extract_key_decisions, _fallback_bullets(transcript, 5)),
        ("open_questions", extract_questions, "No open questions found."),
    ):
        try:
            results[key] = function(transcript)
        except Exception as error:
            results[key] = fallback
            errors.append(
                f"{key.replace('_', ' ').capitalize()} used local fallback."
            )

    if include_rag:
        if progress_callback:
            progress_callback("Building question-answer index", 90)
        results["rag_chain"] = build_rag_chain(transcript)

    for key, heading in (
        ("title", "Title"),
        ("summary", "Summary Bullet Points"),
        ("action_items", "Action Items"),
        ("key_decisions", "Key Decisions"),
        ("open_questions", "Open Questions"),
    ):
        if key in results:
            print(f"\n=== {heading} ===")
            print(results[key])
    if errors:
        print("\nSome AI analysis was unavailable:")
        for message in dict.fromkeys(errors):
            print(f"- {message}")
    print(f"\nTranscript saved to: {transcript_path}")
    return results


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Transcribe and analyze a local audio/video file or URL"
    )
    parser.add_argument("source", nargs="?", default=os.getenv("VIDEO_SOURCE"))
    parser.add_argument(
        "--language",
        help="Spoken language, such as en, Spanish, or French",
    )
    parser.add_argument(
        "--translate",
        action="store_true",
        help="Translate the spoken language to English",
    )
    parser.add_argument(
        "--enable-rag",
        action="store_true",
        help="Build the optional question-answering vector store",
    )
    parser.add_argument("--question", help="Ask a question when RAG is enabled")
    args = parser.parse_args()
    source = args.source or "https://www.youtube.com/watch?v=2dRvcgskIxY"
    results = run_pipeline(
        source,
        language=args.language,
        translate=args.translate,
        include_rag=args.enable_rag,
    )
    if args.question:
        if "rag_chain" not in results:
            raise ValueError("Use --enable-rag before asking a question")
        ask_question(results["rag_chain"], args.question)


if __name__ == "__main__":
    main()
