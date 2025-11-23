FROM python:3.10-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

# 1. 시스템 종속성 설치 (apt-get 사용)
# libpq-dev: PostgreSQL 라이브러리 헤더 파일 (psycopg 설치에 필수)
# gcc: C 컴파일러 (psycopg 설치에 필수)
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# 2. Python 라이브러리 설치
# requirements.txt 파일 복사
COPY requirements.txt .
# 라이브러리 설치 (psycopg[binary] 포함)
RUN pip install --no-cache-dir -r requirements.txt

# 3. 나머지 애플리케이션 코드 복사
COPY . .

# 4. 앱 실행 명령어
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]