# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

# ==========================================
# STAGE 2: Final Image
# ==========================================
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src/ ./src/
COPY entrypoint.sh .
RUN chmod +x entrypoint.sh

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

CMD ["./entrypoint.sh"]