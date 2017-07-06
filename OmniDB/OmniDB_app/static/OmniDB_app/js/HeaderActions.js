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

	var v_fileref = document.createElement("link");
    v_fileref.setAttribute("rel", "stylesheet");
    v_fileref.setAttribute("type", "text/css");
    v_fileref.setAttribute("href", '/static/OmniDB_app/css/themes/' + v_theme_type + '.css');
    document.getElementsByTagName("head")[0].appendChild(v_fileref);

	var v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);


});

/// <summary>
/// Opens user config window.
/// </summary>
function showConfigUser() {

	document.getElementById('sel_editor_font_size').value = v_editor_font_size;
	document.getElementById('sel_editor_theme').value = v_theme_id;

	document.getElementById('txt_confirm_new_pwd').value = '';
	document.getElementById('txt_new_pwd').value = '';

	document.getElementById('chk_enable_chat').checked = ((v_enable_omnichat == 1) ? true : false);

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

	v_enable_omnichat = ((document.getElementById('chk_enable_chat').checked == true) ? 1 : 0);

	if ((v_confirm_pwd.value!='' || v_pwd.value!='') && (v_pwd.value!=v_confirm_pwd.value))
		showAlert('New Password and Confirm New Password fields do not match.');
	else {
		var input = JSON.stringify({"p_font_size" : v_editor_font_size, "p_theme" : v_theme_id, "p_pwd" : v_pwd.value, "p_chat_enabled": v_enable_omnichat});

		execAjax('/save_config_user/',
				input,
				function(p_return) {
					v_editor_theme = p_return.v_data.v_theme_name;
					v_theme_type = p_return.v_data.v_theme_type;
					$('#div_config_user').hide();
					showAlert('Configuration saved. Please, refresh the page for changes to take effect.');

				});
	}
}

/// <summary>
/// Hides command history window.
/// </summary>
function hideCommandList() {

	$('#div_command_list').hide();

	v_commandListObject.ht.destroy();

	document.getElementById('div_command_list_data').innerHTML = '';

}

/// <summary>
/// Wipes command history.
/// </summary>
function deleteCommandList() {

	showConfirm('Are you sure you want to clear command history?',
				function() {

					execAjax('/clear_command_list/',
					JSON.stringify({}),
					function(p_return) {

						hideCommandList();

					});

				});

}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function showCommandList() {

	execAjax('/get_command_list/',
			JSON.stringify({}),
			function(p_return) {

				$('#div_command_list').show();

				var v_height  = window.innerHeight - $('#div_command_list_data').offset().top - 60;
				document.getElementById('div_command_list_data').style.height = v_height + "px";

				var columnProperties = [];

				var col = new Object();
				col.title =  'Date';
				col.readOnly = true;
				col.width = 200;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Command';
				col.readOnly = true;
				col.width = 400;
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_command_list_data');

				if (v_div_result.innerHTML!='')
					v_commandListObject.ht.destroy();

				v_commandListObject = new Object();

				var container = v_div_result;
				v_commandListObject.ht = new Handsontable(container,
														{
															data: p_return.v_data,
															columns : columnProperties,
															colHeaders : true,
															rowHeaders : true,
															copyRowsLimit : 1000000000,
															copyColsLimit : 1000000000,
															manualColumnResize: true,
															contextMenu: {
																callback: function (key, options) {

																	if (key === 'view_data') {
																	  	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),false);
																	}

																},
																items: {
																	"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"/static/OmniDB_app/images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
																}
														    },
														    cells: function (row, col, prop) {

															    var cellProperties = {};
															    if (row % 2 == 0)
																		cellProperties.renderer = blueRenderer;
																	else
																		cellProperties.renderer = whiteRenderer;
															    return cellProperties;

															}
														});

			},
			null,
			'box');

}

/// <summary>
/// Displays edit cell window.
/// </summary>
/// <param name="p_ht">Handsontable object.</param>
/// <param name="p_row">Row number.</param>
/// <param name="p_col">Column number.</param>
/// <param name="p_content">Cell content.</param>
/// <param name="p_can_alter">If ready only or not.</param>
function editCellData(p_ht, p_row, p_col, p_content, p_can_alter) {

	v_canEditContent = p_can_alter;

	if (v_editContentObject!=null)
		if (v_editContentObject.editor!=null) {
			 v_editContentObject.editor.destroy();
			 document.getElementById('txt_edit_content').innerHTML = '';
		}

	var langTools = ace.require("ace/ext/language_tools");
	var v_editor = ace.edit('txt_edit_content');
	v_editor.setTheme("ace/theme/" + v_editor_theme);
	v_editor.session.setMode("ace/mode/text");

	v_editor.setFontSize(Number(v_editor_font_size));

	v_editor.setOptions({enableBasicAutocompletion: true});

	document.getElementById('txt_edit_content').onclick = function() {
  		v_editor.focus();
    };

    var command = {
		name: "replace",
		bindKey: {
		      mac: v_keybind_object.v_replace_mac,
		      win: v_keybind_object.v_replace
		    },
		exec: function(){
			v_copyPasteObject.v_tabControl.selectTabIndex(0);
			showFindReplace(v_editor);
		}
	}

	v_editor.commands.addCommand(command);

	if (p_content!=null)
		v_editor.setValue(p_content);
	else
		v_editor.setValue('');

	v_editor.clearSelection();

	if (p_can_alter)
		v_editor.setReadOnly(false);
	else
		v_editor.setReadOnly(true);

	v_editContentObject = new Object();
	v_editContentObject.editor = v_editor;
	v_editContentObject.row = p_row;
	v_editContentObject.col = p_col;
	v_editContentObject.ht = p_ht;

	$('#div_edit_content').show();

}

/// <summary>
/// Hides edit cell window.
/// </summary>
function hideEditContent() {

	$('#div_edit_content').hide();

	if (v_canEditContent)
		v_editContentObject.ht.setDataAtCell(v_editContentObject.row, v_editContentObject.col, v_editContentObject.editor.getValue());

	v_editContentObject.editor.setValue('');

}
