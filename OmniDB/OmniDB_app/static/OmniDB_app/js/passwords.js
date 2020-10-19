/*
This file is part of OmniDB.
OmniDB is open-source software, distributed "AS IS" under the MIT license in the hope that it will be useful.

The MIT License (MIT)

Portions Copyright (c) 2015-2020, The OmniDB Team
Portions Copyright (c) 2017-2020, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function () {

  $('#modal_password').on('hidden.bs.modal', function (e) {
    if (v_modal_password_ok_clicked !=true && v_modal_password_cancel_callback!=null) {
      v_modal_password_cancel_callback();
    }
    else if(v_modal_password_ok_clicked == true && v_modal_password_ok_after_hide_function!=null) {
      v_modal_password_ok_after_hide_function();
    }
  });

  $('#modal_password').on('shown.bs.modal', function (e) {
    if (v_modal_password_input!=null) {
      v_modal_password_input.focus();
      v_modal_password_input.onkeydown = function(event) {
          if (event.keyCode == 13) {
              v_modal_password_ok_function();
              $('#modal_password').modal('hide');
           }
      };
    }
  });

  v_modal_password_ok_clicked = false;
  v_modal_password_ok_function = null;
  v_modal_password_ok_after_hide_function = null;
  v_modal_password_cancel_callback = null;
  v_modal_password_input = null;
});

function showPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_message, p_send_tab_id = true) {
  v_modal_password_ok_clicked = false;
  v_modal_password_cancel_callback = p_cancel_callback_function;
  var v_content_div = document.getElementById('modal_password_content');
  var v_button_ok = document.getElementById('modal_password_ok');
  var v_button_cancel = document.getElementById('modal_password_cancel');
  v_modal_password_input = document.getElementById('txt_password_prompt');

  if (p_message)
    v_content_div.innerHTML = p_message;

  $('#modal_password').modal();

  v_modal_password_ok_function = function() {
    v_modal_password_ok_clicked = true;
    checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id);
  }

  v_button_ok.onclick = v_modal_password_ok_function;

  v_button_cancel.onclick = function() {
    v_modal_password_ok_clicked = false;
    if (p_cancel_callback_function)
      p_cancel_callback_function();
  }

}

function checkPasswordPrompt(p_database_index, p_callback_function, p_cancel_callback_function, p_send_tab_id) {

  var v_password = document.getElementById('txt_password_prompt').value;
  var v_tab_id = '';
  if (p_send_tab_id)
    v_tab_id = v_connTabControl.selectedTab.id;

  v_modal_password_ok_after_hide_function = function() {
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
			'box'
    );
  }
}
