FROM python:3.13.7-trixie AS base
# Install python/poetry
RUN apt-get update && apt-get install -y exiftool qpdf
ENV PYTHONUNBUFFERED=1
RUN mkdir /etc/poetry
RUN curl -sSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3 -
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN /etc/poetry/bin/poetry config virtualenvs.create false \
  && /etc/poetry/bin/poetry install --no-interaction --no-ansi --no-root
COPY ./src .

ENV HOME=/

CMD ["python", "demo.py"]
