FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir fastapi uvicorn sqlmodel psycopg[binary] pydantic-settings

# Copy shared code (context is services/)
COPY shared /app/shared

# Copy service files (context is services/)
COPY appointments-service /app/

# Expose port
EXPOSE 8001

# Run the service
CMD ["python", "main.py"]
