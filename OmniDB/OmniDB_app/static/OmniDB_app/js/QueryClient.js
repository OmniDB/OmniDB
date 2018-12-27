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
	CancelThread: 6,
	Debug: 7,
	CloseTab: 8,
	DataMining: 9,
	Console: 10
}

/// <summary>
/// Transaction codes of server responses.
/// </summary>
var v_queryResponseCodes = {
	LoginResult: 0,
	QueryResult: 1,
	QueryEditDataResult: 2,
	SaveEditDataResult: 3,
	SessionMissing: 4,
	PasswordRequired: 5,
	QueryAck: 6,
	MessageException: 7,
	DebugResponse: 8,
	RemoveContext: 9,
	DataMiningResult: 10,
	ConsoleResult: 11
}

/// <summary>
/// The variable that will receive the WebSocket object.

/// </summary>
var v_queryWebSocket;

var v_ws_offline = document.getElementById('websocket_status_offline');
var v_ws_connecting = document.getElementById('websocket_status_connecting');
var v_ws_online = document.getElementById('websocket_status_online');

function setStatusIcon(p_mode) {
	var v_img = document.getElementById('websocket_status');
	v_ws_offline.style.display = 'none';
	v_ws_connecting.style.display = 'none';
	v_ws_online.style.display = 'none';
	if (p_mode == 0)
		v_ws_offline.style.display = '';
	else if (p_mode == 1)
		v_ws_connecting.style.display = '';
	else if (p_mode == 2)
		v_ws_online.style.display = '';
}

/// <summary>
/// Starts query client
/// </summary>
/// <param name="p_port">Port where chat will listen for connections.</param>
function startQueryWebSocket(p_port) {

	setStatusIcon(1);

	var v_address = '';
	var v_channel = '';

	var v_secure = false;
	if (window.location.protocol == "https:")
		v_secure  = true;

	var v_port = v_query_port_external;
	if (p_port)
		v_port = p_port;

	if (v_secure) {
		v_address = 'wss://' + window.location.hostname;
		v_channel = 'wss';
	}
	else {
		v_address = 'ws://' + window.location.hostname;
		v_channel = 'ws';
	}

	v_queryWebSocket  = createWebSocket(
		v_address,
		v_port,
		function(p_event) {//Open
			sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Login, v_user_key, false);
			setStatusIcon(2);
		},
		function(p_message, p_context, p_context_code) {//Message
			var v_message = p_message;

			switch(v_message.v_code) {
				case parseInt(v_queryResponseCodes.SessionMissing): {
					showAlert('Session not found please reload the page.');
					break;
				}
				case parseInt(v_queryResponseCodes.MessageException): {
					showError(p_message.v_data);
					break;
				}
				case parseInt(v_queryResponseCodes.PasswordRequired): {
					if (p_context) {
						SetAcked(p_context);
						QueryPasswordRequired(p_context,v_message.v_data);
						break;
					}
				}
				case parseInt(v_queryResponseCodes.QueryAck): {
					if (p_context) {
						SetAcked(p_context);
						break;
					}
				}
				case parseInt(v_queryResponseCodes.QueryResult): {
					if (p_context) {
						SetAcked(p_context);
						if (!v_message.v_error || v_message.v_data.v_chunks) {
							p_context.tab_tag.tempData = p_context.tab_tag.tempData.concat(v_message.v_data.v_data);
						}
						if (!v_message.v_data.v_chunks || v_message.v_data.v_last_block || v_message.v_error) {
							v_message.v_data.v_data = [];
							querySQLReturn(v_message,p_context);
							//Remove context
							removeContext(v_queryWebSocket,p_context_code);
						}

					}
					break;
				}
				case parseInt(v_queryResponseCodes.ConsoleResult): {
					if (p_context) {
						if (!v_message.v_error) {
							p_context.tab_tag.tempData = p_context.tab_tag.tempData += v_message.v_data.v_data;
						}
						if (v_message.v_data.v_last_block || v_message.v_error) {
							v_message.v_data.v_data = [];
							consoleReturn(v_message,p_context);
							//Remove context
							removeContext(v_queryWebSocket,p_context_code);
						}
					}
					break;
				}
				case parseInt(v_queryResponseCodes.QueryEditDataResult): {
					if (p_context) {
						SetAcked(p_context);
						queryEditDataReturn(v_message,p_context);
						removeContext(v_queryWebSocket,p_context_code);
					}
					break;
				}
				case parseInt(v_queryResponseCodes.SaveEditDataResult): {
					if (p_context) {
						saveEditDataReturn(v_message,p_context);
						removeContext(v_queryWebSocket,p_context_code);
					}
					break;
				}
				case parseInt(v_queryResponseCodes.DebugResponse): {
					if (p_context) {
						SetAcked(p_context);
						debugResponse(p_message, p_context);
						if (p_message.v_data.v_remove_context) {
							removeContext(v_queryWebSocket,p_context_code);
						}
					}
					break;
				}
				case parseInt(v_queryResponseCodes.RemoveContext): {
					if (p_context) {
						removeContext(v_queryWebSocket,p_context_code);
					}
					break;
				}
				default: {
					break;
				}
				case parseInt(v_queryResponseCodes.DataMiningResult): {
					if (p_context) {
						SetAcked(p_context);
						dataMiningReturn(v_message, p_context);
						//Remove context
						removeContext(v_queryWebSocket,p_context_code);
					}
					break;
				}
			}
		},
		function(p_event) {//Close
			//showError('The connection with query server was closed.<br>WebSocket error code: ' + p_event.code + '.<br>Reconnected.');
			//startQueryWebSocket(p_port);

			setStatusIcon(0);

			if (!p_port) {
				startQueryWebSocket(v_query_port);
			}
			else {
				showAlert(
					'Cannot connect to websocket server with ports ' + v_query_port_external + ' (external) and ' + v_query_port + ' (internal). Trying again in 5 seconds...'
				,function() {
					setTimeout(function() {
						startQueryWebSocket();
					},5000);
				})
			}
		},
		function(p_event) {//Error
			//showError('An error has occurred during the communication with the query server.');
		},
		v_channel
	);

}

function SetAcked(p_context) {
	if (p_context)
		p_context.acked = true;
}

function QueryPasswordRequired(p_context, p_message) {
	if (p_context.tab_tag.mode=='query') {
		showPasswordPrompt(
			p_context.database_index,
			function() {
				cancelSQLTab(p_context.tab_tag);
				//querySQL(p_context.mode);
				querySQL(p_context.mode,
								 p_context.all_data,
								 p_context.query,
								 p_context.callback,
								 p_context.log_query,
								 p_context.save_query,
								 p_context.cmd_type,
								 p_context.clear_data,
								 p_context.tab_title);
			},
			function() {
				cancelSQLTab(p_context.tab_tag);
			},
			p_message
		);
	}
	else if (p_context.tab_tag.mode=='edit') {
		showPasswordPrompt(
			p_context.database_index,
			function() {
				cancelEditDataTab(p_context.tab_tag);
				//queryEditData();
			},
			function() {
				cancelEditDataTab(p_context.tab_tag);
			},
			p_message
		);
	}
	else if (p_context.tab_tag.mode=='console') {
		showPasswordPrompt(
			p_context.database_index,
			function() {
				cancelConsoleTab(p_context.tab_tag);
				p_context.tab_tag.editor_input.setValue(p_context.tab_tag.last_command);
        p_context.tab_tag.editor_input.clearSelection();
				consoleSQL(p_context.check_command,
									 p_context.mode);
			},
			function() {
				cancelConsoleTab(p_context.tab_tag);
			},
			p_message
		);
	}
}
