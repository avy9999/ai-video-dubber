from pathlib import Path
import subprocess
import wave


def get_audio_duration(audio_file: Path) -> float:
    with wave.open(str(audio_file), "rb") as wav:
        frames = wav.getnframes()
        rate = wav.getframerate()
        return frames / rate

def merge_audio_segments(
    segments: list,
    segment_dir: Path,
    output_file: Path,
    total_duration: float,
):
    segment_dir = Path(segment_dir)

    command = ["ffmpeg", "-y"]

    filter_parts = []

    # Add every generated segment as an input
    for i, segment in enumerate(segments):
        audio_file = segment_dir / f"segment_{i:03d}.wav"

        if not audio_file.exists():
            continue

        duration = get_audio_duration(audio_file)

        if i < len(segments) - 1:
            available = segments[i + 1]["start"] - segment["start"]
        else:
            available = duration

        if duration > available * 1.05 and available > 0:

            speed = duration / available

            # Avoid unnatural speech
            speed = min(max(speed, 1.0), 1.35)

            adjusted = segment_dir / f"segment_{i:03d}_fast.wav"

            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    str(audio_file),
                    "-filter:a",
                    f"atempo={speed:.3f}",
                    str(adjusted),
                ],
                check=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
            )

            audio_file = adjusted

        if not audio_file.exists():
            continue

        command.extend(["-i", str(audio_file)])

        delay = int(segment["start"] * 1000)

        filter_parts.append(
            f"[{len(filter_parts)}:a]adelay={delay}|{delay}[a{i}]"
        )

    if not filter_parts:
        raise RuntimeError("No audio segments found.")

    input_count = len(filter_parts)

    inputs = "".join(f"[a{i}]" for i in range(input_count))

    filter_parts.append(
        f"{inputs}amix=inputs={input_count}:normalize=0"
    )

    command.extend([
        "-filter_complex",
        ";".join(filter_parts),
        "-t",
        str(total_duration),
        str(output_file),
    ])

    subprocess.run(
        command,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    return output_file