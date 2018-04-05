/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

var v_calls_count = 0;

// Adding local loading modal.
function startLoading()
{
	v_calls_count++;
	$body = $("body");
    $body.addClass("loading");
}

// Removing loading modal.
function endLoading()
{
	if (v_calls_count>0)
		v_calls_count--;
	if (v_calls_count==0) {
		$body = $("body");
    $body.removeClass("loading");
  }

}

function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function csrfSafeMethod(method) {
		return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

/// <summary>
/// AJAX call.
/// </summary>
/// <param name="p_url">Webmethod url.</param>
/// <param name="p_data">Data object in JSON.stringify format.</param>
/// <param name="p_successFunc">Success return function.</param>
/// <param name="p_errorFunc">Error return function.</param>
/// <param name="p_notifMode">Notification mode.</param>
/// <param name="p_loading">Has loading or not.</param>
function execAjax(p_url,p_data,p_successFunc,p_errorFunc,p_notifMode,p_loading) {

	if (p_loading==null || p_loading==true)
		startLoading();

	var csrftoken = getCookie('csrftoken');

	$.ajax({
        url: p_url,
        data: {data: p_data},
				type: "post",
        dataType: "json",
				beforeSend: function(xhr, settings) {
		        if (!csrfSafeMethod(settings.type) && !this.crossDomain) {
		            xhr.setRequestHeader("X-CSRFToken", csrftoken);
		        }
		    },
        success: function(p_return) {

        	if (p_loading==null || p_loading==true)
				endLoading();

        	if (p_return.v_error) {

        		if (p_return.v_error_id==1)
        			showAlert('Session object was destroyed, click <a href="Login.aspx">here</a> to be redirected to login screen or finish what you were doing and reload the page.');
						else if (p_errorFunc) {
							p_errorFunc(p_return);
						}
						else
        			showError(p_return.v_data);

       		}
       		else {
		       	if (p_successFunc!=null)
        			p_successFunc(p_return);
        	}
        },
        error: function(msg) {

					showAlert('Request error.')

        	if (p_loading==null || p_loading==true)
						endLoading();

        	if (msg.readyState==0)
        		reportOffline();
        }
	});

}

/// <summary>
/// Reporting that webserver is off.
/// </summary>
function reportOffline() {

	showAlert('Webserver was shutdown, please restart it and reload the application.');

	var v_status_img = document.getElementById("ajax_status");

}
