package com.example.kaijie.ehit;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.Viewport;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

import java.util.Random;

public class baselineActivity extends AppCompatActivity {

    private LineGraphSeries<DataPoint> series;
    private static final Random RANDOM = new Random();
    private int lastX=0;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_baseline);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);


        GraphView graph = (GraphView) findViewById(R.id.baselinePlot);
        series = new LineGraphSeries<DataPoint>();
        graph.addSeries(series);

        Viewport viewport=graph.getViewport();
        viewport.setYAxisBoundsManual(true);
        viewport.setMinY(0);
        viewport.setMaxY(10);
        viewport.setScrollable(true);

    }

    @Override
    protected void onResume() {
        super.onResume();
        // Simulate real-time with thread that appends data to graph
        new Thread(new Runnable(){
            @Override
            public void run(){
                // Add 100 new entries
                for (int i=0;i<100;i++){
                    runOnUiThread(new Runnable() {
                        @Override
                        public void run() {
                            addEntry();

                        }
                    });
                    // Sleep to slow down entries
                    try {
                        Thread.sleep(500);
                    } catch (InterruptedException e) {
                        //e.printStackTrace();
                    }
                }
            }

        }).start();

    }

    // Add random data to graph
    private void addEntry(){
        series.appendData(new DataPoint(lastX++,RANDOM.nextDouble()*10d),true,10);

    }


}


