// TO_PI TOPIC MESSAGES
const SPEECH_TRIGGER = 0;
const TIME_SET = 1;
const ASK_RESULTS = 2;
// TO_APP TOPIC MESSAGES
const START_ALARM = 0;
const STOP_ALARM = 1;
const RESULTS = 2;

var audio = document.getElementById('alarm');
var temperatureData;

//var audio = document.getElementById('alarm')

var client = mqtt.connect('mqtt://test.mosquitto.org:8080');

client.on('connect', function () {
    console.log('connected to MQTT!');
    client.subscribe('IC.embedded/tEEEm/TO_APP', function (err) {
        if(!err){
            console.log('subscribed to TO_APP successfully!');
        }
    });
});

client.on('message', function (topic, message) {
    //console.log(message)
    //console.log('received message!');
    var message = JSON.parse(message)
    if(topic === 'IC.embedded/tEEEm/TO_APP'){
        if (message.type == START_ALARM){
            console.log('play here')
            audio.play();
        }
        else if (message.type == STOP_ALARM){
            audio.pause();
            console.log('pause audio');
        }
        else if (message.type == RESULTS){
            temperatureData = message.data;
        }
    }
});

function sendSleepTriggerMessage() {
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': SPEECH_TRIGGER})); 
}

function showTemperatureData(){
    console.log('show temperature data here');
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS}));
    // use temperatureData with a graph library to create a chart.
}