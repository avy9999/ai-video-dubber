import torch
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM

DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")

MODEL_NAME = "facebook/nllb-200-distilled-600M"

print(f"Loading NLLB translation model on {DEVICE}...")

tokenizer = AutoTokenizer.from_pretrained(MODEL_NAME)
model = AutoModelForSeq2SeqLM.from_pretrained(MODEL_NAME).to(DEVICE)
model.eval()

print("NLLB model loaded.")

LANGUAGE_CODES = {
    "english": "eng_Latn",
    "spanish": "spa_Latn",
    "french": "fra_Latn",
    "german": "deu_Latn",
    "hindi": "hin_Deva",
    "arabic": "arb_Arab",
}

def translate_text(text: str, target_language: str) -> str:
    tokenizer.src_lang = "eng_Latn"

    inputs = tokenizer(
        text,
        return_tensors="pt",
        truncation=True,
    ).to(DEVICE)

    with torch.inference_mode():
        translated_tokens = model.generate(
            **inputs,
            forced_bos_token_id=tokenizer.convert_tokens_to_ids(
                LANGUAGE_CODES[target_language.lower()]
            ),
            max_length=512,
        )

    return tokenizer.batch_decode(
        translated_tokens,
        skip_special_tokens=True
    )[0]

def translate_segments(segments, target_language):
    language = target_language.lower()

    if language not in LANGUAGE_CODES:
        raise ValueError(f"Unsupported language: {target_language}")

    translated_segments = []

    for segment in segments:
        translated_text = translate_text(
            segment["text"],
            target_language,
        )

        translated_segments.append(
            {
                **segment,
                "translated_text": translated_text,
            }
        )

    return translated_segments