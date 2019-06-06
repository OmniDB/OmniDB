/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

//Number of active AJAX calls
var v_calls_count = 0;

/**
 * Used to add a loading gif modal above page content.
 */
function startLoading() {
	v_calls_count++;
	$body = $("body");
	$body.addClass("loading");
}

/**
 * Used to remove a loading gif modal above page content.
 */
function endLoading() {
	if(v_calls_count > 0) {
		v_calls_count--;
	}

	if(v_calls_count==0) {
		$body = $("body");
		$body.removeClass("loading");
	}
}

/**
 * Used to get a cookie value from document, based on cookie name.
 * @param {string} name - the name of the cookie in the document.
 * @returns {string} cookie value, if exists.
 */

function getCookie(name) {
	var cookieValue = null;

	if(document.cookie && document.cookie !== '') {
		var cookies = document.cookie.split(';');

		for(var i = 0; i < cookies.length; i++) {
			var cookie = jQuery.trim(cookies[i]);

			// Does this cookie string begin with the name we want?
			if(cookie.substring(0, name.length + 1) === (name + '=')) {
				cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
				break;
			}
		}
	}

	return cookieValue;
}

/**
 * Used to get see if a http request is one of: GET, HEAD, OPTIONS, TRACE.
 * @param {string} method - the method to be checked.
 * @returns {boolean} if the http request is one of GET, HEAD, OPTIONS, TRACE or not.
 */
function csrfSafeMethod(method) {
	return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

var v_ajax_call = null;
var v_cancel_button = document.getElementById('bt_cancel_ajax');

/**
 * Abort last ajax call.
 */
function cancelAjax() {
	if(v_ajax_call != null) {
		v_ajax_call.abort();
	}
}

/**
 * Used to execute an AJAX call.
 * @param {string} p_url - the url of the view to be executed.
 * @param {object} p_data - a JavaScript object containing anything you want to pass as parameter to the server. Must be in JSON.stringify format.
 * @param {function} p_successFunc - a callback to be called if AJAX call succeeds.
 * @param {function} p_errorFunc - a callback to be called if AJAX call fails.
 * @param {boolean} p_notifMode - the notification mode of this call.
 * @param {boolean} p_loading - if this AJAX call should add a loading gif or not.
 * @param {boolean} p_cancel_button - if the cancel button must be displayed or not.
 */
function execAjax(p_url,p_data,p_successFunc,p_errorFunc,p_notifMode,p_loading, p_cancel_button) {
	if(p_loading==null || p_loading==true) {
		startLoading();
	}

	v_cancel_button.style.display = 'none';

	if(p_cancel_button != null && p_cancel_button == true) {
		v_cancel_button.style.display = 'block';
	}

	var csrftoken = getCookie('omnidb_csrftoken');

	v_ajax_call = $.ajax({
		url: v_url_folder + p_url,
		data: {
			data: p_data,
			tab_token: ''
		},
		type: "post",
		dataType: "json",
		beforeSend: function(xhr, settings) {
			if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
		success: function(p_return) {
			if(p_loading==null || p_loading==true) {
				endLoading();
			}

			if(p_return.v_error) {
				if(p_return.v_error_id == 1) {
					showAlert('Session object was destroyed, click <a href="Login.aspx">here</a> to be redirected to login screen or finish what you were doing and reload the page.');
				}
				else if(p_errorFunc) {
					p_errorFunc(p_return);
				}
				else {
					showError(p_return.v_data);
				}
			}
			else {
				if(p_successFunc != null) {
					p_successFunc(p_return);
				}
			}
		},
		error: function(msg) {
			if(p_loading == null || p_loading == true) {
				endLoading();
			}

			if(msg.readyState != 0) {
				showAlert('Request error.')
			}
			else {
				if(msg.statusText!='abort') {
					reportOffline();
				}
			}
		}
	});
}

/**
 * Reporting that webserver is off.
 */
function reportOffline() {
	showAlert('Webserver was shutdown, please restart it and reload the application.');
	var v_status_img = document.getElementById("ajax_status");
}
