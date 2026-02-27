import { Geolocation } from '@capacitor/geolocation';
import { LocalNotifications } from '@capacitor/local-notifications';

const KIIT = {
    lat: 20.356873000543768,
    lng: 85.82012030142747,
    radius: 250
};

let inside = null;

function distance(lat1, lon1, lat2, lon2) {
    const R = 6371000;
    const toRad = x => x * Math.PI / 180;

    const dLat = toRad(lat2 - lat1);
    const dLon = toRad(lon2 - lon1);

    const a =
        Math.sin(dLat / 2) ** 2 +
        Math.cos(toRad(lat1)) *
        Math.cos(toRad(lat2)) *
        Math.sin(dLon / 2) ** 2;

    return R * 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
}

async function checkLocation() {
    const pos = await Geolocation.getCurrentPosition({
        enableHighAccuracy: true
    });

    const d = distance(
        pos.coords.latitude,
        pos.coords.longitude,
        KIIT.lat,
        KIIT.lng
    );

    const nowInside = d <= KIIT.radius;

    if (inside === null) {
        inside = nowInside;
        return;
    }

    if (!inside && nowInside) {
        inside = true;
        LocalNotifications.schedule({
            notifications: [{
                title: "Welcome to KIIT Campus 🎓",
                body: "You have entered KIIT campus area",
                id: 1,
                schedule: { at: new Date(Date.now() + 1000) }
            }]
        });
    }

    if (inside && !nowInside) {
        inside = false;
        LocalNotifications.schedule({
            notifications: [{
                title: "Leaving KIIT Campus",
                body: "You exited KIIT campus",
                id: 2,
                schedule: { at: new Date(Date.now() + 1000) }
            }]
        });
    }
}

setInterval(checkLocation, 60000);