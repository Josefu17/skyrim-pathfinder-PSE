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

# Run the backend controller and keep the container running
CMD sh -c "export PYTHONPATH=$(pwd) && python -m backend.src.web_backend.web_backend_controller && tail -f /dev/null"
