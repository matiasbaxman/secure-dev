FROM python:3.12-slim-bookworm

RUN useradd --create-home --uid 10001 appuser && mkdir /data && chown appuser /data
WORKDIR /app
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt
COPY app.py ./
COPY templates ./templates
COPY static ./static
COPY tests ./tests

ENV PYTHONUNBUFFERED=1 DATABASE_PATH=/data/securedev.db
USER appuser
EXPOSE 8000
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "--workers", "1", "--threads", "4", "app:create_app()"]