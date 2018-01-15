var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/download');
    socket.on('connect', function() {
        console.log("Connected to socket")
        socket.emit('list_downloads', {});
    });
    socket.on('file_found', function(item) {
      add_file(item);
    });
})

function add_file(item) {
  console.log("Video found: ");
  console.log(item);
  var nresults = Number($('#nresults').attr('data-number'))
  nresults += 1;
  $('#nresults').attr('data-number', String(nresults));
  console.log(nresults + " results found.");
  $('#nresults').html(nresults + " results found.");
  var url = item.download_url;
  var title = item.title;
  var row = [
    "<div class='ui item'>",
    "<a href='" + url + "' class='ui header'>" + title + "</a>"
    "<div>"
  ].join("");
  $('#results').append(row);
}
