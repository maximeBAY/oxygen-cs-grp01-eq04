# Step 1: Specify the base image
FROM python:3.8

# Step 2: Copy project files
COPY . /app

# Step 3: Set the working directory
WORKDIR /app

# Step 5: Install dependencies during runtime
pipenv install

# Step 6: Run the application
CMD python app.py
