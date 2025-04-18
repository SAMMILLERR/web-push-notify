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
FROM nginx:alpine

RUN apk add --no-cache python3 py3-pip

# Install Uvicorn + FastAPI
RUN pip3 install --no-cache-dir uvicorn fastapi firebase-admin

# Copy built frontend files
COPY --from=frontend-builder /app/frontend /usr/share/nginx/html

# Copy backend files
COPY --from=backend-builder /app/backend /app/backend

# Copy nginx configuration (optional)
#COPY ./nginx.conf /etc/nginx/nginx.conf

# Expose ports
EXPOSE 80 8000

# Start both frontend and backend
CMD ["sh", "-c", "nginx && uvicorn /app/backend/main:app --host 0.0.0.0 --port 8000"]