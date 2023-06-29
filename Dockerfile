# Step 1: Build stage
FROM python:3.8-alpine AS builder

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE_HOST=
ENV OXYGENCS_DATABASE_PORT=
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

# Copy project files
COPY src /app/src/
COPY Pipfile /app
COPY Pipfile.lock /app

# Set the working directory
WORKDIR /app

# Install build dependencies, pipenv, and cleanup
RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential \
    && pip install --no-cache-dir pipenv \
    && pipenv install --deploy \
    && apt-get remove -y build-essential \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Step 2: Runtime stage
FROM python:3.8-alpine

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE_HOST=
ENV OXYGENCS_DATABASE_PORT=
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

RUN pip install pipenv

# Copy project files from the builder stage
COPY --from=builder /app /app

# Set the working directory
WORKDIR /app

# Install runtime dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends libpq-dev \
    && pipenv install --deploy \
    && apt-get remove -y libpq-dev \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*

# Run the application
CMD ["pipenv", "run", "start"]
