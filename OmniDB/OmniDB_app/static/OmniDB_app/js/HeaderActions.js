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

	var v_configTabControl = null;
});

/// <summary>
/// Opens user config window.
/// </summary>
function showConfigUser() {
	var v_popUp = v_popUpControl.getPopUpById('show_config_user');

	if(v_popUp != null) {
		v_popUp.turnActive();
		return;
	}

	var v_html =
		'<div id="div_config_user" style="margin-right: 15px;">' +
		'	<div id="config_tabs" style="margin-top: 10px; margin-left: 10px; margin-right: 10px; margin-bottom: 10px;">' +
		'		<ul>' +
		'		<li id="config_tabs_tab1">Editor</li>' +
		'	  {% if not desktop_mode %}' +
		'		 <li id="config_tabs_tab2">User</li>' +
		'	  {% endif %}' +
		'		</ul>' +
		'		<div id="div_config_tabs_tab1">' +
		'			<div style="margin: 30px; height: auto; top: 0px; bottom: 0px; left: 0px; right: 0px;">' +
		'			<div style="text-align: center;">' +
		'			<div style="margin-bottom: 10px;">Editor font size</div>' +
		'			<select id="sel_editor_font_size" style="width: 200px; margin-bottom: 20px;">' +
		'				<option value="10">10</option>' +
		'				<option value="11">11</option>' +
		'				<option value="12">12</option>' +
		'				<option value="13">13</option>' +
		'				<option value="14">14</option>' +
		'				<option value="15">15</option>' +
		'				<option value="16">16</option>' +
		'				<option value="17">17</option>' +
		'				<option value="18">18</option>' +
		'			</select>' +
		'		<div style="margin-bottom: 10px;">Editor theme</div>' +
		'			<select id="sel_editor_theme" style="width: 200px; margin-bottom: 20px;">' +
		'				<option value="1">(Light) OmniDB</option>' +
		'				<option value="2">(Light) Chrome</option>' +
		'				<option value="3">(Light) Clouds</option>' +
		'				<option value="4">(Light) Crimson Editor</option>' +
		'				<option value="5">(Light) Dawn</option>' +
		'				<option value="6">(Light) Dreamweaver</option>' +
		'				<option value="7">(Light) Eclipse</option>' +
		'				<option value="8">(Light) Github</option>' +
		'				<option value="9">(Light) Iplastic</option>' +
		'				<option value="10">(Light) Katzenmilch</option>' +
		'				<option value="11">(Light) Kuroir</option>' +
		'				<option value="12">(Light) Solarized Light</option>' +
		'				<option value="13">(Light) SQL Server</option>' +
		'				<option value="14">(Light) Textmate</option>' +
		'				<option value="15">(Light) Tomorrow</option>' +
		'				<option value="16">(Light) XCode</option>' +
		'				<option value="17">(Dark) OmniDB Dark</option>' +
		'				<option value="18">(Dark) Ambiance</option>' +
		'				<option value="19">(Dark) Chaos</option>' +
		'				<option value="20">(Dark) Clouds Midnight</option>' +
		'				<option value="21">(Dark) Cobalt</option>' +
		'				<option value="22">(Dark) Idle Fingers</option>' +
		'				<option value="23">(Dark) KR Theme</option>' +
		'				<option value="24">(Dark) Merbivore</option>' +
		'				<option value="25">(Dark) Merbivore Soft</option>' +
		'				<option value="26">(Dark) Mono Industrial</option>' +
		'				<option value="27">(Dark) Monokai</option>' +
		'				<option value="28">(Dark) Pastel On Dark</option>' +
		'				<option value="29">(Dark) Solarized Dark</option>' +
		'				<option value="30">(Dark) Terminal</option>' +
		'				<option value="31">(Dark) Tomorrow Night</option>' +
		'				<option value="32">(Dark) Tomorrow Night Blue</option>' +
		'				<option value="33">(Dark) Tomorrow Night Bright</option>' +
		'				<option value="34">(Dark) Tomorrow Night 80s</option>' +
		'				<option value="35">(Dark) Twilight</option>' +
		'				<option value="36">(Dark) Vibrant Ink</option>' +
		'			</select>' +
		'			</div>' +
		'		<div style="text-align: center;">' +
		'		  <button onclick="saveConfigUser();">Save Changes</button>' +
		'		</div>' +
		'			</div>' +
		'		</div>';

	if(!v_desktop_mode) {
		v_html += '		<div id="div_config_tabs_tab2">';
	}
	else {
		v_html += '     <div id="div_config_tabs_tab2" style="display: none;">';
	}

	v_html +=
		'			<div style="margin: 30px; height: auto; top: 0px; bottom: 0px; left: 0px; right: 0px;">' +
		'				<div style="text-align: center;">' +
		'					<div style="margin-bottom: 10px;">New Password</div>' +
		'					<input id="txt_new_pwd" type="password" style="width: 200px; margin-bottom: 20px;">' +
		'				</div>' +
		'				<div style="text-align: center;">' +
		'					<div style="margin-bottom: 10px;">Confirm New Password</div>' +
		'					<input id="txt_confirm_new_pwd" type="password" style="width: 200px; margin-bottom: 20px;">' +
		'				</div>' +
		'				<div style="text-align: center; display: none;">' +
		'					<div style="margin-bottom: 10px;">Enable OmniChat</div>' +
		'					<input id="chk_enable_chat" type="checkbox" style="width: 200px; margin-bottom: 20px;">' +
		'				</div>' +
		'				<div style="text-align: center;">' +
		'					<button onclick="saveConfigUser();">Save Changes</button>' +
		'				</div>' +
		'			</div>' +
		'		</div>' +
		'	</div>' +
		'</div>';

	var v_config = {
		width: '600px',
		height: '345px',
		resizable: true,
		draggable: true,
		top: (window.innerHeight - 345) / 2 + 'px',
		left: (window.innerWidth - 600) / 2 + 'px',
		forceClose: true
	};

	v_popUpControl.addPopUp(
		'show_config_user',
		'User Configurations',
		v_html,
		v_config,
		null
	);

	v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);

	document.getElementById('sel_editor_font_size').value = v_editor_font_size;
	document.getElementById('sel_editor_theme').value = v_theme_id;
	document.getElementById('txt_confirm_new_pwd').value = '';
	document.getElementById('txt_new_pwd').value = '';
	document.getElementById('chk_enable_chat').checked = ((v_enable_omnichat == 1) ? true : false);
}

/// <summary>
/// Opens OmniDB about window.
/// </summary>
function showAbout() {
	var v_popUp = v_popUpControl.getPopUpById('show_about');

	if(v_popUp != null) {
		v_popUp.turnActive();
		return;
	}

	var v_html =
		'<div id="div_about">' +
	    '    <div style="width: 100%; text-align: center;">' +
	    '        <div style="margin: 20px;">' +
		'            <h1>' + v_omnidb_version + '</h1>' +
		'        </div>' +
	    '        <div style="margin: 20px;">' +
	    '            <img src="/static/OmniDB_app/images/postgresql_medium.png" title="PostgreSQL"/>' +
	    '            <!--<img src="/static/OmniDB_app/images/oracle_medium.png" title="Oracle"/>' +
	    '            <img src="/static/OmniDB_app/images/mysql_medium.png" title="MySQL"/>' +
	    '            <img src="/static/OmniDB_app/images/sqlserver_medium.png" title="SQL Server"/>' +
	    '            <img src="/static/OmniDB_app/images/firebird_medium.png" title="Firebird"/>' +
	    '            <img src="/static/OmniDB_app/images/sqlite_medium.png" title="SQLite"/>' +
	    '            <img src="/static/OmniDB_app/images/access_medium.png" title="Microsoft Access"/>' +
	    '            <img src="/static/OmniDB_app/images/mariadb_medium.png" title="MariaDB"/>' +
		'            <img src="/static/OmniDB_app/images/filedb_medium.png" title="Spartacus FileDB"/>-->' +
	    '       </div>' +
	    '       <div style="margin: 20px;"><a onclick="showWebsite("OmniDB", "https://www.omnidb.org")" >www.omnidb.org</a></div>' +
	    '       <div style="margin: 20px;">' +
	    '           <h2>Primary Supporter:</h2>' +
	    '           <a onclick="showWebsite("2ndQuadrant", "https://www.2ndquadrant.com")" ><img style="width: 120px;" src="/static/OmniDB_app/images/supporters/2ndquadrant.png" title="2ndQuadrant"/></a>' +
	    '       </div>' +
	    '    </div>' +
	    '</div>';

	var v_config = {
		width: '400px',
		height: '250px',
		resizable: true,
		draggable: true,
		top: (window.innerHeight - 250) / 2 + 'px',
		left: (window.innerWidth - 400) / 2 + 'px',
		forceClose: true
	};

	v_popUpControl.addPopUp(
		'show_about',
		'About us',
		v_html,
		v_config,
		null
	);
}

/// <summary>
/// Hides user config window.
/// </summary>
function hideAbout() {
	var v_popUp = v_popUpControl.getPopUpById('show_about');

	if(v_popUp != null) {
		v_popUp.close(true);
		return;
	}
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
	var v_popUp = v_popUpControl.getPopUpById('show_config_user');

	if(v_popUp != null) {
		v_popUp.close(true);
		return;
	}
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

	if((v_confirm_pwd.value!='' || v_pwd.value!='') && (v_pwd.value!=v_confirm_pwd.value)) {
		showAlert('New Password and Confirm New Password fields do not match.');
	}
	else {
		var input = JSON.stringify({
			"p_font_size": v_editor_font_size,
			"p_theme": v_theme_id,
			"p_pwd": v_pwd.value,
			"p_chat_enabled": v_enable_omnichat
		});

		execAjax(
			'/save_config_user/',
			input,
			function(p_return) {
				v_editor_theme = p_return.v_data.v_theme_name;
				v_theme_type = p_return.v_data.v_theme_type;
				hideConfigUser();
				showAlert('Configuration saved. Please, refresh the page for changes to take effect.');
			}
		);
	}
}

/// <summary>
/// Hides command history window.
/// </summary>
function hideCommandList() {
	var v_popUp = v_popUpControl.getPopUpById('show_command_list');

	if(v_popUp != null) {
		v_popUp.close(true);
		return;
	}

	v_commandListObject.ht.destroy();
}

/// <summary>
/// Wipes command history.
/// </summary>
function deleteCommandList() {
	showConfirm(
		'Are you sure you want to clear command history?',
		function() {
			execAjax(
				'/clear_command_list/',
				JSON.stringify({}),
				function(p_return) {
					hideCommandList();
				}
			);
		}
	);
}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function showCommandList() {
	v_commandListObject = new Object();
	v_commandListObject.current_page = 1;
	refreshCommandList();
}

function commandHistoryNextPage() {
	if (v_commandListObject.current_page < v_commandListObject.pages) {
		v_commandListObject.current_page += 1;
		refreshCommandList();
	}
}

function commandHistoryPreviousPage() {
	if (v_commandListObject.current_page > 1) {
		v_commandListObject.current_page -= 1;
		refreshCommandList();
	}
}

function commandHistoryFirstPage() {
	if (v_commandListObject.current_page != 1) {
		v_commandListObject.current_page = 1;
		refreshCommandList();
	}
}

function commandHistoryLastPage() {
	if (v_commandListObject.current_page != v_commandListObject.pages) {
		v_commandListObject.current_page = v_commandListObject.pages;
		refreshCommandList();
	}
}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function refreshCommandList() {

	execAjax(
		'/get_command_list/',
		JSON.stringify({
			'p_current_page': v_commandListObject.current_page
		}),
		function(p_return) {
			var v_html =
				'<div style="margin-left:10px; margin-top: 10px; display:inline-block;">' +
				'	<button onclick="commandHistoryFirstPage()">First</button>' +
				'	<button onclick="commandHistoryPreviousPage()">Previous</button>' +
				'	<span id="cl_curr_page"></span> / <span id="cl_num_pages"></span>' +
				'	<button onclick="commandHistoryNextPage()">Next</button>' +
				'	<button onclick="commandHistoryLastPage()">Last</button>' +
				'	<button onclick="deleteCommandList()" class="bt_red">Clear list</button>' +
				'</div>' +
				'<div style="padding: 10px;">' +
				'	<div id="div_command_list_data" style="width: 100%; height: 600px; overflow: auto;"></div>' +
				'</div>';

			var v_popUp = v_popUpControl.getPopUpById('show_command_list');

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
					'show_command_list',
					'Command List',
					v_html,
					v_config,
					null
				);
			}

			var v_height  = window.innerHeight - $('#div_command_list_data').offset().top - 60;
			document.getElementById('div_command_list_data').style.height = v_height + "px";

			v_commandListObject.pages = p_return.v_data.pages;
			document.getElementById('cl_num_pages').innerHTML = p_return.v_data.pages;
			document.getElementById('cl_curr_page').innerHTML = v_commandListObject.current_page;

			var columnProperties = [];

			var col = new Object();
			col.title =  'Start';
			col.readOnly = true;
			col.width = 180;
			columnProperties.push(col);

			var col = new Object();
			col.title =  'End';
			col.readOnly = true;
			col.width = 180;
			columnProperties.push(col);

			var col = new Object();
			col.title =  'Duration';
			col.readOnly = true;
			col.width = 150;
			columnProperties.push(col);

			var col = new Object();
			col.title =  'Mode';
			col.readOnly = true;
			col.width = 100;
			columnProperties.push(col);

			var col = new Object();
			col.title =  'Status';
			col.readOnly = true;
			col.width = 50;
			columnProperties.push(col);

			var col = new Object();
			col.title =  'Command';
			col.readOnly = true;
			col.width = 400;
			columnProperties.push(col);

			var v_div_result = document.getElementById('div_command_list_data');

			if (v_div_result.innerHTML!='')
				v_commandListObject.ht.destroy();

			var container = v_div_result;
			v_commandListObject.ht = new Handsontable(container,
													{
														data: p_return.v_data.command_list,
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
																	cellProperties.renderer = blueHtmlRenderer;
																else
																	cellProperties.renderer = whiteHtmlRenderer;
														    return cellProperties;

														}
													});

		},
		null,
		'box'
	);
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
	var v_html =
		'<div style="height: 90%; margin-right: 20px;">' +
		'	<div id="txt_edit_content" style="text-align: left; width: 100%; height: 100%; font-size: 12px; border: 1px solid rgb(195, 195, 195);">' +
		'	</div>' +
		'</div>';

	var v_popUp = v_popUpControl.getPopUpById('edit_cell_data');

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

		var v_callbacks = {
			beforeClose: function(p_popUp) {
				if(v_canEditContent) {
					v_editContentObject.ht.setDataAtCell(v_editContentObject.row, v_editContentObject.col, v_editContentObject.editor.getValue());
				}

				v_editContentObject.editor.setValue('');
			}
		};

		v_popUp = v_popUpControl.addPopUp(
			'edit_cell_data',
			'Content',
			v_html,
			v_config,
			v_callbacks
		);
	}

	v_canEditContent = p_can_alter;

	if(v_editContentObject != null) {
		if(v_editContentObject.editor != null) {
			 v_editContentObject.editor.destroy();
			 document.getElementById('txt_edit_content').innerHTML = '';
		}
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
			showFindReplace(v_editor);
			v_copyPasteObject.v_tabControl.selectTabIndex(0);
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

}
