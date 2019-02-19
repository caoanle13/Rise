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


var client = mqtt.connect('mqtt://ee-estott-octo.ee.ic.ac.uk:8080');

client.on('connect', function () {
    console.log('connected to MQTT!');
    client.subscribe('IC.embedded/tEEEm/TO_APP', function (err) {
        if(!err){
            console.log('subscribed to TO_APP successfully!');
        }
    });
});

// Callback when message is received on subscribed topic
client.on('message', function (topic, message) {

    // Parse the message
    var message = JSON.parse(message)

    // Check that it is the right topic
    if(topic === 'IC.embedded/tEEEm/TO_APP'){

        // START_ALARM: play alarm and display wake up modal
        if (message.type == START_ALARM){
            audio.play();
            $('#wake_up_modal').modal('show');
            client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': RECEIVED_START_ALARM}));
        }

        // STOP_ALARM: stop alarm and hide wake up modal
        else if (message.type == STOP_ALARM){
            audio.pause();
            $('#wake_up_modal').modal('hide');
            client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': RECEIVED_STOP_ALARM}));
        }

        // SPEAK: perform speech synthesis of the received message
        else if (message.type == SPEAK){
            responsiveVoice.speak(message.say);
        }

        // RESULTS: display results in graph modal
        else if (message.type == RESULTS){
            if(message.data_for == HUMIDITY){
                displayGraphModal("Humidity", message.humid_data, message.time);
            } else {
                displayGraphModal("Temperature", message.temp_data, message.time);
            }
        }
    }
});

// Function to send a SPEECH_TRIGGER message (when user presses sleep button)
function sendSleepTriggerMessage() {
    responsiveVoice.speak("When would you like to wake up?");
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': SPEECH_TRIGGER})); 
}

// Function to send ASK_RESULTS for Temperature message (when user presses on data graph buttons)
function askTempData(){
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS, 'data_for': TEMPERATURE}));
}

// Function to send ASK_RESULTS for Humidity message (when user presses on data graph buttons)
function askHumidData(){
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS, 'data_for': HUMIDITY}));
}

// Function to display the graph modal upon receival of a RESULTS message
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