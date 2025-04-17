# First stage: build environment
FROM python:3.9-slim as builder

RUN apt-get update && apt-get install -y \
    build-essential \
    libgl1 \
    libglib2.0-0

WORKDIR /install

COPY requirements.txt .

RUN pip install --upgrade pip
RUN pip install --prefix=/install/deps -r requirements.txt


# Final image
FROM python:3.9-slim

RUN apt-get update && apt-get install -y \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy installed deps from builder
COPY --from=builder /install/deps /usr/local

COPY api/ .

EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]