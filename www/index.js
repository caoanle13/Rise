// TO_PI TOPIC MESSAGES
const SPEECH_TRIGGER = 0;
const TIME_SET = 1;
const ASK_RESULTS = 2;
const RECEIVED_START_ALARM = 3;
const RECEIVED_STOP_ALARM = 4;
const TEMPERATURE = 0;
const HUMIDITY = 1;
// TO_APP TOPIC MESSAGES
const START_ALARM = 0;
const STOP_ALARM = 1;
const RESULTS = 2;
const SPEAK = 3;

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
            audio.play();
            $('#wake_up_modal').modal('show');
            client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': RECEIVED_START_ALARM}));
        }
        else if (message.type == STOP_ALARM){
            audio.pause();
            $('#wake_up_modal').modal('hide');
            client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': RECEIVED_STOP_ALARM}));
        }
        else if (message.type == SPEAK){
            responsiveVoice.speak(message.say);
        }
        else if (message.type == RESULTS){
            if(message.data_for == HUMIDITY){
                displayGraphModal("Humidity", message.humid_data, message.time);
            } else {
                displayGraphModal("Temperature", message.temp_data, message.time);
            }
        }
    }
});

function sendSleepTriggerMessage() {
    responsiveVoice.speak("When would you like to wake up?");
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': SPEECH_TRIGGER})); 
}

function askTempData(){
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS, 'data_for': TEMPERATURE}));
}

function askHumidData(){
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS, 'data_for': HUMIDITY}));
}

function displayGraphModal(title, sensorData, timeData){
    console.log(timeData);
    var ctx = document.getElementById("my_chart").getContext('2d');
    let chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets:[  {
                    data: sensorData,
                    borderColor:  '#ffffff',
                    backgroundColor: '#888888',
                    fill: true
                    } 
                ],
        labels: timeData,
    },
    options: {
        legend:{
            display: false
        },
        title: {
            display: true,
            text: title,
            fontSize: 14
        }
    }
});
    $('#graph_modal').modal('show');
}