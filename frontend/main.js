// frontend/main.js

(async () => {
  try {
    // Fetch the configuration file
    const response = await fetch('/etc/secrets/config.js');
    if (!response.ok) {
      throw new Error(`Failed to load config.js: ${response.statusText}`);
    }

    // Parse the configuration
    const config = await response.json();
    window.env = config;

    // Initialize Firebase
    firebase.initializeApp(window.env.firebaseConfig);
    const messaging = firebase.messaging();

    // Register the service worker
    if ('serviceWorker' in navigator) {
      navigator.serviceWorker
        .register('firebase-messaging-sw.js')
        .then(registration => {
          console.log("Service Worker registered:", registration.scope);
          window.swRegistration = registration;
        })
        .catch(err => {
          console.error("Service Worker registration failed:", err);
        });
    } else {
      console.warn("Service Workers not supported.");
    }

    // Add event listener for the subscribe button
    document.getElementById("subscribeBtn").addEventListener("click", async () => {
      const statusElem = document.getElementById("status");
      try {
        const permission = await Notification.requestPermission();
        if (permission !== "granted") {
          statusElem.textContent = "Status: Notification permission denied.";
          return;
        }

        const token = await messaging.getToken({
          vapidKey: window.env.firebaseConfig.vapidKey,
          serviceWorkerRegistration: window.swRegistration
        });

        if (!token) {
          statusElem.textContent = "Status: Failed to receive token.";
          return;
        }

        // Send token to backend
        const res = await fetch(
          `${window.env.backendUrl}/devices/register`,
          {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ fcm_token: token })
          }
        );

        const data = await res.json();
        if (res.ok) {
          statusElem.textContent = `Status: Subscribed (${data.total_tokens} tokens)`;
        } else {
          statusElem.textContent = `Status: Registration error: ${data.detail || "Unknown error"}`;
        }

      } catch (err) {
        console.error("Subscription error:", err);
        statusElem.textContent = "Status: Error during subscription.";
      }
    });

  } catch (err) {
    console.error("Error loading configuration:", err);
  }
})();
