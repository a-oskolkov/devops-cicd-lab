FROM python:3.12-slim AS builder

WORKDIR /build

COPY src/requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt


FROM python:3.12-slim AS runtime

LABEL maintainer="your@email.com"
LABEL description="DevOps lab application"

WORKDIR /app

COPY --from=builder /install /usr/local
COPY src/ .

RUN useradd --create-home appuser
USER appuser

EXPOSE 5000

HEALTHCHECK --interval=30s --timeout=3s \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

CMD ["python", "app.py"]
