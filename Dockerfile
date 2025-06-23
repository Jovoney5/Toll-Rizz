# Use official Python slim image
FROM python:3.13-slim

# Install system dependencies (including portaudio)
RUN apt-get update && apt-get install -y \
    portaudio19-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Set working directory inside container
WORKDIR /app

# Copy requirements.txt first (for caching)
COPY requirements.txt .

# Upgrade pip and install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy all your app files to container
COPY . .

# Expose port 5000 (Flask default)
EXPOSE 5000

# Run your app using gunicorn
CMD ["gunicorn", "app:app", "--bind", "0.0.0.0:5000"]
