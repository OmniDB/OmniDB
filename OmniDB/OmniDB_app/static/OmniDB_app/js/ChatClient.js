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
var v_chatRequestCodes = {
	Login: 0,
	GetOldMessages: 1,
	sendText: 2,
	Writing: 3,
	NotWriting: 4,
	SendImage: 5
}

/// <summary>
/// Transaction codes of server responses.
/// </summary>
var v_chatResponseCodes = {
	OldMessages: 0,
	NewMessage: 1,
	UserList: 2,
	UserWriting: 3,
	UserNotWriting: 4,
	LoginError: 5
}

/// <summary>
/// Global Variable to say if user is or is not writing a message
/// </summary>
var v_wasWriting = false;

/// <summary>
/// Global Variable to say how many old messages the user has requested to the chat server
/// </summary>
var v_oldMessagesRequested = 0;

/// <summary>
/// Global Variable to say if it's the first time the chat receive old messages
/// </summary>
var v_firstOldMessages = true;

/// <summary>
/// The variable that will receive the WebSocket object.
/// </summary>
var v_chatWebSocket;

/// <summary>
/// Stops blinking effect of new message notification.
/// </summary>
function stopMessageNotification() {
	if(typeof messageNotification != 'undefined' && messageNotification != null) {
		clearInterval(messageNotification);

		var v_chatHeader = document.getElementById('div_chat_header');

		if(v_chatHeader.classList.contains('div_chat_header_blink')) {
			v_chatHeader.classList.remove('div_chat_header_blink');
		}
	}
}

/// <summary>
/// Sends a text message from an user to chat server.
/// </summary>
function sendText() {
	var v_textarea = document.getElementById('textarea_chat_message');
	sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.sendText, v_textarea.value, false);
	v_textarea.value = '';
}

/// <summary>
/// Sends a image message from an user to chat server.
/// </summary>
/// <param name="p_url">The image url.</param>
function sendImage(p_url) {
	sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SendImage, p_url, false);
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
			v_userOnline.src = '/static/OmniDB_app/images/status/status_F.png';

			v_userStatusDiv.appendChild(v_userOnline);
		}
		else {
			var v_userOnline = document.createElement('img');
			v_userOnline.style.width = '9px';
			v_userOnline.src = '/static/OmniDB_app/images/status/status_N.png';

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

	var v_scrollAtBottom = false;

	if((v_chatContent.scrollTop + v_chatContent.offsetHeight) == v_chatContent.scrollHeight) {
		v_scrollAtBottom = true;
	}

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

	if(p_message.v_image) {
		var v_messageImage = document.createElement('div');
		v_messageImage.classList.add('div_message_image');
		v_messageImage.style.backgroundImage = 'url(' + p_message.v_text + ')';
		v_messageImage.setAttribute('src', p_message.v_text);

		v_messageImage.addEventListener(
			'click',
			function(p_event) {
				var v_divShowImage = document.createElement('div');
				v_divShowImage.classList.add('div_show_img');

				v_divShowImage.addEventListener(
					'click',
					function(p_event) {
						this.parentElement.removeChild(this);
					}
				);

				var v_divContainerImg = document.createElement('div');
				v_divContainerImg.classList.add('div_container_img');

				var v_imgShowImage = document.createElement('img');
				v_imgShowImage.classList.add('img_show_img');
				v_imgShowImage.src = this.getAttribute('src');

				v_divContainerImg.appendChild(v_imgShowImage);
				v_divShowImage.appendChild(v_divContainerImg);
				document.body.appendChild(v_divShowImage);
			}
		);

		v_messageDiv.appendChild(v_messageImage);
	}
	else {
		var v_messageText = document.createElement('div');
		v_messageText.classList.add('div_message_text');
		v_messageText.innerHTML = p_message.v_text;
		v_messageDiv.appendChild(v_messageText);
	}

	v_chatContent.appendChild(v_messageDiv);

	if(v_scrollAtBottom) {
		v_chatContent.scrollTop = v_chatContent.scrollHeight - v_chatContent.offsetHeight;
	}

	var v_chatDetails = document.getElementById('div_chat_details');

	if(((v_chatDetails.style.height == '0px') || (!v_scrollAtBottom)) && (!(v_user_name == p_message.v_user_name))) {
		var v_chatHeader = document.getElementById('div_chat_header');

		stopMessageNotification();

		messageNotification = setInterval(
			function() {
				if(v_chatHeader.classList.contains('div_chat_header_blink')) {
					v_chatHeader.classList.remove('div_chat_header_blink');
				}
				else {
					v_chatHeader.classList.add('div_chat_header_blink');
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
}

/// <summary>
/// Function called when a chat client receives a list of old messages.
/// </summary>
/// <param name="p_messageList">The message list.</param>
function OldMessages(p_messageList) {
	if(p_messageList.length > 0) {
		var v_lastUser = '';

		var v_fakeDiv = document.createElement('div');

		for(var i = p_messageList.length - 1; i >= 0; i--) {
			var v_messageDiv = document.createElement('div');
			v_messageDiv.classList.add('div_message');

			if(v_lastUser != p_messageList[i].v_user_name) {
				var v_messageUser = document.createElement('div');
				v_messageUser.classList.add('div_message_user');
				v_messageUser.innerHTML = p_messageList[i].v_user_name;
				v_messageDiv.appendChild(v_messageUser);

				var v_messageTime = document.createElement('div');
				v_messageTime.classList.add('div_message_time');
				v_messageTime.innerHTML = '(' + p_messageList[i].v_timestamp.substring(11, 16) + ') ';
				v_messageDiv.appendChild(v_messageTime);

				v_lastUser = p_messageList[i].v_user_name;
			}

			if(p_messageList[i].v_image) {
				var v_messageImage = document.createElement('div');
				v_messageImage.classList.add('div_message_image');
				v_messageImage.style.backgroundImage = 'url(' + p_messageList[i].v_text + ')';
				v_messageImage.setAttribute('src', p_messageList[i].v_text);

				v_messageImage.addEventListener(
					'click',
					function(p_event) {
						var v_divShowImage = document.createElement('div');
						v_divShowImage.classList.add('div_show_img');

						v_divShowImage.addEventListener(
							'click',
							function(p_event) {
								this.parentElement.removeChild(this);
							}
						);

						var v_divContainerImg = document.createElement('div');
						v_divContainerImg.classList.add('div_container_img');

						var v_imgShowImage = document.createElement('img');
						v_imgShowImage.classList.add('img_show_img');
						v_imgShowImage.src = this.getAttribute('src');

						v_divContainerImg.appendChild(v_imgShowImage);
						v_divShowImage.appendChild(v_divContainerImg);
						document.body.appendChild(v_divShowImage);
					}
				);

				v_messageDiv.appendChild(v_messageImage);
			}
			else {
				var v_messageText = document.createElement('div');
				v_messageText.classList.add('div_message_text');
				v_messageText.innerHTML = p_messageList[i].v_text;
				v_messageDiv.appendChild(v_messageText);
			}

			v_fakeDiv.appendChild(v_messageDiv);
		}

		var v_chatContent = document.getElementById('div_chat_content');
		var v_messageList = v_fakeDiv.childNodes;

		for(var i = v_messageList.length - 1; i >= 0; i--) {
			v_chatContent.insertBefore(v_messageList[i], v_chatContent.firstChild);
		}

		if(v_firstOldMessages) {
			v_chatContent.scrollTop = v_chatContent.scrollHeight - v_chatContent.offsetHeight;

			v_firstOldMessages = false;
		}

		v_fakeDiv = null;
	}
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

		stopMessageNotification();
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
/// Function called when a user scrolls the div that contains chat messages
/// </summary>
function scrollChatContent() {
	var v_chatContent = document.getElementById('div_chat_content');

	if(v_chatContent.scrollTop == 0) {
		sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.GetOldMessages, v_oldMessagesRequested, false);
		v_oldMessagesRequested += 20;
		v_chatContent.scrollTop = 1;
	}
	else if(v_chatContent.scrollTop == (v_chatContent.scrollHeight - v_chatContent.offsetHeight)){
		stopMessageNotification();
	}
}

/// <summary>
/// Textarea keydown event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function textareaKeyDown(p_event) {
	if(p_event.keyCode == 13) {//Enter
		sendText();
		p_event.preventDefault();
		p_event.stopPropagation();
	}
}

/// <summary>
/// Textarea keyup event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function textareaKeyUp(p_event) {
	if(this.value.length > 0 && !v_wasWriting) {
		v_wasWriting = true;
		sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.Writing, '', false);
	}
	else if(this.value.length == 0 && v_wasWriting) {
		v_wasWriting = false;
		sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.NotWriting, '', false);
	}
}

/// <summary>
/// Textarea paste event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function textareaPaste(p_event) {
	var v_items = (p_event.clipboardData || p_event.originalEvent.clipboardData).items;

	for(v_index in v_items) {
		var v_item = v_items[v_index];
		if(v_item.kind === 'file') {
			var v_blob = v_item.getAsFile();

			var v_reader = new FileReader();

			v_reader.onload = function(p_event) {
				var v_dataInfo = p_event.target.result.split(';')[0];

				if(v_dataInfo != null && (v_dataInfo.indexOf('image') != -1)) {
					p_event.preventDefault();
					p_event.stopPropagation();
					sendImage(p_event.target.result);
				}
			}

			v_reader.readAsDataURL(v_blob);
		}
	}
}

/// <summary>
/// Chat drag enter event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function chatDragEnter(p_event) {
	p_event.preventDefault();
	p_event.stopPropagation();
}

/// <summary>
/// Chat drag leave event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function chatDragLeave(p_event) {
	p_event.preventDefault();
	p_event.stopPropagation();
}

/// <summary>
/// Chat drag over event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function chatDragOver(p_event) {
	p_event.preventDefault();
	p_event.stopPropagation();
}

/// <summary>
/// Chat drop event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function chatDrop(p_event) {
	p_event.preventDefault();
	p_event.stopPropagation();

	for(var i = 0; i < p_event.dataTransfer.files.length; i++) {
		var v_blob = p_event.dataTransfer.files[i];

		var v_reader = new FileReader();

		v_reader.onload = function(p_event) {
			var v_dataInfo = p_event.target.result.split(';')[0];

			if(v_dataInfo != null && (v_dataInfo.indexOf('image') != -1)) {
				sendImage(p_event.target.result);
			}
		}

		v_reader.readAsDataURL(v_blob);
	}
}

/// <summary>
/// Button send message click event listener
/// </summary>
/// <param name="p_event">The event object.</param>
function clickSendMessage(p_event) {
	sendText();

	var v_textarea = document.getElementById('textarea_chat_message');

	//In order to remove "Writing" icon when sending messages by button click
	var v_keyboardEvent = new KeyboardEvent(
		'keyup',
		{
			bubbles : true,
			cancelable : true,
			shiftKey : false,
			ctrlKey: false,
			altKey: false,
			metaKey: false
		}
	);

	delete v_keyboardEvent.keyCode;
	Object.defineProperty(
		v_keyboardEvent,
		'keyCode',
		{'value' : 13}
	);

	v_textarea.dispatchEvent(v_keyboardEvent);

	v_textarea.focus();
}

/// <summary>
/// Starts chat server
/// </summary>
/// <param name="p_port">Port where chat will listen for connections.</param>
/// <param name="p_chatEnabled">If chat is enabled by user.</param>
function startChatWebSocket(p_port, p_chatEnabled) {
	v_chatWebSocket  = createWebSocket(
		'ws://' + window.location.hostname,
		p_port,
		function(p_event) {//Open
			sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.Login, v_user_key, false);
			sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.GetOldMessages, v_oldMessagesRequested, false);
			v_oldMessagesRequested += 20;
		},
		function(p_event) {//Message
			var v_message = p_event;

			if(v_message.v_error) {
				showError('An error message has been received from the server:  <br>' + v_message.v_data);
				return;
			}

			switch(v_message.v_code) {
				case parseInt(v_chatResponseCodes.OldMessages): {
					OldMessages(v_message.v_data);

					break;
				}
				case parseInt(v_chatResponseCodes.NewMessage): {
					NewMessage(v_message.v_data);
					break;
				}
				case parseInt(v_chatResponseCodes.UserList): {
					buildUserList(v_message.v_data);

					if(!v_chatWebSocket.chatEnabled) {
						v_chatWebSocket.close(1000);//Normal closing
					}

					break;
				}
				case parseInt(v_chatResponseCodes.UserWriting): {
					var v_userDiv = document.getElementById('chat_user_' + v_message.v_data);

					if(typeof v_userDiv != 'undefined' && v_userDiv != null && v_userDiv.childNodes.length > 0) {
						var v_lastChild = v_userDiv.childNodes[v_userDiv.childNodes.length -1];

						if(!v_lastChild.classList.contains('div_user_writing')) {
							var v_img = document.createElement('img');
							v_img.src = '/static/OmniDB_app/images/icons/bubble_64.png';
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
						var v_lastChild = v_userDiv.childNodes[v_userDiv.childNodes.length - 1];

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
			//console.log(p_event);
			//showError('The connection with chat server was closed.<br>WebSocket error code: ' + p_event.code + '.');
			if(p_event.code != 1000) {//1000: normal closing
				startChatWebSocket(p_port, p_chatEnabled);
			}
		},
		function(p_event) {//Error
			//console.log(p_event);
			//showError('An error has occurred during the communication with the chat server.');
			startChatWebSocket(p_port, p_chatEnabled);
		}
	);

	v_chatWebSocket.chatEnabled = p_chatEnabled;

	var v_textarea = document.getElementById('textarea_chat_message');
	v_textarea.value = '';

	v_textarea.removeEventListener('keydown', textareaKeyDown);
	v_textarea.addEventListener('keydown', textareaKeyDown);

	v_textarea.removeEventListener('keyup', textareaKeyUp);
	v_textarea.addEventListener('keyup', textareaKeyUp);

	v_textarea.removeEventListener('paste', textareaPaste);
	v_textarea.addEventListener('paste', textareaPaste);

	var v_chatDiv = document.getElementById('div_chat');

	v_chatDiv.removeEventListener('dragenter', chatDragEnter);
	v_chatDiv.addEventListener('dragenter', chatDragEnter);

	v_chatDiv.removeEventListener('dragleave', chatDragLeave);
	v_chatDiv.addEventListener('dragleave', chatDragLeave);

	v_chatDiv.removeEventListener('dragover', chatDragOver);
	v_chatDiv.addEventListener('dragover', chatDragOver);

	v_chatDiv.removeEventListener('drop', chatDrop);
	v_chatDiv.addEventListener('drop', chatDrop);

	document.getElementById('div_chat_header').removeEventListener('click', clickChatHeader);
	document.getElementById('div_chat_header').addEventListener('click', clickChatHeader);

	document.getElementById('button_chat_send_message').removeEventListener('click', clickSendMessage);
	document.getElementById('button_chat_send_message').addEventListener('click', clickSendMessage);

	document.getElementById('div_chat_content').removeEventListener('scroll', scrollChatContent);
	document.getElementById('div_chat_content').addEventListener('scroll', scrollChatContent);
}
