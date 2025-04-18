# Web Push Notify

A simple project to implement web push notifications.

## Features

- Send push notifications to users.
- Support for subscription management.
- Easy integration with web applications.

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/your-username/web-push-notify.git
    ```
2. Navigate to the project directory:
    ```bash
    cd web-push-notify
    ```
3. Run with docker:
    ```bash
    docker-compose up --build
    ```

## Usage

1. Open your browser and navigate to `http://localhost:8080`.

2. Click on Subscribe button.

3. Send a POST request on `localhost:8000/notifications/publish`.
With a header with key: Content-Type and value: application/json.
The body of the POST request being:
{
  "title": "Test Notification",
  "body": "This is the test message being received!",
  "image_url": "",
  "action_url": "https://example.com"
}

4. Run rabbitmq_consumer.py to push the notification.

## Configuration

- Update the `config.js.sample` file in frontend folder with your VAPID keys and other settings, and rename it as `config.js`. It is found under Project settings >> General >> SDK setup and configuration.

- Get private key from Project Settings >> Service Accounts >> Generate a new private Key. Rename it as serviceAccountKey.json and place it in backend directory.
