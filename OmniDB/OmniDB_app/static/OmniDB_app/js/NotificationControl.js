/*
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

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
