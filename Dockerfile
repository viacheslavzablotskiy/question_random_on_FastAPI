#I'am working on Python 3.10 taht's way used this image
FROM python:3.10-alpine

#in this step, install peotry namely 1.6.1 to escape all problem if will update the version's Poetry
RUN pip install poetry==1.6.1

#create vertualenv in my image, and indicate where the directory cache will be located
ENV POETRY_NO_INTERACTION=1 \
POETRY_VERTUALENVS_IN_PROJECT=1 \
POETRY_VERTUALENVS_CREATE=1 \
POETRY_CACHE_DIR=/tmp/poetry_cahce

#indicateting where the main directory will be located
WORKDIR ./my_project

#copy my dependencies
COPY pyproject.toml poetry.lock ./

#copy to avoid constanly  changing the entire design and reducing the number of layers
COPY my_project ./my_project

#add descriptino
RUN touch README.md

#installing all besides package for testing my image
RUN poetry install --without dev --no-root && rm -rf $POETRY_CACHE_DIR

RUN poetry install --without dev

#command for starting my image
ENTRYPOINT ["poetry", "run", "uvicorn", "my_project.main:app", "--host", "0.0.0.0", "--port", "8000"]