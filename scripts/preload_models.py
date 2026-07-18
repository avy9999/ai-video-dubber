import os
import whisper

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from pyannote.audio import Pipeline

HF_TOKEN = os.environ.get("HUGGINGFACE_TOKEN")

print("Downloading Whisper...")
whisper.load_model("small")
print("✓ Whisper ready")

print("Downloading NLLB...")
AutoTokenizer.from_pretrained("facebook/nllb-200-distilled-600M")
AutoModelForSeq2SeqLM.from_pretrained("facebook/nllb-200-distilled-600M")
print("✓ NLLB ready")

print("Downloading Pyannote...")
Pipeline.from_pretrained(
    "pyannote/speaker-diarization-3.1",
    token=HF_TOKEN,
)
print("✓ Pyannote ready")