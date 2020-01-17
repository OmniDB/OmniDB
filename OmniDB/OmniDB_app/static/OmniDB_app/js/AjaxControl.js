/*
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
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
