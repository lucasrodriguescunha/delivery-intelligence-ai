FROM python:3.12-slim

WORKDIR /app

# Copy requirements first — Docker caches this layer; reinstall only when deps change
COPY backend/requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY backend/app/ ./backend/app/
COPY data/ ./data/

WORKDIR /app/backend/app

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]