self.addEventListener("install", (event) => {
    console.log("Service Worker installed");
    self.skipWaiting();
});

self.addEventListener("activate", (event) => {
    console.log("Service Worker activated");
});

self.addEventListener("notificationclick", (event) => {
    event.notification.close();
    event.waitUntil(
        clients.openWindow("/")
    );
});