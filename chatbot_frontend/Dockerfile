# ==========================================
# STAGE 1: Builder
# ==========================================
FROM python:3.11-slim AS builder

WORKDIR /build

COPY pyproject.toml .
RUN pip install --no-cache-dir --prefix=/install .

# ==========================================
# STAGE 2: Final Image
# ==========================================
FROM python:3.11-slim

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src/ ./src/

EXPOSE 8501

ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Streamlit production flags
CMD ["streamlit", "run", "src/main.py", "--server.address", "0.0.0.0", "--server.port", "8501", "--server.headless", "true"]