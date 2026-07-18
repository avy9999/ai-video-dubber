from pathlib import Path
import time

from app.models.job import JobStatus
from app.services.audio.audio_extractor import extract_audio
from app.services.upload_service import jobs
from app.utils.file_utils import get_upload_path


def process_video(job_id: str):
    job = jobs[job_id]

    job.status = JobStatus.PROCESSING

    # Step 1: Extract audio
    job.progress = 10

    video_path = get_upload_path(job.id, job.filename)
    audio_path = Path("temp") / f"{job.id}.wav"

    Path("temp").mkdir(exist_ok=True)

    extract_audio(video_path, audio_path)

    # Simulate remaining stages for now
    for progress in [30, 50, 70, 90, 100]:
        time.sleep(2)
        job.progress = progress

    job.status = JobStatus.COMPLETED