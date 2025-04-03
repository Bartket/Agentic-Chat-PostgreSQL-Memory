FROM python:3.11-slim

WORKDIR /app

COPY poetry.lock pyproject.toml README.md /app/
COPY agentchat /app/agentchat

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install


CMD ["uvicorn", "agentchat.app:app", "--host", "0.0.0.0", "--port", "80"]
