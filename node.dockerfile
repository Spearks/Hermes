FROM python:3.10-slim-bullseye AS build

WORKDIR /app

COPY pyproject.toml pyproject.toml
ENV PYTHONPATH=${PYTHONPATH}:${PWD} 

RUN PYTHONPATH=${PYTHONPATH}:${PWD} pip3 install poetry
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev

COPY . . 

EXPOSE 8000

RUN ["chmod", "+x", "/app/node/celery.sh"]

CMD ["/bin/bash"]
ENTRYPOINT ["/app/node/celery.sh"]
