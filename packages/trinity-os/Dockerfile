FROM python:3.12-slim

# 시스템 패키지 설치
RUN apt-get update && apt-get install -y \
    bash \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# 작업 디렉터리 설정
WORKDIR /app

# Python 의존성 설치
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 소스 코드 복사
COPY . .

# 실행 권한 설정
RUN chmod +x run_trinity_os.sh \
    && chmod +x init_trinity_os.sh \
    && chmod +x test_trinity_os.sh \
    && chmod +x scripts/*.sh

# 기본 명령어
CMD ["./run_trinity_os.sh"]