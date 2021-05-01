// MQTT variables, one for names one for values.
var MQTTmotorrpm = ["fmotorrpm","rmtorrpm"];
var MQTTmotorrpmvalues = [0,0];
var MQTTpercentage = ["frefficiency","rrefficiency","rrfrtorquebias","wattpedal"];
var MQTTpercentagevalues = [0,0,0,0];
var MQTTpower1 = ["propulsion","hpcombined"];
var MQTTpowervalues1 = [0,0];
var MQTTspeed1 = ["speed"];
var MQTTspeedvalues1 = [0];
var MQTTsteering1 = ["steeringangle"];
var MQTTsteeringvalues1 = [0];
var MQTTBattery1 = ["batteryvoltage","batterycurrent","batterypower","consumption"];
var MQTTBatteryvalues1 = [0,0,0,0];
var MQTTCurrent1 = ["dcdccurrent","rrstatorcurrent","frstatorcurrent","dcdcefficiency"];
var MQTTCurrentvalues1 = [0,0,0,0];
var MQTTTemp1 = ["dcdccoolantinlet","rrcoolantinlettemp","rrinverterpcbtemp","rrstatortemp","rrdccapacitortemp","rrheatsinktemp","rrinvertertemp","coolant"];
var MQTTTempvalues1 = [0,0,0,0,0,0,0,0];

// GUAGES, Further down is LineCharts!
//Define the Gauge for MOTOR RPM.
        google.charts.load('current', {'packages':['gauge']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {

        var data1 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTmotorrpm[0], MQTTmotorrpmvalues[0]],
        [MQTTmotorrpm[1], MQTTmotorrpmvalues[1]],      
        ]);

        var options1 = {
            width: 380, height: 380,
            redFrom: 16000, redTo: 20000,
            yellowFrom: 14000, yellowTo: 16000,
            minorTicks: 5, max: 20000,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };

        var chart1 = new google.visualization.Gauge(document.getElementById('chart_motorrpm'));

        chart1.draw(data1, options1);

        setInterval(function() {
        for (var i=0; i < MQTTmotorrpm.length; i++) {
        data1.setValue(i, 1, MQTTmotorrpmvalues[i]);
        }
            chart1.draw(data1, options1);

        }, 0);
//Define the charts for DC-DC,
        var data2 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTpercentage[0], MQTTpercentagevalues[0]],
        [MQTTpercentage[1], MQTTpercentagevalues[1]],
        [MQTTpercentage[2], MQTTpercentagevalues[2]],
        [MQTTpercentage[3], MQTTpercentagevalues[3]],      
        ]);

        var options2 = {
            width: 280, height: 280,
            greenFrom: 70, greenTo: 100,
            yellowFrom: 20, yellowTo: 70,
            redFrom: 0, redTo: 20,
            minorTicks: 5, max: 100,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };

        var chart2 = new google.visualization.Gauge(document.getElementById('chart_motorefficiency'));

        chart2.draw(data2, options2);

        setInterval(function() {
        for (var i=0; i < MQTTpercentage.length; i++) {
        data2.setValue(i, 1, MQTTpercentagevalues[i]);
        }
            chart2.draw(data2, options2);

        }, 0);
        // Define charts for powerdelivery
        var data3 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTpower1[0], MQTTpowervalues1[0]],
        [MQTTpower1[1], MQTTpowervalues1[1]],      
        ]);
        
        var options3 = {
            width: 380, height: 380,
            greenFrom: 0, greenTo: 100,
            yellowFrom: 100, yellowTo: 200,
            redFrom: 200, redTo: 400,
            minorTicks: 0, max: 400,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart3 = new google.visualization.Gauge(document.getElementById('chart_propulsion'));
        
        chart3.draw(data3, options3);
        
        setInterval(function() {
        for (var i=0; i < MQTTpower1.length; i++) {
        data3.setValue(i, 1, MQTTpowervalues1[i]);
        }
            chart3.draw(data3, options3);
        
        }, 1);
        // SPEED GAUGE! ONLY ONE
        var data4 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTspeed1[0], MQTTspeedvalues1[0]],     
        ]);
        
        var options4 = {
            width: 380, height: 380,
            greenFrom: 0, greenTo: 140,
            yellowFrom: 140, yellowTo: 200,
            redFrom: 200, redTo: 250,
            minorTicks: 0, max: 250,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart4 = new google.visualization.Gauge(document.getElementById('chart_speed'));
        
        chart4.draw(data4, options4);
        
        setInterval(function() {
        for (var i=0; i < MQTTspeed1.length; i++) {
        data4.setValue(i, 1, MQTTspeedvalues1[i]);
        }
            chart4.draw(data4, options4);
        
        }, 0);
        //STEERINGWHEEL
        var data5 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTsteering1[0], MQTTsteeringvalues1[0]],     
        ]);
        
        var options5 = {
            width: 380, height: 380,
            greenFrom: -360, greenTo: 360,
            yellowFrom: 360, yellowTo: 425,
            blueFrom: 100, blueTo: 150,
            redFrom: -425, redTo: -360,
            minorTicks: 0, max: 425, min: -425,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart5 = new google.visualization.Gauge(document.getElementById('chart_steeringangle'));
        
        chart5.draw(data5, options5);
        
        setInterval(function() {
        for (var i=0; i < MQTTsteering1.length; i++) {
        data5.setValue(i, 1, MQTTsteeringvalues1[i]);
        }
            chart5.draw(data5, options5);
        
        }, 0);
        var data6 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTBattery1[0], MQTTBatteryvalues1[0]],
        [MQTTBattery1[1], MQTTBatteryvalues1[1]],
        [MQTTBattery1[2], MQTTBatteryvalues1[2]],
        [MQTTBattery1[3], MQTTBatteryvalues1[3]],     
        ]);
        
        var options6 = {
            width: 280, height: 280,
            greenFrom: 0, greenTo: 100,
            yellowFrom: 100, yellowTo: 200,
            redFrom: 200, redTo: 400,
            minorTicks: 5, max: 400,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart6 = new google.visualization.Gauge(document.getElementById('chart_battery1'));
        
        chart6.draw(data6, options6);
        
        setInterval(function() {
        for (var i=0; i < MQTTBattery1.length; i++) {
        data6.setValue(i, 1, MQTTBatteryvalues1[i]);
        }
            chart6.draw(data6, options6);
        
        }, 0);
        var data7 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTCurrent1[0], MQTTCurrentvalues1[0]],
        [MQTTCurrent1[1], MQTTCurrentvalues1[1]],
        [MQTTCurrent1[2], MQTTCurrentvalues1[2]],
        [MQTTCurrent1[3], MQTTCurrentvalues1[3]],     
        ]);
        
        var options7 = {
            width: 280, height: 280,
            greenFrom: 0, greenTo: 100,
            yellowFrom: 100, yellowTo: 200,
            redFrom: 200, redTo: 400,
            minorTicks: 5, max: 400,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart7 = new google.visualization.Gauge(document.getElementById('chart_current1'));
        
        chart7.draw(data7, options7);
        
        setInterval(function() {
        for (var i=0; i < MQTTCurrent1.length; i++) {
        data7.setValue(i, 1, MQTTCurrentvalues1[i]);
        }
            chart7.draw(data7, options7);
        
        }, 0);
        var data8 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTTemp1[0], MQTTTempvalues1[0]],
        [MQTTTemp1[1], MQTTTempvalues1[1]],
        [MQTTTemp1[2], MQTTTempvalues1[2]],
        [MQTTTemp1[3], MQTTTempvalues1[3]],
        [MQTTTemp1[4], MQTTTempvalues1[4]],
        [MQTTTemp1[5], MQTTTempvalues1[5]],
        [MQTTTemp1[6], MQTTTempvalues1[6]],
        [MQTTTemp1[7], MQTTTempvalues1[7]],      
        ]);
        
        var options8 = {
            width: 700, height: 300,
            greenFrom: 0, greenTo: 55,
            yellowFrom: 55, yellowTo: 70,
            redFrom: 70, redTo: 100,
            minorTicks: 5, max: 100,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart8 = new google.visualization.Gauge(document.getElementById('chart_temp1'));
        
        chart8.draw(data8, options8);
        
        setInterval(function() {
        for (var i=0; i < MQTTTemp1.length; i++) {
        data8.setValue(i, 1, MQTTTempvalues1[i]);
        }
            chart8.draw(data8, options8);
        
        }, 0);
        
        
    }

// Create a client instance
client = new Paho.MQTT.Client(window.location.hostname, 80,"");
client.onMessageArrived = onMessageArrived;

// connect the client
client.connect({onSuccess:onConnect});

// called when the client connects
function onMessageArrived(message) {
    
    for (var i=0; i < MQTTmotorrpm.length; i++) {
    if (message.destinationName == MQTTmotorrpm[i]) {
    MQTTmotorrpmvalues[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTpercentage.length; i++) {
    if (message.destinationName == MQTTpercentage[i]) {
    MQTTpercentagevalues[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTpower1.length; i++) {
    if (message.destinationName == MQTTpower1[i]) {
    MQTTpowervalues1[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTspeed1.length; i++) {
    if (message.destinationName == MQTTspeed1[i]) {
    MQTTspeedvalues1[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTsteering1.length; i++) {
    if (message.destinationName == MQTTsteering1[i]) {
    MQTTsteeringvalues1[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTBattery1.length; i++) {
    if (message.destinationName == MQTTBattery1[i]) {
    MQTTBatteryvalues1[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTCurrent1.length; i++) {
    if (message.destinationName == MQTTCurrent1[i]) {
    MQTTCurrentvalues1[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTTemp1.length; i++) {
    if (message.destinationName == MQTTTemp1[i]) {
    MQTTTempvalues1[i] = Number(message.payloadString);
    }
    }
}
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    for (var i=0; i < MQTTmotorrpm.length; i++) {
    client.subscribe(MQTTmotorrpm[i]);
    }
    for (var i=0; i < MQTTpercentage.length; i++) {
    client.subscribe(MQTTpercentage[i]);
    }
    for (var i=0; i < MQTTpower1.length; i++) {
    client.subscribe(MQTTpower1[i]);
    }
    for (var i=0; i < MQTTspeed1.length; i++) {
    client.subscribe(MQTTspeed1[i]);
    }
    for (var i=0; i < MQTTsteering1.length; i++) {
    client.subscribe(MQTTsteering1[i]);
    }
    for (var i=0; i < MQTTBattery1.length; i++) {
    client.subscribe(MQTTBattery1[i]);
    }
    for (var i=0; i < MQTTCurrent1.length; i++) {
    client.subscribe(MQTTCurrent1[i]);
    }
    for (var i=0; i < MQTTTemp1.length; i++) {
    client.subscribe(MQTTTemp1[i]);
    }
}
// called when a message arrives