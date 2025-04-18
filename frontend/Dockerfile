# frontend/Dockerfile (place inside ./frontend folder)
FROM nginx:alpine

# Remove default nginx content (optional)
RUN rm -rf /usr/share/nginx/html/*

# Copy your static files (index.html, main.js, firebase-messaging-sw.js, etc.)
COPY . /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80