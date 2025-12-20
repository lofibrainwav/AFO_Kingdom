# ==========================================
# Phase 17: Cloud Ascension - Optimized Base
# ==========================================
FROM python:3.12-slim as builder

WORKDIR /app

# Install system dependencies for build
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies to user directory
COPY requirements.txt requirements_minimal.txt* ./
RUN pip install --user --no-cache-dir -r requirements.txt || pip install --user --no-cache-dir -r requirements_minimal.txt

# ==========================================
# Final Stage - Light & Secure (Guidance: 善)
# ==========================================
FROM python:3.12-slim

WORKDIR /app

# Install runtime dependencies (curl for healthcheck)
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy python dependencies from builder
COPY --from=builder /root/.local /root/.local
ENV PATH=/root/.local/bin:$PATH

# Copy Application Code (Truth: AFO is the SSOT)
COPY AFO /app/AFO
COPY afo_soul_engine /app/afo_soul_engine
COPY scripts /app/scripts

# Set Environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose Soul Engine Port
EXPOSE 8010

# Healthcheck (Phase 17-4 preparation)
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8010/health || exit 1

# Command (Running the Soul Engine)
CMD ["python", "-m", "uvicorn", "AFO.api_server:app", "--host", "0.0.0.0", "--port", "8010"]
