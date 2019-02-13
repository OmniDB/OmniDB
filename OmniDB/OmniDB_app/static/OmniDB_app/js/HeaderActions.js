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

	var v_fileref = document.getElementById("ss_theme");
  v_fileref.setAttribute("href", '/static/OmniDB_app/css/themes/' + v_theme_type + '.css');

	var v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);

	//setting font size of body
	document.body.style['font-size'] = v_interface_font_size + 'px';


});

function adjustChartTheme(p_chart) {
	var v_chart_font_color = '#666666';
	var v_chart_grid_color = "rgba(0, 0, 0, 0.1)";

	if (v_theme_type=='dark') {
		v_chart_font_color = '#d7d7d7';
		v_chart_grid_color = "rgba(100, 100, 100, 0.3)";
	}

	try {
		p_chart.legend.options.labels.fontColor = v_chart_font_color;
		p_chart.options.title.fontColor = v_chart_font_color;
		p_chart.scales["y-axis-0"].options.gridLines.color = v_chart_grid_color;
		p_chart.scales["x-axis-0"].options.gridLines.color = v_chart_grid_color;
		p_chart.scales["y-axis-0"].options.ticks.minor.fontColor = v_chart_font_color;
		p_chart.scales["y-axis-0"].options.scaleLabel.fontColor = v_chart_font_color;
		p_chart.scales["x-axis-0"].options.ticks.minor.fontColor = v_chart_font_color;
		p_chart.scales["x-axis-0"].options.scaleLabel.fontColor = v_chart_font_color;
	}
	catch(err) {
	}
	p_chart.update();

}

function changeTheme(p_option) {
	var v_fileref = document.getElementById("ss_theme");
	var p_options = p_option.split('/');

	if (parseInt(p_options[0])>=17) {
		v_fileref.setAttribute("href", '/static/OmniDB_app/css/themes/dark.css');
		v_theme_type = 'dark';
	}
	else {
		v_fileref.setAttribute("href", '/static/OmniDB_app/css/themes/light.css');
		v_theme_type = 'light';
	}
	v_editor_theme = p_options[1];
	v_theme_id = p_options[0];

	var els = document.getElementsByClassName("ace_editor");

	Array.prototype.forEach.call(els, function(el) {
	    // Do stuff here
			ace.edit(el).setTheme("ace/theme/" + p_options[1]);
	});

	Chart.helpers.each(Chart.instances, function(instance){
		adjustChartTheme(instance.chart);
	})

	//Hooks
	if (v_connTabControl.tag.hooks.changeTheme.length>0) {
		for (var i=0; i<v_connTabControl.tag.hooks.changeTheme.length; i++)
			v_connTabControl.tag.hooks.changeTheme[i](v_editor_theme,v_theme_type);
	}
}

function changeFontSize(p_option) {
	var els = document.getElementsByClassName("ace_editor");
	v_editor_font_size = p_option;
	Array.prototype.forEach.call(els, function(el) {
	    // Do stuff here
			ace.edit(el).setFontSize(Number(p_option));
	});
}

function changeInterfaceFontSize(p_option) {
	v_interface_font_size = p_option;
	document.body.style['font-size'] = v_interface_font_size + 'px';
}

/// <summary>
/// Opens user config window.
/// </summary>
function showConfigUser() {

	document.getElementById('sel_editor_font_size').value = v_editor_font_size;
	document.getElementById('sel_interface_font_size').value = v_interface_font_size;
	document.getElementById('sel_editor_theme').value = v_theme_id + '/' + v_editor_theme;

	document.getElementById('txt_confirm_new_pwd').value = '';
	document.getElementById('txt_new_pwd').value = '';

	document.getElementById('chk_enable_chat').checked = ((v_enable_omnichat == 1) ? true : false);

	document.getElementById('sel_csv_encoding').value = v_csv_encoding;
	document.getElementById('txt_csv_delimiter').value = v_csv_delimiter;

	$('#div_config_user').addClass('isActive');

}

/// <summary>
/// Opens OmniDB about window.
/// </summary>
function showAbout() {

	$('#div_about').addClass('isActive');

}

/// <summary>
/// Hides user config window.
/// </summary>
function hideAbout() {

	$('#div_about').removeClass('isActive');

}

/// <summary>
/// Go to connections.
/// </summary>
function goToConnections() {

	showConfirm('You will lose existing changes. Would you like to continue?',
		function() {

			window.open("../connections","_self");

		});

}

/// <summary>
/// Go to connections.
/// </summary>
function confirmSignout() {

	showConfirm('Are you sure you want to sign out?',
		function() {

			window.open("../logout","_self");

		});

}

/// <summary>
/// Go to workspace.
/// </summary>
function goToWorkspace() {

	showConfirm('You will lose existing changes. Would you like to continue?',
		function() {

			window.open("../workspace","_self");

		});

}

/// <summary>
/// Shows website in outer tab.
/// </summary>
function showWebsite(p_name, p_url) {

	if (v_connTabControl)
		hideAbout();
		v_connTabControl.tag.createWebsiteOuterTab(p_name,p_url);

}

/// <summary>
/// Hides user config window.
/// </summary>
function hideConfigUser() {

	$('#div_config_user').removeClass('isActive');

}

/// <summary>
/// Saves user config to OmniDB database.
/// </summary>
function saveConfigUser() {

	v_editor_font_size = document.getElementById('sel_editor_font_size').value;
	v_theme_id = document.getElementById('sel_editor_theme').value.split('/')[0];

	var v_confirm_pwd = document.getElementById('txt_confirm_new_pwd');
	var v_pwd = document.getElementById('txt_new_pwd');

	v_enable_omnichat = ((document.getElementById('chk_enable_chat').checked == true) ? 1 : 0);

	v_csv_encoding = document.getElementById('sel_csv_encoding').value;
	v_csv_delimiter = document.getElementById('txt_csv_delimiter').value;

	if ((v_confirm_pwd.value!='' || v_pwd.value!='') && (v_pwd.value!=v_confirm_pwd.value))
		showAlert('New Password and Confirm New Password fields do not match.');
	else {
		var input = JSON.stringify({"p_font_size" : v_editor_font_size, "p_interface_font_size" : v_interface_font_size, "p_theme" : v_theme_id, "p_pwd" : v_pwd.value, "p_chat_enabled": v_enable_omnichat, "p_csv_encoding": v_csv_encoding, "p_csv_delimiter": v_csv_delimiter});

		execAjax('/save_config_user/',
				input,
				function(p_return) {
					v_editor_theme = p_return.v_data.v_theme_name;
					v_theme_type = p_return.v_data.v_theme_type;
					$('#div_config_user').removeClass('isActive');
					showAlert('Configuration saved.');

				});
	}
}

/// <summary>
/// Saves shortcuts to OmniDB database.
/// </summary>
function saveShortcuts() {

	var v_shortcut_list = [];

	for (var property in v_shortcut_object.shortcuts) {
    if (v_shortcut_object.shortcuts.hasOwnProperty(property)) {
        v_shortcut_list.push(v_shortcut_object.shortcuts[property]);
    }
  }

	var input = JSON.stringify({"p_shortcuts": v_shortcut_list});

	execAjax('/save_shortcuts/',
			input,
			function(p_return) {
				showAlert('Shortcuts saved.');

			});
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
	v_editor.$blockScrolling = Infinity;

	v_editor.setFontSize(Number(v_editor_font_size));

	v_editor.setOptions({enableBasicAutocompletion: true});

	document.getElementById('txt_edit_content').onclick = function() {
  		v_editor.focus();
    };

	if (p_content!=null)
		v_editor.setValue(String(p_content));
	else
		v_editor.setValue('');

	v_editor.clearSelection();

	if (p_can_alter)
		v_editor.setReadOnly(false);
	else
		v_editor.setReadOnly(true);

	//Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
	v_editor.commands.bindKey("Cmd-,", null)
	v_editor.commands.bindKey("Ctrl-,", null)
	v_editor.commands.bindKey("Cmd-Delete", null)
	v_editor.commands.bindKey("Ctrl-Delete", null)

	v_editContentObject = new Object();
	v_editContentObject.editor = v_editor;
	v_editContentObject.row = p_row;
	v_editContentObject.col = p_col;
	v_editContentObject.ht = p_ht;

	$('#div_edit_content').addClass('isActive');

}

/// <summary>
/// Hides edit cell window.
/// </summary>
function hideEditContent() {

	$('#div_edit_content').removeClass('isActive');

	if (v_canEditContent)
		v_editContentObject.ht.setDataAtCell(v_editContentObject.row, v_editContentObject.col, v_editContentObject.editor.getValue());

	v_editContentObject.editor.setValue('');

}
