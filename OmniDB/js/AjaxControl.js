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
	v_calls_count--;
	if (v_calls_count==0) {
		$body = $("body");
	    $body.removeClass("loading");
    }
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

	var v_status_img = document.getElementById("ajax_status");

	if (v_status_img!=null)
		v_status_img.src = "images/status_blue.png";

	$.ajax({
        type: "POST",
        url: p_url,
        data: p_data,
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(p_return) {

        	if (v_status_img!=null)
				v_status_img.src = "images/status_green.png";

        	if (p_loading==null || p_loading==true)
				endLoading();

        	if (p_return.d.v_error) {

        		if (p_return.d.v_error_id==1)
        			showAlert('Session object was destroyed, click <a href="Login.aspx">here</a> to be redirected to login screen or finish what you were doing and reload the page.');
        		else
        			showError(p_return.d.v_data);

       		}
       		else {
		       	if (p_successFunc!=null)
        			p_successFunc(p_return.d);
        	}
        },
        error: function(msg) {

        	if (v_status_img!=null)
				v_status_img.src = "images/status_green.png";

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