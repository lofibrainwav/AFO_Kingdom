FROM python:3.12-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
# Copy requirements first for layer caching
COPY afo_soul_engine/requirements.txt afo_soul_engine/requirements_minimal.txt* ./
RUN pip install --no-cache-dir -r requirements.txt || pip install --no-cache-dir -r requirements_minimal.txt || echo "No requirements installed"

# Install Trinity-OS (The Grand Unification)
COPY trinity-os /app/trinity-os
RUN pip install -e /app/trinity-os

# Copy application code to afo_soul_engine package directory
COPY afo_soul_engine /app/afo_soul_engine/

# Also copy api_server.py to root for direct execution
COPY afo_soul_engine/api_server.py /app/

# Set PYTHONPATH so imports like 'from afo_soul_engine.X import Y' work
ENV PYTHONPATH=/app

# Expose ports for various services
# 8001: RAG, 8005: Input, 8006: Discord, 8008: Registry, 8010: Soul Engine, 9100: Browser Auth
EXPOSE 8001 8005 8006 8008 8010 9100

# Default command (can be overridden in docker-compose)
CMD ["python", "-m", "uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8010"]
