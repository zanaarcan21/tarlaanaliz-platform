# =============================================================================
# Dockerfile — Backend (FastAPI) production-ready container imaji
# KR-040 Konteyner guvenligi: multi-stage build, non-root user, minimal image
# =============================================================================

# ---------------------------------------------------------------------------
# Stage 1: Builder — bagimlilik kurulumu
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS builder

WORKDIR /build

# Sistem bagimliliklari (derleme icin gerekli)
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Python bagimliliklari
COPY pyproject.toml ./
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir --prefix=/install .

# ---------------------------------------------------------------------------
# Stage 2: Runtime — minimal production image
# ---------------------------------------------------------------------------
FROM python:3.12-slim AS runtime

# Guvenlik: non-root kullanici [KR-040]
RUN groupadd --gid 1000 appuser \
    && useradd --uid 1000 --gid appuser --shell /bin/bash --create-home appuser

WORKDIR /app

# Sistem runtime bagimliliklari
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Builder'dan Python paketlerini kopyala
COPY --from=builder /install /usr/local

# Kaynak kodu kopyala
COPY alembic/ ./alembic/
COPY alembic.ini ./
COPY src/ ./src/

# Non-root kullaniciya gec [KR-040: least privilege]
USER appuser

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
    CMD curl -f http://localhost:8000/health || exit 1

# Port
EXPOSE 8000

# Calistirma komutu: Uvicorn ile FastAPI
CMD ["python", "-m", "uvicorn", "src.presentation.api.main:app", \
     "--host", "0.0.0.0", \
     "--port", "8000", \
     "--workers", "4", \
     "--log-level", "info"]
