from pathlib import Path
import time

from app.models.job import JobStatus
from app.services.audio.audio_extractor import extract_audio
from app.services.upload_service import jobs
from app.utils.file_utils import get_upload_path
from app.services.speech.transcriber import transcribe
from app.services.speech.diarization import diarize
from app.services.speech.merger import merge_speakers
from app.services.translation.translator import translate_segments


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

        # Step 2: Speaker diarization
        speakers = diarize(str(audio_path))
        job.progress = 35

        # Step 3: Speech transcription
        whisper_result = transcribe(str(audio_path))
        job.progress = 50

        # Step 4: Merge speakers with transcript
        merged = merge_speakers(
            speakers,
            whisper_result["segments"],
        )
        job.progress = 60

        # Step 5: Translate transcript
        translated = translate_segments(
            merged,
            "spanish",
        )
        job.transcript = translated
        job.progress = 80

        print("=" * 60)
        print("TRANSLATED TRANSCRIPT")
        print("=" * 60)

        for line in translated:
            print(line)

        print("=" * 60)

        job.progress = 100
        job.status = JobStatus.COMPLETED

    except Exception as e:
        job.status = JobStatus.FAILED
        print(e)