# Use a lightweight Python base image
FROM python:3.13-slim

# Set the working directory inside the container as
WORKDIR /app

# Add a non-root user
RUN useradd --create-home appuser

# Copy dependencies file and install them
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the application source code
COPY backend/src /app/backend/src

# Copy Makefile
COPY Makefile /app/Makefile

# Install make (requires root)
RUN apt update \
    && apt install -y --no-install-recommends make \
    && apt clean \
    && rm -rf /var/lib/apt/lists/* /var/cache/apt/archives/*

# Switch to newly created non-root user for better security
USER appuser

# Expose ports for the service
EXPOSE 8000 5678

# Specify python path
ENV PYTHONPATH=/app

# Run the server
CMD ["python", "-m", "backend.src.rpc_api.server"]
