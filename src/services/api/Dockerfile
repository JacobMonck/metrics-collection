FROM python:3.10-slim-buster

WORKDIR /api

RUN pip install poetry

COPY pyproject.toml /api
COPY poetry.lock /api

RUN poetry install

COPY . /api

CMD ["sh", "launcher.sh"]