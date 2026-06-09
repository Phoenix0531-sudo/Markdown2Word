# Build/test environment only -- GUI requires display server
FROM python:3.11-slim

WORKDIR /app

# Install system dependencies for PySide6, QtWebEngine, and pandoc CLI
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libegl1 \
    libxkbcommon-x11-0 \
    libdbus-1-3 \
    libxcb-cursor0 \
    pandoc \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Smoke test: verify Python imports and pandoc CLI (GUI will not render in Docker)
CMD ["python", "scripts/docker_smoke_test.py"]
