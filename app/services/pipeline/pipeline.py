from pathlib import Path
import time

from app.models.job import JobStatus
from app.services.audio.audio_extractor import extract_audio
from app.services.upload_service import jobs
from app.utils.file_utils import get_upload_path
from app.services.speech.transcriber import transcribe
from app.services.speech.diarization import diarize
from app.services.speech.merger import merge_speakers


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
        whisper_result = transcribe(str(audio_path))

        merged = merge_speakers(
            speakers,
            whisper_result["segments"],
        )

        print("=" * 60)
        print("SPEAKER TRANSCRIPT")
        print("=" * 60)

        for line in merged:
            print(line)

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