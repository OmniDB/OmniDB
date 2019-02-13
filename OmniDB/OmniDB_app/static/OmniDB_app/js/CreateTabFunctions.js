/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function initCreateTabFunctions() {

  var v_createConnTabFunction = function(p_index,p_create_query_tab = true) {

    if (v_connTabControl.tag.connections.length==0) {
      v_connTabControl.selectTabIndex(v_connTabControl.tabList.length-2);
      showAlert('Create connections first.')
    }
    else {

    	v_connTabControl.removeTabIndex(v_connTabControl.tabList.length-1);
    	var v_tab = v_connTabControl.createTab(
          '<span id="tab_title"><img src="/static/OmniDB_app/images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/> ' + v_connTabControl.tag.connections[0].v_alias + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i>',
          false,
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
    	"<div style='padding-right: 12px;'><div id='" + v_tab.id + "_div_select_group' style='width: 100%; margin-bottom: 5px; display: inline-block;'></div>" +
      "<div id='" + v_tab.id + "_div_select_db' style='width: 100%; display: inline-block;'></div>" +
    	"</div>" +
    	"<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +
    	"<div style='margin-right: 10px;'>" +
      "<div id='" + v_tab.id + "_details' class='connection_details' ></div>" +
      "<div id='" + v_tab.id + "_tree' style='margin-top: 5px; overflow: auto; height: 50%;'>" +
      "</div>" +
      "<div onmousedown='resizeTreeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +

      "<div id='tree_tabs_" + v_tab.id + "' style='position: relative;'>" +
      "<div id='" + v_tab.id + "_loading' class='div_loading_local' style='z-index: 1000;'></div>" +
      "<ul>" +
      "<li id='tree_tabs_" + v_tab.id + "_tab1'>Properties</li>" +
      "<li id='tree_tabs_" + v_tab.id + "_tab2'>DDL</li>" +
      "</ul>" +
      "<div id='div_tree_tabs_" + v_tab.id + "_tab1' style='position: relative;'>" +
      "<div id='" + v_tab.id + "_properties' style='width: 100%; overflow: auto;'></div>" +
      "</div>" +
      "<div id='div_tree_tabs_" + v_tab.id + "_tab2'>" +
      "<div id='" + v_tab.id + "_ddl' style='width: 100%; line-height: 16px;'></div>" +
      "</div>" +
      "</div>" +
      "</div>" +
    	"</div>" +
    	"<div id='" + v_tab.id + "_div_right' class='div_right' style='float:left; width:80%;'>" +
    	"<div id='" + v_tab.id + "_tabs'>" +
    	"<ul>" +
    	"</ul>" +
    	"</div>" +
    	"</div>";

      var v_tab_title_span = document.getElementById('tab_title');
      v_tab_title_span.id = 'tab_title_' + v_tab.id;
      var v_tab_close_span = document.getElementById('tab_close');
  		v_tab_close_span.id = 'tab_close_' + v_tab.id;
  		v_tab_close_span.onclick = function(e) {
        var v_this_tab = v_tab;
        beforeCloseTab(e,
          function() {
            var v_tabs_to_remove = [];
            for (var i=0; i < v_connTabControl.selectedTab.tag.tabControl.tabList.length; i++) {

              var v_tab = v_connTabControl.selectedTab.tag.tabControl.tabList[i];
              if (v_tab.tag!=null) {
                if (v_tab.tag.mode=='query' || v_tab.tag.mode=='edit' || v_tab.tag.mode=='debug' || v_tab.tag.mode=='console') {
                  var v_message_data = { tab_id: v_tab.tag.tab_id, tab_db_id: null };
                  if (v_tab.tag.mode=='query')
                    v_message_data.tab_db_id = v_tab.tag.tab_db_id;
                  v_tabs_to_remove.push(v_message_data);
                }
                else if (v_tab.tag.mode=='monitor_dashboard') {
                  v_tab.tag.tab_active = false;
                  cancelMonitorUnits(v_tab.tag);
                }
              }

              if (v_tab.tag.tabCloseFunction)
                v_tab.tag.tabCloseFunction(v_tab.tag);
            }
            if (v_tabs_to_remove.length>0)
              sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CloseTab, v_tabs_to_remove, false, null);
            v_this_tab.removeTab();
          });
  		};

    	var v_div = document.getElementById('div_' + v_tab.id);
    	v_div.innerHTML = v_html;

      var v_treeTabs = createTabControl('tree_tabs_' + v_tab.id,0,null);
      v_treeTabs.selectTabIndex(0);

    	var v_currTabControl = createTabControl(v_tab.id + '_tabs',0,null);

    	v_currTabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);

      //DDL editor
      var v_ddl_div = document.getElementById(v_tab.id + '_ddl');

  		var langTools = ace.require("ace/ext/language_tools");
  		var v_editor = ace.edit(v_tab.id + '_ddl');
      v_editor.$blockScrolling = Infinity;
  		v_editor.setTheme("ace/theme/" + v_editor_theme);
  		v_editor.session.setMode("ace/mode/sql");

  		v_editor.setFontSize(Number(v_editor_font_size));

  		v_editor.commands.bindKey("ctrl-space", null);

      //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
      v_editor.commands.bindKey("Cmd-,", null)
      v_editor.commands.bindKey("Ctrl-,", null)
      v_editor.commands.bindKey("Cmd-Delete", null)
      v_editor.commands.bindKey("Ctrl-Delete", null)
      v_editor.commands.bindKey("Ctrl-Up", null)
      v_editor.commands.bindKey("Ctrl-Down", null)
      v_editor.setReadOnly(true);

  		v_ddl_div.onclick = function() {

  			v_editor.focus();

  		};

      //Properties Grid
      var v_divProperties = document.getElementById(v_tab.id + '_properties');

      var columnProperties = [];

      var col = new Object();
      col.title =  'Property';
      col.readOnly = true;
      columnProperties.push(col);

      var col = new Object();
      col.title =  'Value';
      col.readOnly = true;
      columnProperties.push(col);

      var ht = new Handsontable(v_divProperties,
                          {
                            data: [],
                            columns : columnProperties,
                            colHeaders : true,
                            stretchH: 'all',
                            autoColumnSize : true,
                            manualColumnResize: false,
                            minSpareCols :0,
                            minSpareRows :0,
                            fillHandle:false,
                            contextMenu: {
                  						callback: function (key, options) {
                  							if (key === 'view_data') {
                  							  	editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),false);
                  							}
                                else if (key === 'copy') {
              										this.selectCell(options[0].start.row,options[0].start.col,options[0].end.row,options[0].end.col);
              									  document.execCommand('copy');
              									}
              								},
              								items: {
              									"copy": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-copy cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Copy</div>'},
              									"view_data": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
              								}
                				    },
                            cells: function (row, col, prop) {

                              var cellProperties = {};

                              if (row % 2 == 0)
                                cellProperties.renderer = blueHtmlRenderer;
                              else
                                cellProperties.renderer =whiteHtmlRenderer;


                              return cellProperties;

                            }
                          });

    	var v_tag = {
        tab_id: v_tab.id,
    		tabControl: v_currTabControl,
        tabTitle: v_tab_title_span,
        divDetails: document.getElementById(v_tab.id + '_details'),
    		divTree: document.getElementById(v_tab.id + '_tree'),
        divProperties: v_divProperties,
        gridProperties: ht,
        gridPropertiesCleared: true,
        divDDL: document.getElementById(v_tab.id + '_ddl'),
        divLoading: document.getElementById(v_tab.id + '_loading'),
    		divLeft: document.getElementById(v_tab.id + '_div_left'),
    		divRight: document.getElementById(v_tab.id + '_div_right'),
        divSelectDB: document.getElementById(v_tab.id + '_div_select_db'),
        divSelectGroup: document.getElementById(v_tab.id + '_div_select_group'),
    		selectedDatabaseIndex: 0,
    		connTabControl: v_connTabControl,
        mode: 'connection',
        tabCloseSpan: v_tab_close_span,
        firstTimeOpen: true,
        TreeTabControl: v_treeTabs,
        currTreeTab: null,
        ddlEditor: v_editor,
        consoleHistoryFecthed: false,
        consoleHistoryList: null
    	};

    	v_tab.tag = v_tag;

      var v_selectPropertiesTabFunc = function() {
  			v_treeTabs.selectTabIndex(0);
        v_tag.currTreeTab = 'properties';
        refreshTreeHeight();
  		}

      var v_selectDDLTabFunc = function() {
  			v_treeTabs.selectTabIndex(1);
        v_tag.currTreeTab = 'ddl';
        refreshTreeHeight();
  		}

      v_tag.selectPropertiesTabFunc    = v_selectPropertiesTabFunc;
      v_tag.selectDDLTabFunc = v_selectDDLTabFunc;

      v_treeTabs.tabList[0].elementLi.onclick = v_selectPropertiesTabFunc;
  		v_treeTabs.tabList[1].elementLi.onclick = v_selectDDLTabFunc;

      v_selectPropertiesTabFunc();

      var v_index = v_connTabControl.tag.connections[0].v_conn_id;
      if (p_index)
        v_index = p_index;

      v_tag.divSelectDB.innerHTML = v_connTabControl.tag.selectHTML;
      v_tag.divSelectDB.childNodes[0].value=v_index;

      v_tag.divSelectGroup.innerHTML = v_connTabControl.tag.selectGroupHTML;
      v_tag.divSelectGroup.childNodes[0].value=v_connTabControl.tag.groups[0].v_group_id;

      v_tab.tag.dd_object = $(v_tag.divSelectDB.childNodes[0]).msDropDown().data("dd");

      v_tab.tag.dd_group_object = $(v_tag.divSelectGroup.childNodes[0]).msDropDown().data("dd");

      changeDatabase(v_index);
      changeGroup(v_connTabControl.tag.groups[0].v_group_id);

      if (p_create_query_tab) {
         v_connTabControl.tag.createConsoleTab();
    	   v_connTabControl.tag.createQueryTab();
      }

      v_connTabControl.createTab('+',false,function(e) {showMenuNewTabOuter(e); },null,null,null,null,null,false);

      setTimeout(function() {
        refreshTreeHeight();
      },10);

    }

    endLoading();

  }

  var v_createSnippetTabFunction = function() {

  	var v_tab = v_connTabControl.createTab(
        '<i class="fas fa-align-left icon-tab-title"></i> Snippets',
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

  	v_currTabControl.createTab('+',false,function(e) { showMenuNewTab(e); },null,null,null,null,null,false);

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

    v_connTabControl.createTab('+',false,v_connTabControl.tag.createConnTab,false);

    setTimeout(function() {
      refreshTreeHeight();
    },10);

  }

  var v_createNewMonitorUnitTabFunction = function() {


		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<i class="fas fa-align-left icon-tab-title"></i> <span id="tab_title">Monitor Unit</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
          if (v_tab.tag.tabCloseFunction)
            v_tab.tag.tabCloseFunction(v_tab.tag);
        });
		};

		var v_html = "<div style='margin-top: 5px; margin-bottom: 5px;'>" +
    "<span class='query_info'>Name: </span><input type='text' id='txt_unit_name_" + v_tab.id + "' />" +
    "<span style='margin-left: 5px;' class='query_info'>Type: </span><select id='select_type_" + v_tab.id + "' class='sel_export_file_type'><option value='chart_append'>Chart (Append)</option><option value='chart'>Chart (No Append)</option><option value='grid'>Grid</option></select>" +
    "<span style='margin-left: 5px;' class='query_info'>Refresh Interval: </span><input type='text' id='txt_interval_" + v_tab.id + "' style='width: 100px;' onkeypress='return event.charCode >= 48 && event.charCode <= 57'/> <span class='query_info'>seconds</span>" +
    "</div>" +
    "<div style='margin-top: 5px; margin-bottom: 5px;'>" +
    "<span class='query_info'>Template: </span><select id='select_template_" + v_tab.id + "' onchange='selectUnitTemplate(this.value)' class='sel_export_file_type'  ><option value=-1>Select Template</option></select>" +
    "</div>" +
    "<div>" +
    "<div style='width:50%; display: inline-block; box-sizing: border-box; padding-right: 5px;'><div style='margin-bottom: 5px;' class='query_info'>Data Script:</div><div id='txt_data_" + v_tab.id + "' style=' width: 100%; height: 250px; border: 1px solid #c3c3c3;'></div></div>" +
    "<div style='width:50%; display: inline-block; box-sizing: border-box; padding-left: 5px;'><div style='margin-bottom: 5px;' class='query_info'>Chart Script:</div><div id='txt_script_" + v_tab.id + "' style=' width: 100%; height: 250px; border: 1px solid #c3c3c3;'></div></div>" +
    "</div>" +
		"<button class='bt_icon_only' title='Test' style='margin-top: 5px; margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='testMonitorScript();'><i class='fas fa-bolt fa-light'></i></button>" +
    "<button class='bt_icon_only' title='Save' style='margin-top: 5px; margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='saveMonitorScript();'><i class='fas fa-save fa-light'></i></button>" +
    "<div class='dashboard_unit_test'><div id='div_result_" + v_tab.id + "' ></div><div id='div_result_label_" + v_tab.id + "' class='dashboard_unit_legend_box'></div></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var langTools = ace.require("ace/ext/language_tools");

    var v_txt_script = document.getElementById('txt_script_' + v_tab.id);
    var v_editor = ace.edit('txt_script_' + v_tab.id);
    v_editor.$blockScrolling = Infinity;
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/python");
		v_editor.setFontSize(Number(v_editor_font_size));
		v_editor.commands.bindKey("ctrl-space", null);
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.commands.bindKey("Ctrl-Up", null)
    v_editor.commands.bindKey("Ctrl-Down", null)

    var v_txt_data = document.getElementById('txt_data_' + v_tab.id);
    var v_editor_data = ace.edit('txt_data_' + v_tab.id);
    v_editor_data.$blockScrolling = Infinity;
		v_editor_data.setTheme("ace/theme/" + v_editor_theme);
		v_editor_data.session.setMode("ace/mode/python");
		v_editor_data.setFontSize(Number(v_editor_font_size));
		v_editor_data.commands.bindKey("ctrl-space", null);
    v_editor_data.commands.bindKey("Cmd-,", null)
    v_editor_data.commands.bindKey("Ctrl-,", null)
    v_editor_data.commands.bindKey("Cmd-Delete", null)
    v_editor_data.commands.bindKey("Ctrl-Delete", null)
    v_editor_data.commands.bindKey("Ctrl-Up", null)
    v_editor_data.commands.bindKey("Ctrl-Down", null)

		v_txt_script.onclick = function() {

			v_editor.focus();

		};

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'monitor_unit',
			editor: v_editor,
      editor_data: v_editor_data,
      editorDiv: v_txt_script,
      editorDataDiv: v_txt_data,
			editorDivId: 'txt_script_' + v_tab.id,
			tab_title_span : v_tab_title_span,
			tab_close_span : v_tab_close_span,
      select_type: document.getElementById('select_type_' + v_tab.id),
      select_template: document.getElementById('select_template_' + v_tab.id),
      input_unit_name: document.getElementById('txt_unit_name_' + v_tab.id),
      input_interval: document.getElementById('txt_interval_' + v_tab.id),
      div_result: document.getElementById('div_result_' + v_tab.id),
      div_result_label: document.getElementById('div_result_label_' + v_tab.id),
      bt_test: document.getElementById('bt_test_' + v_tab.id),
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      unit_id: null,
      object: null,
      tabCloseSpan: v_tab_close_span,
      tabCloseFunction: function(p_tag) {
        try {
          p_tag.object.destroy();
        }
        catch(err) {
        }
      }
		};

		v_tab.tag = v_tag;

		v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createMonitorDashboardTabFunction = function() {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
      '<i class="fas fa-chart-bar fa-light"></i><span id="tab_title"> Monitoring</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
      false,
      null,
      null,
      null,
      null,
      true,
      function() {
        if(this.tag != null) {
          refreshHeights();
          refreshMonitorUnitsObjects();
          if (this.tag.unit_list_grid!=null) {
            showMonitorUnitList();
          }
        }
      });
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_title_span = document.getElementById('tab_title');
		v_tab_title_span.id = 'tab_title_' + v_tab.id;
    var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          closeMonitorDashboardTab(v_tab);
          if (v_tab.tag.tabCloseFunction)
            v_tab.tag.tabCloseFunction(v_tab.tag);
        });

		};

		var v_html = "<div id='monitor_dashboard_buttons_div'>" +
    "<button onclick='refreshMonitorDashboard(true)'>Refresh All</button>" +
    "<span style='position: relative; margin-left: 5px;'><button onclick='showMonitorUnitList()'>Manage Units</button>" +
    "<div id='unit_list_div_" + v_tab.id + "' class='dashboard_unit_list'><a class='modal-closer' onclick='closeMonitorUnitList()'>x</a>" +
    "<button onclick='editMonitorUnit()'>New Unit</button>" +
    "<div id='unit_list_grid_" + v_tab.id + "' class='unit_list_grid'></div>" +
    "</div>" +
    "</span>" +
    "</div>" +
    "<div id='dashboard_" + v_tab.id + "' class='dashboard_all'>" +
    "</div>";

    var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_txt_snippet = document.getElementById('txt_snippet_' + v_tab.id);

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'monitor_dashboard',
			dashboard_div: document.getElementById('dashboard_' + v_tab.id),
      unit_list_div: document.getElementById('unit_list_div_' + v_tab.id),
      unit_list_grid_div: document.getElementById('unit_list_grid_' + v_tab.id),
      unit_list_grid: null,
      unit_list_id_list: [],
			tab_title_span : v_tab_title_span,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      units: [],
      unit_sequence: 0,
      tab_active: true,
      connTabTag: v_connTabControl.selectedTab.tag,
      tabCloseSpan: v_tab_close_span,
      tabCloseFunction: function(p_tag) {
        for (var i=0; i<p_tag.units.length; i++) {
          try {
            p_tag.units[i].object.destroy();
          }
          catch(err) {
          }
        }
      }
		};

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createSnippetTextTabFunction = function(p_snippet) {

		var v_name = 'New Snippet';
		if (p_snippet)
			v_name = p_snippet;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<span id="tab_title">' + v_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          closeSnippetTab(v_current_tab);
        });
		};

		var v_html = "<div id='txt_snippet_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +
					 "<button id='bt_save_" + v_tab.id + "' class='bt_icon_only' title='Save' style='margin-top: 5px; margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='saveSnippetText();'><i class='fas fa-save fa-light'></i></button>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_txt_snippet = document.getElementById('txt_snippet_' + v_tab.id);

    v_txt_snippet.style.height = window.innerHeight - $(v_txt_snippet).offset().top - 70 + 'px';

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_snippet_' + v_tab.id);
    v_editor.$blockScrolling = Infinity;
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.commands.bindKey("Ctrl-Up", null)
    v_editor.commands.bindKey("Ctrl-Down", null)

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
      snippetObject: null,
      tabCloseSpan: v_tab_close_span
		};

		v_tab.tag = v_tag;

		v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function() { v_connTabControl.tag.createSnippetTextTab() });

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createGraphTabFunction = function(p_name) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
      '<i class="fab fa-hubspot icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i>',
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.network) {
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.network.destroy();
          }
          v_current_tab.removeTab();
        });
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
      network: null,
      tabCloseSpan: v_tab_close_span
		};

		v_tab.tag = v_tag;

		var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
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
      '<i class="fas fa-globe-americas icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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

    var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
		};

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
      tabCloseSpan: v_tab.elementClose
		};

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
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
      '<i class="fas fa-globe-americas icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
		v_connTabControl.selectTab(v_tab);

    var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
		};

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
      tabCloseSpan: v_tab.elementClose
		};

		v_tab.tag = v_tag;

    v_connTabControl.createTab('+',false,function(e) {showMenuNewTabOuter(e); },null,null,null,null,null,false);

    setTimeout(function() {
      refreshHeights();
    },10);

	};

  var v_createMonitoringTabFunction = function(p_name, p_query, p_actions) {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
      '<i class="fas fa-desktop fa-light"></i><span id="tab_title"> ' + p_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
		};

    var v_html = "<button id='bt_refresh_" + v_tab.id + "' class='bt_execute' title='Refresh' style='margin-bottom: 5px; margin-right: 5px; display: inline-block;'>Refresh</button>" +
					 "<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					 "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>";

    var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_bt_refresh = document.getElementById('bt_refresh_' + v_tab.id);

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'monitor_grid',
			tab_title_span : v_tab_title_span,
      tab_close_span : v_tab_close_span,
      query_info: document.getElementById('div_query_info_' + v_tab.id),
			div_result: document.getElementById('div_result_' + v_tab.id),
      bt_refresh: v_bt_refresh,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      ht: null,
      query: p_query,
      actions: p_actions,
      tabCloseSpan: v_tab_close_span
		};

    //Adding action to button
    v_bt_refresh.onclick = function() {
			refreshMonitoring(v_tag);
		};

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
      refreshMonitoring(v_tag);
    },10);

	};

  var v_createQueryTabFunction = function(p_table, p_tab_db_id) {

		var v_name = 'Query';
		if (p_table)
			v_name = p_table;

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<span id="tab_title">' + v_name + '</span><span id="tab_stub"><img style="width: 16px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i>',
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
		};
    var v_tab_check_span = document.getElementById('tab_check');
		v_tab_check_span.id = 'tab_check_' + v_tab.id;
    var v_tab_stub_span = document.getElementById('tab_stub');
		v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

		var v_html = "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +

					"<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
          "<div id='command_history_div_" + v_tab.id + "' class='query_command_history'><a class='modal-closer' onclick='closeCommandHistory()'>x</a>" +
          "<div id='command_history_header_" + v_tab.id + "' class='query_command_history_header'></div>" +
          "<div id='command_history_grid_" + v_tab.id + "' class='query_command_history_grid'></div>" +
          "</div><div class='tab_actions'>" +
					"<button id='bt_start_" + v_tab.id + "' class='bt_execute bt_icon_only' title='Run' onclick='querySQL(0);'><i class='fas fa-play fa-light'></i></button>" +
          "<button id='bt_indent_" + v_tab.id + "' class='bt_execute bt_icon_only' title='Indent SQL' onclick='indentSQL();'><i class='fas fa-indent fa-light'></i></button>" +
          "<button id='bt_history_" + v_tab.id + "' class='bt_execute bt_icon_only' title='Command History' onclick='showCommandList();'><i class='fas fa-list fa-light'></i></button>" +
          "<button id='bt_explain_" + v_tab.id + "' class='dbms_object postgresql_object bt_icon_only' onclick='getExplain(0)' title='Explain' style='display: none;'><i class='fas fa-search fa-light'></i></button>" +
          "<button id='bt_analyze_" + v_tab.id + "' class='dbms_object postgresql_object bt_icon_only' onclick='getExplain(1)' title='Explain Analyze' style='display: none;'><i class='fas fa-search-plus fa-light'></i></button>" +
          "<label class='dbms_object postgresql_object custom_checkbox query_info' style='margin: 0px 10px 0px 5px;'>Autocommit<input id='check_autocommit_" + v_tab.id + "' type='checkbox' checked='checked'><span class='checkmark'></span></label>" +
          "<i id='query_tab_status_" + v_tab.id + "' title='Not connected' class='fas fa-dot-circle tab-status tab-status-closed dbms_object postgresql_object'></i>" +
          "<span id='query_tab_status_text_" + v_tab.id + "' title='Not connected' class='tab-status-text query_info dbms_object postgresql_object'>Not connected</span>" +
          "<button id='bt_fetch_more_" + v_tab.id + "' class='bt_execute bt_fetch' title='Run' style='display: none; ' onclick='querySQL(1);'>Fetch more</button>" +
          "<button id='bt_fetch_all_" + v_tab.id + "' class='bt_execute bt_fetch' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(2);'>Fetch all</button>" +
          "<button id='bt_commit_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object bt_fetch' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(3);'>Commit</button>" +
          "<button id='bt_rollback_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object bt_fetch' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(4);'>Rollback</button>" +
          "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='display: none; ' onclick='cancelSQL();'>Cancel</button>" +
					"<div id='div_query_info_" + v_tab.id + "' class='query_info query_info_summary' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
					"<button class='bt_export' title='Export Data' style='margin-bottom: 5px; margin-left: 5px; float: right;' onclick='exportData();'><i class='fas fa-file-export fa-light'></i></button>" +
					"<select id='sel_export_type_" + v_tab.id + "' class='sel_export_file_type' style='float: right;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option></select></div>" +
          "        <div id='query_result_tabs_" + v_tab.id + "'>" +
          "            <ul>" +
          "            <li id='query_result_tabs_" + v_tab.id + "_tab1'>Data</li>" +
          "            <li id='query_result_tabs_" + v_tab.id + "_tab2' class='dbms_object postgresql_object' style='display: none;'>Messages <div id='query_result_tabs_count_notices_" + v_tab.id + "' class='count_notices' style='display: none;'></div></li>" +
          "            <li id='query_result_tabs_" + v_tab.id + "_tab3' class='dbms_object postgresql_object' style='display: none;'>Explain</li>" +
          "			</ul>" +
          "			<div id='div_query_result_tabs_" + v_tab.id + "_tab1'>" +
          "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_query_result_tabs_" + v_tab.id + "_tab2'>" +
          "<div id='div_notices_" + v_tab.id + "' class='query_result' style='width: 100%; line-height: 16px; user-select: initial;'></div>" +
          "			</div>" +
          "			<div id='div_query_result_tabs_" + v_tab.id + "_tab3'>" +
          "<div id='div_explain_" + v_tab.id + "' style='width: 100%; overflow: auto;'></div>" +
          "			</div></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_curr_tabs = createTabControl('query_result_tabs_' + v_tab.id,0,null);

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_query_' + v_tab.id);
    v_editor.$blockScrolling = Infinity;
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");

		v_editor.setFontSize(Number(v_editor_font_size));

		//v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.commands.bindKey("Ctrl-Up", null)
    v_editor.commands.bindKey("Ctrl-Down", null)

		document.getElementById('txt_query_' + v_tab.id).onclick = function() {

			v_editor.focus();

		};


    var v_tab_db_id = null;
    if (p_tab_db_id)
      v_tab_db_id = p_tab_db_id;

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
      tab_stub_span : v_tab_stub_span,
      query_tab_status: document.getElementById('query_tab_status_' + v_tab.id),
      query_tab_status_text: document.getElementById('query_tab_status_text_' + v_tab.id),
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_fetch_more: document.getElementById('bt_fetch_more_' + v_tab.id),
      bt_fetch_all: document.getElementById('bt_fetch_all_' + v_tab.id),
      bt_commit: document.getElementById('bt_commit_' + v_tab.id),
      bt_rollback: document.getElementById('bt_rollback_' + v_tab.id),
      bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_indent: document.getElementById('bt_indent_' + v_tab.id),
      bt_explain: document.getElementById('bt_explain_' + v_tab.id),
      bt_analyze: document.getElementById('bt_analyze_' + v_tab.id),
      bt_history: document.getElementById('bt_history_' + v_tab.id),
      bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
      bt_export: document.getElementById('bt_export_' + v_tab.id),
      check_autocommit: document.getElementById('check_autocommit_' + v_tab.id),
			state : 0,
      context: null,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      queryTabControl: v_curr_tabs,
      currQueryTab: null,
			connTab: v_connTabControl.selectedTab,
      currDatabaseIndex: null,
      tab_db_id: v_tab_db_id,
      tabCloseSpan: v_tab_close_span,
      tempData: [],
      commandHistory: {
           div: document.getElementById('command_history_div_' + v_tab.id),
           headerDiv: document.getElementById('command_history_header_' + v_tab.id),
           gridDiv: document.getElementById('command_history_grid_' + v_tab.id),
           grid: null,
           currentPage: 1,
           pages: 1,
           spanNumPages: null,
           spanCurrPage: null,
           inputStartedFrom: null,
           inputStartedFromLastValue: null,
           inputStartedTo: null,
           inputStartedToLastValue: null,
           inputCommandContains: null,
           inputCommandContainsLastValue: null
       }
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

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

    adjustQueryTabObjects(false);
    v_editor.focus();

	};

  var v_createConsoleTabFunction = function() {

		v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
		var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
            '<i class="fas fa-terminal icon-tab-title"></i><span> Console</span><span id="tab_stub"><img style="width: 16px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
              if(this.tag != null && this.tag.editor_input != null) {
                  this.tag.editor_input.focus();
                  checkConsoleStatus(this);
              }
            }
        );
		v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

		//Adding unique names to spans
		var v_tab_loading_span = document.getElementById('tab_loading');
		v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
		var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
		};
    var v_tab_check_span = document.getElementById('tab_check');
		v_tab_check_span.id = 'tab_check_' + v_tab.id;
    var v_tab_stub_span = document.getElementById('tab_stub');
		v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

		var v_html = "<div id='txt_console_" + v_tab.id + "' style=' width: 100%; height: 120px; border: 1px solid #c3c3c3;'></div>" +
					"<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
          "<div id='console_history_div_" + v_tab.id + "' class='console_command_history'><a class='modal-closer' onclick='closeConsoleHistory()'>x</a>" +
          "<div id='console_history_grid_" + v_tab.id + "' class='console_command_history_grid'></div>" +
          "</div>" +
          "</span>" +
          "</div>" +
          "<div class='tab_actions'>" +
          "<button id='bt_start_" + v_tab.id + "' class='bt_icon_only' title='Run' onclick='consoleSQL(false);'><i class='fas fa-play fa-light'></i></button>" +
          "<button id='bt_indent_" + v_tab.id + "' class='bt_icon_only' title='Indent SQL' onclick='indentSQL();'><i class='fas fa-indent fa-light'></i></button>" +
          "<button id='bt_clear_" + v_tab.id + "' class='bt_icon_only' title='Clear Console' onclick='clearConsole();'><i class='fas fa-broom fa-light'></i></button>" +
          "<button id='bt_history_" + v_tab.id + "' class='bt_icon_only' title='Command History' onclick='showConsoleHistory();'><i class='fas fa-list fa-light'></i></button>" +
          "<label class='dbms_object postgresql_object custom_checkbox query_info' style='margin: 0px 10px 0px 5px;'>Autocommit<input id='check_autocommit_" + v_tab.id + "' type='checkbox' checked='checked'><span class='checkmark'></span></label>" +
          "<i id='query_tab_status_" + v_tab.id + "' title='Not connected' class='fas fa-dot-circle tab-status tab-status-closed dbms_object postgresql_object'></i>" +
          "<span id='query_tab_status_text_" + v_tab.id + "' title='Not connected' class='tab-status-text query_info dbms_object postgresql_object'>Not connected</span>" +
          "<button id='bt_fetch_more_" + v_tab.id + "' class='bt_execute bt_fetch' title='Fetch More' style='display: none; ' onclick='consoleSQL(false,1);'>Fetch more</button>" +
          "<button id='bt_fetch_all_" + v_tab.id + "' class='bt_execute bt_fetch' title='Fetch All' style='margin-left: 5px; display: none; ' onclick='consoleSQL(false,2);'>Fetch all</button>" +
          "<button id='bt_skip_fetch_" + v_tab.id + "' class='bt_execute bt_fetch' title='Skip Fetch' style='margin-left: 5px; display: none; ' onclick='consoleSQL(false,3);'>Skip Fetch</button>" +
          "<button id='bt_commit_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object bt_fetch' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(3);'>Commit</button>" +
          "<button id='bt_rollback_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object bt_fetch' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(4);'>Rollback</button>" +
          "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style=' display: none;' onclick='cancelConsole();'>Cancel</button>" +
					"<div id='div_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
          "</div>" +
          "<div id='txt_input_" + v_tab.id + "' style=' width: 100%; height: 150px; border: 1px solid #c3c3c3;'></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor1 = ace.edit('txt_input_' + v_tab.id);
    v_editor1.$blockScrolling = Infinity;
		v_editor1.setTheme("ace/theme/" + v_editor_theme);
		v_editor1.session.setMode("ace/mode/sql");


		v_editor1.setFontSize(Number(v_editor_font_size));

		//v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor1.commands.bindKey("Cmd-,", null)
    v_editor1.commands.bindKey("Ctrl-,", null)
    v_editor1.commands.bindKey("Cmd-Delete", null)
    v_editor1.commands.bindKey("Ctrl-Delete", null)
    v_editor1.commands.bindKey("Ctrl-Up", null)
    v_editor1.commands.bindKey("Ctrl-Down", null)

		document.getElementById('txt_input_' + v_tab.id).onclick = function() {

			v_editor1.focus();

		};

    v_editor1.focus();

    var v_editor2 = ace.edit('txt_console_' + v_tab.id);
    v_editor2.renderer.setOption('showLineNumbers', false);
    v_editor2.setOptions({
      //fontFamily: '"Poppins", sans-serif'
    });
    v_editor2.$blockScrolling = Infinity;
		v_editor2.setTheme("ace/theme/" + v_editor_theme);

		v_editor2.setFontSize(Number(v_editor_font_size));

		//v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor2.commands.bindKey("Cmd-,", null)
    v_editor2.commands.bindKey("Ctrl-,", null)
    v_editor2.commands.bindKey("Cmd-Delete", null)
    v_editor2.commands.bindKey("Ctrl-Delete", null)
    v_editor2.commands.bindKey("Ctrl-Up", null)
    v_editor2.commands.bindKey("Ctrl-Down", null)



		document.getElementById('txt_console_' + v_tab.id).onclick = function() {

			v_editor2.focus();

		};

		v_editor2.setOptions({enableBasicAutocompletion: true});
    v_editor2.setValue('>> ' + v_connTabControl.selectedTab.tag.consoleHelp)
    v_editor2.setReadOnly(true);
    v_editor2.clearSelection();

    v_editor1.commands.bindKey("Enter",
    function() {
      v_editor1.session.insert(v_editor1.getCursorPosition(),'\n');
      consoleSQL();
    });

		var v_tag = {
			tab_id: v_tab.id,
			mode: 'console',
			editor_input: v_editor1,
      editor_console: v_editor2,
      editorDivId: 'txt_console_' + v_tab.id,
			div_console: document.getElementById('txt_console_' + v_tab.id),
      div_result: document.getElementById('txt_input_' + v_tab.id),
      query_info: document.getElementById('div_query_info_' + v_tab.id),
      query_tab_status: document.getElementById('query_tab_status_' + v_tab.id),
      query_tab_status_text: document.getElementById('query_tab_status_text_' + v_tab.id),
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_fetch_more: document.getElementById('bt_fetch_more_' + v_tab.id),
      bt_fetch_all: document.getElementById('bt_fetch_all_' + v_tab.id),
      bt_skip_fetch: document.getElementById('bt_skip_fetch_' + v_tab.id),
      bt_commit: document.getElementById('bt_commit_' + v_tab.id),
      bt_rollback: document.getElementById('bt_rollback_' + v_tab.id),
      bt_indent: document.getElementById('bt_indent_' + v_tab.id),
      bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
      check_autocommit: document.getElementById('check_autocommit_' + v_tab.id),
			tab_loading_span : v_tab_loading_span,
			tab_close_span : v_tab_close_span,
			tab_check_span : v_tab_check_span,
      tab_stub_span : v_tab_stub_span,
      context: null,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
			connTab: v_connTabControl.selectedTab,
      currDatabaseIndex: null,
      tabCloseSpan: v_tab_close_span,
      state: 0,
      console_history_div: document.getElementById('console_history_div_' + v_tab.id),
      console_history_grid_div: document.getElementById('console_history_grid_' + v_tab.id),
      console_history_grid: null,
      console_history_cmd_index: -1,
      tempData: []
		};

		v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
    v_add_tab.tag = {
      mode: 'add'
    }

    setTimeout(function() {
      refreshHeights();
    },10);

    adjustQueryTabObjects(false);

	};

  var v_createEditDataTabFunction = function(p_table) {

    v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
    var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
        '<i class="fas fa-table icon-tab-title"></i><span id="tab_title"> ' + p_table + '</span><span id="tab_stub"><img style="width: 16px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
    v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
    };
    var v_tab_check_span = document.getElementById('tab_check');
    v_tab_check_span.id = 'tab_check_' + v_tab.id;
    var v_tab_stub_span = document.getElementById('tab_stub');
    v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

    v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

    var v_html = "<div id='div_edit_data_select_" + v_tab.id + "' class='query_info' style='margin-top: 5px; margin-bottom: 5px; font-size: 14px;'>select * from " + p_table + " t</div>" +
           "<div id='txt_filter_data_" + v_tab.id + "' style=' width: 100%; height: 100px;border: 1px solid #c3c3c3;'></div>" +
           "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
           "<div class='tab_actions'>" +
           "<button id='bt_start_" + v_tab.id + "' class='bt_execute bt_icon_only' title='Run' style='margin: 0px 5px 5px; 0px;' onclick='queryEditData();'><i class='fas fa-play fa-light'></i></button>" +
           "<select id='sel_filtered_data_" + v_tab.id + "' class='sel_export_file_type' onchange='queryEditData()'><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option></select>" +
           "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='margin-bottom: 5px; margin-left: 5px; display: none;' onclick='cancelEditData();'>Cancel</button>" +
           "<div id='div_edit_data_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
           "<button id='bt_saveEditData_" + v_tab.id + "' onclick='saveEditData()' style='visibility: hidden; margin-left: 5px;'>Save Changes</button>" +
           "</div>" +
           "<div id='div_edit_data_data_" + v_tab.id + "' style='width: 100%; height: 250px; overflow: hidden;'></div>";

    var v_div = document.getElementById('div_' + v_tab.id);
    v_div.innerHTML = v_html;

    var v_height  = window.innerHeight - $('#div_edit_data_data_' + v_tab.id).offset().top - 20;

    document.getElementById('div_edit_data_data_' + v_tab.id).style.height = v_height + "px"

    var langTools = ace.require("ace/ext/language_tools");
    var v_editor = ace.edit('txt_filter_data_' + v_tab.id);
    v_editor.$blockScrolling = Infinity;
    v_editor.setTheme("ace/theme/" + v_editor_theme);
    v_editor.session.setMode("ace/mode/sql");
    v_editor.commands.bindKey(v_keybind_object.v_autocomplete, "startAutocomplete");
    v_editor.commands.bindKey(v_keybind_object.v_autocomplete_mac, "startAutocomplete");

    v_editor.setFontSize(Number(v_editor_font_size));

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.commands.bindKey("Ctrl-Up", null)
    v_editor.commands.bindKey("Ctrl-Down", null)

    document.getElementById('txt_filter_data_' + v_tab.id).onclick = function() {

      v_editor.focus();

    };



    var qtags = {
      getCompletions: function(editor, session, pos, prefix, callback) {

        if (v_completer_ready && prefix!='') {

            var wordlist = [];

            v_completer_ready = false;

            addLoadingCursor();

            execAjax('/get_completions_table/',
                JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                                "p_tab_id": v_connTabControl.selectedTab.id,
                                "p_table": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.table,
                                "p_schema": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.schema}),
                function(p_return) {

                  removeLoadingCursor();
                  v_completer_ready = true;

                  wordlist = p_return.v_data;
                  callback(null, wordlist);

                },
                function(p_return) {
                  removeLoadingCursor();
                  v_completer_ready = true;
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
        else {
          callback(null, wordlist);
        }
      }
    }
    langTools.addCompleter([qtags]);
    v_editor.completers = [qtags];
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
      tab_stub_span : v_tab_stub_span,
      state: 0,
      context: null,
      tabControl: v_connTabControl.selectedTab.tag.tabControl,
      connTab: v_connTabControl.selectedTab,
      tabId: v_connTabControl.selectedTab.tag.tabControl.tabCounter,
      tabCloseSpan: v_tab_close_span
    };

    v_tab.tag = v_tag;

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
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
            '<i class="fas fa-table icon-tab-title"></i><span id="tab_title"> ' + p_table + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
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
			alterTableObject: { mode: null },
      tabCloseSpan: v_tab_close_span
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

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
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
            '<i class="fas fa-code-branch icon-tab-title"></i><span id="tab_title">' + v_name + '</span><span id="tab_stub"><img style="width: 16px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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
                  checkDebugStatus(this);
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
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          var v_message_data = { tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id, tab_db_id: null };
          sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CloseTab, [v_message_data], false, null);
          v_current_tab.removeTab();
          if (v_tab.tag.tabCloseFunction)
            v_tab.tag.tabCloseFunction(v_tab.tag);
        });

		};
    var v_tab_check_span = document.getElementById('tab_check');
		v_tab_check_span.id = 'tab_check_' + v_tab.id;
    var v_tab_stub_span = document.getElementById('tab_stub');
		v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

		var v_html = "<div id='txt_func_body_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +

					"<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
          "<div style='margin-bottom: 5px;'>" +
          "<button id='bt_start_" + v_tab.id + "' class='bt_icon_only' title='Start' onclick='startDebug();'><i class='fas fa-bolt fa-light'></i></button>" +
          "<button id='bt_reload_" + v_tab.id + "' class='bt_icon_only' title='Reload Function Attributes'><i class='fas fa-sync-alt fa-light'></i></button>" +
					"<button id='bt_step_over_" + v_tab.id + "' class='bt_icon_only' title='Step Over (Next Statement)' style='display: none;' onclick='stepDebug(0);'><i class='fas fa-angle-right fa-light'></i></button>" +
          "<button id='bt_step_out_" + v_tab.id + "' class='bt_icon_only' title='Resume (Next Breakpoint)' style='display: none;' onclick='stepDebug(1);'><i class='fas fa-angle-double-right fa-light'></i></button>" +
          "<button id='bt_cancel_" + v_tab.id + "' class='bt_red' title='Cancel' style='display: none; vertical-align: middle;' onclick='cancelDebug();'>Cancel</button>" +
					"<div id='div_debug_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
          "</div>" +
          "        <div id='debug_result_tabs_" + v_tab.id + "'>" +
          "            <ul>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab1'>Parameters</li>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab2'>Variables</li>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab3'>Result</li>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab4'>Messages <div id='debug_result_tabs_count_notices_" + v_tab.id + "' class='count_notices' style='display: none;'></div></li>" +
          "            <li id='debug_result_tabs_" + v_tab.id + "_tab5'>Statistics</li>" +
          "			</ul>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab1'>" +
          "<div id='div_parameters_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab2'>" +
          "<div id='div_variables_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab3'>" +
          "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab4'>" +
          "<div id='div_notices_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: auto;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab5'>" +
          "<div id='div_statistics_" + v_tab.id + "' style='width: 100%; overflow: auto; position: relative;'>" +
          "<div id='div_statistics_container_" + v_tab.id + "' style='height: 100%; position: relative;'>" +
          "<canvas id='div_statistics_canvas_" + v_tab.id + "''></canvas>" +
          "</div>" +
          "</div>" +
          "			</div></div>";

		var v_div = document.getElementById('div_' + v_tab.id);
		v_div.innerHTML = v_html;

    var v_curr_tabs = createTabControl('debug_result_tabs_' + v_tab.id,0,null);

		var langTools = ace.require("ace/ext/language_tools");
		var v_editor = ace.edit('txt_func_body_' + v_tab.id);
    v_editor.$blockScrolling = Infinity;
		v_editor.setTheme("ace/theme/" + v_editor_theme);
		v_editor.session.setMode("ace/mode/sql");

		v_editor.setFontSize(Number(v_editor_font_size));

		v_editor.commands.bindKey("ctrl-space", null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey("Cmd-,", null)
    v_editor.commands.bindKey("Ctrl-,", null)
    v_editor.commands.bindKey("Cmd-Delete", null)
    v_editor.commands.bindKey("Ctrl-Delete", null)
    v_editor.commands.bindKey("Ctrl-Up", null)
    v_editor.commands.bindKey("Ctrl-Down", null)
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
      div_parameter: document.getElementById('div_parameters_' + v_tab.id),
      div_variable: document.getElementById('div_variables_' + v_tab.id),
			div_result: document.getElementById('div_result_' + v_tab.id),
      div_notices: document.getElementById('div_notices_' + v_tab.id),
      div_statistics: document.getElementById('div_statistics_' + v_tab.id),
      div_statistics_container: document.getElementById('div_statistics_container_' + v_tab.id),
      div_statistics_canvas: document.getElementById('div_statistics_canvas_' + v_tab.id),
      div_count_notices: document.getElementById('debug_result_tabs_count_notices_' + v_tab.id),
			tab_title_span : v_tab_title_span,
			tab_loading_span : v_tab_loading_span,
			tab_close_span : v_tab_close_span,
			tab_check_span : v_tab_check_span,
      tab_stub_span : v_tab_stub_span,
      bt_reload: document.getElementById('bt_reload_' + v_tab.id),
			bt_start: document.getElementById('bt_start_' + v_tab.id),
      bt_step_over: document.getElementById('bt_step_over_' + v_tab.id),
      bt_step_out: document.getElementById('bt_step_out_' + v_tab.id),
      bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
			state : 0,
      hasDataToRender: false,
      context: null,
			tabControl: v_connTabControl.selectedTab.tag.tabControl,
      queryTabControl: v_curr_tabs,
      currDebugTab: null,
			connTab: v_connTabControl.selectedTab,
      currDatabaseIndex: null,
      markerId: null,
      markerList: [],
      htParameter: null,
      htVariable: null,
      htResult: null,
      chart: null,
      breakPoint: null,
      tabCloseSpan: v_tab_close_span,
      tabCloseFunction: function(p_tag) {
        try {
          p_tag.chart.destroy();
        }
        catch(err) {
        }
      }
		};

		v_tab.tag = v_tag;

    var v_selectParameterTabFunc = function() {
			v_curr_tabs.selectTabIndex(0);
      v_tag.currDebugTab = 'parameter';
      refreshHeights();
		}

    var v_selectVariableTabFunc = function() {
			v_curr_tabs.selectTabIndex(1);
      v_tag.currDebugTab = 'variable';
      refreshHeights();
		}

    var v_selectResultTabFunc = function() {
			v_curr_tabs.selectTabIndex(2);
      v_tag.currDebugTab = 'result';
      refreshHeights();
		}

    var v_selectMessageTabFunc = function() {

			v_curr_tabs.selectTabIndex(3);
      v_tag.currDebugTab = 'message';
			v_tag.div_count_notices.style.display = 'none';
      refreshHeights();
		}

    var v_selectStatisticsTabFunc = function() {
			v_curr_tabs.selectTabIndex(4);
      v_tag.currDebugTab = 'statistics';
      refreshHeights();
		}

    v_tag.selectParameterTabFunc = v_selectParameterTabFunc;
    v_tag.selectVariableTabFunc = v_selectVariableTabFunc;
    v_tag.selectResultTabFunc = v_selectResultTabFunc;
    v_tag.selectMessageTabFunc = v_selectMessageTabFunc;
    v_tag.selectStatisticsTabFunc = v_selectStatisticsTabFunc;

    v_curr_tabs.tabList[0].elementLi.onclick = v_selectParameterTabFunc;
    v_curr_tabs.tabList[1].elementLi.onclick = v_selectVariableTabFunc;
    v_curr_tabs.tabList[2].elementLi.onclick = v_selectResultTabFunc;
		v_curr_tabs.tabList[3].elementLi.onclick = v_selectMessageTabFunc;
    v_curr_tabs.tabList[4].elementLi.onclick = v_selectStatisticsTabFunc;

		v_selectParameterTabFunc();

    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
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
  //v_connTabControl.tag.createChatTab = v_createChatTabFunction;
  //v_connTabControl.tag.createServerMonitoringTab = v_createServerMonitoringTabFunction;

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
  v_connTabControl.tag.createNewMonitorUnitTab = v_createNewMonitorUnitTabFunction;
  v_connTabControl.tag.createMonitorDashboardTab = v_createMonitorDashboardTabFunction;
  v_connTabControl.tag.createConsoleTab = v_createConsoleTabFunction;

  //Functions to create tabs inside monitor tab
  //v_connTabControl.tag.createNewMonitorNodeTab = v_createNewMonitorNodeTabFunction;
}

function beforeCloseTab(e,p_confirm_function) {
  if (e.clientX==0 && e.clientY==0)
    showConfirm('Are you sure you want to remove this tab?',
    function() {
      p_confirm_function();
    });
  else
    customMenu(
      {
        x:e.clientX+5,
        y:e.clientY+5
      },
      [
        {
          text: 'Confirm',
          icon: 'fas cm-all fa-check',
          action: function() {
            p_confirm_function();
          }
        },
        {
          text: 'No',
          icon: 'fas cm-all fa-times',
          action: function() {
          }
        }
      ],
      null);

}
