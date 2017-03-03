/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function() {


});

/// <summary>
/// Opens user config window.
/// </summary>
function showConfigUser() {

	document.getElementById('sel_editor_font_size').value = v_editor_font_size;
	document.getElementById('sel_editor_theme').value = v_theme_id;

	document.getElementById('txt_confirm_new_pwd').value = '';
	document.getElementById('txt_new_pwd').value = '';

	$('#div_config_user').show();

}

/// <summary>
/// Opens OmniDB about window.
/// </summary>
function showAbout() {

	$('#div_about').show();

}

/// <summary>
/// Hides user config window.
/// </summary>
function hideAbout() {

	$('#div_about').hide();

}

/// <summary>
/// Hides user config window.
/// </summary>
function hideConfigUser() {

	$('#div_config_user').hide();

}

/// <summary>
/// Saves user config to OmniDB database.
/// </summary>
function saveConfigUser() {

	v_editor_font_size = document.getElementById('sel_editor_font_size').value;
	v_theme_id = document.getElementById('sel_editor_theme').value;

	var v_confirm_pwd = document.getElementById('txt_confirm_new_pwd');
	var v_pwd = document.getElementById('txt_new_pwd');

	if ((v_confirm_pwd.value!='' || v_pwd.value!='') && (v_pwd.value!=v_confirm_pwd.value))
		showAlert('New Password and Confirm New Password fields do not match.');
	else {
		var input = JSON.stringify({"p_font_size" : v_editor_font_size, "p_theme" : v_theme_id, "p_pwd" : v_pwd.value});

		execAjax('MainDB.aspx/SaveConfigUser',
				input,
				function(p_return) {
					v_editor_theme = p_return.v_data.v_theme_name;
					v_theme_type = p_return.v_data.v_theme_type;
					$('#div_config_user').hide();
					showAlert('Configuration saved. Please, refresh the page for changes to take effect.');

				});
	}

}