FROM python:3.10-slim

# Install system packages needed for OpenCV and Ultralytics
RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only the API app (and its requirements)
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy all code inside /api
COPY api/ .

# Expose FastAPI port
EXPOSE 8000

# Start FastAPI app
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]