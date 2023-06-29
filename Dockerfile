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

# Install dependencies
RUN apk add --no-cache build-base && \
    pip install pipenv && \
    pipenv install --deploy

# Step 2: Runtime stage
FROM python:3.8-alpine

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE_HOST=
ENV OXYGENCS_DATABASE_PORT=
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

# Copy project files from the builder stage
COPY --from=builder /usr/local/lib/python3.8/site-packages /usr/local/lib/python3.8/site-packages
COPY --from=builder /usr/local/bin/pipenv /usr/local/bin/pipenv
COPY --from=builder /app/src /app/src
COPY --from=builder /app/Pipfile /app/Pipfile
COPY --from=builder /app/Pipfile.lock /app/Pipfile.lock

# Set the working directory
WORKDIR /app


# Run the application
CMD ["pipenv", "run","start"]
