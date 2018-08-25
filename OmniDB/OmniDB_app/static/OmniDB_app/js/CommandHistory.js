/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

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
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage = 1;
					refreshCommandList();
				}
			);
		}
	);
}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function showCommandList() {
	var v_connTag = v_connTabControl.selectedTab.tag;
	var v_tabTag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_gridDiv = v_tabTag.commandHistory.gridDiv;
	v_gridDiv.innerHTML = '';

	if(v_tabTag.commandHistory.grid != null) {
		v_tabTag.commandHistory.grid.destroy();
	}

	var v_columnProperties = [];

	var v_column = new Object();
	v_column.title =  'Start';
	v_column.readOnly = true;
	v_column.width = 180;
	v_columnProperties.push(v_column);

	var v_column = new Object();
	v_column.title =  'End';
	v_column.readOnly = true;
	v_column.width = 180;
	v_columnProperties.push(v_column);

	var v_column = new Object();
	v_column.title =  'Duration';
	v_column.readOnly = true;
	v_column.width = 150;
	v_columnProperties.push(v_column);

	var v_column = new Object();
	v_column.title =  'Status';
	v_column.readOnly = true;
	v_column.width = 50;
	v_columnProperties.push(v_column);

	var v_column = new Object();
	v_column.title =  'Command';
	v_column.readOnly = true;
	v_column.width = 400;
	v_columnProperties.push(v_column);

	var v_column = new Object();
	v_column.title =  'Actions';
	v_column.readOnly = true;
	v_column.width = 60;
	v_columnProperties.push(v_column);

	v_tabTag.commandHistory.grid = new Handsontable(
		v_gridDiv,
		{
			data: [],
			columns : v_columnProperties,
			colHeaders : true,
			rowHeaders : false,
			copyPaste: {
				pasteMode: '',
				rowsLimit: 1000000000,
				columnsLimit: 1000000000
			},
			manualColumnResize: true,
			fillHandle: false,
			contextMenu: {
				callback: function(p_key, p_options) {
					if(p_key === 'view_data') {
						editCellData(
							this,
							p_options[0].start.row,
							p_options[0].start.col,
							this.getDataAtCell(p_options[0].start.row, p_options[0].start.col),
							false
						);
					}
				},
				items: {
					'view_data': {
						name: '<div style="position: absolute;"><img class="img_ht" src="/static/OmniDB_app/images/rename.png"></div><div style="padding-left: 30px;">View Content</div>'
					}
				}
			},
			cells: function (p_row, p_col, p_prop) {
				var v_cellProperties = {};

				if(p_row % 2 == 0) {
					v_cellProperties.renderer = blueHtmlRenderer;
				}
				else {
					v_cellProperties.renderer = whiteHtmlRenderer;
				}

				return v_cellProperties;
			}
		}
	);

	v_tabTag.commandHistory.div.style.display = 'block';
	v_tabTag.commandHistory.grid.render();

	v_tabTag.commandHistory.headerDiv.innerHTML =
		"<button id='bt_first_" + v_tabTag.tab_id + "' onclick='commandHistoryFirstPage()' class='bt_execute' style='margin: 0 5px 5px 0px;' title='First'>First</button>" +
		"<button id='bt_previous_" + v_tabTag.tab_id + "' onclick='commandHistoryPreviousPage()' class='bt_execute' style='margin: 0 5px 5px 0px;' title='Previous'>Previous</button>" +
		"<span id='cl_curr_page_" + v_tabTag.tab_id + "'></span> / <span id='cl_num_pages_" + v_tabTag.tab_id + "'></span>" +
		"<button id='bt_next_" + v_tabTag.tab_id + "' onclick='commandHistoryNextPage()' class='bt_execute' style='margin: 0 5px 5px 5px;' title='Next'>Next</button>" +
		"<button id='bt_last_" + v_tabTag.tab_id + "' onclick='commandHistoryLastPage()' class='bt_execute' style='margin: 0 5px 5px 0px;' title='Last'>Last</button>" +
		"<button id='bt_refresh_" + v_tabTag.tab_id + "' onclick='refreshCommandList()' class='bt_execute' style='margin: 0 5px 5px 0px;' title='Refresh'>Refresh</button>" +
		"<button id='bt_clear_" + v_tabTag.tab_id + "' onclick='deleteCommandList()' class='bt_execute bt_red' style='margin: 0 0px 5px 0px;' title='Clear List'>Clear List</button>";

	v_tabTag.commandHistory.currentPage = 1;
	v_tabTag.commandHistory.pages = 1;
	v_tabTag.commandHistory.spanNumPages = document.getElementById('cl_num_pages_' + v_tabTag.tab_id);
	v_tabTag.commandHistory.spanNumPages.innerHTML = 1;
	v_tabTag.commandHistory.spanCurrPage = document.getElementById('cl_curr_page_' + v_tabTag.tab_id);
	v_tabTag.commandHistory.spanCurrPage.innerHTML = 1;

	refreshCommandList();
}

function commandHistoryNextPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage < v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.pages) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage += 1;
		refreshCommandList();
	}
}

function commandHistoryPreviousPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage > 1) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage -= 1;
		refreshCommandList();
	}
}

function commandHistoryFirstPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage != 1) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage = 1;
		refreshCommandList();
	}
}

function commandHistoryLastPage() {
	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage != v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.pages) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.pages;
		refreshCommandList();
	}
}

function commandHistoryOpenCmd(p_index) {
	var v_command = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.grid.getDataAtRow(p_index)[4];
	v_connTabControl.tag.createQueryTab('Query');
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(v_command);
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function refreshCommandList() {
	execAjax(
		'/get_command_list/',
		JSON.stringify({
			'p_current_page': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage,
			'p_database_index': v_connTabControl.selectedTab.tag.selectedDatabaseIndex
		}),
		function(p_return) {
			if(p_return.v_data.commandList.length == 0) {
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage = 1;
			}

			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.pages = p_return.v_data.pages;
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.spanNumPages.innerHTML = p_return.v_data.pages;
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.spanCurrPage.innerHTML = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage;
		},
		null,
		'box'
	);
}

function closeCommandHistory() {
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.div.style.display = 'none';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.grid.destroy();
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.grid = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.headerDiv.innerHTML = '';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.gridDiv.innerHTML = '';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.currentPage = 1;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.pages = 1;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.spanNumPages = null;
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.spanCurrPages = null;
}
