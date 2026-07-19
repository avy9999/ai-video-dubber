from pydantic import BaseModel


class UploadResponse(BaseModel):
    job_id: str
    message: str


class JobResponse(BaseModel):
    job_id: str
    status: str
    progress: int