# Design Decisions

This document explains the engineering decisions made while developing the AI Video Dubber platform.

---

# FastAPI

FastAPI was selected because it provides:

- High performance
- Automatic OpenAPI documentation
- Type safety
- Asynchronous request handling

These features make it well suited for AI inference services.

---

# React

React was chosen because it enables responsive user interfaces while keeping frontend and backend responsibilities separate.

---

# Whisper Small

Whisper Small was selected because it provides an effective balance between transcription accuracy and inference speed.

Larger Whisper models improve accuracy but significantly increase GPU memory usage and processing time.

---

# Pyannote Audio

Speaker diarization is essential for preserving conversation flow.

Pyannote provides accurate speaker segmentation without requiring speaker enrollment.

---

# NLLB-200 Distilled 600M

NLLB was chosen because it supports many languages while remaining lightweight enough for local GPU inference.

This avoids dependency on paid translation APIs.

---

# Piper TTS

Piper provides:

- Offline inference
- Fast synthesis
- Natural speech
- Open-source models

This makes it suitable for local deployment without cloud services.

---

# FFmpeg

FFmpeg is the industry standard for multimedia processing.

It is used for:

- Audio extraction
- Audio merging
- Video rendering
- Final encoding

---

# Docker

Docker ensures reproducible deployment by packaging:

- Runtime dependencies
- Python environment
- AI models
- FFmpeg
- Piper runtime

This removes platform-specific configuration issues.

---

# GPU Acceleration

CUDA acceleration is used for:

- Whisper
- Pyannote
- NLLB

GPU inference significantly reduces overall processing time compared to CPU execution.

---

# Background Processing

Video dubbing is computationally intensive.

Instead of blocking HTTP requests, uploads create processing jobs that execute asynchronously.

The frontend periodically polls job status until processing is complete.

---

# Trade-offs

Several design trade-offs were made during development.

### Whisper Small

Pros

- Faster inference
- Lower memory usage

Cons

- Slightly lower transcription accuracy than larger models

---

### Offline Translation

Pros

- No API costs
- Better privacy
- Works without internet

Cons

- Larger Docker image
- Higher local resource usage

---

### Piper TTS

Pros

- Offline
- Lightweight
- Fast

Cons

- Limited voice variety compared to cloud TTS providers

---

# Future Improvements

- Voice cloning
- Lip synchronization
- Queue management
- Distributed workers
- Cloud object storage
- Authentication
- Streaming inference
- Additional languages