# Multi-stage build for a smaller final image
# Stage 1: Build the application
FROM python:3.9-slim-buster AS builder

# Set working directory inside the container
WORKDIR /usr/src/app

# Copy requirements file and install dependencies
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code
COPY . .

# Stage 2: Create a minimal production image
FROM python:3.9-slim-buster

# Create a non-root user and switch to it for security
RUN groupadd --system --gid 1001 appuser && \
    useradd --system --uid 1001 --gid appuser appuser
USER appuser

# Set working directory
WORKDIR /usr/src/app

# Copy only the necessary files from the builder stage
COPY --from=builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=builder /usr/src/app .

# Expose the application port
EXPOSE 5000

# Define the command to run the application
CMD ["python", "./app.py"]