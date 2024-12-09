# Use a lightweight Python base image
FROM python:3.13-slim

# Set the working directory inside the container
WORKDIR /app

# Add a non-root user
RUN useradd --create-home appuser

# Copy dependencies file and install them
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir --upgrade pip && \
    pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy the application source code
COPY backend/src /app/backend/src

# Copy alembic.ini for database migration
COPY backend/alembic.ini /app/backend/alembic.ini

# Copy environment variables file
COPY .env /app/.env

# Switch to newly created non-root user for better security
USER appuser

# Expose ports for the service
EXPOSE 4243 5678

# Specify python path
ENV PYTHONPATH=/app

# Run migrate db first by running alembic upgrade and then start the web backend controller
CMD ["sh", "-c", "\
    alembic -c backend/alembic.ini upgrade head && \
    python -m backend.src.web_backend.web_backend_controller"]
