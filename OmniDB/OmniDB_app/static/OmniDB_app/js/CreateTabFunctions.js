/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function initCreateTabFunctions() {

  var v_createConnTabFunction = function(p_index) {

  	v_connTabControl.removeTabIndex(v_connTabControl.tabList.length-1);
  	var v_tab = v_connTabControl.createTab(
        '<img src="/static/OmniDB_app/images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/> ' + v_connTabControl.tag.connections[0].v_alias,
        true,
        null,
        null,
        null,
        null,
        true,
        function() {
          if(this.tag != null) {
            checkTabStatus(this);
            refreshHeights(true);
          }
          if(this.tag != null && this.tag.tabControl != null && this.tag.tabControl.selectedTab.tag.editor != null) {
              this.tag.tabControl.selectedTab.tag.editor.focus();
          }
        }
    );

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
  		connTabControl: v_connTabControl,
      mode: 'connection'
  	};

  	v_tab.tag = v_tag;

  	v_connTabControl.tag.createQueryTab();

    var v_index = 0;
    if (p_index)
      v_index = p_index;

  	var v_div_select_db = document.getElementById(v_tab.id + '_div_select_db');
  	v_div_select_db.innerHTML = v_connTabControl.tag.selectHTML;
    v_div_select_db.childNodes[0].childNodes[v_index].selected=true
  	$(v_div_select_db.childNodes[0]).msDropDown();

  	changeDatabase(v_index)

  	v_connTabControl.createTab('+',false,v_createConnTabFunction);

    setTimeout(function() {
      refreshTreeHeight();
    },10);

  }

  var v_createSnippetTabFunction = function() {

  	var v_tab = v_connTabControl.createTab(
        '<img src="/static/OmniDB_app/images/snippet_medium.png"/> Snippets',
        false,
        null,
        null,
        null,
        null,
        true,
        function() {
          if(this.tag != null) {
            refreshHeights(true);
          }
          if(this.tag != null && this.tag.tabControl != null && this.tag.tabControl.selectedTab.tag.editor != null) {
              this.tag.tabControl.selectedTab.tag.editor.focus();
          }
        }
    );

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
  		connTabControl: v_connTabControl,
      mode: 'snippets'
  	};

    v_tab.tag = v_tag;

    getTreeSnippets(v_tag.divTree.id);

    v_connTabControl.tag.createSnippetTextTab('Welcome');
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue('Welcome to OmniDB!');
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);

    setTimeout(function() {
      refreshTreeHeight();
    },10);

  }

  var v_createSnippetTextTabFunction = function(p_snippet) {

		var v_name = 'New Snippet';
		if (p_snippet)
			v_name = p_snippet;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<span id="tab_title">' + v_name + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
            false,
            null,
            null,
            null,
            null,
            true,
            function() {
              if(this.tag != null) {
                refreshHeights();
              }
              if(this.tag != null && this.tag.editor != null) {
                  this.tag.editor.focus();
              }
            }
        );
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

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)

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

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createGraphTabFunction = function(p_name) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
      '<img src="/static/OmniDB_app/images/graph.png"/><span id="tab_title"> ' + p_name + '</span><span id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
      false,
      null,
      null,
      null,
      null,
      true,
      function() {
        if(this.tag != null) {
          refreshHeights();
        }
      });
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

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'graph',
			graph_div: document.getElementById('graph_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_close_span : v_tab_close_span,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      network: null
		};

		v_tab.tag = v_tag;

		var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createWebsiteTabFunction = function(p_name, p_site) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
      '<img src="/static/OmniDB_app/images/globe.png"/><span id="tab_title"> ' + p_name + '</span>',
      true,
      null,
      null,
      null,
      null,
      true,
      function() {
        if(this.tag != null) {
          refreshHeights();
        }
      });
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;

		var v_html = "<iframe id='website_" + v_tab.id + "' src='" + p_site + "' style=' width: 100%; height: 200px;'></iframe>";

    var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'website',
			iframe: document.getElementById('website_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
		};

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createWebsiteOuterTabFunction = function(p_name, p_site) {

		v_connTabControl.removeTabIndex(v_connTabControl.tabList.length-1);
		var v_tab = v_connTabControl.createTab(
      '<img src="/static/OmniDB_app/images/globe.png"/><span id="tab_title"> ' + p_name + '</span>',
      true,
      null,
      null,
      null,
      null,
      true,
      function() {
        if(this.tag != null) {
          refreshHeights();
        }
      });
		v_connTabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;

		var v_html = "<iframe id='website_" + v_tab.id + "' src='" + p_site + "' style=' width: 100%; height: 200px;'></iframe>";

    var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'website_outer',
			iframe: document.getElementById('website_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tabControl: v_connTabControl,
		};

		v_tab.tag = v_tag;

		v_connTabControl.createTab('+',false,v_createConnTabFunction);

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createMonitoringTabFunction = function(p_name, p_query, p_actions) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
      '<img src="/static/OmniDB_app/images/monitoring.png"/><span id="tab_title"> ' + p_name + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
      false,
      null,
      null,
      null,
      null,
      true,
      function() {
        if(this.tag != null) {
          refreshHeights();
        }
      });
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;
    var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function() {
			removeTab(v_tab);
		};

    var v_html = "<button id='bt_refresh_" + v_tab.id + "' class='bt_execute' title='Refresh' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;'>Refresh</button>" +
					 "<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					 "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>";

    var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_bt_refresh = document.getElementById('bt_refresh_' + v_tab.id);

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'monitoring',
			tab_title_span : v_tab_title_span,
      tab_close_span : v_tab_close_span,
      query_info: document.getElementById('div_query_info_' + v_tab.id),
			div_result: document.getElementById('div_result_' + v_tab.id),
      bt_refresh: v_bt_refresh,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      ht: null,
      query: p_query,
      actions: p_actions
		};

    //Adding action to button
    v_bt_refresh.onclick = function() {
			refreshMonitoring(v_tag);
		};

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
      refreshMonitoring(v_tag);
    },10);

	};

  var v_createQueryTabFunction = function(p_table) {

		var v_name = 'Query';
		if (p_table)
			v_name = p_table;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<span id="tab_title">' + v_name + '</span><span id="tab_loading" style="display:none;"><img src="/static/OmniDB_app/images/spin.svg"/></span><span id="tab_check" style="display:none;"><img src="/static/OmniDB_app/images/check.png"/></span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
            false,
            null,
            renameTab,
            null,
            null,
            true,
            function() {
              if(this.tag != null) {
                refreshHeights();
              }
              if(this.tag != null && this.tag.editor != null) {
                  this.tag.editor.focus();
                  checkQueryStatus(this);
              }
            }
        );
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
					"<button id='bt_start_" + v_tab.id + "' class='bt_execute' title='Run' style='margin-bottom: 5px; margin-right: 5px; display: inline-block; vertical-align: middle;' onclick='querySQL(0);'><img src='/static/OmniDB_app/images/play.png' style='vertical-align: middle;'/></button>" +
          "<button id='bt_indent_" + v_tab.id + "' class='bt_execute' title='Indent SQL' style='margin-bottom: 5px; margin-right: 5px; display: inline-block; vertical-align: middle;' onclick='indentSQL();'><img src='/static/OmniDB_app/images/indent.png' style='vertical-align: middle;'/></button>" +
					"<select id='sel_filtered_data_" + v_tab.id + "' style='display: none;'><option value='0' >Script</option><option selected='selected' value='1' >Query</option></select>" +
          "<button onclick='getExplain(0)' title='Explain' style='margin-bottom: 5px; margin-right: 5px; display: inline-block; vertical-align: middle;'><img src='/static/OmniDB_app/images/explain.png' style='vertical-align: middle;'/></button>" +
          "<button onclick='getExplain(1)' title='Explain Analyze' style='margin-bottom: 5px; display: inline-block; vertical-align: middle;'><img src='/static/OmniDB_app/images/analyze.png' style='vertical-align: middle;'/></button>" +
          "<button id='bt_fetch_more_" + v_tab.id + "' class='bt_execute' title='Run' style='margin-bottom: 5px; margin-left: 5px; display: none; vertical-align: middle;' onclick='querySQL(1);'>Fetch more</button>" +
          "<button id='bt_fetch_all_" + v_tab.id + "' class='bt_execute' title='Run' style='margin-bottom: 5px; margin-left: 5px; display: none; vertical-align: middle;' onclick='querySQL(2);'>Fetch all</button>" +
          "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='margin-bottom: 5px; margin-left: 5px; display: none; vertical-align: middle;' onclick='cancelSQL();'>Cancel</button>" +
					"<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					"<button class='bt_export' title='Export Data' style='display: none; margin-bottom: 5px; margin-left: 5px; float: right;' onclick='exportData();'><img src='/static/OmniDB_app/images/table_export.png' style='vertical-align: middle;'/></button>" +
					"<select id='sel_export_type_" + v_tab.id + "' style='display: none; float: right;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option><option value='DBF' >DBF</option></select>" +
          "        <div id='query_result_tabs_" + v_tab.id + "'>" +
          "            <ul>" +
          "            <li id='query_result_tabs_" + v_tab.id + "_tab1'>Data</li>" +
          "            <li id='query_result_tabs_" + v_tab.id + "_tab2'>Messages <div id='query_result_tabs_count_notices_" + v_tab.id + "' class='count_notices' style='display: none;'></div></li>" +
          "            <li id='query_result_tabs_" + v_tab.id + "_tab3'>Explain</li>" +
          "			</ul>" +
          "			<div id='div_query_result_tabs_" + v_tab.id + "_tab1'>" +
          "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_query_result_tabs_" + v_tab.id + "_tab2'>" +
          "<div id='div_notices_" + v_tab.id + "' style='width: 100%; line-height: 16px; user-select: initial;'></div>" +
          "			</div>" +
          "			<div id='div_query_result_tabs_" + v_tab.id + "_tab3'>" +
          "<div id='div_explain_" + v_tab.id + "' style='width: 100%; overflow: auto;'></div>" +
          "			</div></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_curr_tabs = createTabControl('query_result_tabs_' + v_tab.id,0,null);

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_query_' + v_tab.id);
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");
		v_editor.commands.bindKey(".", "startAutocomplete");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)

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
			querySQL(0);
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
            //return [];

            if (prefix!='') {

            addLoadingCursor();

            execAjax('/get_completions/',
                JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, p_prefix: prefix, p_sql: editor.getValue(), p_prefix_pos: editor.session.doc.positionToIndex(editor.selection.getCursor())}),
                function(p_return) {

                  removeLoadingCursor();

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
                      },
          						p_return.v_data.message
                    );
                  }
                  else {
                    removeLoadingCursor();
                    editor.insert('.');
                  }
                },
                'box',
                false);
          }
          else
            editor.insert('.');
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
      div_notices: document.getElementById('div_notices_' + v_tab.id),
      div_explain: document.getElementById('div_explain_' + v_tab.id),
      div_count_notices: document.getElementById('query_result_tabs_count_notices_' + v_tab.id),
			sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
			sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_loading_span : v_tab_loading_span,
			tab_close_span : v_tab_close_span,
			tab_check_span : v_tab_check_span,
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_fetch_more: document.getElementById('bt_fetch_more_' + v_tab.id),
      bt_fetch_all: document.getElementById('bt_fetch_all_' + v_tab.id),
      bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_save: document.getElementById('bt_save_' + v_tab.id),
      bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
			state : 0,
      context: null,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      queryTabControl: v_curr_tabs,
      currQueryTab: null,
			connTab: v_connTabControl.selectedTab,
      currDatabaseIndex: null
		};

		v_tab.tag = v_tag;

    var v_selectDataTabFunc = function() {
			v_curr_tabs.selectTabIndex(0);
      v_tag.currQueryTab = 'data';
      refreshHeights();
		}

    var v_selectMessageTabFunc = function() {

			v_curr_tabs.selectTabIndex(1);
      v_tag.currQueryTab = 'message';
			v_tag.div_count_notices.style.display = 'none';
      refreshHeights();
		}

    var v_selectExplainTabFunc = function() {
      v_curr_tabs.selectTabIndex(2);
      v_tag.currQueryTab = 'explain';
      refreshHeights();
    }

    v_tag.selectDataTabFunc    = v_selectDataTabFunc;
    v_tag.selectMessageTabFunc = v_selectMessageTabFunc;
    v_tag.selectExplainTabFunc = v_selectExplainTabFunc;

    v_curr_tabs.tabList[0].elementLi.onclick = v_selectDataTabFunc;
		v_curr_tabs.tabList[1].elementLi.onclick = v_selectMessageTabFunc;
		v_curr_tabs.tabList[2].elementLi.onclick = v_selectExplainTabFunc;

		v_selectDataTabFunc();

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createEditDataTabFunction = function(p_table) {

    v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
        '<img src="/static/OmniDB_app/images/edit_data.png"/><span id="tab_title"> ' + p_table + '</span><span id="tab_loading" style="display:none;"><img src="/static/OmniDB_app/images/spin.svg"/></span><span id="tab_check" style="display:none;"><img src="/static/OmniDB_app/images/check.png"/></span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
        false,
        null,
        null,
        null,
        removeTab,
        true,
        function() {
          if(this.tag != null) {
            refreshHeights();
          }
          if(this.tag != null && this.tag.editor != null) {
              this.tag.editor.focus();
              checkEditDataStatus(this);
          }
        }
    );

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

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)

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
                      },
          						p_return.v_data.message
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
      connTab: v_connTabControl.selectedTab,
      tabId: v_connTabControl.selectedTab.tag.tabControl.tabCounter
    };

    v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

  };

	var v_createAlterTableTabFunction = function(p_table) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<img src="/static/OmniDB_app/images/table_edit.png"/><span id="tab_title"> ' + p_table + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
            false,
            null,
            null,
            null,
            removeTab,
            true,
            function() {
              if(this.tag != null) {
                refreshHeights();
              }
            }
        );
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
			v_tag.alterTableObject.window = 'columns';
      refreshHeights();
		}

		v_curr_tabs.tabList[1].elementLi.onclick = function() {

			v_curr_tabs.selectTabIndex(1);
			v_tag.alterTableObject.window = 'constraints';
      refreshHeights();
		}

		v_curr_tabs.tabList[2].elementLi.onclick = function() {

			if (v_tag.alterTableObject.mode!='alter')
				showAlert('Create the table first.');
			else {
				v_curr_tabs.selectTabIndex(2);
				v_tag.alterTableObject.window = 'indexes';
        refreshHeights();
			}

		}

		v_curr_tabs.selectTabIndex(0);

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createDebuggerTabFunction = function(p_function) {

		var v_name = ' Debugger: ' + p_function;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<img src="/static/OmniDB_app/images/debug.png"/><span id="tab_title">' + v_name + '</span><span id="tab_loading" style="display:none;"><img src="/static/OmniDB_app/images/spin.svg"/></span><span id="tab_check" style="display:none;"><img src="/static/OmniDB_app/images/check.png"/></span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
            false,
            null,
            renameTab,
            null,
            null,
            true,
            function() {
              if(this.tag != null) {
                refreshHeights();
              }
              if(this.tag != null && this.tag.editor != null) {
                  this.tag.editor.focus();
              }
            }
        );
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

		var v_html = "<div id='txt_func_body_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +

					"<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
					"<button id='bt_step_" + v_tab.id + "' class='bt_execute' title='Step' style='margin-bottom: 5px; margin-right: 5px; display: inline-block; vertical-align: middle;' onclick='stepDebug();'><img src='/static/OmniDB_app/images/play.png' style='vertical-align: middle;'/></button>" +
					"<div id='div_debug_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
          "        <div id='debug_result_tabs_" + v_tab.id + "'>" +
          "            <ul>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab1'>Variables</li>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab2'>Messages <div id='debug_result_tabs_count_notices_" + v_tab.id + "' class='count_notices' style='display: none;'></div></li>" +
          "			</ul>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab1'>" +
          "<div id='div_variables_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab2'>" +
          "<div id='div_notices_" + v_tab.id + "' style='width: 100%; line-height: 16px; user-select: initial;'></div>" +
          "			</div></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_curr_tabs = createTabControl('debug_result_tabs_' + v_tab.id,0,null);

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_func_body_' + v_tab.id);
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");
		v_editor.commands.bindKey(".", "startAutocomplete");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.setReadOnly(true);

		document.getElementById('txt_func_body_' + v_tab.id).onclick = function() {

			v_editor.focus();

		};

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'debug',
			editor: v_editor,
			editorDivId: 'txt_func_body_' + v_tab.id,
			debug_info: document.getElementById('div_debug_info_' + v_tab.id),
			div_result: document.getElementById('div_variables_' + v_tab.id),
      div_notices: document.getElementById('div_notices_' + v_tab.id),
      div_count_notices: document.getElementById('debug_result_tabs_count_notices_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_loading_span : v_tab_loading_span,
			tab_close_span : v_tab_close_span,
			tab_check_span : v_tab_check_span,
			bt_start: document.getElementById('bt_step_' + v_tab.id),
			state : 0,
      context: null,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      queryTabControl: v_curr_tabs,
      currDebugTab: null,
			connTab: v_connTabControl.selectedTab,
      currDatabaseIndex: null,
      markerId: null,
      ht: null
		};

		v_tab.tag = v_tag;

    var v_selectVariableTabFunc = function() {
			v_curr_tabs.selectTabIndex(0);
      v_tag.currDebugTab = 'variable';
      refreshHeights();
		}

    var v_selectMessageTabFunc = function() {

			v_curr_tabs.selectTabIndex(1);
      v_tag.currDebugTab = 'message';
			v_tag.div_count_notices.style.display = 'none';
      refreshHeights();
		}


    v_tag.selectVariableTabFunc = v_selectVariableTabFunc;
    v_tag.selectMessageTabFunc = v_selectMessageTabFunc;

    v_curr_tabs.tabList[0].elementLi.onclick = v_selectVariableTabFunc;
		v_curr_tabs.tabList[1].elementLi.onclick = v_selectMessageTabFunc;

		v_selectVariableTabFunc();

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,v_connTabControl.tag.createQueryTab);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

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
  v_connTabControl.tag.createWebsiteTab = v_createWebsiteTabFunction;
  v_connTabControl.tag.createWebsiteOuterTab = v_createWebsiteOuterTabFunction;
  v_connTabControl.tag.createMonitoringTab = v_createMonitoringTabFunction;
  v_connTabControl.tag.createDebuggerTab = v_createDebuggerTabFunction;
}
