# Base image
FROM python:3.12-slim

# Prevent Python from writing .pyc files and buffer stdout/stderr
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PORT=5000 \
    APP_ENV=production

# Set working directory
WORKDIR /app

# Install system dependencies if required, then Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source code
COPY . .

# Create a non-privileged user and switch to it for better security
RUN useradd -u 8888 appuser && chown -R appuser:appuser /app
USER appuser

# Expose service port
EXPOSE 5000

# Container healthcheck using standard Python urllib
HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
    CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:5000/health')" || exit 1

# Start application using Gunicorn WSGI server
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
