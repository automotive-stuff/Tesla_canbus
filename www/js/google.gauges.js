// MQTT variables, one for names one for values.
var MQTTname1 = ["fmotorrpm","rmtorrpm"];
var MQTTvalues1 = [0,0];
var MQTTname2 = ["frefficiency","rrefficiency","rrfrtorquebias","wattpedal"];
var MQTTvalues2 = [0,0,0,0];
var MQTTname3 = ["propulsion","hpcombined"];
var MQTTvalues3 = [0,0];
var MQTTname4 = ["speed"];
var MQTTvalues4 = [0];
var MQTTname5 = ["steeringangle"];
var MQTTvalues5 = [0];
var MQTTname6 = ["batteryvoltage","batterycurrent","batterypower","consumption"];
var MQTTvalues6 = [0,0,0,0];
var MQTTname7 = ["dcdccurrent","rrstatorcurrent","frstatorcurrent","dcdcefficiency"];
var MQTTvalues7 = [0,0,0,0];
var MQTTname7 = ["dcdccoolantinlet","rrcoolantinlettemp","rrinverterpcbtemp","rrstatortemp","rrdccapacitortemp","rrheatsinktemp","rrinvertertemp","coolant"];
var MQTTvalues7 = [0,0,0,0,0,0,0,0];

// GUAGES, Further down is LineCharts!
//Define the Gauge for MOTOR RPM.
        google.charts.load('current', {'packages':['gauge']});
        google.charts.setOnLoadCallback(drawChart);

        function drawChart() {

        var data1 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname1[0], MQTTvalues1[0]],
        [MQTTname1[1], MQTTvalues1[1]],      
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
        for (var i=0; i < MQTTname1.length; i++) {
        data1.setValue(i, 1, MQTTvalues1[i]);
        }
            chart1.draw(data1, options1);

        }, 0);
//Define the charts for DC-DC,
        var data2 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname2[0], MQTTvalues2[0]],
        [MQTTname2[1], MQTTvalues2[1]],
        [MQTTname2[2], MQTTvalues2[2]],
        [MQTTname2[3], MQTTvalues2[3]],      
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
        for (var i=0; i < MQTTname2.length; i++) {
        data2.setValue(i, 1, MQTTvalues2[i]);
        }
            chart2.draw(data2, options2);

        }, 0);
        // Define charts for powerdelivery
        var data3 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname3[0], MQTTvalues3[0]],
        [MQTTname3[1], MQTTvalues3[1]],      
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
        for (var i=0; i < MQTTname3.length; i++) {
        data3.setValue(i, 1, MQTTvalues3[i]);
        }
            chart3.draw(data3, options3);
        
        }, 1);
        // SPEED GAUGE! ONLY ONE
        var data4 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname4[0], MQTTvalues4[0]],     
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
        for (var i=0; i < MQTTname4.length; i++) {
        data4.setValue(i, 1, MQTTvalues4[i]);
        }
            chart4.draw(data4, options4);
        
        }, 0);
        //STEERINGWHEEL
        var data5 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname5[0], MQTTvalues5[0]],     
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
        for (var i=0; i < MQTTname5.length; i++) {
        data5.setValue(i, 1, MQTTvalues5[i]);
        }
            chart5.draw(data5, options5);
        
        }, 0);
        var data6 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname6[0], MQTTvalues6[0]],
        [MQTTname6[1], MQTTvalues6[1]],
        [MQTTname6[2], MQTTvalues6[2]],
        [MQTTname6[3], MQTTvalues6[3]],     
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
        for (var i=0; i < MQTTname6.length; i++) {
        data6.setValue(i, 1, MQTTvalues6[i]);
        }
            chart6.draw(data6, options6);
        
        }, 0);
        var data7 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname7[0], MQTTvalues7[0]],
        [MQTTname7[1], MQTTvalues7[1]],
        [MQTTname7[2], MQTTvalues7[2]],
        [MQTTname7[3], MQTTvalues7[3]],     
        ]);
        
        var options7 = {
            width: 280, height: 280,
            greenFrom: 10, greenTo: 60,
            yellowFrom: -20, yellowTo: 10,
            redFrom: 60, redTo: 100,
            minorTicks: 5, max: 100, min: -20,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart7 = new google.visualization.Gauge(document.getElementById('chart_current1'));
        
        chart7.draw(data7, options7);
        
        setInterval(function() {
        for (var i=0; i < MQTTname7.length; i++) {
        data7.setValue(i, 1, MQTTvalues7[i]);
        }
            chart7.draw(data7, options7);
        
        }, 0);
        var data8 = google.visualization.arrayToDataTable([
            ['Label', 'Value'], 
        [MQTTname7[0], MQTTvalues7[0]],
        [MQTTname7[1], MQTTvalues7[1]],
        [MQTTname7[2], MQTTvalues7[2]],
        [MQTTname7[3], MQTTvalues7[3]],
        [MQTTname7[4], MQTTvalues7[4]],
        [MQTTname7[5], MQTTvalues7[5]],
        [MQTTname7[6], MQTTvalues7[6]],
        [MQTTname7[7], MQTTvalues7[7]],      
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
        for (var i=0; i < MQTTname7.length; i++) {
        data8.setValue(i, 1, MQTTvalues7[i]);
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
    
    for (var i=0; i < MQTTname1.length; i++) {
    if (message.destinationName == MQTTname1[i]) {
    MQTTvalues1[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname2.length; i++) {
    if (message.destinationName == MQTTname2[i]) {
    MQTTvalues2[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname3.length; i++) {
    if (message.destinationName == MQTTname3[i]) {
    MQTTvalues3[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname4.length; i++) {
    if (message.destinationName == MQTTname4[i]) {
    MQTTvalues4[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname5.length; i++) {
    if (message.destinationName == MQTTname5[i]) {
    MQTTvalues5[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname6.length; i++) {
    if (message.destinationName == MQTTname6[i]) {
    MQTTvalues6[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname7.length; i++) {
    if (message.destinationName == MQTTname7[i]) {
    MQTTvalues7[i] = Number(message.payloadString);
    }
    }
    for (var i=0; i < MQTTname7.length; i++) {
    if (message.destinationName == MQTTname7[i]) {
    MQTTvalues7[i] = Number(message.payloadString);
    }
    }
}
function onConnect() {
    // Once a connection has been made, make a subscription and send a message.
    for (var i=0; i < MQTTname1.length; i++) {
    client.subscribe(MQTTname1[i]);
    }
    for (var i=0; i < MQTTname2.length; i++) {
    client.subscribe(MQTTname2[i]);
    }
    for (var i=0; i < MQTTname3.length; i++) {
    client.subscribe(MQTTname3[i]);
    }
    for (var i=0; i < MQTTname4.length; i++) {
    client.subscribe(MQTTname4[i]);
    }
    for (var i=0; i < MQTTname5.length; i++) {
    client.subscribe(MQTTname5[i]);
    }
    for (var i=0; i < MQTTname6.length; i++) {
    client.subscribe(MQTTname6[i]);
    }
    for (var i=0; i < MQTTname7.length; i++) {
    client.subscribe(MQTTname7[i]);
    }
    for (var i=0; i < MQTTname7.length; i++) {
    client.subscribe(MQTTname7[i]);
    }
}
// called when a message arrives