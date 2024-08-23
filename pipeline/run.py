from typing import IO

from speech_model import transcribe
from summarize import summarize


def run_pipeline(audio: IO[bytes]):
    transcription = transcribe(audio)
    summary = summarize(transcription)

    return summary
