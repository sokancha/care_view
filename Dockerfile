FROM python:3.12-slim

ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# 🚨 수정된 부분: CMD를 쉘 스크립트 실행 명령으로 변경
# 1. 'python initial_data.py'를 실행하여 DB 테이블 생성
# 2. '&&' 연산자로 스크립트가 성공적으로 종료된 후, Uvicorn 서버를 실행
CMD ["sh", "-c", "python initial_data.py && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
