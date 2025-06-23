# Use an official Python runtime as a parent image
FROM python:3.13-slim

# Install system dependencies required for PyAudio
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run the Flask app
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]

