import time

from app.models.job import JobStatus
from app.services.upload_service import jobs


def process_video(job_id: str):
    job = jobs[job_id]

    job.status = JobStatus.PROCESSING

    for progress in [10, 30, 50, 70, 90, 100]:
        time.sleep(2)
        job.progress = progress

    job.status = JobStatus.COMPLETED