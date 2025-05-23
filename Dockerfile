# Stage 1: Build the frontend
FROM nginx:alpine as frontend-builder

WORKDIR /app/frontend
COPY ./frontend ./

# Stage 2: Backend setup
FROM python:3.9-slim as backend-builder

WORKDIR /app/backend
COPY ./backend/requirements.txt ./
RUN pip install -r requirements.txt
COPY ./backend ./

# Stage 3: Final image
FROM python:3.9-slim

# Install Nginx
RUN apt-get update && apt-get install -y nginx && apt-get clean

# Copy built frontend files
COPY --from=frontend-builder /app/frontend /usr/share/nginx/html

# Copy backend files
COPY --from=backend-builder /app/backend /app/backend
COPY --from=backend-builder /usr/local/lib/python3.9/site-packages /usr/local/lib/python3.9/site-packages
COPY --from=backend-builder /usr/local/bin /usr/local/bin

# Copy nginx configuration (optional)
#COPY ./nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 8000

# Start both frontend and backend
CMD ["sh", "-c", "nginx && uvicorn app.backend.main:app --host 0.0.0.0 --port 8000"]