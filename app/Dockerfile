# =========================
# Stage 1: Build dependencies
# =========================
FROM python:3.11-slim AS builder
# Use Python 3.11 slim image as the base for building dependencies

WORKDIR /usr/src/app
# Set working directory inside the container

# Set pip cache directory to improve rebuild performance
ENV PIP_CACHE_DIR=/root/.cache/pip

# Copy only requirements.txt first to leverage Docker layer caching
# This ensures that dependencies are only rebuilt if requirements.txt changes
COPY requirements.txt .

# Build wheel files for all Python dependencies
# Wheels allow faster installation in the final image
RUN pip wheel --wheel-dir=/usr/src/app/wheels -r requirements.txt

# =========================
# Stage 2: Production image
# =========================
FROM python:3.11-slim AS final
# Use a fresh slim Python image for the final runtime

# Set environment variables
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PATH="/home/appuser/.local/bin:$PATH"
# PYTHONDONTWRITEBYTECODE: prevent .pyc files
# PYTHONUNBUFFERED: unbuffered stdout/stderr for logging
# PATH: include local user binaries

WORKDIR /usr/src/app
# Set working directory in the final image

# Install runtime dependencies (minimal)
# libpq5 is needed for PostgreSQL client (psycopg2)
# curl is used for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    && rm -rf /var/lib/apt/lists/*
# Clean apt cache to reduce image size

# Create a non-root user for security
RUN groupadd --system --gid 1001 appuser && \
    useradd --system --uid 1001 --gid appuser --home /home/appuser --create-home appuser

# Copy Python wheels and application code
COPY --from=builder /usr/src/app/wheels /usr/src/app/wheels
COPY --chown=appuser:appuser . .
# Using --chown ensures the non-root user owns the files

# Install Python dependencies from wheels without internet
RUN pip install --no-index --find-links=/usr/src/app/wheels -r requirements.txt

# Switch to the non-root user
USER appuser

# Expose Flask app port
EXPOSE 5000

# Add a healthcheck for Docker to monitor container health
HEALTHCHECK --interval=30s --timeout=5s CMD curl -f http://localhost:5000/healthz || exit 1

# Default command to run the app
CMD ["python", "app.py"]
