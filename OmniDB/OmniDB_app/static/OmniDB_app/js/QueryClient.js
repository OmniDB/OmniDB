/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Transaction codes of client requests.
/// </summary>
var v_queryRequestCodes = {
	Login: 0,
	Query: 1,
	Execute: 2,
	Script: 3,
	QueryEditData: 4,
	SaveEditData: 5,
	CancelThread: 6
}

/// <summary>
/// Transaction codes of server responses.
/// </summary>
var v_queryResponseCodes = {
	LoginResult: 0,
	QueryResult: 1,
	QueryEditDataResult: 2,
	SaveEditDataResult: 3,
	SessionMissing: 4
}

/// <summary>
/// The variable that will receive the WebSocket object.
/// </summary>
var v_queryWebSocket;

/// <summary>
/// Starts query client
/// </summary>
/// <param name="p_port">Port where chat will listen for connections.</param>
function startQueryWebSocket(p_port) {

	var v_address = '';

	if (v_is_secure)
		v_address = 'wss://' + window.location.hostname;
	else
		v_address = 'ws://' + window.location.hostname;

	v_queryWebSocket  = createWebSocket(
		v_address,
		p_port,
		function(p_event) {//Open
			sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Login, v_user_key, false);
		},
		function(p_message, p_context) {//Message
			var v_message = p_message;

			switch(v_message.v_code) {
				case parseInt(v_queryResponseCodes.SessionMissing): {
					showAlert('Session not found please reload the page.');
					break;
				}
				case parseInt(v_queryResponseCodes.QueryResult): {
					querySQLReturn(v_message,p_context);
					break;
				}
				case parseInt(v_queryResponseCodes.QueryEditDataResult): {
					queryEditDataReturn(v_message,p_context);
					break;
				}
				case parseInt(v_queryResponseCodes.SaveEditDataResult): {
					saveEditDataReturn(v_message,p_context);
					break;
				}
				default: {
					break;
				}
			}
		},
		function(p_event) {//Close
			showError('The connection with query server was closed.<br>WebSocket error code: ' + p_event.code + '.<br>Reconnected.');
			startQueryWebSocket(p_port);
		},
		function(p_event) {//Error
			showError('An error has occurred during the communication with the query server.');
		}
	);

}
