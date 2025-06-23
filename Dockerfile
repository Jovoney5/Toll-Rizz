FROM python:3.13-slim

# Install system dependencies for PyAudio
RUN apt-get update && apt-get install -y portaudio19-dev gcc

# Set working directory
WORKDIR /app

# Copy requirements file
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy app source code
COPY . .

# Start the app (update with your actual start command)
CMD ["gunicorn", "your_application.wsgi"]
