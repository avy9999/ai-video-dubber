from pathlib import Path
import subprocess

from app.config.voices import PIPER_VOICES


def get_voice_model(language):
    if language not in PIPER_VOICES:
        raise ValueError(
            f"No Piper voice available for {language}"
        )

    return PIPER_VOICES[language]["model"]


PIPER_EXE = Path("/app/piper/runtime/piper/piper")


def synthesize(
    text,
    output_file,
    language
):
    model = get_voice_model(language)

    command = [
        str(PIPER_EXE),
        "--model",
        model,
        "--output_file",
        str(output_file),
    ]

    subprocess.run(
        command,
        input=text.encode("utf-8"),
        check=True,
    )


def synthesize_segments(
    segments: list,
    output_dir: str,
    language: str
):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_files = []

    for i, segment in enumerate(segments):
        output_file = output_dir / f"segment_{i:03d}.wav"

        synthesize(
            segment["translated_text"],
            str(output_file),
            language,
        )

        audio_files.append(str(output_file))

    return audio_files