
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var tweets_received = [];

    //receive details from server
    socket.on('newtweet', function(msg) {
        console.log("Received number" + msg.tweet);
        //maintain a list of 20 tweets
        if (tweets_received.length >= 20){
            tweets_received.shift()
        }
        tweets_received.push(msg.tweet);
        tweet_string = ''
        for (var i = 0; i < tweets_received.length; i++){
            tweet_string =  tweet_string + '<p>' + i.toString() + ')' + tweets_received[i] + '</p>';
        }
        $('#log').html(tweet_string);
    });

});


function initDB() {
    $.get('/api/initdb');
};

function fillDB() {
    $.get('/api/filldb', function(){
       $("#success_alert").html("Success");
    });
};