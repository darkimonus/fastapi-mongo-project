FROM python:3.10

ENV PYTHONUNBUFFERED 1
ENV POETRY_HOME="/opt/poetry"
# ENV POETRY_VIRTUALENVS_IN_PROJECT=true
ENV POETRY_NO_INTERACTION=1
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR /app

RUN python -m pip install --upgrade pip

RUN pip install poetry
COPY ./source /app
COPY ./docker-entrypoint.sh /

RUN poetry install --no-root
RUN chmod 755 /docker-entrypoint.sh

CMD ["/docker-entrypoint.sh"]
