$(document).ready(function() {
  $('.button').on('click', function() {
    $('.content').toggleClass('isOpen');
  });
});

/**
 * @desc Ajax - Pings server connections, displays status
 */
$(document).ready(function(){
    var $myForm = $('.checkConn');
    $myForm.submit(function(event){
        event.preventDefault();
        document.getElementById('submit').disabled = true;
        document.getElementById('connectionProcess').innerHTML = 'Checking connection...';
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
        // document.getElementById('navbar_info').innerHTML = 'Checking done <span class="glyphicon glyphicon-ok"></span>';
        submitIcon();
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }

    /**
     * @desc This function changes button icon based on button state
     */
    function submitIcon(){
      var submit = document.getElementById('submit');
      if(submit.disabled === true) {
        document.getElementById('cProgress').classList.add('fa-sync');
        document.getElementById('cProgress').classList.remove('fa-angle-right');
      }
      else{
        document.getElementById('cProgress').classList.add('fa-angle-right');
        document.getElementById('cProgress').classList.remove('fa-sync');
      }
    }

});

/**
 * @desc Ajax - Install database service
 */
$(document).ready(function(){
    var $myForm = $('.createDB');
    $myForm.submit(function(event){
        event.preventDefault();
        $("#outputTable tr").remove();
        var submit = document.getElementById('create_db');
        submit.disabled = true;
        submit.innerText = 'Installing...';
        document.getElementById('service_time').innerHTML = 'Installing database...';
        // document.getElementById('navbar_info').innerHTML = 'Service running...';
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
        var button = document.getElementById('create_db');
        serviceOutput(s_time, output, button);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

$(document).ready(function(){
    var $myForm = $('.installedDbForm');
    $myForm.submit(function(event){
        var $thisURL = '';
        var submit = document.activeElement.id;
        console.log(submit);
        if (submit === "start_server") {
          $thisURL = 'startDb/';
          console.log($thisURL);
          document.activeElement.disabled = true;
        }
         else if (submit === "stop_server") {
          $thisURL = 'stopDb/';
          console.log($thisURL);
          document.activeElement.disabled = true;
        }
        console.log($thisURL);
        event.preventDefault();
        $("#outputTable tr").remove();
        document.getElementsByClassName("button").disabled = true;
        document.getElementById('service_time').innerHTML = 'Running process...';
        var $formData = $(this).serialize();
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
        var button = document.getElementsByClassName("button");
        document.activeElement.disabled = false;
        serviceOutput(s_time, output, button);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/**
 * @desc This function applies output of CTRLPNL services
 * @param s_time - Time used on executing service
 * @param output - The output data of an executed service
 * @param button - Submit button of form executing service
 */
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
            var newCell4 = newRow.insertCell(3);
            var cell1 = document.createTextNode((i+1).toString());
            var split = o_keys[i].split(",");
            var server = split[1];
            var task = split[0];
            var cell2 = document.createTextNode(server);
            var cell3 = document.createTextNode(task);
            var cell4 = document.createTextNode(value);
            if(value === 'Success'){
                newCell4.style.color = 'green';
            }
            else{
                newCell4.style.color = 'red';
            }
            newCell1.appendChild(cell1);
            newCell2.appendChild(cell2);
            newCell3.appendChild(cell3);
            newCell4.appendChild(cell4);
        }
        document.getElementById('service_time').innerHTML = s_time;
        var submit = button;
        submit.disabled = false;
        submit.innerText = 'Install';
        // document.getElementById('navbar_info').innerHTML = 'Service done <span class="glyphicon glyphicon-ok"></span>';
}

/**
 * @desc This function selects/deselects all checkboxes when selecting server
 */
$(document).ready(function(){
    var $select = $('#id_createDB-server_name_1');
    $select.on('change', function() {
    var checkboxes = document.getElementsByName('createDB-server_name');
        for (var checkbox in checkboxes) {
            if(document.getElementById('id_createDB-server_name_1').checked) {
                checkboxes[checkbox].checked = true;
            }
            else{
                checkboxes[checkbox].checked = false;
            }
        }
    })
});
