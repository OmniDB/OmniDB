function showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_message) {
    var v_html =
        '<h2>Password Expired</h2>' +
        '<img src="/static/OmniDB_app/images/keys.png"/>' +
        '<div id="div_password_prompt_msg" class="error_text" style="margin:20px 0px 20px 0px; padding: 0px 20px 0px 20px; max-height: 50px; overflow-y: auto;">' +
        '</div>' +
        '<div>' +
        '   <input id="txt_password_prompt" type="password" placeholder="Password" style="margin-bottom:20px; text-align: center;"/>' +
        '</div>' +
        '<div style="margin-bottom: 20px;">' +
        '   <button id="bt_password_prompt_ok">Ok</button>' +
        '   <button id="bt1_password_prompt_cancel">Cancel</button>' +
        '</div>';

    var v_popUp = v_popUpControl.getPopUpById('show_password_prompt');

	if(v_popUp != null) {
		v_popUp.turnActive();
		v_popUp.setContent(v_html);
	}
	else {
		var v_config = {
			width: '800px',
			height: '400px',
			resizable: true,
			draggable: true,
			top: (window.innerHeight - 400) / 2 + 'px',
			left: (window.innerWidth - 800) / 2 + 'px',
			forceClose: true
		};

		v_popUp = v_popUpControl.addPopUp(
			'show_password_prompt',
			'Connection Password',
			v_html,
			v_config,
			null
		);
	}

    if(p_message) {
        document.getElementById('div_password_prompt_msg').innerHTML = p_message;
    }

    var v_button = document.getElementById('bt_password_prompt_ok');

    if(v_button != null) {
        v_button.onclick = function() {
            checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function);
        }
    }

    var v_button1 = document.getElementById('bt1_password_prompt_cancel');

    if(v_button1 != null) {
        v_button1.onclick = function() {
            hidePasswordPrompt();

            if(p_cancel_callback_function) {
                p_cancel_callback_function();
            }
        }
    }

    var v_button2 = document.getElementById('bt2_password_prompt_cancel');

    if(v_button2 != null) {
        v_button2.onclick = function() {
            hidePasswordPrompt();

            if(p_cancel_callback_function) {
                p_cancel_callback_function();
            }
        }
    }

    document.getElementById('txt_password_prompt').focus();

    document.getElementById('txt_password_prompt').onkeydown = function(event) {
        if (event.keyCode == 13) {
            checkPasswordPrompt(p_database_index, p_callback_function);
            return false;
        }
    };
}

function checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function) {
    var v_password = document.getElementById('txt_password_prompt').value;
    hidePasswordPrompt();

    execAjax(
        '/renew_password/',
        JSON.stringify({
            "p_database_index": p_database_index,
            "p_password": v_password
        }),
        function(p_return) {
            if(p_callback_function) {
                p_callback_function();
            }
        },
        function(p_return) {
            showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_return.v_data);
        },
        'box'
    );
}

function hidePasswordPrompt() {
    var v_popUp = v_popUpControl.getPopUpById('show_password_prompt');

	if(v_popUp != null) {
		v_popUp.close(true);
	}
}
