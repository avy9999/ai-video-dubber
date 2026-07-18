from pathlib import Path
import traceback

from app.models.job import JobStatus
from app.services.upload_service import jobs
from app.utils.file_utils import get_upload_path
from app.services.speech.transcriber import transcribe
from app.services.speech.diarization import diarize
from app.services.translation.translator import translate_segments
from app.services.tts.piper_tts import synthesize_segments
from app.services.audio.audio_merger import merge_audio_segments
from app.services.speech.sentence_builder import build_segments
from app.services.audio.audio_extractor import (
    extract_audio,
    get_video_duration,
    replace_audio,
)
from app.services.cleanup_service import cleanup_job

def process_video(job_id: str):
    job = jobs[job_id]
    
    try:
        job.status = JobStatus.PROCESSING

        # Step 1: Extract audio
        job.progress = 10

        video_path = get_upload_path(job.id, job.filename)

        duration = get_video_duration(video_path)

        if duration > 600:
            raise ValueError(
                "Video length must be under 10 minutes"
            )

        audio_path = Path("temp") / f"{job.id}.wav"

        Path("temp").mkdir(exist_ok=True)

        extract_audio(video_path, audio_path)

        job.progress = 20

        # Step 2: Speaker diarization
        speakers = diarize(str(audio_path))
        job.progress = 35

        # Step 3: Speech transcription
        whisper_result = transcribe(
            str(audio_path),
            job.source_language,
        )

        # print("\nFirst 5 Whisper segments:")
        # for segment in whisper_result["segments"][:5]:
        #     print(segment)

        job.progress = 50

        # Step 4: Merge speakers with transcript
        segments = build_segments(
            whisper_result["segments"],
            speakers,
        )

        # print("\nFirst 10 built segments:")
        # for segment in segments[:10]:
        #     print(segment)

        job.progress = 60

        # Step 5: Translate transcript
        translated = translate_segments(
            segments,
            job.target_language,
        )

        job.transcript = translated
        job.progress = 80

        # 👇 Temporary debug
        # print("\nFirst 5 translated segments:")
        # for segment in translated[:5]:
        #     print(segment)

        # Step 6: Generate speech
        audio_segments = synthesize_segments(
            translated,
            Path("temp") / job.id,
            job.target_language,
        )

        duration = get_video_duration(video_path)

        dubbed_audio = Path("temp") / f"{job.id}_dubbed.wav"

        merge_audio_segments(
            translated,
            Path("temp") / job.id,
            dubbed_audio,
            duration,
        )

        job.progress = 95

        output_dir = Path("output")
        output_dir.mkdir(exist_ok=True)

        output_video = output_dir / f"{job.id}_dubbed.mp4"

        replace_audio(
            video_path,
            dubbed_audio,
            output_video,
        )

        job.output_video = str(output_video)

        # Remove uploaded original video
        if video_path.exists():
            video_path.unlink()

        cleanup_job(job.id)

        job.progress = 100
        job.status = JobStatus.COMPLETED

    except Exception as e:
        job.status = JobStatus.FAILED
        traceback.print_exc()