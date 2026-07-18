from pathlib import Path
from fastapi import UploadFile
import shutil

from app.models.job import Job, JobStatus
from app.utils.file_utils import generate_job_id, get_upload_path

jobs: dict[str, Job] = {}


def save_video(
    file: UploadFile,
    source_language: str,
    target_language: str,
) -> Job:
    job_id = generate_job_id()

    save_path = get_upload_path(job_id, file.filename)

    with save_path.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    job = Job(
        id=job_id,
        filename=file.filename,
        status=JobStatus.PENDING,
        progress=0,
        source_language=source_language,
        target_language=target_language,
    )

    jobs[job_id] = job

    return job


def get_job(job_id: str):
    return jobs.get(job_id)