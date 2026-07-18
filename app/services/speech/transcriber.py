import torch
import whisper

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading Whisper model on {DEVICE}...")

model = whisper.load_model("base", device=DEVICE)


def transcribe(audio_path: str):
    result = model.transcribe(
        audio_path,
        language="en",
        fp16=torch.cuda.is_available()
    )

    return result["text"]