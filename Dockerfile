FROM python:3.11-slim-bookworm

ARG HUGGINGFACE_TOKEN
ENV HUGGINGFACE_TOKEN=$HUGGINGFACE_TOKEN

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

# Extract Piper
RUN mkdir -p /app/piper/runtime && \
    tar -xzf /app/piper/piper_linux_x86_64.tar.gz -C /app/piper/runtime

RUN chmod +x /app/piper/runtime/piper

ENV LD_LIBRARY_PATH=/app/piper/runtime:$LD_LIBRARY_PATH

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]