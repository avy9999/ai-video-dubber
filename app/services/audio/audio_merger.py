from pathlib import Path
import subprocess


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

        command.extend(["-i", str(audio_file)])

        delay = int(segment["start"] * 1000)

        filter_parts.append(
            f"[{len(filter_parts)}:a]adelay={delay}|{delay}[a{i}]"
        )

    if not filter_parts:
        raise RuntimeError("No audio segments found.")

    inputs = "".join(f"[a{i}]" for i in range(len(filter_parts)))

    filter_parts.append(
        f"{inputs}amix=inputs={len(filter_parts)}:normalize=0"
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