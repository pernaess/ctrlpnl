$(document).ready(function() {
  $('.button').on('click', function() {
    $('.content').toggleClass('isOpen');
  });
});

$(document).ready(function(){
    var $myForm = $('.checkConn');
    $myForm.submit(function(event){
        event.preventDefault();
        document.getElementById('submit').disabled = true;
        var $formData = $(this).serialize();
        var $thisURL = 'CheckConn/';
        submitIcon();
        $.ajax({
            method: "POST",
            url: $thisURL,
            data: $formData,
            success: handleFormSuccess,
            error: handleFormError
        })
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        for (var i = 0; i < data.length; i++){
            document.getElementById('serverstatus' +(i+1)).innerHTML = data[i];
            if (data[i].valueOf() == "Running"){
                document.getElementById('serverstatus' +(i+1)).style.color = "green";
            }
            else{
               document.getElementById('serverstatus' +(i+1)).style.color = "red";
            }
        }
        document.getElementById('submit').disabled = false;
        submitIcon();
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }

    function submitIcon(){
      var submit = document.getElementById('submit');
      if(submit.disabled === true) {
        document.getElementById('cProgress').classList.add('glyphicon-time');
        document.getElementById('cProgress').classList.remove('glyphicon-refresh');
      }
      else{
        document.getElementById('cProgress').classList.add('glyphicon-refresh');
        document.getElementById('cProgress').classList.remove('glyphicon-time');
      }
    }

});

