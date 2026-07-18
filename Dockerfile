FROM python:3.11-slim-bookworm

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libsndfile1 \
    libespeak-ng1 \
    tar \
    && rm -rf /var/lib/apt/lists/*

# Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy project
COPY . .

# Extract Piper inside Linux (preserves symlinks)
RUN mkdir -p /app/piper/runtime && \
    tar -xzf /app/piper/piper_linux_x86_64.tar.gz -C /app/piper/runtime

# Make Piper executable
RUN chmod +x /app/piper/runtime/piper

# Allow Piper to find its shared libraries
ENV LD_LIBRARY_PATH=/app/piper/runtime:$LD_LIBRARY_PATH

# ---------- Pre-download Whisper ----------
RUN python scripts/preload_models.py

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]