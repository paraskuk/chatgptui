# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Checks all images
ENV DOCKER_CONTENT_TRUST = 1

# Labels
LABEL version = "1.0.0"

# Set the working directory
WORKDIR OpenAI

# Create volume directory
RUN mkdir -p /docker/data

ENV PYTHONDONTWRITEBYTECODE 1

ENV PYTHONUNBUFFERED 1

RUN apt-get update \
    && apt-get install -y curl \
    && apt-get -y install  nano \
     && apt-get clean

# Copy the requirements file into the container
COPY requirements.txt .

# Install any needed packages specified in requirements.txt
RUN pip3 install --trusted-host pypi.python.org -r requirements.txt

# Set environment variables
ARG OPEN_AI_KEY
ENV OPEN_AI_KEY=${OPEN_AI_KEY}

# Copy the rest of the application code
COPY . .

# Run the command to start the app
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "80"]
