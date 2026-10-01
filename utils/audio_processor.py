import os

import certifi
import yt_dlp
from pydub import AudioSegment


PROJECT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DOWNLOAD_DIR = os.path.join(PROJECT_DIR, "downloads")
os.makedirs(DOWNLOAD_DIR, exist_ok=True)


def download_youtube_audio(url: str) -> str:
    output_path = os.path.join(DOWNLOAD_DIR, "%(title)s.%(ext)s")
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": output_path,
        "noplaylist": True,
        "nopart": True,
        "overwrites": True,
        "restrictfilenames": True,
        "ca_certs": certifi.where(),
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=True)
        downloaded_file = ydl.prepare_filename(info_dict)
    if not os.path.exists(downloaded_file):
        raise FileNotFoundError(
            f"YouTube download did not create the source file: {downloaded_file}"
        )
    return convert_to_wav(downloaded_file)


def convert_to_wav(input_file: str) -> str:
    """Convert any audio or video file to mono 16 kHz WAV format."""
    output_file = os.path.splitext(input_file)[0] + "_converted.wav"
    audio = AudioSegment.from_file(input_file)
    audio = audio.set_channels(1).set_frame_rate(16000)
    audio.export(output_file, format="wav")
    return output_file


def chunk_audio(wav_path: str, chunk_minutes: int = 10) -> list[str]:
    """Split a WAV file into fixed-duration chunks and return their paths."""
    if chunk_minutes <= 0:
        raise ValueError("chunk_minutes must be greater than zero")

    audio = AudioSegment.from_wav(wav_path)
    chunk_ms = chunk_minutes * 60 * 1000
    chunks = []
    for index, start in enumerate(range(0, len(audio), chunk_ms)):
        chunk = audio[start:start + chunk_ms]
        chunk_path = f"{os.path.splitext(wav_path)[0]}_chunk_{index}.wav"
        chunk.export(chunk_path, format="wav")
        chunks.append(chunk_path)
    return chunks


if __name__ == "__main__":
    url = "https://www.youtube.com/watch?v=X4FVEEegCbk"
    downloaded_file = download_youtube_audio(url)
    print(downloaded_file)
    converted_file = convert_to_wav(downloaded_file)
    print(converted_file)
    print(chunk_audio(converted_file))

def process_input(source: str, chunk_minutes: int = 2) -> list[str]:
    if source.startswith(("http://", "https://")):
        print("Detected YouTube URL. Downloading audio...")
        wav_path = download_youtube_audio(source)
    else:
        if not os.path.isfile(source):
            raise FileNotFoundError(f"Input file does not exist: {source}")
        print("Detected local file. Converting to WAV...")
        wav_path = convert_to_wav(source)

    print("Chunking audio...")
    chunks = chunk_audio(wav_path, chunk_minutes=chunk_minutes)
    print(f"Audio ready - {len(chunks)} chunk(s) created.")
    return chunks
    
