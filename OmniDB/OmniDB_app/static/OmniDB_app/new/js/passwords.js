/// <summary>
/// Startup function.
/// </summary>
$(function () {

  $('#modal_password').on('hide.bs.modal', function (e) {
    if (v_modal_password_ok_clicked !=true && v_modal_password_cancel_callback!=null) {
      v_modal_password_cancel_callback();
    }
  })

  v_modal_password_ok_clicked = false;
  v_modal_password_cancel_callback = null;

});

function showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_message, p_send_tab_id = true) {
  v_modal_password_ok_clicked = false;
  v_modal_password_cancel_callback = p_cancel_callback_function;
  var v_content_div = document.getElementById('modal_password_content');
  var v_button_ok = document.getElementById('modal_password_ok');
  var v_button_cancel = document.getElementById('modal_password_cancel');
  var v_password_input = document.getElementById('txt_password_prompt');

  if (p_message)
    v_content_div.innerHTML = p_message;

  $('#modal_password').modal();

  v_button_ok.onclick = function() {
    v_modal_password_ok_clicked = true;
    checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id);
  }

  v_button_cancel.onclick = function() {
    if (p_cancel_callback_function)
      p_cancel_callback_function();
  }

  setTimeout(function() {
    v_password_input.focus();
    v_password_input.onkeydown = function(event) {
        if (event.keyCode == 13) {
            checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id);
            return false;
         }
    };
  },500);

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
	document.getElementById('modal_password_content').innerHTML = '';
  document.getElementById('txt_password_prompt').value = '';
}
