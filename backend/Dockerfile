# python:3.12-slim instead of full python:3.12 — reduces image size by ~700MB
# since we don't need compilers or system tools in production
FROM python:3.12-slim

# Prevents Python from writing .pyc files — not needed in containers
# since the container is always fresh on startup
ENV PYTHONDONTWRITEBYTECODE=1

# netcat is used in docker-compose to wait for PostgreSQL to be ready
# before running migrations and starting the server
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*

# Forces stdout/stderr to flush immediately — ensures logs appear
# in real time in Docker and Kubernetes instead of being buffered
ENV PYTHONUNBUFFERED=1

# All app code lives here — standard convention for containerized apps
WORKDIR /app

# Copy requirements first, before the rest of the code.
# Docker builds in layers — if requirements.txt hasn't changed,
# Docker reuses the cached layer and skips reinstalling dependencies.
# This makes rebuilds much faster during development.
COPY requirements.txt .

# --no-cache-dir avoids storing pip's download cache inside the image,
# keeping the final image smaller
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the code after installing dependencies,
# so code changes don't invalidate the dependency cache layer
COPY . .