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
    $myForm.submit(function(event) {
        event.preventDefault();
        if (validateCreateDB()) {
            $("#outputTable tr").remove();
            var submit = document.getElementById('create_db');
            submit.disabled = true;
            submit.innerText = 'Installing...';
            document.getElementById('service_time').innerHTML = 'Installing database...';
            var $formData = $(this).serialize();
            var $thisURL = 'createDB/';
            $.ajax({
                method: "POST",
                url: $thisURL,
                data: $formData,
                success: handleFormSuccess,
                error: handleFormError
            })
        }
    });

    function validateCreateDB(){
        if(validateCheckboxes('div_id_createDB-server_name') &
            validateElement('div_id_createDB-database_name', false) &
            validateElement('div_id_createDB-username', false) &
            validateElement('div_id_createDB-password', true) &
            validateElement('div_id_createDB-sudo_password', true))
            return true;
        // Send a return message saying a server must be chosen to the chosen div.
        return false;
    }

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


/**
 * @desc Ajax - Install Nginx service
 */
$(document).ready(function(){
    var $myForm = $('.installNginx');
    $myForm.submit(function(event){
        event.preventDefault();
        if(validateCheckboxes('div_id_nginx-servers') && validateElement('div_id_nginx-sudo_password', true)){
            $("#outputTable tr").remove();
            var submit = document.getElementById('install_nginx');
            submit.disabled = true;
            submit.innerText = 'Installing...';
            document.getElementById('service_time').innerHTML = 'Installing Nginx...';
            var $formData = $(this).serialize();
            var $thisURL = 'installNginx/';
            $.ajax({
                method: "POST",
                url: $thisURL,
                data: $formData,
                success: handleFormSuccess,
                error: handleFormError
            })
        }

    });

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        var s_time = data['t_output'];
        var output = data['p_output'];
        var button = document.getElementById('install_nginx');
        serviceOutput(s_time, output, button);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/**
 * @desc Ajax - Install PHP service
 */
$(document).ready(function(){
    var $myForm = $('.installPHP');
    $myForm.submit(function(event){
        event.preventDefault();
        if (validateCheckboxes('div_id_php-servers')) {
            $("#outputTable tr").remove();
            var submit = document.getElementById('install_php');
            submit.disabled = true;
            submit.innerText = 'Installing...';
            document.getElementById('service_time').innerHTML = 'Installing PHP...';
            var $formData = $(this).serialize();
            var $thisURL = 'installPHP/';
            $.ajax({
                method: "POST",
                url: $thisURL,
                data: $formData,
                success: handleFormSuccess,
                error: handleFormError
            })
        }
    });

    function handleFormSuccess(data, textStatus, jqXHR){
        console.log(data);
        console.log(textStatus);
        console.log(jqXHR);
        var s_time = data['t_output'];
        var output = data['p_output'];
        var button = document.getElementById('install_php');
        serviceOutput(s_time, output, button);
    }

    function handleFormError(jqXHR, textStatus, errorThrown){
        console.log(jqXHR);
        console.log(textStatus);
        console.log(errorThrown);
    }
});

/**
 * @desc Ajax - Start/Stop/Restart/Reload/Uninstall MYSQL database server
 */
$(document).ready(function(){
    var $myForm = $('.installedDbForm');
    $myForm.submit(function(event){
        var $thisURL = '';

        switch (document.activeElement.id){
            case "start_server":
                $thisURL = 'startDb/';
                break;
            case "stop_server":
                $thisURL = 'stopDb/';
                break;
            case "restart_server":
                $thisURL = 'restartDb/';
                break;
            case "reload_server":
                $thisURL = 'reloadDb/';
                break;
            case "uninstall_server":
                $thisURL = "uninstallMysql/";
                break;
            default:
                console.log("Could not apply");
        }
        event.preventDefault();

        if(validateElement('div_id_installed_db-sudo_password', true)) {
            document.activeElement.disabled = true;
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
        }
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
 * @desc Ajax - Uninstall PHP packages
 */
$(document).ready(function(){
    var $myForm = $('.installedPhpForm');
    $myForm.submit(function(event){
        var $thisURL = '';
        if (document.activeElement.id === "uninstall_php")
          $thisURL = 'uninstallPhp/';

        event.preventDefault();

        if(validateElement('div_id_installed_php-sudo_password'), true) {
            document.activeElement.disabled = true;
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
        }
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
 * @desc Ajax - Start/Stop/Restart/Reload/Uninstall NGINX server
 */
$(document).ready(function(){
    var $myForm = $('.installedNginxForm');
    $myForm.submit(function(event){
        var $thisURL = '';

        switch (document.activeElement.id){
            case "start_nginx":
                $thisURL = 'startNginx/';
                break;
            case "stop_nginx":
                $thisURL = 'stopNginx/';
                break;
            case "restart_nginx":
                $thisURL = 'restartNginx/';
                break;
            case "reload_nginx":
                $thisURL = 'reloadNginx/';
                break;
            case "uninstall_nginx":
                $thisURL = "uninstallNginx/";
                break;
            default:
                console.log("Could not apply");
        }
        event.preventDefault();

        if(validateElement('div_id_installed_nginx-sudo_password', true)) {
            document.activeElement.disabled = true;
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
        }
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
 * @desc Ajax - Start/Stop/Restart/Reload/Uninstall PostgreSql database server
 */
$(document).ready(function(){
    var $myForm = $('.installedPostgresForm');
    $myForm.submit(function(event){
        var $thisURL = '';
        switch (document.activeElement.id){
            case "start_server1":
                $thisURL = 'startPostgreSql/';
                break;
            case "stop_server1":
                $thisURL = 'stopPostgreSql/';
                break;
            case "restart_server1":
                $thisURL = 'restartPostgreSql/';
                break;
            case "reload_server1":
                $thisURL = 'reloadPostgreSql/';
                break;
            case "uninstall_server1":
                $thisURL = "uninstallPostgreSql/";
                break;
            default:
                console.log("Could not apply");
        }
        event.preventDefault();
        if(validateElement('div_id_installed_postgres-sudo_password', true)) {
            document.activeElement.disabled = true;
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
        }
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
 * @desc This function selects/deselects all checkboxes in install database when selecting server
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

/**
 * @desc This function selects/deselects all checkboxes in install Nginx when selecting server
 */
$(document).ready(function(){
    var $select = $('#id_nginx-servers_1');
    $select.on('change', function() {
    var checkboxes = document.getElementsByName('nginx-servers');
        for (var checkbox in checkboxes) {
            if(document.getElementById('id_nginx-servers_1').checked) {
                checkboxes[checkbox].checked = true;
            }
            else{
                checkboxes[checkbox].checked = false;
            }
        }
    })
});

// Validation methods:
function validateConnectServer() {
    if (validateElement("div_id_createServer-server_nickname", false) &
        validateElement("div_id_createServer-server_ip", false) &
        validateElement("div_id_createServer-sudo_user", false) &
        validateElement("div_id_createServer-sudo_password", true))
        return true;
    return false;
}

function validateElement(path, isPasswordValidation){
    var validationElement = document.getElementById(path).children[1].children[0];
    var val = validationElement.value;
    if (isPasswordValidation){
        var bool = passwordLengthRequirement(val);
        validationElement.style.backgroundColor = bool ? "lightgreen" : "red";
        return bool;
    }
    var bool = allowedTextFieldValidation(val);
    validationElement.style.backgroundColor = bool ? "lightgreen" : "red";
    return bool;
}

function allowedTextFieldValidation(text){
    if (text == '')
        return false;
    else if (text.match(/[^\w\.\-]/))
        return false;
    return true;
}

function passwordLengthRequirement(text){
    if (text.length < 6)
        return false;
    if (text.length > 20)
        return false;
    return allowedTextFieldValidation(text);
}

function checkServerIsChosen(path){
    var validationElement = document.getElementById(path);
    var serverNameList = validationElement.getElementsByTagName('INPUT');

    for(var x = 0; x < serverNameList.length; x++)
        if(serverNameList[x].type.toUpperCase()=='CHECKBOX')
            if(serverNameList[x].checked){
                validationElement.style.backgroundColor = "lightgreen";
                return true;
            }
    validationElement.style.backgroundColor = "red";
    return false;
}

function validateCheckboxes(path){
    if(checkServerIsChosen(path))
        return true;
    // Send a return message saying a server must be chosen to the chosen div.
    return false;
}