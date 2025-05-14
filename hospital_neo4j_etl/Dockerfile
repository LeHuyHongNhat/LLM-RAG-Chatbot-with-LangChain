# Use Python 3.11 as base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Copy project files
COPY pyproject.toml .
COPY src/ ./src/
COPY entrypoint.sh .

# Make entrypoint script executable
RUN chmod +x entrypoint.sh

# Install dependencies
RUN pip install --no-cache-dir .

# Set Python specific environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Command to run the ETL script
CMD ["./entrypoint.sh"]