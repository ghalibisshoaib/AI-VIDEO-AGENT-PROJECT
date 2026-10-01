import os
import sys
from pathlib import Path

from utils.audio_processor import process_input
from core.transcriber import transcribe_all
from core.summarize import generate_title, summarize
from core.extractor import extract_action_items


def main() -> None:
	source = sys.argv[1] if len(sys.argv) > 1 else os.getenv(
		"VIDEO_SOURCE",
		"https://www.youtube.com/watch?v=2dRvcgskIxY",
	)
	chunks = process_input(source, chunk_minutes=2)
	output_path = str(Path(__file__).with_name("transcript.txt"))
	transcript = transcribe_all(chunks, output_path=output_path)

	if not transcript:
		raise RuntimeError("No transcript was produced from the video")

	print("\n=== Full Transcription ===")
	print(transcript)

	try:
		meeting_summary = summarize(transcript)
	except Exception as error:
		meeting_summary = f"Summary unavailable: {error}"

	print("\n=== Summary Bullet Points ===")
	print(meeting_summary)

	try:
		title = generate_title(transcript)
	except Exception as error:
		title = "Meeting Transcript"
		print(f"\nTitle unavailable: {error}")

	print(f"\n=== {title} ===")

	try:
		action_items = extract_action_items(transcript)
	except Exception as error:
		action_items = f"Action items unavailable: {error}"

	print("\n=== Action Items ===")
	print(action_items)


if __name__ == "__main__":
	main()
