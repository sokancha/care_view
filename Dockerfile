FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1
ENV FASTAPI_ENV "production"

WORKDIR /app

# 1. 시스템 종속성 설치 및 Python 패키지 설치를 한 번에 처리합니다.
# 단일 스테이지에서는 모든 설치가 최종 이미지에 남아있어 경로 문제가 발생하지 않습니다.
RUN apt-get update && \
    apt-get install -y --no-install-recommends gcc libpq-dev && \
    rm -rf /var/lib/apt/lists/*
    
COPY requirements.txt .
# pip 설치 시 gunicorn 실행 파일이 /usr/local/bin에 확실하게 생성됩니다.
RUN pip install --no-cache-dir -r requirements.txt

# 2. 나머지 애플리케이션 코드 복사
COPY . .

EXPOSE 8000

# 3. 앱 실행 명령어 (단일 스테이지이므로 절대 경로 없이 실행)
# gunicorn이 이제 PATH 환경 변수를 통해 정상적으로 실행됩니다.
CMD ["gunicorn", "main:app", "-w", "4", "-k", "uvicorn.workers.UvicornWorker", "-b", "0.0.0.0:8000"]
