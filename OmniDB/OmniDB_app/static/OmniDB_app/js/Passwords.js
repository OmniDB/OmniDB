function showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_message) {
  if (p_message)
    document.getElementById('div_password_prompt_msg').innerHTML = p_message;
	$('#div_password_prompt').show();

  document.getElementById('bt_password_prompt_ok').onclick = function() {
    checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function);
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
          checkPasswordPrompt(p_database_index, p_callback_function);
          return false;
       }
  };

}

function checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function) {

  var v_password = document.getElementById('txt_password_prompt').value;

  hidePasswordPrompt();

  execAjax('/renew_password/',
			JSON.stringify({"p_database_index": p_database_index,
                      "p_password": v_password}),
			function(p_return) {

        if (p_callback_function)
          p_callback_function();

			},
			function(p_return) {
        showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_return.v_data);
      },
			'box');

}

function hidePasswordPrompt() {
	$('#div_password_prompt').hide();
	document.getElementById('div_password_prompt_msg').innerHTML = '';
  document.getElementById('txt_password_prompt').value = '';
}
