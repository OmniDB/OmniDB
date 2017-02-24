/// <summary>
/// Transaction codes of client requests.
/// </summary>
var v_chatRequestCodes = {
	Login: '0',
	GetOldMessages: '1',
	ViewMessage: '2',
	SendMessage: '3',
	Writing: '4',
	NotWriting: '5'
}

/// <summary>
/// Transaction codes of server responses.
/// </summary>
var v_chatResponseCodes = {
	OldMessages: '0',
	NewMessage: '1',
	UserList: '2',
	UserWriting: '3',
	UserNotWriting: '4'
}

/// <summary>
/// Global Variable to say if user is or is not writing a message
/// </summary>
var v_wasWriting = false;

/// <summary>
/// The variable that will receive the WebSocket object.
/// </summary>
var v_chatWebSocket;

/// <summary>
/// Sends a message from an user to chat server.
/// </summary>
function sendMessage() {
	var v_textarea = document.getElementById('textarea_chat_message');
	sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SendMessage, v_textarea.value, false);
	v_textarea.value = '';
}

/// <summary>
/// Builds the list of users, online and offline, in OmniChat.
/// </summary>
/// <param name="p_userList">The user list received from the server.</param>
function buildUserList(p_userList) {
	var v_chatLeftPanel = document.getElementById('div_chat_left_panel');
	v_chatLeftPanel.innerHTML = '';

	var v_userList = p_userList;
	for(var i = 0; i < v_userList.length; i++) {
		var v_userDiv = document.createElement('div');
		v_userDiv.id = 'chat_user_' + v_userList[i].v_user_id;
		v_userDiv.classList.add('div_user');

		var v_userStatusDiv = document.createElement('div');
		v_userStatusDiv.classList.add('div_user_status');
		v_userDiv.appendChild(v_userStatusDiv);

		if(v_userList[i].v_user_online == 1) {
			var v_userOnline = document.createElement('img');
			v_userOnline.style.width = '9px';
			v_userOnline.src = 'images/status/status_F.png';

			v_userStatusDiv.appendChild(v_userOnline);
		}
		else {
			var v_userOnline = document.createElement('img');
			v_userOnline.style.width = '9px';
			v_userOnline.src = 'images/status/status_N.png';

			v_userStatusDiv.appendChild(v_userOnline);
		}

		var v_userNameDiv = document.createElement('div');
		v_userNameDiv.classList.add('div_user_name');
		v_userNameDiv.innerHTML = v_userList[i].v_user_name;
		v_userDiv.appendChild(v_userNameDiv);

		v_chatLeftPanel.appendChild(v_userDiv);
	}
}


/// <summary>
/// Function called when a chat client receives a user message.
/// </summary>
/// <param name="p_message">The message itself.</param>
function NewMessage(p_message) {
	var v_chatContent = document.getElementById('div_chat_content');

	var v_messageDiv = document.createElement('div');
	v_messageDiv.classList.add('div_message');

	var v_lastUser = null;
	var v_chatMessages = v_chatContent.children;

	for(var j = v_chatMessages.length - 1; j >= 0 && v_lastUser == null; j--) {
		if(v_chatMessages[j].firstChild.classList.contains('div_message_user')) {
			v_lastUser = v_chatMessages[j].firstChild.innerHTML;
		}
	}

	if(v_lastUser != p_message.v_user_name) {
		var v_messageUser = document.createElement('div');
		v_messageUser.classList.add('div_message_user');
		v_messageUser.innerHTML = p_message.v_user_name;
		v_messageDiv.appendChild(v_messageUser);

		var v_messageTime = document.createElement('div');
		v_messageTime.classList.add('div_message_time');
		v_messageTime.innerHTML = '(' + p_message.v_timestamp.substring(11, 16) + ') ';
		v_messageDiv.appendChild(v_messageTime);
	}

	var v_messageText = document.createElement('div');
	v_messageText.classList.add('div_message_text');
	v_messageText.innerHTML = p_message.v_text;
	v_messageDiv.appendChild(v_messageText);

	v_chatContent.appendChild(v_messageDiv);
	v_chatContent.scrollTop = v_chatContent.scrollHeight;

	var v_chatDetails = document.getElementById('div_chat_details');
	if(v_chatDetails.style.height == '0px') {
		var v_chatHeader = document.getElementById('div_chat_header');

		if(typeof messageNotification != 'undefined' && messageNotification != null) {
			clearInterval(messageNotification);
		}

		messageNotification = setInterval(
			function() {
				if(v_chatHeader.style.backgroundColor == 'rgb(74, 104, 150)') {
					v_chatHeader.style.backgroundColor = 'rgb(255, 147, 15)';
				}
				else {
					v_chatHeader.style.backgroundColor = 'rgb(74, 104, 150)';
				}
			},
			400
		);
	}

	if(v_browserTabActive) {
		document.title = 'OmniDB';
	}
	else {
		document.title = 'OmniDB (!)';
	}

	sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.ViewMessage, p_message, false);
}

/// <summary>
/// Function called when a user clicks on its chat header
/// </summary>
function clickChatHeader() {
	var v_chatDetails = document.getElementById('div_chat_details');

	if(v_chatDetails.style.height == '0px') {
		for(var i = 0; i < v_chatDetails.children.length; i++) {
			v_chatDetails.children[i].style.display = '';
		}

		setTimeout(
			function() {
				document.getElementById('button_chat_send_message').innerHTML = 'Send';
			},
			150
		);

		v_chatDetails.style.height = '315px';
		document.getElementById('div_chat_header').style.backgroundColor = 'rgb(74, 104, 150)';

		if(typeof messageNotification != 'undefined' && messageNotification != null) {
			clearInterval(messageNotification);
		}
	}
	else {
		v_chatDetails.style.height = '0px';

		setTimeout(
			function() {
				for(var i = 0; i < v_chatDetails.children.length; i++) {
					v_chatDetails.children[i].style.display = 'none';
				}
			},
			350
		);

		setTimeout(
			function() {
				document.getElementById('button_chat_send_message').innerHTML = '';
			},
			150
		);
	}
}

/// <summary>
/// Starts chat server
/// </summary>
/// <param name="p_port">Port where chat will listen for connections.</param>
function startChatWebSocket(p_port) {
	v_chatWebSocket  = createWebSocket(
		'ws://' + window.location.hostname,
		p_port,
		function(p_event) {//Open
			sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.Login, v_user_id, false);
			sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.GetOldMessages, v_user_id, false);
		},
		function(p_event) {//Message
			var v_message = JSON.parse(p_event.data);

			if(v_message.v_error) {
				showError('An error message has been received from the server:  <br>' + v_message.v_data);
				return;
			}

			switch(v_message.v_code) {
				case parseInt(v_chatResponseCodes.OldMessages): {
					for(var i = 0; i < v_message.v_data.length; i++) {
						NewMessage(v_message.v_data[i]);
					}

					break;
				}
				case parseInt(v_chatResponseCodes.NewMessage): {
					NewMessage(v_message.v_data);
					break;
				}
				case parseInt(v_chatResponseCodes.UserList): {
					buildUserList(v_message.v_data);

					break;
				}
				case parseInt(v_chatResponseCodes.UserWriting): {
					var v_userDiv = document.getElementById('chat_user_' + v_message.v_data);

					if(typeof v_userDiv != 'undefined' && v_userDiv != null && v_userDiv.childNodes.length > 0) {
						var v_lastChild = v_userDiv.childNodes[v_userDiv.childNodes.length -1];

						if(!v_lastChild.classList.contains('div_user_writing')) {
							var v_img = document.createElement('img');
							v_img.src = 'images/icons/bubble_64.png';
							v_img.style.width = '15px';

							var v_div = document.createElement('div');
							v_div.classList.add('div_user_writing');
							v_div.appendChild(v_img);

							v_userDiv.appendChild(v_div);
						}
					}

					break;
				}
				case parseInt(v_chatResponseCodes.UserNotWriting): {
					var v_userDiv = document.getElementById('chat_user_' + v_message.v_data);

					if(typeof v_userDiv != 'undefined' && v_userDiv != null && v_userDiv.childNodes.length > 0) {
						var v_lastChild = v_userDiv.childNodes[v_userDiv.childNodes.length -1];

						if(v_lastChild.classList.contains('div_user_writing')) {
							v_userDiv.removeChild(v_lastChild);
						}
					}

					break;
				}
				default: {
					break;
				}
			}
		},
		function(p_event) {//Close
			showError('The connection with chat server was closed.<br>WebSocket error code: ' + p_event.code + '.');
		},
		function(p_event) {//Error
			showError('An error has occurred during the communication with the chat server.');
		}
	);

	var v_textarea = document.getElementById('textarea_chat_message');
	v_textarea.value = '';
	v_textarea.onkeydown = function(event) {
		if(event.keyCode == 13) {//Enter
			sendMessage();
			event.preventDefault();
			event.stopPropagation();
		}
	}

	v_textarea.onkeyup = function(event) {
		if(this.value.length > 0 && !v_wasWriting) {
			v_wasWriting = true;
			sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.Writing, '', false);
		}
		else if(this.value.length == 0 && v_wasWriting) {
			v_wasWriting = false;
			sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.NotWriting, '', false);
		}
	}
}