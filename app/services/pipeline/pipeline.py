from pathlib import Path
import time

from app.models.job import JobStatus
from app.services.audio.audio_extractor import extract_audio
from app.services.upload_service import jobs
from app.utils.file_utils import get_upload_path
from app.services.speech.transcriber import transcribe
from app.services.speech.diarization import diarize


def process_video(job_id: str):
    job = jobs[job_id]
    
    try:
        job.status = JobStatus.PROCESSING

        # Step 1: Extract audio
        job.progress = 10

        video_path = get_upload_path(job.id, job.filename)
        audio_path = Path("temp") / f"{job.id}.wav"

        Path("temp").mkdir(exist_ok=True)

        extract_audio(video_path, audio_path)

        job.progress = 20

        speakers = diarize(str(audio_path))

        print("=" * 60)
        print("SPEAKERS")
        print("=" * 60)

        for speaker in speakers:
            print(speaker)

        print("=" * 60)

        job.progress = 40

        text = transcribe(str(audio_path))

        print("=" * 60)
        print("TRANSCRIPTION")
        print("=" * 60)
        print(text)
        print("=" * 60)

        job.progress = 60

        # Simulate remaining stages for now
        for progress in [80, 100]:
            time.sleep(2)
            job.progress = progress

        job.status = JobStatus.COMPLETED

    except Exception as e:
        job.status = JobStatus.FAILED
        print(e)