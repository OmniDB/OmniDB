/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Create a WebSocket connection.
/// </summary>
/// <param name="p_address">Server address.</param>
/// <param name="p_port">Server port.</param>
/// <param name="p_onOpen">On connection open callback.</param>
/// <param name="p_onMessage">On message receive callback.</param>
/// <param name="p_onClose">On connection close callback.</param>
/// <param name="p_onError">On connection error callback.</param>
/// <param name="p_channel">The channel to be used in the server.</param>
function createWebSocket(p_address, p_port, p_onOpen, p_onMessage, p_onClose, p_onError, p_channel) {
	if(typeof p_address == 'undefined' || p_address == null) {
		return;
	}

	var v_port = 80;

	if(p_port != null && typeof p_port == 'number') {
		v_port = p_port;
	}

	var v_connection = new WebSocket(p_address + ':' + v_port + v_url_folder + '/' + p_channel);

	if(p_onOpen != null && typeof p_onOpen == 'function') {
		v_connection.onopen = p_onOpen;
	}

	if(p_onMessage != null && typeof p_onMessage == 'function') {

		v_connection.onmessage = (function() {

			return function(e) {

				var v_context_code = null;

				var v_message = JSON.parse(e.data);
				var v_context = null;

				if (v_message.v_context_code!=0 && v_message.v_context_code!=null) {

					for (var i=0; i<v_connection.contextList.length; i++) {

						if (v_connection.contextList[i].code == v_message.v_context_code) {
							v_context = v_connection.contextList[i].context;
							v_context_code = v_connection.contextList[i].code;
							break;
						}
					}
				}

				p_onMessage(v_message,v_context, v_context_code);

			}
		})();
	}

	if(p_onClose != null && typeof p_onClose == 'function') {
		v_connection.onclose = p_onClose;
	}

	if(p_onError != null && typeof p_onError == 'function') {
		v_connection.onerror = p_onError;
	}

	v_connection.contextList = [];
	v_connection.contextCode = 1;

	return v_connection;
}

function createContext(p_connection, p_context) {
	p_connection.contextCode += 1;
	v_context_code = p_connection.contextCode;
	p_context.v_context_code = v_context_code;
	var v_context = {
		code: v_context_code,
		context: p_context
	}
	p_connection.contextList.push(v_context);
	return v_context;
}

function removeContext(p_connection, p_context_code) {
	for (var i=0; i<p_connection.contextList.length; i++) {
		if (p_connection.contextList[i].code == p_context_code) {
			p_connection.contextList.splice(i,1);
			break;
		}
	}
}

/// <summary>
/// Sends a message through the websocket connection to the server.
/// </summary>
/// <param name="p_connection">The websocket object that corresponds to the connection.</param>
/// <param name="p_messageCode">Transaction code that identify the operation.</param>
/// <param name="p_messageData">A object that will be send to the server.</param>
/// <param name="p_error">If it's an error message.</param>
/// <param name="p_context">The message context object. Anything that would be used when client receives a response message related to this request.</param>
function sendWebSocketMessage(p_connection, p_messageCode, p_messageData, p_error, p_context) {

	var v_context_code = 0;

	//Configuring context
	if (p_context!=null) {

		//Context code is passed
		if (p_context === parseInt(p_context, 10)) {
			v_context_code = p_context;
		}
		else {
			p_connection.contextCode += 1;
			v_context_code = p_connection.contextCode;
			p_context.v_context_code = v_context_code;
			var v_context = {
				code: v_context_code,
				context: p_context
			}
			p_connection.contextList.push(v_context);
		}
	}

	waitForSocketConnection(
		p_connection,
		function() {
			p_connection.send(
				JSON.stringify({
					v_code: p_messageCode,
					v_context_code: v_context_code,
					v_error: p_error,
					v_data: p_messageData
				})
			);
		}
	);

	return v_context_code;
}

/// <summary>
/// Do something when the connection is opened
/// </summary>
/// <param name="p_connection">The websocket object that corresponds to the connection.</param>
/// <param name="p_callback">The callback that contains somenthing to be done.</param>
function waitForSocketConnection(p_connection, p_callback){
	setTimeout(
		function () {
			if (p_connection.readyState == 1) {
				if(p_callback != null) {
					p_callback();
				}

				return;
			}
			else {
				waitForSocketConnection(p_connection, p_callback);
			}
		},
		5
	);
}
