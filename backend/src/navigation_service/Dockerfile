# Use a lightweight Python base image
FROM python:3.13-slim

# Set the working directory inside the container as
WORKDIR /app

# Copy dependencies file and install them
COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/requirements.txt

# Copy the application source code
COPY backend/src /app/backend/src

# Copy Makefile
COPY Makefile /app/Makefile

# Install make
RUN apt update && apt install -y make

# Expose ports for the service
EXPOSE 8000 5678

# Specify python path
ENV PYTHONPATH=backend/

# Run the server
CMD ["python", "-m", "backend.src.rpc_api.server"]
