import os
from importlib import import_module
from typing import Any


WHISPER_MODEL = os.getenv("WHISPER_MODEL", "small").strip().lower()
_model: Any | None = None


def load_model() -> Any:
    """Load and cache the configured Whisper model."""
    global _model

    if _model is None:
        try:
            whisper = import_module("whisper")
        except ImportError as error:
            raise RuntimeError(
                "Whisper is not installed. Install openai-whisper before transcribing."
            ) from error

        print(f"Loading Whisper model: {WHISPER_MODEL}")
        _model = whisper.load_model(WHISPER_MODEL)
        print("Whisper model loaded successfully.")
    return _model


def transcribe_chunk(
    chunk_path: str,
    translate: bool = False,
    language: str | None = None,
) -> str:
    """Transcribe one audio chunk, optionally translating it to English."""
    model = load_model()
    task = "translate" if translate else "transcribe"
    device = getattr(model, "device", "cpu")
    device_type = getattr(device, "type", str(device))
    result = model.transcribe(
        chunk_path,
        task=task,
        language=language,
        fp16=device_type != "cpu",
        beam_size=1,
        best_of=1,
        temperature=0,
        condition_on_previous_text=False,
        verbose=True,
    )
    return result["text"].strip()


def transcribe_all(
    chunks: list[str],
    translate: bool = False,
    language: str | None = None,
    output_path: str = "transcript.txt",
) -> str:
    """Transcribe all audio chunks and save each completed chunk."""
    transcript_parts = []
    for index, chunk_path in enumerate(chunks, start=1):
        print(f"Transcribing chunk {index}/{len(chunks)}...", flush=True)
        chunk_transcript = transcribe_chunk(
            chunk_path,
            translate=translate,
            language=language,
        )
        transcript_parts.append(chunk_transcript)
        print(f"\n--- Transcription for chunk {index}/{len(chunks)} ---", flush=True)
        print(chunk_transcript or "[No speech detected]", flush=True)
        print("--- End chunk transcription ---\n", flush=True)
        partial_transcript = "\n\n".join(transcript_parts).strip()
        with open(output_path, "w", encoding="utf-8") as transcript_file:
            transcript_file.write(partial_transcript + "\n")
        print(
            f"Chunk {index}/{len(chunks)} complete. "
            f"Saved to {output_path}",
            flush=True,
        )

    full_transcript = " ".join(transcript_parts).strip()
    print("Transcription completed.")
    return full_transcript
