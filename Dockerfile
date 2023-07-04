# Step 1: Build stage
FROM python:3.8-alpine AS builder

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE=postgres
ENV OXYGENCS_DATABASE_HOST=postgres_container
ENV OXYGENCS_DATABASE_PORT=5432
ENV OXYGENCS_DATABASE_USERNAME=postgres
ENV OXYGENCS_DATABASE_PASSWORD=postgres
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

# Copy project files
COPY src /app/src/
COPY src /app/tests/
COPY Pipfile /app
COPY Pipfile.lock /app

# Set the working directory
WORKDIR /app

# Install dependencies
RUN apk add --no-cache build-base && \
    pip install --no-cache-dir pipenv && \
    pipenv install --deploy

# Step 2: Runtime stage
FROM python:3.8-alpine

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE=postgres
ENV OXYGENCS_DATABASE_HOST=postgres_container
ENV OXYGENCS_DATABASE_PORT=5432
ENV OXYGENCS_DATABASE_USERNAME=postgres
ENV OXYGENCS_DATABASE_PASSWORD=postgres
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

RUN pip install pipenv

# Copy project files from the builder stage
COPY --from=builder /app /app

# Set the working directoryy
WORKDIR /app

# Install runtime dependencies
RUN apk add --no-cache libpq
RUN pipenv install --deploy


# Run the application
CMD ["pipenv", "run", "start"]
