// MQTT variables, one for names one for values.
var MQTTmotorrpm = ["FMotorRPM","RMotorRPM"];
var MQTTmotorrpmvalues = [0,0];
var MQTTpercentage = ["FMotorEff","RMotorEff","TorqueBias","WattPedal"];
var MQTTpercentagevalues = [0,0,0,0];
var MQTTpower1 = ["PropulsionkW","HPUsageComb"];
var MQTTpowervalues1 = [0,0];
var MQTTspeed1 = ["Speed"];
var MQTTspeedvalues1 = [0];
var MQTTsteering1 = ["Steeringangle"];
var MQTTsteeringvalues1 = [0];


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

        var chart1 = new google.visualization.Gauge(document.getElementById('chart_div'));

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

        var chart2 = new google.visualization.Gauge(document.getElementById('chart_div2'));

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
        
        var chart3 = new google.visualization.Gauge(document.getElementById('chart_div3'));
        
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
            width: 280, height: 280,
            greenFrom: 0, greenTo: 140,
            yellowFrom: 140, yellowTo: 200,
            redFrom: 200, redTo: 250,
            minorTicks: 0, max: 250,
            animation:{
            duration: 0,
            easing: 'linear',
        },
            
        };
        
        var chart4 = new google.visualization.Gauge(document.getElementById('chart_div4'));
        
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
            width: 280, height: 280,
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
        
        var chart5 = new google.visualization.Gauge(document.getElementById('chart_div5'));
        
        chart5.draw(data5, options5);
        
        setInterval(function() {
        for (var i=0; i < MQTTsteering1.length; i++) {
        data5.setValue(i, 1, MQTTsteeringvalues1[i]);
        }
            chart5.draw(data5, options5);
        
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
}
// called when a message arrives
