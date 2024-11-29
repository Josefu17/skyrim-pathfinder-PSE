# Use a lightweight Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file and install them
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the application source code
COPY backend/src /app/backend/src

# Copy environment variables file
COPY backend/env/.env /app/backend/env/.env

# Expose ports for the service
EXPOSE 4243 5678

# Specify python path
ENV PYTHONPATH=backend/

# Run the backend controller
CMD ["python", "-m", "backend.src.web_backend.web_backend_controller"]
