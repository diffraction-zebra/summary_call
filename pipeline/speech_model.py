import os
from typing import IO
import replicate

model_name = 'thomasmol/whisper-diarization'

client = replicate.Client(api_token=os.environ["REPLICATE_API_KEY"])

accepted_formats = ['.mp3']


def transcribe(audio: IO[bytes], num_speakers=2) -> str:
    output = client.run(
        "thomasmol/whisper-diarization:b9fd8313c0d492bf1ce501b3d188f945389327730773ec1deb6ef233df6ea119",
        input={
            "file": audio,
            "num_speakers": num_speakers,
            "group_segments": True,
            "transcript_output_format": "both"
        }
    )

    return '\n'.join([segment['speaker']+': '+segment['text'] for segment in output['segments']])
