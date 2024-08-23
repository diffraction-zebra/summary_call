from typing import IO

from pipeline.speech_model import transcribe
from pipeline.summarize import summarize


def run_pipeline(audio: IO[bytes]):
    transcription = transcribe(audio)
    summary = summarize(transcription)

    return summary
