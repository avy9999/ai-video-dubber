import torch
import whisper

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

print(f"Loading Whisper model on {DEVICE}...")

model = whisper.load_model("small", device=DEVICE)


def transcribe(audio_path: str, language: str):
    result = model.transcribe(
        audio_path,
        language=language,
        fp16=torch.cuda.is_available(),
        word_timestamps=True,
    )

    return result