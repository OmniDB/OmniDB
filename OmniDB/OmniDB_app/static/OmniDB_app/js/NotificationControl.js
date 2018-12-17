/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function checkSessionMessage() {

	execAjax('/check_session_message/',
				JSON.stringify({}),
        function(p_return) {
          if (p_return.v_data!='')
          	showAlert(p_return.v_data);
        },
        null,
    'box');

}

function showError(p_message) {
	document.getElementById('div_error_msg').innerHTML = '<img src="/static/OmniDB_app/images/error.png"/ style="display: block; margin-left: auto; margin-right: auto;"><br/>' + p_message;
	$('#div_error').addClass('isActive');
}

function hideError() {
	$('#div_error').removeClass('isActive');
	document.getElementById('div_error_msg').innerHTML = '';
}


function showAlert(p_info, p_funcYes = null)
{
	var v_div_text = document.createElement('div');
	v_div_text.className = 'div_alert_text';
	v_div_text.innerHTML = p_info;

	var v_div_buttons = document.createElement('div');
	v_div_buttons.className = 'div_alert_buttons';

	var v_button = document.createElement('button');
	v_button.innerHTML = 'Ok';
	v_button.onclick = function() {
		document.getElementById('div_alert_content').innerHTML = '';
		$('#div_alert').removeClass('isActive');
		if (p_funcYes!=null)
			p_funcYes();
	};

	v_div_buttons.appendChild(v_button);

	document.getElementById('div_alert_content').innerHTML = '';

	document.getElementById('div_alert_content').appendChild(v_div_text);
	document.getElementById('div_alert_content').appendChild(v_div_buttons);

	$('#div_alert').addClass('isActive');

	v_button.focus();
}


function clickConfirmCancel() {

        $('#div_alert').removeClass('isActive');

}

function showConfirm(p_info,p_funcYes,p_funcNo)
{
	var v_div_text = document.createElement('div');
	v_div_text.className = 'div_alert_text';
	v_div_text.innerHTML = p_info;

	var v_div_buttons = document.createElement('div');
	v_div_buttons.className = 'div_alert_buttons';

	var v_button_ok = document.createElement('button');
	v_button_ok.id = 'button_confirm_ok';
	v_button_ok.innerHTML = 'Ok';
	v_button_ok.onclick = function() {
		clickConfirmCancel();
		p_funcYes();
	};
	v_div_buttons.appendChild(v_button_ok);

	var v_button_cancel = document.createElement('button');
	v_button_cancel.id = 'button_confirm_cancel';
	v_button_cancel.innerHTML = 'Cancel';
	v_button_cancel.onclick = function() {
		clickConfirmCancel();
		if (p_funcNo)
			p_funcNo();
	};
	v_div_buttons.appendChild(v_button_cancel);

	document.getElementById('div_alert_content').innerHTML = '';

	document.getElementById('div_alert_content').appendChild(v_div_text);
	document.getElementById('div_alert_content').appendChild(v_div_buttons);

	$('#div_alert').addClass('isActive');

	v_button_ok.focus();

}

function showConfirm2(p_info,p_funcYes,p_funcNo)
{

	var v_div_text = document.createElement('div');
	v_div_text.className = 'div_alert_text';
	v_div_text.innerHTML = p_info;

	var v_div_buttons = document.createElement('div');
	v_div_buttons.className = 'div_alert_buttons';

	var v_button = document.createElement('button');
	v_button.innerHTML = 'Yes';
	v_button.onclick = function() {
		clickConfirmCancel();
		p_funcYes();
	};
	v_div_buttons.appendChild(v_button);

	v_button = document.createElement('button');
	v_button.innerHTML = 'No';
	v_button.onclick = function() {
		clickConfirmCancel();
		p_funcNo();
	};
	v_div_buttons.appendChild(v_button);

	v_button = document.createElement('button');
	v_button.innerHTML = 'Cancel';
	v_button.onclick = function() {
		clickConfirmCancel();
	};
	v_div_buttons.appendChild(v_button);

	document.getElementById('div_alert_content').innerHTML = '';

	document.getElementById('div_alert_content').appendChild(v_div_text);
	document.getElementById('div_alert_content').appendChild(v_div_buttons);

	$('#div_alert').addClass('isActive');

}

function showConfirm3(p_info,p_funcYes,p_funcNo)
{

	var v_div_text = document.createElement('div');
	v_div_text.className = 'div_alert_text';
	v_div_text.innerHTML = p_info;

	var v_div_buttons = document.createElement('div');
	v_div_buttons.className = 'div_alert_buttons';

	var v_button = document.createElement('button');
	v_button.innerHTML = 'Yes';
	v_button.onclick = function() {
		clickConfirmCancel();
		p_funcYes();
	};
	v_div_buttons.appendChild(v_button);

	v_button = document.createElement('button');
	v_button.innerHTML = 'No';
	v_button.onclick = function() {
		clickConfirmCancel();
		p_funcNo();
	};
	v_div_buttons.appendChild(v_button);

	document.getElementById('div_alert_content').innerHTML = '';

	document.getElementById('div_alert_content').appendChild(v_div_text);
	document.getElementById('div_alert_content').appendChild(v_div_buttons);

	$('#div_alert').addClass('isActive');

}
