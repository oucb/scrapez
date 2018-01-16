var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/chat');
    socket.on('connect', function() {
        console.log("Connected to socket")
        socket.emit('joined', { name: $('#name').val() });
    });
    socket.on('status', function(data) {
        console.log("Status event received.")
        write_chat('#chat', '<' + data.msg + '>')
    });
    socket.on('message', function(data) {
        console.log("Message event received.")
        write_chat('#chat', data.msg)
    });
    socket.on('name_changed', function(data){
      var old_name = data.old_name;
      var new_name = data.new_name;
      var msg = "<'" + data.old_name + "' changed his name to '" + data.new_name + "'>"
      socket.emit('message', {msg: msg})
    })
    $('#text').keypress(function(e){
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
      var name = $('#name').val();
      socket.emit('change_name', {name: name})
    })
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        // go back to the login page
        window.location.href = "{{ url_for('videos.index') }}";
    });
}

function write_chat(selector, message){
  $(selector).val($(selector).val() + message + '\n');
  $(selector).scrollTop($(selector)[0].scrollHeight);
}
