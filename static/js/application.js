
$(document).ready(function(){
    //connect to the socket server.
    var socket = io.connect('http://' + document.domain + ':' + location.port + '/test');
    var tweets_received = [];

    //receive details from server
    socket.on('newtweet', function(msg) {
        console.log("Received number" + msg.tweet);
        //maintain a list of ten numbers
        if (tweets_received.length >= 100){
            tweets_received.shift()
        }
        tweets_received.push(msg.tweet);
        tweet_string = ''
        for (var i = 0; i < tweets_received.length; i++){
            tweet_string =  tweet_string + '<p>' + tweets_received[i] + '</p>';
        }
        $('#log').html(tweet_string);
    });

});