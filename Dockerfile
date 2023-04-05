FROM python:3.11

WORKDIR /app
ENV PYTHONUNBUFFERED 1
RUN pip install --upgrade pip poetry==1.4.2 && poetry config virtualenvs.create false

COPY pyproject.toml .
COPY poetry.lock .
RUN poetry install --no-dev
COPY . .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8080"]
