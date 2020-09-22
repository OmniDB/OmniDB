
var v_client_id;


var v_context_object = {
  'contextCode': 0,
  'contextList': []
}

var v_polling_started = false;

/// <summary>
/// Startup function.
/// </summary>
$(function () {

  setInterval(function() {
    execAjax('/client_keep_alive/',
  			JSON.stringify({}),
  			function(p_return) {
  			},
  			null,
  			'box',
        false);

  },60000);
});

function call_polling(p_startup) {
  execAjax('/long_polling/',
			JSON.stringify({
        'p_startup': p_startup
      }),
			function(p_return) {
        for (var i=0; i<p_return.returning_rows.length; i++)
          polling_response(p_return.returning_rows[i]);
        call_polling(false);

			},
			null,
			'box',
      false);
}

$(window).on('beforeunload', function() {
  clear_client().then(function() {});
});

async function clear_client() {
  // Setting the token.
 	var csrftoken = getCookie('omnidb_csrftoken');
	// Requesting data with ajax.
 	const v_ajax_call = await $.ajax({
 		url: v_url_folder + '/clear_client',
 		data: null,
 		type: "get",
 		dataType: "json",
 		beforeSend: function(xhr, settings) {
 			if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
 				xhr.setRequestHeader("X-CSRFToken", csrftoken);
 			}
 		},
 		success: function(p_return) {
 		},
 		error: function(msg) {
 		}
 	});

  return v_ajax_call;
}

function polling_response(p_message) {
  var v_message = p_message;

  var p_context_code = null;
  var p_context = null;

  if (v_message.v_context_code!=0 && v_message.v_context_code!=null) {

    for (var i=0; i<v_context_object.contextList.length; i++) {

      if (v_context_object.contextList[i].code == v_message.v_context_code) {
        p_context = v_context_object.contextList[i].context;
        p_context_code = v_context_object.contextList[i].code;
        break;
      }
    }
  }

  switch(v_message.v_code) {
    case parseInt(v_queryResponseCodes.Pong): {
      websocketPong();
      break;
    }
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
    case parseInt(v_queryResponseCodes.TerminalResult): {
      if (p_context) {
        terminalReturn(v_message,p_context);
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
    case parseInt(v_queryResponseCodes.AdvancedObjectSearchResult): {
      if (p_context) {
        SetAcked(p_context);
        advancedObjectSearchReturn(v_message, p_context);
        //Remove context
        removeContext(v_queryWebSocket,p_context_code);
      }
      break;
    }
  }
}

function createContext(p_connection, p_context) {
	v_context_object.contextCode += 1;
	v_context_code = v_context_object.contextCode;
	p_context.v_context_code = v_context_code;
	var v_context = {
		code: v_context_code,
		context: p_context
	}
	v_context_object.contextList.push(v_context);
	return v_context;
}

function removeContext(p_context_code) {
	for (var i=0; i<v_context_object.contextList.length; i++) {
		if (v_context_object.contextList[i].code == p_context_code) {
			v_context_object.contextList.splice(i,1);
			break;
		}
	}
}

function createRequest(p_messageCode, p_messageData, p_context) {

  var v_context_code = 0;

	//Configuring context
	if (p_context!=null) {

		//Context code is passed
		if (p_context === parseInt(p_context, 10)) {
			v_context_code = p_context;
		}
		else {
			v_context_object.contextCode += 1;
			v_context_code = v_context_object.contextCode;
			p_context.v_context_code = v_context_code;
			var v_context = {
				code: v_context_code,
				context: p_context
			}
			v_context_object.contextList.push(v_context);
		}
	}

  execAjax('/create_request/',
			JSON.stringify({
        v_code: p_messageCode,
        v_context_code: v_context_code,
        v_data: p_messageData
      }),
			function(p_return) {
        if (!v_polling_started) {
          v_polling_started=true;
          call_polling(true);
        }
			},
			null,
			'box',
      false);
}
