/*
This file is part of OmniDB.
OmniDB is open-source software, distributed "AS IS" under the MIT license in the hope that it will be useful.

The MIT License (MIT)

Portions Copyright (c) 2015-2020, The OmniDB Team
Portions Copyright (c) 2017-2020, 2ndQuadrant Limited

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
var v_is_loading = false;

/**
 * Used to add a loading gif modal above page content.
 */
function startLoading() {
	v_calls_count++;
	if (!v_is_loading) {

		$('#div_loading').fadeIn(100);
		v_is_loading = true;
	}
}

/**
 * Used to remove a loading gif modal above page content.
 */
function endLoading() {
	if(v_calls_count > 0) {
		v_calls_count--;
	}

	if(v_calls_count==0) {
		$('#div_loading').fadeOut(100);
		v_is_loading = false;
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
  * ## execAjax
  * @desc Used to execute an AJAX call.
  *
	* @param {String} p_url - The url of the view to be executed.
  * @param {Object} p_data - A JavaScript object containing anything you want to pass as parameter to the server. Must be in JSON.stringify format.
  * @param {String} p_successFunc - A callback to be called if AJAX call succeeds.
  * @param {String} p_errorFunc - A callback to be called if AJAX call succeeds but returns with errors.
  * @param {Boolean} p_notifMode - The notification mode of this call.
  * @param {Boolean} p_loading - If this AJAX call should add a loading gif or not.
  * @param {Boolean} p_cancel_button - If the cancel button must be displayed or not.
  * @param {String} p_onAjaxErrorCallBack = false A callback to be called on AJAX error. Ex: connectivity issue.
  * @return {Function} Contextual callback returns based on status cases and returned data.
  */
 function execAjax(p_url,p_data,p_successFunc,p_errorFunc,p_notifMode,p_loading, p_cancel_button, p_onAjaxErrorCallBack = false) {
	// Starting the load animation if requested.
 	if(p_loading==null || p_loading==true) {
 		startLoading();
 	}
	// Showing the cancel button during the ajax if requested.
	if(v_cancel_button !== undefined) {
		v_cancel_button.style.display = 'none';

		if(p_cancel_button != null && p_cancel_button == true) {
			v_cancel_button.style.display = 'block';
		}
	}
	// Setting the token.
 	var csrftoken = getCookie(v_csrf_cookie_name);
	// Requesting data with ajax.
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
			// Terminating the load animation.
 			if(p_loading==null || p_loading==true) {
 				endLoading();
 			}
			// Intercepting the workflow when the request returns with evaluated server errors.
 			if(p_return.v_error) {
 				if(p_return.v_error_id == 1) {
 					showAlert('User not authenticated, please reload the page.');
 				}
 				else if(p_errorFunc) {
 					p_errorFunc(p_return);
 				}
 				else {
 					showAlert(p_return.v_data);
 				}
 			}
			// Resuming the workflow with the success callback function.
 			else {
 				if(p_successFunc != null) {
 					p_successFunc(p_return);
 				}
 			}
 		},
 		error: function(msg) {
			// Terminating the load animation.
 			if(p_loading == null || p_loading == true) {
 				endLoading();
 			}

			// Calling the optional function assigned as a callback if the ajax request fails.
 			if (p_onAjaxErrorCallBack) {
 				p_onAjaxErrorCallBack(msg);
 			}
			else {
				// Prompting error messages related to ajax error.
	 			if(msg.readyState != 0) {
	 				showAlert('Request error.')
	 			}
	 			else {
	 				if(msg.statusText!='abort') {
	 					reportOffline();
	 				}
	 			}
			}
 		}
 	});

	return v_ajax_call;
 }

/**
 * Reporting that webserver is off.
 */
function reportOffline() {
	showAlert('Webserver was shutdown, please restart it and reload the application.');
	var v_status_img = document.getElementById("ajax_status");
}
