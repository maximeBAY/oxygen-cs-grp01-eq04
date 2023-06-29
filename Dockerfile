FROM python:3.8-alpine as base

# Setup env
ENV LANG C.UTF-8
ENV LC_ALL C.UTF-8
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONFAULTHANDLER 1


FROM base AS python-deps

# Install pipenv and compilation dependencies
RUN pip install pipenv
RUN apt-get update && apt-get install -y --no-install-recommends gcc

# Install python dependencies in /.venv
COPY Pipfile .
COPY Pipfile.lock .
RUN PIPENV_VENV_IN_PROJECT=1 pipenv install --deploy


FROM base AS runtime

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE_HOST=
ENV OXYGENCS_DATABASE_PORT=
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

# Copy virtual env from python-deps stage
COPY --from=python-deps /.venv /.venv
ENV PATH="/.venv/bin:$PATH"


# Install application into container
# Copy project files from the builder stage
COPY --from=python-deps /app/src /app/src
COPY --from=python-deps /app/Pipfile /app/Pipfile
COPY --from=python-deps /app/Pipfile.lock /app/Pipfile.lock

WORKDIR /app


# Run the application
CMD ["pipenv", "run","start"]
