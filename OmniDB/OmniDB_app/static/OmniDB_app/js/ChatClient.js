/**
 * Create fadeIn and fadeOut functions. Put it in window.FX
 * Got from: https://codepen.io/gabrieleromanato/pen/frIwl
 */
(function() {
    var FX = {
        easing: {
            linear: function(progress) {
                return progress;
            },
            quadratic: function(progress) {
                return Math.pow(progress, 2);
            },
            swing: function(progress) {
                return 0.5 - Math.cos(progress * Math.PI) / 2;
            },
            circ: function(progress) {
                return 1 - Math.sin(Math.acos(progress));
            },
            back: function(progress, x) {
                return Math.pow(progress, 2) * ((x + 1) * progress - x);
            },
            bounce: function(progress) {
                for (var a = 0, b = 1, result; 1; a += b, b /= 2) {
                    if (progress >= (7 - 4 * a) / 11) {
                        return -Math.pow((11 - 6 * a - 11 * progress) / 4, 2) + Math.pow(b, 2);
                    }
                }
            },
            elastic: function(progress, x) {
                return Math.pow(2, 10 * (progress - 1)) * Math.cos(20 * Math.PI * x / 3 * progress);
            }
        },
        animate: function(options) {
            var start = new Date;
            var id = setInterval(function() {
                var timePassed = new Date - start;
                var progress = timePassed / options.duration;
                if (progress > 1) {
                    progress = 1;
                }
                options.progress = progress;
                var delta = options.delta(progress);
                options.step(delta);
                if (progress == 1) {
                    clearInterval(id);
                    options.complete();
                }
            }, options.delay || 10);
        },
        fadeOut: function(element, options) {
            var to = 1;
            this.animate({
                duration: options.duration,
                delta: function(progress) {
                    progress = this.progress;
                    return FX.easing.swing(progress);
                },
                complete: options.complete,
                step: function(delta) {
                    element.style.opacity = to - delta;
                }
            });
        },
        fadeIn: function(element, options) {
            var to = 0;
            this.animate({
                duration: options.duration,
                delta: function(progress) {
                    progress = this.progress;
                    return FX.easing.swing(progress);
                },
                complete: options.complete,
                step: function(delta) {
                    element.style.opacity = to + delta;
                }
            });
        }
    };
    window.FX = FX;
})()

/**
 * Converts all properties types of an object to string.
 * @param {object} p_data - the object of whose properties should be converted to string.
 */
function stringifyData(p_data) {
    for(var v_key in p_data) {
        if(typeof p_data[v_key] != 'object') {
            p_data[v_key] = String(p_data[v_key]);
        }
    }
}

/**
 * Changes a datetime format.
 * @param {object} p_date - The date to be formatted.
 * @returns {string} - The date in the following format: 'mm/dd/yyyy hh:mm:ss'.
 */
function formatTimestamp(p_date) {
    var v_dd = p_date.getDate();
    var v_mm = p_date.getMonth() + 1;
    var v_yyyy = p_date.getFullYear();
    var v_HH = p_date.getHours();
    var v_MM = p_date.getMinutes();
    var v_SS = p_date.getSeconds();

    if(v_dd < 10) {
        v_dd = '0' + v_dd;
    }

    if(v_mm < 10) {
        v_mm = '0' + v_mm;
    }

    if(v_HH < 10) {
        v_HH = '0' + v_HH;
    }

    if(v_MM < 10) {
        v_MM = '0' + v_MM;
    }

    if(v_SS < 10) {
        v_SS = '0' + v_SS;
    }

    return v_mm + '-' + v_dd + '-' + v_yyyy + ' ' + v_HH + ':' + v_MM + ':' + v_SS;
}

/**
 * Open a modal based on a given content.
 * @param {string} p_html - Modal content.
 * @returns {object} - The element corresponding to the created modal.
 */
 function openModal(p_html) {
    var v_modal = document.createElement('div');
    v_modal.classList.add('modal');

    var v_modalContent = document.createElement('div');
    v_modalContent.classList.add('modal_content');
    v_modalContent.innerHTML = p_html;
    v_modal.appendChild(v_modalContent);

    var v_modalClose = document.createElement('span');
    v_modalClose.classList.add('modal_close');
    v_modalClose.innerHTML = '&times;';

    v_modalClose.addEventListener(
        'click',
        function(p_modal, p_event) {
            p_modal.remove();
        }.bind(v_modalClose, v_modal)
    );

    v_modalContent.insertBefore(v_modalClose, v_modalContent.firstChild);

    document.body.appendChild(v_modal);

    return v_modal;
}

/// <summary>
/// Controls connection loss
/// </summary>
var v_chatPingTimeout = null;
var v_chatPingInterval = null;
var v_chatReconnecting = false;
var v_chatPingTries = 0;

/// <summary>
/// Controls websocket connection status
/// </summary>
/// <param name="p_status">the websocket connection status
/// <paramref name="p_status">Takes a string in 'red', 'yellow' or 'green'.
/// <param name="p_showPopUp">If we should show a popup to the user.
/// <paramref name="p_showPopUp">Takes a boolean.
function updateChatConnectionStatus(p_status, p_showPopUp) {
    var v_src = null;
    var v_title = null;
    var v_msg = null;

    switch(p_status) {
        case 'red': {
            v_src = '/static/OmniDB_app/images/icons/status_chat_offline.png';
            v_title = 'Connection Status: disconnected.';
            v_msg = 'Connection to the server was lost.';
            break;
        }
        case 'yellow': {
            v_src = '/static/OmniDB_app/images/icons/status_chat_reconnecting.png';
            v_title = 'Connection Status: trying to reconnect.';
            v_msg = 'Trying to reconnect to the server...';
            v_chatReconnecting = true;
            break;
        }
        case 'green': {
            v_src = '/static/OmniDB_app/images/icons/status_chat_online.png';
            v_title = 'Connection Status: conectado.';
            v_msg = 'A connection to the server was established..';
            v_chatReconnecting = false;
            break;
        }
        default: {
            return;
        }
    }

    var v_imgStatus = document.getElementById('chat_websocket_status');

    if(v_imgStatus != null) {
        v_imgStatus.src = v_src;
        v_imgStatus.title = v_title;
    }
    else {
        v_imgStatus = document.createElement('img');
        v_imgStatus.id = 'chat_websocket_status';
        v_imgStatus.src = v_src;
        v_imgStatus.title = v_title;
        v_imgStatus.style.width = '15px';
        v_imgStatus.style.height = '15px';
        v_imgStatus.style.marginBottom = '-3px';

        var v_headerContent = document.querySelector('#popup_chat #div_chat_user_info_login');

        if(v_headerContent != null) {
            v_headerContent.insertBefore(v_imgStatus, v_headerContent.firstChild);
        }
    }

    if(p_showPopUp) {
        $.fn.qtip.zindex = 10000000000;
        $('#chat_websocket_status').qtip({
            content: {
                text: v_msg,
                title: {
                    button: true,
                    text: 'Connection to the server.'
                }
            },
            style: {
                classes: 'qtip-' + p_status + ' qtip-websocket-connection'
            },
            show: {
                ready: true,
                solo: true
            },
            hide: false,
            events: {
                hide: function () {
                    $(this).qtip('destroy');
                }
            }
        });
    }
}

/**
 * Controls page popups.
 */
var gv_chatPopUpControl = null;

/**
 * Transaction codes of client requests.
 */
var v_chatRequestCodes = {
    Login: '0',
    SendGroupMessage: '1',
    RetrieveGroupHistory: '2',
    MarkGroupMessagesAsRead: '3',
    GetUserStatus: '4',
    SetGroupUserWriting: '5',
    ChangeGroupSilenceSettings: '6',
    RemoveGroupMessage: '7',
    UpdateGroupSnippetMessage: '8',
    UpdateGroupMessage: '9',
    SendChannelMessage: '10',
    RetrieveChannelHistory: '11',
    MarkChannelMessagesAsRead: '12',
    SetChannelUserWriting: '13',
    ChangeChannelSilenceSettings: '14',
    RemoveChannelMessage: '15',
    UpdateChannelSnippetMessage: '16',
    UpdateChannelMessage: '17',
    CreatePrivateChannel: '18',
    RenamePrivateChannel: '19',
    QuitPrivateChannel: '20',
    InvitePrivateChannelMembers: '21',
    Ping: '22',
    SetUserChatStatus: '23',
    SearchOldMessages: '24'
}

/**
 * Transaction codes of server responses.
 */
var v_chatResponseCodes = {
    LoginResult: '0',
    NewGroupMessage: '1',
    RetrievedGroupHistory: '2',
    MarkedGroupMessagesAsRead: '3',
    UserStatus: '4',
    GroupUserWriting: '5',
    GroupSilenceSettings: '6',
    RemovedGroupMessage: '7',
    UpdatedGroupSnippetMessage: '8',
    UpdatedGroupMessage: '9',
    NewChannelMessage: '10',
    RetrievedChannelHistory: '11',
    MarkedChannelMessagesAsRead: '12',
    ChannelUserWriting: '13',
    ChannelSilenceSettings: '14',
    RemovedChannelMessage: '15',
    UpdatedChannelSnippetMessage: '16',
    UpdatedChannelMessage: '17',
    NewPrivateChannel: '18',
    RenamedPrivateChannel: '19',
    QuittedPrivateChannel: '20',
    InvitedPrivateChannelMembers: '21',
    Pong: '22',
    UserChatStatus: '23',
    SearchedOldMessages: '24'
}

/**
 * The variable that will receive the WebSocket object.
 */
var v_chatWebSocket;

/**
 * Starts Chat WebSocket Client.
 * @param {integer} p_port - Port where v_chatWebSocket will connecto to. Takes an integer between 1024 and 65536.
 */
function startChatWebSocket(p_port) {
    if(!v_chatReconnecting) {
        updateChatConnectionStatus('red', false);
    }

    var v_address = '';
    var v_channel = '';

    if(v_is_secure) {
		v_address = 'wss://' + window.location.hostname;
        v_channel = 'chatwss';
    }
	else {
		v_address = 'ws://' + window.location.hostname;
        v_channel = 'chatws';
    }

    v_chatWebSocket  = createWebSocket(
        v_address,
        p_port,
        function(p_event) {//Open
            chatLogin();

            if(v_chatPingInterval != null) {
                clearInterval(v_chatPingInterval);
            }

            chatPing();

            v_chatPingInterval = setInterval(
                function() {
                    v_chatPingTries = 0;
                    chatPing();
                },
                30000
            );
        },
        function(p_message, p_context) {//Message
            if(p_message.v_error) {
                showError('An error message was received from the server:  <br>' + p_message.v_data);
                return;
            }

            switch(p_message.v_code) {
                case v_chatResponseCodes.LoginResult: {
                    chatLoginResult(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.NewGroupMessage: {
                    chatNewGroupMessage(p_message.v_data, p_context);
                    break;
                }
                case v_chatResponseCodes.RetrievedGroupHistory: {
                    chatRetrievedGroupHistory(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.MarkedGroupMessagesAsRead: {
                    chatMarkedGroupMessagesAsRead(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.UserStatus: {
                    chatUserStatus(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.GroupUserWriting: {
                    chatGroupUserWriting(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.GroupSilenceSettings: {
                    chatGroupSilenceSettings(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.RemovedGroupMessage: {
                    chatRemovedGroupMessage(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.UpdatedGroupSnippetMessage: {
                    chatUpdatedGroupSnippetMessage(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.UpdatedGroupMessage: {
                    chatUpdatedGroupMessage(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.NewChannelMessage: {
                    chatNewChannelMessage(p_message.v_data, p_context);
                    break;
                }
                case v_chatResponseCodes.RetrievedChannelHistory: {
                    chatRetrievedChannelHistory(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.MarkedChannelMessagesAsRead: {
                    chatMarkedChannelMessagesAsRead(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.ChannelUserWriting: {
                    chatChannelUserWriting(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.ChannelSilenceSettings: {
                    chatChannelSilenceSettings(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.RemovedChannelMessage: {
                    chatRemovedChannelMessage(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.UpdatedChannelSnippetMessage: {
                    chatUpdatedChannelSnippetMessage(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.UpdatedChannelMessage: {
                    chatUpdatedChannelMessage(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.NewPrivateChannel: {
                    chatNewPrivateChannel(p_message.v_data, p_context);
                    break;
                }
                case v_chatResponseCodes.RenamedPrivateChannel: {
                    chatRenamedPrivateChannel(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.QuittedPrivateChannel: {
                    chatQuittedPrivateChannel(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.InvitedPrivateChannelMembers: {
                    chatInvitedPrivateChannelMembers(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.Pong: {
                    chatPong(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.UserChatStatus: {
                    chatUserChatStatus(p_message.v_data);
                    break;
                }
                case v_chatResponseCodes.SearchedOldMessages: {
                    chatSearchedOldMessages(p_message.v_data);
                    break;
                }
            }
        },
        function(p_event) {//Close
            console.log(p_event);

            if(v_chatPingTries == 3) {
                updateChatConnectionStatus('yellow', true);

                setTimeout(
                    function() {
                        startChatWebSocket(gv_chatWebSocketPort);
                    },
                    3000
                );
            }
            else {
                updateChatConnectionStatus('red', true);
            }
        },
        function(p_event) {//Error
            updateChatConnectionStatus('red', true);
        },
        v_channel
    );
}

/**
 * Function executed after page load.
 */
$(document).ready(function() {
    if(!gv_desktopMode) {
        //Configure popup component
        gv_chatPopUpControl = createPopUpControl('chat', 1000000);

        gv_chatPopUpControl.getChatPopUp = function() {
            for(var i = 0; i < this.popUpList.length; i++) {
                if(this.popUpList[i].tag.mode == 'Chat') {
                    return this.popUpList[i];
                }
            }

            return null;
        };

        //Open a new connection to the server
        startChatWebSocket(gv_chatWebSocketPort);

        //Try to grant notification permission
        Notification.requestPermission();

        //Append history overlay to body
        var v_divHistory = document.createElement('div');
        v_divHistory.id = 'div_history';
        v_divHistory.innerHTML = 'Retrieving history...';
        document.body.appendChild(v_divHistory);
    }
});

/**
 * Sends a login message to server.
 */
function chatLogin() {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.Login, v_session_key, false);
}

/**
 * Sends a send group message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {messageAttachmentName, messageTitle, messageType, messageContent, messageRawContent, groupCode, messageSnippetMode, mentionedMessageContent, commentMessageContent, commentMessageRawContent, forwardMessageCode}.
 * @param {object} p_context - some useful javascript object that can be used for controls.
 */
function chatSendGroupMessage(p_data, p_context) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SendGroupMessage, p_data, false, p_context);
}

/**
 * Sends a retrieve group history message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {groupCode, offset, fromMessageCode}.
 */
function chatRetrieveGroupHistory(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.RetrieveGroupHistory, p_data, false);
    document.getElementById('div_history').style.display = 'block';
}

/**
 * Sends a mark group messages as read message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {groupCode, messageCodeList}.
 */
function chatMarkGroupMessagesAsRead(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.MarkGroupMessagesAsRead, p_data, false);
}

/**
 * Sends a get user status message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {userCode}.
 */
function chatGetUserStatus(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.GetUserStatus, p_data, false);
}

/**
 * Sends a set group user writing message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {groupCode, userCode, userWriting}.
 */
function chatSetGroupUserWriting(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SetGroupUserWriting, p_data, false);
}

/**
 * Sends a change group silence settings message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {groupCode, silenceGroup}.
 */
function chatChangeGroupSilenceSettings(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.ChangeGroupSilenceSettings, p_data, false);
}

/**
 * Sends a remove group message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {groupCode, messageCode}.
 */
function chatRemoveGroupMessage(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.RemoveGroupMessage, p_data, false);
}

/**
 * Sends an update group snippet message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {snippetTitle, snippetContent, snippetMode, messageCode, groupCode}.
 */
function chatUpdateGroupSnippetMessage(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.UpdateGroupSnippetMessage, p_data, false);
}

/**
 * Sends an update group message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {messageContent, messageRawContent, messageCode, groupCode}.
 */
function chatUpdateGroupMessage(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.UpdateGroupMessage, p_data, false);
}

/**
 * Sends a send channel message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {messageAttachmentName, messageTitle, messageType, messageContent, messageRawContent, channelCode, messageSnippetMode, mentionedMessageContent, commentMessageContent, commentMessageRawContent, forwardMessageCode}.
 * @param {object} p_context - some useful javascript object that can be used for controls.
 */
function chatSendChannelMessage(p_data, p_context) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SendChannelMessage, p_data, false, p_context);
}

/**
 * Sends a retrieve channel history message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, offset, fromMessageCode}.
 */
function chatRetrieveChannelHistory(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.RetrieveChannelHistory, p_data, false);
    document.getElementById('div_history').style.display = 'block';
}

/**
 * Sends a mark channel messages as read message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, messageCodeList}.
 */
function chatMarkChannelMessagesAsRead(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.MarkChannelMessagesAsRead, p_data, false);
}

/**
 * Sends a set channel user writing message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, userCode, userWriting}.
 */
function chatSetChannelUserWriting(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SetChannelUserWriting, p_data, false);
}

/**
 * Sends a change channel silence settings message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, silenceChannel}.
 */
function chatChangeChannelSilenceSettings(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.ChangeChannelSilenceSettings, p_data, false);
}

/**
 * Sends a remove channel message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, messageCode}.
 */
function chatRemoveChannelMessage(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.RemoveChannelMessage, p_data, false);
}

/**
 * Sends an update channel snippet message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {snippetTitle, snippetContent, snippetMode, messageCode, channelCode}.
 */
function chatUpdateChannelSnippetMessage(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.UpdateChannelSnippetMessage, p_data, false);
}

/**
 * Sends an update channel message message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {messageContent, messageRawContent, messageCode, channelCode}.
 */
function chatUpdateChannelMessage(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.UpdateChannelMessage, p_data, false);
}

/**
 * Sends a create private channel message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelName}.
 * @param {object} p_context - some useful javascript object that can be used for controls.
 */
function chatCreatePrivateChannel(p_data, p_context) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.CreatePrivateChannel, p_data, false, p_context);
}

/**
 * Sends a rename private channel message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, channelName}.
 */
function chatRenamePrivateChannel(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.RenamePrivateChannel, p_data, false);
}

/**
 * Sends a quit private channel message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode}.
 */
function chatQuitPrivateChannel(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.QuitPrivateChannel, p_data, false);
}

/**
 * Sends an invte private channel members message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {channelCode, userCodeList}.
 */
function chatInvitePrivateChannelMembers(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.InvitePrivateChannelMembers, p_data, false);
}

/**
 * Sends a ping message to the server in order to verify if connections is still up.
 */
function chatPing() {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.Ping, null, false);

    v_chatPingTimeout = setTimeout(
        function() {
            if(v_chatPingInterval != null) {
                clearInterval(v_chatPingInterval);
            }

            v_chatPingTries = 0;
            updateChatConnectionStatus('yellow', true);

            v_chatPingInterval = setInterval(
                function() {
                    if(v_chatPingTries == 3) {
                        if(v_chatPingInterval != null) {
                            clearInterval(v_chatPingInterval);
                        }

                        v_chatWebSocket.close(1000);
                        return;
                    }

                    chatPing();
                    v_chatPingTries++;
                },
                10000
            );
        },
        5000
    );
}

/**
 * Sends a set user chat status message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {userChatStatusCode}.
 */
function chatSetUserChatStatus(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SetUserChatStatus, p_data, false);
}

/**
 * Sends a search old messages message to server.
 * @param {object} p_data - The message to be sent to the server. Structure: {textPattern}.
 */
function chatSearchOldMessages(p_data) {
    sendWebSocketMessage(v_chatWebSocket, v_chatRequestCodes.SearchOldMessages, p_data, false);
}

/**
 * Handles login result message received from the server.
 * @param {object} p_data - Some useful data sent by the server. Javascript object containing useful data along the code.
 */
function chatLoginResult(p_data) {
    //Remove old popups
    var v_popUpList = [];

    for(var i = 0; i < gv_chatPopUpControl.popUpList.length; i++) {
        v_popUpList.push(gv_chatPopUpControl.popUpList[i]);
        v_popUpList[i].close(true);
    }

    var v_config = {
        width: 'calc(100vw - 47px)',
        height: 'calc(100vh - 90px)',
        top: '0',
        left: '0',
        resizable: false,
        draggable: false,
        forceClose: true
    };

    var v_callbacks = null;

    var v_html =
        '<div id="div_chat_container">' +
        '    <div id="div_chat_left">' +
        '        <div id="div_chat_user_info">' +
        '            <div id="div_chat_user_info_header">' +
        '                OmniDB' +
        '            </div>' +
        '            <div id="div_chat_user_info_login">' +
        '                ' + v_user_login +
        '                <img id="img_user_chat_status" src="" class="img_user_status_icon" />' +
        '            </div>' +
        '        </div>' +
        '        <div id="div_chat_channels">' +
        '            <div class="div_chat_left_header">' +
        '                Channels' +
        '                <button id="button_create_private_channel" class="button_chat_left_header" title="Create a private channel">+</button>' +
        '                <div class="div_chat_left_header_filter_container">' +
        '                    <input type="text" id="input_channel_filter" class="form-control" title="Search by Channel name" placeholder="Type to filter..." />' +
        '                </div>' +
        '            </div>' +
        '            <div class="div_chat_left_content">' +
        '            </div>' +
        '        </div>' +
        '        <div id="div_chat_groups">' +
        '            <div class="div_chat_left_header">' +
        '                Private Messages' +
        '                <div class="div_chat_left_header_filter_container">' +
        '                    <input type="text" id="input_group_filter" class="form-control" title="Search by user login" placeholder="Type to filter..." />' +
        '                </div>' +
        '            </div>' +
        '            <div class="div_chat_left_content">' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '    <div id="div_chat_right">' +
        '        <div id="div_chat_right_left">' +
        '        </div>' +
        '        <div id="div_chat_right_right" class="display_hidden">' +
        '            <div id="div_chat_right_right_close">' +
        '                <button id="button_chat_right_right_close">X</button>' +
        '            </div>' +
        '            <div id="div_chat_right_right_content">' +
        '            </div>' +
        '        </div>' +
        '    </div>' +
        '</div>';

    var v_chatPopUp = gv_chatPopUpControl.addPopUp(
        'chat',//ID
        'OmniDB Chat',//Title
        v_html,//Content
        v_config,//Config
        v_callbacks//Callbacks
    );

    for(var i = 0; i < v_connTabControl.tabList.length; i++) {
        if(v_connTabControl.tabList[i].tag.mode == 'chat') {
            v_connTabControl.tabList[i].elementDiv.appendChild(v_chatPopUp.containerElement);

            break;
        }
    }

    document.getElementById('div_chat_user_info_login').addEventListener(
        'contextmenu',
        function(p_chatPopUp, p_event) {
            p_event.preventDefault();

            if(p_chatPopUp != null) {
                var v_contextMenu = document.createElement('div');
                v_contextMenu.classList.add('context_menu');
                v_contextMenu.style.top = p_event.pageY + 'px';
                v_contextMenu.style.left = p_event.pageX + 'px';
                v_contextMenu.tabIndex = '0';
                document.body.appendChild(v_contextMenu);
                v_contextMenu.focus();

                var v_contextMenuItem = document.createElement('div');
                v_contextMenuItem.classList.add('context_menu_item');
                v_contextMenuItem.innerHTML = 'Change Status';

                v_contextMenuItem.addEventListener(
                    'mouseenter',
                    function(p_event) {
                        this.children[1].style.top = '0px';
                        this.children[1].style.left = this.offsetWidth + 3 + 'px';
                        this.children[1].style.display = 'block';
                    }
                )

                v_contextMenuItem.addEventListener(
                    'mouseleave',
                    function(p_event) {
                        this.children[1].style.display = 'none';
                    }
                )

                v_contextMenu.appendChild(v_contextMenuItem);

                var v_arrowRight = document.createElement('div');
                v_arrowRight.classList.add('arrow_right');
                v_contextMenuItem.appendChild(v_arrowRight);

                var v_subContextMenu = document.createElement('div');
                v_subContextMenu.classList.add('context_menu');
                v_subContextMenu.style.display = 'none';
                v_subContextMenu.style.top =  '0px';
                v_subContextMenu.style.left = '200px';

                var v_subContextMenuItem = document.createElement('div');
                v_subContextMenuItem.classList.add('context_menu_item');
                v_subContextMenuItem.innerHTML = 'None';
                v_subContextMenuItem.value = 1;
                v_subContextMenu.appendChild(v_subContextMenuItem);

                var v_subContextMenuItem = document.createElement('div');
                v_subContextMenuItem.classList.add('context_menu_item');
                v_subContextMenuItem.innerHTML = '<img src="/static/OmniDB_app/images/icons/userstatus_chat_meeting.png" class="img_user_status_icon" />In a Meeting';
                v_subContextMenuItem.value = 2;
                v_subContextMenu.appendChild(v_subContextMenuItem);

                var v_subContextMenuItem = document.createElement('div');
                v_subContextMenuItem.classList.add('context_menu_item');
                v_subContextMenuItem.innerHTML = '<img src="/static/OmniDB_app/images/icons/userstatus_chat_homeoffice.png" class="img_user_status_icon" />Remote Work';
                v_subContextMenuItem.value = 3;
                v_subContextMenu.appendChild(v_subContextMenuItem);

                var v_subContextMenuItem = document.createElement('div');
                v_subContextMenuItem.classList.add('context_menu_item');
                v_subContextMenuItem.innerHTML = '<img src="/static/OmniDB_app/images/icons/userstatus_chat_busy.png" class="img_user_status_icon" />Busy';
                v_subContextMenuItem.value = 4;
                v_subContextMenu.appendChild(v_subContextMenuItem);

                var v_userStatusCode = null;

                var v_user = p_chatPopUp.tag.userList.getUserByCode(v_user_id);

                if(v_user != null) {
                    v_userStatusCode = v_user.status.code;
                }

                for(var i = 0; i < v_subContextMenu.children.length; i++) {
                    if(v_userStatusCode == v_subContextMenu.children[i].value) {
                        v_subContextMenu.children[i].classList.add('context_menu_item_disabled');
                    }

                    v_subContextMenu.children[i].addEventListener(
                        'click',
                        function(p_event) {
                            var v_data = {
                                userChatStatusCode: this.value
                            };

                            chatSetUserChatStatus(v_data);

                            this.parentElement.parentElement.parentElement.blur();
                        }
                    );
                }

                v_contextMenuItem.appendChild(v_subContextMenu);

                v_contextMenu.addEventListener(
                    'blur',
                    function(p_event) {
                        this.remove();
                    }
                );
            }
        }.bind(document.getElementById('div_chat_user_info_login'), v_chatPopUp)
    );

    document.getElementById('input_channel_filter').addEventListener(
        'keyup',
        function(p_event) {
            var v_value = this.value.toLowerCase();

            var v_channelItems = document.querySelectorAll('#div_chat_channels .div_chat_left_content_item');

            for(var i = 0; i < v_channelItems.length; i++) {
                v_channelItems[i].classList.remove('div_chat_left_content_item_hidden');

                if(v_channelItems[i].name.indexOf(v_value) == -1) {
                    v_channelItems[i].classList.add('div_chat_left_content_item_hidden');
                }
            }
        }
    );

    document.getElementById('input_group_filter').addEventListener(
        'keyup',
        function(p_event) {
            var v_value = this.value.toLowerCase();

            var v_groupItems = document.querySelectorAll('#div_chat_groups .div_chat_left_content_item');

            for(var i = 0; i < v_groupItems.length; i++) {
                v_groupItems[i].classList.remove('div_chat_left_content_item_hidden');

                if(v_groupItems[i].userName.indexOf(v_value) == -1 && v_groupItems[i].userLogin.indexOf(v_value) == -1) {
                    v_groupItems[i].classList.add('div_chat_left_content_item_hidden');
                }
            }
        }
    );

    document.getElementById('button_chat_right_right_close').addEventListener(
        'click',
        function(p_event) {
            var v_divChatRightRight = document.getElementById('div_chat_right_right');
            v_divChatRightRight.classList.add('display_hidden');

            var v_divChatRightRightContent = document.getElementById('div_chat_right_right_content');
            v_divChatRightRightContent.removeAttribute('style');
            v_divChatRightRightContent.innerHTML = '';
        }
    );

    document.addEventListener(
        'webkitfullscreenchange',
        function(p_chatPopUp, p_event) {
            if(document.webkitFullscreenElement == null) {//Not full screen
                if(p_chatPopUp != null) {
                    p_chatPopUp.changePosition(p_chatPopUp.config.defaultTop, p_chatPopUp.config.defaultLeft);
                }
            }
        }.bind(document, v_chatPopUp)
    );

    v_chatPopUp.tag.mode = 'Chat';
    v_chatPopUp.tag.userList = p_data.userList;

    v_chatPopUp.tag.userList.getUserByCode = function(p_userCode) {
        for(var i = 0; i < this.length; i++) {
            if(this[i].code == p_userCode) {
                return this[i];
            }
        }

        return null;
    };

    v_chatPopUp.tag.contextList = [];

    v_chatPopUp.tag.contextList.getContextByChannelCode = function(p_channelCode) {
        for(var i = 0; i < this.length; i++) {
            if(this[i].type = 1 && this[i].code == p_channelCode) {//Is channel and is the given channel
                return this[i];
            }
        }

        return null;
    };

    v_chatPopUp.tag.contextList.getContextByGroupCode = function(p_groupCode) {
        for(var i = 0; i < this.length; i++) {
            if(this[i].type = 2 && this[i].code == p_groupCode) {//Is group and is the given group
                return this[i];
            }
        }

        return null;
    };

    /*Removed while embeding chat to outer tab
    var v_headerMenu = document.querySelector('.header_menu > div > ul');

    if(v_headerMenu != null) {
        if(document.getElementById('chat_icon') == null) {
            var v_li = document.createElement('li');
            v_li.style.paddingRight = '10px';
            v_headerMenu.insertBefore(v_li, v_headerMenu.children[1]);

            var v_chatIcon = document.createElement('img');
            v_chatIcon.id = 'chat_icon';
            v_chatIcon.style.height = '16px';
            v_chatIcon.style.width = '16px';
            v_chatIcon.title = 'Show / Hide Chat PopUp'
            v_chatIcon.src = '/static/OmniDB_app/images/icons/header_chat_icon_active.png';

            /*Removed while embeding chat to outer tab
            v_chatIcon.addEventListener(
                'click',
                function(p_chatPopUp, p_event) {
                    if(p_chatPopUp != null) {
                        if(this.src.indexOf('inactive.png') != -1) {
                            this.src = '/static/OmniDB_app/images/icons/header_chat_icon_active.png';
                            p_chatPopUp.show();

                            var v_divLeftContent = document.getElementById('div_chat_right_left_content');

                            if(v_divLeftContent != null) {
                                v_divLeftContent.scrollTop += 50; //scrollTop is adjusted to correctly display notifications while hidden
                            }
                        }
                        else {
                            this.src = '/static/OmniDB_app/images/icons/header_chat_icon_inactive.png';
                            p_chatPopUp.hide();

                            var v_divLeftContent = document.getElementById('div_chat_right_left_content');

                            if(v_divLeftContent != null) {
                                v_divLeftContent.scrollTop -= 50; //scrollTop is adjusted to correctly display notifications while hidden
                            }
                        }
                    }
                }.bind(v_chatIcon, v_chatPopUp)
            );

            if(v_chatIcon.src.indexOf('inactive.png') != -1) {
                v_chatPopUp.hide();
            }
            else {
                v_chatPopUp.show();
            }

            v_chatIcon.addEventListener(
                'click',
                function(p_event) {
                    for(var i = 0; i < v_connTabControl.tabList.length; i++) {
                        if(v_connTabControl.tabList[i].tag.mode == 'chat') {
                            v_connTabControl.selectTab(v_connTabControl.tabList[i]);
                            break;
                        }
                    }
                }
            )

            v_li.appendChild(v_chatIcon);

            var v_chatSpan = document.createElement('span');
            v_chatSpan.id = 'chat_status';
            v_chatSpan.classList.add('badge');
            v_chatSpan.innerHTML = '0';
            v_li.appendChild(v_chatSpan);
        }
    }*/

    v_chatPopUp.maximizeElement.remove();
    v_chatPopUp.minimizeElement.remove();

    v_chatPopUp.contentElement.classList.add('popup-prevent-container-drag');
    var v_cloneNode = v_chatPopUp.closeElement.cloneNode(true);
    v_chatPopUp.closeElement.parentElement.insertBefore(v_cloneNode, v_chatPopUp.closeElement);
    v_chatPopUp.closeElement.remove();
    v_chatPopUp.closeElement = v_cloneNode;

    /*Removed while embeding chat to outer tab
    v_cloneNode.addEventListener(
        'click',
        function(p_chatIcon, p_event) {
            p_chatIcon.click();
        }.bind(v_cloneNode, v_chatIcon)
    );*/

    var v_buttonCreatePrivateChannel = document.getElementById('button_create_private_channel');

    v_buttonCreatePrivateChannel.addEventListener(
        'click',
        function(p_event) {
            var v_html =
                '<div id="div_create_channel_container">' +
                '    <span id="span_create_channel_name">Channel name: </span>' +
                '    <input type="text" id="input_create_channel_name" class="form-control" />' +
                '</div>' +
                '<div style="text-align: center;">' +
                '    <button id="button_create_channel_cancel">Cancel</button>' +
                '    <button id="button_create_channel_ok">Ok</button>' +
                '</div>';

            var v_modal = openModal(v_html);

            var v_buttonCancel = document.getElementById('button_create_channel_cancel');

            v_buttonCancel.addEventListener(
                'click',
                function(p_modal, p_event) {
                    p_modal.remove();
                }.bind(v_buttonCancel, v_modal)
            );

            var v_buttonOk = document.getElementById('button_create_channel_ok');

            v_buttonOk.addEventListener(
                'click',
                function(p_modal, p_event) {
                    var v_inputCreateChannelName = document.getElementById('input_create_channel_name');

                    if(v_inputCreateChannelName.value.length == 0) {
                        openModal('<div>Please, type the name of the channel to be created.</div>');
                        return;
                    }

                    var v_data = {
                        channelName: v_inputCreateChannelName.value
                    };

                    var v_context = {
                        userCode: v_user_id
                    };

                    chatCreatePrivateChannel(v_data, v_context);

                    p_modal.remove();
                }.bind(v_buttonOk, v_modal)
            );

            var v_inputCreateChannelName = document.getElementById('input_create_channel_name');

            v_inputCreateChannelName.addEventListener(
                'keydown',
                function(p_buttonOk, p_event) {
                    if(p_event.keyCode == 13) {//Enter
                        p_buttonOk.click();
                    }
                }.bind(v_inputCreateChannelName, v_buttonOk)
            );
        }
    );

    v_chatPopUp.tag.onlineUserCodeList = p_data.onlineUserCodeList;

    v_chatPopUp.tag.channelList = p_data.channelList;

    v_chatPopUp.tag.channelList.getChannelByCode = function(p_channelCode) {
        for(var i = 0; i < this.length; i++) {
            if(this[i].code == p_channelCode) {
                return this[i];
            }
        }

        return null;
    };

    for(var i = 0; i < v_chatPopUp.tag.channelList.length; i++) {
        v_chatPopUp.tag.channelList[i].messageList.getMessageByCode = function(p_messageCode) {
            for(var i = 0; i < this.length; i++) {
                if(this[i].code == p_messageCode) {
                    return this[i];
                }
            }

            return null;
        }

        v_chatPopUp.tag.channelList[i].messageList.removeMessageByCode = function(p_messageCode) {
            for(var i = 0; i < this.length; i++) {
                if(this[i].code == p_messageCode) {
                    this.splice(i, 1);
                    return;
                }
            }
        }
    }

    v_chatPopUp.tag.groupList = p_data.groupList;

    v_chatPopUp.tag.groupList.getGroupByCode = function(p_groupCode) {
        for(var i = 0; i < this.length; i++) {
            if(this[i].code == p_groupCode) {
                return this[i];
            }
        }

        return null;
    };

    for(var i = 0; i < v_chatPopUp.tag.groupList.length; i++) {
        v_chatPopUp.tag.groupList[i].messageList.getMessageByCode = function(p_messageCode) {
            for(var i = 0; i < this.length; i++) {
                if(this[i].code == p_messageCode) {
                    return this[i];
                }
            }

            return null;
        }

        v_chatPopUp.tag.groupList[i].messageList.removeMessageByCode = function(p_messageCode) {
            for(var i = 0; i < this.length; i++) {
                if(this[i].code == p_messageCode) {
                    this.splice(i, 1);
                    return;
                }
            }
        }
    }

    v_chatPopUp.tag.updateHeader = function() {
        var v_unreadMessages = 0;
        var v_badgeList = document.querySelectorAll('.div_chat_left_content_item > .badge');

        for(var i = 0; i < v_badgeList.length; i++) {
            v_unreadMessages += parseInt(v_badgeList[i].innerHTML);
        }

        var v_chatStatus = document.getElementById('chat_status');
        v_chatStatus.innerHTML = v_unreadMessages;

        if(v_unreadMessages > 0) {
            v_chatStatus.style.display = 'inline-block';
        }
        else {
            v_chatStatus.style.display = '';
        }
    };

    v_chatPopUp.tag.getUserChatStatusStyle = function(p_userCode) {
        var v_return = null;

        var v_user = this.userList.getUserByCode(p_userCode);

        if(v_user != null) {
            switch(v_user.status.code) {
                case 1: { //None
                    v_return = {
                        src: '',
                        title: '',
                        display: 'none'
                    };

                    break;
                }
                case 2: { //In a meeting
                    v_return = {
                        src: '/static/OmniDB_app/images/icons/userstatus_chat_meeting.png',
                        title: v_user.status.name,
                        display: ''
                    };

                    break;
                }
                case 3: { //Home office
                    v_return = {
                        src: '/static/OmniDB_app/images/icons/userstatus_chat_homeoffice.png',
                        title: v_user.status.name,
                        display: ''
                    };

                    break;
                }
                case 4: { //Busy
                    v_return = {
                        src: '/static/OmniDB_app/images/icons/userstatus_chat_busy.png',
                        title: v_user.status.name,
                        display: ''
                    };

                    break;
                }
            }
        }

        return v_return;
    };

    var v_style = v_chatPopUp.tag.getUserChatStatusStyle(v_user_id);

    if(v_style != null) {
        var v_imgUserChatStatus = document.getElementById('img_user_chat_status');

        if(v_imgUserChatStatus != null) {
            v_imgUserChatStatus.src = v_style.src;
            v_imgUserChatStatus.title = v_style.title;
            v_imgUserChatStatus.style.display = v_style.display;
        }
    }

    v_chatPopUp.tag.getRenderedChannelMessage = function(p_chatPopUp, p_channelCode, p_message, p_withHeader) {
        var v_item = document.createElement('div');
        v_item.messageCode = p_message.code;
        v_item.channelCode = p_channelCode;
        v_item.userCode = p_message.user.code;
        v_item.classList.add('div_chat_right_left_item');
        v_item.createdAt = p_message.createdAt;

        if(p_message.createdAt != p_message.updatedAt) {//Message was edited
            v_item.title = p_message.updatedAt + ' (Edited)';
        }
        else {
            v_item.title = p_message.createdAt;
        }

        var v_messageBody = document.createElement('div');
        v_messageBody.classList.add('div_chat_right_left_item_body');
        v_messageBody.classList.add('div_chat_right_left_item_body_padding');

        var v_messageContent = document.createElement('div');
        v_messageContent.classList.add('div_chat_right_left_item_content');

        switch(p_message.type) {
            case 1: { //Plain text
                v_messageContent.classList.add('div_chat_message_plain_text');
                v_messageContent.innerHTML = p_message.content;

                break;
            }
            case 2: { //Pasted image
                v_messageContent.classList.add('div_chat_message_pasted_img');
                v_messageContent.innerHTML = p_message.title;

                var v_img = document.createElement('img');
                v_img.src = gv_chatAttachmentPath + '/' + p_message.code;

                v_img.addEventListener(
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
                        v_imgShowImage.src = this.src;

                        v_divContainerImg.appendChild(v_imgShowImage);
                        v_divShowImage.appendChild(v_divContainerImg);
                        document.body.appendChild(v_divShowImage);
                    }
                );

                v_messageContent.appendChild(v_img);

                break;
            }
            case 3: { //Snippet
                v_messageContent.classList.add('div_chat_message_snippet');

                var v_div = document.createElement('div');
                v_div.innerHTML = 'Snippet Upload';
                v_messageContent.appendChild(v_div);

                var v_container = document.createElement('div');
                v_container.classList.add('div_chat_message_snippet_container');

                var v_img = document.createElement('img');
                v_img.src = '/static/OmniDB_app/images/icons/extension_chat_code.png';
                v_img.title = 'Click to open the Snippet';
                v_container.appendChild(v_img);

                var v_divName = document.createElement('div');
                v_divName.innerHTML = p_message.title;
                v_container.appendChild(v_divName);

                v_messageContent.appendChild(v_container);

                break;
            }
            case 4: { //Attachment
                v_messageContent.classList.add('div_chat_message_attachment');

                var v_extension = p_message.attachmentName.split('.').pop().toLowerCase();

                switch(v_extension) {
                    case 'jpeg':
                    case 'png':
                    case 'jpg': {
                        v_messageContent.innerHTML = p_message.title;

                        var v_img = document.createElement('img');
                        v_img.src = gv_chatAttachmentPath + '/' + p_message.code;

                        v_img.addEventListener(
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
                                v_imgShowImage.src = this.src;

                                v_divContainerImg.appendChild(v_imgShowImage);
                                v_divShowImage.appendChild(v_divContainerImg);
                                document.body.appendChild(v_divShowImage);
                            }
                        );

                        v_messageContent.appendChild(v_img);

                        break;
                    }
                    default: {
                        var v_div = document.createElement('div');
                        v_div.innerHTML = 'File Upload';
                        v_messageContent.appendChild(v_div);

                        var v_container = document.createElement('div');
                        v_container.classList.add('div_chat_message_attachment_container');

                        var v_img = document.createElement('img');
                        v_img.title = 'Click to download file.';

                        switch(v_extension) {
                            case '3gp':
                            case 'aac':
                            case 'aiff':
                            case 'asp':
                            case 'aspx':
                            case 'avi':
                            case 'bin':
                            case 'bmp':
                            case 'c':
                            case 'cpp':
                            case 'css':
                            case 'csv':
                            case 'dat':
                            case 'db':
                            case 'dll':
                            case 'dmg':
                            case 'doc':
                            case 'docx':
                            case 'exe':
                            case 'flv':
                            case 'h':
                            case 'html':
                            case 'ico':
                            case 'ics':
                            case 'iso':
                            case 'java':
                            case 'js':
                            case 'key':
                            case 'log':
                            case 'mdb':
                            case 'mid':
                            case 'mp3':
                            case 'mp4':
                            case 'odp':
                            case 'odt':
                            case 'ots':
                            case 'ott':
                            case 'pdf':
                            case 'php':
                            case 'pps':
                            case 'ppt':
                            case 'pptx':
                            case 'psd':
                            case 'py':
                            case 'rar':
                            case 'rb':
                            case 'rtf':
                            case 'sql':
                            case 'svg':
                            case 'sys':
                            case 'tex':
                            case 'tga':
                            case 'tgz':
                            case 'txt':
                            case 'wav':
                            case 'xls':
                            case 'xlsx':
                            case 'xml':
                            case 'zip': {
                                v_img.src = '/static/OmniDB_app/images/icons/extension_chat_' + v_extension + '.png';
                                break;
                            }
                            default: {
                                v_img.alt = v_extension;
                            }
                        }

                        v_img.addEventListener(
                            'click',
                            function(p_message, p_event) {
                                var v_link = document.createElement('a');
                                v_link.href = gv_chatAttachmentPath + '/' + p_message.code;
                                v_link.download = p_message.attachmentName;
                                v_link.click();
                                v_link.remove();
                            }.bind(v_img, p_message)
                        );

                        v_container.appendChild(v_img);

                        var v_divName = document.createElement('div');
                        v_divName.innerHTML = p_message.attachmentName;
                        v_container.appendChild(v_divName);

                        if(v_extension == 'mp3' || v_extension == 'ogg' || v_extension == 'wav') {
                            var v_audio = document.createElement('audio');
                            v_audio.controls = true;
                            v_audio.controlsList= 'nodownload';

                            var v_source = document.createElement('source');
                            v_source.src = gv_chatAttachmentPath + '/' + p_message.code;
                            v_source.type = 'audio/' + v_extension;
                            v_audio.appendChild(v_source);

                            v_container.appendChild(v_audio);
                        }

                        if(v_extension == 'mp4') {
                            var v_video = document.createElement('video');
                            v_video.controls = true;
                            v_video.controlsList= 'nodownload';

                            var v_source = document.createElement('source');
                            v_source.src = gv_chatAttachmentPath + '/' + p_message.code;
                            v_source.type = 'video/mp4';
                            v_video.appendChild(v_source);

                            v_container.appendChild(v_video);
                        }

                        v_messageContent.appendChild(v_container);

                        break;
                    }
                }

                break;
            }
            case 5: {//Mention
                v_messageContent.classList.add('div_chat_message_mention');
                v_messageContent.innerHTML = p_message.content;

                break;
            }
        }

        v_messageBody.appendChild(v_messageContent);
        v_item.appendChild(v_messageBody);

        //Context menu shown on message hover
        var v_contextMenu = document.createElement('div');
        v_contextMenu.classList.add('context_menu');
        v_contextMenu.classList.add('context_menu_fit');
        v_contextMenu.classList.add('context_menu_hidden');
        v_contextMenu.style.top = '-15px';
        v_contextMenu.style.right = '3px';
        v_contextMenu.style.left = 'auto';
        v_contextMenu.style.borderRadius = '10px';
        v_contextMenu.tabIndex = '0';

        var v_actionDelete = document.createElement('div');
        v_actionDelete.classList.add('context_menu_item');
        v_actionDelete.classList.add('context_menu_item_inline');
        v_actionDelete.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_delete.png" class="context_menu_item_img" />';
        v_actionDelete.title = 'Delete Message';

        v_actionDelete.addEventListener(
            'click',
            function(p_item, p_message, p_event) {
                var v_innerHTML = '';

                if(p_item.children[0].classList.contains('div_chat_right_left_item_body_padding')) {
                    var v_div = document.createElement('div');
                    v_div.innerHTML = p_item.outerHTML;

                    var v_time = p_message.createdAt.substring(11, 16);

                    //Prepend message header
                    var v_messageHeader = document.createElement('div');
                    v_messageHeader.innerHTML = p_message.user.login + ' <span class="span_chat_right_item_header">' + v_time + '</span>';
                    v_messageHeader.classList.add('div_chat_right_left_item_header');
                    v_div.firstChild.firstChild.insertBefore(v_messageHeader, v_div.firstChild.firstChild.firstChild);

                    //Prepend user icon
                    var v_userImg = document.createElement('img');
                    v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
                    v_userImg.classList.add('img_chat_user');
                    v_div.firstChild.insertBefore(v_userImg, v_div.firstChild.firstChild);

                    v_div.firstChild.childNodes[1].classList.remove('div_chat_right_left_item_body_padding');

                    v_innerHTML = v_div.innerHTML;
                    v_div.remove();
                }
                else {
                    v_innerHTML = p_item.outerHTML;
                }

                var v_html =
                    '<div style="margin-bottom: 20px;">' +
                    '    Do you really want to delete the message below? This operation cannot be undone.' +
                    '</div>' +
                    '<div>' +
                    v_innerHTML +
                    '</div>' +
                    '<div style="margin-top: 10px; text-align: center;">' +
                    '    <button id="button_modal_no">No</button>' +
                    '    <button id="button_modal_yes" style="margin-left: 5px;">Yes</button>' +
                    '</div>';

                var v_modal = openModal(v_html);

                var v_buttonNo = document.getElementById('button_modal_no');

                v_buttonNo.addEventListener(
                    'click',
                    function(p_modal, p_event) {
                        p_modal.remove();
                    }.bind(v_buttonNo, v_modal)
                );

                var v_buttonYes = document.getElementById('button_modal_yes');

                v_buttonYes.addEventListener(
                    'click',
                    function(p_item, p_modal, p_event) {
                        p_modal.remove();

                        var v_data = {
                            channelCode: p_item.channelCode,
                            messageCode: p_item.messageCode
                        };

                        chatRemoveChannelMessage(v_data);
                    }.bind(v_buttonYes, p_item, v_modal)
                );

                v_buttonNo.focus();
            }.bind(v_actionDelete, v_item, p_message)
        );

        v_contextMenu.appendChild(v_actionDelete);

        var v_actionMention = document.createElement('div');
        v_actionMention.classList.add('context_menu_item');
        v_actionMention.classList.add('context_menu_item_inline');
        v_actionMention.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_mention.png" class="context_menu_item_img" />';
        v_actionMention.title = 'Comment Message';

        v_actionMention.addEventListener(
            'click',
            function(p_item, p_message, p_event) {
                var v_dropdownMenu = document.querySelectorAll('.dropdown-menu.textcomplete-dropdown');

                if(v_dropdownMenu != null && v_dropdownMenu.length > 0) {
                    for(var i = 0; i < v_dropdownMenu.length; i++) {
                        v_dropdownMenu[i].remove();
                    }
                }

                var v_innerHTML = '';

                if(p_item.children[0].classList.contains('div_chat_right_left_item_body_padding')) {
                    var v_div = document.createElement('div');
                    v_div.innerHTML = p_item.outerHTML;

                    var v_time = p_message.createdAt.substring(11, 16);

                    //Prepend message header
                    var v_messageHeader = document.createElement('div');
                    v_messageHeader.innerHTML = p_message.user.login + ' <span class="span_chat_right_item_header">' + v_time + '</span>';
                    v_messageHeader.classList.add('div_chat_right_left_item_header');
                    v_div.firstChild.firstChild.insertBefore(v_messageHeader, v_div.firstChild.firstChild.firstChild);

                    //Prepend user icon
                    var v_userImg = document.createElement('img');
                    v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
                    v_userImg.classList.add('img_chat_user');
                    v_div.firstChild.insertBefore(v_userImg, v_div.firstChild.firstChild);

                    v_div.firstChild.childNodes[1].classList.remove('div_chat_right_left_item_body_padding');

                    v_innerHTML = v_div.innerHTML;
                    v_div.remove();
                }
                else {
                    v_innerHTML = p_item.outerHTML;
                }

                var v_html =
                    '<div style="margin-bottom: 20px;">' +
                    '    <div id="div_chat_message_mention_content">' +
                    '    </div>' +
                    '</div>' +
                    '<div>' +
                    v_innerHTML +
                    '</div>' +
                    '<div style="margin-top: 10px; text-align: center;">' +
                    '    <button id="button_modal_cancel">Cancel</button>' +
                    '    <button id="button_modal_ok" style="margin-left: 5px;">Ok</button>' +
                    '</div>';

                var v_modal = openModal(v_html);

                document.querySelector('.modal_content').style.width = '70vw';

                var v_editor = $('#div_chat_message_mention_content').emojioneArea({
                    pickerPosition: 'top',
                    filtersPosition: 'top',
                    tonesStyle: 'bullet',
                    placeholder: 'Type your comment...',
                    saveEmojisAs: 'shortname',
                    useInternalCDN: false
                });

                window.addEventListener(
                    'blur',
                    function(p_editor, p_event) {
                        if(p_editor != null) {
                            p_editor.altPressed = false;
                            p_editor.shiftPressed = false;
                        }
                    }.bind(window, v_editor[0].emojioneArea)
                );

                var v_buttonCancel = document.getElementById('button_modal_cancel');

                v_buttonCancel.addEventListener(
                    'click',
                    function(p_modal, p_event) {
                        p_modal.remove();

                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            v_dropdownMenu.remove();
                        }
                    }.bind(v_buttonCancel, v_modal)
                );

                var v_buttonOk = document.getElementById('button_modal_ok');

                v_buttonOk.addEventListener(
                    'click',
                    function(p_item, p_modal, p_messageContent, p_editor, p_event) {
                        var v_data = {
                            messageType: 5, //Mentioned message
                            channelCode: p_item.channelCode,
                            mentionedMessageContent: p_messageContent,
                            commentMessageRawContent: p_editor[0].emojioneArea.getText(),
                            commentMessageContent: p_editor[0].emojioneArea.editor[0].innerHTML
                        };

                        chatSendChannelMessage(v_data);

                        p_modal.remove();

                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            v_dropdownMenu.remove();
                        }
                    }.bind(v_buttonOk, p_item, v_modal, v_innerHTML, v_editor)
                );

                v_editor[0].emojioneArea.altPressed = false;
                v_editor[0].emojioneArea.shiftPressed = false;
                v_editor[0].selectingEmoji = false;

                v_editor[0].emojioneArea.on(
                    'keydown',
                    function(p_editor, p_event) {
                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            this.selectingEmoji = v_dropdownMenu.style.display == 'block';
                        }
                        else {
                            this.selectingEmoji = false;
                        }

                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = true;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = true;
                        }

                        if(p_event.keyCode == 13) { //Enter
                            p_event.preventDefault();

                            if(this.altPressed || this.shiftPressed) {
                                var v_selection = window.getSelection();
                                var v_range = v_selection.getRangeAt(0);
                                var v_div = document.createElement('div');
                                var v_br = document.createElement('br');
                                v_div.appendChild(v_br);
                                v_range.deleteContents();
                                v_range.insertNode(v_div);
                                v_range.setStartAfter(v_div);
                                v_range.setEndAfter(v_div);
                                v_range.collapse(false);
                                v_selection.removeAllRanges();
                                v_selection.addRange(v_range);
                            }
                        }
                    }.bind(v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.on(
                    'keyup',
                    function(p_buttonOk, p_editor, p_event) {
                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = false;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = false;
                        }

                        if(p_event.keyCode == 13 && !this.selectingEmoji && !this.altPressed && !this.shiftPressed) { //Enter and not selecting emoticons or inserting new lines
                            p_event.preventDefault();

                            if(p_editor[0].innerHTML.length > 0) {
                                p_buttonOk.click();
                            }
                        }
                    }.bind(v_editor[0].emojioneArea, v_buttonOk)
                );

                v_editor[0].emojioneArea.setText('');
                v_editor[0].nextSibling.childNodes[0].focus();
            }.bind(v_actionMention, v_item, p_message)
        );

        v_contextMenu.appendChild(v_actionMention);

        var v_actionShare = document.createElement('div');
        v_actionShare.classList.add('context_menu_item');
        v_actionShare.classList.add('context_menu_item_inline');
        v_actionShare.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_share.png" class="context_menu_item_img" />';
        v_actionShare.title = 'Forward Message';

        v_actionShare.addEventListener(
            'click',
            function(p_item, p_event) {
                var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

                if(v_chatPopUp != null) {
                    var v_html =
                        '<div class="div_chat_right_left_item">' +
                        p_item.querySelector('.div_chat_right_left_item_content').outerHTML +
                        '</div>' +
                        '<div id="div_share_with">' +
                        '    <span id="span_share_with">Forward to: </span>' +
                        '    <select id="select_share_message_with" class="form-control">';

                    var v_channelItems = document.querySelectorAll('#div_chat_channels .div_chat_left_content_item');

                    for(var i = 0; i < v_channelItems.length; i++) {
                        v_html += '        <option value="channel_' + v_channelItems[i].channelCode + '">' + v_channelItems[i].childNodes[1].textContent + '</option>';
                    }

                    var v_groupItems = document.querySelectorAll('#div_chat_groups .div_chat_left_content_item');

                    for(var i = 0; i < v_groupItems.length; i++) {
                        v_html += '        <option value="group_' + v_groupItems[i].groupCode + '">' + v_groupItems[i].childNodes[1].textContent + '</option>';
                    }

                    v_html +=
                        '    </select>' +
                        '</div>' +
                        '<div id="div_share_with_footer">' +
                        '    <button id="button_modal_cancel">Cancel</button>' +
                        '    <button id="button_modal_ok">Ok</button>' +
                        '</div>';

                    var v_modal = openModal(v_html);

                    document.querySelector('.modal_content').style.maxWidth = '60vw';

                    var v_buttonCancel = document.getElementById('button_modal_cancel');

                    v_buttonCancel.addEventListener(
                        'click',
                        function(p_modal, p_event) {
                            p_modal.remove();
                        }.bind(v_buttonCancel, v_modal)
                    );

                    var v_buttonOk = document.getElementById('button_modal_ok');

                    v_buttonOk.addEventListener(
                        'click',
                        function(p_modal, p_item, p_event) {
                            var v_selectedValue = document.getElementById('select_share_message_with').value;
                            var v_type = v_selectedValue.split('_')[0];
                            var v_code = parseInt(v_selectedValue.split('_').pop());

                            switch(v_type) {
                                case 'channel': {
                                    var v_data = {
                                        forwardMessageCode: p_item.messageCode,
                                        channelCode: v_code,
                                        messageType: 0
                                    };

                                    chatSendChannelMessage(v_data);

                                    break;
                                }
                                case 'group': {
                                    var v_data = {
                                        forwardMessageCode: p_item.messageCode,
                                        groupCode: v_code,
                                        messageType: 0
                                    };

                                    chatSendGroupMessage(v_data);

                                    break;
                                }
                            }

                            p_modal.remove();
                        }.bind(v_buttonOk, v_modal, p_item)
                    );
                }
            }.bind(v_actionShare, v_item)
        );

        v_contextMenu.appendChild(v_actionShare);

        if(p_message.type == 1 || p_message.type == 5) {//Plain text or Mention
            if(p_message.user.code == v_user_id) {//Same user
                var v_actionEdit = document.createElement('div');
                v_actionEdit.classList.add('context_menu_item');
                v_actionEdit.classList.add('context_menu_item_inline');
                v_actionEdit.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_edit.png" class="context_menu_item_img" />';
                v_actionEdit.title = 'Edit Message';
                v_actionEdit.channelCode = p_channelCode;

                v_actionEdit.addEventListener(
                    'click',
                    function(p_message, p_event) {
                        var v_dropdownMenu = document.querySelectorAll('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null && v_dropdownMenu.length > 0) {
                            for(var i = 0; i < v_dropdownMenu.length; i++) {
                                v_dropdownMenu[i].remove();
                            }
                        }

                        var v_html =
                            '<div style="margin-bottom: 20px;">' +
                            '    <div id="div_chat_message_edit_message">' +
                            '    </div>' +
                            '</div>' +
                            '<div style="margin-top: 10px; text-align: center;">' +
                            '    <button id="button_modal_cancel">Cancel</button>' +
                            '    <button id="button_modal_ok" style="margin-left: 5px;">Ok</button>' +
                            '</div>';

                        var v_modal = openModal(v_html);

                        document.querySelector('.modal_content').style.width = '70vw';

                        var v_editor = $('#div_chat_message_edit_message').emojioneArea({
                            pickerPosition: 'top',
                            filtersPosition: 'top',
                            tonesStyle: 'bullet',
                            saveEmojisAs: 'shortname',
                            useInternalCDN: false
                        });

                        window.addEventListener(
                            'blur',
                            function(p_editor, p_event) {
                                if(p_editor != null) {
                                    p_editor.altPressed = false;
                                    p_editor.shiftPressed = false;
                                }
                            }.bind(window, v_editor[0].emojioneArea)
                        );

                        if(p_message.type == 1) { //Plain text
                            v_editor[0].emojioneArea.setText(p_message.rawContent);
                        }
                        else if(p_message.type == 5) { //Mention
                            var v_content = p_message.rawContent.substring(0, p_message.rawContent.indexOf('#start_mentioned_message#'));
                            v_editor[0].emojioneArea.setText(v_content);
                        }

                        v_editor[0].nextSibling.childNodes[0].focus();

                        var v_buttonCancel = document.getElementById('button_modal_cancel');

                        v_buttonCancel.addEventListener(
                            'click',
                            function(p_modal, p_event) {
                                p_modal.remove();

                                var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                                if(v_dropdownMenu != null) {
                                    v_dropdownMenu.remove();
                                }
                            }.bind(v_buttonCancel, v_modal)
                        );

                        var v_buttonOk = document.getElementById('button_modal_ok');
                        v_buttonOk.messageCode = p_message.code;
                        v_buttonOk.channelCode = this.channelCode;

                        v_buttonOk.addEventListener(
                            'click',
                            function(p_editor, p_modal, p_message, p_event) {
                                var v_rawContent = p_editor[0].emojioneArea.getText();
                                var v_content = p_editor[0].emojioneArea.editor[0].innerHTML;

                                if(p_message.type == 5) { //Mention
                                    v_rawContent += p_message.rawContent.substring(p_message.rawContent.indexOf('#start_mentioned_message#'), p_message.rawContent.length);
                                    v_content += p_message.rawContent.substring(p_message.rawContent.indexOf('#start_mentioned_message#'), p_message.rawContent.length);
                                }

                                var v_data = {
                                    messageCode: this.messageCode,
                                    channelCode: this.channelCode,
                                    messageContent: v_content,
                                    messageRawContent: v_rawContent
                                };

                                chatUpdateChannelMessage(v_data);

                                p_modal.remove();

                                var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                                if(v_dropdownMenu != null) {
                                    v_dropdownMenu.remove();
                                }
                            }.bind(v_buttonOk, v_editor, v_modal, p_message)
                        );

                        v_editor[0].emojioneArea.altPressed = false;
                        v_editor[0].emojioneArea.shiftPressed = false;
                        v_editor[0].selectingEmoji = false;

                        v_editor[0].emojioneArea.on(
                            'keydown',
                            function(p_editor, p_event) {
                                var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                                if(v_dropdownMenu != null) {
                                    this.selectingEmoji = v_dropdownMenu.style.display == 'block';
                                }
                                else {
                                    this.selectingEmoji = false;
                                }

                                if(p_event.keyCode == 18) { //Alt
                                    this.altPressed = true;
                                }
                                else if(p_event.keyCode == 16) { //Shift
                                    this.shiftPressed = true;
                                }

                                if(p_event.keyCode == 13) { //Enter
                                    p_event.preventDefault();

                                    if(this.altPressed || this.shiftPressed) {
                                        var v_selection = window.getSelection();
                                        var v_range = v_selection.getRangeAt(0);
                                        var v_div = document.createElement('div');
                                        var v_br = document.createElement('br');
                                        v_div.appendChild(v_br);
                                        v_range.deleteContents();
                                        v_range.insertNode(v_div);
                                        v_range.setStartAfter(v_div);
                                        v_range.setEndAfter(v_div);
                                        v_range.collapse(false);
                                        v_selection.removeAllRanges();
                                        v_selection.addRange(v_range);
                                    }
                                }
                            }.bind(v_editor[0].emojioneArea)
                        );

                        v_editor[0].emojioneArea.on(
                            'keyup',
                            function(p_buttonOk, p_editor, p_event) {
                                if(p_event.keyCode == 18) { //Alt
                                    this.altPressed = false;
                                }
                                else if(p_event.keyCode == 16) { //Shift
                                    this.shiftPressed = false;
                                }

                                if(p_event.keyCode == 13 && !this.selectingEmoji && !this.altPressed && !this.shiftPressed) { //Enter and not selecting emoticons or inserting new lines
                                    p_event.preventDefault();

                                    if(p_editor[0].innerHTML.length > 0) {
                                        p_buttonOk.click();
                                    }
                                }
                            }.bind(v_editor[0].emojioneArea, v_buttonOk)
                        );
                    }.bind(v_actionEdit, p_message)
                );

                v_contextMenu.appendChild(v_actionEdit);
            }
        }

        if(p_message.type == 2 || p_message.type == 4) {//Pasted image or Attachment
            var v_actionDownload = document.createElement('div');
            v_actionDownload.classList.add('context_menu_item');
            v_actionDownload.classList.add('context_menu_item_inline');
            v_actionDownload.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_download.png" class="context_menu_item_img" />';
            v_actionDownload.title = 'Download File';

            v_actionDownload.addEventListener(
                'click',
                function(p_message, p_event) {
                    var v_link = document.createElement('a');
                    v_link.href = gv_chatAttachmentPath + '/' + p_message.code;
                    v_link.download = p_message.attachmentName;
                    v_link.click();
                    v_link.remove();
                }.bind(v_actionDownload, p_message)
            );

            v_contextMenu.appendChild(v_actionDownload);
        }

        if(p_message.type == 3) {//Snippet
            var v_html =
                '<div style="text-align: center; font-family: lato-bold;">' +
                '    <input id="input_snippet_title" type="text" style="display: inline-block !important; width: 40%;" placeholder="Snippet Title" class="form-control" />' +
                '    <select id="select_snippet_mode" style="display: inline-block !important; width: 40%; margin-left: 5%;" class="form-control">' +
                '        <option value="plain_text" selected="selected">Plain Text</option>' +
                '        <option value="abap">ABAP</option>' +
                '        <option value="abc">ABC</option>' +
                '        <option value="actionscript">ActionScript</option>' +
                '        <option value="ada">Ada</option>' +
                '        <option value="apache_conf">ApachConf</option>' +
                '        <option value="applescript">AppleScript</option>' +
                '        <option value="asciidoc">AsciiDoc</option>' +
                '        <option value="assembly_x86">Assembly x86</option>' +
                '        <option value="autohotkey">AutoHotkey</option>' +
                '        <option value="batchfile">Batch file</option>' +
                '        <option value="behaviour">Behaviour</option>' +
                '        <option value="bro">Bro</option>' +
                '        <option value="c_cpp">C</option>' +
                '        <option value="c_cpp">C++</option>' +
                '        <option value="cirru">Cirru</option>' +
                '        <option value="clojure">Clojure</option>' +
                '        <option value="cobol">COBOL</option>' +
                '        <option value="coffee">CoffeeScript</option>' +
                '        <option value="coldfusion">ColdFusion</option>' +
                '        <option value="csharp">C#</option>' +
                '        <option value="csound">CSound</option>' +
                '        <option value="css">CSS</option>' +
                '        <option value="curly">curly</option>' +
                '        <option value="d">D</option>' +
                '        <option value="dart">Dart</option>' +
                '        <option value="diff">Diff</option>' +
                '        <option value="django">Django</option>' +
                '        <option value="dockerfile">Dockerfile</option>' +
                '        <option value="dot">DOT</option>' +
                '        <option value="drools">Drools</option>' +
                '        <option value="eiffel">Eiffel</option>' +
                '        <option value="ejs">EJS</option>' +
                '        <option value="elixir">Elixir</option>' +
                '        <option value="elm">Elm</option>' +
                '        <option value="erlang">Erlang</option>' +
                '        <option value="forth">Forth</option>' +
                '        <option value="fortran">Fortran</option>' +
                '        <option value="ftl">FTL</option>' +
                '        <option value="gcode">G-code</option>' +
                '        <option value="gherkin">Gherkin</option>' +
                '        <option value="gitignore">GitIgnore</option>' +
                '        <option value="glsl">GLSL</option>' +
                '        <option value="gobstones">Gobstones</option>' +
                '        <option value="golang">GoLang</option>' +
                '        <option value="graphqlschema">GraphQLSchema</option>' +
                '        <option value="groovy">Groovy</option>' +
                '        <option value="haml">Haml</option>' +
                '        <option value="handlebars">Handlebars</option>' +
                '        <option value="haskell">Haskell</option>' +
                '        <option value="haxe">Haxe</option>' +
                '        <option value="hjson">Hjson</option>' +
                '        <option value="html">HTML</option>' +
                '        <option value="ini">INI</option>' +
                '        <option value="io">Io</option>' +
                '        <option value="jack">Jack</option>' +
                '        <option value="jade">Jade</option>' +
                '        <option value="java">Java</option>' +
                '        <option value="javascript">JavaScript</option>' +
                '        <option value="json">JSON</option>' +
                '        <option value="jsoniq">JSONiq</option>' +
                '        <option value="jsp">JSP</option>' +
                '        <option value="jssm">JSSM</option>' +
                '        <option value="jsx">JSX</option>' +
                '        <option value="julia">Julia</option>' +
                '        <option value="kotlin">Kotlin</option>' +
                '        <option value="latex">LaTeX</option>' +
                '        <option value="less">Less</option>' +
                '        <option value="liquid">Liquid</option>' +
                '        <option value="lisp">Lisp</option>' +
                '        <option value="livescript">LiveScript</option>' +
                '        <option value="logiql">LogiQL</option>' +
                '        <option value="lsl">LSL</option>' +
                '        <option value="lua">Lua</option>' +
                '        <option value="luapage">Lua Page</option>' +
                '        <option value="lucene">Lucene</option>' +
                '        <option value="makefile">Makefile</option>' +
                '        <option value="markdown">Markdown</option>' +
                '        <option value="mask">MASK</option>' +
                '        <option value="matlab">MATLAB</option>' +
                '        <option value="maze">Maze</option>' +
                '        <option value="mel">MEL</option>' +
                '        <option value="mushcode">MUSHCode</option>' +
                '        <option value="mysql">MySQL</option>' +
                '        <option value="nix">Nix</option>' +
                '        <option value="nsis">NSIS</option>' +
                '        <option value="objectivec">Objective-C</option>' +
                '        <option value="ocaml">OCaml</option>' +
                '        <option value="pascal">Pascal</option>' +
                '        <option value="nsis">NSIS</option>' +
                '        <option value="perl">Perl</option>' +
                '        <option value="pgsql">pgSQL</option>' +
                '        <option value="php">PHP</option>' +
                '        <option value="pig">Pig</option>' +
                '        <option value="powershell">PowerShell</option>' +
                '        <option value="praat">Praat</option>' +
                '        <option value="prolog">Prolog</option>' +
                '        <option value="protobuf">protobuf</option>' +
                '        <option value="python">Python</option>' +
                '        <option value="r">R</option>' +
                '        <option value="razor">Razor</option>' +
                '        <option value="rdoc">RDoC</option>' +
                '        <option value="red">Red</option>' +
                '        <option value="rhtml">RHTML</option>' +
                '        <option value="rst">reStructuredText</option>' +
                '        <option value="ruby">Ruby</option>' +
                '        <option value="rust">Rust</option>' +
                '        <option value="sass">Sass</option>' +
                '        <option value="scad">SCAD</option>' +
                '        <option value="scala">Scala</option>' +
                '        <option value="scheme">Scheme</option>' +
                '        <option value="scss">Scss</option>' +
                '        <option value="sh">Shell script</option>' +
                '        <option value="sjs">SJS</option>' +
                '        <option value="smarty">Smarty</option>' +
                '        <option value="snippet">Snippet</option>' +
                '        <option value="soy_template">Soy Template</option>' +
                '        <option value="sparql">SPARQL</option>' +
                '        <option value="sql">SQL</option>' +
                '        <option value="sqlserver">SQL Server</option>' +
                '        <option value="stylus">Stylus</option>' +
                '        <option value="svg">SVG</option>' +
                '        <option value="swift">Swift</option>' +
                '        <option value="tcl">Tcl</option>' +
                '        <option value="tex">TeX</option>' +
                '        <option value="toml">TOML</option>' +
                '        <option value="tsx">TSX</option>' +
                '        <option value="turtle">Turtle</option>' +
                '        <option value="twig">Twig</option>' +
                '        <option value="typescript">TypeScript</option>' +
                '        <option value="vala">Vala</option>' +
                '        <option value="vbscript">VBScript</option>' +
                '        <option value="velocity">Velocity</option>' +
                '        <option value="verilog">Verilog</option>' +
                '        <option value="vhdl">VHDL</option>' +
                '        <option value="wollok">Wollok</option>' +
                '        <option value="xml">XML</option>' +
                '        <option value="xquery">XQuery</option>' +
                '        <option value="yaml">YAML</option>' +
                '    </select>' +
                '</div>' +
                '<div id="div_snippet_editor" style="margin-top: 20px; margin-bottom: 20px; height: calc(70vh - 100px); width: 70vw; border: 2px solid rgba(0, 0, 0, 0.5); border-radius: 8px;">' +
                '</div>' +
                '<div style="margin-top: 10px; text-align: center;">' +
                '    <button id="button_modal_cancel">Cancel</button>' +
                '    <button id="button_modal_ok" style="margin-left: 5px;">Ok</button>' +
                '</div>';

            if(p_message.user.code == v_user_id) {//Same user
                var v_actionEdit = document.createElement('div');
                v_actionEdit.classList.add('context_menu_item');
                v_actionEdit.classList.add('context_menu_item_inline');
                v_actionEdit.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_edit.png" class="context_menu_item_img" />';
                v_actionEdit.title = 'Edit Snippet';
                v_actionEdit.channelCode = p_channelCode;

                v_actionEdit.addEventListener(
                    'click',
                    function(p_message, p_html, p_event) {
                        var v_modal = openModal(p_html);

                        document.getElementById('input_snippet_title').value = p_message.title;

                        var v_editor = ace.edit('div_snippet_editor');
                        v_editor.getSession().setMode('ace/mode/' + p_message.snippetMode);
                        v_editor.setTheme("ace/theme/" + v_editor_theme);
                        v_editor.getSession().setUseSoftTabs(true);
                        v_editor.setValue(p_message.content);
                        v_editor.clearSelection();
                        v_editor.focus();

                        var v_selectSnippetMode = document.getElementById('select_snippet_mode');
                        v_selectSnippetMode.value = p_message.snippetMode;

                        v_selectSnippetMode.addEventListener(
                            'change',
                            function(p_editor, p_event) {
                                p_editor.getSession().setMode('ace/mode/' + this.value);
                            }.bind(v_selectSnippetMode, v_editor)
                        );

                        var v_buttonCancel = document.getElementById('button_modal_cancel');

                        v_buttonCancel.addEventListener(
                            'click',
                            function(p_modal, p_event) {
                                p_modal.remove();
                            }.bind(v_buttonCancel, v_modal)
                        );

                        var v_buttonOk = document.getElementById('button_modal_ok');
                        v_buttonOk.messageCode = p_message.code;
                        v_buttonOk.channelCode = this.channelCode;

                        v_buttonOk.addEventListener(
                            'click',
                            function(p_editor, p_modal, p_event) {
                                var v_data = {
                                    snippetTitle: document.getElementById('input_snippet_title').value,
                                    snippetContent: p_editor.getValue(),
                                    snippetMode: document.getElementById('select_snippet_mode').value,
                                    messageCode: this.messageCode,
                                    channelCode: this.channelCode
                                };

                                chatUpdateChannelSnippetMessage(v_data);

                                p_modal.remove();
                            }.bind(v_buttonOk, v_editor, v_modal)
                        );
                    }.bind(v_actionEdit, p_message, v_html)
                );

                v_contextMenu.appendChild(v_actionEdit);

                var v_snippetContainerImg = v_messageContent.querySelector('.div_chat_message_snippet_container > img')

                if(v_snippetContainerImg != null) {
                    v_snippetContainerImg.addEventListener(
                        'click',
                        function(p_actionEdit, p_event) {
                            p_actionEdit.click();
                        }.bind(v_snippetContainerImg, v_actionEdit)
                    );
                }
            }
            else {
                var v_actionView = document.createElement('div');
                v_actionView.classList.add('context_menu_item');
                v_actionView.classList.add('context_menu_item_inline');
                v_actionView.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_view.png" class="context_menu_item_img" />';
                v_actionView.title = 'View Snippet';

                v_actionView.addEventListener(
                    'click',
                    function(p_message, p_html, p_event) {
                        var v_modal = openModal(p_html);

                        document.getElementById('input_snippet_title').value = p_message.title;
                        document.getElementById('input_snippet_title').disabled = true;

                        var v_editor = ace.edit('div_snippet_editor');
                        v_editor.getSession().setMode('ace/mode/' + p_message.snippetMode);
                        v_editor.setTheme("ace/theme/" + v_editor_theme);
                        v_editor.getSession().setUseSoftTabs(true);
                        v_editor.setValue(p_message.content);
                        v_editor.clearSelection();
                        v_editor.focus();
                        v_editor.setReadOnly(true);

                        var v_selectSnippetMode = document.getElementById('select_snippet_mode');
                        v_selectSnippetMode.value = p_message.snippetMode;
                        v_selectSnippetMode.disabled = true;

                        var v_buttonCancel = document.getElementById('button_modal_cancel');
                        v_buttonCancel.style.display = 'none';

                        var v_buttonOk = document.getElementById('button_modal_ok');
                        v_buttonOk.messageCode = p_message.code;

                        v_buttonOk.addEventListener(
                            'click',
                            function(p_modal, p_event) {
                                p_modal.remove();
                            }.bind(v_buttonOk, v_modal)
                        );
                    }.bind(v_actionView, p_message, v_html)
                );

                v_contextMenu.appendChild(v_actionView);

                var v_snippetContainerImg = v_messageContent.querySelector('.div_chat_message_snippet_container > img')

                if(v_snippetContainerImg != null) {
                    v_snippetContainerImg.addEventListener(
                        'click',
                        function(p_actionView, p_event) {
                            p_actionView.click();
                        }.bind(v_snippetContainerImg, v_actionView)
                    );
                }
            }
        }

        v_item.appendChild(v_contextMenu);

        if(p_withHeader) {
            var v_time = p_message.createdAt.substring(11, 16);

            //Prepend message header
            var v_messageHeader = document.createElement('div');
            v_messageHeader.innerHTML = p_message.user.login + ' <span class="span_chat_right_item_header">' + v_time + '</span>';
            v_messageHeader.classList.add('div_chat_right_left_item_header');
            v_item.firstChild.insertBefore(v_messageHeader, v_item.firstChild.firstChild);

            //Prepend user icon
            var v_userImg = document.createElement('img');
            v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
            v_userImg.classList.add('img_chat_user');
            v_item.insertBefore(v_userImg, v_item.firstChild);

            v_item.childNodes[1].classList.remove('div_chat_right_left_item_body_padding');
        }

        return v_item;
    }.bind(v_chatPopUp.tag.getRenderedChannelMessage, v_chatPopUp);

    v_chatPopUp.tag.renderChannel = function(p_chatPopUp, p_channelCode, p_renderAtMessage, p_preventContextScroll) {
        if(p_chatPopUp.tag.renderedType == 1) { //Channel
            /*var v_data = {
                channelCode: p_chatPopUp.tag.renderedChannel,
                userCode: parseInt(v_user_id),
                userWriting: false
            };

            chatSetChannelUserWriting(v_data);*/

            var v_channelContext = p_chatPopUp.tag.contextList.getContextByChannelCode(p_chatPopUp.tag.renderedChannel);

            if(v_channelContext != null) {
                v_channelContext.text = p_chatPopUp.tag.renderedEditor.getText();
            }
        }
        else if(p_chatPopUp.tag.renderedType == 2) { //Group
            /*var v_data = {
                groupCode: p_chatPopUp.tag.renderedGroup,
                userCode: parseInt(v_user_id),
                userWriting: false
            };

            chatSetGroupUserWriting(v_data);*/

            var v_groupContext = p_chatPopUp.tag.contextList.getContextByGroupCode(p_chatPopUp.tag.renderedGroup);

            if(v_groupContext != null) {
                v_groupContext.text = p_chatPopUp.tag.renderedEditor.getText();
            }
        }

        //Change active element
        var v_activeChannelElement = document.querySelector('.div_chat_left_content > .div_chat_left_content_item_active');

        if(v_activeChannelElement != null) {
            v_activeChannelElement.classList.remove('div_chat_left_content_item_active');
        }

        var v_channel = p_chatPopUp.tag.channelList.getChannelByCode(p_channelCode);

        if(v_channel != null) {
            var v_sameChannel = false;
            var v_onLastMessage = false;
            var v_firstVisibleMessageCode = null;
            var v_firstUnreadMessageCode = null;

            if(p_chatPopUp.tag.renderedType == 1 && v_chatPopUp.tag.renderedChannel == v_channel.code) {//If the rendered type is channel and this channel are the rendered one.
                v_sameChannel = true;
                var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

                if((v_divChatRightContent.offsetHeight + v_divChatRightContent.scrollTop + 1) >= v_divChatRightContent.scrollHeight) {//If scroll was at max allowed
                    v_onLastMessage = true;
                }
                else {
                    for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                        if(v_divChatRightContent.childNodes[i].offsetTop >= v_divChatRightContent.scrollTop) {
                            v_firstVisibleMessageCode = v_divChatRightContent.childNodes[i].messageCode;
                            break;
                        }
                    }
                }
            }

            var v_divChatRight = document.getElementById('div_chat_right_left');
            var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

            if(!v_sameChannel) {
                //Remove drop down from last render, if any
		        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

		        if(v_dropdownMenu != null) {
		            v_dropdownMenu.remove();
		        }

	            p_chatPopUp.tag.renderedType = 1; //Channel popup
	            p_chatPopUp.tag.renderedChannel = v_channel.code;

	            v_divChatRight.type = 1; //Channel container
	            v_divChatRight.channelCode = v_channel.code;

                //Recover last header items, if any
                var v_oldRightHeader = document.getElementById('div_chat_right_left_header');
                var v_oldRightHeaderChildren = [];

                if(v_oldRightHeader != null) {
                    for(var i = 0; i < v_oldRightHeader.childNodes.length; i++) {
                        v_oldRightHeaderChildren.push(v_oldRightHeader.childNodes[i]);
                    }
                }

	            v_divChatRight.innerHTML = '';

                var v_rightPreHeader = document.createElement('div');
                v_rightPreHeader.id = 'div_chat_right_left_pre_header';

                var v_divContainer = document.createElement('div');
                v_divContainer.id = 'div_chat_right_left_pre_header_name_container';
                v_rightPreHeader.appendChild(v_divContainer);

                var v_imgRightPreHeader = document.createElement('img');
                v_imgRightPreHeader.id = 'img_chat_right_pre_header_icon';

                if(v_channel.private) {
                    v_imgRightPreHeader.src = '/static/OmniDB_app/images/icons/status_chat_privatechannel.png';
                }
                else {
                    v_imgRightPreHeader.src = '/static/OmniDB_app/images/icons/status_chat_channel.png';
                }

                v_divContainer.appendChild(v_imgRightPreHeader);

                var v_spanRightPreHeader = document.createElement('span');
                v_spanRightPreHeader.id = 'span_chat_right_pre_header_name';
                v_spanRightPreHeader.innerHTML = v_channel.name;
                v_divContainer.appendChild(v_spanRightPreHeader);

                var v_inputRightPreHeader = document.createElement('input');
                v_inputRightPreHeader.type = 'text';
                v_inputRightPreHeader.id = 'input_chat_right_pre_header_search';
                v_inputRightPreHeader.classList.add('form-control');
                v_inputRightPreHeader.placeholder = 'Search...';
                v_inputRightPreHeader.title = 'Type and, at end, press enter to start searching.'

                v_inputRightPreHeader.addEventListener(
                    'keydown',
                    function(p_event) {
                        if(p_event.keyCode == 13) { //Enter
                            var v_value = this.value.toLowerCase();

                            if(v_value != '') {
                                this.value = '';

                                var v_divChatRightRight = document.getElementById('div_chat_right_right');
                                v_divChatRightRight.classList.remove('display_hidden');

                                var v_divChatRightRightContent = document.getElementById('div_chat_right_right_content');
                                v_divChatRightRightContent.removeAttribute('style');
                                v_divChatRightRightContent.innerHTML = '<div class="gif_loading"></div>';
                                v_divChatRightRightContent.style.justifyContent = 'center';
                                v_divChatRightRightContent.style.alignItems = 'center';

                                var v_data = {
                                    textPattern: v_value
                                };

                                chatSearchOldMessages(v_data);
                            }
                        }
                    }
                );

                v_rightPreHeader.appendChild(v_inputRightPreHeader);

                v_divChatRight.appendChild(v_rightPreHeader);

                var v_rightHeader = document.createElement('div');
                v_rightHeader.id = 'div_chat_right_left_header';
                v_divChatRight.appendChild(v_rightHeader);

                //Observer used to rightly format header
                var v_rightHeaderObserver = new MutationObserver(
                    function(p_rightHeader, p_mutationList, p_this) {
                        if(p_rightHeader.childNodes.length == 0) {
                            p_rightHeader.style.padding = '';
                            p_rightHeader.style.borderBottom = '';
                        }
                        else {
                            p_rightHeader.style.padding = '10px';
                            p_rightHeader.style.borderBottom = '1px solid rgba(0, 0, 0, 0.5)';
                        }
                    }.bind(v_rightHeaderObserver, v_rightHeader)
                );

                v_rightHeaderObserver.observe(
                    v_rightHeader,
                    {
                        childList: true
                    }
                );

                //Restore last header items, if any
                if(v_oldRightHeaderChildren.length > 0) {
                    for(var i = 0; i < v_oldRightHeaderChildren.length; i++) {
                        v_rightHeader.appendChild(v_oldRightHeaderChildren[i]);
                    }
                }

	            var v_rightContent = document.createElement('div');
                v_divChatRightContent = v_rightContent;
	            v_rightContent.id = 'div_chat_right_left_content';

                //Controls when to recover older messages from server
                v_rightContent.addEventListener(
                    'scroll',
                    function(p_chatPopUp, p_event) {
                        var v_channelContext = p_chatPopUp.tag.contextList.getContextByChannelCode(this.parentElement.channelCode);

                        if(v_channelContext != null) {
                            v_channelContext.scrollTop = this.scrollTop;
                        }

                        var v_channel = p_chatPopUp.tag.channelList.getChannelByCode(this.parentElement.channelCode);

                        if(v_channel != null) {
	                        if(this.scrollTop == 0) {
	                            var v_data = {
	                                channelCode: v_channel.code,
	                                offset: v_channel.messageList.length,
                                    fromMessageCode: null
	                            };

	                            chatRetrieveChannelHistory(v_data);
	                        }
	                        else {
	                            //Mark messages as read, if it's the case
					            if((this.offsetHeight + this.scrollTop + 1) >= this.scrollHeight) {
                                    var v_messageCodeList = [];

                                    for(var i = 0; i < v_channel.messageList.length; i++) {
                                        if(!v_channel.messageList[i].viewed) {
                                            v_messageCodeList.push(v_channel.messageList[i].code);
                                        }
                                    }

                                    if(v_messageCodeList.length > 0) {
                                        var v_data = {
                                            channelCode: v_channel.code,
                                            messageCodeList: v_messageCodeList
                                        };

                                        chatMarkChannelMessagesAsRead(v_data);
                                    }
                                }
                            }
                        }
                    }.bind(v_rightContent, p_chatPopUp)
                );

	            v_divChatRight.appendChild(v_rightContent);

                p_chatPopUp.tag.renderedContent = v_rightContent;

	            var v_rightFooter = document.createElement('div');
	            v_rightFooter.id = 'div_chat_right_left_footer';
	            v_divChatRight.appendChild(v_rightFooter);

	            var v_rightFooterLeft = document.createElement('div');
	            v_rightFooterLeft.id = 'div_chat_right_left_footer_left';
	            v_rightFooter.appendChild(v_rightFooterLeft);

	            var v_buttonChatRightFooterLeft = document.createElement('button');
	            v_buttonChatRightFooterLeft.classList.add('button_chat_right_footer_left');
	            v_buttonChatRightFooterLeft.innerHTML = '+';
	            v_rightFooterLeft.appendChild(v_buttonChatRightFooterLeft);

                //Used for uploading snippets and files
	            v_buttonChatRightFooterLeft.addEventListener(
	                'click',
	                function(p_chatPopUp, p_event) {
	                    var v_div = document.createElement('div');
                        v_div.classList.add('div_chat_right_left_footer_left_options');
                        v_div.tabIndex = '0';

                        v_div.addEventListener(
                            'blur',
                            function(p_event) {
                                this.remove();
                            }
                        );

                        var v_snippetItem = document.createElement('div');
                        v_snippetItem.classList.add('div_chat_right_left_footer_left_options_item');
                        v_snippetItem.innerHTML = 'Create Snippet';

                        v_snippetItem.addEventListener(
                            'click',
                            function(p_chatPopUp, p_event) {
                                this.parentElement.blur();

                                var v_html =
                                    '<div style="text-align: center; font-family: lato-bold;">' +
                                    '    <input id="input_snippet_title" type="text" style="display: inline-block !important; width: 40%;" placeholder="Snippet Title" class="form-control" />' +
                                    '    <select id="select_snippet_mode" style="display: inline-block !important; width: 40%; margin-left: 5%;" class="form-control">' +
                                    '        <option value="plain_text" selected="selected">Plain Text</option>' +
                                    '        <option value="abap">ABAP</option>' +
                                    '        <option value="abc">ABC</option>' +
                                    '        <option value="actionscript">ActionScript</option>' +
                                    '        <option value="ada">Ada</option>' +
                                    '        <option value="apache_conf">ApachConf</option>' +
                                    '        <option value="applescript">AppleScript</option>' +
                                    '        <option value="asciidoc">AsciiDoc</option>' +
                                    '        <option value="assembly_x86">Assembly x86</option>' +
                                    '        <option value="autohotkey">AutoHotkey</option>' +
                                    '        <option value="batchfile">Batch file</option>' +
                                    '        <option value="behaviour">Behaviour</option>' +
                                    '        <option value="bro">Bro</option>' +
                                    '        <option value="c_cpp">C</option>' +
                                    '        <option value="c_cpp">C++</option>' +
                                    '        <option value="cirru">Cirru</option>' +
                                    '        <option value="clojure">Clojure</option>' +
                                    '        <option value="cobol">COBOL</option>' +
                                    '        <option value="coffee">CoffeeScript</option>' +
                                    '        <option value="coldfusion">ColdFusion</option>' +
                                    '        <option value="csharp">C#</option>' +
                                    '        <option value="csound">CSound</option>' +
                                    '        <option value="css">CSS</option>' +
                                    '        <option value="curly">curly</option>' +
                                    '        <option value="d">D</option>' +
                                    '        <option value="dart">Dart</option>' +
                                    '        <option value="diff">Diff</option>' +
                                    '        <option value="django">Django</option>' +
                                    '        <option value="dockerfile">Dockerfile</option>' +
                                    '        <option value="dot">DOT</option>' +
                                    '        <option value="drools">Drools</option>' +
                                    '        <option value="eiffel">Eiffel</option>' +
                                    '        <option value="ejs">EJS</option>' +
                                    '        <option value="elixir">Elixir</option>' +
                                    '        <option value="elm">Elm</option>' +
                                    '        <option value="erlang">Erlang</option>' +
                                    '        <option value="forth">Forth</option>' +
                                    '        <option value="fortran">Fortran</option>' +
                                    '        <option value="ftl">FTL</option>' +
                                    '        <option value="gcode">G-code</option>' +
                                    '        <option value="gherkin">Gherkin</option>' +
                                    '        <option value="gitignore">GitIgnore</option>' +
                                    '        <option value="glsl">GLSL</option>' +
                                    '        <option value="gobstones">Gobstones</option>' +
                                    '        <option value="golang">GoLang</option>' +
                                    '        <option value="graphqlschema">GraphQLSchema</option>' +
                                    '        <option value="groovy">Groovy</option>' +
                                    '        <option value="haml">Haml</option>' +
                                    '        <option value="handlebars">Handlebars</option>' +
                                    '        <option value="haskell">Haskell</option>' +
                                    '        <option value="haxe">Haxe</option>' +
                                    '        <option value="hjson">Hjson</option>' +
                                    '        <option value="html">HTML</option>' +
                                    '        <option value="ini">INI</option>' +
                                    '        <option value="io">Io</option>' +
                                    '        <option value="jack">Jack</option>' +
                                    '        <option value="jade">Jade</option>' +
                                    '        <option value="java">Java</option>' +
                                    '        <option value="javascript">JavaScript</option>' +
                                    '        <option value="json">JSON</option>' +
                                    '        <option value="jsoniq">JSONiq</option>' +
                                    '        <option value="jsp">JSP</option>' +
                                    '        <option value="jssm">JSSM</option>' +
                                    '        <option value="jsx">JSX</option>' +
                                    '        <option value="julia">Julia</option>' +
                                    '        <option value="kotlin">Kotlin</option>' +
                                    '        <option value="latex">LaTeX</option>' +
                                    '        <option value="less">Less</option>' +
                                    '        <option value="liquid">Liquid</option>' +
                                    '        <option value="lisp">Lisp</option>' +
                                    '        <option value="livescript">LiveScript</option>' +
                                    '        <option value="logiql">LogiQL</option>' +
                                    '        <option value="lsl">LSL</option>' +
                                    '        <option value="lua">Lua</option>' +
                                    '        <option value="luapage">Lua Page</option>' +
                                    '        <option value="lucene">Lucene</option>' +
                                    '        <option value="makefile">Makefile</option>' +
                                    '        <option value="markdown">Markdown</option>' +
                                    '        <option value="mask">MASK</option>' +
                                    '        <option value="matlab">MATLAB</option>' +
                                    '        <option value="maze">Maze</option>' +
                                    '        <option value="mel">MEL</option>' +
                                    '        <option value="mushcode">MUSHCode</option>' +
                                    '        <option value="mysql">MySQL</option>' +
                                    '        <option value="nix">Nix</option>' +
                                    '        <option value="nsis">NSIS</option>' +
                                    '        <option value="objectivec">Objective-C</option>' +
                                    '        <option value="ocaml">OCaml</option>' +
                                    '        <option value="pascal">Pascal</option>' +
                                    '        <option value="nsis">NSIS</option>' +
                                    '        <option value="perl">Perl</option>' +
                                    '        <option value="pgsql">pgSQL</option>' +
                                    '        <option value="php">PHP</option>' +
                                    '        <option value="pig">Pig</option>' +
                                    '        <option value="powershell">PowerShell</option>' +
                                    '        <option value="praat">Praat</option>' +
                                    '        <option value="prolog">Prolog</option>' +
                                    '        <option value="protobuf">protobuf</option>' +
                                    '        <option value="python">Python</option>' +
                                    '        <option value="r">R</option>' +
                                    '        <option value="razor">Razor</option>' +
                                    '        <option value="rdoc">RDoC</option>' +
                                    '        <option value="red">Red</option>' +
                                    '        <option value="rhtml">RHTML</option>' +
                                    '        <option value="rst">reStructuredText</option>' +
                                    '        <option value="ruby">Ruby</option>' +
                                    '        <option value="rust">Rust</option>' +
                                    '        <option value="sass">Sass</option>' +
                                    '        <option value="scad">SCAD</option>' +
                                    '        <option value="scala">Scala</option>' +
                                    '        <option value="scheme">Scheme</option>' +
                                    '        <option value="scss">Scss</option>' +
                                    '        <option value="sh">Shell script</option>' +
                                    '        <option value="sjs">SJS</option>' +
                                    '        <option value="smarty">Smarty</option>' +
                                    '        <option value="snippet">Snippet</option>' +
                                    '        <option value="soy_template">Soy Template</option>' +
                                    '        <option value="sparql">SPARQL</option>' +
                                    '        <option value="sql">SQL</option>' +
                                    '        <option value="sqlserver">SQL Server</option>' +
                                    '        <option value="stylus">Stylus</option>' +
                                    '        <option value="svg">SVG</option>' +
                                    '        <option value="swift">Swift</option>' +
                                    '        <option value="tcl">Tcl</option>' +
                                    '        <option value="tex">TeX</option>' +
                                    '        <option value="toml">TOML</option>' +
                                    '        <option value="tsx">TSX</option>' +
                                    '        <option value="turtle">Turtle</option>' +
                                    '        <option value="twig">Twig</option>' +
                                    '        <option value="typescript">TypeScript</option>' +
                                    '        <option value="vala">Vala</option>' +
                                    '        <option value="vbscript">VBScript</option>' +
                                    '        <option value="velocity">Velocity</option>' +
                                    '        <option value="verilog">Verilog</option>' +
                                    '        <option value="vhdl">VHDL</option>' +
                                    '        <option value="wollok">Wollok</option>' +
                                    '        <option value="xml">XML</option>' +
                                    '        <option value="xquery">XQuery</option>' +
                                    '        <option value="yaml">YAML</option>' +
                                    '    </select>' +
                                    '</div>' +
                                    '<div id="div_snippet_editor" style="margin-top: 20px; margin-bottom: 20px; height: calc(70vh - 100px); width: 70vw; border: 2px solid rgba(0, 0, 0, 0.5); border-radius: 8px;">' +
                                    '</div>' +
                                    '<div style="margin-top: 10px; text-align: center;">' +
                                    '    <button id="button_modal_cancel">Cancel</button>' +
                                    '    <button id="button_modal_create" style="margin-left: 5px;">Create Snippet</button>' +
                                    '</div>';

                                var v_modal = openModal(v_html);

                                var v_editor = ace.edit('div_snippet_editor');
                                v_editor.getSession().setMode('ace/mode/plain_text');
                                v_editor.setTheme("ace/theme/" + v_editor_theme);
                                v_editor.getSession().setUseSoftTabs(true);

                                var v_selectSnippetMode = document.getElementById('select_snippet_mode');

                                v_selectSnippetMode.addEventListener(
                                    'change',
                                    function(p_editor, p_event) {
                                        p_editor.getSession().setMode('ace/mode/' + this.value);
                                    }.bind(v_selectSnippetMode, v_editor)
                                );

                                var v_buttonCancel = document.getElementById('button_modal_cancel');

                                v_buttonCancel.addEventListener(
                                    'click',
                                    function(p_modal, p_event) {
                                        p_modal.remove();
                                    }.bind(v_buttonCancel, v_modal)
                                );

                                var v_buttonCreate = document.getElementById('button_modal_create');
                                v_buttonCreate.channelCode = p_chatPopUp.tag.renderedChannel;

                                v_buttonCreate.addEventListener(
                                    'click',
                                    function(p_editor, p_modal, p_event) {
                                        var v_data = {
                                            messageTitle: document.getElementById('input_snippet_title').value,
                                            messageContent: p_editor.getValue(),
                                            messageType: 3, //Snippet
                                            messageSnippetMode: document.getElementById('select_snippet_mode').value,
                                            channelCode: this.channelCode
                                        };

                                        chatSendChannelMessage(v_data);

                                        p_modal.remove();
                                    }.bind(v_buttonCreate, v_editor, v_modal)
                                );
                            }.bind(v_snippetItem, p_chatPopUp)
                        );

                        v_div.appendChild(v_snippetItem);

                        var v_uploadItem = document.createElement('div');
                        v_uploadItem.classList.add('div_chat_right_left_footer_left_options_item');
                        v_uploadItem.innerHTML = 'File Upload';

                        v_uploadItem.addEventListener(
                            'click',
                            function(p_chatPopUp, p_event) {
                                var v_inputFile = document.createElement('input');
                                v_inputFile.type = 'file';
                                v_inputFile.multiple = true;
                                v_inputFile.value = '';

                                v_inputFile.addEventListener(
                                    'change',
                                    function(p_chatPopUp, p_event) {
                                        if('files' in this && this.files.length > 0) {
                                            for(var i = 0; i < this.files.length; i++) {
                                                var v_blob = this.files[i];

                                                var v_binaryReader = new FileReader();
                                                v_binaryReader.channelCode = p_chatPopUp.tag.renderedChannel;

                                                var v_progressBar = document.createElement('div');
	                                            v_progressBar.classList.add('progress_bar');

	                                            var v_bar = document.createElement('div')
	                                            v_bar.classList.add('bar_yellow');
	                                            v_bar.style.width = '0%';
	                                            v_progressBar.appendChild(v_bar);

	                                            var v_percent = document.createElement('div');
	                                            v_percent.classList.add('percent');
	                                            v_percent.innerHTML = 'Uploading File "' + v_blob.name + '": 0%';
	                                            v_progressBar.appendChild(v_percent);

	                                            var v_binaryReader = new FileReader();
	                                            v_binaryReader.channelCode = p_chatPopUp.tag.renderedChannel;

	                                            v_binaryReader.addEventListener(
	                                                'loadstart',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    if(p_progressBar != null) {
	                                                        document.getElementById('div_chat_right_left_header').appendChild(p_progressBar)
	                                                    }
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.addEventListener(
	                                                'progress',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    if(p_event.lengthComputable) {
	                                                        if(p_progressBar != null) {
	                                                            var v_progress = parseInt(((p_event.loaded / p_event.total) * 100), 10);
	                                                            p_progressBar.firstChild.style.width = v_progress + '%';
	                                                            p_progressBar.lastChild.innerHTML = 'Uploading File "' + p_name + '": ' + v_progress + '%';
	                                                        }
	                                                    }
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.addEventListener(
	                                                'loadend',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    if(p_progressBar != null) {
	                                                        p_progressBar.firstChild.style.width = '100%';
	                                                        p_progressBar.firstChild.classList.remove('bar_yellow');
	                                                        p_progressBar.firstChild.classList.add('bar_green');
	                                                        p_progressBar.lastChild.innerHTML = 'File Upload "' + p_name + '" finished: 100%. Processing File...';
	                                                    }
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.addEventListener(
	                                                'load',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    var v_data = {
	                                                        messageAttachmentName: p_name,
	                                                        messageTitle: p_name,
	                                                        messageContent: window.btoa(p_event.target.result),
	                                                        messageType: 4, //Attachment
	                                                        channelCode: this.channelCode
	                                                    };

	                                                    var v_context = {
	                                                        progressBar: p_progressBar
	                                                    };

                                                        chatSendChannelMessage(v_data, v_context);
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.readAsBinaryString(v_blob);
                                            }
                                        }
                                    }.bind(v_inputFile, p_chatPopUp)
                                );

                                v_inputFile.click();
                            }.bind(v_uploadItem, p_chatPopUp)
                        );

                        v_div.appendChild(v_uploadItem);

                        this.parentElement.appendChild(v_div);
                        v_div.focus();
	                }.bind(v_buttonChatRightFooterLeft, p_chatPopUp)
	            );

                //Editor container
	            var v_rightFooterMiddle = document.createElement('div');
	            v_rightFooterMiddle.id = 'div_chat_right_left_footer_middle';
	            v_rightFooter.appendChild(v_rightFooterMiddle);

                var v_editor = $('#div_chat_right_left_footer_middle').emojioneArea({
				    pickerPosition: 'top',
				    filtersPosition: 'top',
				    tonesStyle: 'bullet',
                    saveEmojisAs: 'shortname',
                    useInternalCDN: false
                });

                p_chatPopUp.tag.renderedEditor = v_editor[0].emojioneArea;

                window.addEventListener(
                    'blur',
                    function(p_editor, p_event) {
                        if(p_editor != null) {
                            p_editor.altPressed = false;
                            p_editor.shiftPressed = false;
                        }
                    }.bind(window, v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.sentWriting = false;
                v_editor[0].emojioneArea.sentNotWriting = true; //true in order to avoid first message bug
                v_editor[0].emojioneArea.altPressed = false;
                v_editor[0].emojioneArea.shiftPressed = false;
                v_editor[0].selectingEmoji = false;
                v_editor[0].selectingUserMenu = null;

                v_editor[0].emojioneArea.checkSelectingUser = function() {
                    var v_return = false;

                    if(window.getSelection().rangeCount > 0) {
                        var v_range = window.getSelection().getRangeAt(0);

                        var i = v_range.startOffset;

                        var v_content = '';

                        if(v_range.startContainer.nodeType == 1) {//Element Node
                            if(v_range.startContainer.childNodes.length > v_range.startOffset) {
                                v_content = (v_range.startContainer.childNodes[v_range.startOffset].innerHTML || v_range.startContainer.childNodes[v_range.startOffset].textContent);
                            }
                        }
                        else if(v_range.startContainer.nodeType == 3) {//Text Node
                            v_content = v_range.startContainer.textContent
                        }

                        var v_char = v_content.substring(i, i + 1);

                        if(v_char == ' ' || v_char == String.fromCharCode(160)) {
                            i--;
                            v_char = v_content.substring(i, i + 1);
                        }

                        while(i >= 0 && v_char != ' ' && v_char != String.fromCharCode(160)) {
                            if(v_char == '@') {
                                v_return = true;
                                break;
                            }

                            i--;
                            v_char = v_content.substring(i, i + 1);
                        }
                    }

                    return v_return;
                }.bind(v_editor[0].emojioneArea);

                v_editor[0].emojioneArea.getSelectingUserInfo = function() {
                    var v_return = {
                        startOffset: -1,
                        endOffset: -1,
                        text: '',
                        node: null
                    };

                    var v_text = '';

                    var v_range = window.getSelection().getRangeAt(0);
                    v_return.node = v_range.startContainer;

                    var i = v_range.startOffset;
                    var v_startChar = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(i, i + 1);

                    if(v_startChar == ' ' || v_startChar == String.fromCharCode(160)) {
                        i--;
                    }

                    v_return.startOffset = i;

                    while(i >= 0) {
                        var v_char = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(i, i + 1);

                        if(v_char == '@') {
                            break;
                        }

                        v_text = v_char + v_text;

                        v_return.startOffset = i;
                        v_return.text = v_text;

                        i--;
                    }

                    i = v_range.startOffset + 1;

                    if(v_startChar == ' ' || v_startChar == String.fromCharCode(160)) {
                        i--;
                    }

                    v_return.endOffset = i;

                    while(i <= (v_range.startContainer.innerHTML || v_range.startContainer.textContent).length) {
                        var v_char = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(i, i + 1);

                        if(v_char == ' ' || v_char == String.fromCharCode(160)) {
                            break;
                        }

                        v_text += v_char;

                        v_return.endOffset = i;
                        v_return.text = v_text;

                        i++;
                    }

                    return v_return;
                }.bind(v_editor[0].emojioneArea);

                v_editor[0].emojioneArea.on(
                    'blur',
                    function(p_editor, p_event) {
                        if(this.selectingUserMenu != null) {
                            this.selectingUserMenu.classList.add('context_menu_hidden');
                        }
                    }.bind(v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.on(
                    'focus',
                    function(p_editor, p_event) {
                        if(this.checkSelectingUser()) {
                            if(this.selectingUserMenu != null) {
                                this.selectingUserMenu.classList.remove('context_menu_hidden');
                            }
                        }
                    }.bind(v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.on(
                    'keydown',
                    function(p_chatPopUp, p_editor, p_event) {
                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            this.selectingEmoji = v_dropdownMenu.style.display == 'block';
                        }
                        else {
                            this.selectingEmoji = false;
                        }

                        if(p_editor[0].innerHTML.length > 0 && !this.sentWriting) {
                            var v_data = {
                                channelCode: p_chatPopUp.tag.renderedChannel,
                                userCode: parseInt(v_user_id),
                                userWriting: true
                            };

                            chatSetChannelUserWriting(v_data);

                            this.sentWriting = true;
                            this.sentNotWriting = false;
                        }
                        else {
                            if(p_editor[0].innerHTML.length == 0 && !this.sentNotWriting) {
                                var v_data = {
                                    channelCode: p_chatPopUp.tag.renderedChannel,
                                    userCode: parseInt(v_user_id),
                                    userWriting: false
                                };

                                chatSetChannelUserWriting(v_data);

                                this.sentWriting = false;
                                this.sentNotWriting = true;
                            }
                        }

                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = true;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = true;
                        }

                        if(!this.checkSelectingUser()) {
                            if(p_event.key == '@') {
                                if(this.selectingUserMenu != null) {
                                    this.selectingUserMenu.remove();
                                }

                                var v_range = window.getSelection().getRangeAt(0);
                                var v_showMenu = false;

                                if(v_range.startOffset > 0) {
                                    var v_previousChar = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(v_range.startOffset - 1, v_range.startOffset);

                                    if(v_previousChar == String.fromCharCode(160) || v_previousChar ==  ' ') { //If it's a space
                                        v_showMenu = true;
                                    }
                                }
                                else {
                                    v_showMenu = true;
                                }

                                if(v_showMenu) {
                                    var v_channel = p_chatPopUp.tag.channelList.getChannelByCode(p_chatPopUp.tag.renderedChannel);

                                    if(v_channel != null) {
                                        var v_contextMenu = document.createElement('div');
                                        v_contextMenu.classList.add('context_menu');
                                        v_contextMenu.classList.add('notify_context_menu');
                                        v_contextMenu.style.left = '0px';
                                        v_contextMenu.tabIndex = '0';

                                        for(var i = 0; i < v_channel.userList.length; i++) {
                                            var v_contextMenuItem = document.createElement('div');
                                            v_contextMenuItem.classList.add('context_menu_item');
                                            v_contextMenuItem.innerHTML = v_channel.userList[i].login + ' (' + v_channel.userList[i].name + ')';
                                            v_contextMenuItem.value = v_channel.userList[i].login;

                                            v_contextMenuItem.addEventListener(
                                                'mousedown',
                                                function(p_editor, p_event) {
                                                    var v_info = p_editor.getSelectingUserInfo();

                                                    if(v_info.node.innerHTML != null) {
                                                        v_info.node.innerHTML = v_info.node.innerHTML.substring(0, v_info.startOffset) + this.value + '\u00A0' + v_info.node.innerHTML.substring(v_info.endOffset, v_info.node.innerHTML.length);
                                                    }
                                                    else if(v_info.node.textContent != null) {
                                                        v_info.node.textContent = v_info.node.textContent.substring(0, v_info.startOffset) + this.value + '\u00A0' + v_info.node.textContent.substring(v_info.endOffset, v_info.node.textContent.length);
                                                    }

                                                    this.parentElement.remove();
                                                    v_info.node.parentElement.focus();

                                                    var v_offset = v_info.startOffset + this.value.length + 1;

                                                    setTimeout(
                                                        function(p_node, p_offset) {
                                                            p_node.focus();

                                                            var v_selection = window.getSelection();
                                                            v_selection.collapse(p_node.firstChild, p_offset);
                                                        }.bind(null, v_info.node.parentElement, v_offset),
                                                        10
                                                    );
                                                }.bind(v_contextMenuItem, this)
                                            );

                                            v_contextMenuItem.addEventListener(
                                                'mouseenter',
                                                function(p_event) {
                                                    for(var i = 0; i < this.parentElement.children.length; i++) {
                                                        this.parentElement.children[i].classList.remove('context_menu_item_active');
                                                    }

                                                    this.classList.add('context_menu_item_active');
                                                }
                                            );

                                            v_contextMenu.appendChild(v_contextMenuItem);
                                        }

                                        v_contextMenu.firstChild.classList.add('context_menu_item_active');

                                        document.getElementById('div_chat_right_left_footer_left').appendChild(v_contextMenu);

                                        v_contextMenu.style.width = document.getElementById('div_chat_right_left_footer').offsetWidth + 'px';
                                        v_contextMenu.style.top = - 5 - v_contextMenu.offsetHeight + 'px';

                                        this.selectingUserMenu = v_contextMenu;
                                    }
                                }

                                return;
                            }
                        }
                        else {
                            if(this.selectingUserMenu != null) {
                                var v_visibleItems = this.selectingUserMenu.querySelectorAll('.context_menu_item:not(.context_menu_item_hidden)');

                                if(v_visibleItems.length > 0) {
                                    if(p_event.keyCode == 38) {//Arrow Up
                                        p_event.preventDefault();

                                        var i = 0;

                                        for(i; i < v_visibleItems.length; i++) {
                                            if(v_visibleItems[i].classList.contains('context_menu_item_active')) {
                                                v_visibleItems[i].classList.remove('context_menu_item_active');
                                                break;
                                            }
                                        }

                                        if(v_visibleItems.length == 1) {
                                            v_visibleItems[i].classList.add('context_menu_item_active');
                                        }
                                        else {
                                            if(i == 0) {
                                                v_visibleItems[v_visibleItems.length - 1].classList.add('context_menu_item_active');
                                            }
                                            else {
                                                v_visibleItems[i - 1].classList.add('context_menu_item_active');
                                            }
                                        }
                                    }
                                    else if(p_event.keyCode == 40) {//Arrow Down
                                        p_event.preventDefault();

                                        var i = 0;

                                        for(i; i < v_visibleItems.length; i++) {
                                            if(v_visibleItems[i].classList.contains('context_menu_item_active')) {
                                                v_visibleItems[i].classList.remove('context_menu_item_active');
                                                break;
                                            }
                                        }

                                        if(v_visibleItems.length == 1) {
                                            v_visibleItems[i].classList.add('context_menu_item_active');
                                        }
                                        else {
                                            if(i == v_visibleItems.length - 1) {
                                                v_visibleItems[0].classList.add('context_menu_item_active');
                                            }
                                            else {
                                                v_visibleItems[i + 1].classList.add('context_menu_item_active');
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        if(p_event.keyCode == 13) { //Enter
                            p_event.preventDefault();

                            if(!this.checkSelectingUser()) {
                                if(this.altPressed || this.shiftPressed) {
                                    var v_selection = window.getSelection();
                                    var v_range = v_selection.getRangeAt(0);
                                    var v_div = document.createElement('div');
                                    var v_br = document.createElement('br');
                                    v_div.appendChild(v_br);
                                    v_range.deleteContents();
                                    v_range.insertNode(v_div);
                                    v_range.setStartAfter(v_div);
                                    v_range.setEndAfter(v_div);
                                    v_range.collapse(false);
                                    v_selection.removeAllRanges();
                                    v_selection.addRange(v_range);
                                }
                            }
                        }
                    }.bind(v_editor[0].emojioneArea, p_chatPopUp)
                );

                v_editor[0].emojioneArea.on(
                    'keyup',
                    function(p_chatPopUp, p_editor, p_event) {
                        if(p_editor[0].innerHTML.length > 0 && !this.sentWriting) {
                            var v_data = {
                                channelCode: p_chatPopUp.tag.renderedChannel,
                                userCode: parseInt(v_user_id),
                                userWriting: true
                            };

                            chatSetChannelUserWriting(v_data);

                            this.sentWriting = true;
                            this.sentNotWriting = false;
                        }
                        else {
                            if(p_editor[0].innerHTML.length == 0 && !this.sentNotWriting) {
                                var v_data = {
                                    channelCode: p_chatPopUp.tag.renderedChannel,
                                    userCode: parseInt(v_user_id),
                                    userWriting: false
                                };

                                chatSetChannelUserWriting(v_data);

                                this.sentWriting = false;
                                this.sentNotWriting = true;
                            }
                        }

                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = false;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = false;
                        }

                        if(this.checkSelectingUser()) {
                            if(p_event.keyCode != 38 && p_event.keyCode != 40 && p_event.keyCode != 13) {//Arrow Up | Arrow Down | Enter
                                if(this.selectingUserMenu != null) {
                                    this.selectingUserMenu.classList.remove('context_menu_hidden');

                                    var v_text = this.getSelectingUserInfo().text;

                                    for(var i = 0; i < this.selectingUserMenu.children.length; i++) {
                                        this.selectingUserMenu.children[i].classList.remove('context_menu_item_hidden');

                                        if(this.selectingUserMenu.children[i].innerHTML.indexOf(v_text) == -1) {
                                            this.selectingUserMenu.children[i].classList.add('context_menu_item_hidden');
                                        }
                                    }

                                    this.selectingUserMenu.style.top = - 5 - this.selectingUserMenu.offsetHeight + 'px';

                                    for(var i = 0; i < this.selectingUserMenu.children.length; i++) {
                                        this.selectingUserMenu.children[i].classList.remove('context_menu_item_active');
                                    }

                                    var v_visibleItems = this.selectingUserMenu.querySelectorAll('.context_menu_item:not(.context_menu_item_hidden)');

                                    if(v_visibleItems.length > 0) {
                                        v_visibleItems[0].classList.add('context_menu_item_active');
                                    }
                                }
                            }
                        }
                        else {
                            if(this.selectingUserMenu != null) {
                                this.selectingUserMenu.classList.add('context_menu_hidden');
                            }
                        }

                        if(p_event.keyCode == 13 && !this.selectingEmoji && !this.altPressed && !this.shiftPressed) { //Enter and not selecting emoticons or inserting new lines
                            p_event.preventDefault();

                            if(this.checkSelectingUser() && this.selectingUserMenu != null) {
                                var v_active = this.selectingUserMenu.querySelector('.context_menu_item_active');

                                if(v_active != null) {
                                    var v_info = this.getSelectingUserInfo();

                                    if(v_info.node.textContent != null) {
                                        v_info.node.textContent = v_info.node.textContent.substring(0, v_info.startOffset) + v_active.value + '\u00A0' + v_info.node.textContent.substring(v_info.endOffset, v_info.node.textContent.length);
                                    }
                                    else if(v_info.node.innerHTML != null) {
                                        v_info.node.innerHTML = v_info.node.innerHTML.substring(0, v_info.startOffset) + v_active.value + '\u00A0' + v_info.node.innerHTML.substring(v_info.endOffset, v_info.node.innerHTML.length);
                                    }

                                    this.selectingUserMenu.remove();
                                    v_info.node.parentElement.focus();

                                    var v_offset = v_info.startOffset + v_active.value.length + 1;

                                    setTimeout(
                                        function(p_node, p_offset) {
                                            p_node.focus();

                                            var v_selection = window.getSelection();
                                            v_selection.collapse(p_node.firstChild, p_offset);
                                        }.bind(null, v_info.node.parentElement, v_offset),
                                        10
                                    );
                                }
                            }
                            else {
                                if(p_editor[0].innerHTML.length > 0) {
                                    var v_data = {
                                        messageType: 1, //Plain Text
                                        messageContent: p_editor[0].innerHTML,
                                        messageRawContent: this.getText(),
                                        channelCode: p_chatPopUp.tag.renderedChannel
                                    }

                                    chatSendChannelMessage(v_data);

                                    this.setText('');
                                    p_editor[0].focus();

                                    var v_data = {
                                        channelCode: p_chatPopUp.tag.renderedChannel,
                                        userCode: parseInt(v_user_id),
                                        userWriting: false
                                    };

                                    chatSetChannelUserWriting(v_data);

                                    this.sentWriting = false;
                                    this.sentNotWriting = true;
                                }
                            }
                        }
                    }.bind(v_editor[0].emojioneArea, p_chatPopUp)
                );

                //Using third party software (emojioneArea), so we need an observer to know when things are ready to be used
                var v_mutationObserver = new MutationObserver(
                    function(p_chatPopUp, p_mutationList, p_this) {
						var v_editor = document.querySelector('.emojionearea-editor');

                        if(v_editor != null) {
                            v_editor.addEventListener(
                                'paste',
                                function(p_chatPopUp, p_event) {
                                    var v_items = (p_event.clipboardData || p_event.originalEvent.clipboardData).items;

                                    for(v_key in v_items) {
                                        var v_item = v_items[v_key];

			                            if(v_item.kind === 'file') {
                                            var v_blob = v_item.getAsFile();

                                            if(v_blob.type.indexOf('image') == -1) {
                                                return;
                                            }

                                            var v_name = 'Pasted image at ' + formatTimestamp(new Date()) + '.png';

                                            var v_progressBar = document.createElement('div');
                                            v_progressBar.classList.add('progress_bar');

                                            var v_bar = document.createElement('div')
                                            v_bar.classList.add('bar_yellow');
                                            v_bar.style.width = '0%';
                                            v_progressBar.appendChild(v_bar);

                                            var v_percent = document.createElement('div');
                                            v_percent.classList.add('percent');
                                            v_percent.innerHTML = 'Uploading File "' + v_name + '": 0%';
                                            v_progressBar.appendChild(v_percent);

                                            var v_binaryReader = new FileReader();
                                            v_binaryReader.channelCode = p_chatPopUp.tag.renderedChannel;

                                            v_binaryReader.addEventListener(
                                                'loadstart',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    if(p_progressBar != null) {
                                                        document.getElementById('div_chat_right_left_header').appendChild(p_progressBar)
                                                    }
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.addEventListener(
                                                'progress',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    if(p_event.lengthComputable) {
                                                        if(p_progressBar != null) {
	                                                        var v_progress = parseInt(((p_event.loaded / p_event.total) * 100), 10);
	                                                        p_progressBar.firstChild.style.width = v_progress + '%';
	                                                        p_progressBar.lastChild.innerHTML = 'Uploading File "' + p_name + '": ' + v_progress + '%';
                                                        }
                                                    }
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.addEventListener(
                                                'loadend',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    if(p_progressBar != null) {
	                                                    p_progressBar.firstChild.style.width = '100%';
	                                                    p_progressBar.firstChild.classList.remove('bar_yellow');
	                                                    p_progressBar.firstChild.classList.add('bar_green');
	                                                    p_progressBar.lastChild.innerHTML = 'File Upload "' + p_name + '" finished: 100%. Processing File...';
                                                    }
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.addEventListener(
                                                'load',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    var v_data = {
                                                        messageAttachmentName: p_name,
                                                        messageTitle: p_name,
                                                        messageContent: window.btoa(p_event.target.result),
                                                        messageType: 2,//Pasted image
                                                        channelCode: this.channelCode
                                                    };

                                                    var v_context = {
                                                        progressBar: p_progressBar
                                                    };

                                                    chatSendChannelMessage(v_data, v_context);
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.readAsBinaryString(v_blob);
                                        }
                                    }
                                }.bind(v_editor, p_chatPopUp)
                            );

                            v_editor.addEventListener(
                                'drop',
                                function(p_chatPopUp, p_event) {
                                    for(var i = 0; i < p_event.dataTransfer.files.length; i++) {
            							var v_blob = p_event.dataTransfer.files[i];

                                        var v_binaryReader = new FileReader();
                                        v_binaryReader.channelCode = p_chatPopUp.tag.renderedChannel;

                                        var v_progressBar = document.createElement('div');
                                        v_progressBar.classList.add('progress_bar');

                                        var v_bar = document.createElement('div')
                                        v_bar.classList.add('bar_yellow');
                                        v_bar.style.width = '0%';
                                        v_progressBar.appendChild(v_bar);

                                        var v_percent = document.createElement('div');
                                        v_percent.classList.add('percent');
                                        v_percent.innerHTML = 'Uploading File "' + v_blob.name + '": 0%';
                                        v_progressBar.appendChild(v_percent);

                                        var v_binaryReader = new FileReader();
                                        v_binaryReader.channelCode = p_chatPopUp.tag.renderedChannel;

                                        v_binaryReader.addEventListener(
                                            'loadstart',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                if(p_progressBar != null) {
                                                    document.getElementById('div_chat_right_left_header').appendChild(p_progressBar)
                                                }
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.addEventListener(
                                            'progress',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                if(p_event.lengthComputable) {
                                                    if(p_progressBar != null) {
                                                        var v_progress = parseInt(((p_event.loaded / p_event.total) * 100), 10);
                                                        p_progressBar.firstChild.style.width = v_progress + '%';
                                                        p_progressBar.lastChild.innerHTML = 'Uploading File "' + p_name + '": ' + v_progress + '%';
                                                    }
                                                }
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.addEventListener(
                                            'loadend',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                if(p_progressBar != null) {
                                                    p_progressBar.firstChild.style.width = '100%';
                                                    p_progressBar.firstChild.classList.remove('bar_yellow');
                                                    p_progressBar.firstChild.classList.add('bar_green');
                                                    p_progressBar.lastChild.innerHTML = 'File Upload "' + p_name + '" finished: 100%. Processing File...';
                                                }
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.addEventListener(
                                            'load',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                var v_data = {
                                                    messageAttachmentName: p_name,
                                                    messageTitle: p_name,
                                                    messageContent: window.btoa(p_event.target.result),
                                                    messageType: 4, //Attachment
                                                    channelCode: this.channelCode
                                                };

                                                var v_context = {
                                                    progressBar: p_progressBar
                                                };

                                                chatSendChannelMessage(v_data, v_context);
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.readAsBinaryString(v_blob);
                                    }
                                }.bind(v_editor, p_chatPopUp)
                            );

							p_this.disconnect(); // stop observing
						    return;
						}
                    }.bind(v_mutationObserver, p_chatPopUp)
                );

                v_mutationObserver.observe(
                    document,
                    {
                        childList: true,
                        subtree: true
                    }
                );

                //Position scroll on first unread message
                for(var i = v_channel.messageList.length - 1; i >= 0; i--) {
                    if(!v_channel.messageList[i].viewed) {
                        v_firstUnreadMessageCode = v_channel.messageList[i].code
                        break;
                    }
                }
            }
            else {
                v_divChatRightContent.innerHTML = '';
            }

            for(var i = 0; i < v_channel.messageList.length; i++) {
                var j = i;

                for(j; j < v_channel.messageList.length; j++) {
                    if(v_channel.messageList[i].user.code != v_channel.messageList[j].user.code) {
                        break;
                    }

                    var v_item = p_chatPopUp.tag.getRenderedChannelMessage(v_channel.code, v_channel.messageList[j], false);
                    v_divChatRightContent.insertBefore(v_item, v_divChatRightContent.firstChild);
                }

                v_divChatRightContent.children[0].remove();
                var v_item = p_chatPopUp.tag.getRenderedChannelMessage(v_channel.code, v_channel.messageList[j - 1], true);
                v_divChatRightContent.insertBefore(v_item, v_divChatRightContent.firstChild);
                i = j - 1;
            }

            var v_actualDate = '';
            var v_itemList = document.querySelectorAll('#div_chat_right_left_content > .div_chat_right_left_item');

            for(var j = 0; j < v_itemList.length; j++) {
                //If date has changed, then add date mark
                if(v_itemList[j].createdAt.substring(0, 10) != v_actualDate) {
                    v_actualDate = v_itemList[j].createdAt.substring(0, 10);

                    var v_h2SideLinesContainer = document.createElement('h2');
                    v_h2SideLinesContainer.classList.add('h2_side_lines_container');

                    var v_spanSideLinesContent = document.createElement('span');
                    v_spanSideLinesContent.classList.add('span_side_lines_content');
                    v_spanSideLinesContent.innerHTML = v_actualDate;
                    v_h2SideLinesContainer.appendChild(v_spanSideLinesContent);

                    v_divChatRightContent.insertBefore(v_h2SideLinesContainer, v_itemList[j]);
                }
            }

            //Remove first date mark
            if(v_divChatRightContent.children.length > 0) {
                v_divChatRightContent.children[0].remove();
            }

            if(p_renderAtMessage != null) {
                for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                    if(v_divChatRightContent.childNodes[i].messageCode == p_renderAtMessage) {
                        v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                        break;
                    }
                }
            }
            else {
                if(v_sameChannel) {
                    if(v_onLastMessage) {
                        v_divChatRightContent.scrollTop = v_divChatRightContent.scrollHeight;
                    }
                    else {
                        if(v_firstVisibleMessageCode != null) {
                            for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                                if(v_divChatRightContent.childNodes[i].messageCode == v_firstVisibleMessageCode) {
                                    v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                                    break;
                                }
                            }
                        }
                    }
                }
                else {
                    if(v_firstUnreadMessageCode != null) {
                        for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                            if(v_divChatRightContent.childNodes[i].messageCode == v_firstUnreadMessageCode) {
                                v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                                break;
                            }
                        }
                    }
                    else {
                        v_divChatRightContent.scrollTop = v_divChatRightContent.scrollHeight - v_divChatRightContent.offsetHeight;
                    }
                }
            }

            var v_channelElementList = document.querySelectorAll('#div_chat_channels > .div_chat_left_content > .div_chat_left_content_item');

            for(var i = 0; i < v_channelElementList.length; i++) {
                if(v_channelElementList[i].channelCode == p_channelCode) {
                    v_channelElementList[i].classList.add('div_chat_left_content_item_active');
                    break;
                }
            }

            //Mark messages as read, if it's the case
            if((v_divChatRightContent.offsetHeight + v_divChatRightContent.scrollTop + 1) >= v_divChatRightContent.scrollHeight) {
                var v_messageCodeList = [];

	            for(var i = 0; i < v_channel.messageList.length; i++) {
	                if(!v_channel.messageList[i].viewed) {
	                    v_messageCodeList.push(v_channel.messageList[i].code);
	                }
	            }

	            if(v_messageCodeList.length > 0) {
	                var v_data = {
	                    channelCode: v_channel.code,
	                    messageCodeList: v_messageCodeList
	                };

	                chatMarkChannelMessagesAsRead(v_data);
	            }
            }

            var v_channelContext = p_chatPopUp.tag.contextList.getContextByChannelCode(v_channel.code);

            if(v_channelContext != null) {
                if(!v_channelContext.firstRender) {
                    p_chatPopUp.tag.renderedEditor.setText(v_channelContext.text);

                    if(!p_preventContextScroll) {
                        p_chatPopUp.tag.renderedContent.scrollTop = v_channelContext.scrollTop + 1; //In order to avoid bug and recover messages
                    }
                }
                else {
                    v_channelContext.firstRender = false;
                }
            }
        }

        p_chatPopUp.tag.updateHeader();
    }.bind(v_chatPopUp.tag.renderChannel, v_chatPopUp);

    v_chatPopUp.tag.getRenderedGroupMessage = function(p_chatPopUp, p_groupCode, p_message, p_withHeader) {
        var v_item = document.createElement('div');
        v_item.messageCode = p_message.code;
        v_item.groupCode = p_groupCode;
        v_item.userCode = p_message.user.code;
        v_item.classList.add('div_chat_right_left_item');
        v_item.createdAt = p_message.createdAt;

        if(p_message.createdAt != p_message.updatedAt) {//Message was edited
            v_item.title = p_message.updatedAt + ' (Edited)';
        }
        else {
            v_item.title = p_message.createdAt;
        }

        var v_messageBody = document.createElement('div');
        v_messageBody.classList.add('div_chat_right_left_item_body');
        v_messageBody.classList.add('div_chat_right_left_item_body_padding');

        var v_messageContent = document.createElement('div');
        v_messageContent.classList.add('div_chat_right_left_item_content');

        switch(p_message.type) {
            case 1: { //Plain text
                v_messageContent.classList.add('div_chat_message_plain_text');
                v_messageContent.innerHTML = p_message.content;

                break;
            }
            case 2: { //Pasted image
                v_messageContent.classList.add('div_chat_message_pasted_img');
                v_messageContent.innerHTML = p_message.title;

                var v_img = document.createElement('img');
                v_img.src = gv_chatAttachmentPath + '/' + p_message.code;

                v_img.addEventListener(
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
                        v_imgShowImage.src = this.src;

                        v_divContainerImg.appendChild(v_imgShowImage);
                        v_divShowImage.appendChild(v_divContainerImg);
                        document.body.appendChild(v_divShowImage);
                    }
                );

                v_messageContent.appendChild(v_img);

                break;
            }
            case 3: { //Snippet
                v_messageContent.classList.add('div_chat_message_snippet');

                var v_div = document.createElement('div');
                v_div.innerHTML = 'Snippet Upload';
                v_messageContent.appendChild(v_div);

                var v_container = document.createElement('div');
                v_container.classList.add('div_chat_message_snippet_container');

                var v_img = document.createElement('img');
                v_img.src = '/static/OmniDB_app/images/icons/extension_chat_code.png';
                v_img.title = 'Click to open the Snippet';
                v_container.appendChild(v_img);

                var v_divName = document.createElement('div');
                v_divName.innerHTML = p_message.title;
                v_container.appendChild(v_divName);

                v_messageContent.appendChild(v_container);

                break;
            }
            case 4: { //Attachment
                v_messageContent.classList.add('div_chat_message_attachment');

                var v_extension = p_message.attachmentName.split('.').pop().toLowerCase();

                switch(v_extension) {
                    case 'jpeg':
                    case 'png':
                    case 'jpg': {
                        v_messageContent.innerHTML = p_message.title;

                        var v_img = document.createElement('img');
                        v_img.src = gv_chatAttachmentPath + '/' + p_message.code;

                        v_img.addEventListener(
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
                                v_imgShowImage.src = this.src;

                                v_divContainerImg.appendChild(v_imgShowImage);
                                v_divShowImage.appendChild(v_divContainerImg);
                                document.body.appendChild(v_divShowImage);
                            }
                        );

                        v_messageContent.appendChild(v_img);

                        break;
                    }
                    default: {
                        var v_div = document.createElement('div');
                        v_div.innerHTML = 'File Upload';
                        v_messageContent.appendChild(v_div);

                        var v_container = document.createElement('div');
                        v_container.classList.add('div_chat_message_attachment_container');

                        var v_img = document.createElement('img');
                        v_img.title = 'Click to download file.';

                        switch(v_extension) {
                            case '3gp':
                            case 'aac':
                            case 'aiff':
                            case 'asp':
                            case 'aspx':
                            case 'avi':
                            case 'bin':
                            case 'bmp':
                            case 'c':
                            case 'cpp':
                            case 'css':
                            case 'csv':
                            case 'dat':
                            case 'db':
                            case 'dll':
                            case 'dmg':
                            case 'doc':
                            case 'docx':
                            case 'exe':
                            case 'flv':
                            case 'h':
                            case 'html':
                            case 'ico':
                            case 'ics':
                            case 'iso':
                            case 'java':
                            case 'js':
                            case 'key':
                            case 'log':
                            case 'mdb':
                            case 'mid':
                            case 'mp3':
                            case 'mp4':
                            case 'odp':
                            case 'odt':
                            case 'ots':
                            case 'ott':
                            case 'pdf':
                            case 'php':
                            case 'pps':
                            case 'ppt':
                            case 'pptx':
                            case 'psd':
                            case 'py':
                            case 'rar':
                            case 'rb':
                            case 'rtf':
                            case 'sql':
                            case 'svg':
                            case 'sys':
                            case 'tex':
                            case 'tga':
                            case 'tgz':
                            case 'txt':
                            case 'wav':
                            case 'xls':
                            case 'xlsx':
                            case 'xml':
                            case 'zip': {
                                v_img.src = '/static/OmniDB_app/images/icons/extension_chat_' + v_extension + '.png';
                                break;
                            }
                            default: {
                                v_img.alt = v_extension;
                            }
                        }

                        v_img.addEventListener(
                            'click',
                            function(p_message, p_event) {
                                var v_link = document.createElement('a');
                                v_link.href = gv_chatAttachmentPath + '/' + p_message.code;
                                v_link.download = p_message.attachmentName;
                                v_link.click();
                                v_link.remove();
                            }.bind(v_img, p_message)
                        );

                        v_container.appendChild(v_img);

                        var v_divName = document.createElement('div');
                        v_divName.innerHTML = p_message.attachmentName;
                        v_container.appendChild(v_divName);

                        if(v_extension == 'mp3' || v_extension == 'ogg' || v_extension == 'wav') {
                            var v_audio = document.createElement('audio');
                            v_audio.controls = true;
                            v_audio.controlsList= 'nodownload';

                            var v_source = document.createElement('source');
                            v_source.src = gv_chatAttachmentPath + '/' + p_message.code;
                            v_source.type = 'audio/' + v_extension;
                            v_audio.appendChild(v_source);

                            v_container.appendChild(v_audio);
                        }

                        if(v_extension == 'mp4') {
                            var v_video = document.createElement('video');
                            v_video.controls = true;
                            v_video.controlsList= 'nodownload';

                            var v_source = document.createElement('source');
                            v_source.src = gv_chatAttachmentPath + '/' + p_message.code;
                            v_source.type = 'video/mp4';
                            v_video.appendChild(v_source);

                            v_container.appendChild(v_video);
                        }

                        v_messageContent.appendChild(v_container);

                        break;
                    }
                }

                break;
            }
            case 5: {//Mention
                v_messageContent.classList.add('div_chat_message_mention');
                v_messageContent.innerHTML = p_message.content;

                break;
            }
        }

        v_messageBody.appendChild(v_messageContent);
        v_item.appendChild(v_messageBody);

        //Context menu shown on message hover
        var v_contextMenu = document.createElement('div');
        v_contextMenu.classList.add('context_menu');
        v_contextMenu.classList.add('context_menu_fit');
        v_contextMenu.classList.add('context_menu_hidden');
        v_contextMenu.style.top = '-15px';
        v_contextMenu.style.right = '3px';
        v_contextMenu.style.left = 'auto';
        v_contextMenu.style.borderRadius = '10px';
        v_contextMenu.tabIndex = '0';

        var v_actionDelete = document.createElement('div');
        v_actionDelete.classList.add('context_menu_item');
        v_actionDelete.classList.add('context_menu_item_inline');
        v_actionDelete.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_delete.png" class="context_menu_item_img" />';
        v_actionDelete.title = 'Delete Message';

        v_actionDelete.addEventListener(
            'click',
            function(p_item, p_message, p_event) {
                var v_innerHTML = '';

                if(p_item.children[0].classList.contains('div_chat_right_left_item_body_padding')) {
                    var v_div = document.createElement('div');
                    v_div.innerHTML = p_item.outerHTML;

                    var v_time = p_message.createdAt.substring(11, 16);

                    //Prepend message header
                    var v_messageHeader = document.createElement('div');
                    v_messageHeader.innerHTML = p_message.user.login + ' <span class="span_chat_right_item_header">' + v_time + '</span>';
                    v_messageHeader.classList.add('div_chat_right_left_item_header');
                    v_div.firstChild.firstChild.insertBefore(v_messageHeader, v_div.firstChild.firstChild.firstChild);

                    //Prepend user icon
                    var v_userImg = document.createElement('img');
                    v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
                    v_userImg.classList.add('img_chat_user');
                    v_div.firstChild.insertBefore(v_userImg, v_div.firstChild.firstChild);

                    v_div.firstChild.childNodes[1].classList.remove('div_chat_right_left_item_body_padding');

                    v_innerHTML = v_div.innerHTML;
                    v_div.remove();
                }
                else {
                    v_innerHTML = p_item.outerHTML;
                }

                var v_html =
                    '<div style="margin-bottom: 20px;">' +
                    '    Do you really want to delete the message below? This operation cannot be undone.' +
                    '</div>' +
                    '<div>' +
                    v_innerHTML +
                    '</div>' +
                    '<div style="margin-top: 10px; text-align: center;">' +
                    '    <button id="button_modal_no">No</button>' +
                    '    <button id="button_modal_yes" style="margin-left: 5px;">Yes</button>' +
                    '</div>';

                var v_modal = openModal(v_html);

                var v_buttonNo = document.getElementById('button_modal_no');

                v_buttonNo.addEventListener(
                    'click',
                    function(p_modal, p_event) {
                        p_modal.remove();
                    }.bind(v_buttonNo, v_modal)
                );

                var v_buttonYes = document.getElementById('button_modal_yes');

                v_buttonYes.addEventListener(
                    'click',
                    function(p_item, p_modal, p_event) {
                        p_modal.remove();

                        var v_data = {
                            groupCode: p_item.groupCode,
                            messageCode: p_item.messageCode
                        };

                        chatRemoveGroupMessage(v_data);
                    }.bind(v_buttonYes, p_item, v_modal)
                );

                v_buttonNo.focus();
            }.bind(v_actionDelete, v_item, p_message)
        );

        v_contextMenu.appendChild(v_actionDelete);

        var v_actionMention = document.createElement('div');
        v_actionMention.classList.add('context_menu_item');
        v_actionMention.classList.add('context_menu_item_inline');
        v_actionMention.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_mention.png" class="context_menu_item_img" />';
        v_actionMention.title = 'Comment Message';

        v_actionMention.addEventListener(
            'click',
            function(p_item, p_message, p_event) {
                var v_dropdownMenu = document.querySelectorAll('.dropdown-menu.textcomplete-dropdown');

                if(v_dropdownMenu != null && v_dropdownMenu.length > 0) {
                    for(var i = 0; i < v_dropdownMenu.length; i++) {
                        v_dropdownMenu[i].remove();
                    }
                }

                var v_innerHTML = '';

                if(p_item.children[0].classList.contains('div_chat_right_left_item_body_padding')) {
                    var v_div = document.createElement('div');
                    v_div.innerHTML = p_item.outerHTML;

                    var v_time = p_message.createdAt.substring(11, 16);

                    //Prepend message header
                    var v_messageHeader = document.createElement('div');
                    v_messageHeader.innerHTML = p_message.user.login + ' <span class="span_chat_right_item_header">' + v_time + '</span>';
                    v_messageHeader.classList.add('div_chat_right_left_item_header');
                    v_div.firstChild.firstChild.insertBefore(v_messageHeader, v_div.firstChild.firstChild.firstChild);

                    //Prepend user icon
                    var v_userImg = document.createElement('img');
                    v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
                    v_userImg.classList.add('img_chat_user');
                    v_div.firstChild.insertBefore(v_userImg, v_div.firstChild.firstChild);

                    v_div.firstChild.childNodes[1].classList.remove('div_chat_right_left_item_body_padding');

                    v_innerHTML = v_div.innerHTML;
                    v_div.remove();
                }
                else {
                    v_innerHTML = p_item.outerHTML;
                }

                var v_html =
                    '<div style="margin-bottom: 20px;">' +
                    '    <div id="div_chat_message_mention_content">' +
                    '    </div>' +
                    '</div>' +
                    '<div>' +
                    v_innerHTML +
                    '</div>' +
                    '<div style="margin-top: 10px; text-align: center;">' +
                    '    <button id="button_modal_cancel">Cancel</button>' +
                    '    <button id="button_modal_ok" style="margin-left: 5px;">Ok</button>' +
                    '</div>';

                var v_modal = openModal(v_html);

                document.querySelector('.modal_content').style.width = '70vw';

                var v_editor = $('#div_chat_message_mention_content').emojioneArea({
                    pickerPosition: 'top',
                    filtersPosition: 'top',
                    tonesStyle: 'bullet',
                    placeholder: 'Type your comment...',
                    saveEmojisAs: 'shortname',
                    useInternalCDN: false
                });

                window.addEventListener(
                    'blur',
                    function(p_editor, p_event) {
                        if(p_editor != null) {
                            p_editor.altPressed = false;
                            p_editor.shiftPressed = false;
                        }
                    }.bind(window, v_editor[0].emojioneArea)
                );

                var v_buttonCancel = document.getElementById('button_modal_cancel');

                v_buttonCancel.addEventListener(
                    'click',
                    function(p_modal, p_event) {
                        p_modal.remove();

                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            v_dropdownMenu.remove();
                        }
                    }.bind(v_buttonCancel, v_modal)
                );

                var v_buttonOk = document.getElementById('button_modal_ok');

                v_buttonOk.addEventListener(
                    'click',
                    function(p_item, p_modal, p_messageContent, p_editor, p_event) {
                        var v_data = {
                            messageType: 5, //Mentioned message
                            groupCode: p_item.groupCode,
                            mentionedMessageContent: p_messageContent,
                            commentMessageRawContent: p_editor[0].emojioneArea.getText(),
                            commentMessageContent: p_editor[0].emojioneArea.editor[0].innerHTML
                        };

                        chatSendGroupMessage(v_data);

                        p_modal.remove();

                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            v_dropdownMenu.remove();
                        }
                    }.bind(v_buttonOk, p_item, v_modal, v_innerHTML, v_editor)
                );

                v_editor[0].emojioneArea.altPressed = false;
                v_editor[0].emojioneArea.shiftPressed = false;
                v_editor[0].selectingEmoji = false;

                v_editor[0].emojioneArea.on(
                    'keydown',
                    function(p_editor, p_event) {
                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            this.selectingEmoji = v_dropdownMenu.style.display == 'block';
                        }
                        else {
                            this.selectingEmoji = false;
                        }

                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = true;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = true;
                        }

                        if(p_event.keyCode == 13) { //Enter
                            p_event.preventDefault();

                            if(this.altPressed || this.shiftPressed) {
                                var v_selection = window.getSelection();
                                var v_range = v_selection.getRangeAt(0);
                                var v_div = document.createElement('div');
                                var v_br = document.createElement('br');
                                v_div.appendChild(v_br);
                                v_range.deleteContents();
                                v_range.insertNode(v_div);
                                v_range.setStartAfter(v_div);
                                v_range.setEndAfter(v_div);
                                v_range.collapse(false);
                                v_selection.removeAllRanges();
                                v_selection.addRange(v_range);
                            }
                        }
                    }.bind(v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.on(
                    'keyup',
                    function(p_buttonOk, p_editor, p_event) {
                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = false;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = false;
                        }

                        if(p_event.keyCode == 13 && !this.selectingEmoji && !this.altPressed && !this.shiftPressed) { //Enter and not selecting emoticons or inserting new lines
                            p_event.preventDefault();

                            if(p_editor[0].innerHTML.length > 0) {
                                p_buttonOk.click();
                            }
                        }
                    }.bind(v_editor[0].emojioneArea, v_buttonOk)
                );

                v_editor[0].emojioneArea.setText('');
                v_editor[0].nextSibling.childNodes[0].focus();
            }.bind(v_actionMention, v_item, p_message)
        );

        v_contextMenu.appendChild(v_actionMention);

        var v_actionShare = document.createElement('div');
        v_actionShare.classList.add('context_menu_item');
        v_actionShare.classList.add('context_menu_item_inline');
        v_actionShare.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_share.png" class="context_menu_item_img" />';
        v_actionShare.title = 'Forward Message';

        v_actionShare.addEventListener(
            'click',
            function(p_item, p_event) {
                var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

                if(v_chatPopUp != null) {
                    var v_html =
                        '<div class="div_chat_right_left_item">' +
                        p_item.querySelector('.div_chat_right_left_item_content').outerHTML +
                        '</div>' +
                        '<div id="div_share_with">' +
                        '    <span id="span_share_with">Forward to: </span>' +
                        '    <select id="select_share_message_with" class="form-control">';

                    var v_channelItems = document.querySelectorAll('#div_chat_channels .div_chat_left_content_item');

                    for(var i = 0; i < v_channelItems.length; i++) {
                        v_html += '        <option value="channel_' + v_channelItems[i].channelCode + '">' + v_channelItems[i].childNodes[1].textContent + '</option>';
                    }

                    var v_groupItems = document.querySelectorAll('#div_chat_groups .div_chat_left_content_item');

                    for(var i = 0; i < v_groupItems.length; i++) {
                        v_html += '        <option value="group_' + v_groupItems[i].groupCode + '">' + v_groupItems[i].childNodes[1].textContent + '</option>';
                    }

                    v_html +=
                        '    </select>' +
                        '</div>' +
                        '<div id="div_share_with_footer">' +
                        '    <button id="button_modal_cancel">Cancel</button>' +
                        '    <button id="button_modal_ok">Ok</button>' +
                        '</div>';

                    var v_modal = openModal(v_html);

                    document.querySelector('.modal_content').style.maxWidth = '60vw';

                    var v_buttonCancel = document.getElementById('button_modal_cancel');

                    v_buttonCancel.addEventListener(
                        'click',
                        function(p_modal, p_event) {
                            p_modal.remove();
                        }.bind(v_buttonCancel, v_modal)
                    );

                    var v_buttonOk = document.getElementById('button_modal_ok');

                    v_buttonOk.addEventListener(
                        'click',
                        function(p_modal, p_item, p_event) {
                            var v_selectedValue = document.getElementById('select_share_message_with').value;
                            var v_type = v_selectedValue.split('_')[0];
                            var v_code = parseInt(v_selectedValue.split('_').pop());

                            switch(v_type) {
                                case 'channel': {
                                    var v_data = {
                                        forwardMessageCode: p_item.messageCode,
                                        channelCode: v_code,
                                        messageType: 0
                                    };

                                    chatSendChannelMessage(v_data);

                                    break;
                                }
                                case 'group': {
                                    var v_data = {
                                        forwardMessageCode: p_item.messageCode,
                                        groupCode: v_code,
                                        messageType: 0
                                    };

                                    chatSendGroupMessage(v_data);

                                    break;
                                }
                            }

                            p_modal.remove();
                        }.bind(v_buttonOk, v_modal, p_item)
                    );
                }
            }.bind(v_actionShare, v_item)
        );

        v_contextMenu.appendChild(v_actionShare);

        if(p_message.type == 1 || p_message.type == 5) {//Plain text or Mention
            if(p_message.user.code == v_user_id) {//Same user
                var v_actionEdit = document.createElement('div');
                v_actionEdit.classList.add('context_menu_item');
                v_actionEdit.classList.add('context_menu_item_inline');
                v_actionEdit.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_edit.png" class="context_menu_item_img" />';
                v_actionEdit.title = 'Edit Message';
                v_actionEdit.groupCode = p_groupCode;

                v_actionEdit.addEventListener(
                    'click',
                    function(p_message, p_event) {
                        var v_dropdownMenu = document.querySelectorAll('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null && v_dropdownMenu.length > 0) {
                            for(var i = 0; i < v_dropdownMenu.length; i++) {
                                v_dropdownMenu[i].remove();
                            }
                        }

                        var v_html =
                            '<div style="margin-bottom: 20px;">' +
                            '    <div id="div_chat_message_edit_message">' +
                            '    </div>' +
                            '</div>' +
                            '<div style="margin-top: 10px; text-align: center;">' +
                            '    <button id="button_modal_cancel">Cancel</button>' +
                            '    <button id="button_modal_ok" style="margin-left: 5px;">Ok</button>' +
                            '</div>';

                        var v_modal = openModal(v_html);

                        document.querySelector('.modal_content').style.width = '70vw';

                        var v_editor = $('#div_chat_message_edit_message').emojioneArea({
                            pickerPosition: 'top',
                            filtersPosition: 'top',
                            tonesStyle: 'bullet',
                            saveEmojisAs: 'shortname',
                            useInternalCDN: false
                        });

                        window.addEventListener(
                            'blur',
                            function(p_editor, p_event) {
                                if(p_editor != null) {
                                    p_editor.altPressed = false;
                                    p_editor.shiftPressed = false;
                                }
                            }.bind(window, v_editor[0].emojioneArea)
                        );

                        if(p_message.type == 1) { //Plain text
                            v_editor[0].emojioneArea.setText(p_message.rawContent);
                        }
                        else if(p_message.type == 5) { //Mention
                            var v_content = p_message.rawContent.substring(0, p_message.rawContent.indexOf('#start_mentioned_message#'));
                            v_editor[0].emojioneArea.setText(v_content);
                        }

                        v_editor[0].nextSibling.childNodes[0].focus();

                        var v_buttonCancel = document.getElementById('button_modal_cancel');

                        v_buttonCancel.addEventListener(
                            'click',
                            function(p_modal, p_event) {
                                p_modal.remove();

                                var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                                if(v_dropdownMenu != null) {
                                    v_dropdownMenu.remove();
                                }
                            }.bind(v_buttonCancel, v_modal)
                        );

                        var v_buttonOk = document.getElementById('button_modal_ok');
                        v_buttonOk.messageCode = p_message.code;
                        v_buttonOk.groupCode = this.groupCode;

                        v_buttonOk.addEventListener(
                            'click',
                            function(p_editor, p_modal, p_message, p_event) {
                                var v_rawContent = p_editor[0].emojioneArea.getText();
                                var v_content = p_editor[0].emojioneArea.editor[0].innerHTML;

                                if(p_message.type == 5) { //Mention
                                    v_rawContent += p_message.rawContent.substring(p_message.rawContent.indexOf('#start_mentioned_message#'), p_message.rawContent.length);
                                    v_content += p_message.rawContent.substring(p_message.rawContent.indexOf('#start_mentioned_message#'), p_message.rawContent.length);
                                }

                                var v_data = {
                                    messageCode: this.messageCode,
                                    groupCode: this.groupCode,
                                    messageContent: v_content,
                                    messageRawContent: v_rawContent
                                };

                                chatUpdateGroupMessage(v_data);

                                p_modal.remove();

                                var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                                if(v_dropdownMenu != null) {
                                    v_dropdownMenu.remove();
                                }
                            }.bind(v_buttonOk, v_editor, v_modal, p_message)
                        );

                        v_editor[0].emojioneArea.altPressed = false;
                        v_editor[0].emojioneArea.shiftPressed = false;
                        v_editor[0].selectingEmoji = false;

                        v_editor[0].emojioneArea.on(
                            'keydown',
                            function(p_editor, p_event) {
                                var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                                if(v_dropdownMenu != null) {
                                    this.selectingEmoji = v_dropdownMenu.style.display == 'block';
                                }
                                else {
                                    this.selectingEmoji = false;
                                }

                                if(p_event.keyCode == 18) { //Alt
                                    this.altPressed = true;
                                }
                                else if(p_event.keyCode == 16) { //Shift
                                    this.shiftPressed = true;
                                }

                                if(p_event.keyCode == 13) { //Enter
                                    p_event.preventDefault();

                                    if(this.altPressed || this.shiftPressed) {
                                        var v_selection = window.getSelection();
                                        var v_range = v_selection.getRangeAt(0);
                                        var v_div = document.createElement('div');
                                        var v_br = document.createElement('br');
                                        v_div.appendChild(v_br);
                                        v_range.deleteContents();
                                        v_range.insertNode(v_div);
                                        v_range.setStartAfter(v_div);
                                        v_range.setEndAfter(v_div);
                                        v_range.collapse(false);
                                        v_selection.removeAllRanges();
                                        v_selection.addRange(v_range);
                                    }
                                }
                            }.bind(v_editor[0].emojioneArea)
                        );

                        v_editor[0].emojioneArea.on(
                            'keyup',
                            function(p_buttonOk, p_editor, p_event) {
                                if(p_event.keyCode == 18) { //Alt
                                    this.altPressed = false;
                                }
                                else if(p_event.keyCode == 16) { //Shift
                                    this.shiftPressed = false;
                                }

                                if(p_event.keyCode == 13 && !this.selectingEmoji && !this.altPressed && !this.shiftPressed) { //Enter and not selecting emoticons or inserting new lines
                                    p_event.preventDefault();

                                    if(p_editor[0].innerHTML.length > 0) {
                                        p_buttonOk.click();
                                    }
                                }
                            }.bind(v_editor[0].emojioneArea, v_buttonOk)
                        );
                    }.bind(v_actionEdit, p_message)
                );

                v_contextMenu.appendChild(v_actionEdit);
            }
        }

        if(p_message.type == 2 || p_message.type == 4) {//Pasted image or Attachment
            var v_actionDownload = document.createElement('div');
            v_actionDownload.classList.add('context_menu_item');
            v_actionDownload.classList.add('context_menu_item_inline');
            v_actionDownload.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_download.png" class="context_menu_item_img" />';
            v_actionDownload.title = 'Download File';

            v_actionDownload.addEventListener(
                'click',
                function(p_message, p_event) {
                    var v_link = document.createElement('a');
                    v_link.href = gv_chatAttachmentPath + '/' + p_message.code;
                    v_link.download = p_message.attachmentName;
                    v_link.click();
                    v_link.remove();
                }.bind(v_actionDownload, p_message)
            );

            v_contextMenu.appendChild(v_actionDownload);
        }

        if(p_message.type == 3) {
            var v_html =
                '<div style="text-align: center; font-family: lato-bold;">' +
                '    <input id="input_snippet_title" type="text" style="display: inline-block !important; width: 40%;" placeholder="Snippet Title" class="form-control" />' +
                '    <select id="select_snippet_mode" style="display: inline-block !important; width: 40%; margin-left: 5%;" class="form-control">' +
                '        <option value="plain_text" selected="selected">Plain Text</option>' +
                '        <option value="abap">ABAP</option>' +
                '        <option value="abc">ABC</option>' +
                '        <option value="actionscript">ActionScript</option>' +
                '        <option value="ada">Ada</option>' +
                '        <option value="apache_conf">ApachConf</option>' +
                '        <option value="applescript">AppleScript</option>' +
                '        <option value="asciidoc">AsciiDoc</option>' +
                '        <option value="assembly_x86">Assembly x86</option>' +
                '        <option value="autohotkey">AutoHotkey</option>' +
                '        <option value="batchfile">Batch file</option>' +
                '        <option value="behaviour">Behaviour</option>' +
                '        <option value="bro">Bro</option>' +
                '        <option value="c_cpp">C</option>' +
                '        <option value="c_cpp">C++</option>' +
                '        <option value="cirru">Cirru</option>' +
                '        <option value="clojure">Clojure</option>' +
                '        <option value="cobol">COBOL</option>' +
                '        <option value="coffee">CoffeeScript</option>' +
                '        <option value="coldfusion">ColdFusion</option>' +
                '        <option value="csharp">C#</option>' +
                '        <option value="csound">CSound</option>' +
                '        <option value="css">CSS</option>' +
                '        <option value="curly">curly</option>' +
                '        <option value="d">D</option>' +
                '        <option value="dart">Dart</option>' +
                '        <option value="diff">Diff</option>' +
                '        <option value="django">Django</option>' +
                '        <option value="dockerfile">Dockerfile</option>' +
                '        <option value="dot">DOT</option>' +
                '        <option value="drools">Drools</option>' +
                '        <option value="eiffel">Eiffel</option>' +
                '        <option value="ejs">EJS</option>' +
                '        <option value="elixir">Elixir</option>' +
                '        <option value="elm">Elm</option>' +
                '        <option value="erlang">Erlang</option>' +
                '        <option value="forth">Forth</option>' +
                '        <option value="fortran">Fortran</option>' +
                '        <option value="ftl">FTL</option>' +
                '        <option value="gcode">G-code</option>' +
                '        <option value="gherkin">Gherkin</option>' +
                '        <option value="gitignore">GitIgnore</option>' +
                '        <option value="glsl">GLSL</option>' +
                '        <option value="gobstones">Gobstones</option>' +
                '        <option value="golang">GoLang</option>' +
                '        <option value="graphqlschema">GraphQLSchema</option>' +
                '        <option value="groovy">Groovy</option>' +
                '        <option value="haml">Haml</option>' +
                '        <option value="handlebars">Handlebars</option>' +
                '        <option value="haskell">Haskell</option>' +
                '        <option value="haxe">Haxe</option>' +
                '        <option value="hjson">Hjson</option>' +
                '        <option value="html">HTML</option>' +
                '        <option value="ini">INI</option>' +
                '        <option value="io">Io</option>' +
                '        <option value="jack">Jack</option>' +
                '        <option value="jade">Jade</option>' +
                '        <option value="java">Java</option>' +
                '        <option value="javascript">JavaScript</option>' +
                '        <option value="json">JSON</option>' +
                '        <option value="jsoniq">JSONiq</option>' +
                '        <option value="jsp">JSP</option>' +
                '        <option value="jssm">JSSM</option>' +
                '        <option value="jsx">JSX</option>' +
                '        <option value="julia">Julia</option>' +
                '        <option value="kotlin">Kotlin</option>' +
                '        <option value="latex">LaTeX</option>' +
                '        <option value="less">Less</option>' +
                '        <option value="liquid">Liquid</option>' +
                '        <option value="lisp">Lisp</option>' +
                '        <option value="livescript">LiveScript</option>' +
                '        <option value="logiql">LogiQL</option>' +
                '        <option value="lsl">LSL</option>' +
                '        <option value="lua">Lua</option>' +
                '        <option value="luapage">Lua Page</option>' +
                '        <option value="lucene">Lucene</option>' +
                '        <option value="makefile">Makefile</option>' +
                '        <option value="markdown">Markdown</option>' +
                '        <option value="mask">MASK</option>' +
                '        <option value="matlab">MATLAB</option>' +
                '        <option value="maze">Maze</option>' +
                '        <option value="mel">MEL</option>' +
                '        <option value="mushcode">MUSHCode</option>' +
                '        <option value="mysql">MySQL</option>' +
                '        <option value="nix">Nix</option>' +
                '        <option value="nsis">NSIS</option>' +
                '        <option value="objectivec">Objective-C</option>' +
                '        <option value="ocaml">OCaml</option>' +
                '        <option value="pascal">Pascal</option>' +
                '        <option value="nsis">NSIS</option>' +
                '        <option value="perl">Perl</option>' +
                '        <option value="pgsql">pgSQL</option>' +
                '        <option value="php">PHP</option>' +
                '        <option value="pig">Pig</option>' +
                '        <option value="powershell">PowerShell</option>' +
                '        <option value="praat">Praat</option>' +
                '        <option value="prolog">Prolog</option>' +
                '        <option value="protobuf">protobuf</option>' +
                '        <option value="python">Python</option>' +
                '        <option value="r">R</option>' +
                '        <option value="razor">Razor</option>' +
                '        <option value="rdoc">RDoC</option>' +
                '        <option value="red">Red</option>' +
                '        <option value="rhtml">RHTML</option>' +
                '        <option value="rst">reStructuredText</option>' +
                '        <option value="ruby">Ruby</option>' +
                '        <option value="rust">Rust</option>' +
                '        <option value="sass">Sass</option>' +
                '        <option value="scad">SCAD</option>' +
                '        <option value="scala">Scala</option>' +
                '        <option value="scheme">Scheme</option>' +
                '        <option value="scss">Scss</option>' +
                '        <option value="sh">Shell script</option>' +
                '        <option value="sjs">SJS</option>' +
                '        <option value="smarty">Smarty</option>' +
                '        <option value="snippet">Snippet</option>' +
                '        <option value="soy_template">Soy Template</option>' +
                '        <option value="sparql">SPARQL</option>' +
                '        <option value="sql">SQL</option>' +
                '        <option value="sqlserver">SQL Server</option>' +
                '        <option value="stylus">Stylus</option>' +
                '        <option value="svg">SVG</option>' +
                '        <option value="swift">Swift</option>' +
                '        <option value="tcl">Tcl</option>' +
                '        <option value="tex">TeX</option>' +
                '        <option value="toml">TOML</option>' +
                '        <option value="tsx">TSX</option>' +
                '        <option value="turtle">Turtle</option>' +
                '        <option value="twig">Twig</option>' +
                '        <option value="typescript">TypeScript</option>' +
                '        <option value="vala">Vala</option>' +
                '        <option value="vbscript">VBScript</option>' +
                '        <option value="velocity">Velocity</option>' +
                '        <option value="verilog">Verilog</option>' +
                '        <option value="vhdl">VHDL</option>' +
                '        <option value="wollok">Wollok</option>' +
                '        <option value="xml">XML</option>' +
                '        <option value="xquery">XQuery</option>' +
                '        <option value="yaml">YAML</option>' +
                '    </select>' +
                '</div>' +
                '<div id="div_snippet_editor" style="margin-top: 20px; margin-bottom: 20px; height: calc(70vh - 100px); width: 70vw; border: 2px solid rgba(0, 0, 0, 0.5); border-radius: 8px;">' +
                '</div>' +
                '<div style="margin-top: 10px; text-align: center;">' +
                '    <button id="button_modal_cancel">Cancel</button>' +
                '    <button id="button_modal_ok" style="margin-left: 5px;">Ok</button>' +
                '</div>';

            if(p_message.user.code == v_user_id) {//Same user
                var v_actionEdit = document.createElement('div');
                v_actionEdit.classList.add('context_menu_item');
                v_actionEdit.classList.add('context_menu_item_inline');
                v_actionEdit.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_edit.png" class="context_menu_item_img" />';
                v_actionEdit.title = 'Edit Snippet';
                v_actionEdit.groupCode = p_groupCode;

                v_actionEdit.addEventListener(
                    'click',
                    function(p_message, p_html, p_event) {
                        var v_modal = openModal(p_html);

                        document.getElementById('input_snippet_title').value = p_message.title;

                        var v_editor = ace.edit('div_snippet_editor');
                        v_editor.getSession().setMode('ace/mode/' + p_message.snippetMode);
                        v_editor.setTheme("ace/theme/" + v_editor_theme);
                        v_editor.getSession().setUseSoftTabs(true);
                        v_editor.setValue(p_message.content);
                        v_editor.clearSelection();
                        v_editor.focus();

                        var v_selectSnippetMode = document.getElementById('select_snippet_mode');
                        v_selectSnippetMode.value = p_message.snippetMode;

                        v_selectSnippetMode.addEventListener(
                            'change',
                            function(p_editor, p_event) {
                                p_editor.getSession().setMode('ace/mode/' + this.value);
                            }.bind(v_selectSnippetMode, v_editor)
                        );

                        var v_buttonCancel = document.getElementById('button_modal_cancel');

                        v_buttonCancel.addEventListener(
                            'click',
                            function(p_modal, p_event) {
                                p_modal.remove();
                            }.bind(v_buttonCancel, v_modal)
                        );

                        var v_buttonOk = document.getElementById('button_modal_ok');
                        v_buttonOk.messageCode = p_message.code;
                        v_buttonOk.groupCode = this.groupCode;

                        v_buttonOk.addEventListener(
                            'click',
                            function(p_editor, p_modal, p_event) {
                                var v_data = {
                                    snippetTitle: document.getElementById('input_snippet_title').value,
                                    snippetContent: p_editor.getValue(),
                                    snippetMode: document.getElementById('select_snippet_mode').value,
                                    messageCode: this.messageCode,
                                    groupCode: this.groupCode
                                };

                                chatUpdateGroupSnippetMessage(v_data);

                                p_modal.remove();
                            }.bind(v_buttonOk, v_editor, v_modal)
                        );
                    }.bind(v_actionEdit, p_message, v_html)
                );

                v_contextMenu.appendChild(v_actionEdit);

                var v_snippetContainerImg = v_messageContent.querySelector('.div_chat_message_snippet_container > img')

                if(v_snippetContainerImg != null) {
                    v_snippetContainerImg.addEventListener(
                        'click',
                        function(p_actionEdit, p_event) {
                            p_actionEdit.click();
                        }.bind(v_snippetContainerImg, v_actionEdit)
                    );
                }
            }
            else {
                var v_actionView = document.createElement('div');
                v_actionView.classList.add('context_menu_item');
                v_actionView.classList.add('context_menu_item_inline');
                v_actionView.innerHTML = '<img src="/static/OmniDB_app/images/icons/action_chat_view.png" class="context_menu_item_img" />';
                v_actionView.title = 'View Snippet';

                v_actionView.addEventListener(
                    'click',
                    function(p_message, p_html, p_event) {
                        var v_modal = openModal(p_html);

                        document.getElementById('input_snippet_title').value = p_message.title;
                        document.getElementById('input_snippet_title').disabled = true;

                        var v_editor = ace.edit('div_snippet_editor');
                        v_editor.getSession().setMode('ace/mode/' + p_message.snippetMode);
                        v_editor.setTheme("ace/theme/" + v_editor_theme);
                        v_editor.getSession().setUseSoftTabs(true);
                        v_editor.setValue(p_message.content);
                        v_editor.clearSelection();
                        v_editor.focus();
                        v_editor.setReadOnly(true);

                        var v_selectSnippetMode = document.getElementById('select_snippet_mode');
                        v_selectSnippetMode.value = p_message.snippetMode;
                        v_selectSnippetMode.disabled = true;

                        var v_buttonCancel = document.getElementById('button_modal_cancel');
                        v_buttonCancel.style.display = 'none';

                        var v_buttonOk = document.getElementById('button_modal_ok');
                        v_buttonOk.messageCode = p_message.code;

                        v_buttonOk.addEventListener(
                            'click',
                            function(p_modal, p_event) {
                                p_modal.remove();
                            }.bind(v_buttonOk, v_modal)
                        );
                    }.bind(v_actionView, p_message, v_html)
                );

                v_contextMenu.appendChild(v_actionView);

                var v_snippetContainerImg = v_messageContent.querySelector('.div_chat_message_snippet_container > img')

                if(v_snippetContainerImg != null) {
                    v_snippetContainerImg.addEventListener(
                        'click',
                        function(p_actionView, p_event) {
                            p_actionView.click();
                        }.bind(v_snippetContainerImg, v_actionView)
                    );
                }
            }
        }

        v_item.appendChild(v_contextMenu);

        if(p_withHeader) {
            var v_time = p_message.createdAt.substring(11, 16);

            //Prepend message header
            var v_messageHeader = document.createElement('div');
            v_messageHeader.innerHTML = p_message.user.login + ' <span class="span_chat_right_item_header">' + v_time + '</span>';
            v_messageHeader.classList.add('div_chat_right_left_item_header');
            v_item.firstChild.insertBefore(v_messageHeader, v_item.firstChild.firstChild);

            //Prepend user icon
            var v_userImg = document.createElement('img');
            v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
            v_userImg.classList.add('img_chat_user');
            v_item.insertBefore(v_userImg, v_item.firstChild);

            v_item.childNodes[1].classList.remove('div_chat_right_left_item_body_padding');
        }

        return v_item;
    }.bind(v_chatPopUp.tag.getRenderedGroupMessage, v_chatPopUp);

    v_chatPopUp.tag.renderGroup = function(p_chatPopUp, p_groupCode, p_renderAtMessage, p_preventContextScroll) {
        if(p_chatPopUp.tag.renderedType == 1) { //Channel
            /*var v_data = {
                channelCode: p_chatPopUp.tag.renderedChannel,
                userCode: parseInt(v_user_id),
                userWriting: false
            };

            chatSetChannelUserWriting(v_data);*/

            var v_channelContext = p_chatPopUp.tag.contextList.getContextByChannelCode(p_chatPopUp.tag.renderedChannel);

            if(v_channelContext != null) {
                v_channelContext.text = p_chatPopUp.tag.renderedEditor.getText();
            }
        }
        else if(p_chatPopUp.tag.renderedType == 2) { //Group
            /*var v_data = {
                groupCode: p_chatPopUp.tag.renderedGroup,
                userCode: parseInt(v_user_id),
                userWriting: false
            };

            chatSetGroupUserWriting(v_data);*/

            var v_groupContext = p_chatPopUp.tag.contextList.getContextByGroupCode(p_chatPopUp.tag.renderedGroup);

            if(v_groupContext != null) {
                v_groupContext.text = p_chatPopUp.tag.renderedEditor.getText();
            }
        }

        //Change active element
        var v_activeGroupElement = document.querySelector('.div_chat_left_content > .div_chat_left_content_item_active');

        if(v_activeGroupElement != null) {
            v_activeGroupElement.classList.remove('div_chat_left_content_item_active');
        }

        var v_group = p_chatPopUp.tag.groupList.getGroupByCode(p_groupCode);

        if(v_group != null) {
            var v_sameGroup = false;
            var v_onLastMessage = false;
            var v_firstVisibleMessageCode = null;
            var v_firstUnreadMessageCode = null;

            if(p_chatPopUp.tag.renderedType == 2 && v_chatPopUp.tag.renderedGroup == v_group.code) {//If the rendered type is group and this group are the rendered one.
                v_sameGroup = true;
                var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

                if((v_divChatRightContent.offsetHeight + v_divChatRightContent.scrollTop + 1) >= v_divChatRightContent.scrollHeight) {//If scroll was at max allowed
                    v_onLastMessage = true;
                }
                else {
                    for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                        if(v_divChatRightContent.childNodes[i].offsetTop >= v_divChatRightContent.scrollTop) {
                            v_firstVisibleMessageCode = v_divChatRightContent.childNodes[i].messageCode;
                            break;
                        }
                    }
                }
            }

            var v_divChatRight = document.getElementById('div_chat_right_left');
            var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

            if(!v_sameGroup) {
                //Remove drop down from last render, if any
		        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

		        if(v_dropdownMenu != null) {
		            v_dropdownMenu.remove();
		        }

	            p_chatPopUp.tag.renderedType = 2; //Group popup
	            p_chatPopUp.tag.renderedGroup = v_group.code;

	            v_divChatRight.type = 2; //Group container
	            v_divChatRight.groupCode = v_group.code;

                //Recover last header items, if any
                var v_oldRightHeader = document.getElementById('div_chat_right_left_header');
                var v_oldRightHeaderChildren = [];

                if(v_oldRightHeader != null) {
                    for(var i = 0; i < v_oldRightHeader.childNodes.length; i++) {
                        v_oldRightHeaderChildren.push(v_oldRightHeader.childNodes[i]);
                    }
                }

	            v_divChatRight.innerHTML = '';

                var v_rightPreHeader = document.createElement('div');
                v_rightPreHeader.id = 'div_chat_right_left_pre_header';

                var v_divContainer = document.createElement('div');
                v_divContainer.id = 'div_chat_right_left_pre_header_name_container';
                v_rightPreHeader.appendChild(v_divContainer);

                var v_imgRightPreHeader = document.createElement('img');
                v_imgRightPreHeader.id = 'img_chat_right_pre_header_icon';

                var v_user = null;

                for(var i = 0; i < v_group.userList.length; i++) {
                    if(v_group.userList[i].code != v_user_id) {
                        v_user = v_group.userList[i];

                        if(v_chatPopUp.tag.onlineUserCodeList.indexOf(v_group.userList[i].code) != -1) {
                            v_imgRightPreHeader.src = '/static/OmniDB_app/images/icons/status_chat_online.png';
                        }
                        else {
                            v_imgRightPreHeader.src = '/static/OmniDB_app/images/icons/status_chat_offline.png';
                        }

                        break;
                    }
                }

                v_divContainer.appendChild(v_imgRightPreHeader);

                var v_spanRightPreHeader = document.createElement('span');
                v_spanRightPreHeader.id = 'span_chat_right_pre_header_name';
                v_spanRightPreHeader.innerHTML = v_user.login;
                v_divContainer.appendChild(v_spanRightPreHeader);

                v_imgRightPreHeader.userCode = v_user.code;
                v_divContainer.title = v_user.name;

                var v_inputRightPreHeader = document.createElement('input');
                v_inputRightPreHeader.type = 'text';
                v_inputRightPreHeader.id = 'input_chat_right_pre_header_search';
                v_inputRightPreHeader.classList.add('form-control');
                v_inputRightPreHeader.placeholder = 'Search...';
                v_inputRightPreHeader.title = 'Type and, at end, press enter to start searching.'

                v_inputRightPreHeader.addEventListener(
                    'keydown',
                    function(p_event) {
                        if(p_event.keyCode == 13) { //Enter
                            var v_value = this.value.toLowerCase();

                            if(v_value != '') {
                                this.value = '';

                                var v_divChatRightRight = document.getElementById('div_chat_right_right');
                                v_divChatRightRight.classList.remove('display_hidden');

                                var v_divChatRightRightContent = document.getElementById('div_chat_right_right_content');
                                v_divChatRightRightContent.removeAttribute('style');
                                v_divChatRightRightContent.innerHTML = '<div class="gif_loading"></div>';
                                v_divChatRightRightContent.style.justifyContent = 'center';
                                v_divChatRightRightContent.style.alignItems = 'center';

                                var v_data = {
                                    textPattern: v_value
                                };

                                chatSearchOldMessages(v_data);
                            }
                        }
                    }
                );


                v_rightPreHeader.appendChild(v_inputRightPreHeader);

                v_divChatRight.appendChild(v_rightPreHeader);

                var v_rightHeader = document.createElement('div');
                v_rightHeader.id = 'div_chat_right_left_header';
                v_divChatRight.appendChild(v_rightHeader);

                //Observer used to rightly format header
                var v_rightHeaderObserver = new MutationObserver(
                    function(p_rightHeader, p_mutationList, p_this) {
                        if(p_rightHeader.childNodes.length == 0) {
                            p_rightHeader.style.padding = '';
                            p_rightHeader.style.borderBottom = '';
                        }
                        else {
                            p_rightHeader.style.padding = '10px';
                            p_rightHeader.style.borderBottom = '1px solid rgba(0, 0, 0, 0.5)';
                        }
                    }.bind(v_rightHeaderObserver, v_rightHeader)
                );

                v_rightHeaderObserver.observe(
                    v_rightHeader,
                    {
                        childList: true
                    }
                );

                //Restore last header items, if any
                if(v_oldRightHeaderChildren.length > 0) {
                    for(var i = 0; i < v_oldRightHeaderChildren.length; i++) {
                        v_rightHeader.appendChild(v_oldRightHeaderChildren[i]);
                    }
                }

	            var v_rightContent = document.createElement('div');
                v_divChatRightContent = v_rightContent;
	            v_rightContent.id = 'div_chat_right_left_content';

                //Controls when to recover older messages from server
                v_rightContent.addEventListener(
                    'scroll',
                    function(p_chatPopUp, p_event) {
                        var v_groupContext = p_chatPopUp.tag.contextList.getContextByGroupCode(this.parentElement.groupCode);

                        if(v_groupContext != null) {
                            v_groupContext.scrollTop = this.scrollTop;
                        }

                        var v_group = p_chatPopUp.tag.groupList.getGroupByCode(this.parentElement.groupCode);

                        if(v_group != null) {
	                        if(this.scrollTop == 0) {
	                            var v_data = {
	                                groupCode: v_group.code,
	                                offset: v_group.messageList.length,
                                    fromMessageCode: null
	                            };

	                            chatRetrieveGroupHistory(v_data);
	                        }
	                        else {
	                            //Mark messages as read, if it's the case
					            if((this.offsetHeight + this.scrollTop + 1) >= this.scrollHeight) {
                                    var v_messageCodeList = [];

                                    for(var i = 0; i < v_group.messageList.length; i++) {
                                        if(!v_group.messageList[i].viewed) {
                                            v_messageCodeList.push(v_group.messageList[i].code);
                                        }
                                    }

                                    if(v_messageCodeList.length > 0) {
                                        var v_data = {
                                            groupCode: v_group.code,
                                            messageCodeList: v_messageCodeList
                                        };

                                        chatMarkGroupMessagesAsRead(v_data);
                                    }
                                }
                            }
                        }
                    }.bind(v_rightContent, p_chatPopUp)
                );

	            v_divChatRight.appendChild(v_rightContent);

                p_chatPopUp.tag.renderedContent = v_rightContent;

	            var v_rightFooter = document.createElement('div');
	            v_rightFooter.id = 'div_chat_right_left_footer';
	            v_divChatRight.appendChild(v_rightFooter);

	            var v_rightFooterLeft = document.createElement('div');
	            v_rightFooterLeft.id = 'div_chat_right_left_footer_left';
	            v_rightFooter.appendChild(v_rightFooterLeft);

	            var v_buttonChatRightFooterLeft = document.createElement('button');
	            v_buttonChatRightFooterLeft.classList.add('button_chat_right_footer_left');
	            v_buttonChatRightFooterLeft.innerHTML = '+';
	            v_rightFooterLeft.appendChild(v_buttonChatRightFooterLeft);

                //Used for uploading snippets and files
	            v_buttonChatRightFooterLeft.addEventListener(
	                'click',
	                function(p_chatPopUp, p_event) {
	                    var v_div = document.createElement('div');
                        v_div.classList.add('div_chat_right_left_footer_left_options');
                        v_div.tabIndex = '0';

                        v_div.addEventListener(
                            'blur',
                            function(p_event) {
                                this.remove();
                            }
                        );

                        var v_snippetItem = document.createElement('div');
                        v_snippetItem.classList.add('div_chat_right_left_footer_left_options_item');
                        v_snippetItem.innerHTML = 'Create Snippet';

                        v_snippetItem.addEventListener(
                            'click',
                            function(p_chatPopUp, p_event) {
                                this.parentElement.blur();

                                var v_html =
                                    '<div style="text-align: center; font-family: lato-bold;">' +
                                    '    <input id="input_snippet_title" type="text" style="display: inline-block !important; width: 40%;" placeholder="Snippet Title" class="form-control" />' +
                                    '    <select id="select_snippet_mode" style="display: inline-block !important; width: 40%; margin-left: 5%;" class="form-control">' +
                                    '        <option value="plain_text" selected="selected">Plain Text</option>' +
                                    '        <option value="abap">ABAP</option>' +
                                    '        <option value="abc">ABC</option>' +
                                    '        <option value="actionscript">ActionScript</option>' +
                                    '        <option value="ada">Ada</option>' +
                                    '        <option value="apache_conf">ApachConf</option>' +
                                    '        <option value="applescript">AppleScript</option>' +
                                    '        <option value="asciidoc">AsciiDoc</option>' +
                                    '        <option value="assembly_x86">Assembly x86</option>' +
                                    '        <option value="autohotkey">AutoHotkey</option>' +
                                    '        <option value="batchfile">Batch file</option>' +
                                    '        <option value="behaviour">Behaviour</option>' +
                                    '        <option value="bro">Bro</option>' +
                                    '        <option value="c_cpp">C</option>' +
                                    '        <option value="c_cpp">C++</option>' +
                                    '        <option value="cirru">Cirru</option>' +
                                    '        <option value="clojure">Clojure</option>' +
                                    '        <option value="cobol">COBOL</option>' +
                                    '        <option value="coffee">CoffeeScript</option>' +
                                    '        <option value="coldfusion">ColdFusion</option>' +
                                    '        <option value="csharp">C#</option>' +
                                    '        <option value="csound">CSound</option>' +
                                    '        <option value="css">CSS</option>' +
                                    '        <option value="curly">curly</option>' +
                                    '        <option value="d">D</option>' +
                                    '        <option value="dart">Dart</option>' +
                                    '        <option value="diff">Diff</option>' +
                                    '        <option value="django">Django</option>' +
                                    '        <option value="dockerfile">Dockerfile</option>' +
                                    '        <option value="dot">DOT</option>' +
                                    '        <option value="drools">Drools</option>' +
                                    '        <option value="eiffel">Eiffel</option>' +
                                    '        <option value="ejs">EJS</option>' +
                                    '        <option value="elixir">Elixir</option>' +
                                    '        <option value="elm">Elm</option>' +
                                    '        <option value="erlang">Erlang</option>' +
                                    '        <option value="forth">Forth</option>' +
                                    '        <option value="fortran">Fortran</option>' +
                                    '        <option value="ftl">FTL</option>' +
                                    '        <option value="gcode">G-code</option>' +
                                    '        <option value="gherkin">Gherkin</option>' +
                                    '        <option value="gitignore">GitIgnore</option>' +
                                    '        <option value="glsl">GLSL</option>' +
                                    '        <option value="gobstones">Gobstones</option>' +
                                    '        <option value="golang">GoLang</option>' +
                                    '        <option value="graphqlschema">GraphQLSchema</option>' +
                                    '        <option value="groovy">Groovy</option>' +
                                    '        <option value="haml">Haml</option>' +
                                    '        <option value="handlebars">Handlebars</option>' +
                                    '        <option value="haskell">Haskell</option>' +
                                    '        <option value="haxe">Haxe</option>' +
                                    '        <option value="hjson">Hjson</option>' +
                                    '        <option value="html">HTML</option>' +
                                    '        <option value="ini">INI</option>' +
                                    '        <option value="io">Io</option>' +
                                    '        <option value="jack">Jack</option>' +
                                    '        <option value="jade">Jade</option>' +
                                    '        <option value="java">Java</option>' +
                                    '        <option value="javascript">JavaScript</option>' +
                                    '        <option value="json">JSON</option>' +
                                    '        <option value="jsoniq">JSONiq</option>' +
                                    '        <option value="jsp">JSP</option>' +
                                    '        <option value="jssm">JSSM</option>' +
                                    '        <option value="jsx">JSX</option>' +
                                    '        <option value="julia">Julia</option>' +
                                    '        <option value="kotlin">Kotlin</option>' +
                                    '        <option value="latex">LaTeX</option>' +
                                    '        <option value="less">Less</option>' +
                                    '        <option value="liquid">Liquid</option>' +
                                    '        <option value="lisp">Lisp</option>' +
                                    '        <option value="livescript">LiveScript</option>' +
                                    '        <option value="logiql">LogiQL</option>' +
                                    '        <option value="lsl">LSL</option>' +
                                    '        <option value="lua">Lua</option>' +
                                    '        <option value="luapage">Lua Page</option>' +
                                    '        <option value="lucene">Lucene</option>' +
                                    '        <option value="makefile">Makefile</option>' +
                                    '        <option value="markdown">Markdown</option>' +
                                    '        <option value="mask">MASK</option>' +
                                    '        <option value="matlab">MATLAB</option>' +
                                    '        <option value="maze">Maze</option>' +
                                    '        <option value="mel">MEL</option>' +
                                    '        <option value="mushcode">MUSHCode</option>' +
                                    '        <option value="mysql">MySQL</option>' +
                                    '        <option value="nix">Nix</option>' +
                                    '        <option value="nsis">NSIS</option>' +
                                    '        <option value="objectivec">Objective-C</option>' +
                                    '        <option value="ocaml">OCaml</option>' +
                                    '        <option value="pascal">Pascal</option>' +
                                    '        <option value="nsis">NSIS</option>' +
                                    '        <option value="perl">Perl</option>' +
                                    '        <option value="pgsql">pgSQL</option>' +
                                    '        <option value="php">PHP</option>' +
                                    '        <option value="pig">Pig</option>' +
                                    '        <option value="powershell">PowerShell</option>' +
                                    '        <option value="praat">Praat</option>' +
                                    '        <option value="prolog">Prolog</option>' +
                                    '        <option value="protobuf">protobuf</option>' +
                                    '        <option value="python">Python</option>' +
                                    '        <option value="r">R</option>' +
                                    '        <option value="razor">Razor</option>' +
                                    '        <option value="rdoc">RDoC</option>' +
                                    '        <option value="red">Red</option>' +
                                    '        <option value="rhtml">RHTML</option>' +
                                    '        <option value="rst">reStructuredText</option>' +
                                    '        <option value="ruby">Ruby</option>' +
                                    '        <option value="rust">Rust</option>' +
                                    '        <option value="sass">Sass</option>' +
                                    '        <option value="scad">SCAD</option>' +
                                    '        <option value="scala">Scala</option>' +
                                    '        <option value="scheme">Scheme</option>' +
                                    '        <option value="scss">Scss</option>' +
                                    '        <option value="sh">Shell script</option>' +
                                    '        <option value="sjs">SJS</option>' +
                                    '        <option value="smarty">Smarty</option>' +
                                    '        <option value="snippet">Snippet</option>' +
                                    '        <option value="soy_template">Soy Template</option>' +
                                    '        <option value="sparql">SPARQL</option>' +
                                    '        <option value="sql">SQL</option>' +
                                    '        <option value="sqlserver">SQL Server</option>' +
                                    '        <option value="stylus">Stylus</option>' +
                                    '        <option value="svg">SVG</option>' +
                                    '        <option value="swift">Swift</option>' +
                                    '        <option value="tcl">Tcl</option>' +
                                    '        <option value="tex">TeX</option>' +
                                    '        <option value="toml">TOML</option>' +
                                    '        <option value="tsx">TSX</option>' +
                                    '        <option value="turtle">Turtle</option>' +
                                    '        <option value="twig">Twig</option>' +
                                    '        <option value="typescript">TypeScript</option>' +
                                    '        <option value="vala">Vala</option>' +
                                    '        <option value="vbscript">VBScript</option>' +
                                    '        <option value="velocity">Velocity</option>' +
                                    '        <option value="verilog">Verilog</option>' +
                                    '        <option value="vhdl">VHDL</option>' +
                                    '        <option value="wollok">Wollok</option>' +
                                    '        <option value="xml">XML</option>' +
                                    '        <option value="xquery">XQuery</option>' +
                                    '        <option value="yaml">YAML</option>' +
                                    '    </select>' +
                                    '</div>' +
                                    '<div id="div_snippet_editor" style="margin-top: 20px; margin-bottom: 20px; height: calc(70vh - 100px); width: 70vw; border: 2px solid rgba(0, 0, 0, 0.5); border-radius: 8px;">' +
                                    '</div>' +
                                    '<div style="margin-top: 10px; text-align: center;">' +
                                    '    <button id="button_modal_cancel">Cancel</button>' +
                                    '    <button id="button_modal_create" style="margin-left: 5px;">Create Snippet</button>' +
                                    '</div>';

                                var v_modal = openModal(v_html);

                                var v_editor = ace.edit('div_snippet_editor');
                                v_editor.getSession().setMode('ace/mode/plain_text');
                                v_editor.setTheme("ace/theme/" + v_editor_theme);
                                v_editor.getSession().setUseSoftTabs(true);

                                var v_selectSnippetMode = document.getElementById('select_snippet_mode');

                                v_selectSnippetMode.addEventListener(
                                    'change',
                                    function(p_editor, p_event) {
                                        p_editor.getSession().setMode('ace/mode/' + this.value);
                                    }.bind(v_selectSnippetMode, v_editor)
                                );

                                var v_buttonCancel = document.getElementById('button_modal_cancel');

                                v_buttonCancel.addEventListener(
                                    'click',
                                    function(p_modal, p_event) {
                                        p_modal.remove();
                                    }.bind(v_buttonCancel, v_modal)
                                );

                                var v_buttonCreate = document.getElementById('button_modal_create');
                                v_buttonCreate.groupCode = p_chatPopUp.tag.renderedGroup;

                                v_buttonCreate.addEventListener(
                                    'click',
                                    function(p_editor, p_modal, p_event) {
                                        var v_data = {
                                            messageTitle: document.getElementById('input_snippet_title').value,
                                            messageContent: p_editor.getValue(),
                                            messageType: 3, //Snippet
                                            messageSnippetMode: document.getElementById('select_snippet_mode').value,
                                            groupCode: this.groupCode
                                        };

                                        chatSendGroupMessage(v_data);

                                        p_modal.remove();
                                    }.bind(v_buttonCreate, v_editor, v_modal)
                                );
                            }.bind(v_snippetItem, p_chatPopUp)
                        );

                        v_div.appendChild(v_snippetItem);

                        var v_uploadItem = document.createElement('div');
                        v_uploadItem.classList.add('div_chat_right_left_footer_left_options_item');
                        v_uploadItem.innerHTML = 'File Upload';

                        v_uploadItem.addEventListener(
                            'click',
                            function(p_chatPopUp, p_event) {
                                var v_inputFile = document.createElement('input');
                                v_inputFile.type = 'file';
                                v_inputFile.multiple = true;
                                v_inputFile.value = '';

                                v_inputFile.addEventListener(
                                    'change',
                                    function(p_chatPopUp, p_event) {
                                        if('files' in this && this.files.length > 0) {
                                            for(var i = 0; i < this.files.length; i++) {
                                                var v_blob = this.files[i];

                                                var v_binaryReader = new FileReader();
                                                v_binaryReader.groupCode = p_chatPopUp.tag.renderedGroup;

                                                var v_progressBar = document.createElement('div');
	                                            v_progressBar.classList.add('progress_bar');

	                                            var v_bar = document.createElement('div')
	                                            v_bar.classList.add('bar_yellow');
	                                            v_bar.style.width = '0%';
	                                            v_progressBar.appendChild(v_bar);

	                                            var v_percent = document.createElement('div');
	                                            v_percent.classList.add('percent');
	                                            v_percent.innerHTML = 'Uploading File "' + v_blob.name + '": 0%';
	                                            v_progressBar.appendChild(v_percent);

	                                            var v_binaryReader = new FileReader();
	                                            v_binaryReader.groupCode = p_chatPopUp.tag.renderedGroup;

	                                            v_binaryReader.addEventListener(
	                                                'loadstart',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    if(p_progressBar != null) {
	                                                        document.getElementById('div_chat_right_left_header').appendChild(p_progressBar)
	                                                    }
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.addEventListener(
	                                                'progress',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    if(p_event.lengthComputable) {
	                                                        if(p_progressBar != null) {
	                                                            var v_progress = parseInt(((p_event.loaded / p_event.total) * 100), 10);
	                                                            p_progressBar.firstChild.style.width = v_progress + '%';
	                                                            p_progressBar.lastChild.innerHTML = 'Uploading File "' + p_name + '": ' + v_progress + '%';
	                                                        }
	                                                    }
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.addEventListener(
	                                                'loadend',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    if(p_progressBar != null) {
	                                                        p_progressBar.firstChild.style.width = '100%';
	                                                        p_progressBar.firstChild.classList.remove('bar_yellow');
	                                                        p_progressBar.firstChild.classList.add('bar_green');
	                                                        p_progressBar.lastChild.innerHTML = 'File Upload "' + p_name + '" finished: 100%. Processing File...';
	                                                    }
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.addEventListener(
	                                                'load',
	                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
	                                                    var v_data = {
	                                                        messageAttachmentName: p_name,
	                                                        messageTitle: p_name,
	                                                        messageContent: window.btoa(p_event.target.result),
	                                                        messageType: 4, //Attachment
	                                                        groupCode: this.groupCode
	                                                    };

	                                                    var v_context = {
	                                                        progressBar: p_progressBar
	                                                    };

                                                        chatSendGroupMessage(v_data, v_context);
	                                                }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
	                                            );

	                                            v_binaryReader.readAsBinaryString(v_blob);
                                            }
                                        }
                                    }.bind(v_inputFile, p_chatPopUp)
                                );

                                v_inputFile.click();
                            }.bind(v_uploadItem, p_chatPopUp)
                        );

                        v_div.appendChild(v_uploadItem);

                        this.parentElement.appendChild(v_div);
                        v_div.focus();
	                }.bind(v_buttonChatRightFooterLeft, p_chatPopUp)
	            );

                //Editor container
	            var v_rightFooterMiddle = document.createElement('div');
	            v_rightFooterMiddle.id = 'div_chat_right_left_footer_middle';
	            v_rightFooter.appendChild(v_rightFooterMiddle);

                var v_editor = $('#div_chat_right_left_footer_middle').emojioneArea({
				    pickerPosition: 'top',
				    filtersPosition: 'top',
				    tonesStyle: 'bullet',
                    saveEmojisAs: 'shortname',
                    useInternalCDN: false
                });

                p_chatPopUp.tag.renderedEditor = v_editor[0].emojioneArea;

                window.addEventListener(
                    'blur',
                    function(p_editor, p_event) {
                        if(p_editor != null) {
                            p_editor.altPressed = false;
                            p_editor.shiftPressed = false;
                        }
                    }.bind(window, v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.sentWriting = false;
                v_editor[0].emojioneArea.sentNotWriting = true; //true in order to avoid first message bug
                v_editor[0].emojioneArea.altPressed = false;
                v_editor[0].emojioneArea.shiftPressed = false;
                v_editor[0].selectingEmoji = false;
                v_editor[0].selectingUserMenu = null;

                v_editor[0].emojioneArea.checkSelectingUser = function() {
                    var v_return = false;

                    if(window.getSelection().rangeCount > 0) {
                        var v_range = window.getSelection().getRangeAt(0);

                        var i = v_range.startOffset;

                        var v_content = '';

                        if(v_range.startContainer.nodeType == 1) {//Element Node
                            if(v_range.startContainer.childNodes.length > v_range.startOffset) {
                                v_content = (v_range.startContainer.childNodes[v_range.startOffset].innerHTML || v_range.startContainer.childNodes[v_range.startOffset].textContent);
                            }
                        }
                        else if(v_range.startContainer.nodeType == 3) {//Text Node
                            v_content = v_range.startContainer.textContent
                        }

                        var v_char = v_content.substring(i, i + 1);

                        if(v_char == ' ' || v_char == String.fromCharCode(160)) {
                            i--;
                            v_char = v_content.substring(i, i + 1);
                        }

                        while(i >= 0 && v_char != ' ' && v_char != String.fromCharCode(160)) {
                            if(v_char == '@') {
                                v_return = true;
                                break;
                            }

                            i--;
                            v_char = v_content.substring(i, i + 1);
                        }
                    }

                    return v_return;
                }.bind(v_editor[0].emojioneArea);

                v_editor[0].emojioneArea.getSelectingUserInfo = function() {
                    var v_return = {
                        startOffset: -1,
                        endOffset: -1,
                        text: '',
                        node: null
                    };

                    var v_text = '';

                    var v_range = window.getSelection().getRangeAt(0);
                    v_return.node = v_range.startContainer;

                    var i = v_range.startOffset;
                    var v_startChar = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(i, i + 1);

                    if(v_startChar == ' ' || v_startChar == String.fromCharCode(160)) {
                        i--;
                    }

                    v_return.startOffset = i;

                    while(i >= 0) {
                        var v_char = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(i, i + 1);

                        if(v_char == '@') {
                            break;
                        }

                        v_text = v_char + v_text;

                        v_return.startOffset = i;
                        v_return.text = v_text;

                        i--;
                    }

                    i = v_range.startOffset + 1;

                    if(v_startChar == ' ' || v_startChar == String.fromCharCode(160)) {
                        i--;
                    }

                    v_return.endOffset = i;

                    while(i <= (v_range.startContainer.innerHTML || v_range.startContainer.textContent).length) {
                        var v_char = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(i, i + 1);

                        if(v_char == ' ' || v_char == String.fromCharCode(160)) {
                            break;
                        }

                        v_text += v_char;

                        v_return.endOffset = i;
                        v_return.text = v_text;

                        i++;
                    }

                    return v_return;
                }.bind(v_editor[0].emojioneArea);

                v_editor[0].emojioneArea.on(
                    'blur',
                    function(p_editor, p_event) {
                        if(this.selectingUserMenu != null) {
                            this.selectingUserMenu.classList.add('context_menu_hidden');
                        }
                    }.bind(v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.on(
                    'focus',
                    function(p_editor, p_event) {
                        if(this.checkSelectingUser()) {
                            if(this.selectingUserMenu != null) {
                                this.selectingUserMenu.classList.remove('context_menu_hidden');
                            }
                        }
                    }.bind(v_editor[0].emojioneArea)
                );

                v_editor[0].emojioneArea.on(
                    'keydown',
                    function(p_chatPopUp, p_editor, p_event) {
                        var v_dropdownMenu = document.querySelector('.dropdown-menu.textcomplete-dropdown');

                        if(v_dropdownMenu != null) {
                            this.selectingEmoji = v_dropdownMenu.style.display == 'block';
                        }
                        else {
                            this.selectingEmoji = false;
                        }

                        if(p_editor[0].innerHTML.length > 0 && !this.sentWriting) {
                            var v_data = {
                                groupCode: p_chatPopUp.tag.renderedGroup,
                                userCode: parseInt(v_user_id),
                                userWriting: true
                            };

                            chatSetGroupUserWriting(v_data);

                            this.sentWriting = true;
                            this.sentNotWriting = false;
                        }
                        else {
                            if(p_editor[0].innerHTML.length == 0 && !this.sentNotWriting) {
                                var v_data = {
                                    groupCode: p_chatPopUp.tag.renderedGroup,
                                    userCode: parseInt(v_user_id),
                                    userWriting: false
                                };

                                chatSetGroupUserWriting(v_data);

                                this.sentWriting = false;
                                this.sentNotWriting = true;
                            }
                        }

                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = true;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = true;
                        }

                        if(!this.checkSelectingUser()) {
                            if(p_event.key == '@') {
                                if(this.selectingUserMenu != null) {
                                    this.selectingUserMenu.remove();
                                }

                                var v_range = window.getSelection().getRangeAt(0);
                                var v_showMenu = false;

                                if(v_range.startOffset > 0) {
                                    var v_previousChar = (v_range.startContainer.innerHTML || v_range.startContainer.textContent).substring(v_range.startOffset - 1, v_range.startOffset);

                                    if(v_previousChar == String.fromCharCode(160) || v_previousChar ==  ' ') { //If it's a space
                                        v_showMenu = true;
                                    }
                                }
                                else {
                                    v_showMenu = true;
                                }

                                if(v_showMenu) {
                                    var v_group= p_chatPopUp.tag.groupList.getGroupByCode(p_chatPopUp.tag.renderedGroup);

                                    if(v_group != null) {
                                        var v_contextMenu = document.createElement('div');
                                        v_contextMenu.classList.add('context_menu');
                                        v_contextMenu.classList.add('notify_context_menu');
                                        v_contextMenu.style.left = '0px';
                                        v_contextMenu.tabIndex = '0';

                                        for(var i = 0; i < v_group.userList.length; i++) {
                                            var v_contextMenuItem = document.createElement('div');
                                            v_contextMenuItem.classList.add('context_menu_item');
                                            v_contextMenuItem.innerHTML = v_group.userList[i].login + ' (' + v_group.userList[i].name + ')';
                                            v_contextMenuItem.value = v_group.userList[i].login;

                                            v_contextMenuItem.addEventListener(
                                                'mousedown',
                                                function(p_editor, p_event) {
                                                    var v_info = p_editor.getSelectingUserInfo();

                                                    if(v_info.node.innerHTML != null) {
                                                        v_info.node.innerHTML = v_info.node.innerHTML.substring(0, v_info.startOffset) + this.value + '\u00A0' + v_info.node.innerHTML.substring(v_info.endOffset, v_info.node.innerHTML.length);
                                                    }
                                                    else if(v_info.node.textContent != null) {
                                                        v_info.node.textContent = v_info.node.textContent.substring(0, v_info.startOffset) + this.value + '\u00A0' + v_info.node.textContent.substring(v_info.endOffset, v_info.node.textContent.length);
                                                    }

                                                    this.parentElement.remove();
                                                    v_info.node.parentElement.focus();

                                                    var v_offset = v_info.startOffset + this.value.length + 1;

                                                    setTimeout(
                                                        function(p_node, p_offset) {
                                                            p_node.focus();

                                                            var v_selection = window.getSelection();
                                                            v_selection.collapse(p_node.firstChild, p_offset);
                                                        }.bind(null, v_info.node.parentElement, v_offset),
                                                        10
                                                    );
                                                }.bind(v_contextMenuItem, this)
                                            );

                                            v_contextMenuItem.addEventListener(
                                                'mouseenter',
                                                function(p_event) {
                                                    for(var i = 0; i < this.parentElement.children.length; i++) {
                                                        this.parentElement.children[i].classList.remove('context_menu_item_active');
                                                    }

                                                    this.classList.add('context_menu_item_active');
                                                }
                                            );

                                            v_contextMenu.appendChild(v_contextMenuItem);
                                        }

                                        v_contextMenu.firstChild.classList.add('context_menu_item_active');

                                        document.getElementById('div_chat_right_left_footer_left').appendChild(v_contextMenu);

                                        v_contextMenu.style.width = document.getElementById('div_chat_right_left_footer').offsetWidth + 'px';
                                        v_contextMenu.style.top = - 5 - v_contextMenu.offsetHeight + 'px';

                                        this.selectingUserMenu = v_contextMenu;
                                    }
                                }

                                return;
                            }
                        }
                        else {
                            if(this.selectingUserMenu != null) {
                                var v_visibleItems = this.selectingUserMenu.querySelectorAll('.context_menu_item:not(.context_menu_item_hidden)');

                                if(v_visibleItems.length > 0) {
                                    if(p_event.keyCode == 38) {//Arrow Up
                                        p_event.preventDefault();

                                        var i = 0;

                                        for(i; i < v_visibleItems.length; i++) {
                                            if(v_visibleItems[i].classList.contains('context_menu_item_active')) {
                                                v_visibleItems[i].classList.remove('context_menu_item_active');
                                                break;
                                            }
                                        }

                                        if(v_visibleItems.length == 1) {
                                            v_visibleItems[i].classList.add('context_menu_item_active');
                                        }
                                        else {
                                            if(i == 0) {
                                                v_visibleItems[v_visibleItems.length - 1].classList.add('context_menu_item_active');
                                            }
                                            else {
                                                v_visibleItems[i - 1].classList.add('context_menu_item_active');
                                            }
                                        }
                                    }
                                    else if(p_event.keyCode == 40) {//Arrow Down
                                        p_event.preventDefault();

                                        var i = 0;

                                        for(i; i < v_visibleItems.length; i++) {
                                            if(v_visibleItems[i].classList.contains('context_menu_item_active')) {
                                                v_visibleItems[i].classList.remove('context_menu_item_active');
                                                break;
                                            }
                                        }

                                        if(v_visibleItems.length == 1) {
                                            v_visibleItems[i].classList.add('context_menu_item_active');
                                        }
                                        else {
                                            if(i == v_visibleItems.length - 1) {
                                                v_visibleItems[0].classList.add('context_menu_item_active');
                                            }
                                            else {
                                                v_visibleItems[i + 1].classList.add('context_menu_item_active');
                                            }
                                        }
                                    }
                                }
                            }
                        }

                        if(p_event.keyCode == 13) { //Enter
                            p_event.preventDefault();

                            if(!this.checkSelectingUser()) {
                                if(this.altPressed || this.shiftPressed) {
                                    var v_selection = window.getSelection();
                                    var v_range = v_selection.getRangeAt(0);
                                    var v_div = document.createElement('div');
                                    var v_br = document.createElement('br');
                                    v_div.appendChild(v_br);
                                    v_range.deleteContents();
                                    v_range.insertNode(v_div);
                                    v_range.setStartAfter(v_div);
                                    v_range.setEndAfter(v_div);
                                    v_range.collapse(false);
                                    v_selection.removeAllRanges();
                                    v_selection.addRange(v_range);
                                }
                            }
                        }
                    }.bind(v_editor[0].emojioneArea, p_chatPopUp)
                );

                v_editor[0].emojioneArea.on(
                    'keyup',
                    function(p_chatPopUp, p_editor, p_event) {
                        if(p_editor[0].innerHTML.length > 0 && !this.sentWriting) {
                            var v_data = {
                                groupCode: p_chatPopUp.tag.renderedGroup,
                                userCode: parseInt(v_user_id),
                                userWriting: true
                            };

                            chatSetGroupUserWriting(v_data);

                            this.sentWriting = true;
                            this.sentNotWriting = false;
                        }
                        else {
                            if(p_editor[0].innerHTML.length == 0 && !this.sentNotWriting) {
                                var v_data = {
                                    groupCode: p_chatPopUp.tag.renderedGroup,
                                    userCode: parseInt(v_user_id),
                                    userWriting: false
                                };

                                chatSetGroupUserWriting(v_data);

                                this.sentWriting = false;
                                this.sentNotWriting = true;
                            }
                        }

                        if(p_event.keyCode == 18) { //Alt
                            this.altPressed = false;
                        }
                        else if(p_event.keyCode == 16) { //Shift
                            this.shiftPressed = false;
                        }

                        if(this.checkSelectingUser()) {
                            if(p_event.keyCode != 38 && p_event.keyCode != 40 && p_event.keyCode != 13) {//Arrow Up | Arrow Down | Enter
                                if(this.selectingUserMenu != null) {
                                    this.selectingUserMenu.classList.remove('context_menu_hidden');

                                    var v_text = this.getSelectingUserInfo().text;

                                    for(var i = 0; i < this.selectingUserMenu.children.length; i++) {
                                        this.selectingUserMenu.children[i].classList.remove('context_menu_item_hidden');

                                        if(this.selectingUserMenu.children[i].innerHTML.indexOf(v_text) == -1) {
                                            this.selectingUserMenu.children[i].classList.add('context_menu_item_hidden');
                                        }
                                    }

                                    this.selectingUserMenu.style.top = - 5 - this.selectingUserMenu.offsetHeight + 'px';

                                    for(var i = 0; i < this.selectingUserMenu.children.length; i++) {
                                        this.selectingUserMenu.children[i].classList.remove('context_menu_item_active');
                                    }

                                    var v_visibleItems = this.selectingUserMenu.querySelectorAll('.context_menu_item:not(.context_menu_item_hidden)');

                                    if(v_visibleItems.length > 0) {
                                        v_visibleItems[0].classList.add('context_menu_item_active');
                                    }
                                }
                            }
                        }
                        else {
                            if(this.selectingUserMenu != null) {
                                this.selectingUserMenu.classList.add('context_menu_hidden');
                            }
                        }

                        if(p_event.keyCode == 13 && !this.selectingEmoji && !this.altPressed && !this.shiftPressed) { //Enter and not selecting emoticons or inserting new lines
                            p_event.preventDefault();

                            if(this.checkSelectingUser() && this.selectingUserMenu != null) {
                                var v_active = this.selectingUserMenu.querySelector('.context_menu_item_active');

                                if(v_active != null) {
                                    var v_info = this.getSelectingUserInfo();

                                    if(v_info.node.textContent != null) {
                                        v_info.node.textContent = v_info.node.textContent.substring(0, v_info.startOffset) + v_active.value + '\u00A0' + v_info.node.textContent.substring(v_info.endOffset, v_info.node.textContent.length);
                                    }
                                    else if(v_info.node.innerHTML != null) {
                                        v_info.node.innerHTML = v_info.node.innerHTML.substring(0, v_info.startOffset) + v_active.value + '\u00A0' + v_info.node.innerHTML.substring(v_info.endOffset, v_info.node.innerHTML.length);
                                    }

                                    this.selectingUserMenu.remove();
                                    v_info.node.parentElement.focus();

                                    var v_offset = v_info.startOffset + v_active.value.length + 1;

                                    setTimeout(
                                        function(p_node, p_offset) {
                                            p_node.focus();

                                            var v_selection = window.getSelection();
                                            v_selection.collapse(p_node.firstChild, p_offset);
                                        }.bind(null, v_info.node.parentElement, v_offset),
                                        10
                                    );
                                }
                            }
                            else {
                                if(p_editor[0].innerHTML.length > 0) {
                                    var v_data = {
                                        messageType: 1, //Plain Text
                                        messageContent: p_editor[0].innerHTML,
                                        messageRawContent: this.getText(),
                                        groupCode: p_chatPopUp.tag.renderedGroup
                                    }

                                    chatSendGroupMessage(v_data);

                                    this.setText('');
                                    p_editor[0].focus();

                                    var v_data = {
                                        groupCode: p_chatPopUp.tag.renderedGroup,
                                        userCode: parseInt(v_user_id),
                                        userWriting: false
                                    };

                                    chatSetGroupUserWriting(v_data);

                                    this.sentWriting = false;
                                    this.sentNotWriting = true;
                                }
                            }
                        }
                    }.bind(v_editor[0].emojioneArea, p_chatPopUp)
                );

                //Using third party software (emojioneArea), so we need an observer to know when things are ready to be used
                var v_mutationObserver = new MutationObserver(
                    function(p_chatPopUp, p_mutationList, p_this) {
						var v_editor = document.querySelector('.emojionearea-editor');

                        if(v_editor != null) {
                            v_editor.addEventListener(
                                'paste',
                                function(p_chatPopUp, p_event) {
                                    var v_items = (p_event.clipboardData || p_event.originalEvent.clipboardData).items;

                                    for(v_key in v_items) {
                                        var v_item = v_items[v_key];

			                            if(v_item.kind === 'file') {
                                            var v_blob = v_item.getAsFile();

                                            if(v_blob.type.indexOf('image') == -1) {
                                                return;
                                            }

                                            var v_name = 'Pasted Image at ' + formatTimestamp(new Date()) + '.png';

                                            var v_progressBar = document.createElement('div');
                                            v_progressBar.classList.add('progress_bar');

                                            var v_bar = document.createElement('div')
                                            v_bar.classList.add('bar_yellow');
                                            v_bar.style.width = '0%';
                                            v_progressBar.appendChild(v_bar);

                                            var v_percent = document.createElement('div');
                                            v_percent.classList.add('percent');
                                            v_percent.innerHTML = 'Uploading File "' + v_name + '": 0%';
                                            v_progressBar.appendChild(v_percent);

                                            var v_binaryReader = new FileReader();
                                            v_binaryReader.groupCode = p_chatPopUp.tag.renderedGroup;

                                            v_binaryReader.addEventListener(
                                                'loadstart',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    if(p_progressBar != null) {
                                                        document.getElementById('div_chat_right_left_header').appendChild(p_progressBar)
                                                    }
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.addEventListener(
                                                'progress',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    if(p_event.lengthComputable) {
                                                        if(p_progressBar != null) {
	                                                        var v_progress = parseInt(((p_event.loaded / p_event.total) * 100), 10);
	                                                        p_progressBar.firstChild.style.width = v_progress + '%';
	                                                        p_progressBar.lastChild.innerHTML = 'Uploading File "' + p_name + '": ' + v_progress + '%';
                                                        }
                                                    }
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.addEventListener(
                                                'loadend',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    if(p_progressBar != null) {
	                                                    p_progressBar.firstChild.style.width = '100%';
	                                                    p_progressBar.firstChild.classList.remove('bar_yellow');
	                                                    p_progressBar.firstChild.classList.add('bar_green');
	                                                    p_progressBar.lastChild.innerHTML = 'File Upload "' + p_name + '" finished: 100%. Processing File...';
                                                    }
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.addEventListener(
                                                'load',
                                                function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                    var v_data = {
                                                        messageAttachmentName: p_name,
                                                        messageTitle: p_name,
                                                        messageContent: window.btoa(p_event.target.result),
                                                        messageType: 2,//Pasted image
                                                        groupCode: this.groupCode
                                                    };

                                                    var v_context = {
                                                        progressBar: p_progressBar
                                                    };

                                                    chatSendGroupMessage(v_data, v_context);
                                                }.bind(v_binaryReader, p_chatPopUp, v_name, v_progressBar)
                                            );

                                            v_binaryReader.readAsBinaryString(v_blob);
                                        }
                                    }
                                }.bind(v_editor, p_chatPopUp)
                            );

                            v_editor.addEventListener(
                                'drop',
                                function(p_chatPopUp, p_event) {
                                    for(var i = 0; i < p_event.dataTransfer.files.length; i++) {
            							var v_blob = p_event.dataTransfer.files[i];

                                        var v_binaryReader = new FileReader();
                                        v_binaryReader.groupCode = p_chatPopUp.tag.renderedGroup;

                                        var v_progressBar = document.createElement('div');
                                        v_progressBar.classList.add('progress_bar');

                                        var v_bar = document.createElement('div')
                                        v_bar.classList.add('bar_yellow');
                                        v_bar.style.width = '0%';
                                        v_progressBar.appendChild(v_bar);

                                        var v_percent = document.createElement('div');
                                        v_percent.classList.add('percent');
                                        v_percent.innerHTML = 'Uploading File "' + v_blob.name + '": 0%';
                                        v_progressBar.appendChild(v_percent);

                                        var v_binaryReader = new FileReader();
                                        v_binaryReader.groupCode = p_chatPopUp.tag.renderedGroup;

                                        v_binaryReader.addEventListener(
                                            'loadstart',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                if(p_progressBar != null) {
                                                    document.getElementById('div_chat_right_left_header').appendChild(p_progressBar)
                                                }
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.addEventListener(
                                            'progress',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                if(p_event.lengthComputable) {
                                                    if(p_progressBar != null) {
                                                        var v_progress = parseInt(((p_event.loaded / p_event.total) * 100), 10);
                                                        p_progressBar.firstChild.style.width = v_progress + '%';
                                                        p_progressBar.lastChild.innerHTML = 'Uploading File "' + p_name + '": ' + v_progress + '%';
                                                    }
                                                }
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.addEventListener(
                                            'loadend',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                if(p_progressBar != null) {
                                                    p_progressBar.firstChild.style.width = '100%';
                                                    p_progressBar.firstChild.classList.remove('bar_yellow');
                                                    p_progressBar.firstChild.classList.add('bar_green');
                                                    p_progressBar.lastChild.innerHTML = 'File Upload "' + p_name + '" finished: 100%. Processing File...';
                                                }
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.addEventListener(
                                            'load',
                                            function(p_chatPopUp, p_name, p_progressBar, p_event) {
                                                var v_data = {
                                                    messageAttachmentName: p_name,
                                                    messageTitle: p_name,
                                                    messageContent: window.btoa(p_event.target.result),
                                                    messageType: 4, //Attachment
                                                    groupCode: this.groupCode
                                                };

                                                var v_context = {
                                                    progressBar: p_progressBar
                                                };

                                                chatSendGroupMessage(v_data, v_context);
                                            }.bind(v_binaryReader, p_chatPopUp, v_blob.name, v_progressBar)
                                        );

                                        v_binaryReader.readAsBinaryString(v_blob);
                                    }
                                }.bind(v_editor, p_chatPopUp)
                            );

							p_this.disconnect(); // stop observing
						    return;
						}
                    }.bind(v_mutationObserver, p_chatPopUp)
                );

                v_mutationObserver.observe(
                    document,
                    {
                        childList: true,
                        subtree: true
                    }
                );

                //Position scroll on first unread message
                for(var i = v_group.messageList.length - 1; i >= 0; i--) {
                    if(!v_group.messageList[i].viewed) {
                        v_firstUnreadMessageCode = v_group.messageList[i].code
                        break;
                    }
                }
            }
            else {
                v_divChatRightContent.innerHTML = '';
            }

            for(var i = 0; i < v_group.messageList.length; i++) {
                var j = i;

                for(j; j < v_group.messageList.length; j++) {
                    if(v_group.messageList[i].user.code != v_group.messageList[j].user.code) {
                        break;
                    }

                    var v_item = p_chatPopUp.tag.getRenderedGroupMessage(v_group.code, v_group.messageList[j], false);
                    v_divChatRightContent.insertBefore(v_item, v_divChatRightContent.firstChild);
                }

                v_divChatRightContent.children[0].remove();
                var v_item = p_chatPopUp.tag.getRenderedGroupMessage(v_group.code, v_group.messageList[j - 1], true);
                v_divChatRightContent.insertBefore(v_item, v_divChatRightContent.firstChild);
                i = j - 1;
            }

            var v_actualDate = '';
            var v_itemList = document.querySelectorAll('#div_chat_right_left_content > .div_chat_right_left_item');

            for(var j = 0; j < v_itemList.length; j++) {
                //If date has changed, then add date mark
                if(v_itemList[j].createdAt.substring(0, 10) != v_actualDate) {
                    v_actualDate = v_itemList[j].createdAt.substring(0, 10);

                    var v_h2SideLinesContainer = document.createElement('h2');
                    v_h2SideLinesContainer.classList.add('h2_side_lines_container');

                    var v_spanSideLinesContent = document.createElement('span');
                    v_spanSideLinesContent.classList.add('span_side_lines_content');
                    v_spanSideLinesContent.innerHTML = v_actualDate;
                    v_h2SideLinesContainer.appendChild(v_spanSideLinesContent);

                    v_divChatRightContent.insertBefore(v_h2SideLinesContainer, v_itemList[j]);
                }
            }

            //Remove first date mark
            if(v_divChatRightContent.children.length > 0) {
                v_divChatRightContent.children[0].remove();
            }

            if(p_renderAtMessage != null) {
                for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                    if(v_divChatRightContent.childNodes[i].messageCode == p_renderAtMessage) {
                        v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                        break;
                    }
                }
            }
            else {
                if(v_sameGroup) {
                    if(v_onLastMessage) {
                        v_divChatRightContent.scrollTop = v_divChatRightContent.scrollHeight;
                    }
                    else {
                        if(v_firstVisibleMessageCode != null) {
                            for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                                if(v_divChatRightContent.childNodes[i].messageCode == v_firstVisibleMessageCode) {
                                    v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                                    break;
                                }
                            }
                        }
                    }
                }
                else {
                    if(v_firstUnreadMessageCode != null) {
                        for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                            if(v_divChatRightContent.childNodes[i].messageCode == v_firstUnreadMessageCode) {
                                v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                                break;
                            }
                        }
                    }
                    else {
                        v_divChatRightContent.scrollTop = v_divChatRightContent.scrollHeight - v_divChatRightContent.offsetHeight;
                    }
                }
            }

            var v_groupElementList = document.querySelectorAll('#div_chat_groups > .div_chat_left_content > .div_chat_left_content_item');

            for(var i = 0; i < v_groupElementList.length; i++) {
                if(v_groupElementList[i].groupCode == p_groupCode) {
                    v_groupElementList[i].classList.add('div_chat_left_content_item_active');
                    break;
                }
            }

            //Mark messages as read, if it's the case
            if((v_divChatRightContent.offsetHeight + v_divChatRightContent.scrollTop + 1) >= v_divChatRightContent.scrollHeight) {
                var v_messageCodeList = [];

	            for(var i = 0; i < v_group.messageList.length; i++) {
	                if(!v_group.messageList[i].viewed) {
	                    v_messageCodeList.push(v_group.messageList[i].code);
	                }
	            }

	            if(v_messageCodeList.length > 0) {
	                var v_data = {
	                    groupCode: v_group.code,
	                    messageCodeList: v_messageCodeList
	                };

	                chatMarkGroupMessagesAsRead(v_data);
	            }
            }

            var v_groupContext = p_chatPopUp.tag.contextList.getContextByGroupCode(v_group.code);

            if(v_groupContext != null) {
                if(!v_groupContext.firstRender) {
                    p_chatPopUp.tag.renderedEditor.setText(v_groupContext.text);

                    if(!p_preventContextScroll) {
                        p_chatPopUp.tag.renderedContent.scrollTop = v_groupContext.scrollTop + 1; //In order to avoid bug and recover messages
                    }
                }
                else {
                    v_groupContext.firstRender
                }
            }
        }

        p_chatPopUp.tag.updateHeader();
    }.bind(v_chatPopUp.tag.renderGroup, v_chatPopUp);

    v_chatPopUp.tag.renderChannelItem = function(p_channel) {
        var v_channelsContent = document.querySelector('#div_chat_channels > .div_chat_left_content');

        var v_unreadCount = 0;

        for(var k = 0; k < p_channel.messageList.length; k++) {
            if(!p_channel.messageList[k].viewed) {
                v_unreadCount++;
            }
        }

        var v_item = document.createElement('div');
        v_item.channelCode = p_channel.code;
        v_item.name = p_channel.name.toLowerCase();
        v_item.innerHTML = p_channel.name;
        v_item.classList.add('div_chat_left_content_item');

        var v_status = document.createElement('img');
        v_status.classList.add('div_chat_left_content_item_status');

        if(p_channel.private) {
            v_status.src = '/static/OmniDB_app/images/icons/status_chat_privatechannel.png';
        }
        else {
            v_status.src = '/static/OmniDB_app/images/icons/status_chat_channel.png';
        }

        v_item.insertBefore(v_status, v_item.firstChild);

        var v_badge = document.createElement('span');
        v_badge.classList.add('badge');
        v_badge.classList.add('badge_hidden');
        v_badge.innerHTML = v_unreadCount;
        v_item.appendChild(v_badge);

        if(v_unreadCount > 0) {
            v_item.classList.add('div_chat_left_content_item_unread');
            v_badge.classList.remove('badge_hidden');
        }

        v_item.addEventListener(
            'click',
            function(p_chatPopUp, p_event) {
                p_chatPopUp.tag.renderChannel(this.channelCode, null, false);
            }.bind(v_item, v_chatPopUp)
        );

        v_item.addEventListener(
            'contextmenu',
            function(p_chatPopUp, p_event) {
                p_event.preventDefault();

                if(this.channelCode != null) {
                    var v_channel = p_chatPopUp.tag.channelList.getChannelByCode(this.channelCode);

                    if(v_channel != null) {
                        var v_contextMenu = document.createElement('div');
                        v_contextMenu.classList.add('context_menu');
                        v_contextMenu.style.top = p_event.pageY + 'px';
                        v_contextMenu.style.left = p_event.pageX + 'px';
                        v_contextMenu.tabIndex = '0';

                        var v_contextMenuItem = document.createElement('div');
                        v_contextMenuItem.classList.add('context_menu_item');

                        if(v_channel.silenced) {
                            v_contextMenuItem.innerHTML = 'Enable Notifications';
                        }
                        else {
                            v_contextMenuItem.innerHTML = 'Disable Notifications';
                        }

                        v_contextMenuItem.addEventListener(
                            'click',
                            function(p_channel, p_event) {
                                var v_data = {
                                    channelCode: p_channel.code,
                                    silenceChannel: !p_channel.silenced
                                };

                                chatChangeChannelSilenceSettings(v_data);

                                this.parentElement.blur();
                            }.bind(v_contextMenuItem, v_channel)
                        );

                        v_contextMenu.appendChild(v_contextMenuItem);

                        if(v_channel.private) {
                            var v_contextMenuItem = document.createElement('div');
                            v_contextMenuItem.classList.add('context_menu_item');
                            v_contextMenuItem.innerHTML = 'Add Users';

                            v_contextMenuItem.addEventListener(
                                'click',
                                function(p_chatPopUp, p_channel, p_event) {
                                    var v_html =
                                        '<div id="div_invite_channel_container">' +
                                        '    <input type="text" id="input_invite_channel_filter" class="form-control" placeholder="Type to filter results"/>' +
                                        '    <div id="div_invite_channel_items_container">';

                                    for(var i = 0; i < p_chatPopUp.tag.userList.length; i++) {
                                        var v_found = false;

                                        for(var j = 0; j < p_channel.userList.length; j++) {
                                            if(p_chatPopUp.tag.userList[i].code == p_channel.userList[j].code) {
                                                v_found = true;
                                                break;
                                            }
                                        }

                                        if(!v_found) {//Not a channel member yet
                                            v_html +=
                                                '<div class="div_invite_channel_item">' +
                                                '    <input type="checkbox" value="' + p_chatPopUp.tag.userList[i].code + '" />' +
                                                '    <span><b>' + p_chatPopUp.tag.userList[i].login + '</b> (' + p_chatPopUp.tag.userList[i].name + ')</span>' +
                                                '</div>';
                                        }
                                    }

                                    v_html +=
                                        '    </div>' +
                                        '</div>' +
                                        '<div style="text-align: center;">' +
                                        '    <button id="button_invite_channel_cancel">Cancel</button>' +
                                        '    <button id="button_invite_channel_ok">Ok</button>' +
                                        '</div>';

                                    var v_modal = openModal(v_html);

                                    var v_buttonCancel = document.getElementById('button_invite_channel_cancel');

                                    v_buttonCancel.addEventListener(
                                        'click',
                                        function(p_modal, p_event) {
                                            p_modal.remove();
                                        }.bind(v_buttonCancel, v_modal)
                                    );

                                    var v_buttonOk = document.getElementById('button_invite_channel_ok');
                                    v_buttonOk.channelCode = p_channel.code;

                                    v_buttonOk.addEventListener(
                                        'click',
                                        function(p_modal, p_event) {
                                            var v_userCodeList = [];

                                            var v_inviteChannelItems = document.querySelectorAll('.div_invite_channel_item');

                                            for(var i = 0; i < v_inviteChannelItems.length; i++) {
                                                if(v_inviteChannelItems[i].children[0].checked) {
                                                    v_userCodeList.push(parseInt(v_inviteChannelItems[i].children[0].value));
                                                }
                                            }

                                            var v_data = {
                                                userCodeList: v_userCodeList,
                                                channelCode: this.channelCode
                                            };

                                            chatInvitePrivateChannelMembers(v_data);

                                            p_modal.remove();
                                        }.bind(v_buttonOk, v_modal)
                                    );

                                    var v_inputInviteChannelFilter = document.getElementById('input_invite_channel_filter');

                                    v_inputInviteChannelFilter.addEventListener(
                                        'keydown',
                                        function(p_buttonOk, p_event) {
                                            if(p_event.keyCode == 13) {//Enter
                                                p_buttonOk.click();
                                            }
                                            else {
                                                var v_inviteChannelItems = document.querySelectorAll('.div_invite_channel_item');

                                                for(var i = 0; i < v_inviteChannelItems.length; i++) {
                                                    if(v_inviteChannelItems[i].innerText.toLowerCase().indexOf(this.value.toLowerCase()) != -1) {
                                                        v_inviteChannelItems[i].style.display = '';
                                                    }
                                                    else {
                                                        v_inviteChannelItems[i].style.display = 'none';
                                                    }
                                                }
                                            }
                                        }.bind(v_inputInviteChannelFilter, v_buttonOk)
                                    );

                                    v_inputInviteChannelFilter.addEventListener(
                                        'keyup',
                                        function(p_buttonOk, p_event) {
                                            var v_inviteChannelItems = document.querySelectorAll('.div_invite_channel_item');

                                            for(var i = 0; i < v_inviteChannelItems.length; i++) {
                                                if(v_inviteChannelItems[i].innerText.toLowerCase().indexOf(this.value.toLowerCase()) != -1) {
                                                    v_inviteChannelItems[i].style.display = '';
                                                }
                                                else {
                                                    v_inviteChannelItems[i].style.display = 'none';
                                                }
                                            }
                                        }.bind(v_inputInviteChannelFilter, v_buttonOk)
                                    );

                                    v_inputInviteChannelFilter.focus();

                                    this.parentElement.blur();
                                }.bind(v_contextMenuItem, p_chatPopUp, v_channel)
                            );

                            v_contextMenu.appendChild(v_contextMenuItem);

                            var v_contextMenuItem = document.createElement('div');
                            v_contextMenuItem.classList.add('context_menu_item');
                            v_contextMenuItem.innerHTML = 'Rename Channel';

                            v_contextMenuItem.addEventListener(
                                'click',
                                function(p_channel, p_event) {
                                    var v_html =
                                        '<div id="div_rename_channel_container">' +
                                        '    <span id="span_rename_channel_name">New name of the channel: </span>' +
                                        '    <input type="text" id="input_rename_channel_name" class="form-control" />' +
                                        '</div>' +
                                        '<div style="text-align: center;">' +
                                        '    <button id="button_rename_channel_cancel">Cancel</button>' +
                                        '    <button id="button_rename_channel_ok">Ok</button>' +
                                        '</div>';

                                    var v_modal = openModal(v_html);

                                    var v_buttonCancel = document.getElementById('button_rename_channel_cancel');

                                    v_buttonCancel.addEventListener(
                                        'click',
                                        function(p_modal, p_event) {
                                            p_modal.remove();
                                        }.bind(v_buttonCancel, v_modal)
                                    );

                                    var v_buttonOk = document.getElementById('button_rename_channel_ok');
                                    v_buttonOk.channelCode = p_channel.code;

                                    v_buttonOk.addEventListener(
                                        'click',
                                        function(p_modal, p_event) {
                                            var v_inputRenameChannelName = document.getElementById('input_rename_channel_name');

                                            if(v_inputRenameChannelName.value.length == 0) {
                                                openModal('<div>Please, type the new name of the channel.</div>');
                                                return;
                                            }

                                            var v_data = {
                                                channelName: v_inputRenameChannelName.value,
                                                channelCode: this.channelCode
                                            };

                                            chatRenamePrivateChannel(v_data);

                                            p_modal.remove();
                                        }.bind(v_buttonOk, v_modal)
                                    );

                                    var v_inputRenameChannelName = document.getElementById('input_rename_channel_name');
                                    v_inputRenameChannelName.value = p_channel.name;

                                    v_inputRenameChannelName.addEventListener(
                                        'keydown',
                                        function(p_buttonOk, p_event) {
                                            if(p_event.keyCode == 13) {//Enter
                                                p_buttonOk.click();
                                            }
                                        }.bind(v_inputRenameChannelName, v_buttonOk)
                                    );

                                    v_inputRenameChannelName.focus();

                                    this.parentElement.blur();
                                }.bind(v_contextMenuItem, v_channel)
                            );

                            v_contextMenu.appendChild(v_contextMenuItem);

                            var v_contextMenuItem = document.createElement('div');
                            v_contextMenuItem.classList.add('context_menu_item');
                            v_contextMenuItem.innerHTML = 'Leave Channel';

                            v_contextMenuItem.addEventListener(
                                'click',
                                function(p_channel, p_event) {
                                    var v_html =
                                        '<div style="margin-bottom: 10px;">' +
                                        '    <span>Do you really want to leave the channel <b>' + p_channel.name + '</b>?</span> ' +
                                        '</div>' +
                                        '<div style="text-align: center;">' +
                                        '    <button id="button_quit_channel_no">No</button>' +
                                        '    <button id="button_quit_channel_yes">Yes</button>' +
                                        '</div>';

                                    var v_modal = openModal(v_html);

                                    var v_buttonNo = document.getElementById('button_quit_channel_no');

                                    v_buttonNo.addEventListener(
                                        'click',
                                        function(p_modal, p_event) {
                                            p_modal.remove();
                                        }.bind(v_buttonNo, v_modal)
                                    );

                                    var v_buttonYes = document.getElementById('button_quit_channel_yes');
                                    v_buttonYes.channelCode = p_channel.code;

                                    v_buttonYes.addEventListener(
                                        'click',
                                        function(p_modal, p_event) {
                                            var v_data = {
                                                channelCode: this.channelCode
                                            };

                                            chatQuitPrivateChannel(v_data);

                                            p_modal.remove();
                                        }.bind(v_buttonYes, v_modal)
                                    );

                                    v_buttonNo.focus();

                                    this.parentElement.blur();
                                }.bind(v_contextMenuItem, v_channel)
                            );

                            v_contextMenu.appendChild(v_contextMenuItem);
                        }

                        v_contextMenu.addEventListener(
                            'blur',
                            function(p_event) {
                                this.remove();
                            }
                        );

                        document.body.appendChild(v_contextMenu);
                        v_contextMenu.focus();
                    }
                }
            }.bind(v_item, v_chatPopUp)
        );

        v_channelsContent.appendChild(v_item);

        //Sort channels by name
        var v_itemsArray = [];

        for(var i = 0; i < v_channelsContent.children.length; i++) {
            v_itemsArray.push(v_channelsContent.children[i]);
        }

        v_itemsArray.sort(
            function(a, b) {
                return ((a.innerHTML == b.innerHTML) ? 0 : ((a.innerHTML > b.innerHTML) ? 1 : -1));
            }
        );

        for(var i = 0; i < v_itemsArray.length; i++) {
            v_channelsContent.appendChild(v_itemsArray[i]);
        }
    };

    //Render channels items
    for(var i = 0; i < v_chatPopUp.tag.channelList.length; i++) {
        v_chatPopUp.tag.renderChannelItem(v_chatPopUp.tag.channelList[i]);

        v_chatPopUp.tag.contextList.push({
            type: 1, //Channel
            code: v_chatPopUp.tag.channelList[i].code,
            text: '',
            scrollTop: 0,
            firstRender: true
        });
    }

    v_chatPopUp.tag.renderGroupItem = function(p_group) {
        var v_groupsContent = document.querySelector('#div_chat_groups > .div_chat_left_content');

        for(var j = 0; j < p_group.userList.length; j++) {
            if(p_group.userList[j].code != v_user_id) {
                var v_unreadCount = 0;

                for(var k = 0; k < p_group.messageList.length; k++) {
                    if(!p_group.messageList[k].viewed) {
                        v_unreadCount++;
                    }
                }

                var v_item = document.createElement('div');
                v_item.groupCode = p_group.code;
                v_item.userCode = p_group.userList[j].code;
                v_item.userName = p_group.userList[j].name.toLowerCase();
                v_item.userLogin = p_group.userList[j].login.toLowerCase();
		        v_item.innerHTML = p_group.userList[j].login;
                v_item.title = p_group.userList[j].name;
		        v_item.classList.add('div_chat_left_content_item');

                var v_status = document.createElement('img');
                v_status.classList.add('div_chat_left_content_item_status');

                if(v_chatPopUp.tag.onlineUserCodeList.indexOf(p_group.userList[j].code) != -1) {
                    v_status.src = '/static/OmniDB_app/images/icons/status_chat_online.png';
                }
                else {
                    v_status.src = '/static/OmniDB_app/images/icons/status_chat_offline.png';
                }

                v_item.insertBefore(v_status, v_item.firstChild);

                var v_userStatus = document.createElement('img');
                v_userStatus.classList.add('img_user_status_icon');
                v_userStatus.style.marginLeft = '5px';

                for(var i = 0; i < v_chatPopUp.tag.userList.length; i++) {
                    if(v_chatPopUp.tag.userList[i].code == p_group.userList[j].code) {
                        var v_style = v_chatPopUp.tag.getUserChatStatusStyle(v_chatPopUp.tag.userList[i].code);

                        if(v_style != null) {
                            v_userStatus.src = v_style.src;
                            v_userStatus.title = v_style.title;
                            v_userStatus.style.display = v_style.display;
                        }

                        break;
                    }
                }

                v_item.appendChild(v_userStatus);

                var v_badge = document.createElement('span');
                v_badge.classList.add('badge');
                v_badge.classList.add('badge_hidden');
                v_badge.innerHTML = v_unreadCount;
                v_item.appendChild(v_badge);

                if(v_unreadCount > 0) {
                    v_item.classList.add('div_chat_left_content_item_unread');
                    v_badge.classList.remove('badge_hidden');
                }

                v_item.addEventListener(
                    'click',
                    function(p_chatPopUp, p_event) {
                        p_chatPopUp.tag.renderGroup(this.groupCode, null, false);
                    }.bind(v_item, v_chatPopUp)
                );

                v_item.addEventListener(
                    'contextmenu',
                    function(p_chatPopUp, p_event) {
                        p_event.preventDefault();

                        if(this.groupCode != null) {
                            var v_group = p_chatPopUp.tag.groupList.getGroupByCode(this.groupCode);

                            if(v_group != null) {
                                var v_contextMenu = document.createElement('div');
                                v_contextMenu.classList.add('context_menu');
                                v_contextMenu.style.top = p_event.pageY + 'px';
                                v_contextMenu.style.left = p_event.pageX + 'px';
                                v_contextMenu.tabIndex = '0';

                                var v_contextMenuItem = document.createElement('div');
                                v_contextMenuItem.classList.add('context_menu_item');

                                if(v_group.silenced) {
                                    v_contextMenuItem.innerHTML = 'Enable Notifications';
                                }
                                else {
                                    v_contextMenuItem.innerHTML = 'Disable Notifications';
                                }

                                v_contextMenuItem.addEventListener(
                                    'click',
                                    function(p_group, p_event) {
                                        var v_data = {
                                            groupCode: p_group.code,
                                            silenceGroup: !p_group.silenced
                                        };

                                        chatChangeGroupSilenceSettings(v_data);

                                        this.parentElement.blur();
                                    }.bind(v_contextMenuItem, v_group)
                                );

                                v_contextMenu.appendChild(v_contextMenuItem);

                                v_contextMenu.addEventListener(
                                    'blur',
                                    function(p_event) {
                                        this.remove();
                                    }
                                );

                                document.body.appendChild(v_contextMenu);
                                v_contextMenu.focus();
                            }
                        }
                    }.bind(v_item, v_chatPopUp)
                );

                v_groupsContent.appendChild(v_item);

                break;
            }
        }

        //Sort groups by user name
        var v_itemsArray = [];

        for(var i = 0; i < v_groupsContent.children.length; i++) {
            v_itemsArray.push(v_groupsContent.children[i]);
        }

        v_itemsArray.sort(
            function(a, b) {
                return ((a.title == b.title) ? 0 : ((a.title > b.title) ? 1 : -1));
            }
        );

        for(var i = 0; i < v_itemsArray.length; i++) {
            v_groupsContent.appendChild(v_itemsArray[i]);
        }
    };

    //Render groups items
    for(var i = 0; i < v_chatPopUp.tag.groupList.length; i++) {
        v_chatPopUp.tag.renderGroupItem(v_chatPopUp.tag.groupList[i]);

        v_chatPopUp.tag.contextList.push({
            type: 2, //Group
            code: v_chatPopUp.tag.groupList[i].code,
            text: '',
            scrollTop: 0,
            firstRender: true
        });
    }

    //Click first group to initialize a chat window
    var v_item = document.querySelector('.div_chat_left_content > .div_chat_left_content_item');

    if(v_item != null) {
        v_item.click();
    }
}

/**
 * Handles new group message message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {groupCode, message}.
 * @param {object} p_context - some useful javascript object that can be used for controls.
 */
function chatNewGroupMessage(p_data, p_context) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            v_group.messageList.splice(0, 0, p_data.message);

            var v_unreadCount = 0;

            for(var i = 0; i < v_group.messageList.length; i++) {
                if(!v_group.messageList[i].viewed) {
                    v_unreadCount++;
                }
            }

            var v_groupElementList = document.querySelectorAll('#div_chat_groups > .div_chat_left_content > .div_chat_left_content_item');

            for(var i = 0; i < v_groupElementList.length; i++) {
                if(v_groupElementList[i].groupCode == v_group.code) {
                    v_groupElementList[i].lastChild.innerHTML = v_unreadCount;

                    if(v_unreadCount > 0) {
                        if(!v_groupElementList[i].classList.contains('div_chat_left_content_item_unread')) {
                            v_groupElementList[i].classList.add('div_chat_left_content_item_unread');
                        }

                        v_groupElementList[i].lastChild.classList.remove('badge_hidden');
                    }
                    else {
                        v_groupElementList[i].classList.remove('div_chat_left_content_item_unread');

                        if(!v_groupElementList[i].lastChild.classList.contains('badge_hidden')) {
                            v_groupElementList[i].lastChild.classList.add('badge_hidden');
                        }
                    }

                    break;
                }
            }

            var v_forceNotify = (p_data.message.content.indexOf('<span class="span_notify_user">@' + v_user_login + '</span>') != -1) || (!v_group.silenced && document.hidden);

            var v_notify = true;

            if(v_chatPopUp.tag.renderedType == 2 && v_chatPopUp.tag.renderedGroup == v_group.code) {//If the rendered type is group and this group are the rendered one.
                var v_divChatRightContent = document.getElementById('div_chat_right_left_content');
                var v_onLastMessage = false;
                var v_firstVisibleMessageCode = null;

                if((v_divChatRightContent.offsetHeight + v_divChatRightContent.scrollTop + 1) >= v_divChatRightContent.scrollHeight) {//If scroll was at max allowed
                    v_onLastMessage = true;
                    v_notify = false;
                }
                else {
                    for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                        if(v_divChatRightContent.childNodes[i].offsetTop >= v_divChatRightContent.scrollTop) {
                            v_firstVisibleMessageCode = v_divChatRightContent.childNodes[i].messageCode;
                            break;
                        }
                    }
                }

                if(v_divChatRightContent.children.length > 0) {
                    if(v_divChatRightContent.children[v_divChatRightContent.children.length - 1].title.substring(0, 10) != p_data.message.createdAt.substring(0, 10)) {
                        var v_h2SideLinesContainer = document.createElement('h2');
                        v_h2SideLinesContainer.classList.add('h2_side_lines_container');

                        var v_spanSideLinesContent = document.createElement('span');
                        v_spanSideLinesContent.classList.add('span_side_lines_content');
                        v_spanSideLinesContent.innerHTML = p_data.message.createdAt.substring(0, 10);
                        v_h2SideLinesContainer.appendChild(v_spanSideLinesContent);

                        v_divChatRightContent.appendChild(v_h2SideLinesContainer);
                    }

                    var v_item = v_chatPopUp.tag.getRenderedGroupMessage(v_group.code, p_data.message, v_divChatRightContent.children[v_divChatRightContent.children.length - 1].userCode != p_data.message.user.code);
                    v_divChatRightContent.appendChild(v_item);
                }
                else {
                    var v_item = v_chatPopUp.tag.getRenderedGroupMessage(v_group.code, p_data.message, true);
                    v_divChatRightContent.appendChild(v_item);
                }

                if(v_onLastMessage) {
                    v_divChatRightContent.scrollTop = v_divChatRightContent.scrollHeight;
                }
                else {
                    if(v_firstVisibleMessageCode != null) {
                        for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                            if(v_divChatRightContent.childNodes[i].messageCode == v_firstVisibleMessageCode) {
                                v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                                break;
                            }
                        }
                    }
                }
            }

            if(p_data.message.user.code == v_user_id) {
                v_notify = false;
            }

            if(v_forceNotify || (v_notify && !v_group.silenced)) {
                var v_body = '';

                switch(p_data.message.type) {
                    case 1: { //Plain text
                        v_body = p_data.message.rawContent;
                        break;
                    }
                    case 2: { //Pasted image
                        v_body = 'Image Upload';
                        break;
                    }
                    case 3: { //Snippet
                        v_body = 'New Snippet';
                        break;
                    }
                    case 4: { //Attachment
                        v_body = 'File Upload';
                        break;
                    }
                    case 5: { //Mention
                        v_body = p_data.message.rawContent;
                        break;
                    }
                }

                new Notification(
                    p_data.message.user.login + ': ',
                    {
                        icon: '/static/OmniDB_app/images/omnidb.ico',
                        body: v_body
                    }
                );
            }
        }

        v_chatPopUp.tag.updateHeader();
    }

    if(p_context != null && (p_data.message.type == 2 || p_data.message.type == 4)) {//Pasted image or Attachment
        if(p_context.progressBar != null) {
            p_context.progressBar.lastChild.innerHTML = 'Uploading and processing of ' + p_data.message.title + ' finished!';

            setTimeout(
                function(p_progressBar) {
                    if(p_progressBar != null) {
                        p_progressBar.remove();
                    }
                }.bind(null, p_context.progressBar),
                3000
            );
        }
    }
}

/**
 * Handles retrieved group history message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {groupCode, messageList, fromMessageCode}.
 */
function chatRetrievedGroupHistory(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            for(var i = 0; i < p_data.messageList.length; i++) {
                v_group.messageList.push(p_data.messageList[i]);
            }

            if(p_data.fromMessageCode != null) {
                v_chatPopUp.tag.renderGroup(v_group.code, p_data.fromMessageCode, true);
            }
            else {
                v_chatPopUp.tag.renderGroup(v_group.code, null, true);
            }
        }
    }

    FX.fadeOut(
        document.getElementById('div_history'),
        {
            duration: 1000,
            complete: function() {
                document.getElementById('div_history').style.display = '';
            }
        }
    );
}

/**
 * Handles marked group messages as read message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {groupCode, messageCodeList}.
 */
function chatMarkedGroupMessagesAsRead(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            for(var i = 0; i < p_data.messageCodeList.length; i++) {
                var v_message = v_group.messageList.getMessageByCode(p_data.messageCodeList[i]);

                if(v_message != null) {
                    v_message.viewed = true;
                }
            }

            var v_unreadCount = 0;

            for(var i = 0; i < v_group.messageList.length; i++) {
                if(!v_group.messageList[i].viewed) {
                    v_unreadCount++;
                }
            }

            var v_groupElementList = document.querySelectorAll('#div_chat_groups > .div_chat_left_content > .div_chat_left_content_item');

            for(var i = 0; i < v_groupElementList.length; i++) {
                if(v_groupElementList[i].groupCode == v_group.code) {
                    v_groupElementList[i].lastChild.innerHTML = v_unreadCount;

                    if(v_unreadCount > 0) {
                        if(!v_groupElementList[i].classList.contains('div_chat_left_content_item_unread')) {
	                        v_groupElementList[i].classList.add('div_chat_left_content_item_unread');
                        }

	                    v_groupElementList[i].lastChild.classList.remove('badge_hidden');
	                }
                    else {
                        v_groupElementList[i].classList.remove('div_chat_left_content_item_unread');

                        if(!v_groupElementList[i].lastChild.classList.contains('badge_hidden')) {
                            v_groupElementList[i].lastChild.classList.add('badge_hidden');
                        }
                    }

                    break;
                }
            }
        }

        v_chatPopUp.tag.updateHeader();
    }
}

/**
 * Handles user status message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {userCode, userStatus}.
 */
function chatUserStatus(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_index = v_chatPopUp.tag.onlineUserCodeList.indexOf(p_data.userCode);

        if(p_data.userStatus == 'online') {
            if(v_index == -1) {
                v_chatPopUp.tag.onlineUserCodeList.push(p_data.userCode);
            }
        }
        else {
            if(v_index != -1) {
                v_chatPopUp.tag.onlineUserCodeList.splice(v_index, 1);
            }
        }

        var v_groupElementList = document.querySelectorAll('#div_chat_groups > .div_chat_left_content > .div_chat_left_content_item');

        for(var i = 0; i < v_groupElementList.length; i++) {
            if(v_groupElementList[i].userCode == p_data.userCode) {
                v_groupElementList[i].firstChild.src = '/static/OmniDB_app/images/icons/status_chat_' + p_data.userStatus + '.png';
                break;
            }
        }

        var v_imgRightPreHeader = document.getElementById('img_chat_right_pre_header_icon');

        if(v_imgRightPreHeader != null && v_imgRightPreHeader.userCode == p_data.userCode) {
            v_imgRightPreHeader.src = '/static/OmniDB_app/images/icons/status_chat_' + p_data.userStatus + '.png';
        }
    }
}

/**
 * Handles group user writing message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {groupCode, userCode, userWriting}.
 */
function chatGroupUserWriting(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_groupElementList = document.querySelectorAll('#div_chat_groups > .div_chat_left_content > .div_chat_left_content_item');

        for(var i = 0; i < v_groupElementList.length; i++) {
            if(v_groupElementList[i].groupCode == p_data.groupCode && v_groupElementList[i].userCode == p_data.userCode) {
                if(p_data.userWriting) {
                    v_groupElementList[i].firstChild.src = '/static/OmniDB_app/images/icons/status_chat_typing.png';
                }
                else {
                    if(v_chatPopUp.tag.onlineUserCodeList.indexOf(p_data.userCode) == -1) {
		                v_groupElementList[i].firstChild.src = '/static/OmniDB_app/images/icons/status_chat_offline.png';
		            }
                    else {
                        v_groupElementList[i].firstChild.src = '/static/OmniDB_app/images/icons/status_chat_online.png';
                    }
                }

                break;
            }
        }
    }
}

/**
 * Handles group silence settings received from the server.
 * @param {object} p_data - The message received from the server. Structure: {groupCode, groupSilenced}.
 */
function chatGroupSilenceSettings(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            v_group.silenced = p_data.groupSilenced;
        }
    }
}

/**
 * Handles removed group message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {groupCode, messageCode}.
 */
function chatRemovedGroupMessage(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            v_group.messageList.removeMessageByCode(p_data.messageCode);

            if(v_chatPopUp.tag.renderedType == 2 && v_chatPopUp.tag.renderedGroup == v_group.code) {//If the rendered type is group and this group are the rendered one.
                var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

                for(var i = 0; i < v_divChatRightContent.children.length; i++) {
                    if(v_divChatRightContent.children[i].messageCode == p_data.messageCode) {
                        var v_removeDate = false;

                        if(i > 0 && i == v_divChatRightContent.children.length - 1) {
                            if(v_divChatRightContent.children[i - 1].classList.contains('h2_side_lines_container')) {
                                v_removeDate = true;
                            }
                        }
                        else if(i > 0 && (i + 1) < v_divChatRightContent.children.length) {
                            if(v_divChatRightContent.children[i - 1].classList.contains('h2_side_lines_container') && v_divChatRightContent.children[i + 1].classList.contains('h2_side_lines_container')) {
                                v_removeDate = true;
                            }
                        }

                        v_divChatRightContent.children[i].remove();

                        if(v_removeDate) {
                            v_divChatRightContent.children[i - 1].remove();
                        }

                        break;
                    }
                }
            }
        }

        v_chatPopUp.tag.updateHeader();
    }
}

 /**
 * Handles updated group snippet messsage message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {snippetTitle, snippetContent, snippetMode, messageCode, groupCode, updatedAt}.
 */
function chatUpdatedGroupSnippetMessage(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            var v_message = v_group.messageList.getMessageByCode(p_data.messageCode);

            if(v_message != null) {
                v_message.title = p_data.snippetTitle;
                v_message.snippetMode = p_data.snippetMode;
                v_message.content = p_data.snippetContent;
                v_message.updatedAt = p_data.updatedAt;

                if(v_chatPopUp.tag.renderedType == 2 && v_chatPopUp.tag.renderedGroup == v_group.code) {//If the rendered type is group and this group are the rendered one.
                    var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

                    for(var i = 0; i < v_divChatRightContent.children.length; i++) {
                        if(v_divChatRightContent.children[i].messageCode == v_message.code) {
                            v_divChatRightContent.children[i].querySelector('.div_chat_message_snippet_container > div').innerHTML = v_message.title;
                            break;
                        }
                    }
	            }
            }
        }
    }
}

/**
* Handles updated group messsage message received from the server.
* @param {object} p_data - The message received from the server. Structure: {messageContent, messageRawContent, messageCode, groupCode}.
*/
function chatUpdatedGroupMessage(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.groupCode);

        if(v_group != null) {
            var v_message = v_group.messageList.getMessageByCode(p_data.messageCode);

            if(v_message != null) {
                v_message.content = p_data.messageContent;
                v_message.rawContent = p_data.messageRawContent;
                v_message.updatedAt = p_data.updatedAt;

                if(v_chatPopUp.tag.renderedType == 2 && v_chatPopUp.tag.renderedGroup == v_group.code) {//If the rendered type is group and this group are the rendered one.
                    var v_divChatRightContent = document.getElementById('div_chat_right_left_content');
                    var v_toUpdate = null;

                    for(var i = 0; i < v_divChatRightContent.children.length; i++) {
                        if(v_divChatRightContent.children[i].messageCode == v_message.code) {
                            v_toUpdate = v_divChatRightContent.children[i];
                            break;
                        }
                    }

                    if(v_toUpdate != null) {
                        var v_item = v_chatPopUp.tag.getRenderedGroupMessage(v_group.code, v_message, v_toUpdate.querySelector('.img_chat_user') != null);
                        v_divChatRightContent.insertBefore(v_item, v_toUpdate);
                        v_toUpdate.remove();
                    }
                }
            }
        }
    }
}

/**
 * Handles new channel message message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channelCode, message}.
 * @param {object} p_context - some useful javascript object that can be used for controls.
 */
function chatNewChannelMessage(p_data, p_context) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

        if(v_channel != null) {
            v_channel.messageList.splice(0, 0, p_data.message);

            var v_unreadCount = 0;

            for(var i = 0; i < v_channel.messageList.length; i++) {
                if(!v_channel.messageList[i].viewed) {
                    v_unreadCount++;
                }
            }

            var v_channelElementList = document.querySelectorAll('#div_chat_channels > .div_chat_left_content > .div_chat_left_content_item');

            for(var i = 0; i < v_channelElementList.length; i++) {
                if(v_channelElementList[i].channelCode == v_channel.code) {
                    v_channelElementList[i].lastChild.innerHTML = v_unreadCount;

                    if(v_unreadCount > 0) {
                        if(!v_channelElementList[i].classList.contains('div_chat_left_content_item_unread')) {
                            v_channelElementList[i].classList.add('div_chat_left_content_item_unread');
                        }

                        v_channelElementList[i].lastChild.classList.remove('badge_hidden');
                    }
                    else {
                        v_channelElementList[i].classList.remove('div_chat_left_content_item_unread');

                        if(!v_channelElementList[i].lastChild.classList.contains('badge_hidden')) {
                            v_channelElementList[i].lastChild.classList.add('badge_hidden');
                        }
                    }

                    break;
                }
            }

            var v_forceNotify = (p_data.message.content.indexOf('<span class="span_notify_user">@' + v_user_login + '</span>') != -1) || (!v_channel.silenced && document.hidden);

            var v_notify = true;

            if(v_chatPopUp.tag.renderedType == 1 && v_chatPopUp.tag.renderedChannel == v_channel.code) {//If the rendered type is channel and this channel are the rendered one.
                var v_divChatRightContent = document.getElementById('div_chat_right_left_content');
                var v_onLastMessage = false;
                var v_firstVisibleMessageCode = null;

                if((v_divChatRightContent.offsetHeight + v_divChatRightContent.scrollTop + 1) >= v_divChatRightContent.scrollHeight) {//If scroll was at max allowed
                    v_onLastMessage = true;
                    v_notify = false;
                }
                else {
                    for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                        if(v_divChatRightContent.childNodes[i].offsetTop >= v_divChatRightContent.scrollTop) {
                            v_firstVisibleMessageCode = v_divChatRightContent.childNodes[i].messageCode;
                            break;
                        }
                    }
                }

                if(v_divChatRightContent.children.length > 0) {
                    if(v_divChatRightContent.children[v_divChatRightContent.children.length - 1].title.substring(0, 10) != p_data.message.createdAt.substring(0, 10)) {
                        var v_h2SideLinesContainer = document.createElement('h2');
                        v_h2SideLinesContainer.classList.add('h2_side_lines_container');

                        var v_spanSideLinesContent = document.createElement('span');
                        v_spanSideLinesContent.classList.add('span_side_lines_content');
                        v_spanSideLinesContent.innerHTML = p_data.message.createdAt.substring(0, 10);
                        v_h2SideLinesContainer.appendChild(v_spanSideLinesContent);

                        v_divChatRightContent.appendChild(v_h2SideLinesContainer);
                    }

                    var v_item = v_chatPopUp.tag.getRenderedChannelMessage(v_channel.code, p_data.message, v_divChatRightContent.children[v_divChatRightContent.children.length - 1].userCode != p_data.message.user.code);
                    v_divChatRightContent.appendChild(v_item);
                }
                else {
                    var v_item = v_chatPopUp.tag.getRenderedChannelMessage(v_channel.code, p_data.message, true);
                    v_divChatRightContent.appendChild(v_item);
                }

                if(v_onLastMessage) {
                    v_divChatRightContent.scrollTop = v_divChatRightContent.scrollHeight;
                }
                else {
                    if(v_firstVisibleMessageCode != null) {
                        for(var i = 0; i < v_divChatRightContent.childNodes.length; i++) {
                            if(v_divChatRightContent.childNodes[i].messageCode == v_firstVisibleMessageCode) {
                                v_divChatRightContent.scrollTop = v_divChatRightContent.childNodes[i].offsetTop;
                                break;
                            }
                        }
                    }
                }
            }

            if(p_data.message.user.code == v_user_id) {
                v_notify = false;
            }

            if(v_forceNotify || (v_notify && !v_channel.silenced)) {
                var v_body = '';

                switch(p_data.message.type) {
                    case 1: { //Plain text
                        v_body = p_data.message.rawContent;
                        break;
                    }
                    case 2: { //Pasted image
                        v_body = 'Image Upload';
                        break;
                    }
                    case 3: { //Snippet
                        v_body = 'New Snippet';
                        break;
                    }
                    case 4: { //Attachment
                        v_body = 'File Upload';
                        break;
                    }
                    case 5: { //Mention
                        v_body = p_data.message.rawContent;
                        break;
                    }
                }

                new Notification(
                    v_channel.name + ' (' + p_data.message.user.login + ') : ',
                    {
                        icon: '/static/OmniDB_app/images/omnidb.ico',
                        body: v_body
                    }
                );
            }
        }

        v_chatPopUp.tag.updateHeader();
    }

    if(p_context != null && (p_data.message.type == 2 || p_data.message.type == 4)) {//Pasted image or Attachment
        if(p_context.progressBar != null) {
            p_context.progressBar.lastChild.innerHTML = 'Uploading and Processing of ' + p_data.message.title + ' finished!';

            setTimeout(
                function(p_progressBar) {
                    if(p_progressBar != null) {
                        p_progressBar.remove();
                    }
                }.bind(null, p_context.progressBar),
                3000
            );
        }
    }
}

/**
 * Handles retrieved channel history message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channelCode, messageList, fromMessageCode}.
 */
function chatRetrievedChannelHistory(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

        if(v_channel != null) {
            for(var i = 0; i < p_data.messageList.length; i++) {
                v_channel.messageList.push(p_data.messageList[i]);
            }

            if(p_data.fromMessageCode != null) {
                v_chatPopUp.tag.renderChannel(v_channel.code, p_data.fromMessageCode, true);
            }
            else {
                v_chatPopUp.tag.renderChannel(v_channel.code, null, true);
            }
        }
    }

    FX.fadeOut(
        document.getElementById('div_history'),
        {
            duration: 1000,
            complete: function() {
                document.getElementById('div_history').style.display = '';
            }
        }
    );
}

/**
 * Handles marked channel messages as read message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channelCode, messageCodeList}.
 */
function chatMarkedChannelMessagesAsRead(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

        if(v_channel != null) {
            for(var i = 0; i < p_data.messageCodeList.length; i++) {
                var v_message = v_channel.messageList.getMessageByCode(p_data.messageCodeList[i]);

                if(v_message != null) {
                    v_message.viewed = true;
                }
            }

            var v_unreadCount = 0;

            for(var i = 0; i < v_channel.messageList.length; i++) {
                if(!v_channel.messageList[i].viewed) {
                    v_unreadCount++;
                }
            }

            var v_channelElementList = document.querySelectorAll('#div_chat_channels > .div_chat_left_content > .div_chat_left_content_item');

            for(var i = 0; i < v_channelElementList.length; i++) {
                if(v_channelElementList[i].channelCode == v_channel.code) {
                    v_channelElementList[i].lastChild.innerHTML = v_unreadCount;

                    if(v_unreadCount > 0) {
                        if(!v_channelElementList[i].classList.contains('div_chat_left_content_item_unread')) {
	                        v_channelElementList[i].classList.add('div_chat_left_content_item_unread');
                        }

	                    v_channelElementList[i].lastChild.classList.remove('badge_hidden');
	                }
                    else {
                        v_channelElementList[i].classList.remove('div_chat_left_content_item_unread');

                        if(!v_channelElementList[i].lastChild.classList.contains('badge_hidden')) {
                            v_channelElementList[i].lastChild.classList.add('badge_hidden');
                        }
                    }

                    break;
                }
            }
        }

        v_chatPopUp.tag.updateHeader();
    }
}

/**
 * Handles channel user writing message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channelCode, userCode, userWriting}.
 */
function chatChannelUserWriting(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

        if(v_channel != null) {
            if(v_channel.usersWriting == null) {
                v_channel.usersWriting = [];
            }

            var v_indexOf = v_channel.usersWriting.indexOf(p_data.userCode);

            if(p_data.userWriting) {
                if(v_indexOf == -1) {
                    v_channel.usersWriting.push(p_data.userCode)
                }
            }
            else {
                if(v_indexOf != -1) {
                    v_channel.usersWriting.splice(v_indexOf, 1);
                }
            }

            var v_channelElementList = document.querySelectorAll('#div_chat_channels > .div_chat_left_content > .div_chat_left_content_item');
            var v_channelElement = null;

            for(var i = 0; i < v_channelElementList.length; i++) {
                if(v_channelElementList[i].channelCode == p_data.channelCode) {
                    v_channelElement = v_channelElementList[i];
                    break;
                }
            }

            if(v_channelElement != null) {
                if((v_channel.usersWriting.length == 1 && v_channel.usersWriting[0] != v_user_id) || v_channel.usersWriting.length > 1) {
                    v_channelElement.firstChild.src = '/static/OmniDB_app/images/icons/status_chat_typing.png';
                }
                else {
                    if(v_channel.private) {
                        v_channelElement.firstChild.src = '/static/OmniDB_app/images/icons/status_chat_privatechannel.png';
                    }
                    else {
                        v_channelElement.firstChild.src = '/static/OmniDB_app/images/icons/status_chat_channel.png';
                    }
                }
            }
        }
    }
}

/**
 * Handles channel silence settings received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channelCode, channelSilenced}.
 */
function chatChannelSilenceSettings(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

        if(v_channel != null) {
            v_channel.silenced = p_data.channelSilenced;
        }
    }
}

/**
 * Handles removed channel message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channelCode, messageCode}.
 */
function chatRemovedChannelMessage(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

        if(v_channel != null) {
            v_channel.messageList.removeMessageByCode(p_data.messageCode);

            if(v_chatPopUp.tag.renderedType == 1 && v_chatPopUp.tag.renderedChannel == v_channel.code) {//If the rendered type is channel and this channel are the rendered one.
                var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

                for(var i = 0; i < v_divChatRightContent.children.length; i++) {
                    if(v_divChatRightContent.children[i].messageCode == p_data.messageCode) {
                        var v_removeDate = false;

                        if(i > 0 && i == v_divChatRightContent.children.length - 1) {
                            if(v_divChatRightContent.children[i - 1].classList.contains('h2_side_lines_container')) {
                                v_removeDate = true;
                            }
                        }
                        else if(i > 0 && (i + 1) < v_divChatRightContent.children.length) {
                            if(v_divChatRightContent.children[i - 1].classList.contains('h2_side_lines_container') && v_divChatRightContent.children[i + 1].classList.contains('h2_side_lines_container')) {
                                v_removeDate = true;
                            }
                        }

                        v_divChatRightContent.children[i].remove();

                        if(v_removeDate) {
                            v_divChatRightContent.children[i - 1].remove();
                        }

                        break;
                    }
                }
            }
        }

        v_chatPopUp.tag.updateHeader();
    }
}

/**
* Handles updated channel snippet messsage message received from the server.
* @param {object} p_data - The message received from the server. Structure: {snippetTitle, snippetContent, snippetMode, messageCode, channelCode, updatedAt}.
*/
function chatUpdatedChannelSnippetMessage(p_data) {
   var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

   if(v_chatPopUp != null) {
       var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

       if(v_channel != null) {
           var v_message = v_channel.messageList.getMessageByCode(p_data.messageCode);

           if(v_message != null) {
               v_message.title = p_data.snippetTitle;
               v_message.snippetMode = p_data.snippetMode;
               v_message.content = p_data.snippetContent;
               v_message.updatedAt = p_data.updatedAt;

               if(v_chatPopUp.tag.renderedType == 1 && v_chatPopUp.tag.renderedChannel == v_channel.code) {//If the rendered type is channel and this channel are the rendered one.
                   var v_divChatRightContent = document.getElementById('div_chat_right_left_content');

                   for(var i = 0; i < v_divChatRightContent.children.length; i++) {
                       if(v_divChatRightContent.children[i].messageCode == v_message.code) {
                           v_divChatRightContent.children[i].querySelector('.div_chat_message_snippet_container > div').innerHTML = v_message.title;
                           break;
                       }
                   }
               }
           }
       }
   }
}

/**
* Handles updated channel messsage message received from the server.
* @param {object} p_data - The message received from the server. Structure: {messageContent, messageRawContent, messageCode, channelCode}.
*/
function chatUpdatedChannelMessage(p_data) {
   var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

   if(v_chatPopUp != null) {
       var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

       if(v_channel != null) {
           var v_message = v_channel.messageList.getMessageByCode(p_data.messageCode);

           if(v_message != null) {
               v_message.content = p_data.messageContent;
               v_message.rawContent = p_data.messageRawContent;
               v_message.updatedAt = p_data.updatedAt;

               if(v_chatPopUp.tag.renderedType == 1 && v_chatPopUp.tag.renderedChannel == v_channel.code) {//If the rendered type is channel and this channel are the rendered one.
                   var v_divChatRightContent = document.getElementById('div_chat_right_left_content');
                   var v_toUpdate = null;

                   for(var i = 0; i < v_divChatRightContent.children.length; i++) {
                       if(v_divChatRightContent.children[i].messageCode == v_message.code) {
                           v_toUpdate = v_divChatRightContent.children[i];
                           break;
                       }
                   }

                   if(v_toUpdate != null) {
                       var v_item = v_chatPopUp.tag.getRenderedChannelMessage(v_channel.code, v_message, v_toUpdate.querySelector('.img_chat_user') != null);
                       v_divChatRightContent.insertBefore(v_item, v_toUpdate);
                       v_toUpdate.remove();
                   }
               }
           }
       }
   }
}

/**
 * Handles new private channel message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channel}.
 * @param {object} p_context - some useful javascript object that can be used for controls.
 */
function chatNewPrivateChannel(p_data, p_context) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        v_chatPopUp.tag.channelList.push(p_data.channel);
        v_chatPopUp.tag.renderChannelItem(p_data.channel);

        v_chatPopUp.tag.contextList.push({
            type: 1, //Channel
            code: p_data.channel.code,
            text: '',
            scrollTop: 0,
            firstRender: true
        });

        if(p_context != null && p_context.userCode == v_user_id) {
            v_chatPopUp.tag.renderChannel(p_data.channel.code, null, false);
        }
    }
}

/**
* Handles renamed private channel message received from the server.
* @param {object} p_data - The message received from the server. Structure: {channelCode, channelName}.
*/
function chatRenamedPrivateChannel(p_data) {
   var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

   if(v_chatPopUp != null) {
       var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);

       if(v_channel != null) {
           v_channel.name = p_data.channelName;
       }

       var v_channelItems = document.querySelectorAll('#div_chat_channels .div_chat_left_content_item');

       for(var i = 0; i < v_channelItems.length; i++) {
           if(v_channelItems[i].channelCode == p_data.channelCode) {
               v_channelItems[i].childNodes[1].textContent = p_data.channelName;
               v_channelItems[i].name = p_data.channelName.toLowerCase();
               break;
           }
       }

       //Sort channels by name
       var v_channelsContent = document.querySelector('#div_chat_channels > .div_chat_left_content');
       var v_itemsArray = [];

       for(var i = 0; i < v_channelsContent.children.length; i++) {
           v_itemsArray.push(v_channelsContent.children[i]);
       }

       v_itemsArray.sort(
           function(a, b) {
               return ((a.innerHTML == b.innerHTML) ? 0 : ((a.innerHTML > b.innerHTML) ? 1 : -1));
           }
       );

       for(var i = 0; i < v_itemsArray.length; i++) {
           v_channelsContent.appendChild(v_itemsArray[i]);
       }
   }
}

/**
* Handles quitted private channel message received from the server.
* @param {object} p_data - The message received from the server. Structure: {channelCode, userCode}.
*/
function chatQuittedPrivateChannel(p_data) {
   var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

   if(v_chatPopUp != null) {
       var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channelCode);
       var v_indexOf = v_chatPopUp.tag.channelList.indexOf(v_channel);

       if(v_channel != null) {
           for(var i = 0; i < v_channel.userList.length; i++) {
               if(v_channel.userList[i].code == p_data.userCode) {
                   v_channel.userList.splice(i, 1);
               }
           }
       }

       if(p_data.userCode == v_user_id) {
           var v_channelItems = document.querySelectorAll('#div_chat_channels .div_chat_left_content_item');

           for(var i = 0; i < v_channelItems.length; i++) {
               if(v_channelItems[i].channelCode == p_data.channelCode) {
                   v_channelItems[i].remove();
                   break;
               }
           }

           if(v_indexOf != -1) {
               v_chatPopUp.tag.channelList.splice(v_indexOf, 1);
           }
       }
   }
}

/**
 * Handles invted private channel members message received from the server.
 * @param {object} p_data - The message received from the server. Structure: {channel}.
 */
function chatInvitedPrivateChannelMembers(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.channel.code);
        var v_indexOf = v_chatPopUp.tag.channelList.indexOf(v_channel);

        p_data.channel.messageList.getMessageByCode = function(p_messageCode) {
            for(var i = 0; i < this.length; i++) {
                if(this[i].code == p_messageCode) {
                    return this[i];
                }
            }

            return null;
        }

        p_data.channel.messageList.removeMessageByCode = function(p_messageCode) {
            for(var i = 0; i < this.length; i++) {
                if(this[i].code == p_messageCode) {
                    this.splice(i, 1);
                    return;
                }
            }
        }

        if(v_indexOf != -1) {
            v_chatPopUp.tag.channelList.splice(v_indexOf, 1, p_data.channel);
        }
        else {//Other users that just received this message
            v_chatPopUp.tag.channelList.push(p_data.channel);
            v_chatPopUp.tag.renderChannelItem(p_data.channel)

            v_chatPopUp.tag.contextList.push({
                type: 1, //Channel
                code: p_data.channel.code,
                text: '',
                scrollTop: 0,
                firstRender: true
            });
        }
    }
}

/**
 * Handles the pong message received from server.
 * @param {object} p_data - The message received from the server. Structure: {}.
 */
function chatPong(p_data) {
    if(v_chatPingTimeout != null) {
        clearTimeout(v_chatPingTimeout);

        if(v_chatPingInterval != null) {
            clearInterval(v_chatPingInterval);
        }

        v_chatPingInterval = setInterval(
            chatPing,
            30000
        );

        updateChatConnectionStatus('green', (v_chatReconnecting || (document.querySelectorAll('.qtip-websocket-connection').length > 0)));
    }
}

/**
 * Handles the user chat status message received from server.
 * @param {object} p_data - The message received from the server. Structure: {userCode, userChatStatus}.
 */
function chatUserChatStatus(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_user = v_chatPopUp.tag.userList.getUserByCode(p_data.userCode);

        if(v_user != null) {
            v_user.status = p_data.userChatStatus;

            var v_item = null;

            if(v_user.code == v_user_id) {
                v_item = document.getElementById('div_chat_user_info_login');
            }
            else {
                var v_groupItems = document.querySelectorAll('#div_chat_groups .div_chat_left_content_item');

                for(var i = 0; i < v_groupItems.length; i++) {
                    if(v_groupItems[i].userCode == v_user.code) {
                        v_item = v_groupItems[i];
                        break;
                    }
                }
            }

            var v_userStatus = v_item.querySelector('.img_user_status_icon');

            if(v_userStatus != null) {
                var v_style = v_chatPopUp.tag.getUserChatStatusStyle(v_user.code);

                if(v_style != null) {
                    v_userStatus.src = v_style.src;
                    v_userStatus.title = v_style.title;
                    v_userStatus.style.display = v_style.display;
                }
            }
        }
    }
}

/**
 * Handles the searched old messages message received from server.
 * @param {object} p_data - The message received from the server. Structure: {textPattern, messageList}.
 */
function chatSearchedOldMessages(p_data) {
    var v_chatPopUp = gv_chatPopUpControl.getChatPopUp();

    if(v_chatPopUp != null) {
        var v_divChatRightRight = document.getElementById('div_chat_right_right');
        v_divChatRightRight.classList.remove('display_hidden');

        var v_divChatRightRightContent = document.getElementById('div_chat_right_right_content');
        v_divChatRightRightContent.removeAttribute('style');
        v_divChatRightRightContent.innerHTML = '';

        if(p_data.messageList.length > 0) {//At least one match of search text
            v_divChatRightRightContent.style.alignItems = 'left';
            v_divChatRightRightContent.style.padding = '5px';
            v_divChatRightRightContent.innerHTML =
                '<p>' +
                '    ' + p_data.messageList.length + ' results for <b>' + p_data.textPattern + '</b>:' +
                '</p>' +
                '<div id="div_chat_searched_old_messages">' +
                '</div>';

            var v_divChatSearchedOldMessages = document.getElementById('div_chat_searched_old_messages');

            for(var i = 0; i < p_data.messageList.length; i++) {
                var v_item = document.createElement('div');
                v_item.messageCode = p_data.messageList[i].message.code;
                v_item.code = p_data.messageList[i].code;
                v_item.type = p_data.messageList[i].type;
                v_item.classList.add('div_chat_searched_old_messages_item');

                v_item.title = 'Click to jump to this message';

                var v_messageBody = document.createElement('div');
                v_messageBody.classList.add('div_chat_searched_old_messages_item_body');

                var v_messageContent = document.createElement('div');
                v_messageContent.classList.add('div_chat_searched_old_messages_item_content');
                v_messageContent.classList.add('div_chat_searched_old_messages_item_plain_text');
                v_messageContent.innerHTML = p_data.messageList[i].message.rawContent;
                v_messageBody.appendChild(v_messageContent);
                v_item.appendChild(v_messageBody);
                v_divChatSearchedOldMessages.appendChild(v_item);

                var v_datetime = '';

                if(p_data.messageList[i].message.createdAt != p_data.messageList[i].message.updatedAt) {//Message was edited
                    v_datetime = p_data.messageList[i].message.updatedAt.substring(0, 16);
                }
                else {
                    v_datetime = p_data.messageList[i].message.createdAt.substring(0, 16);
                }

                //Prepend message header 2
                var v_messageHeader2 = document.createElement('div');
                v_messageHeader2.innerHTML = p_data.messageList[i].message.user.login + ' <span class="span_chat_searched_old_messages_item_header2">' + v_datetime + '</span>';
                v_messageHeader2.classList.add('div_chat_searched_old_messages_item_header2');
                v_item.firstChild.insertBefore(v_messageHeader2, v_item.firstChild.firstChild);

                //Prepend message header 1
                var v_messageHeader1 = document.createElement('div');

                if(p_data.messageList[i].type == 1) { //Channel
                    var v_channel = v_chatPopUp.tag.channelList.getChannelByCode(p_data.messageList[i].code);

                    if(v_channel != null) {
                        v_messageHeader1.innerHTML = ' <span class="span_chat_searched_old_messages_item_header1">#' + v_channel.name + '</span>';
                    }
                }
                else if(p_data.messageList[i].type == 2) { //Group
                    var v_group = v_chatPopUp.tag.groupList.getGroupByCode(p_data.messageList[i].code);

                    if(v_group != null) {
                        for(var j = 0; j < v_group.userList.length; j++) {
                            if(v_group.userList[j].code != v_user_id) {
                                v_messageHeader1.innerHTML = ' <span class="span_chat_searched_old_messages_item_header1">@' + v_group.userList[j].login + '</span>';
                                break;
                            }
                        }
                    }
                }

                v_messageHeader1.classList.add('div_chat_searched_old_messages_item_header2');
                v_item.firstChild.insertBefore(v_messageHeader1, v_item.firstChild.firstChild);

                //Prepend user icon
                var v_userImg = document.createElement('img');
                v_userImg.src = "/static/OmniDB_app/images/omnidb.ico";
                v_userImg.classList.add('img_chat_user');
                v_item.insertBefore(v_userImg, v_item.firstChild);

                v_item.addEventListener(
                    'click',
                    function(p_chatPopUp, p_event) {
                        if(p_chatPopUp != null) {
                            if(this.type == 1) { //Channel
                                var v_channel = p_chatPopUp.tag.channelList.getChannelByCode(this.code);

                                if(v_channel != null) {
                                    var v_message = v_channel.messageList.getMessageByCode(this.messageCode);

                                    if(v_message != null) {
                                        p_chatPopUp.tag.renderChannel(v_channel.code, v_message.code, false);
                                    }
                                    else {
                                        var v_data = {
        	                                channelCode: v_channel.code,
        	                                offset: v_channel.messageList.length,
                                            fromMessageCode: this.messageCode
        	                            };

        	                            chatRetrieveChannelHistory(v_data);
                                    }
                                }
                            }
                            else if(this.type == 2) { //Group
                                var v_group = p_chatPopUp.tag.groupList.getGroupByCode(this.code);

                                if(v_group != null) {
                                    var v_message = v_group.messageList.getMessageByCode(this.messageCode);

                                    if(v_message != null) {
                                        p_chatPopUp.tag.renderGroup(v_group.code, v_message.code, false);
                                    }
                                    else {
                                        var v_data = {
        	                                groupCode: v_group.code,
        	                                offset: v_group.messageList.length,
                                            fromMessageCode: this.messageCode
        	                            };

        	                            chatRetrieveGroupHistory(v_data);
                                    }
                                }
                            }
                        }
                    }.bind(v_item, v_chatPopUp)
                )
            }
        }
        else {
            v_divChatRightRightContent.style.justifyContent = 'center';
            v_divChatRightRightContent.style.alignItems = 'center';
            v_divChatRightRightContent.innerHTML = 'No results for <b>' + p_data.textPattern + '</b>';
        }
    }
}
