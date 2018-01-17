var socket;
$(document).ready(function(){
    socket = io.connect('http://' + document.domain + ':' + location.port + '/video');
    socket.on('connect', function() {
        console.log("Connected to socket")
        socket.emit('joined', {});
    });
    socket.on('new_video', function(item) {
      add_video(item);
    });
    socket.on('downloaded', function(item){
      $('a[href="' + item.url + '"]').parent().find('.ui.download.button')
        .text("Downloaded !")
        .toggleClass('primary positive')
        .addClass('disabled')
    })
    socket.on('progress', function(item){
      console.log(item.percent);
      console.log(item.url + ' :' + item.percent);
      console.log("Updating progress")
      $('a[href="' + item.url + '"]').parent().find('.progress').find('.progress-percent').text(String(item.percent) + ' %');
    })
    $('#loader').hide();

    //on keyup, start the countdown
    var typingTimer;
    var doneTypingInterval = 500;
    $('#search').keyup(function(){
        clearTimeout(typingTimer);
        if ($('#search').val()) {
            typingTimer = setTimeout(doneTyping, doneTypingInterval);
        }
    });
    function doneTyping() {
      search_query = $('#search').val();
      $('#results').html("");
      $('#nresults').html("No results found.")
      $('#loader').show()
      $.ajax({
        method: "GET",
        url: Flask.url_for('videos.search_youtube') + "?query=" + search_query,
        contentType: "application/json;charset=utf-8"
      })
    }
});

function leave_room() {
    socket.emit('left', {}, function() {
        socket.disconnect();
        // go back to the login page
        window.location.href = "{{ url_for('videos.index') }}";
    });
}

function add_video(item) {
  console.log("Video found: ");
  console.log(item);
  // if ($("#results").html() == ""){
    // $('#results').append("<div class='ui header'>Results</div>")
  // }
  var nresults = Number($('#nresults').attr('data-number'))
  nresults += 1;
  $('#nresults').attr('data-number', String(nresults));
  console.log(nresults + " results found.")
  $('#nresults').html(nresults + " results found.")
  var url = item.url;
  var title = item.title;
  var row_content= "<img src='" + item.thumbnail_url + "'/>";
  var header = "<a target='_blank' href='" + url + "' class='header'>" + title + "</a>";
  var dropdown = [
    "<div class='ui selection resolution dropdown'>",
    "<div class='default text'>Quality</div>",
    "<i class='ui dropdown icon'></i>",
    "<div class='ui menu'>"
  ].join("")
  var first = true;
  var s = false;
  item.streams.forEach(function(stream){
    if (!stream.resolution){
      return false;
    }
    if (first){
      s = stream;
      first = false;
    }
    dropdown += "<div class='ui item' data-value='" + stream.itag + "'>" + stream.resolution + " (" + stream.mime_type +")" + "</div>"
  })
  dropdown += "</div></div>"
  var button = "&nbsp<div class='ui download disabled primary button'><i class='ui download icon'></i>Download</div>"

  // row_content += "<div class='content'>" + header + "</div>"
  row_content += "<div class='content'>" + header + "</br></br>" + dropdown + button + "</div>"
  var row = $('<div/>', {
    class: "ui item",
    css: {
      "min-height": "90px",
      "padding": "15px"
    }
  })
  if (typeof url != 'undefined'){
    row.html(row_content)
    $('#loader').hide();
    $('#results').append(row);
    $('.ui.download.button').unbind();
    $('.ui.resolution.dropdown').dropdown({
      onChange: function(){
        $(this).parent().find('.ui.download.button').removeClass('disabled')
      }
    })

    // Refresh dropdown and set default values (best resolution)
    $('a[href="' + item.url + '"]').parent().find('.ui.dropdown').dropdown('refresh');
    $('a[href="' + item.url + '"]').parent().find('.ui.dropdown').dropdown('set selected', String(s.itag));
    $('a[href="' + item.url + '"]').parent().find('.ui.dropdown').dropdown('set text', s.resolution + " (" + s.mime_type +")");
    // TODO: Replace above by following
    // var $dropdown = $(row).find('.ui.dropdown')
    // console.log("Dropdown resolution: ")
    // console.log($dropdown)
    // $dropdown.dropdown('refresh')
    // $dropdown.dropdown('set selected', String(s.itag));
    // $dropdown.dropdown('set text', s.resolution + " (" + s.mime_type +")");

    // Downloaded
    $('.ui.download.button').on('click', function(){
      $(this).after('<div class="progress"><i class="ui loading icon"></i><div class="progress-percent"></div></div>')
      var itag = $(this).parent().find('.ui.dropdown').dropdown('get value');
      var url = $(this).parent().find('.header').attr('href');
      console.log("Itag: " + itag)
      console.log("URL: " + url)
      var get_url = Flask.url_for('videos.download_youtube') + "?url=" + url + "&itag=" + itag;
      console.log("GET URL: " + get_url)
      var download_button = $(this);
      $.ajax({
        method: "GET",
        url: get_url,
        contentType: "application/json;charset=utf-8",
        success: function(data){
          console.log(data)
          if (data.success){
            download_button.addClass('disabled')
            download_button.text('Downloading ...')
          }
        }
      })
    })
  }
}
