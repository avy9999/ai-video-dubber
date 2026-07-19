from fastapi import APIRouter, UploadFile, File, HTTPException, Form
from fastapi.responses import FileResponse

from app.schemas.job import UploadResponse, JobResponse
from app.services.upload_service import save_video, get_job
from fastapi import BackgroundTasks
from app.services.pipeline.pipeline import process_video

router = APIRouter()


@router.get("/")
def root():
    return {"message": "AI Video Dubber API"}


@router.post("/videos/upload", response_model=UploadResponse)
def upload_video(
    background_tasks: BackgroundTasks,
    file: UploadFile = File(...),
    source_language: str = Form(...),
    target_language: str = Form(...),
):
    job = save_video(
        file,
        source_language,
        target_language,
    )

    background_tasks.add_task(process_video, job.id)

    return UploadResponse(
        job_id=job.id,
        message="Video uploaded successfully"
    )

@router.get("/jobs/{job_id}", response_model=JobResponse)
def job_status(job_id: str):
    job = get_job(job_id)

    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobResponse(
        job_id=job.id,
        status=job.status.value,
        progress=job.progress,
    )

@router.get("/videos/download/{job_id}")
def download_video(job_id: str):

    job = get_job(job_id)

    if not job:
        raise HTTPException(
            status_code=404,
            detail="Job not found"
        )

    if not job.output_video:
        raise HTTPException(
            status_code=404,
            detail="Output video not ready"
        )

    return FileResponse(
        path=job.output_video,
        media_type="video/mp4",
        filename="dubbed_video.mp4",
    )