$(document).ready(function() {
  s_status();
  $('.button').on('click', function() {
    $('.content').toggleClass('isOpen');
  });
});

function s_status(){
  var status=document.getElementById("serverstatus").value.toString();
  var running = "Running!";

  if (status === running){
    document.getElementById("serverstatus").style.color = "green";
  }
  else{
    document.getElementById("serverstatus").style.color = "red";
  }
}


