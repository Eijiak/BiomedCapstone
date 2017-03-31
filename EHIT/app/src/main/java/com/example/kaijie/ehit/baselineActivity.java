package com.example.kaijie.ehit;

import android.os.Bundle;
import android.support.design.widget.FloatingActionButton;
import android.support.design.widget.Snackbar;
import android.support.v7.app.AppCompatActivity;
import android.support.v7.widget.Toolbar;
import android.view.View;

import com.jjoe64.graphview.GraphView;
import com.jjoe64.graphview.series.DataPoint;
import com.jjoe64.graphview.series.LineGraphSeries;

public class baselineActivity extends AppCompatActivity {

    LineGraphSeries<DataPoint> series;

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_baseline);
        Toolbar toolbar = (Toolbar) findViewById(R.id.toolbar);
        setSupportActionBar(toolbar);


        double x,y;
        x=-5;
        GraphView graph = (GraphView) findViewById(R.id.baselinePlot);
        series = new LineGraphSeries<DataPoint>();
        for (int i=0; i<500;i++){
            x=x+0.1;
            y=Math.sin(x);
            series.appendData(new DataPoint(x,y),true,500);
        }
        graph.addSeries(series);
    }


}


