/*
Copyright 2016 The OmniDB Team

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
/// <param name="p_userId">On connection error callback.</param>
function createWebSocket(p_address, p_port, p_onOpen, p_onMessage, p_onClose, p_onError) {
	if(typeof p_address == 'undefined' || p_address == null) {
		return;
	}

	var v_port = 80;

	if(p_port != null && typeof p_port == 'number') {
		v_port = p_port;
	}

	var v_connection = new WebSocket(p_address + ':' + v_port);

	if(p_onOpen != null && typeof p_onOpen == 'function') {
		v_connection.onopen = p_onOpen;
	}

	if(p_onMessage != null && typeof p_onMessage == 'function') {
		v_connection.onmessage = p_onMessage;
	}

	if(p_onClose != null && typeof p_onClose == 'function') {
		v_connection.onclose = p_onClose;
	}

	if(p_onError != null && typeof p_onError == 'function') {
		v_connection.onerror = p_onError;
	}

	return v_connection;
}

/// <summary>
/// Sends a message through the websocket connection to the server.
/// </summary>
/// <param name="p_connection">The websocket object that corresponds to the connection.</param>
/// <param name="p_messageCode">Transaction code that identify the operation.</param>
/// <param name="p_messageData">A object that will be send to the server.</param>
/// <param name="p_error">If it's an error message.</param>
function sendWebSocketMessage(p_connection, p_messageCode, p_messageData, p_error) {
	waitForSocketConnection(
		p_connection,
		function() {
			p_connection.send(
				JSON.stringify({
					v_code: p_messageCode,
					v_error: p_error,
					v_data: p_messageData
				})
			);
		}
	);
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