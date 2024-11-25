# Use a lightweight Python base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy dependencies file and install them
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the application source code
COPY /backend/src /app/backend/src

# Copy Makefile
COPY Makefile /app/Makefile

# Copy environment variables file
COPY /backend/env/.env /app/backend/env/.env

# Install make
RUN apt update && apt install -y make

# Expose ports for the service
EXPOSE 8000 5678

# Run the server and keep the container running
CMD sh -c "export PYTHONPATH=$(pwd) && python -m backend.src.rpc_api.server && tail -f /dev/null"
