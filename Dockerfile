# Step 1: Specify the base image
FROM python:3.8-alpine

ENV OXYGENCS_HOST=http://34.95.34.5
ENV OXYGENCS_TICKETS=3
ENV OXYGENCS_T_MAX=30
ENV OXYGENCS_T_MIN=15
ENV OXYGENCS_DATABASE_HOST=TODO
ENV OXYGENCS_DATABASE_PORT=TODO
ENV OXYGENCS_TOKEN=liLAxrQ6Ed

# Step 2: Copy project files
COPY src /app/src/
COPY Pipfile /app

# Step 3: Set the working directory
WORKDIR /app

# Step 4: Install dependencies
RUN set -ex \
    && pip install pipenv \
    && pipenv install \
    && rm -rf /var/lib/apt/lists/* \
    && rm -rf /media \ 
    && rm -rf /bin/busybox \
    && rm -rf /tmp 

# Step 5: Run the application
CMD ["pipenv", "run", "start"]
