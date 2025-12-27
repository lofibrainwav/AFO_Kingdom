# ==========================================
# Phase 17: Cloud Ascension - Unified Build
# ==========================================
FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies globally
COPY requirements.txt requirements_minimal.txt* ./
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir -r requirements_minimal.txt



# Explicit uvicorn installation (RAG service fix)
RUN pip install --no-cache-dir "uvicorn[standard]>=0.31.1"
RUN python -c "import uvicorn; print('uvicorn', uvicorn.__version__)"
# Copy Application Code
COPY AFO /app/AFO
COPY afo_soul_engine /app/afo_soul_engine
COPY scripts /app/scripts

# Set Environment
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

ENV HOME=/tmp
ENV PIP_CACHE_DIR=/tmp/pip-cache
ENV PIP_DISABLE_PIP_VERSION_CHECK=1
RUN python -m pip install -U pip && python -m pip install --no-cache-dir crewai 'crewai[tools]' autogen-agentchat

# Expose Ports
EXPOSE 8010 8001

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
  CMD curl -f http://localhost:8010/health || exit 1

# Command
CMD ["python", "-m", "uvicorn", "AFO.api_server:app", "--host", "0.0.0.0", "--port", "8010"]
