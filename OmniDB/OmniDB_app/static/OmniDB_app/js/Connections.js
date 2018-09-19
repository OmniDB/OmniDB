/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Creates a new connection.
/// </summary>
function newConnectionConfirm() {

	execAjax('/new_connection/',
			JSON.stringify({}),
			function(p_return) {

				showConnectionList();

			},
			null,
			'box');

}

function dropConnection() {

	var v_row = v_connections_data.ht.getSelected()[0][0];
	v_row = v_connections_data.v_conn_ids.getConnIndexById(v_connections_data.ht.getCellMeta(v_row, 0).v_conn_id);

	//New connection, just remove from grid
	if (v_connections_data.v_conn_ids[v_row].mode==2) {

		v_connections_data.v_conn_ids.splice(v_row,1);
		v_connections_data.ht.alter('remove_row',v_row);


	}
	else {

		var v_mode = v_connections_data.v_conn_ids[v_row].mode;
		v_connections_data.v_conn_ids[v_row].mode = v_connections_data.v_conn_ids[v_row].old_mode;
		v_connections_data.v_conn_ids[v_row].old_mode = v_mode;

		v_connections_data.ht.render()

	}

	document.getElementById('div_save').style.visibility = 'visible';
}

/// <summary>
/// Displays question to create new connection.
/// </summary>
function newConnection() {

	var v_conn_id = v_connections_data.v_next_conn_id;
	v_connections_data.v_next_conn_id--;
	v_connections_data.v_conn_ids.push({
		'id': v_conn_id,
		'mode': 2,
		'old_mode': 2,
		'ssh_server': '',
		'ssh_port': '22',
		'ssh_user': '',
		'ssh_password': '',
		'ssh_key': '',
		'ssh_enabled': false
	})
	v_connections_data.ht.getSourceData().push(['postgresql','','','','','',false,'','22','','','','<img src="/static/OmniDB_app/images/tab_close.png" class="img_ht" onclick="dropConnection()"/>']);
	v_connections_data.ht.render();
	var v_cellMeta = v_connections_data.ht.getCellMeta(v_connections_data.v_conn_ids.length - 1, 0);
	v_cellMeta.v_conn_id = v_conn_id;
	v_connections_data.v_conn_ids[v_connections_data.v_conn_ids.length - 1].v_cellMeta = v_cellMeta

	var v_div_result = document.getElementById('connection_list_div_grid');

	v_div_result.childNodes[0].childNodes[0].scrollTop = v_div_result.childNodes[0].childNodes[0].scrollHeight;

	document.getElementById('div_save').style.visibility = 'visible';

}

/// <summary>
/// Tests specific connection.
/// </summary>
/// <param name="p_index">Connection index in the connection list.</param>
function testConnectionConfirm(p_index) {

	var input = JSON.stringify({"p_index": p_index});

	execAjax('/test_connection/',
			input,
			function(p_return) {

				if (p_return.v_data=="Connection successful.")
					showAlert(p_return.v_data);
				else
					showPasswordPrompt(
						p_index,
						function() {
							testConnectionConfirm(p_index);
						},
						null,
						p_return.v_data,
						false
					);

			},
			function(p_return) {
				if (p_return.v_data.password_timeout) {
					showPasswordPrompt(
						p_index,
						function() {
							testConnectionConfirm(p_index);
						},
						null,
						p_return.v_data.message,
						false
					);
				}
			},
			'box',
			true);

}

/// <summary>
/// Displays question to test specific connection.
/// </summary>
/// <param name="p_index">Connection index in the connection list.</param>
function testConnection(p_index) {

	var v_has_changes = false

	for (var i=0; i < v_connections_data.v_conn_ids.length; i++) {
		if (v_connections_data.v_conn_ids[i].mode!=0) {
			v_has_changes = true;
			break;
		}
	}

	if (v_has_changes)
		showConfirm('There are changes on the connections list, would you like to save them?',
					function() {

						saveConnections(function() { testConnectionConfirm(p_index); });

					});
	  else
	  	testConnectionConfirm(p_index);

}

/// <summary>
/// Go to workspace with selected connection.
/// </summary>
function selectConnection(p_index) {

	var v_has_changes = false

	for (var i=0; i < v_connections_data.v_conn_ids.length; i++) {
		if (v_connections_data.v_conn_ids[i].mode!=0) {
			v_has_changes = true;
			break;
		}
	}

	if (v_has_changes)
		showConfirm('There are changes on the connections list, would you like to save them?',
					function() {

						saveConnections(function() { selectConnectionConfirm(p_index); });

					});
	  else
	  	selectConnectionConfirm(p_index);

}

function selectConnectionConfirm(p_index) {

	var input = JSON.stringify({"p_index": p_index});

    execAjax('/select_connection/',
			input,
			function(p_return) {

				if (p_return.v_data=="Connection successful.")

					closeConnectionList(p_index);

				else
					showPasswordPrompt(
						p_index,
						function() {
							selectConnection(p_index);
						},
						null,
						p_return.v_data,
						false
					);

			},
			function(p_return) {
				if (p_return.v_data.password_timeout) {
					showPasswordPrompt(
						p_index,
						function() {
							selectConnection(p_index);
						},
						null,
						p_return.v_data.message,
						false
					);
				}
			},
			'box',
			true);

}

/// <summary>
/// Saves all changes in the connections list.
/// </summary>
function saveConnections(p_callback) {

	var v_data_list = [];
	var v_conn_id_list = [];

	for (var i=0; i < v_connections_data.v_conn_ids.length; i++) {
		if (v_connections_data.v_conn_ids[i].mode!=0) {
			var v_clone = jQuery.extend(true, {}, v_connections_data.v_conn_ids[i]);
			delete v_clone['v_cellMeta'];
			v_conn_id_list.push(v_clone)
			var v_temp_row = v_connections_data.ht.getDataAtRow(v_connections_data.v_conn_ids[i].v_cellMeta.visualRow);
			v_data_list.push([v_temp_row[0],v_temp_row[1],v_temp_row[2],v_temp_row[3],v_temp_row[4],v_temp_row[5],v_temp_row[6],v_temp_row[7],v_temp_row[8],v_temp_row[9],v_temp_row[10],v_temp_row[11]])
		}
	}


	var input = JSON.stringify({"p_data_list": v_data_list, "p_conn_id_list": v_conn_id_list});


	execAjax('/save_connections/',
			input,
			function() {

				document.getElementById('div_save').style.visibility = 'hidden';
				showConnectionList();
				if (p_callback)
					p_callback();

			},
			null,
			'box');

}

function showConnectionList() {

  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex});

	document.getElementById('connection_list_div').classList.add('isActive');

	var v_conn_id_list = [];

	for (var i=0; i < v_connTabControl.tabList.length; i++) {
		var v_tab = v_connTabControl.tabList[i];
		if (v_tab.tag && v_tab.tag.mode=='connection') {
			v_conn_id_list.push(v_tab.tag.selectedDatabaseIndex);
		}
	}

	var input = JSON.stringify({"p_conn_id_list": v_conn_id_list});

	execAjax('/get_connections/',
			input,
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Technology';
				col.type = 'dropdown';
				col.allowInvalid = false,
				col.source = p_return.v_data.v_technologies;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Server';
				col.width = '120'
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Port';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Database';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'User';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Title';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Tunnel';
				col.type = "checkbox",
				col.checkedTemplate = true,
        		col.uncheckedTemplate = false
				col.width = '80'
				columnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Server';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Port';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'SSH User';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Password';
				col.type = "password",
				columnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Key';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.readOnly = true;
				col.width = '80'
				columnProperties.push(col);

				var v_div_result = document.getElementById('connection_list_div_grid');

				if (v_div_result.innerHTML!='') {
					v_connections_data.ht.destroy();
				}

				v_connections_data = new Object();
				v_connections_data.v_next_conn_id = -1;
				v_connections_data.v_conn_ids = p_return.v_data.v_conn_ids;

				v_connections_data.v_conn_ids.getConnIndexById = function(p_conn_id) {
					for(var i = 0; i < this.length; i++) {
						if(this[i].id == p_conn_id) {
							return i;
						}
					}

					return -1;
				};

				v_connections_data.v_active = true;

				var container = v_div_result;
				v_connections_data.ht = new Handsontable(container,
					{
						data: p_return.v_data.v_data,
						columns : columnProperties,
						colHeaders : true,
						manualColumnResize: true,
						minSpareCols :0,
						minSpareRows :0,
						fillHandle:false,
						columnSorting: true,
						sortIndicator: true,
						contextMenu: {
							callback: function (key, options) {
								if (key === 'view_data') {
									if (options[0].start.col!=6 && options[0].start.col!=10 && options[0].start.col!=12) {
										var v_row = v_connections_data.v_conn_ids.getConnIndexById(v_connections_data.ht.getCellMeta(options[0].start.row, 0).v_conn_id);

										if (v_connections_data.v_conn_ids[v_row].locked)
									  	editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),false);
										else
											editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),true);
									}
								}
							},
							items: {
								"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"/static/OmniDB_app/images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
							}
				    },
						beforeChange: function (changes, source) {

							if (!changes)
							    return;

							$.each(changes, function (index, element) {
							    var change = element;
							    var rowIndex = change[0];
								var rowIndex = v_connections_data.v_conn_ids.getConnIndexById(v_connections_data.ht.getCellMeta(rowIndex, 0).v_conn_id);
							    var columnIndex = change[1];
							    var oldValue = change[2];
							    var newValue = change[3];

							    if(oldValue != newValue && v_connections_data.v_conn_ids[rowIndex].mode!=2) {

											if (v_connections_data.v_conn_ids[rowIndex].mode!=-1)
												v_connections_data.v_conn_ids[rowIndex].mode = 1;
											else
												v_connections_data.v_conn_ids[rowIndex].old_mode = 1;

							        document.getElementById('div_save').style.visibility = 'visible';

							    }
							});

						},
						cells: function (row, col, prop) {

							if (v_connections_data.v_conn_ids.length!=0 && row < v_connections_data.v_conn_ids.length) {
								var v_even = row % 2 == 0;

								var cellProperties = {};

								var v_read_only = false;

								if (v_connections_data.v_conn_ids[row].locked) {
									cellProperties.renderer = grayHtmlRenderer;
									cellProperties.readOnly = true;
									v_read_only = true;
								}

								if (!v_read_only) {

									if (v_connections_data.v_conn_ids[row].mode==2)
										cellProperties.renderer = greenHtmlRenderer;
									else if (v_connections_data.v_conn_ids[row].mode==-1)
										cellProperties.renderer = redHtmlRenderer;
									else if (v_connections_data.v_conn_ids[row].mode==1)
										cellProperties.renderer = yellowHtmlRenderer;
									else if (v_even % 2 == 0)
										cellProperties.renderer = blueHtmlRenderer;
									else
										cellProperties.renderer =whiteHtmlRenderer;

								}

								return cellProperties;
							}

						}
					}
				);

				for(var i = 0; i < v_connections_data.v_conn_ids.length; i++) {
					var v_cellMeta = v_connections_data.ht.getCellMeta(i, 0);
					v_cellMeta.v_conn_id = v_connections_data.v_conn_ids[i].id;
					v_connections_data.v_conn_ids[i].v_cellMeta = v_cellMeta
				}
			},
			null,
			'box');

}

function showConnectionLocked() {
	showAlert('This connection is locked because there are connection tabs using it, close the tabs first or change the selected connection in these tabs.')
}

function closeConnectionList(p_index) {
  document.getElementById('connection_list_div_grid').innerHTML = '';
	document.getElementById('connection_list_div').classList.remove('isActive');
	document.getElementById('div_save').style.visibility = 'hidden';
  v_connections_data.ht.destroy();
  v_connections_data.ht = null;
	v_connections_data.v_active = false;
	getDatabaseList(false, function() { closeConnectionListFinish(p_index) });
}

function closeConnectionListFinish(p_index) {

		for (var i=0; i < v_connTabControl.tabList.length; i++) {

			var v_tab = v_connTabControl.tabList[i];
			if (v_tab.tag && v_tab.tag.mode=='connection') {

				v_tab.tag.divSelectDB.innerHTML = v_connTabControl.tag.selectHTML;
				v_tab.tag.divSelectDB.childNodes[0].value = v_tab.tag.selectedDatabaseIndex;
				v_tab.tag.dd_object = $(v_tab.tag.divSelectDB.childNodes[0]).msDropDown().data("dd");
				v_tab.tag.dd_selected_index = v_tab.tag.dd_object.selectedIndex;

			}
		}

		if (p_index)
			v_connTabControl.tag.createConnTab(p_index);

}
