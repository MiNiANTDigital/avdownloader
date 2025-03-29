# Use a Python base image
FROM python:3.11-slim

# Install ffmpeg
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Set the working directory
WORKDIR /app

# Copy the application files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt


# Expose the port the app will run on
EXPOSE 8080

# Run the Flask application
CMD ["python", "app.py"]
# CMD ["gunicorn", "-b", "0.0.0.0:8080", "app:app"]

