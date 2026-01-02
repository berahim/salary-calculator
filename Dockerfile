FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY main.py .

# Create logs directory
RUN mkdir -p /app/logs
ENV PORT=8001
ENV TAX_RATE=0.6
ENV LOG_LEVEL=INFO
EXPOSE $PORT
CMD uvicorn main:app --host 0.0.0.0 --port $PORT