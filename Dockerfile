# AFO Kingdom Docker Image
# 眞善美孝永 (Truth·Goodness·Beauty·Serenity·Eternity)

FROM python:3.12.3-slim

# 眞 (Truth): Metadata for transparency
LABEL org.opencontainers.image.title="AFO Kingdom Soul Engine"
LABEL org.opencontainers.image.description="A-Philosophy-First Operating System with Trinity AI"
LABEL org.opencontainers.image.version="6.3.0"
LABEL org.opencontainers.image.authors="AFO Kingdom"

# 善 (Goodness): Security hardening - Create user BEFORE setting WORKDIR
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/* \
    && useradd --create-home --shell /bin/bash --uid 1000 app

# Set working directory AFTER user creation to avoid root-owned files
WORKDIR /app

# Copy requirements first for better caching
COPY packages/afo-core/requirements.txt /app/requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY packages/afo-core/ /app/

# 美 (Beauty): Clean up and organize
RUN mkdir -p /app/logs /app/data && \
    chown -R app:app /app

# Switch to non-root user
USER app

# 永 (Eternity): Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8010/health || exit 1

# 孝 (Serenity): Environment variables
ENV PYTHONPATH=/app
ENV API_SERVER_HOST=0.0.0.0
ENV API_SERVER_PORT=8010
ENV ENV=production

# Expose port
EXPOSE 8010

# Start the application (올바른 entrypoint)
# 방법 1: 직접 실행 (api_server.py가 /app에 있음)
CMD ["python", "api_server.py"]
# 방법 2: uvicorn 모듈 실행 (대안)
# CMD ["python", "-m", "uvicorn", "AFO.api_server:app", "--host", "0.0.0.0", "--port", "8010"]
