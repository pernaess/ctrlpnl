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

$(document).ready(function(){
    var $myForm = $('.createDB');
    $myForm.submit(function(event){
        event.preventDefault();
        var submit = document.getElementById('create_db');
        submit.disabled = true;
        submit.innerText = 'Installing...';
        document.getElementById('service_time').innerHTML = 'Installing database...';
        document.getElementById('navbar_info').innerHTML = 'Service running...';
        var $formData = $(this).serialize();
        var $thisURL = 'createDB/';
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
        var s_time = data['t_output'];
        var output = data['p_output'];
        var button = 'create_db';
        serviceOutput(s_time, output, button);

    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

function serviceOutput(s_time, output, button){
          var o_keys = Object.keys(output);
        var table = document.getElementById('outputTable');
        console.log(Object.keys(output).length);
        for(var i=0; i<o_keys.length; i++){
            var key = Object.keys(output)[i];
            var value = output[key];
            var newRow = table.insertRow(table.rows.length);
            var newCell1 = newRow.insertCell(0);
            var newCell2 = newRow.insertCell(1);
            var newCell3 = newRow.insertCell(2);
            var cell1 = document.createTextNode((i+1).toString());
            var cell2 = document.createTextNode(o_keys[i]);
            var cell3 = document.createTextNode(value);
            if(value === 'Success'){
                newCell3.style.color = 'green';
            }
            else{
                newCell3.style.color = 'red';
            }
            newCell1.appendChild(cell1);
            newCell2.appendChild(cell2);
            newCell3.appendChild(cell3);
        }
        document.getElementById('service_time').innerHTML = s_time;
        var submit = document.getElementById(button);
        submit.disabled = false;
        submit.innerText = 'Install';
        document.getElementById('navbar_info').innerHTML = 'Service done <span class="glyphicon glyphicon-ok"></span>';
}

