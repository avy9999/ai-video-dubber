import os

import numpy as np
import soundfile as sf
import torch
from dotenv import load_dotenv
from pyannote.audio import Pipeline

load_dotenv()

HF_TOKEN = os.getenv("HUGGINGFACE_TOKEN")

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

print(f"Loading Speaker Diarization model on {DEVICE}...")

pipeline = Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=HF_TOKEN,
)

pipeline.to(DEVICE)

print("Speaker Diarization model loaded.")


def diarize(audio_path: str):
    waveform, sample_rate = sf.read(audio_path)

    # Convert stereo to mono if needed
    if waveform.ndim == 2:
        waveform = waveform.mean(axis=1)

    # Convert to float32 (required by the model)
    waveform = waveform.astype(np.float32)

    # Create tensor and move it to the same device as the model
    waveform = torch.from_numpy(waveform).unsqueeze(0).to(DEVICE)

    diarization = pipeline(
        {
            "waveform": waveform,
            "sample_rate": sample_rate,
        }
    )

    annotation = diarization.speaker_diarization

    speakers = []

    for turn, _, speaker in annotation.itertracks(yield_label=True):
        speakers.append(
            {
                "speaker": speaker,
                "start": round(turn.start, 2),
                "end": round(turn.end, 2),
            }
        )

    return speakers