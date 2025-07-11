# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

# Install system dependencies
RUN apt-get update && apt-get install -y \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for better caching
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the entire project
COPY . .

# Install the package in development mode
RUN pip install -e .

# Create a non-root user for security
RUN useradd --create-home --shell /bin/bash btg_user && \
    chown -R btg_user:btg_user /app
USER btg_user

# Set the default command
ENTRYPOINT ["python", "btg_client.py"]

# Default command (can be overridden)
CMD ["--help"] 