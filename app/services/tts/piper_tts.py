from pathlib import Path
import subprocess

PIPER_EXE = Path("piper") / "piper.exe"
VOICE_MODEL = (
    Path("piper")
    / "voices"
    / "hi_IN-pratham-medium.onnx"
)


def synthesize(text: str, output_file: str):
    command = [
        str(PIPER_EXE),
        "--model",
        str(VOICE_MODEL),
        "--output_file",
        output_file,
    ]

    subprocess.run(
        command,
        input=text.encode("utf-8"),
        check=True,
    )


def synthesize_segments(segments: list, output_dir: str):
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    audio_files = []

    for i, segment in enumerate(segments):
        output_file = output_dir / f"segment_{i:03d}.wav"

        synthesize(
            segment["translated_text"],
            str(output_file),
        )

        audio_files.append(str(output_file))

    return audio_files