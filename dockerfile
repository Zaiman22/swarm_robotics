# Use an official lightweight Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    python3-dev \
    libblas-dev \
    liblapack-dev \
    gfortran \
    python3-tk \
    && rm -rf /var/lib/apt/lists/*

COPY ./requirements.txt .

# Install PyDy and common scientific packages
RUN pip install --no-cache-dir -r ./requirements.txt

CMD [ "bash" ]