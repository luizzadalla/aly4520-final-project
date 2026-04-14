FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY inference/ inference/
COPY models/ models/

EXPOSE 8080

ENTRYPOINT ["python", "inference/inference.py"]