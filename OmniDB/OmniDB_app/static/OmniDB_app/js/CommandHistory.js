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

	showConfirm('Are you sure you want to clear command history?',
				function() {

					execAjax('/clear_command_list/',
					JSON.stringify({}),
					function(p_return) {

						v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page = 1;
						refreshCommandList();

					});

				});

}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function showCommandList() {

	if (v_connTabControl.selectedTab.tag.mode=='connection')
		v_connTabControl.tag.createQueryHistoryTab();
	else
		showAlert('Please select a connection tab to view SQL history.')

}

function commandHistoryNextPage() {
	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page < v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.pages) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page += 1;
		refreshCommandList();
	}
}

function commandHistoryPreviousPage() {
	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page > 1) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page -= 1;
		refreshCommandList();
	}
}

function commandHistoryFirstPage() {
	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page != 1) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page = 1;
		refreshCommandList();
	}
}

function commandHistoryLastPage() {
	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page != v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.pages) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.pages;
		refreshCommandList();
	}
}

function commandHistoryOpenCmd(p_index) {
	var v_command = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.getDataAtRow(p_index)[4];
	v_connTabControl.tag.createQueryTab('Query');
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(v_command);
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function refreshCommandList() {

	execAjax('/get_command_list/',
			JSON.stringify({'p_current_page': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page}),
			function(p_return) {

				if (p_return.v_data.command_list.length==0)
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page = 1;

				//$('#div_command_list').show();

				//var v_height  = window.innerHeight - $('#div_command_list_data').offset().top - 60;
				//document.getElementById('div_command_list_data').style.height = v_height + "px";

				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.pages = p_return.v_data.pages;
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.span_num_pages.innerHTML = p_return.v_data.pages;
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.span_curr_page.innerHTML = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.current_page;

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
				col.title =  'Status';
				col.readOnly = true;
				col.width = 50;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Command';
				col.readOnly = true;
				col.width = 400;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.readOnly = true;
				col.width = 60;
				columnProperties.push(col);

				var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

				if (v_div_result.innerHTML!='')
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.destroy();

				var container = v_div_result;
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht = new Handsontable(container,
														{
															data: p_return.v_data.command_list,
															columns : columnProperties,
															colHeaders : true,
															rowHeaders : true,
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
			'box');

}
