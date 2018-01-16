var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log("Connected to socket")
        socket.emit('joined', { name: $('#name').val() });
    });
    socket.on('status', function(data) {
        console.log("Status event received.")
        $('#chat').val($('#chat').val() + '<' + data.msg + '>\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    socket.on('message', function(data) {
        console.log("Message event received.")
        $('#chat').val($('#chat').val() + data.msg + '\n');
        $('#chat').scrollTop($('#chat')[0].scrollHeight);
    });
    $('#save_name').on('click', function(){
      var name = $('#name').val();
      socket.emit('change_name', {name: name})
    })
    $('#text').keypress(function(e) {
        console.log("Text event received.")
        var code = e.keyCode || e.which;
        if (code == 13) {
            text = $('#text').val();
            $('#text').val('');
            socket.emit('text', {msg: text});
            console.log("Text event sent to server")
        }
    });
    $('#rename').on('click', function(){

    })
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        // go back to the login page
        window.location.href = "{{ url_for('videos.index') }}";
    });
}
