/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Console state
/// </summary>
var v_consoleState = {
	Idle: 0,
	Executing: 1,
	Ready: 2
}

function showConsoleHistory() {

  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
															"p_tab_id": v_connTabControl.selectedTab.id});
	var v_conn_tag = v_connTabControl.selectedTab.tag;
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  var v_grid_div = v_tab_tag.console_history_grid_div;
  v_grid_div.innerHTML = '';

  execAjax('/get_console_history/',
        input,
        function(p_return) {
					v_conn_tag.consoleHistoryFecthed = true;
					v_conn_tag.consoleHistoryList = p_return.v_data.data_clean;


          var columnProperties = [];

          var col = new Object();
          col.readOnly = true;
          col.title =  ' ';
          col.width = '26px';
          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Date';
          col.width = '115px';
          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Command';
          col.width = '435px';
          columnProperties.push(col);

          v_tab_tag.console_history_div.style.display = 'block';
          if (v_tab_tag.console_history_grid) {
            v_tab_tag.console_history_grid.destroy();
          }


          v_tab_tag.console_history_grid = new Handsontable(v_grid_div,
          {
			licenseKey: 'non-commercial-and-evaluation',
            data: p_return.v_data.data,
            columns : columnProperties,
            colHeaders : true,
            rowHeaders : false,
            //copyRowsLimit : 1000000000,
            //copyColsLimit : 1000000000,
            copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
            manualColumnResize: true,
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
                cellProperties.renderer = whiteHtmlRenderer;
                return cellProperties;
            }
          });

        },
        null,
        'box');

}

function getConsoleHistoryCommand(p_mode) {
	//fetch command history if not fetched before
	var v_conn_tag = v_connTabControl.selectedTab.tag;
	if (!v_conn_tag.consoleHistoryFecthed) {
		var input = JSON.stringify({"p_database_index": v_conn_tag.selectedDatabaseIndex,
																"p_tab_id": v_connTabControl.selectedTab.id});

	  execAjax('/get_console_history_clean/',
	        input,
	        function(p_return) {
						v_conn_tag.consoleHistoryFecthed = true;
						v_conn_tag.consoleHistoryList = p_return.v_data;
						getConsoleHistoryCommandConfirm(p_mode);
	        },
	        null,
	        'box');

	}
	else
		getConsoleHistoryCommandConfirm(p_mode);
}

function getConsoleHistoryCommandConfirm(p_mode) {
	var v_conn_tag = v_connTabControl.selectedTab.tag;
	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_next_index = null;

	if (p_mode=='previous') {
		if (v_tab_tag.console_history_cmd_index<v_conn_tag.consoleHistoryList.length-1) {
			v_next_index = v_tab_tag.console_history_cmd_index + 1;
			v_tab_tag.console_history_cmd_index = v_next_index;
		}
	}
	else if (p_mode=='next') {
		if (v_tab_tag.console_history_cmd_index>=0) {
			v_next_index = v_tab_tag.console_history_cmd_index - 1;
			v_tab_tag.console_history_cmd_index = v_next_index;
		}
	}

	if (v_next_index!=null) {
		var v_command = '';
		if (v_next_index>=0)
			v_command = v_conn_tag.consoleHistoryList[v_next_index];
		v_tab_tag.editor_input.setValue(v_command);
	  v_tab_tag.editor_input.clearSelection();
	  v_tab_tag.editor_input.focus();
	}

}

function closeConsoleHistory() {
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.console_history_grid_div.innerHTML = '';
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.console_history_div.style.display = 'none';
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.console_history_grid.destroy();
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.console_history_grid = null;
}

function consoleHistorySelectCommand() {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  var v_grid = v_tab_tag.console_history_grid;

  var v_command = v_grid.getDataAtRow(v_grid.getSelected()[0][0])[2];
  closeConsoleHistory();
  v_tab_tag.editor_input.setValue(v_command);
  v_tab_tag.editor_input.clearSelection();
  v_tab_tag.editor_input.focus();
}

function appendToEditor(p_editor, p_text) {
  var v_last_row = p_editor.session.getLength() - 1;
  var v_last_col = p_editor.session.getLine(v_last_row).length;
  p_editor.session.insert({ row: v_last_row, column: v_last_col},p_text);
  p_editor.gotoLine(Infinity);
  p_editor.resize();
}

function clearConsole() {
  var v_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  v_tag.editor_console.setValue('>> ' + v_connTabControl.selectedTab.tag.consoleHelp);
  v_tag.editor_console.clearSelection();

}

function consoleSQL(p_check_command = true, p_mode = 0) {
  var v_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_tag.tempData = '';
  var v_content = v_tag.editor_input.getValue().trim();
  //var v_cursor_position = v_tag.editor_input.getCursorPosition();
  //var v_last_row = v_tag.editor_input.session.getLength() - 1;
  //var v_last_col = v_tag.editor_input.session.getLine(v_last_row).length;

    //last character is semi-colon or first is backslash
  //if (!p_check_command || (v_content[v_content.length-1]==';' || v_content[0]=='\\') {
  if (!p_check_command || v_content[0]=='\\') {

    if (v_tag.state!=v_consoleState.Idle) {
  		showAlert('Tab with activity in progress.');
  	}
  	else {

      if (v_content=='' && p_mode == 0) {
  			showAlert('Please provide a string.');
  		}
  		else {

				//append to command history list
				if (v_connTabControl.selectedTab.tag.consoleHistoryList)
					v_connTabControl.selectedTab.tag.consoleHistoryList.unshift(v_content);
				v_tag.console_history_cmd_index = -1;

        //appendToEditor(v_tag.editor_console,'\n');
        v_tag.editor_input.setValue('');
        v_tag.editor_input.clearSelection();
        v_tag.editor_input.setReadOnly(false);
				v_tag.last_command = v_content;

        var v_message_data = {
          v_sql_cmd : v_content,
					v_mode: p_mode,
          v_db_index: v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
					v_conn_tab_id: v_connTabControl.selectedTab.id,
          v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
					v_autocommit: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.check_autocommit.checked
        }

        v_tag.editor_input.setReadOnly(true);

        var d = new Date,
        dformat = [(d.getMonth()+1).padLeft(),
                   d.getDate().padLeft(),
                   d.getFullYear()].join('/') +' ' +
                  [d.getHours().padLeft(),
                   d.getMinutes().padLeft(),
                   d.getSeconds().padLeft()].join(':');

        var v_context = {
          tab_tag: v_tag,
          start_datetime: dformat,
          database_index: v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
          acked: false,
					last_command: v_content,
					check_command: p_check_command,
					mode: p_mode
        }
        v_context.tab_tag.context = v_context;

        sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Console, v_message_data, false, v_context);

        v_tag.state = v_consoleState.Executing;
        v_tag.tab_loading_span.style.display = '';
        v_tag.tab_check_span.style.display = 'none';
        v_tag.tab_stub_span.style.display = 'none';
        v_tag.bt_cancel.style.display = '';
        v_tag.query_info.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Running...</b>';
				v_tag.bt_fetch_more.style.display = 'none';
				v_tag.bt_fetch_all.style.display = 'none';
				v_tag.bt_skip_fetch.style.display = 'none';
				v_tag.bt_commit.style.display = 'none';
				v_tag.bt_rollback.style.display = 'none';
				setTabStatus(v_tag,2);

        setTimeout(function() {
          if (!v_context.acked) {
            cancelConsoleTab(v_context.tab_tag);
          }
        },20000);
      }
    }
  }
}

function cancelConsole(p_tab_tag) {
  var v_tab_tag;
	if (p_tab_tag)
		v_tab_tag = p_tab_tag;
	else
		v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CancelThread, v_tab_tag.tab_id, false);

	cancelConsoleTab(v_tab_tag);

}

function cancelConsoleTab(p_tab_tag) {

  var v_tab_tag;
	if (p_tab_tag)
		v_tab_tag = p_tab_tag;
	else
		v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	if(v_tab_tag.editor_input) {
		v_tab_tag.editor_input.setReadOnly(false);
	}

	v_tab_tag.state = v_consoleState.Idle;
	v_tab_tag.tab_loading_span.style.display = 'none';
	v_tab_tag.tab_check_span.style.display = 'none';
	v_tab_tag.tab_stub_span.style.display = '';
	v_tab_tag.bt_cancel.style.display = 'none';
	v_tab_tag.query_info.innerHTML = 'Canceled.';

	removeContext(v_queryWebSocket,v_tab_tag.context.v_context_code);

	SetAcked(v_tab_tag.context);

}

function checkConsoleStatus(p_tab) {

	if (p_tab.tag.state == v_consoleState.Ready) {
		consoleReturnRender(p_tab.tag.data,p_tab.tag.context);
	}
}

function consoleReturn(p_data,p_context) {

	//If query wasn't canceled already
	if (p_context.tab_tag.state!=v_consoleState.Idle) {

		if (p_context.tab_tag.tab_id == p_context.tab_tag.tabControl.selectedTab.id && p_context.tab_tag.connTab.id == p_context.tab_tag.connTab.tag.connTabControl.selectedTab.id) {
			consoleReturnRender(p_data,p_context);
		}
		else {
			p_context.tab_tag.state = v_consoleState.Ready;
			p_context.tab_tag.context = p_context;
			p_context.tab_tag.data = p_data;

			p_context.tab_tag.tab_loading_span.style.display = 'none';
			p_context.tab_tag.tab_check_span.style.display = '';

		}
	}
}

function consoleReturnRender(p_message,p_context) {
  p_context.tab_tag.state = v_consoleState.Idle;

  var v_tag = p_context.tab_tag;

	setTabStatus(p_context.tab_tag,p_message.v_data.v_con_status);

  v_tag.editor_input.setReadOnly(false);

  appendToEditor(v_tag.editor_console,v_tag.tempData);

  v_tag.editor_input.setValue('');
  v_tag.editor_input.clearSelection();

  v_tag.query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
  v_tag.tab_loading_span.style.display = 'none';
  v_tag.tab_check_span.style.display = 'none';
  v_tag.bt_cancel.style.display = 'none';
	v_tag.tab_stub_span.style.display = '';
	if (p_message.v_data.v_show_fetch_button) {
		v_tag.bt_fetch_more.style.display = '';
		v_tag.bt_fetch_all.style.display = '';
		v_tag.bt_skip_fetch.style.display = '';
	}


}
