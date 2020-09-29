/*
The MIT License (MIT)

Portions Copyright (c) 2015-2019, The OmniDB Team
Portions Copyright (c) 2017-2019, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

/// <summary>
/// Console state
/// </summary>
var v_consoleState = {
	Idle: 0,
	Executing: 1,
	Ready: 2
}

/// <summary>
/// Wipes command history.
/// </summary>
function deleteConsoleHistoryList() {
	showConfirm(
		'Are you sure you want to clear console history corresponding to applied filters?',
		function() {
			execAjax(
				'/clear_console_list/',
				JSON.stringify({
					'p_database_index': v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
					'p_console_from': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedFrom.value,
					'p_console_to': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedTo.value,
					'p_console_contains': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputCommandContains.value
				}),
				function(p_return) {
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage = 1;
					refreshConsoleHistoryList();
				}
			);
		}
	);
}

function showConsoleHistory() {
  // var input = JSON.stringify({
	// 	"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
	// 	"p_tab_id": v_connTabControl.selectedTab.id
	// });
	var v_conn_tag = v_connTabControl.selectedTab.tag;
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	v_tab_tag.consoleHistory.headerDiv.innerHTML =
	"<div class='mb-2 form-inline justify-content-center'>" +
		"<div class='input-group w-auto mr-2'>" +
			"<span class='my-auto'>Select a daterange:</span>&nbsp;" +
			"<input type='text' class='form-control form-control-sm d-none' placeholder='Start Time' id='cl_input_from_" + v_tab_tag.tab_id + "'>" +
			"<input type='text' class='form-control form-control-sm d-none' placeholder='End Time' id='cl_input_to_" + v_tab_tag.tab_id + "'>" +
			"<button type='button' class='btn btn-sm omnidb__theme__btn--primary' id='cl_time_range_" + v_tab_tag.tab_id + "'>" +
				"<i class='far fa-calendar-alt'></i>&nbsp;" +
				"<span>Last 6 Hours</span> <i class='fa fa-caret-down'></i>" +
			"</button>" +
		"</div>" +
		"<label class='mr-1'>Command contains:</label>" +
		"<input type='text' id='cl_input_contains_" + v_tab_tag.tab_id + "' class='mr-2 form-control' onchange='refreshConsoleHistoryList();' />" +
	"</div>" +
	"<div id='console_history_daterangepicker_container_" + v_tab_tag.id  + "' style='position:relative;'></div>" +
	"<div class='mb-2 d-flex justify-content-center align-items-center'>" +
		"<button id='bt_first_" + v_tab_tag.tab_id + "' onclick='consoleHistoryFirstPage()' class='bt_execute btn btn-sm omnidb__theme__btn--secondary mx-1' title='First'>First</button>" +
		"<button id='bt_previous_" + v_tab_tag.tab_id + "' onclick='consoleHistoryPreviousPage()' class='bt_execute btn btn-sm omnidb__theme__btn--secondary mx-1' title='Previous'>Previous</button>" +
		"<span id='cl_curr_page_" + v_tab_tag.tab_id + "'></span> / <span id='cl_num_pages_" + v_tab_tag.tab_id + "'></span>" +
		"<button id='bt_next_" + v_tab_tag.tab_id + "' onclick='consoleHistoryNextPage()' class='bt_execute btn btn-sm omnidb__theme__btn--secondary mx-1' title='Next'>Next</button>" +
		"<button id='bt_last_" + v_tab_tag.tab_id + "' onclick='consoleHistoryLastPage()' class='bt_execute btn btn-sm omnidb__theme__btn--secondary mx-1' title='Last'>Last</button>" +
		"<button id='bt_refresh_" + v_tab_tag.tab_id + "' onclick='refreshConsoleHistoryList()' class='bt_execute btn btn-sm omnidb__theme__btn--primary mx-1' title='Refresh'><i class='fas fa-sync-alt mr-1'></i>Refresh</button>" +
		"<button id='bt_clear_" + v_tab_tag.tab_id + "' onclick='deleteConsoleHistoryList()' class='bt_execute btn btn-sm btn-danger mx-1' title='Clear List'><i class='fas fa-broom mr-1'></i>Clear List</button>" +
	"</div>";

  var v_grid_div = v_tab_tag.consoleHistory.gridDiv;
  v_grid_div.innerHTML = '';

	if(v_tab_tag.consoleHistory.grid != null) {
		v_tab_tag.consoleHistory.grid.destroy();
	}

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

	v_tab_tag.consoleHistory.grid = new Handsontable(v_grid_div,
	{
		licenseKey: 'non-commercial-and-evaluation',
		// data: p_return.v_data.data,
		data: [
			["<i title='Select' class='fas fa-check text-success action-grid action-status-ok' onclick='consoleHistorySelectCommand()'></i>", "2020-05-01 19:19:21", "\?"],
			["<i title='Select' class='fas fa-check text-success action-grid action-status-ok' onclick='consoleHistorySelectCommand()'></i>", "2020-05-01 19:19:20", "\?"],
			["<i title='Select' class='fas fa-check text-success action-grid action-status-ok' onclick='consoleHistorySelectCommand()'></i>", "2020-05-01 19:19:19", "\?"]
		],

		columns : columnProperties,
		colHeaders : true,
		rowHeaders : false,
		stretchH: 'last',
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

	$(v_tab_tag.consoleHistory.modal).modal('show');
	v_tab_tag.consoleHistory.div.style.display = 'block';

	v_tab_tag.consoleHistory.currentPage = 1;
	v_tab_tag.consoleHistory.pages = 1;
	v_tab_tag.consoleHistory.spanNumPages = document.getElementById('cl_num_pages_' + v_tab_tag.tab_id);
	v_tab_tag.consoleHistory.spanNumPages.innerHTML = 1;
	v_tab_tag.consoleHistory.spanCurrPage = document.getElementById('cl_curr_page_' + v_tab_tag.tab_id);
	v_tab_tag.consoleHistory.spanCurrPage.innerHTML = 1;
	v_tab_tag.consoleHistory.inputStartedFrom = document.getElementById('cl_input_from_' + v_tab_tag.tab_id);
	v_tab_tag.consoleHistory.inputStartedFrom.value = moment().subtract(6, 'hour').toISOString();
	v_tab_tag.consoleHistory.inputStartedTo = document.getElementById('cl_input_to_' + v_tab_tag.tab_id);
	v_tab_tag.consoleHistory.inputStartedTo.value = moment().toISOString();
	v_tab_tag.consoleHistory.inputCommandContains = document.getElementById('cl_input_contains_' + v_tab_tag.tab_id);
	v_tab_tag.consoleHistory.inputCommandContains.value = v_tab_tag.consoleHistory.inputCommandContainsLastValue;

	// Setting daterangepicker
	var cl_time_range = document.getElementById('cl_time_range_' + v_tab_tag.tab_id);

	$(cl_time_range).daterangepicker({
		timePicker: true,
		startDate: moment(v_tab_tag.consoleHistory.inputStartedFrom.value).format('Y-MM-DD H'),
		endDate: moment(v_tab_tag.consoleHistory.inputStartedTo.value).format('Y-MM-DD H'),
		parentEl: document.getElementById('console_history_daterangepicker_container_' + v_tab_tag.tab_id),
		previewUTC: true,
		locale: {
			format: 'Y-MM-DD H'
		},
		ranges: {
			'Last 6 Hours': [moment().subtract(6, 'hour').format('Y-MM-DD H'), moment().format('Y-MM-DD H')],
			'Last 12 Hours': [moment().subtract(12, 'hour').format('Y-MM-DD H'), moment().format('Y-MM-DD H')],
			'Last 24 Hours': [moment().subtract(24, 'hour').format('Y-MM-DD H'), moment().format('Y-MM-DD H')],
			'Last 7 Days': [moment().subtract(7, 'days').startOf('day').format('Y-MM-DD H'), moment().format('Y-MM-DD H')],
			'Last 30 Days': [moment().subtract(30, 'days').startOf('day').format('Y-MM-DD H'), moment().format('Y-MM-DD H')],
			'Yesterday': [moment().subtract(1, 'days').startOf('day').format('Y-MM-DD H'), moment().subtract(1, 'days').endOf('day').format('Y-MM-DD H')],
			'This Month': [moment().startOf('month').format('Y-MM-DD H'), moment().format('Y-MM-DD H')],
			'Last Month': [moment().subtract(1, 'month').startOf('month').format('Y-MM-DD H'), moment().subtract(1, 'month').endOf('month').format('Y-MM-DD H')]
		}
	}, function(start, end, label) {

		v_tab_tag.consoleHistory.inputStartedFrom.value = moment(start).toISOString();

		// Update Button Labels
		if (label === "Custom Range") {
			$('#cl_time_range_' + v_tab_tag.tab_id + ' span').html(start.format('MMMM D, YYYY hh:mm A') + ' - ' + end.format('MMMM D, YYYY hh:mm A'));
		}
		else {
			$('#cl_time_range_' + v_tab_tag.tab_id + ' span').html(label);
		}

		if (label === "Custom Range" || label === "Yesterday" || label === "Last Month") {
			v_tab_tag.consoleHistory.inputStartedTo.value = moment(end).toISOString();
		}
		else
			v_tab_tag.consoleHistory.inputStartedTo.value = null;

		refreshConsoleHistoryList();
	});

	refreshConsoleHistoryList();
}

function consoleHistoryNextPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage < v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.pages) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage += 1;
		refreshConsoleHistoryList();
	}
}

function consoleHistoryPreviousPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage > 1) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage -= 1;
		refreshConsoleHistoryList();
	}
}

function consoleHistoryFirstPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage != 1) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage = 1;
		refreshConsoleHistoryList();
	}
}

function consoleHistoryLastPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage != v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.pages) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.pages;
		refreshConsoleHistoryList();
	}
}

function consoleHistoryOpenCmd(p_index) {
	var v_command = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.grid.getDataAtRow(p_index)[4];
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(v_command);
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
	closeConsoleHistory();
}

/// <summary>
/// Retrieves and displays console history.
/// </summary>
function refreshConsoleHistoryList() {
	var v_conn_tag = v_connTabControl.selectedTab.tag;
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedFromLastValue = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedFrom.value;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedToLastValue = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedTo.value;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputCommandContainsLastValue = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputCommandContains.value;

	execAjax(
		'/get_console_history/',
		JSON.stringify({
			'p_command_from': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedFrom.value,
			'p_command_to': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedTo.value,
			'p_command_contains': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputCommandContains.value,
			'p_current_page': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage,
			'p_database_index': v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
			"p_tab_id": v_connTabControl.selectedTab.id
		}),
		function(p_return) {
			v_conn_tag.consoleHistoryFecthed = true;
			v_conn_tag.consoleHistoryList = p_return.v_data.data_clean;
			console.log(p_return.v_data);
			if(v_conn_tag.consoleHistoryList.length == 0) {
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage = 1;
			}

			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.pages = p_return.v_data.pages;
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.spanNumPages.innerHTML = p_return.v_data.pages;
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.spanCurrPage.innerHTML = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage;

			// TODO: dates
			// for (let i = 0; i < v_conn_tag.consoleHistoryList.length; i++) {
			// 	p_return.v_data.consoleHistoryList[i][0] = new Date(p_return.v_data.consoleHistoryList[i][0]).toLocaleString();
			// 	p_return.v_data.consoleHistoryList[i][1] = new Date(p_return.v_data.consoleHistoryList[i][1]).toLocaleString();
			// }

			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.grid.loadData(p_return.v_data.data);

			// v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.gridDivParent.style.height = '200px';
		},
		null,
		'box'
	);
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
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.grid.destroy();
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.grid = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.div.style.display = 'none';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.headerDiv.innerHTML = '';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.gridDiv.innerHTML = '';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.currentPage = 1;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.pages = 1;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.spanNumPages = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.spanCurrPages = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedFrom = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputStartedTo = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.inputCommandContains = null;
	$(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.consoleHistory.modal).modal('hide');
}

function consoleHistorySelectCommand() {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  var v_grid = v_tab_tag.consoleHistory.grid;

  var v_command = v_grid.getDataAtRow(v_grid.getSelected()[0][0])[2];
  closeConsoleHistory();
  v_tab_tag.editor_input.setValue(v_command);
  v_tab_tag.editor_input.clearSelection();
  v_tab_tag.editor_input.focus();
}

function appendToEditor(p_editor, p_text) {
  /*var v_last_row = p_editor.session.getLength() - 1;
  var v_last_col = p_editor.session.getLine(v_last_row).length;
  p_editor.session.insert({ row: v_last_row, column: v_last_col},p_text);
  p_editor.gotoLine(Infinity);
  p_editor.resize();*/
	//let v_text = p_text.replace(/(\r\n|\n|\r)/gm, "XXX");

	p_editor.write(p_text);
}

function clearConsole() {
  var v_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_tag.editor_console.write('\x1b[H\x1b[2J');
  v_tag.editor_console.write(v_connTabControl.selectedTab.tag.consoleHelp);
  //v_tag.editor_console.clear();

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

        //sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Console, v_message_data, false, v_context);
				createRequest(v_queryRequestCodes.Console, v_message_data, v_context);

        v_tag.state = v_consoleState.Executing;
        v_tag.tab_loading_span.style.visibility = 'visible';
        v_tag.tab_check_span.style.display = 'none';
        v_tag.bt_cancel.style.display = '';
        v_tag.query_info.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Running...</b>';
				v_tag.bt_fetch_more.style.display = 'none';
				v_tag.bt_fetch_all.style.display = 'none';
				v_tag.bt_skip_fetch.style.display = 'none';
				v_tag.bt_commit.style.display = 'none';
				v_tag.bt_rollback.style.display = 'none';
				setTabStatus(v_tag,2);

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
	v_tab_tag.tab_loading_span.style.visibility = 'hidden';
	v_tab_tag.tab_check_span.style.display = 'none';
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

			p_context.tab_tag.tab_loading_span.style.visibility = 'hidden';
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
  v_tag.tab_loading_span.style.visibility = 'hidden';
  v_tag.tab_check_span.style.display = 'none';
  v_tag.bt_cancel.style.display = 'none';
	if (p_message.v_data.v_show_fetch_button) {
		v_tag.bt_fetch_more.style.display = '';
		v_tag.bt_fetch_all.style.display = '';
		v_tag.bt_skip_fetch.style.display = '';
	}


}
