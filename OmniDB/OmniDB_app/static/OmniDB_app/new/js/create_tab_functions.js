/*
Copyright 2015-2019 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function initCreateTabFunctions() {


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
            '<i class="fas fa-code-branch icon-tab-title"></i><span id="tab_title">' + v_name + '</span><span id="tab_loading" style="visibility:hidden;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i></span>',
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

		var v_html = "<div id='txt_func_body_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +

					"<div class='omnidb__resize-line__container' onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dashed #acc4e8;'></div><div style='height:5px;'></div></div>" +
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
          "<div id='div_parameters_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: hidden;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab2'>" +
          "<div id='div_variables_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: hidden;'></div>" +
          "			</div>" +
          "			<div id='div_debug_result_tabs_" + v_tab.id + "_tab3'>" +
          "<div id='div_result_" + v_tab.id + "' class='query_result' style='width: 100%; overflow: hidden;'></div>" +
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

		v_editor.setFontSize(Number(v_font_size));

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

	// Functions to create a default `add` tab
	v_connTabControl.tag.createAddTab = v_connTabControl.createTab(
    {
      p_icon: '<i class="fas fa-plus"></i>',
      p_name: 'Add connection',
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        showMenuNewTabOuter(e);
      },
      p_tooltip_name: '<h5 class="my-1">Add/Select Connections</h5>'
    }
  );

  // Functions to create tabs globally
  v_connTabControl.tag.createConnTab = v_createConnTabFunction;
  //v_connTabControl.tag.createChatTab = v_createChatTabFunction;
  //v_connTabControl.tag.createServerMonitoringTab = v_createServerMonitoringTabFunction;

  // Functions to create snippet panel globally
  v_connTabControl.tag.createSnippetPanel = v_createSnippetPanelFunction;

  // Functions to create tabs inside snippet panel
  v_connTabControl.tag.createSnippetTextTab = v_createSnippetTextTabFunction;

	// Functions to create welcome tab globally
	v_connTabControl.tag.createWelcomeTab = v_createWelcomeTabFunction;

  // Functions to create tabs inside a connection tab
	v_connTabControl.tag.createQueryTab = v_createQueryTabFunction;
  v_connTabControl.tag.createConsoleTab = v_createConsoleTabFunction;
  v_connTabControl.tag.createWebsiteTab = v_createWebsiteTabFunction;
  v_connTabControl.tag.createWebsiteOuterTab = v_createWebsiteOuterTabFunction;
  v_connTabControl.tag.createNewMonitorUnitTab = v_createNewMonitorUnitTabFunction;
  v_connTabControl.tag.createMonitorDashboardTab = v_createMonitorDashboardTabFunction;

	v_connTabControl.tag.createEditDataTab = v_createEditDataTabFunction;
  v_connTabControl.tag.createGraphTab = v_createGraphTabFunction;
  v_connTabControl.tag.createMonitoringTab = v_createMonitoringTabFunction;
  v_connTabControl.tag.createDebuggerTab = v_createDebuggerTabFunction;
  v_connTabControl.tag.createOuterTerminalTab = v_createOuterTerminalTabFunction;

  // Functions to create tabs inside monitor tab
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
          text: 'Cancel',
          icon: 'fas cm-all fa-times',
          action: function() {
          }
        }
      ],
      null);

}
