import uuid
from pathlib import Path


UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def generate_job_id() -> str:
    return str(uuid.uuid4())


def get_upload_path(job_id: str, filename: str) -> Path:
    return UPLOAD_DIR / f"{job_id}_{filename}"