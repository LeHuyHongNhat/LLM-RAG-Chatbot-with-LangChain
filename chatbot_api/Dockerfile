# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

# Install build dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
# Install dependencies into a temporary directory
RUN pip install --no-cache-dir --prefix=/install .

# ==========================================
# STAGE 2: Final Image
# ==========================================
FROM python:3.11-slim

WORKDIR /app

# Copy only the installed packages from builder
COPY --from=builder /install /usr/local
COPY src/ ./src/

# Render cung cấp biến PORT tự động, mặc định là 10000 nếu không có
EXPOSE 8000

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Giảm xuống 1 worker để chạy vừa vặn trong 512MB RAM của Render Free Tier
CMD ["gunicorn", "-w", "1", "-k", "uvicorn.workers.UvicornWorker", "src.main:app", "--bind", "0.0.0.0:8000"]