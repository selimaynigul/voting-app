# Stage 1: Build dependencies
FROM python:3.11-slim AS builder

WORKDIR /usr/src/app

# Install build tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Upgrade pip and tools
RUN pip install --upgrade pip setuptools wheel

# Install Python deps to /install
COPY requirements.txt ./
RUN pip install --prefix=/install --no-cache-dir -r requirements.txt

# Stage 2: Production image
FROM python:3.11-slim

WORKDIR /usr/src/app

# Create non-root user
RUN groupadd --system --gid 1001 appuser && \
    useradd --system --uid 1001 --gid appuser appuser

USER appuser

# Copy dependencies from builder
COPY --from=builder --chown=appuser:appuser /install /usr/local

# Set environment
ENV PATH=/home/appuser/.local/bin:$PATH
ENV PYTHONUNBUFFERED=1

# Copy app code
COPY --chown=appuser:appuser . .

# Expose app port
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:5000/ || exit 1

# Run app
CMD ["python", "app.py"]
