# Use the official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
  build-essential \
  gcc \
  libffi-dev \
  libssl-dev \
  python3-dev \
  && rm -rf /var/lib/apt/lists/*

# Copy files
COPY . .

# Install pip and dependencies
RUN pip install --upgrade pip setuptools wheel
RUN pip install --no-cache-dir -r requirements.txt