# AI Video Dubber

An end-to-end AI-powered video dubbing platform that automatically translates and dubs videos while preserving speaker identity, conversation flow, and synchronization. The application combines state-of-the-art speech recognition, speaker diarization, machine translation, and neural text-to-speech models into a single processing pipeline.

Built with **FastAPI**, **React**, **Whisper**, **Pyannote Audio**, **NLLB**, **Piper TTS**, **FFmpeg**, and **Docker**.

---

## Features

- 🎥 Upload videos up to **10 minutes** in length
- 🎙️ Automatic speech transcription
- 👥 Multi-speaker identification using speaker diarization
- 🌍 Translation into multiple target languages
- 🗣️ Neural text-to-speech voice synthesis
- 🔄 Audio synchronization with the original video
- 📦 Background asynchronous processing
- 📥 Download generated dubbed videos
- 🐳 Dockerized backend for reproducible deployment
- 📄 Interactive API documentation with Swagger UI

---

### Workflow

```text
Upload Video
      │
      ▼
Speech Recognition
      │
      ▼
Speaker Diarization
      │
      ▼
Translation
      │
      ▼
Neural Voice Synthesis
      │
      ▼
Audio Synchronization
      │
      ▼
Dubbed Video Generation
      │
      ▼
Download Result
```

---

## Tech Stack

### Frontend

- React
- TypeScript
- Vite
- Tailwind CSS
- Axios

### Backend

- FastAPI
- Python 3.11
- FFmpeg
- Docker
- Uvicorn

### AI Models

| Component | Technology |
|------------|------------|
| Speech Recognition | OpenAI Whisper Small |
| Speaker Diarization | Pyannote Audio |
| Translation | Facebook NLLB-200 Distilled 600M |
| Text-to-Speech | Piper TTS |
| Audio/Video Processing | FFmpeg |

---

# Project Structure

```text
ai-video-dubber/
│
├── app/
│   ├── api/
│   ├── config/
│   ├── services/
│   │   ├── audio/
│   │   ├── diarization/
│   │   ├── ffmpeg/
│   │   ├── pipeline/
│   │   ├── transcription/
│   │   ├── translation/
│   │   └── tts/
│   └── utils/
│
├── frontend/
│
├── piper/
│   ├── runtime/
│   └── voices/
│
├── tests/
│
├── docs/
│   ├── ARCHITECTURE.md
│   ├── DESIGN_DECISIONS.md
│   └── architecture.png
│
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
└── README.md
```

---

# AI Processing Pipeline

The application processes every uploaded video through the following pipeline:

```text
                Upload Video
                     │
                     ▼
          Extract Audio (FFmpeg)
                     │
                     ▼
     Speaker Diarization (Pyannote)
                     │
                     ▼
 Speech Recognition (Whisper Small)
                     │
                     ▼
        Translation (NLLB-200)
                     │
                     ▼
      Voice Generation (Piper TTS)
                     │
                     ▼
      Audio Synchronization
                     │
                     ▼
 Merge Audio + Video (FFmpeg)
                     │
                     ▼
          Dubbed Video Output
```

Each stage is modular, allowing individual components to be replaced or upgraded independently.

---

# Supported Languages

Current implementation includes:

- English
- Hindi
- Spanish
- French

Additional Piper voices and translation models can be added with minimal configuration changes.

---

# API Endpoints

## Upload Video

```http
POST /videos/upload
```

Uploads a video and starts background processing.

---

## Get Processing Status

```http
GET /jobs/{job_id}
```

Returns the current processing state.

Example response:

```json
{
    "status": "processing",
    "progress": 60
}
```

---

## Download Dubbed Video

```http
GET /videos/download/{job_id}
```

Downloads the generated dubbed video after processing has completed.

---

# Running Locally

## Backend

Clone the repository

```bash
git clone <repository-url>

cd ai-video-dubber
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run FastAPI

```bash
uvicorn main:app --reload
```

Backend

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

## Frontend

```bash
cd frontend

npm install

npm run dev
```

Frontend

```
http://localhost:5173
```

---

# Docker

Build the Docker image

```bash
docker build -t ai-video-dubber .
```

Run the container

```bash
docker run --gpus all \
-p 8000:8000 \
--env-file .env \
ai-video-dubber
```

---

# Environment Variables

Example `.env`

```env
HF_TOKEN=your_huggingface_token
```

---

# Models Used

## Whisper Small

Responsible for multilingual automatic speech recognition.

---

## Pyannote Audio

Identifies individual speakers throughout the conversation, allowing each translated segment to preserve speaker identity.

---

## NLLB-200 Distilled 600M

Performs multilingual machine translation while maintaining sentence meaning and conversational context.

---

## Piper TTS

Generates natural offline neural speech for translated text using language-specific voice models.

---

## FFmpeg

Responsible for

- Audio extraction
- Audio synchronization
- Video rendering
- Final muxing

---

# Architecture Documentation

A detailed explanation of the application architecture is available in

```
docs/ARCHITECTURE.md
```

This document includes

- Overall system architecture
- AI pipeline
- Request lifecycle
- Processing workflow
- Deployment architecture

---

# Design Decisions

The rationale behind architectural and technology choices is documented in

```
docs/DESIGN_DECISIONS.md
```

Topics include

- Model selection
- Framework selection
- Deployment strategy
- Scalability considerations
- Trade-offs

---

# Performance Notes

The application leverages GPU acceleration whenever CUDA is available.

GPU accelerated components include

- Whisper
- Pyannote Audio
- NLLB Translation

This significantly reduces end-to-end processing time compared to CPU execution.

---

# Current Limitations

- Maximum supported video duration is 10 minutes.
- Voice cloning is not implemented.
- Translation quality depends on source audio quality.
- Uses predefined Piper voice models.
- Processing is asynchronous rather than real-time.

---

# Future Improvements

- Voice cloning
- Lip synchronization
- Streaming inference
- Cloud-native deployment
- User authentication
- Batch processing
- Additional language support
- Queue management
- Distributed processing
- Progress estimation improvements

---

# Documentation

| Document | Description |
|----------|-------------|
| README.md | Project overview |
| docs/ARCHITECTURE.md | System architecture |
| docs/DESIGN_DECISIONS.md | Engineering decisions |

---

# License

This project is licensed under the MIT License.

---

# Acknowledgements

This project makes use of several excellent open-source technologies:

- OpenAI Whisper
- Pyannote Audio
- Meta NLLB
- Piper TTS
- FFmpeg
- FastAPI
- React
- Docker

Special thanks to the open-source community for providing the tools and models that made this project possible.