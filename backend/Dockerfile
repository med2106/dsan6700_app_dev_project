# FastAPI Backend Dockerfile
FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PYTHONPATH=/app/src

WORKDIR /app

# System deps (curl for healthcheck; libgomp1 for xgboost runtime; build tools optional)
RUN apt-get update && apt-get install -y --no-install-recommends \
      curl \
      libgomp1 \
      build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install uv (pip’s fine here)
RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml poetry.lock* ./

# --- Dependencies ---
# Use versions compatible with Pydantic v2 + modern FastAPI
# (pin within sensible ranges; adjust if you truly need the old stack)
RUN poetry config virtualenvs.create false \
    && poetry install --no-interaction --no-ansi --no-root

# --- Source code ---
COPY src/ /app/src/

# Expose port
EXPOSE 8000

# Healthcheck (expects GET /health)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8000/health || exit 1

# Start server (note: api.main, not src.api.main)
CMD ["uvicorn", "api.main:app", "--host", "0.0.0.0", "--port", "8000"]
