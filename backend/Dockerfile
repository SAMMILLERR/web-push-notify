# backend/Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the backend code
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose the backend port
EXPOSE 8000

# Run both the backend server and the RabbitMQ consumer
CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port 8000"]