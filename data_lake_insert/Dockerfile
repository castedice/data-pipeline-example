FROM python:3.9

WORKDIR /app
COPY pyproject.toml /app
COPY .env /app

ENV PYTHONPATH=${PYTHONPATH}:${PWD}

RUN pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY ./data_lake_insert /app/data_lake_insert


