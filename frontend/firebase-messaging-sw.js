// frontend/firebase-messaging-sw.js

importScripts('https://www.gstatic.com/firebasejs/9.6.7/firebase-app-compat.js');
importScripts('https://www.gstatic.com/firebasejs/9.6.7/firebase-messaging-compat.js');

(async () => {
  try {
    // Fetch the configuration file
    const response = await fetch('/etc/secrets/config.js');
    if (!response.ok) {
      throw new Error(`Failed to load config.js: ${response.statusText}`);
    }

    // Parse the configuration
    const config = await response.json();

    // Initialize Firebase
    firebase.initializeApp(config.firebaseConfig);

    const messaging = firebase.messaging();
    messaging.onBackgroundMessage(payload => {
      const { title, body } = payload.notification;
      self.registration.showNotification(title, { body, icon: '/firebase-logo.png' });
    });
  } catch (err) {
    console.error('Error loading Firebase configuration in service worker:', err);
  }
})();
