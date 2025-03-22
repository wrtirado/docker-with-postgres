# Use the official Python image
FROM python:3.11

# Set the working directory inside the container
WORKDIR /app

# Copy files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt