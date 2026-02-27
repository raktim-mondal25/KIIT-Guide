package com.kiit.guide;
import android.app.Application;
import androidx.work.PeriodicWorkRequest;
import androidx.work.WorkManager;
import java.util.concurrent.TimeUnit;


public class App extends Application {

    @Override
    public void onCreate() {
        super.onCreate();

        PeriodicWorkRequest locationWork =
                new PeriodicWorkRequest.Builder(
                        CampusGeofenceWorker.class,
                        15,
                        TimeUnit.MINUTES
                ).build();

        WorkManager.getInstance(this).enqueue(locationWork);
    }
}