# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Install system dependencies required for PyAudio and building packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    portaudio19-dev \
    build-essential \
    python3-dev \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy requirements file and install Python dependencies
COPY requirements.txt .
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the rest of the application
COPY . .

# Expose the port your Flask app runs on
EXPOSE 5000

# Command to run the Flask app using Gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
