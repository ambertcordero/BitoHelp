# -------------------------------------------------------
# CrypToCare Backend — Django REST API dev server
# Uses Python 3.12 to run the Django dev server on :8000
# Build & run:  docker compose up --build
# -------------------------------------------------------
FROM python:3.12-slim

# Prevent Python from writing .pyc files and enable unbuffered output
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Install system dependencies required by some Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first for layer caching
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the backend source code
COPY . .

# Collect static files for whitenoise (--noinput avoids interactive prompts)
RUN python manage.py collectstatic --noinput 2>/dev/null || true

EXPOSE 8000

# Run Django dev server bound to all interfaces so Docker can forward the port
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
