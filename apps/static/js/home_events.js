$(document).ready(function(){
  $('#recurse').on('click', function(){
    $("#recurse_depth").toggle();
  })
  $('#authenticate').on('click', function(){
    $("#auth").toggle();
  })
  $('#query').click(function(){
    url = $('#search').val();
    extensions = $('#extensions').val();
    if (url == '' || extensions == ''){
      var msg = "You must enter a URL and a list of extensions";
      console.log(msg);
      $('#results').html(msg)
      return false;
    }
    var data = {
      url: url,
      extensions: extensions,
      auth: {
        username: $('#username').val(),
        password: $('#password').val()
      },
      recurse: $('#recurse').val() || true,
      recurse_depth: $('#recurse_depth').val() || 4
    }
    console.log(data);
    $.ajax({
      method: "POST",
      url: Flask.url_for("home.query"),
      data: JSON.stringify(data),
      contentType: "application/json;charset=utf-8"
    }).done(function(data) {
      $('#results').html(data.message);
      alert(data.message);
    });
  })

  // Refresh list by interval
  var interval = setInterval(function(){
    $.ajax({
      method: "GET",
      url: Flask.url_for("home.list"),
      success: function(data){
        console.log(data)
        $('#jstree').jstree({'core': {
          'data' : data
        }});
      },
      error: function(data){
        console.log("Error while retrieving data")
        console.log(data)
      }
    })
  }, 5000);
})
