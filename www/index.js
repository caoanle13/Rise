// TO_PI TOPIC MESSAGES
const SPEECH_TRIGGER = 0;
const TIME_SET = 1;
const ASK_RESULTS = 2;
// TO_PI TOPIC MESSAGES
const START_ALARM = 0;
const STOP_ALARM = 1;
const GIVE_RESULTS = 2;


var client = mqtt.connect('mqtt://test.mosquitto.org:8080');

client.on('connect', function () {
    console.log('connected to MQTT!');
    client.subscribe('IC.embedded/tEEEm/TO_APP', function (err) {
        if(!err){
            console.log('subscribed to TO_APP successfully!');
        }
    });

});
