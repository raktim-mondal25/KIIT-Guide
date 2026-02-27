package com.kiit.guide;

import android.Manifest;
import android.app.NotificationChannel;
import android.app.NotificationManager;
import android.content.Context;
import android.content.pm.PackageManager;
import android.location.Location;

import androidx.annotation.NonNull;
import androidx.core.app.ActivityCompat;
import androidx.core.app.NotificationCompat;
import androidx.work.Worker;
import androidx.work.WorkerParameters;

import com.google.android.gms.location.FusedLocationProviderClient;
import com.google.android.gms.location.LocationServices;
import com.google.android.gms.tasks.Tasks;



public class CampusGeofenceWorker extends Worker {

    private static final double KIIT_LAT = 20.35380253557167;
    private static final double KIIT_LNG = 85.81989100774194;

    // KEEP 300m (50m WILL FAIL — GPS accuracy)
    private static final float RADIUS = 300f;

    public CampusGeofenceWorker(@NonNull Context context, @NonNull WorkerParameters params) {
        super(context, params);
    }

    @NonNull
    @Override
    public Result doWork() {

        // Check permission
        if (ActivityCompat.checkSelfPermission(getApplicationContext(),
                Manifest.permission.ACCESS_FINE_LOCATION) != PackageManager.PERMISSION_GRANTED) {
            return Result.success();
        }

        FusedLocationProviderClient client =
                LocationServices.getFusedLocationProviderClient(getApplicationContext());

        try {
            Location location = Tasks.await(client.getLastLocation());

            if (location == null)
                return Result.success();

            double userLat = location.getLatitude();
            double userLng = location.getLongitude();

            float[] results = new float[1];
            Location.distanceBetween(userLat, userLng, KIIT_LAT, KIIT_LNG, results);

            float distance = results[0];

            if (distance <= RADIUS) {
                sendNotification();
            }

        } catch (Exception e) {
            e.printStackTrace();
        }

        return Result.success();
    }

    private void sendNotification() {

        NotificationManager manager =
                (NotificationManager) getApplicationContext()
                        .getSystemService(Context.NOTIFICATION_SERVICE);

        String channelId = "KIIT_GEOFENCE";

        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.O) {
            NotificationChannel channel = new NotificationChannel(
                    channelId,
                    "KIIT Alerts",
                    NotificationManager.IMPORTANCE_HIGH
            );
            manager.createNotificationChannel(channel);
        }

        NotificationCompat.Builder builder =
                new NotificationCompat.Builder(getApplicationContext(), channelId)
                        .setSmallIcon(android.R.drawable.ic_dialog_map)
                        .setContentTitle("KIIT Guide")
                        .setContentText("You entered KIIT Campus 📍")
                        .setPriority(NotificationCompat.PRIORITY_HIGH);

        manager.notify(1001, builder.build());
    }
}