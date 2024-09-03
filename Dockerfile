FROM python:3.10-slim

ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY pyproject.toml poetry.lock* /app/

RUN pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-dev --no-interaction --no-ansi

COPY . /app/

RUN mkdir -p /app/logs

EXPOSE 8000

CMD ["sh", "-c", "pytest && uvicorn app.main:app --host 0.0.0.0 --port 8000"]
