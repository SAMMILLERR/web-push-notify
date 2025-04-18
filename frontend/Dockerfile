# frontend/Dockerfile (place inside ./frontend folder)
FROM nginx:alpine

# Remove default nginx content (optional)
RUN rm -rf /usr/share/nginx/html/*

# Copy your static files (index.html, main.js, firebase-messaging-sw.js, etc.)
COPY /etc/secrets/config.js /usr/share/nginx/html/config.js
COPY . /usr/share/nginx/html

# Expose HTTP port
EXPOSE 80