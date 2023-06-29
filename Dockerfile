# Step 1: Specify the base image
FROM python:3.8-alpine

# Step 2: Copy project files
COPY src Pipfile Pipfile.lock /app/

# Step 3: Set the working directory
WORKDIR /app

# Step 5: Install dependencies during runtime
RUN pip install pipenv
RUN pipenv install

# Step 6: Run the application
CMD ["pipenv", "run", "start"]
