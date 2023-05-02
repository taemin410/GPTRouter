FROM tiangolo/uvicorn-gunicorn:python3.11

COPY ./app /usr/src/app
WORKDIR /usr/src

ARG ENV
ENV ENV=$ENV

RUN pip install poetry

COPY ./poetry.lock ./pyproject.toml ./
RUN poetry install


EXPOSE 8000

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
