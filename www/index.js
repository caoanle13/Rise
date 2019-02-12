// TO_PI TOPIC MESSAGES
const SPEECH_TRIGGER = 0;
const TIME_SET = 1;
const ASK_RESULTS = 2;
const TEMPERATURE = 3;
const HUMIDITY = 4;
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
        }
        else if (message.type == STOP_ALARM){
            audio.pause();
            $('#wake_up_modal').modal('hide');
        }
        else if (message.type == RESULTS){
            tempData = message.temp;
            humidData = message.humid;
            timeData = message.time;
            displayGraphModal(sensorData);
        }
        else if (message.type == SPEAK){
            responsiveVoice.speak(message.say);
        }
    }
});

function sendSleepTriggerMessage() {
    responsiveVoice.speak("When would you like to wake up?");
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': SPEECH_TRIGGER})); 
}

function askTempData(){
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS, 'data': TEMPERATURE}));
}

function askHumidData(){
    client.publish('IC.embedded/tEEEm/TO_PI', JSON.stringify({'type': ASK_RESULTS, 'data': HUMIDITY}));
}

function displayGraphModal(sensorData){
    var ctx = document.getElementById("my_chart").getContext('2d');
    let chart = new Chart(ctx, {
    type: 'line',
    data: {
        datasets:[  {
                    data: [50, 10, 30, 20, 50, 60],
                    borderColor:  '#ffffff',
                    backgroundColor: '#888888',
                    fill: true
                    } 
                ],
        labels: ['1 AM', '2 AM', '3 AM', '4 AM', '5 AM', '6 AM'],
    },
    options: {
        legend: {
            display: true,
            position: 'right',
            labels: {
                text: 'Temperature',
                boxWidth: 20,
            }
        },
        scales: {
            xAxes: [{
                ticks: {
                    min: '1 AM',
                    max: '6 AM'
                }
            }]
        }
    }
});
    $('#graph_modal').modal('show');
}