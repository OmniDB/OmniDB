/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function () {

	var v_fileref = document.createElement("link");
    v_fileref.setAttribute("rel", "stylesheet");
    v_fileref.setAttribute("type", "text/css");
    v_fileref.setAttribute("href", 'css/themes/' + v_theme_type + '.css');
    document.getElementsByTagName("head")[0].appendChild(v_fileref);

	var v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);

	v_copyPasteObject = new Object();

	v_copyPasteObject.v_tabControl = createTabControl('find_replace',0,null);
	v_copyPasteObject.v_tabControl.selectTabIndex(0);

	v_connTabControl = createTabControl('conn_tabs',0,null);


	v_connTabControl.createTab('+',false,createConnTab,false);

	getDatabaseList();

	setTimeout(refreshChatMessages, 1500);
	setInterval(refreshChatMessages, 1500);

	setTimeout(refreshChatUsers, 1500);
	setInterval(refreshChatUsers, 30000);

	var v_textarea = document.getElementById('textarea_chat_message');
	v_textarea.value = '';
	v_textarea.onkeydown = function(event) {
		if(event.keyCode == 13) {//Enter
			sendMessage();
			event.preventDefault();
			event.stopPropagation();
		}
	}
});

/// <summary>
/// Opens copy & paste window.
/// </summary>
function showFindReplace(p_editor) {

	v_copyPasteObject.v_editor = p_editor;

	$('#div_find_replace').show();

	document.getElementById('txt_replacement_text').value = '';
	document.getElementById('txt_replacement_text_new').value = '';

}

/// <summary>
/// Hides copy & paste window.
/// </summary>
function replaceText() {

	var v_old_text = v_copyPasteObject.v_editor.getValue();

	var v_new_text = v_old_text.split(document.getElementById('txt_replacement_text').value).join(document.getElementById('txt_replacement_text_new').value);

	v_copyPasteObject.v_editor.setValue(v_new_text);

	hideFindReplace();

}

/// <summary>
/// Opens copy & paste window.
/// </summary>
function hideFindReplace() {

	$('#div_find_replace').hide();

}

/// <summary>
/// Renames tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function renameTab(p_tab) {

	showConfirm('<input id="tab_name"/ value="' + p_tab.text + '" style="width: 200px;">',
	            function() {

					p_tab.renameTab(document.getElementById('tab_name').value);

	            });

}

/// <summary>
/// Removes tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function removeTab(p_tab) {

	if (p_tab.tag.ht!=null) {
		p_tab.tag.ht.destroy();
		p_tab.tag.div_result.innerHTML = '';
	}

	if (p_tab.tag.editor!=null)
		p_tab.tag.editor.destroy();

}

/// <summary>
/// Changing selected database.
/// </summary>
/// <param name="p_sel_id">Selection tag ID.</param>
/// <param name="p_value">Database ID.</param>
function changeDatabase(p_value) {

	v_connTabControl.selectedTab.tag.selectedDatabaseIndex = p_value;

	v_connTabControl.selectedTab.renameTab('<img src="images/' + v_connTabControl.tag.connections[p_value].v_db_type + '_medium.png"/> ' + v_connTabControl.tag.connections[p_value].v_alias);
	getTree(v_connTabControl.selectedTab.tag.divTree.id);

	/*execAjax('MainDB.aspx/ChangeDatabase',
			JSON.stringify({"p_value": p_value}),
			function(p_return) {

				getTree(v_connTabControl.selectedTab.tag.divTree.id);

			},
			null,
			'box');*/

}

/// <summary>
/// Retrieves database list.
/// </summary>
/// <param name="p_sel_id">Selection tag ID.</param>
/// <param name="p_filter">Filtering a specific database technology.</param>
function getDatabaseList() {

	execAjax('MainDB.aspx/GetDatabaseList',
			null,
			function(p_return) {

				v_connTabControl.tag.selectHTML = p_return.v_data.v_select_html;
				v_connTabControl.tag.connections = p_return.v_data.v_connections;
				createConnTab();

			},
			null,
			'box');

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeVertical(event) {

	v_start_height = event.screenY;
	document.body.addEventListener("mouseup", resizeVerticalEnd);

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeVerticalEnd(event) {

	document.body.removeEventListener("mouseup", resizeVerticalEnd);

	var v_height_diff = event.screenY - v_start_height;

	var v_editor_div = document.getElementById(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editorDivId);
	var v_result_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

	if (v_height_diff < 0) {
		if (Math.abs(v_height_diff) > parseInt(v_editor_div.style.height, 10))
		 v_height_diff = parseInt(v_editor_div.style.height, 10)*-1 + 10;
	}
	else {
		if (Math.abs(v_height_diff) > parseInt(v_result_div.style.height, 10))
		 v_height_diff = parseInt(v_result_div.style.height, 10) - 10;
	}

	v_editor_div.style.height = parseInt(v_editor_div.style.height, 10) + v_height_diff + 'px';
	v_result_div.style.height = parseInt(v_result_div.style.height, 10) - v_height_diff + 'px';

	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();

	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query') {
		if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht!=null)
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.render();
	}
	else {
		if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.ht!=null) {
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.ht.render();
		}
	}

}

/// <summary>
/// Maximize SQL Editor.
/// </summary>
function maximizeEditor() {

	var v_editor_div = document.getElementById(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editorDivId);
	var v_result_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

	var v_height_diff = parseInt(v_result_div.style.height, 10) - 10;

	v_editor_div.style.height = parseInt(v_editor_div.style.height, 10) + v_height_diff + 'px';
	v_result_div.style.height = parseInt(v_result_div.style.height, 10) - v_height_diff + 'px';

	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();

}

/// <summary>
/// Minimize SQL Editor.
/// </summary>
function minimizeEditor() {

	var v_editor_div = document.getElementById(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editorDivId);
	var v_result_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

	var v_height_diff = parseInt(v_editor_div.style.height, 10) - 10;


	v_result_div.style.height = (parseInt(v_result_div.style.height, 10) + parseInt(v_editor_div.style.height, 10) - 300) + 'px';

	v_editor_div.style.height = '300px';

	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();

}

/// <summary>
/// Resize Tab.
/// </summary>
function resizeHorizontal(event) {

	document.body.addEventListener("mouseup", resizeHorizontalEnd);
	v_start_width = event.screenX;
}

/// <summary>
/// Resize Tab.
/// </summary>
function resizeHorizontalEnd(event) {
	document.body.removeEventListener("mouseup", resizeHorizontalEnd);

	var v_width_diff = event.screenX - v_start_width;

	v_width_diff = Math.ceil(v_width_diff/window.innerWidth*100);

	var v_left_div = v_connTabControl.selectedTab.tag.divLeft;
	var v_right_div = v_connTabControl.selectedTab.tag.divRight;

	v_left_div.style.width = parseInt(v_left_div.style.width, 10) + v_width_diff + '%';
	v_right_div.style.width = parseInt(v_right_div.style.width, 10) - v_width_diff + '%';



	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query') {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();
		if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht!=null) {
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.render();
		}
	}
	else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='edit') {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();
		if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.ht!=null)
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.ht.render();
	}
	else {
        v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.render();
	}

}

/// <summary>
/// Creates connection tab.
/// </summary>
function createConnTab() {

	v_connTabControl.removeTabIndex(v_connTabControl.tabList.length-1);
	var v_tab = v_connTabControl.createTab('<img src="images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/> ' + v_connTabControl.tag.connections[0].v_alias,true,null,null,null,null,true);

	v_connTabControl.selectTab(v_tab);

	var v_html = "<div id='" + v_tab.id + "_div_left' class='div_left' style='float:left; position: relative; width:25%; height: 90%;'>" +
	"<div style='padding-right: 12px;'><div id='" + v_tab.id + "_div_select_db' style='width: 100%; display: inline-block;'></div>" +
	"</div>" +
	"<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: col-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +
	"<div style='width: 97%;'><div id='" + v_tab.id + "_tree' style='margin-top: 10px; overflow: auto; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans;'></div>" +
	"</div>" +
	"<div id='html1'>" +
	"</div>" +
	"</div>" +
	"<div id='" + v_tab.id + "_div_right' class='div_right' style='float:left; width:75%;'>" +
	"<div id='" + v_tab.id + "_tabs'>" +
	"<ul>" +
	"</ul>" +
	"</div>" +
	"</div>";

	var v_div = document.getElementById('div_' + v_tab.id);
	v_div.innerHTML = v_html;

	var v_height  = $(window).height() - $('#' + v_tab.id + '_tree').offset().top - 35;
	document.getElementById(v_tab.id + '_tree').style.height = v_height + "px";

	var v_currTabControl = createTabControl(v_tab.id + '_tabs',0,null);

	var v_createTabFunction = function() {

		v_currTabControl.removeTabIndex(v_currTabControl.tabList.length-1);
		var v_tab = v_currTabControl.createTab('Query',true,null,renameTab,'cm_tab',removeTab,true);
		v_currTabControl.selectTab(v_tab);

		var v_html = "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 300px;border: 1px solid #c3c3c3;'></div>" +

					"<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: row-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +

					 "<button class='bt_execute' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='querySQL();'><img src='images/play.png' style='vertical-align: middle;'/></button>" +
					 "<select id='sel_filtered_data_" + v_tab.id + "'><option value='-3' >Script</option><option value='-2' >Execute</option><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option><option value='-1'>Query All rows</option></select>" +
					 "<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					 "<button class='bt_export' title='Export Data' style='margin-bottom: 5px; margin-left: 5px; float: right; display: inline-block;' onclick='exportData();'><img src='images/table_export.png' style='vertical-align: middle;'/></button>" +
					 "<select id='sel_export_type_" + v_tab.id + "' style='float: right;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option><option value='DBF' >DBF</option></select>" +
					 "<div id='div_result_" + v_tab.id + "' style='width: 100%; overflow: hidden;'></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_height  = $(window).height() - $('#div_result_' + v_tab.id).offset().top - 20;

		document.getElementById('div_result_' + v_tab.id).style.height = v_height + "px";

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_query_' + v_tab.id);
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");
		v_editor.commands.bindKey(".", "startAutocomplete");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

		document.getElementById('txt_query_' + v_tab.id).onclick = function() {

			v_editor.focus();

		};


		var command = {
			name: "save",
			bindKey: {
			      mac: v_keybind_object.v_execute_mac,
			      win: v_keybind_object.v_execute
			    },
			exec: function(){
			querySQL();
			}
		}

		v_editor.commands.addCommand(command);

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

		var qtags = {
			getCompletions: function(editor, session, pos, prefix, callback) {

				if (v_completer_ready) {

				  	var wordlist = [];

				  	v_completer_ready = false;
				  	setTimeout(function(){ v_completer_ready = true; }, 1000);

				  	if (prefix!='') {

						execAjax('MainDB.aspx/GetCompletions',
								JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, p_prefix: prefix, p_sql: editor.getValue(), p_prefix_pos: editor.session.doc.positionToIndex(editor.selection.getCursor())}),
								function(p_return) {

									if (p_return.v_data.length==0)
										editor.insert('.');

									wordlist = p_return.v_data;
									callback(null, wordlist);

								},
								null,
								'box',
								false);

					}

				}

			}
		}

		langTools.setCompleters([qtags]);
		v_editor.setOptions({enableBasicAutocompletion: true});

		var v_tag = {
			mode: 'query',
			editor: v_editor,
			editorDivId: 'txt_query_' + v_tab.id,
			query_info: document.getElementById('div_query_info_' + v_tab.id),
			div_result: document.getElementById('div_result_' + v_tab.id),
			sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
			sel_export_type : document.getElementById('sel_export_type_' + v_tab.id)
		};

		v_tab.tag = v_tag;

		v_currTabControl.createTab('+',false,v_createTabFunction);

	};

	var v_createEditDataTabFunction = function(p_table) {

		v_currTabControl.removeTabIndex(v_currTabControl.tabList.length-1);
		var v_tab = v_currTabControl.createTab('<img src="images/edit_data.png"/> ' + p_table,true,null,null,null,removeTab,true);
		v_currTabControl.selectTab(v_tab);

		var v_html = "<div id='div_edit_data_select_" + v_tab.id + "' class='query_info' style='margin-top: 5px; margin-bottom: 5px; font-size: 14px;'>select * from " + p_table + " t</div>" +
					 "<div id='txt_filter_data_" + v_tab.id + "' style=' width: 100%; height: 100px;border: 1px solid #c3c3c3;'></div>" +
					 "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: row-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
					 "<button class='bt_execute' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='queryEditData();'><img src='images/play.png' style='vertical-align: middle;'/></button>" +
					 "<select id='sel_filtered_data_" + v_tab.id + "' onchange='queryEditData()'><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option></select>" +
					 "<div id='div_edit_data_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					 "<button id='bt_saveEditData_" + v_tab.id + "' onclick='saveEditData()' style='visibility: hidden; margin-left: 5px;'>Save Changes</button>" +
					 "<div id='div_edit_data_data_" + v_tab.id + "' style='width: 100%; height: 250px; overflow: hidden;'></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_height  = $(window).height() - $('#div_edit_data_data_' + v_tab.id).offset().top - 20;

		document.getElementById('div_edit_data_data_' + v_tab.id).style.height = v_height + "px"

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_filter_data_' + v_tab.id);
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");
		v_editor.commands.bindKey(".", "startAutocomplete");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

		document.getElementById('txt_filter_data_' + v_tab.id).onclick = function() {

			v_editor.focus();

		};


		var command = {
			name: "save",
			bindKey: {
			      mac: v_keybind_object.v_execute_mac,
			      win: v_keybind_object.v_execute
			    },
			exec: function(){
			queryEditData();
			}
		}

		v_editor.commands.addCommand(command);

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

		var qtags = {
			getCompletions: function(editor, session, pos, prefix, callback) {

				if (v_completer_ready) {

				  	var wordlist = [];

				  	v_completer_ready = false;
				  	setTimeout(function(){ v_completer_ready = true; }, 1000);

				  	if (prefix!='') {

						execAjax('MainDB.aspx/GetCompletionsTable',
								JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, p_table: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.table}),
								function(p_return) {

									if (p_return.v_data.length==0)
										editor.insert('.');

									wordlist = p_return.v_data;
									callback(null, wordlist);

								},
								null,
								'box',
								false);

					}

				}

			}
		}

		langTools.setCompleters([qtags]);
		v_editor.setOptions({enableBasicAutocompletion: true});

		var v_tag = {
			mode: 'edit',
			editor: v_editor,
			editorDivId: 'txt_filter_data_' + v_tab.id,
			query_info: document.getElementById('div_edit_data_query_info_' + v_tab.id),
			div_result: document.getElementById('div_edit_data_data_' + v_tab.id),
			sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
			button_save: document.getElementById('bt_saveEditData_' + v_tab.id),
			sel_export_type : document.getElementById('sel_export_type_' + v_tab.id)
		};

		v_tab.tag = v_tag;

		v_currTabControl.createTab('+',false,v_createTabFunction);

	};

	var v_createAlterTableTabFunction = function(p_table) {

		v_currTabControl.removeTabIndex(v_currTabControl.tabList.length-1);
		var v_tab = v_currTabControl.createTab('<img src="images/table_edit.png"/> ' + p_table,true,null,null,null,removeTab,true);
		v_currTabControl.selectTab(v_tab);

		var v_html = "<span style='margin-left: 10px;'>Table Name: </span><input type='text' id='txt_tableNameAlterTable_" + v_tab.id + "' onchange='changeTableName()' style='margin: 10px;'/>" +
		"<button id='bt_saveAlterTable_" + v_tab.id + "' onclick='saveAlterTable()' style='visibility: hidden;'>Save Changes</button>" +
        "        <div id='alter_tabs_" + v_tab.id + "' style='margin-left: 10px; margin-right: 10px; margin-bottom: 10px;'>" +
	    "            <ul>" +
	    "            <li id='alter_tabs_" + v_tab.id + "_tab1'>Columns</li>" +
	    "            <li id='alter_tabs_" + v_tab.id + "_tab2'>Constraints</li>" +
	    "            <li id='alter_tabs_" + v_tab.id + "_tab3'>Indexes</li>" +
	  	"			</ul>" +
	  	"			<div id='div_alter_tabs_" + v_tab.id + "_tab1'>" +
	  	"				<div style='padding: 20px;'>" +
		"                	<div id='div_alter_table_data_" + v_tab.id + "' style='height: 400px; overflow: hidden;'></div>" +
		"                </div>" +
	  	"			</div>" +
	  	"			<div id='div_alter_tabs_" + v_tab.id + "_tab2'>" +
	  	"				<button id='bt_newConstraintAlterTable_" + v_tab.id + "' onclick='newConstraintAlterTable()' style='margin-left: 20px; margin-top: 20px;'>New Constraint</button>" +
	  	"				<div style='padding: 20px;'>" +
	  	"					<div id='div_alter_constraint_data_" + v_tab.id + "' style='width: 100%; height: 400px; overflow: hidden;'></div>" +
	  	"				</div>" +
	  	"			</div>" +
	  	"			<div id='div_alter_tabs_" + v_tab.id + "_tab3'>" +
	  	"				<button id='bt_newIndexAlterTable_" + v_tab.id + "' onclick='newIndexAlterTable()' style='display: block; margin-left: 20px; margin-top: 20px;'>New Index</button>" +
	  	"				<div style='padding: 20px;'>" +
	  	"					<div id='div_alter_index_data_" + v_tab.id + "' style='width: 100%; height: 400px; overflow: hidden;'></div>" +
	  	"				</div>" +
	  	"			</div>" +
  		"		</div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_height  = $(window).height() - $('#div_alter_table_data_' + v_tab.id).offset().top - 35;

		document.getElementById('div_alter_table_data_' + v_tab.id).style.height = v_height + "px";
		document.getElementById('div_alter_constraint_data_' + v_tab.id).style.height = v_height + "px";
		document.getElementById('div_alter_index_data_' + v_tab.id).style.height = v_height + "px";

		var v_curr_tabs = createTabControl('alter_tabs_' + v_tab.id,0,null);



		var v_tag = {
			mode: 'alter',
			txtTableName: document.getElementById('txt_tableNameAlterTable_' + v_tab.id),
			btSave: document.getElementById('bt_saveAlterTable_' + v_tab.id),
			btNewConstraint: document.getElementById('bt_newConstraintAlterTable_' + v_tab.id),
			btNewIndex: document.getElementById('bt_newIndexAlterTable_' + v_tab.id),
			htColumns: null,
			htConstraints: null,
			htIndexes: null,
			htDivColumns: document.getElementById('div_alter_table_data_' + v_tab.id),
			htDivConstraints: document.getElementById('div_alter_constraint_data_' + v_tab.id),
			htDivIndexes: document.getElementById('div_alter_index_data_' + v_tab.id),
			tabControl: v_curr_tabs,
			alterTableObject: { mode: null }
		};

		v_curr_tabs.tabList[0].elementLi.onclick = function() {

			v_curr_tabs.selectTabIndex(0);
			v_tag.alterTableObject.htColumns.render();
			v_tag.alterTableObject.window = 'columns';

		}

		v_curr_tabs.tabList[1].elementLi.onclick = function() {

			v_curr_tabs.selectTabIndex(1);
			v_tag.alterTableObject.htConstraints.render();
			v_tag.alterTableObject.window = 'constraints';

		}

		v_curr_tabs.tabList[2].elementLi.onclick = function() {

			if (v_tag.alterTableObject.mode!='alter')
				showAlert('Create the table first.');
			else {
				v_curr_tabs.selectTabIndex(2);
				v_tag.alterTableObject.htIndexes.render();
				v_tag.alterTableObject.window = 'indexes';
			}

		}

		v_curr_tabs.selectTabIndex(0);

		v_tab.tag = v_tag;

		v_currTabControl.createTab('+',false,v_createTabFunction);

	};

	v_currTabControl.tag.createQueryTab = v_createTabFunction;
	v_currTabControl.tag.createEditDataTab = v_createEditDataTabFunction;
	v_currTabControl.tag.createAlterTableTab = v_createAlterTableTabFunction;

	v_currTabControl.createTab('+',false,v_createTabFunction);

	v_createTabFunction();

	var v_tag = {
		tabControl: v_currTabControl,
		divTree: document.getElementById(v_tab.id + '_tree'),
		divLeft: document.getElementById(v_tab.id + '_div_left'),
		divRight: document.getElementById(v_tab.id + '_div_right'),
		selectedDatabaseIndex: 0
	};

	v_tab.tag = v_tag;

	var v_div_select_db = document.getElementById(v_tab.id + '_div_select_db');
	v_div_select_db.innerHTML = v_connTabControl.tag.selectHTML;
	$(v_div_select_db.childNodes[0]).msDropDown();

	getTree(v_tab.id + '_tree');

	v_connTabControl.createTab('+',false,createConnTab);

}

/// <summary>
/// Shows or hides graph window.
/// </summary>
/// <param name="p_mode">Mode.</param>
/// <param name="p_graph_type">Graph Type.</param>
function modalGraph(p_mode,p_graph_type) {

    if (p_mode == 'hide') {
        $('#div_graph').hide();
        network.destroy();
    }
    else if (p_mode == 'show') {
        drawGraph(p_graph_type);
    }

}

/// <summary>
/// Draws graph.
/// </summary>
/// <param name="p_graph_type">Graph Type.</param>
function drawGraph(p_graph_type) {

	v_type = '';

	if (p_graph_type==0)
		v_type='DrawGraphSimple';
	else if (p_graph_type==1)
		v_type='DrawGraph';
	else
		v_type='DrawGraphComplete';

	execAjax('MainDB.aspx/' + v_type,
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				$('#div_legend').hide();
				$('#div_graph').show();

				if (p_graph_type==1) {
		        	$('#div_legend').show();

		        	for (i=0; i<6; i++) {
		        		document.getElementById('p_legend_' + i).innerHTML = p_return.v_data.v_legends[i];
		        	}
		        }

	            v_nodes = [];
	            v_edges = [];

	            for (var i=0; i<p_return.v_data.v_nodes.length; i++)
	            {

	            	var v_node_object = new Object();
					v_node_object.data = new Object();
					v_node_object.position = new Object();
					v_node_object.data.id = p_return.v_data.v_nodes[i].id;
					v_node_object.data.label = p_return.v_data.v_nodes[i].label;
					v_node_object.classes = 'group' + p_return.v_data.v_nodes[i].group;

					v_nodes.push(v_node_object);

	            }

	            for (var i=0; i<p_return.v_data.v_edges.length; i++)
	            {

	            	var v_edge_object = new Object();
					v_edge_object.data = new Object();
					v_edge_object.data.source = p_return.v_data.v_edges[i].from;
					v_edge_object.data.target = p_return.v_data.v_edges[i].to;
					v_edge_object.data.label = p_return.v_data.v_edges[i].label;
					v_edge_object.data.faveColor = '#9dbaea';
					v_edge_object.data.arrowColor = '#9dbaea';
					v_edges.push(v_edge_object);

	            }

				network = window.cy = cytoscape({
					container: document.getElementById('div_graph_content'),
					boxSelectionEnabled: false,
					autounselectify: true,
					layout: {
						name: 'cose',
            			idealEdgeLength: 100,
            			nodeOverlap: 20
					},
					style: [
						{
							selector: 'node',
							style: {
								'content': 'data(label)',
								'text-opacity': 0.5,
								'text-valign': 'top',
								'text-halign': 'right',
								'background-color': '#11479e',
								'text-wrap': 'wrap',


							}
						},
						{
							selector: 'node.group1',
							style: {
								'background-color': 'blue'
							}
						},
						{
							selector: 'node.group2',
							style: {
								'background-color': 'cyan'
							}
						},
						{
							selector: 'node.group3',
							style: {
								'background-color': 'lightgreen'
							}
						},
						{
							selector: 'node.group4',
							style: {
								'background-color': 'yellow'
							}
						},
						{
							selector: 'node.group5',
							style: {
								'background-color': 'orange'
							}
						},
						{
							selector: 'node.group6',
							style: {
								'background-color': 'red'
							}
						},

						{
							selector: 'edge',
							style: {
								'curve-style': 'bezier',
						        'target-arrow-shape': 'triangle',
						        'target-arrow-color': 'data(faveColor)',
						        'line-color': 'data(arrowColor)',
						        'text-opacity': 0.75,
						        'width': 2,
						        'control-point-distances': 50,
						        'content': 'data(label)',
						        'text-wrap': 'wrap',
						        'edge-text-rotation': 'autorotate'
							}
						}
					],

					elements: {
						nodes: v_nodes,
						edges: v_edges
					},
				});

			},
			null,
			'box');

}

/// <summary>
/// Hides statistics.
/// </summary>
function hideStatistics() {

    $('#div_statistics').hide();
    myBarChart.destroy();

}

/// <summary>
/// Retrieves and displays statistics.
/// </summary>
function getStatistics() {

	execAjax('MainDB.aspx/GetStatistics',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				$('#div_statistics').show();

	            var data = {
				    labels: p_return.v_data.texts,
				    datasets: [{
				            label: "My Second dataset",
				            fillColor: "rgba(151,187,205,0.5)",
				            strokeColor: "rgba(151,187,205,0.8)",
				            highlightFill: "rgba(151,187,205,0.75)",
				            highlightStroke: "rgba(151,187,205,1)",
				            data: p_return.v_data.values
				        }
				    ]
				};

                document.getElementById('tot_records').innerHTML = '<b>Total Records:</b> ' + p_return.v_data.total;
                document.getElementById('stat_chart').width = 400 + 50*p_return.v_data.texts.length;
				var ctx = document.getElementById("stat_chart").getContext("2d");
				myBarChart = new Chart(ctx).Bar(data);

			},
			null,
			'box');


}

/// <summary>
/// Queries and displays query results.
/// </summary>
function querySQL() {

	var v_sql_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
	var v_sel_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value;

	if (v_sql_value=='') {
		showAlert('Please provide a string.');
	}
	else {
		var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_sql": v_sql_value, "p_select_value" : v_sel_value});

		var start_time = new Date().getTime();

		execAjax('MainDB.aspx/QuerySQL',
				input,
				function(p_return) {

					var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;
					var v_query_info = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.query_info;

					if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht!=null) {
						v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.destroy();
						v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht = null;
					}

					v_div_result.innerHTML = '';

					var request_time = new Date().getTime() - start_time;

					if (v_sel_value==-2) {
						v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";
						v_div_result.innerHTML = '';
					}
					else if (v_sel_value==-3) {

						v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";

						v_div_result.innerHTML = '<div class="query_info">' + p_return.v_data + '</div>';

					}
					else {

						window.scrollTo(0,0);

						v_query_info.innerHTML = p_return.v_data.v_query_info + "<br/>Response time: " + request_time/1000 + " seconds";

						var columnProperties = [];

						for (var i = 0; i < p_return.v_data.v_col_names.length; i++) {
						    var col = new Object();

						    col.readOnly = true;

						    col.title =  p_return.v_data.v_col_names[i];

							columnProperties.push(col);

						}

						var container = v_div_result;
						v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht = new Handsontable(container,
						{
							data: p_return.v_data.v_data,
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
									"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
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

					}

				},
				null,
				'box');
	}

}

/// <summary>
/// Queries and displays query results.
/// </summary>
function exportData() {

	var v_sql_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
	var v_sel_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_export_type.value;

	if (v_sql_value=='') {
		showAlert('Please provide a string.');
	}
	else {

		showConfirm('Are you sure you want to export data from the result of this query?',
				function() {

					var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_sql": v_sql_value, "p_select_value" : v_sel_value, "p_tab_name" : v_connTabControl.selectedTab.tag.tabControl.selectedTab.text});

					var start_time = new Date().getTime();

					execAjax('MainDB.aspx/ExportData',
							input,
							function(p_return) {

								var iframe = document.createElement('iframe');
								iframe.style.display = 'none';
								iframe.setAttribute("src", "DownloadFile.aspx");
								document.body.appendChild(iframe);
								setTimeout(function(){ iframe.parentElement.removeChild(iframe); }, 5000);

							},
							null,
							'box');

				});

	}

}

/// <summary>
/// Saves alter table changes.
/// </summary>
function saveAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_changedRowsColumnsInfo = [];
	var v_changedRowsColumnsData = [];

	var v_changedRowsConstraintsInfo = [];
	var v_changedRowsConstraintsData = [];

	var v_changedRowsIndexesInfo = [];
	var v_changedRowsIndexesData = [];

	for (var i=0; i < v_currTabTag.alterTableObject.infoRowsColumns.length; i++) {
		if (v_currTabTag.alterTableObject.infoRowsColumns[i].mode!=0) {
			v_currTabTag.alterTableObject.infoRowsColumns[i].index = i;
			v_changedRowsColumnsInfo.push(v_currTabTag.alterTableObject.infoRowsColumns[i]);
			v_changedRowsColumnsData.push(v_currTabTag.alterTableObject.htColumns.getDataAtRow(i));

		}
	}

	for (var i=0; i < v_currTabTag.alterTableObject.infoRowsConstraints.length; i++) {
		if (v_currTabTag.alterTableObject.infoRowsConstraints[i].mode!=0) {
			v_currTabTag.alterTableObject.infoRowsConstraints[i].index = i;
			v_changedRowsConstraintsInfo.push(v_currTabTag.alterTableObject.infoRowsConstraints[i]);
			var v_row = v_currTabTag.alterTableObject.htConstraints.getDataAtRow(i);

			v_row[2] = v_row[2].substring(95);

			v_changedRowsConstraintsData.push(v_row);
		}

	}

	for (var i=0; i < v_currTabTag.alterTableObject.infoRowsIndexes.length; i++) {
		if (v_currTabTag.alterTableObject.infoRowsIndexes[i].mode!=0) {
			v_currTabTag.alterTableObject.infoRowsIndexes[i].index = i;
			v_changedRowsIndexesInfo.push(v_currTabTag.alterTableObject.infoRowsIndexes[i]);
			var v_row = v_currTabTag.alterTableObject.htIndexes.getDataAtRow(i);

			v_row[2] = v_row[2].substring(91);

			v_changedRowsIndexesData.push(v_row);
		}

	}

	var v_new_table_name = v_currTabTag.txtTableName.value;


	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_mode" : v_currTabTag.alterTableObject.mode,"p_new_table_name": v_new_table_name, "p_original_table_name": v_currTabTag.alterTableObject.tableName, "p_data_columns": v_changedRowsColumnsData, "p_row_columns_info": v_changedRowsColumnsInfo, "p_data_constraints": v_changedRowsConstraintsData, "p_row_constraints_info": v_changedRowsConstraintsInfo, "p_data_indexes": v_changedRowsIndexesData, "p_row_indexes_info": v_changedRowsIndexesInfo});

	execAjax('MainDB.aspx/SaveAlterTable',
			input,
			function(p_return) {

				var v_div_commands_log = document.getElementById('div_commands_log_list');
				v_div_commands_log.innerHTML = '';
				var v_commands_log = '';

				var v_has_error = false;

				v_currTabTag.btSave.style.visibility = 'hidden';

				//Creating new table
				if (p_return.v_data.v_create_table_command!=null) {

					if (!p_return.v_data.v_create_table_command.error) {
						startAlterTable('alter',v_new_table_name);
						v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab('<img src="images/table_edit.png"/> ' + v_new_table_name);
					}
					else {
						v_has_error = true;

						v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_create_table_command.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_create_table_command.v_message + '<br/><br/>';

						v_currTabTag.btSave.style.visibility = 'visible';

					}


				}
				else {

					if (p_return.v_data.v_rename_table_command!=null) {

						if (!p_return.v_data.v_rename_table_command.error) {

							v_currTabTag.alterTableObject.tableName = v_new_table_name;
							$(v_currTabTag.txtTableName).removeClass('changed_input');
							v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab('<img src="images/table_edit.png"/> ' + v_new_table_name);


						}
						else {
							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_rename_table_command.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_rename_table_command.v_message + '<br/><br/>';

							v_currTabTag.btSave.style.visibility = 'visible';

						}


					}
					else {
						$(v_currTabTag.txtTableName).removeClass('changed_input');
					}

					// New column or delete column
					for (var i = p_return.v_data.v_columns_simple_commands_return.length-1; i >= 0; i--) {

						if (p_return.v_data.v_columns_simple_commands_return[i].mode==-1) {
							if (!p_return.v_data.v_columns_simple_commands_return[i].error) {

								v_currTabTag.alterTableObject.infoRowsColumns.splice(p_return.v_data.v_columns_simple_commands_return[i].index, 1);
								v_currTabTag.alterTableObject.htColumns.alter('remove_row', p_return.v_data.v_columns_simple_commands_return[i].index);


							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_message + '<br/><br/>';

								v_currTabTag.btSave.style.visibility = 'visible';
							}
						}
						else if (p_return.v_data.v_columns_simple_commands_return[i].mode==2) {
							if (!p_return.v_data.v_columns_simple_commands_return[i].error) {

								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].mode = 0;
								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].old_mode = -1;

								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].originalColName = v_currTabTag.alterTableObject.htColumns.getDataAtCell(p_return.v_data.v_columns_simple_commands_return[i].index,0);
								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].originalDataType = v_currTabTag.alterTableObject.htColumns.getDataAtCell(p_return.v_data.v_columns_simple_commands_return[i].index,1);
								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].originalNullable = v_currTabTag.alterTableObject.htColumns.getDataAtCell(p_return.v_data.v_columns_simple_commands_return[i].index,2);

							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_message  + '<br/><br/>';

								v_currTabTag.btSave.style.visibility = 'visible';
							}
						}

					}

					var v_has_group_error;

					// Altering column
					for (var i = p_return.v_data.v_columns_group_commands_return.length-1; i >= 0; i--) {

						v_has_group_error = false;

						if (p_return.v_data.v_columns_group_commands_return[i].alter_datatype!=null) {
							if (!p_return.v_data.v_columns_group_commands_return[i].alter_datatype.error) {

								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].originalDataType = v_currTabTag.alterTableObject.htColumns.getDataAtCell(p_return.v_data.v_columns_group_commands_return[i].index,1);

							}
							else {

								v_has_error = true;
								v_has_group_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_datatype.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_datatype.v_message  + '<br/><br/>';


							}

						}

						if (p_return.v_data.v_columns_group_commands_return[i].alter_nullable!=null) {
							if (!p_return.v_data.v_columns_group_commands_return[i].alter_nullable.error) {

								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].originalNullable = v_currTabTag.alterTableObject.htColumns.getDataAtCell(p_return.v_data.v_columns_group_commands_return[i].index,2);

							}
							else {

								v_has_error = true;
								v_has_group_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_nullable.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_nullable.v_message  + '<br/><br/>';


							}

						}

						if (p_return.v_data.v_columns_group_commands_return[i].alter_colname!=null) {
							if (!p_return.v_data.v_columns_group_commands_return[i].alter_colname.error) {

								v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].originalColName = v_currTabTag.alterTableObject.htColumns.getDataAtCell(p_return.v_data.v_columns_group_commands_return[i].index,0);

							}
							else {

								v_has_error = true;
								v_has_group_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_colname.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_colname.v_message  + '<br/><br/>';


							}

						}

						if (!v_has_group_error) {
							v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].mode = 0;
							v_currTabTag.alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].old_mode = -1;
						}

					}

					// New constraint or delete constraint
					for (var i = p_return.v_data.v_constraints_commands_return.length-1; i >= 0; i--) {

						if (p_return.v_data.v_constraints_commands_return[i].mode==-1) {
							if (!p_return.v_data.v_constraints_commands_return[i].error) {

								v_currTabTag.alterTableObject.infoRowsConstraints.splice(p_return.v_data.v_constraints_commands_return[i].index, 1);
								v_currTabTag.alterTableObject.htConstraints.alter('remove_row', p_return.v_data.v_constraints_commands_return[i].index);


							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_message + '<br/><br/>';

							}
						}
						else if (p_return.v_data.v_constraints_commands_return[i].mode==2) {
							if (!p_return.v_data.v_constraints_commands_return[i].error) {

								v_currTabTag.alterTableObject.infoRowsConstraints[p_return.v_data.v_constraints_commands_return[i].index].mode = 0;
								v_currTabTag.alterTableObject.infoRowsConstraints[p_return.v_data.v_constraints_commands_return[i].index].old_mode = -1;

							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_message  + '<br/><br/>';

							}
						}

					}

					// New index or delete index
					for (var i = p_return.v_data.v_indexes_commands_return.length-1; i >= 0; i--) {

						if (p_return.v_data.v_indexes_commands_return[i].mode==-1) {
							if (!p_return.v_data.v_indexes_commands_return[i].error) {

								v_currTabTag.alterTableObject.infoRowsIndexes.splice(p_return.v_data.v_indexes_commands_return[i].index, 1);
								v_currTabTag.alterTableObject.htIndexes.alter('remove_row', p_return.v_data.v_indexes_commands_return[i].index);


							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_message + '<br/><br/>';

							}
						}
						else if (p_return.v_data.v_indexes_commands_return[i].mode==2) {
							if (!p_return.v_data.v_indexes_commands_return[i].error) {

								v_currTabTag.alterTableObject.infoRowsIndexes[p_return.v_data.v_indexes_commands_return[i].index].mode = 0;
								v_currTabTag.alterTableObject.infoRowsIndexes[p_return.v_data.v_indexes_commands_return[i].index].old_mode = -1;

							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_message  + '<br/><br/>';

							}
						}

					}
				}

				if (v_has_error) {
					v_div_commands_log.innerHTML = v_commands_log;
					$('#div_commands_log').show();

				}
				else {
					v_currTabTag.btSave.style.visibility = 'hidden';
				}

				v_currTabTag.alterTableObject.htColumns.render();
				v_currTabTag.alterTableObject.htConstraints.render();
				v_currTabTag.alterTableObject.htIndexes.render();

			},
			null,
			'box');

}

/// <summary>
/// Saves edit data changes.
/// </summary>
function saveEditData() {

	var v_changedRowsInfo = [];
	var v_changedRowsData = [];

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	for (var i = 0; i < v_currTabTag.editDataObject.infoRows.length; i++) {
		if (v_currTabTag.editDataObject.infoRows[i].mode!=0) {
			v_currTabTag.editDataObject.infoRows[i].index = i;
			v_changedRowsInfo.push(v_currTabTag.editDataObject.infoRows[i]);
			v_changedRowsData.push(v_currTabTag.editDataObject.ht.getDataAtRow(i));
		}
	}

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table_name": v_currTabTag.editDataObject.table, "p_data_rows": v_changedRowsData, "p_rows_info": v_changedRowsInfo, "p_columns": v_currTabTag.editDataObject.columns, "p_pk_info" : v_currTabTag.editDataObject.pk});

	execAjax('MainDB.aspx/SaveEditData',
			input,
			function(p_return) {

				var v_div_commands_log = document.getElementById('div_commands_log_list');
				v_div_commands_log.innerHTML = '';
				var v_commands_log = '';

				var v_has_error = false;

				v_currTabTag.button_save.style.visibility = 'hidden';

				for (var i = p_return.v_data.length-1; i >= 0; i--) {

					if (p_return.v_data[i].mode==-1) {
						if (!p_return.v_data[i].error) {

							v_currTabTag.editDataObject.infoRows.splice(p_return.v_data[i].index, 1);
							v_currTabTag.editDataObject.ht.alter('remove_row', p_return.v_data[i].index);

						}
						else {

							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data[i].v_message + '<br/><br/>';

							v_currTabTag.button_save.style.visibility = 'visible';
						}
					}
					else if (p_return.v_data[i].mode==2) {
						if (!p_return.v_data[i].error) {

							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].mode = 0;
							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].old_mode = -1;
							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].changed_cols = [];

							//Creating pk
							var v_pk_list = [];

							for (var j = 0; j < v_currTabTag.editDataObject.pk.length; j++) {

								var v_pk = { v_column: v_currTabTag.editDataObject.pk[j].v_column,
											 v_value : v_currTabTag.editDataObject.ht.getDataAtCell(p_return.v_data[i].index, v_currTabTag.editDataObject.pk[j].v_index + 1)
										   };
							    v_pk_list.push(v_pk);
							}

							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].pk = v_pk_list;

						}
						else {

							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data[i].v_message  + '<br/><br/>';

							v_currTabTag.button_save.style.visibility = 'visible';
						}
					}
					else if (p_return.v_data[i].mode==1) {
						if (!p_return.v_data[i].error) {

							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].mode = 0;
							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].old_mode = -1;
							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].changed_cols = [];

							//Creating pk
							var v_pk_list = [];

							for (var j = 0; j < v_currTabTag.editDataObject.pk.length; j++) {

								var v_pk = { v_column: v_currTabTag.editDataObject.pk[j].v_column,
											 v_value : v_currTabTag.editDataObject.ht.getDataAtCell(p_return.v_data[i].index, v_currTabTag.editDataObject.pk[j].v_index + 1)
										   };
							    v_pk_list.push(v_pk);
							}

							v_currTabTag.editDataObject.infoRows[p_return.v_data[i].index].pk = v_pk_list;


						}
						else {

							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data[i].v_message  + '<br/><br/>';

							v_currTabTag.button_save.style.visibility = 'visible';
						}
					}

				}

				if (v_has_error) {
					v_div_commands_log.innerHTML = v_commands_log;
					$('#div_commands_log').show();

				}

				v_currTabTag.editDataObject.ht.render();


			},
			null,
			'box');

}

/// <summary>
/// Changes table name.
/// </summary>
function changeTableName() {

	var v_curr_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	v_curr_tab_tag.btSave.style.visibility = 'visible';
	$(v_curr_tab_tag.txtTableName).addClass('changed_input');

}

/// <summary>
/// Queries edit data window.
/// </summary>
function queryEditData() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table" : v_currTabTag.editDataObject.table, "p_filter" : v_currTabTag.editDataObject.editor.getValue(), "p_count": v_currTabTag.sel_filtered_data.value, "p_pk_list" : v_currTabTag.editDataObject.pk, "p_columns" : v_currTabTag.editDataObject.columns});

	v_currTabTag.button_save.style.visibility = 'hidden';

	execAjax('MainDB.aspx/QueryEditData',
			input,
			function(p_return) {

				if (v_currTabTag.editDataObject.pk.length==0) {
					if (v_currTabTag.editDataObject.firstRender)
						showAlert('Table has no primary key, existing rows will be read only.');

					v_currTabTag.editDataObject.firstRender = false;
					v_currTabTag.editDataObject.hasPK = false;
				}
				else
					v_currTabTag.editDataObject.hasPK = true;

				v_currTabTag.query_info.innerHTML = p_return.v_data.v_query_info;

				var columnProperties = [];

				var col = new Object();
				col.title = ' ';
				col.width = 25;
				columnProperties.push(col);

				for (var i = 0; i < v_currTabTag.editDataObject.columns.length; i++) {
				    var col = new Object();

				    if (!v_currTabTag.editDataObject.columns[i].v_is_pk)
				    	col.title =  '<b>' + v_currTabTag.editDataObject.columns[i].v_column + '</b> (' + v_currTabTag.editDataObject.columns[i].v_type + ')';
				    else
				    	col.title = '<img src="images/key.png" style="vertical-align: middle;"/> <b>' + v_currTabTag.editDataObject.columns[i].v_column + '</b> (' + v_currTabTag.editDataObject.columns[i].v_type + ')';

				    col.renderer = 'text';
					columnProperties.push(col);

				}

				var v_infoRows = [];

                for (var i=0; i < p_return.v_data.v_data.length; i++) {
                	var v_object = new Object();
                	v_object.mode = 0;
                	v_object.old_mode = -1;
                	v_object.index = i;
                	v_object.changed_cols = [];
                	v_object.pk = p_return.v_data.v_row_pk[i];
                	v_infoRows.push(v_object);
                }

				var v_div_result = v_currTabTag.div_result;

				if (v_div_result.innerHTML!='') {

					v_currTabTag.editDataObject.ht.destroy();
				}

				v_currTabTag.editDataObject.infoRows = v_infoRows;

				var container = v_div_result;
				v_currTabTag.editDataObject.ht = new Handsontable(container,
				{
					columns : columnProperties,
					data : p_return.v_data.v_data,
					colHeaders : true,
					rowHeaders : true,
					manualColumnResize: true,
					fixedColumnsLeft: 1,
					minSpareRows: 1,
					contextMenu: {
				      callback: function (key, options) {
				        if (key === 'edit_data') {
				          if (v_currTabTag.editDataObject.hasPK)
				          	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),true);
				          else
				          	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),false);
				        }
				      },
				      items: {
				        "edit_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">Edit Content</div>'}
				      }
				    },
					beforeChange: function (changes, source) {
                        if (!changes) {
                            return;
                        }

                        $.each(changes, function (index, element) {
                            var change = element;
                            var rowIndex = change[0];
                            var columnIndex = change[1];
                            var oldValue = change[2];
                            var newValue = change[3];

                            if (rowIndex >= v_currTabTag.editDataObject.infoRows.length)
                            {
                            	var v_object = new Object();
					        	v_object.mode = 2;
					        	v_object.old_mode = -1;
					        	v_object.changed_cols = [];
					        	v_object.index = v_currTabTag.editDataObject.infoRows.length;
					        	v_object.pk = null;

								v_currTabTag.editDataObject.infoRows.push(v_object);

								v_currTabTag.button_save.style.visibility = 'visible';

                            }

                            if(oldValue != newValue && v_currTabTag.editDataObject.infoRows[rowIndex].mode!=2){

                            	var v_found = false;

                            	if (v_currTabTag.editDataObject.infoRows[rowIndex].changed_cols.indexOf(columnIndex-1)==-1) {
                        			v_currTabTag.editDataObject.infoRows[rowIndex].changed_cols.push(columnIndex-1);
                        		}


                            	if (v_currTabTag.editDataObject.infoRows[rowIndex].mode!=-1) {
                            		v_currTabTag.editDataObject.infoRows[rowIndex].mode = 1;

                            	}
                            	else
                            		v_currTabTag.editDataObject.infoRows[rowIndex].old_mode = 1;

                                v_currTabTag.button_save.style.visibility = 'visible';

                            }
                        });
                    },
                    cells: function (row, col, prop) {

                    	var cellProperties = {};


					    if (v_currTabTag.editDataObject.infoRows[row]!=null) {

					    	if (!v_currTabTag.editDataObject.hasPK && v_currTabTag.editDataObject.infoRows[row].mode!=2) {
					    		if (col==0)
					    			cellProperties.renderer = grayEmptyRenderer;
					    		else
					    			cellProperties.renderer = grayRenderer;
    							cellProperties.readOnly = true;
					    	}
					    	else if (col==0) {
					    		cellProperties.renderer = editDataActionRenderer;
    							cellProperties.readOnly = true;
							}
    						else if (v_currTabTag.editDataObject.infoRows[row].mode==2) {
    							cellProperties.renderer = greenRenderer;
    						}
    						else if (v_currTabTag.editDataObject.infoRows[row].mode==-1) {
    							cellProperties.renderer = redRenderer;
    						}
    						else if (v_currTabTag.editDataObject.infoRows[row].mode==1) {
    							cellProperties.renderer = yellowRenderer;
    						}
    						else {
    							if (row % 2 == 0) {
    								cellProperties.renderer = blueRenderer;
    							}
    							else {
    								cellProperties.renderer = whiteRenderer;
    							}
    						}

						}
						else {
							if (col==0) {
					    		cellProperties.renderer = newRowRenderer;
    							cellProperties.readOnly = true;
							}
						}

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

					execAjax('MainDB.aspx/ClearCommandList',
					null,
					function(p_return) {

						hideCommandList();

					});

				});

}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function showCommandList() {

	execAjax('MainDB.aspx/GetCommandList',
			null,
			function(p_return) {

				$('#div_command_list').show();

				var v_height  = $(window).height() - $('#div_command_list_data').offset().top - 120;
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
																	"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
																}
														    },
														    cells: function (row, col, prop) {

															    var cellProperties = {};
															    if (row % 2 == 0)
																	cellProperties.renderer = blueRenderer;
															    return cellProperties;

															}
														});

			},
			null,
			'box');

}

/// <summary>
/// Initiates edit data window.
/// </summary>
/// <param name="p_table">Table name.</param>
function startEditData(p_table) {

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table" : p_table});

	execAjax('MainDB.aspx/StartEditData',
			input,
			function(p_return) {

				var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

				if (v_currTabTag.editDataObject!=null)
				if (v_currTabTag.editor!=null) {
					 v_currTabTag.editor.destroy();
				}


				v_currTabTag.editor.setValue(p_return.v_data.v_ini_orderby);
				v_currTabTag.editor.clearSelection();

				v_currTabTag.editDataObject = new Object();
				v_currTabTag.editDataObject.editor = v_currTabTag.editor;
				v_currTabTag.editDataObject.table = p_table;
				v_currTabTag.editDataObject.firstRender = true;
				v_currTabTag.editDataObject.pk = p_return.v_data.v_pk;
				v_currTabTag.editDataObject.columns = p_return.v_data.v_cols;

				queryEditData();

			});

}

/// <summary>
/// Initiates alter table window.
/// </summary>
/// <param name="p_mode">Alter or new table.</param>
/// <param name="p_table">Table name.</param>
function startAlterTable(p_mode,p_table) {

	

	var v_curr_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_curr_tab_tag.tabControl.selectTabIndex(0);

	v_curr_tab_tag.txtTableName.value = p_table;
	//document.getElementById('txt_tableNameAlterTable').style.backgroundColor = 'white';

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": p_table});

	execAjax('MainDB.aspx/AlterTableData',
				input,
				function(p_return) {

					if (!p_return.v_data.v_can_add_constraint && p_mode=='alter')
						$(v_curr_tab_tag.btNewConstraint).hide();
					else
						$(v_curr_tab_tag.btNewConstraint).show();

					if (!p_return.v_data.v_can_rename_table && p_mode=='alter') {
						$(v_curr_tab_tag.txtTableName).prop("readonly", true);
						v_curr_tab_tag.txtTableName.style.backgroundColor = 'rgb(242, 242, 242)';

					}
					else {
						$(v_curr_tab_tag.txtTableName).prop("readonly", false);
						$(v_curr_tab_tag.txtTableName).removeClass("txt_readonly");
					}

					/*$('#div_alter_table').show();

					var v_height  = $(window).height() - $('#div_alter_table_data').offset().top - 120;
					document.getElementById('div_alter_table_data').style.height = v_height + "px";
					document.getElementById('div_alter_constraint_data').style.height = v_height + "px";*/

					//Columns Table
					var v_div_result = v_curr_tab_tag.htDivColumns;

					var columnProperties = [];

					var col = new Object();
      				col.title =  'Column Name';
      				col.width = '100px';
     	 			columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  'Data Type';
      				col.width = '160px';
      				col.type = 'autocomplete';
	                col.source = p_return.v_data.v_data_types;
     	 			columnProperties.push(col);

					var col = new Object();
	                col.title =  'Nullable';
	                col.width = '80px';
	                col.type = 'dropdown';
	                col.source = ['YES','NO'];
	                columnProperties.push(col);

	                var col = new Object();
      				col.title =  ' ';
      				col.renderer = 'html';
     	 			columnProperties.push(col);


	                var v_infoRowsColumns = [];

	                for (var i=0; i < p_return.v_data.v_data_columns.length; i++) {
	                	var v_object = new Object();
	                	v_object.mode = 0;
	                	v_object.old_mode = -1;
	                	v_object.index = i;
	                	v_object.originalColName = p_return.v_data.v_data_columns[i][0];
	                	v_object.originalDataType = p_return.v_data.v_data_columns[i][1];
	                	v_object.originalNullable = p_return.v_data.v_data_columns[i][2];
	                	v_infoRowsColumns.push(v_object);
	                }



					if (v_curr_tab_tag.htDivColumns.innerHTML!='') {

						v_curr_tab_tag.alterTableObject.htColumns.destroy();

					}

					if (v_curr_tab_tag.htDivConstraints.innerHTML!='') {

						v_curr_tab_tag.alterTableObject.htConstraints.destroy();

					}

					if (v_curr_tab_tag.htDivIndexes.innerHTML!='') {

						v_curr_tab_tag.alterTableObject.htIndexes.destroy();

					}

					var container = v_div_result;

					v_curr_tab_tag.alterTableObject = new Object();

					v_curr_tab_tag.alterTableObject.tableName = p_table;
					v_curr_tab_tag.alterTableObject.infoRowsColumns = v_infoRowsColumns;
					v_curr_tab_tag.alterTableObject.cellChanges = [];
					v_curr_tab_tag.alterTableObject.mode = p_mode;
					v_curr_tab_tag.alterTableObject.window = 'columns';
					v_curr_tab_tag.alterTableObject.canAlterType = p_return.v_data.v_can_alter_type;
                	v_curr_tab_tag.alterTableObject.canAlterNullable = p_return.v_data.v_can_alter_nullable;
                	v_curr_tab_tag.alterTableObject.canRenameColumn = p_return.v_data.v_can_rename_column;
                	v_curr_tab_tag.alterTableObject.hasUpdateRule = p_return.v_data.v_has_update_rule;
					v_curr_tab_tag.alterTableObject.htConstraints = null;
					v_curr_tab_tag.alterTableObject.fkRefColumns = p_return.v_data.table_ref_columns;
					v_curr_tab_tag.alterTableObject.can_drop_column = p_return.v_data.v_can_drop_column;

					v_curr_tab_tag.alterTableObject.htColumns = new Handsontable(container,
					{
						data: p_return.v_data.v_data_columns,
						columns : columnProperties,
						colHeaders : true,
						rowHeaders : true,
						manualColumnResize: true,
						minSpareRows: 1,
						beforeChange: function (changes, source) {

	                        if (!changes) {
	                            return;
	                        }

	                        $.each(changes, function (index, element) {
	                            var change = element;
	                            var rowIndex = change[0];
	                            var columnIndex = change[1];
	                            var oldValue = change[2];
	                            var newValue = change[3];

	                            if (rowIndex >= v_curr_tab_tag.alterTableObject.infoRowsColumns.length)
	                            {
	                            	var v_object = new Object();
						        	v_object.mode = 2;
						        	v_object.old_mode = 2;
						        	v_object.originalColName = '';
						        	v_object.originalDataType = '';
						        	v_object.index = v_curr_tab_tag.alterTableObject.infoRowsColumns.length;
						        	v_object.nullable = '';

									v_curr_tab_tag.alterTableObject.infoRowsColumns.push(v_object);

									v_curr_tab_tag.btSave.style.visibility = 'visible';

	                            }

	                            if(oldValue != newValue && v_curr_tab_tag.alterTableObject.infoRowsColumns[rowIndex].mode!=2) {

	                            	if (v_curr_tab_tag.alterTableObject.infoRowsColumns[rowIndex].mode!=-1)
	                            		v_curr_tab_tag.alterTableObject.infoRowsColumns[rowIndex].mode = 1;
	                            	else
	                            		v_curr_tab_tag.alterTableObject.infoRowsColumns[rowIndex].old_mode = 1;

	                                v_curr_tab_tag.btSave.style.visibility = 'visible';

	                            }
	                        });

	                    },
	                    cells: function (row, col, prop) {

						    var cellProperties = {};

						    if (v_curr_tab_tag.alterTableObject.infoRowsColumns[row]!=null) {

						    	if (col==3) {
						    		if (v_curr_tab_tag.alterTableObject.can_drop_column || v_curr_tab_tag.alterTableObject.infoRowsColumns[row].mode==2)
						    			cellProperties.renderer = columnsActionRenderer;
						    		else
						    			cellProperties.renderer = grayEmptyRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_curr_tab_tag.alterTableObject.infoRowsColumns[row].mode==2) {
	    							cellProperties.renderer = greenHtmlRenderer;
	    						}
	    						else if (v_curr_tab_tag.alterTableObject.infoRowsColumns[row].mode==-1) {
	    							cellProperties.renderer = redHtmlRenderer;
	    						}
	    						else if (v_curr_tab_tag.alterTableObject.infoRowsColumns[row].mode== 1) {
	    							cellProperties.renderer = yellowHtmlRenderer;
	    						}
	    						else if ((!v_curr_tab_tag.alterTableObject.canAlterType && col==1) || (!v_curr_tab_tag.alterTableObject.canAlterNullable && col==2) || (!v_curr_tab_tag.alterTableObject.canRenameColumn && col==0)) {
	    							cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
	    						}
	    						else {
	    							if (row % 2 == 0)
	    								cellProperties.renderer = blueHtmlRenderer;
	    							else
	    								cellProperties.renderer = whiteHtmlRenderer;
	    						}

    						}
    						else {
    							if (col==3) {
						    		cellProperties.renderer = grayEmptyRenderer;
	    							cellProperties.readOnly = true;
								}
    						}

						    return cellProperties;

						}
					});

					v_curr_tab_tag.tabControl.tabList[0].tag = { ht: v_curr_tab_tag.alterTableObject.htColumns };

					//Constraints Table
					var v_div_result = v_curr_tab_tag.htDivConstraints;

					var columnProperties = [];

					var col = new Object();
      				col.title =  'Constraint Name';
      				col.width = '100px';
     	 			columnProperties.push(col);

					var col = new Object();
	                col.title =  'Type';
	                col.width = '100px';
	                col.type = 'dropdown';
	                col.source = ['Primary Key','Foreign Key','Unique'];
	                columnProperties.push(col);

	                var col = new Object();
      				col.title =  'Columns';
      				col.width = '140px';
     	 			columnProperties.push(col);

     	 			var col = new Object();
	                col.title =  'Referenced Table';
	                col.width = '140px';
	                col.type = 'autocomplete';
	                col.source = p_return.v_data.v_tables;
	                columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  'Referenced Columns';
      				col.width = '140px';
      				col.type = 'autocomplete';
     	 			columnProperties.push(col);

     	 			var col = new Object();
	                col.title =  'Delete Rule';
	                col.width = '100px';
	                col.type = 'autocomplete';
	                col.source = p_return.v_data.v_delete_rules;
	                columnProperties.push(col);

	                var col = new Object();
	                col.title =  'Update Rule';
	                col.width = '100px';
	                col.type = 'autocomplete';
	                col.source = p_return.v_data.v_update_rules;
	                columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  ' ';
      				col.renderer = 'html';
     	 			columnProperties.push(col);

     	 			var v_infoRowsConstraints = [];

	                for (var i=0; i < p_return.v_data.v_data_constraints.length; i++) {
	                	var v_object = new Object();
	                	v_object.mode = 0;
	                	v_object.old_mode = -1;
	                	v_object.index = i;
	                	v_infoRowsConstraints.push(v_object);
	                }

	                v_curr_tab_tag.alterTableObject.infoRowsConstraints = v_infoRowsConstraints;
	                v_curr_tab_tag.alterTableObject.canAlterConstraints = false;


					var container = v_div_result;


					v_curr_tab_tag.alterTableObject.htConstraints = new Handsontable(container,
					{
						data: p_return.v_data.v_data_constraints,
						columns : columnProperties,
						colHeaders : true,
						manualColumnResize: true,
						beforeChange: function (changes, source) {

	                        if (!changes) {
	                            return;
	                        }
	                        $.each(changes, function (index, element) {
	                            var change = element;
	                            var rowIndex = change[0];
	                            var columnIndex = change[1];
	                            var oldValue = change[2];
	                            var newValue = change[3];

	                            if(oldValue != newValue){

	                            	if (columnIndex == 3) {
	                            		getReferenceColumnsList(rowIndex,newValue);
	                            	}

	                            	v_curr_tab_tag.btSave.style.visibility = 'visible';
	                            }
	                        });

	                    },
						cells: function (row, col, prop) {

						    var cellProperties = {};

						    if (v_curr_tab_tag.alterTableObject.infoRowsConstraints[row]!=null) {

					    		var v_constraint_type = p_return.v_data.v_data_constraints[row][1];

						    	if (col==7 || (!v_curr_tab_tag.alterTableObject.hasUpdateRule && col==6)) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_curr_tab_tag.alterTableObject.infoRowsConstraints[row].mode==-1) {
	    							cellProperties.renderer = redHtmlRenderer;
	    						}
								else if ( (v_constraint_type!='Primary Key' && v_constraint_type!='Foreign Key' && v_constraint_type!='Unique') && (col==2) ) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if ( (v_constraint_type!='Foreign Key') && (col==3 || col==4 || col==5 || col==6) ) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_curr_tab_tag.alterTableObject.infoRowsConstraints[row].mode==2) {
	    							cellProperties.renderer = greenHtmlRenderer;
	    							cellProperties.readOnly = false;
	    						}
	    						else if (!v_curr_tab_tag.alterTableObject.canAlterConstraints) {
	    							cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
	    						}
	    						else {
	    							if (row % 2 == 0)
	    								cellProperties.renderer = blueHtmlRenderer;
	    							else
	    								cellProperties.renderer = whiteHtmlRenderer;
	    						}

	    						if (col==2)
						    		cellProperties.readOnly = true;

	    						if (col==4) {
							    	if (p_return.v_data.v_data_constraints[row][1]=='Foreign Key') {

							    		cellProperties.type='dropdown';
							    		cellProperties.source = v_curr_tab_tag.alterTableObject.fkRefColumns[row];

							    	}
						    	}

    						}

						    return cellProperties;

						}

					});

					v_curr_tab_tag.tabControl.tabList[1].tag = { ht: v_curr_tab_tag.alterTableObject.htConstraints };

					//Indexes Table
					var v_div_result = v_curr_tab_tag.htDivIndexes;

					var columnProperties = [];

					var col = new Object();
      				col.title =  'Index Name';
      				col.width = '100px';
     	 			columnProperties.push(col);

					var col = new Object();
	                col.title =  'Type';
	                col.width = '100px';
	                col.type = 'dropdown';
	                col.source = ['Non Unique','Unique'];
	                columnProperties.push(col);

	                var col = new Object();
      				col.title =  'Columns';
      				col.width = '160px';
     	 			columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  ' ';
      				col.renderer = 'html';
     	 			columnProperties.push(col);

     	 			var v_infoRowsIndexes = [];

	                for (var i=0; i < p_return.v_data.v_data_indexes.length; i++) {
	                	var v_object = new Object();
	                	v_object.mode = 0;
	                	v_object.old_mode = -1;
	                	v_object.index = i;
	                	v_infoRowsIndexes.push(v_object);
	                }

	                v_curr_tab_tag.alterTableObject.infoRowsIndexes = v_infoRowsIndexes;
	                v_curr_tab_tag.alterTableObject.canAlterIndexes = false;


					var container = v_div_result;

					v_curr_tab_tag.alterTableObject.htIndexes = new Handsontable(container,
					{
						data: p_return.v_data.v_data_indexes,
						columns : columnProperties,
						colHeaders : true,
						manualColumnResize: true,
						beforeChange: function (changes, source) {

	                        if (!changes) {
	                            return;
	                        }
	                        $.each(changes, function (index, element) {
	                            var change = element;
	                            var rowIndex = change[0];
	                            var columnIndex = change[1];
	                            var oldValue = change[2];
	                            var newValue = change[3];

	                            if(oldValue != newValue){

	                            	if (columnIndex == 3) {
	                            		getReferenceColumnsList(rowIndex,newValue);
	                            	}

	                            	v_curr_tab_tag.btSave.style.visibility = 'visible';
	                            }
	                        });

	                    },
						cells: function (row, col, prop) {

						    var cellProperties = {};

						    if (v_curr_tab_tag.alterTableObject.infoRowsIndexes[row]!=null) {

						    	if (col==3) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_curr_tab_tag.alterTableObject.infoRowsIndexes[row].mode==-1) {
	    							cellProperties.renderer = redHtmlRenderer;
	    						}
								else if (v_curr_tab_tag.alterTableObject.infoRowsIndexes[row].mode==2) {
	    							cellProperties.renderer = greenHtmlRenderer;
	    							cellProperties.readOnly = false;
	    						}
	    						else if (!v_curr_tab_tag.alterTableObject.canAlterIndexes) {
	    							cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
	    						}
	    						else {
	    							if (row % 2 == 0)
	    								cellProperties.renderer = blueHtmlRenderer;
	    							else
	    								cellProperties.renderer = whiteHtmlRenderer;
	    						}

	    						if (col==2)
						    		cellProperties.readOnly = true;


    						}

						    return cellProperties;
						}

					});

					v_curr_tab_tag.tabControl.tabList[2].tag = { ht: v_curr_tab_tag.alterTableObject.htIndexes };


				},
				null,
				'box');

}

/// <summary>
/// Retrieves list of pks and uniques referenced by FKs in specific table.
/// </summary>
/// <param name="p_row_index">Row number of current FK.</param>
/// <param name="p_table_name">Table name.</param>
function getReferenceColumnsList(p_row_index, p_table_name) {

	var v_currAlterTableObject = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.alterTableObject;

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table_name": p_table_name});

	execAjax('MainDB.aspx/RefreshRefColumnsList',
				input,
				function(p_return) {

					v_currAlterTableObject.fkRefColumns[p_row_index] = p_return.v_data;
					v_currAlterTableObject.htConstraints.render();

				},
				null,
				'box');

}

/// <summary>
/// Displays message to drop table.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropTable(p_node) {

	showConfirm('Are you sure you want to drop the table ' + p_node.text + '?',
				function() {

					dropTableConfirm(p_node);

				});

}

/// <summary>
/// Displays message to drop function.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropFunction(p_node) {

	showConfirm('Are you sure you want to drop the function ' + p_node.tag.id + '?',
				function() {

					dropFunctionConfirm(p_node);

				});

}

/// <summary>
/// Displays message to drop procedure.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropProcedure(p_node) {

	showConfirm('Are you sure you want to drop the procedure ' + p_node.tag.id + '?',
				function() {

					dropProcedureConfirm(p_node);

				});

}

/// <summary>
/// Displays message to delete table records.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function deleteData(p_node) {

	showConfirm('Are you sure you want to delete all records from table ' + p_node.text + '?',
				function() {

					deleteDataConfirm(p_node);

				});

}

/// <summary>
/// Drops table.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropTableConfirm(p_node) {

	p_node.tag.num_tables = 0;
	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": p_node.text});

	execAjax('MainDB.aspx/DropTable',
				input,
				function(p_return) {

					p_node.removeNode();

					p_node.parent.tag.num_tables = p_node.parent.tag.num_tables-1;
					p_node.parent.setText('Tables (' + p_node.parent.tag.num_tables + ')');

					showAlert('Table dropped.');

				},
				null,
				'box');

}

/// <summary>
/// Drops function.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropFunctionConfirm(p_node) {

	p_node.tag.num_tables = 0;
	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_function": p_node.tag.id});

	execAjax('MainDB.aspx/DropFunction',
				input,
				function(p_return) {

					p_node.removeNode();

					p_node.parent.tag.num_tables = p_node.parent.tag.num_tables-1;
					p_node.parent.setText('Functions (' + p_node.parent.tag.num_tables + ')');

					showAlert('Function dropped.');

				},
				null,
				'box');

}

/// <summary>
/// Drops procedure.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropProcedureConfirm(p_node) {

	p_node.tag.num_tables = 0;
	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_procedure": p_node.tag.id});

	execAjax('MainDB.aspx/DropProcedure',
				input,
				function(p_return) {

					p_node.removeNode();

					p_node.parent.tag.num_tables = p_node.parent.tag.num_tables-1;
					p_node.parent.setText('Procedures (' + p_node.parent.tag.num_tables + ')');

					showAlert('Procedure dropped.');

				},
				null,
				'box');

}

/// <summary>
/// Deletes table records.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function deleteDataConfirm(p_node) {

	p_node.tag.num_tables = 0;

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": p_node.text});

	execAjax('MainDB.aspx/DeleteData',
				input,
				function(p_return) {

					showAlert('Records deleted.');

				},
				null,
				'box');

}

/// <summary>
/// Triggered when X is pressed in specific record at the edit table data window.
/// </summary>
function deleteRowEditData() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	var v_data = v_currTabTag.editDataObject.ht.getData();
	var v_row = v_currTabTag.editDataObject.ht.getSelected()[0];

	if (v_currTabTag.editDataObject.infoRows[v_row].mode==2) {

		v_currTabTag.editDataObject.infoRows.splice(v_row,1);
		v_data.splice(v_row,1);
		v_currTabTag.editDataObject.ht.loadData(v_data);


	}
	else {

		var v_mode = v_currTabTag.editDataObject.infoRows[v_row].mode;
		v_currTabTag.editDataObject.infoRows[v_row].mode = v_currTabTag.editDataObject.infoRows[v_row].old_mode;
		v_currTabTag.editDataObject.infoRows[v_row].old_mode = v_mode;
		v_currTabTag.editDataObject.ht.render();

	}

	v_currTabTag.button_save.style.visibility = 'visible';

}

/// <summary>
/// Triggered when X is pressed in specific column at the alter table window.
/// </summary>
function dropColumnAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_data = v_currTabTag.alterTableObject.htColumns.getData();
	var v_row = v_currTabTag.alterTableObject.htColumns.getSelected()[0];

	if (v_currTabTag.alterTableObject.infoRowsColumns[v_row].mode==2) {

		v_currTabTag.alterTableObject.infoRowsColumns.splice(v_row,1);
		v_data.splice(v_row,1);

		v_currTabTag.alterTableObject.htColumns.loadData(v_data);

	}
	else {

		var v_mode = v_currTabTag.alterTableObject.infoRowsColumns[v_row].mode;
		v_currTabTag.alterTableObject.infoRowsColumns[v_row].mode = v_currTabTag.alterTableObject.infoRowsColumns[v_row].old_mode;
		v_currTabTag.alterTableObject.infoRowsColumns[v_row].old_mode = v_mode;

		v_currTabTag.alterTableObject.htColumns.loadData(v_data);

	}

	v_currTabTag.btSave.style.visibility = 'visible';

}

/// <summary>
/// Triggered when X is pressed in specific constraint at the alter table window.
/// </summary>
function dropConstraintAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_data = v_currTabTag.alterTableObject.htConstraints.getData();
	var v_row = v_currTabTag.alterTableObject.htConstraints.getSelected()[0];

	if (v_currTabTag.alterTableObject.infoRowsConstraints[v_row].mode==2) {

		v_currTabTag.alterTableObject.infoRowsConstraints.splice(v_row,1);
		v_data.splice(v_row,1);

		v_currTabTag.alterTableObject.htConstraints.loadData(v_data);

	}
	else {

		var v_mode = v_currTabTag.alterTableObject.infoRowsConstraints[v_row].mode;
		v_currTabTag.alterTableObject.infoRowsConstraints[v_row].mode = v_currTabTag.alterTableObject.infoRowsConstraints[v_row].old_mode;
		v_currTabTag.alterTableObject.infoRowsConstraints[v_row].old_mode = v_mode;

		v_currTabTag.alterTableObject.htConstraints.loadData(v_data);

	}

	v_currTabTag.btSave.style.visibility = 'visible';

}

/// <summary>
/// Triggered when X is pressed in specific index at the alter table window.
/// </summary>
function dropIndexAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_data = v_currTabTag.alterTableObject.htIndexes.getData();
	var v_row = v_currTabTag.alterTableObject.htIndexes.getSelected()[0];

	if (v_currTabTag.alterTableObject.infoRowsIndexes[v_row].mode==2) {

		v_currTabTag.alterTableObject.infoRowsIndexes.splice(v_row,1);
		v_data.splice(v_row,1);

		v_currTabTag.alterTableObject.htIndexes.loadData(v_data);

	}
	else {

		var v_mode = v_currTabTag.alterTableObject.infoRowsIndexes[v_row].mode;
		v_currTabTag.alterTableObject.infoRowsIndexes[v_row].mode = v_currTabTag.alterTableObject.infoRowsIndexes[v_row].old_mode;
		v_currTabTag.alterTableObject.infoRowsIndexes[v_row].old_mode = v_mode;

		v_currTabTag.alterTableObject.htIndexes.loadData(v_data);

	}

	v_currTabTag.btSave.style.visibility = 'visible';

}

/// <summary>
/// Adds new column at the alter table window.
/// </summary>
function newColumnAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_data = v_currTabTag.alterTableObject.htColumns.getData();

	var v_object = new Object();
	v_object.canAlterType = true;
	v_object.canAlterNullable = true;
	v_object.canRenameColumn = true;
	v_object.mode = 2;
	v_object.originalColName = '';
	v_object.originalDataType = '';
	v_object.nullable = '';

	v_currTabTag.alterTableObject.infoRowsColumns.push(v_object);

	v_data.push(['','','YES','<img src="images/tab_close.png" onclick="dropColumnAlterTable()"/>']);

	v_currTabTag.alterTableObject.htColumns.loadData(v_data);

	v_currTabTag.btSave.style.visibility = 'visible';

}

/// <summary>
/// Adds new index at the alter table window.
/// </summary>
function newIndexAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_data = v_currTabTag.alterTableObject.htIndexes.getData();

	var v_object = new Object();
	v_object.mode = 2;
	v_object.old_mode = 2;
	v_object.index = v_currTabTag.alterTableObject.infoRowsIndexes.length;


	v_currTabTag.alterTableObject.infoRowsIndexes.push(v_object);

	v_data.push(['','',"<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> ",'<img src="images/tab_close.png" onclick="dropIndexAlterTable()"/>']);

	v_currTabTag.alterTableObject.htIndexes.loadData(v_data);

	v_currTabTag.btSave.style.visibility = 'visible';

}

/// <summary>
/// Adds new constraint at the alter table window.
/// </summary>
function newConstraintAlterTable() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_data = v_currTabTag.alterTableObject.htConstraints.getData();

	var v_object = new Object();
	v_object.mode = 2;
	v_object.old_mode = 2;
	v_object.index = v_currTabTag.alterTableObject.infoRowsConstraints.length;


	v_currTabTag.alterTableObject.infoRowsConstraints.push(v_object);

	v_data.push(['','',"<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> ",'','','','','<img src="images/tab_close.png" onclick="dropConstraintAlterTable()"/>']);

	v_currTabTag.alterTableObject.htConstraints.loadData(v_data);

	v_currTabTag.btSave.style.visibility = 'visible';

}

/// <summary>
/// Adds column to right list at columns list window.
/// </summary>
function addColumnToList() {

	var v_select_left = document.getElementById("sel_columns_left");

	var v_select_right = document.getElementById("sel_columns_right");
	var option = document.createElement("option");
	option.text = v_select_left.options[v_select_left.selectedIndex].text;
	v_select_right.add(option);

	v_select_left.remove(v_select_left.selectedIndex);

}

/// <summary>
/// Adds column to left list at columns list window.
/// </summary>
function remColumnFromList() {

	var v_select_right = document.getElementById("sel_columns_right");

	var v_select_left = document.getElementById("sel_columns_left");
	var option = document.createElement("option");
	option.text = v_select_right.options[v_select_right.selectedIndex].text;
	v_select_left.add(option);

	v_select_right.remove(v_select_right.selectedIndex);

}

/// <summary>
/// Hides command history window.
/// </summary>
function hideCommandsLog() {

	$('#div_commands_log').hide();

}

/// <summary>
/// Hides column list window.
/// </summary>
function hideColumnSelection() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_select_right = document.getElementById('sel_columns_right');

	var v_first = true;
	var v_column_string = '';

	for (var i=0; i < v_select_right.options.length; i++) {
		if (!v_first)
			v_column_string += ', ';

		v_first = false;
		v_column_string += v_select_right.options[i].text;

	}

	if (v_currTabTag.alterTableObject.window=='constraints') {
		v_column_string = "<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_string;
		v_currTabTag.alterTableObject.htConstraints.setDataAtCell(v_currTabTag.alterTableObject.selectedConstraintRow, 2, v_column_string);
	}
	else {
		v_column_string = "<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> " + v_column_string;
		v_currTabTag.alterTableObject.htIndexes.setDataAtCell(v_currTabTag.alterTableObject.selectedIndexRow, 2, v_column_string);
	}
	$('#div_column_selection').hide();

}

/// <summary>
/// Displays columns list window for constraints.
/// </summary>
function showColumnSelectionConstraints() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	$("#sel_columns_left").empty();
	$("#sel_columns_right").empty();

	var v_select_left = document.getElementById('sel_columns_left');
	var v_select_right = document.getElementById('sel_columns_right');

	var v_selected = v_currTabTag.alterTableObject.htConstraints.getSelected();

	if (v_currTabTag.alterTableObject.infoRowsConstraints[v_selected[0]].mode==2) {

		v_currTabTag.alterTableObject.selectedConstraintRow = v_selected[0];

		var v_type = v_currTabTag.alterTableObject.htConstraints.getDataAtCell(v_selected[0],1);

		if (v_type=='Primary Key' || v_type=='Foreign Key' || v_type=='Unique') {

			var v_columns = v_currTabTag.alterTableObject.htConstraints.getDataAtCell(v_selected[0],v_selected[1]);
			v_columns = v_columns.substring(95);

			var v_constraint_columns_list;

			if (v_columns=='')
				v_constraint_columns_list = [];
			else
				v_constraint_columns_list = v_columns.split(', ')

			for (var i=0; i < v_constraint_columns_list.length; i++) {
				var option = document.createElement("option");
				option.text = v_constraint_columns_list[i];
				v_select_right.add(option);
			}

			var v_table_columns_list = v_currTabTag.alterTableObject.htColumns.getDataAtCol(0);

			for (var i=0; i < v_table_columns_list.length-1; i++) {
				if (v_constraint_columns_list.indexOf(v_table_columns_list[i])==-1) {
					var option = document.createElement("option");
					option.text = v_table_columns_list[i];
					v_select_left.add(option);
				}
			}

			$('#div_column_selection').show();

		}

	}

}

/// <summary>
/// Displays columns list window for indexes.
/// </summary>
function showColumnSelectionIndexes() {

	var v_currTabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	$("#sel_columns_left").empty();
	$("#sel_columns_right").empty();

	var v_select_left = document.getElementById('sel_columns_left');
	var v_select_right = document.getElementById('sel_columns_right');

	var v_selected = v_currTabTag.alterTableObject.htIndexes.getSelected();

	if (v_currTabTag.alterTableObject.infoRowsIndexes[v_selected[0]].mode==2) {

		v_currTabTag.alterTableObject.selectedIndexRow = v_selected[0];

		var v_type = v_currTabTag.alterTableObject.htIndexes.getDataAtCell(v_selected[0],1);


		var v_columns = v_currTabTag.alterTableObject.htIndexes.getDataAtCell(v_selected[0],v_selected[1]);
		v_columns = v_columns.substring(91);

		var v_index_columns_list;

		if (v_columns=='')
			v_index_columns_list = [];
		else
			v_index_columns_list = v_columns.split(', ')

		for (var i=0; i < v_index_columns_list.length; i++) {
			var option = document.createElement("option");
			option.text = v_index_columns_list[i];
			v_select_right.add(option);
		}

		var v_table_columns_list = v_currTabTag.alterTableObject.htColumns.getDataAtCol(0);

		for (var i=0; i < v_table_columns_list.length-1; i++) {
			if (v_index_columns_list.indexOf(v_table_columns_list[i])==-1) {
				var option = document.createElement("option");
				option.text = v_table_columns_list[i];
				v_select_left.add(option);
			}
		}

		$('#div_column_selection').show();

	}

}

function refreshChatMessages() {
	execAjax(
		'../MainDB.aspx/GetChatMessages',
		null,
		function(p_return) {
			var v_chatContent = document.getElementById('div_chat_content');
			var v_messageList = p_return.v_data;

			for(var i = 0; i < v_messageList.length; i++) {
				var v_messageDiv = document.createElement('div');
				v_messageDiv.classList.add('div_message');

				var v_lastUser = null;
				var v_chatMessages = v_chatContent.children;

				for(var j = v_chatMessages.length - 1; j >= 0 && v_lastUser == null; j--) {
					if(v_chatMessages[j].firstChild.classList.contains('div_message_user')) {
						v_lastUser = v_chatMessages[j].firstChild.innerHTML;
					}
				}

				if(v_lastUser != v_messageList[i].v_user_name) {
					var v_messageUser = document.createElement('div');
					v_messageUser.classList.add('div_message_user');
					v_messageUser.innerHTML = v_messageList[i].v_user_name;
					v_messageDiv.appendChild(v_messageUser);

					var v_messageTime = document.createElement('div');
					v_messageTime.classList.add('div_message_time');
					v_messageTime.innerHTML = '(' + v_messageList[i].v_timestamp.substring(11, 16) + ') ';
					v_messageDiv.appendChild(v_messageTime);
				}

				var v_messageText = document.createElement('div');
				v_messageText.classList.add('div_message_text');
				v_messageText.innerHTML = v_messageList[i].v_text;
				v_messageDiv.appendChild(v_messageText);

				v_chatContent.appendChild(v_messageDiv);
				v_chatContent.scrollTop = v_chatContent.scrollHeight;
			}

			if(v_messageList.length > 0) {
				var v_chatDetails = document.getElementById('div_chat_details');
				if(v_chatDetails.style.height == '0px') {
					var v_chatHeader = document.getElementById('div_chat_header');
					messageNotification = setInterval(
						function() {
							if(v_chatHeader.style.backgroundColor == 'rgb(74, 104, 150)') {
								v_chatHeader.style.backgroundColor = 'rgb(255, 147, 15)';
							}
							else {
								v_chatHeader.style.backgroundColor = 'rgb(74, 104, 150)';
							}
						},
						400
					);
				}
			}

			/*execAjax(
				'../MainDB.aspx/ViewChatMessages',
				JSON.stringify({
					p_message_list: v_messageList
				}),
				null,
				null,
				'box',
				false
			);*/
		},
		null,
		'box',
		false
	); 
}

function sendMessage() {
	var v_textarea = document.getElementById('textarea_chat_message');

	execAjax(
		'../MainDB.aspx/SendChatMessage',
		JSON.stringify({
			p_text: v_textarea.value
		}),
		function(p_return) {
			var v_messageDiv = document.createElement('div');
			v_messageDiv.classList.add('div_message');

			var v_lastUser = null;
			var v_chatMessages = document.getElementById('div_chat_content').children;

			for(var i = v_chatMessages.length - 1; i >= 0 && v_lastUser == null; i--) {
				if(v_chatMessages[i].firstChild.classList.contains('div_message_user')) {
					v_lastUser = v_chatMessages[i].firstChild.innerHTML;
				}
			}

			if(v_lastUser != 'me') {
				var v_messageUser = document.createElement('div');
				v_messageUser.classList.add('div_message_user');
				v_messageUser.innerHTML = 'me';
				v_messageDiv.appendChild(v_messageUser);

				var v_messageTime = document.createElement('div');
				v_messageTime.classList.add('div_message_time');
				v_messageTime.innerHTML = '(' + p_return.v_data.v_timestamp.substring(11, 16) + ') ';
				v_messageTime.title = p_return.v_data.v_timestamp.substring(0, 16).replace(new RegExp('-', 'g'), '/');
				v_messageDiv.appendChild(v_messageTime);
			}

			var v_messageText = document.createElement('div');
			v_messageText.classList.add('div_message_text');
			v_messageText.innerHTML = v_textarea.value;
			v_messageDiv.appendChild(v_messageText);

			var v_chatContent = document.getElementById('div_chat_content');
			v_chatContent.appendChild(v_messageDiv);
			v_chatContent.scrollTop = v_chatContent.scrollHeight;

			v_textarea.value = '';
		},
		null,
		'box',
		false
	); 
}

function clickChatHeader() {
	var v_chatDetails = document.getElementById('div_chat_details');

	if(v_chatDetails.style.height == '0px') {
		for(var i = 0; i < v_chatDetails.children.length; i++) {
			v_chatDetails.children[i].style.display = '';
		}

		setTimeout(
			function() {
				document.getElementById('button_chat_send_message').innerHTML = 'Send';
			},
			150
		);

		v_chatDetails.style.height = '315px';
		document.getElementById('div_chat_header').style.backgroundColor = 'rgb(74, 104, 150)';

		if(typeof messageNotification != 'undefined' && messageNotification != null) {
			clearInterval(messageNotification);
		}
	}
	else {
		v_chatDetails.style.height = '0px';

		setTimeout(
			function() {
				for(var i = 0; i < v_chatDetails.children.length; i++) {
					v_chatDetails.children[i].style.display = 'none';
				}
			},
			350
		);

		setTimeout(
			function() {
				document.getElementById('button_chat_send_message').innerHTML = '';
			},
			150
		);
	}
}

function refreshChatUsers() {
	execAjax(
		'../MainDB.aspx/GetChatUsers',
		null,
		function(p_return) {
			var v_chatLeftPanel = document.getElementById('div_chat_left_panel');
			v_chatLeftPanel.innerHTML = '';

			var v_userList = p_return.v_data;
			console.log(v_userList);
			for(var i = 0; i < v_userList.length; i++) {
				var v_userDiv = document.createElement('div');
				v_userDiv.id = v_userList[i].v_user_id;
				v_userDiv.classList.add('div_user');

				var v_userNameDiv = document.createElement('div');
				v_userNameDiv.classList.add('div_user_name');
				v_userNameDiv.innerHTML = v_userList[i].v_user_name;
				v_userDiv.appendChild(v_userNameDiv);

				var v_userStatusDiv = document.createElement('div');
				v_userStatusDiv.classList.add('div_user_status');

				if(v_userList[i].v_user_online == 1) {
					var v_userOnline = document.createElement('img');
					v_userOnline.src = 'images/status_green.png';

					v_userStatusDiv.appendChild(v_userOnline);
				}
				else {
					var v_userOnline = document.createElement('img');
					v_userOnline.src = 'images/status_red.png';

					v_userStatusDiv.appendChild(v_userOnline);
				}

				v_userDiv.appendChild(v_userStatusDiv);

				v_chatLeftPanel.appendChild(v_userDiv);
			}
		},
		null,
		'box',
		false
	); 
}