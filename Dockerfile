FROM python:3.14

RUN mkdir /booking

WORKDIR /booking

COPY pyproject.toml uv.lock ./

RUN pip install --no-cache-dir .

COPY . .

CMD ["gunicorn", "main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind=0.0.0.0:8000"]