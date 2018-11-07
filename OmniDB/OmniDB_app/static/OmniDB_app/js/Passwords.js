function showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_message, p_send_tab_id = true) {
  if (p_message)
    document.getElementById('div_password_prompt_msg').innerHTML = p_message;
	$('#div_password_prompt').addClass('isActive');

  document.getElementById('bt_password_prompt_ok').onclick = function() {
    checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id);
  }

  document.getElementById('bt1_password_prompt_cancel').onclick = function() {
    hidePasswordPrompt();
    if (p_cancel_callback_function)
      p_cancel_callback_function();
  }
  document.getElementById('bt2_password_prompt_cancel').onclick = function() {
    hidePasswordPrompt();
    if (p_cancel_callback_function)
      p_cancel_callback_function();
  }

  document.getElementById('txt_password_prompt').focus();
  document.getElementById('txt_password_prompt').onkeydown = function(event) {
      if (event.keyCode == 13) {
          checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id);
          return false;
       }
  };

}

function checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id) {

  var v_password = document.getElementById('txt_password_prompt').value;
  var v_tab_id = '';
  if (p_send_tab_id)
    v_tab_id = v_connTabControl.selectedTab.id;

  hidePasswordPrompt();

  execAjax('/renew_password/',
			JSON.stringify({"p_database_index": p_database_index,
                      "p_tab_id": v_tab_id,
                      "p_password": v_password}),
			function(p_return) {

        if (p_callback_function)
          p_callback_function();

			},
			function(p_return) {
        showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_return.v_data, p_send_tab_id);
      },
			'box');

}

function hidePasswordPrompt() {
	$('#div_password_prompt').removeClass('isActive');
	document.getElementById('div_password_prompt_msg').innerHTML = '';
  document.getElementById('txt_password_prompt').value = '';
}
