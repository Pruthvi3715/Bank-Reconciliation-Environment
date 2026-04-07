FROM python:3.11-slim

WORKDIR /app

RUN pip install --no-cache-dir fastapi uvicorn pydantic openai faker rapidfuzz python-dotenv openenv-core

COPY . .

EXPOSE 7860

CMD ["python", "-m", "server.app"]
