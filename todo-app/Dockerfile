FROM python:3.13-slim@sha256:09a17cad02668ae61ece136b4fd36ac3849e14f670ebedb637ea3e15580525bc AS builder

WORKDIR /build

RUN python -m venv /opt/venv

COPY requirements.txt .

RUN /opt/venv/bin/python -m pip install --no-cache-dir --require-hashes -r requirements.txt


FROM python:3.13-slim@sha256:09a17cad02668ae61ece136b4fd36ac3849e14f670ebedb637ea3e15580525bc AS runtime

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/opt/venv/bin:$PATH"

WORKDIR /app

RUN useradd --uid 10001 --create-home appuser

COPY --from=builder /opt/venv /opt/venv
COPY main.py .

USER appuser

EXPOSE 8000

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
