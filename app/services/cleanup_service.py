from pathlib import Path
import shutil


def cleanup_job(job_id: str):
    temp_dir = Path("temp") / job_id

    if temp_dir.exists():
        shutil.rmtree(temp_dir)

    files_to_remove = [
        Path("temp") / f"{job_id}.wav",
        Path("temp") / f"{job_id}_dubbed.wav",
    ]

    for file in files_to_remove:
        if file.exists():
            file.unlink()