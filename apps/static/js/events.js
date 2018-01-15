$(document).ready(function(){
    var socket_url = 'http://' + document.domain + ':' + location.port;
    var socket = io.connect(socket_url);
    console.log("Connected to socket at " + socket_url)
    socket.on('test_response', function(msg) {
        console.log("Received response from server: ")
        console.log(msg)
        $('#log').append('<p>Received: ' + msg.data + '</p>');
    });
    socket.on('connect', function() {
      console.log("Emitting 'test'")
      socket.emit('test', {data: 'I\'m connected!'});
      console.log("After emit !")
   });
});
