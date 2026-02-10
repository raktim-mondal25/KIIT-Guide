package com.kiit.guide;

import android.os.Bundle;
import android.webkit.WebView;
import com.getcapacitor.BridgeActivity;

public class MainActivity extends BridgeActivity {
    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        // 🔥 IMPORTANT: Enable WebView debugging
        WebView.setWebContentsDebuggingEnabled(true);
    }
}
