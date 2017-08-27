/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function checkSessionMessage() {
	execAjax(
		'/check_session_message/',
		JSON.stringify({}),
        function(p_return) {
        	if (p_return.v_data!='')
          	showAlert(p_return.v_data);
        },
        null,
    	'box'
	);
}

function showError(p_message) {
	var v_html =
        '<div id="div_error_msg" class="error_text" style="height:100%; width:100%; margin-top:20px; text-align: center;">' +
		'	<img src="/static/OmniDB_app/images/error.png"/ style="display: block; margin-left: auto; margin-right: auto;">' +
		'	<br/>' + p_message +
		'</div>';

	var v_popUp = v_popUpControl.getPopUpById('show_error');

	if(v_popUp != null) {
		v_popUp.turnActive();
		v_popUp.setContent(v_html);
	}
	else {
		var v_config = {
			width: window.innerWidth * 0.9 + 'px',
			height: window.innerHeight * 0.9 + 'px',
			resizable: true,
			draggable: true,
			top: window.innerHeight * 0.05 + 'px',
			left: window.innerWidth * 0.05 + 'px',
			forceClose: true
		};

		v_popUp = v_popUpControl.addPopUp(
			'show_error',
			'Error!',
			v_html,
			v_config,
			null
		);
	}
}

function hideError() {
	var v_popUp = v_popUpControl.getPopUpById('show_error');

	if(v_popUp != null) {
		v_popUp.close(true);
		return;
	}
}


function showAlert(p_info)
{
	var v_html =
		'<div style="height:100%; width:100%;">' +
		'    <div style="margin-top: unset; padding-top: 20px;" class="div_alert_text">' + p_info + '</div>' +
		'    <div style="position: unset;" class="div_alert_buttons">' +
		'        <button style="position: unset; margin-top: 20px; width: unset;" class="div_alert_buttons">Ok</button>' +
		'    </div>' +
		'</div>';

	var v_popUp = v_popUpControl.getPopUpById('show_alert');

	if(v_popUp != null) {
		v_popUp.turnActive();
		v_popUp.setContent(v_html);
	}
	else {
		var v_config = {
			width: '700px',
			height: '200px',
			resizable: true,
			draggable: true,
			top: (window.innerHeight - 200) / 2 + 'px',
			left: (window.innerWidth - 700) / 2 + 'px',
			forceClose: true
		};

		v_popUp = v_popUpControl.addPopUp(
			'show_alert',
			'Attention',
			v_html,
			v_config,
			null
		);
	}

	var v_button = v_popUp.contentElement.querySelector('button.div_alert_buttons');

	v_button.addEventListener(
		'click',
		function(p_popUp, p_event) {
			p_popUp.close(true);
		}.bind(v_button, v_popUp)
	)

	v_button.focus();
}

function showConfirm(p_info,p_funcYes)
{
	var v_html =
		'<div style="height:100%; width:100%;">' +
		'    <div style="margin-top: unset; padding-top: 20px;" class="div_alert_text">' + p_info + '</div>' +
		'    <div style="position: unset;" class="div_alert_buttons">' +
		'        <button style="position: unset; margin-top: 20px; width: unset;">Ok</button>' +
		'        <button style="position: unset; margin-top: 20px; width: unset;">Cancel</button>' +
		'    </div>' +
		'</div>';

	var v_popUp = v_popUpControl.getPopUpById('show_confirm');

	if(v_popUp != null) {
		v_popUp.turnActive();
		v_popUp.setContent(v_html);
	}
	else {
		var v_config = {
			width: '700px',
			height: '200px',
			resizable: true,
			draggable: true,
			top: (window.innerHeight - 200) / 2 + 'px',
			left: (window.innerWidth - 700) / 2 + 'px',
			forceClose: true
		};

		v_popUp = v_popUpControl.addPopUp(
			'show_confirm',
			'Attention',
			v_html,
			v_config,
			null
		);
	}

	var v_buttonList = v_popUp.contentElement.querySelectorAll('button');

	for(var i = 0; i < v_buttonList.length; i++) {
		if(v_buttonList[i].innerHTML == 'Ok') {
			v_buttonList[i].addEventListener(
				'click',
				function(p_popUp, p_callback, p_event) {
					p_popUp.close(true);
					p_callback();
				}.bind(v_buttonList[i], v_popUp, p_funcYes)
			)
		}
		else if(v_buttonList[i].innerHTML == 'Cancel') {
			v_buttonList[i].addEventListener(
				'click',
				function(p_popUp, _event) {
					p_popUp.close(true);
				}.bind(v_buttonList[i], v_popUp)
			)

			v_buttonList[i].focus();
		}
	}
}

function showConfirm2(p_info,p_funcYes,p_funcNo)
{
	var v_html =
		'<div style="height:100%; width:100%;">' +
		'    <div style="margin-top: unset; padding-top: 20px;" class="div_alert_text">' + p_info + '</div>' +
		'    <div style="position: unset;" class="div_alert_buttons">' +
		'        <button style="position: unset; margin-top: 20px; width: unset;">Yes</button>' +
		'        <button style="position: unset; margin-top: 20px; width: unset;">No</button>' +
		'        <button style="position: unset; margin-top: 20px; width: unset;">Cancel</button>' +
		'    </div>' +
		'</div>';

	var v_popUp = v_popUpControl.getPopUpById('show_confirm_2');

	if(v_popUp != null) {
		v_popUp.turnActive();
		v_popUp.setContent(v_html);
	}
	else {
		var v_config = {
			width: '700px',
			height: '200px',
			resizable: true,
			draggable: true,
			top: (window.innerHeight - 200) / 2 + 'px',
			left: (window.innerWidth - 700) / 2 + 'px',
			forceClose: true
		};

		v_popUp = v_popUpControl.addPopUp(
			'show_confirm_2',
			'Attention',
			v_html,
			v_config,
			null
		);
	}

	var v_buttonList = v_popUp.contentElement.querySelectorAll('button');

	for(var i = 0; i < v_buttonList.length; i++) {
		if(v_buttonList[i].innerHTML == 'Yes') {
			v_buttonList[i].addEventListener(
				'click',
				function(p_popUp, p_callback, p_event) {
					p_popUp.close(true);
					p_callback();
				}.bind(v_buttonList[i], v_popUp, p_funcYes)
			)
		}
		else if(v_buttonList[i].innerHTML == 'No') {
			v_buttonList[i].addEventListener(
				'click',
				function(p_popUp, p_callback, p_event) {
					p_popUp.close(true);
					p_callback();
				}.bind(v_buttonList[i], v_popUp, p_funcNo)
			)
		}
		else if(v_buttonList[i].innerHTML == 'Cancel') {
			v_buttonList[i].addEventListener(
				'click',
				function(p_popUp, _event) {
					p_popUp.close(true);
				}.bind(v_buttonList[i], v_popUp)
			)

			v_buttonList[i].focus();
		}
	}
}
