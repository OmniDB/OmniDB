/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function initCreateTabFunctions() {

  var v_createConnTabFunction = function() {

  	v_connTabControl.removeTabIndex(v_connTabControl.tabList.length-1);
  	var v_tab = v_connTabControl.createTab('<img src="/static/OmniDB_app/images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/> ' + v_connTabControl.tag.connections[0].v_alias,true,null,null,null,null,true);

  	v_connTabControl.selectTab(v_tab);

  	var v_html = "<div id='" + v_tab.id + "_div_left' class='div_left' style='float:left; position: relative; width:20%; '>" +
  	"<div style='padding-right: 12px;'><div id='" + v_tab.id + "_div_select_db' style='width: 100%; display: inline-block;'></div>" +
  	"</div>" +
  	"<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +
  	"<div style='width: 97%;'><div id='" + v_tab.id + "_tree' style='margin-top: 10px; overflow: auto;'></div>" +
  	"</div>" +
  	"<div id='html1'>" +
  	"</div>" +
  	"</div>" +
  	"<div id='" + v_tab.id + "_div_right' class='div_right' style='float:left; width:80%;'>" +
  	"<div id='" + v_tab.id + "_tabs'>" +
  	"<ul>" +
  	"</ul>" +
  	"</div>" +
  	"</div>";

  	var v_div = document.getElementById('div_' + v_tab.id);
  	v_div.innerHTML = v_html;

  	var v_height  = window.innerHeight - $('#' + v_tab.id + '_tree').offset().top - 60;
  	document.getElementById(v_tab.id + '_tree').style.height = v_height + "px";

  	var v_currTabControl = createTabControl(v_tab.id + '_tabs',0,null);

  	v_currTabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);

  	var v_tag = {
  		tabControl: v_currTabControl,
  		divTree: document.getElementById(v_tab.id + '_tree'),
  		divLeft: document.getElementById(v_tab.id + '_div_left'),
  		divRight: document.getElementById(v_tab.id + '_div_right'),
  		selectedDatabaseIndex: 0,
  		connTabControl: v_connTabControl
  	};

  	v_tab.tag = v_tag;

  	v_connTabControl.tag.createQueryTab();

  	v_tab.setClickFunction(function() { checkTabStatus(v_tab); });

  	var v_div_select_db = document.getElementById(v_tab.id + '_div_select_db');
  	v_div_select_db.innerHTML = v_connTabControl.tag.selectHTML;
  	$(v_div_select_db.childNodes[0]).msDropDown();

  	changeDatabase(0)

  	v_connTabControl.createTab('+',false,v_createConnTabFunction);

  }

  var v_createSnippetTabFunction = function() {

  	var v_tab = v_connTabControl.createTab('<img src="/static/OmniDB_app/images/snippet_medium.png"/> Snippets',false,null,null,null,null,true);

  	v_connTabControl.selectTab(v_tab);

  	var v_html = "<div id='" + v_tab.id + "_div_left' class='div_left' style='float:left; position: relative; width:15%; '>" +
  	"<div style='padding-right: 12px;'><div id='" + v_tab.id + "_div_select_db' style='width: 100%; display: inline-block;'></div>" +
  	"</div>" +
  	"<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +
  	"<div style='width: 97%;'><div id='" + v_tab.id + "_tree' style='margin-top: 10px; overflow: auto; font-family: 'Helvetica Neue', Helvetica, 'Segoe UI', Arial, freesans;'></div>" +
  	"</div>" +
  	"<div id='html1'>" +
  	"</div>" +
  	"</div>" +
  	"<div id='" + v_tab.id + "_div_right' class='div_right' style='float:left; width:85%;'>" +
  	"<div id='" + v_tab.id + "_tabs'>" +
  	"<ul>" +
  	"</ul>" +
  	"</div>" +
  	"</div>";

  	var v_div = document.getElementById('div_' + v_tab.id);
  	v_div.innerHTML = v_html;

  	var v_height  = window.innerHeight - $('#' + v_tab.id + '_tree').offset().top - 20;
  	document.getElementById(v_tab.id + '_tree').style.height = v_height + "px";

  	var v_currTabControl = createTabControl(v_tab.id + '_tabs',0,null);

  	v_currTabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);

  	var v_tag = {
  		tabControl: v_currTabControl,
  		divTree: document.getElementById(v_tab.id + '_tree'),
  		divLeft: document.getElementById(v_tab.id + '_div_left'),
  		divRight: document.getElementById(v_tab.id + '_div_right'),
  		connTabControl: v_connTabControl
  	};

    getTreeSnippets(v_tag.divTree.id);

  	v_tab.tag = v_tag;

    v_connTabControl.tag.createSnippetTextTab('Welcome');
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue('Welcome to OmniDB!');
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);

  }

  var v_createSnippetTextTabFunction = function(p_snippet) {

		var v_name = 'New Snippet';
		if (p_snippet)
			v_name = p_snippet;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('<span id="tab_title">' + v_name + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',false,null,null,null,null,true);
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;
		var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function() {
			closeSnippetTab(v_tab);
		};

		var v_html = "<div id='txt_snippet_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +
					 "<button id='bt_save_" + v_tab.id + "' class='bt_execute' title='Save' style='margin-top: 5px; margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='saveSnippetText();'><img src='/static/OmniDB_app/images/save.png' style='vertical-align: middle;'/></button>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_txt_snippet = document.getElementById('txt_snippet_' + v_tab.id);

    v_txt_snippet.style.height = window.innerHeight - $(v_txt_snippet).offset().top - 70 + 'px';

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_snippet_' + v_tab.id);
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");
		v_editor.commands.bindKey(".", "startAutocomplete");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

		v_txt_snippet.onclick = function() {

			v_editor.focus();

		};

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'snippet',
			editor: v_editor,
      editorDiv: v_txt_snippet,
			editorDivId: 'txt_snippet_' + v_tab.id,
			query_info: document.getElementById('div_query_info_' + v_tab.id),
			div_result: document.getElementById('div_result_' + v_tab.id),
			sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
			sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_close_span : v_tab_close_span,
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_save: document.getElementById('bt_save_' + v_tab.id),
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
			snippetTab: v_connTabControl.selectedTab,
      snippetObject: null
		};

		v_tab.tag = v_tag;

		v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createSnippetTextTab);

	};

  var v_createGraphTabFunction = function(p_name) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('<img src="/static/OmniDB_app/images/graph.png"/><span id="tab_title"> ' + p_name + '</span><span id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',false,null,null,null,null,true);
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;
		var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function() {
			closeGraphTab(v_tab);
		};

		var v_html = "<div id='graph_" + v_tab.id + "' style=' width: 100%; height: 200px;'></div>";

    var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_height  = window.innerHeight - $('#graph_' + v_tab.id).offset().top - 20;
		document.getElementById('graph_' + v_tab.id).style.height = v_height + "px";

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'graph',
			graph_div: document.getElementById('graph_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_close_span : v_tab_close_span,
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_save: document.getElementById('bt_save_' + v_tab.id),
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      network: null
		};

		v_tab.tag = v_tag;

		v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);

	};

  var v_createQueryTabFunction = function(p_table) {

		var v_name = 'Query';
		if (p_table)
			v_name = p_table;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('<span id="tab_title">' + v_name + '</span><span id="tab_loading" style="display:none;"><img src="/static/OmniDB_app/images/spin.svg"/></span><span id="tab_check" style="display:none;"><img src="/static/OmniDB_app/images/check.png"/></span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',false,null,renameTab,null,null,true);
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;
		var v_tab_loading_span = document.getElementById('tab_loading');
		v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
		var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function() {
			removeTab(v_tab);
		};
		var v_tab_check_span = document.getElementById('tab_check');
		v_tab_check_span.id = 'tab_check_' + v_tab.id;

		var v_html = "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +

					"<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
					 "<button id='bt_start_" + v_tab.id + "' class='bt_execute' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='querySQL();'><img src='/static/OmniDB_app/images/play.png' style='vertical-align: middle;'/></button>" +
           "<button id='bt_indent_" + v_tab.id + "' class='bt_execute' title='Indent SQL' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='indentSQL();'><img src='/static/OmniDB_app/images/indent.png' style='vertical-align: middle;'/></button>" +
					 "<select id='sel_filtered_data_" + v_tab.id + "'><option value='-3' >Script</option><option value='-2' >Execute</option><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option><option value='-1'>Query All rows</option></select>" +
           "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='margin-bottom: 5px; margin-left: 5px; display: none;' onclick='cancelSQL();'>Cancel</button>" +
					 "<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					 "<button class='bt_export' title='Export Data' style='display: none; margin-bottom: 5px; margin-left: 5px; float: right;' onclick='exportData();'><img src='/static/OmniDB_app/images/table_export.png' style='vertical-align: middle;'/></button>" +
					 "<select id='sel_export_type_" + v_tab.id + "' style='display: none; float: right;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option><option value='DBF' >DBF</option></select>" +
					 "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: hidden;'></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_height  = window.innerHeight - $('#div_result_' + v_tab.id).offset().top - 20;

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

            execAjax('/get_completions/',
                JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, p_prefix: prefix, p_sql: editor.getValue(), p_prefix_pos: editor.session.doc.positionToIndex(editor.selection.getCursor())}),
                function(p_return) {

                  if (p_return.v_data.length==0)
                    editor.insert('.');

                  wordlist = p_return.v_data;
                  callback(null, wordlist);

                },
                function(p_return) {
                  if (p_return.v_data.password_timeout) {
                    showPasswordPrompt(
                      v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                      function() {
                        v_editor.focus();
                      },
                      function() {
                        v_editor.focus();
                      }
                    );
                  }
                },
                'box',
                false);
          }
        }
      }
		}

		langTools.setCompleters([qtags]);
		v_editor.setOptions({enableBasicAutocompletion: true});

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'query',
			editor: v_editor,
			editorDivId: 'txt_query_' + v_tab.id,
			query_info: document.getElementById('div_query_info_' + v_tab.id),
			div_result: document.getElementById('div_result_' + v_tab.id),
			sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
			sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_loading_span : v_tab_loading_span,
			tab_close_span : v_tab_close_span,
			tab_check_span : v_tab_check_span,
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_save: document.getElementById('bt_save_' + v_tab.id),
      bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
			state : 0,
      context: null,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
			connTab: v_connTabControl.selectedTab
		};

		v_tab.tag = v_tag;

		v_tab.setClickFunction(function() { checkQueryStatus(v_tab); });

		v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);

	};

  var v_createEditDataTabFunction = function(p_table) {

    v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('<img src="/static/OmniDB_app/images/edit_data.png"/><span id="tab_title"> ' + p_table + '</span><span id="tab_loading" style="display:none;"><img src="/static/OmniDB_app/images/spin.svg"/></span><span id="tab_check" style="display:none;"><img src="/static/OmniDB_app/images/check.png"/></span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',false,null,null,null,removeTab,true);

    //Adding unique names to spans
    var v_tab_title_span = document.getElementById('tab_title');
    v_tab_title_span.id = 'tab_title_' + v_tab.id;
    var v_tab_loading_span = document.getElementById('tab_loading');
    v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
    var v_tab_close_span = document.getElementById('tab_close');
    v_tab_close_span.id = 'tab_close_' + v_tab.id;
    v_tab_close_span.onclick = function() {
      removeTab(v_tab);
    };
    var v_tab_check_span = document.getElementById('tab_check');
    v_tab_check_span.id = 'tab_check_' + v_tab.id;

    v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

    var v_html = "<div id='div_edit_data_select_" + v_tab.id + "' class='query_info' style='margin-top: 5px; margin-bottom: 5px; font-size: 14px;'>select * from " + p_table + " t</div>" +
           "<div id='txt_filter_data_" + v_tab.id + "' style=' width: 100%; height: 100px;border: 1px solid #c3c3c3;'></div>" +
           "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
           "<button class='bt_execute' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='queryEditData();'><img src='/static/OmniDB_app/images/play.png' style='vertical-align: middle;'/></button>" +
           "<select id='sel_filtered_data_" + v_tab.id + "' onchange='queryEditData()'><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option></select>" +
           "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='margin-bottom: 5px; margin-left: 5px; display: none;' onclick='cancelEditData();'>Cancel</button>" +
           "<div id='div_edit_data_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
           "<button id='bt_saveEditData_" + v_tab.id + "' onclick='saveEditData()' style='visibility: hidden; margin-left: 5px;'>Save Changes</button>" +
           "<div id='div_edit_data_data_" + v_tab.id + "' style='width: 100%; height: 250px; overflow: hidden;'></div>";

    var v_div = document.getElementById('div_' + v_tab.id);
    v_div.innerHTML = v_html;

    var v_height  = window.innerHeight - $('#div_edit_data_data_' + v_tab.id).offset().top - 20;

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

            execAjax('/get_completions_table/',
                JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                                "p_table": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.table,
                                "p_schema": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.schema}),
                function(p_return) {

                  if (p_return.v_data.length==0)
                    editor.insert('.');

                  wordlist = p_return.v_data;
                  callback(null, wordlist);

                },
                function(p_return) {
                  if (p_return.v_data.password_timeout) {
                    showPasswordPrompt(
                      v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                      function() {
                        v_editor.focus();
                      },
                      function() {
                        v_editor.focus();
                      }
                    );
                  }
                },
                'box',
                false);

          }

        }

      }
    }

    langTools.setCompleters([qtags]);
    v_editor.setOptions({enableBasicAutocompletion: true});

    var v_tag = {
      tab_id: v_tab.id,
      mode: 'edit',
      editor: v_editor,
      editorDivId: 'txt_filter_data_' + v_tab.id,
      query_info: document.getElementById('div_edit_data_query_info_' + v_tab.id),
      div_result: document.getElementById('div_edit_data_data_' + v_tab.id),
      sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
      button_save: document.getElementById('bt_saveEditData_' + v_tab.id),
      sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
      bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
      bt_save: document.getElementById('bt_save_' + v_tab.id),
      tab_title_span : v_tab_title_span,
      tab_loading_span : v_tab_loading_span,
      tab_close_span : v_tab_close_span,
      tab_check_span : v_tab_check_span,
      state: 0,
      context: null,
      tabControl: v_connTabControl.selectedTab.tag.tabControl,
      connTab: v_connTabControl.selectedTab
    };

    v_tab.tag = v_tag;

    v_tab.setClickFunction(function() { checkEditDataStatus(v_tab); });

    v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);

  };

	var v_createAlterTableTabFunction = function(p_table) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('<img src="/static/OmniDB_app/images/table_edit.png"/><span id="tab_title"> ' + p_table + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',false,null,null,null,removeTab,true);
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;
		var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function() {
			removeTab(v_tab);
		};
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		var v_html = "<span class='query_info' style='margin-left: 10px;'>Table Name: </span><input type='text' id='txt_tableNameAlterTable_" + v_tab.id + "' onchange='changeTableName()' style='margin: 10px;'/>" +
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

		var v_height  = window.innerHeight - $('#div_alter_table_data_' + v_tab.id).offset().top - 35;

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
			tab_title_span : v_tab_title_span,
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

		v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);

	};

  //Functions to create tabs globally
  v_connTabControl.tag.createConnTab = v_createConnTabFunction;
  v_connTabControl.tag.createSnippetTab = v_createSnippetTabFunction;

  //Functions to create tabs inside snippet tab
  v_connTabControl.tag.createSnippetTextTab = v_createSnippetTextTabFunction;

  //Functions to create tabs inside a connection tab
	v_connTabControl.tag.createQueryTab = v_createQueryTabFunction;
	v_connTabControl.tag.createEditDataTab = v_createEditDataTabFunction;
	v_connTabControl.tag.createAlterTableTab = v_createAlterTableTabFunction;
  v_connTabControl.tag.createGraphTab = v_createGraphTabFunction;
}
