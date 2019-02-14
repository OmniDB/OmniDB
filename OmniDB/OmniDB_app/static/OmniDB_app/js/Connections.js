/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function () {
	v_connections_data = new Object();
	v_connections_data.v_groups_visible = false;
	v_connections_data.ht = null;
	v_connections_data.v_group_list = null;
	v_connections_data.v_group_last_selected = null;
	v_connections_data.v_group_changed = false;
	v_connections_data.v_next_conn_id = -1;
});

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
		'ssh_enabled': false,
		'group_changed': true
	})
	v_connections_data.ht.getSourceData().push([false,'postgresql','','','','','','',false,'','22','','','',"<i title='Remove' class='fas fa-times action-grid action-close' onclick='dropConnection()'></i>"]);
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
			true,
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
			true,
			true);
}

/// <summary>
/// Saves all changes in the connections list.
/// </summary>
function saveConnections(p_callback) {

	var v_data_list = [];
	var v_conn_id_list = [];
	var v_conn_group_list = [];

	for (var i=0; i < v_connections_data.v_conn_ids.length; i++) {
		var v_temp_row = null;
		if (v_connections_data.v_conn_ids[i].mode!=0) {

		}
		if (v_connections_data.v_conn_ids[i].mode!=0 || v_connections_data.v_conn_ids[i].group_changed) {
			var v_clone = jQuery.extend(true, {}, v_connections_data.v_conn_ids[i]);
			var v_temp_row = v_connections_data.ht.getDataAtRow(v_connections_data.v_conn_ids[i].v_cellMeta.visualRow);
			delete v_clone['v_cellMeta'];
			v_clone['group_value'] = v_temp_row[0]
			v_conn_id_list.push(v_clone)
			if (v_connections_data.v_conn_ids[i].mode!=0) {
				v_temp_row.shift();
				v_data_list.push([v_temp_row[0],v_temp_row[1],v_temp_row[2],v_temp_row[3],v_temp_row[4],v_temp_row[5],v_temp_row[6],v_temp_row[7],v_temp_row[8],v_temp_row[9],v_temp_row[10],v_temp_row[11],v_temp_row[12]])
			}
			else {
				v_data_list.push([]);
			}
		}
	}

	var input = JSON.stringify({"p_data_list": v_data_list, "p_conn_id_list": v_conn_id_list, "p_group_id": v_connections_data.v_group_last_selected});

	execAjax('/save_connections/',
			input,
			function() {
				document.getElementById('div_save').style.visibility = 'hidden';
				if (v_connections_data.v_group_changed==true) {
					getGroups(true);
					v_connections_data.v_group_changed = false;
				}
				else
					showConnectionList();

				if (p_callback)
					p_callback();

			},
			null,
			'box');

}

function groupChange(p_value) {

	if (v_connections_data.v_group_changed) {

		showConfirm('There are changes on the connections list, would you like to save them?',
					function() {

						saveConnections();

					},
					function() {
						document.getElementById('group_selector').value = v_connections_data.v_group_last_selected;
					});


	}
	else {
		v_connections_data.v_group_last_selected = p_value;
		if (p_value!=-1) {
			document.getElementById('div_edit_group').style.display = 'inline-block';
			document.getElementById('div_delete_group').style.display = 'inline-block';
			v_connections_data.v_groups_visible = true;
			configureConnectionGroups(p_value);
		}
		else {
			document.getElementById('div_edit_group').style.display = 'none';
			document.getElementById('div_delete_group').style.display = 'none';
			document.getElementById('group_selector').value = -1;

			v_connections_data.v_groups_visible = false;

			if (v_connections_data.ht) {
				var v_conn_ids_indexes = [];
				var v_data = v_connections_data.ht.getData();
				for (var i=0; i < v_data.length; i++) {
					var v_row = v_connections_data.v_conn_ids.getConnIndexById(v_connections_data.ht.getCellMeta(i, 0).v_conn_id);
					v_conn_ids_indexes.push(v_row);
					v_data[i][0] = false;
					v_connections_data.v_conn_ids[v_row].group_changed = false;
				}
				v_connections_data.v_group_changed = false;
				v_connections_data.ht.loadData(v_data);

				//fixing cells metadatas
				for(var i = 0; i < v_conn_ids_indexes.length; i++) {
					var v_cellMeta = v_connections_data.ht.getCellMeta(i, 0);
					v_cellMeta.v_conn_id = v_connections_data.v_conn_ids[v_conn_ids_indexes[i]].id;
					v_connections_data.v_conn_ids[v_conn_ids_indexes[i]].v_cellMeta = v_cellMeta
				}
			}
		}
	}
}

function configureConnectionGroups(p_value) {
	if (v_connections_data.v_groups_visible) {
		var v_current_group = null;
		for (var i=0; i<v_connections_data.v_group_list.length; i++) {
			if (v_connections_data.v_group_list[i].id==p_value) {
				v_current_group = v_connections_data.v_group_list[i];
				break;
			}
		}
		if (v_current_group != null) {
			var v_conn_ids_indexes = [];
			var v_data = v_connections_data.ht.getData();
			for (var i=0; i < v_data.length; i++) {
				var v_id = v_connections_data.ht.getCellMeta(i, 0).v_conn_id;
				var v_row = v_connections_data.v_conn_ids.getConnIndexById(v_id);
				v_conn_ids_indexes.push(v_row);
				if (v_current_group.conn_list.includes(v_id)) {
					v_data[i][0] = true;
				}
				else {
					v_data[i][0] = false;
				}
				v_connections_data.v_conn_ids[v_row].group_changed = false;
			}
			v_connections_data.v_group_changed = false;
			v_connections_data.ht.loadData(v_data);

			//fixing cells metadatas
			for(var i = 0; i < v_conn_ids_indexes.length; i++) {
				var v_cellMeta = v_connections_data.ht.getCellMeta(i, 0);
				v_cellMeta.v_conn_id = v_connections_data.v_conn_ids[v_conn_ids_indexes[i]].id;
				v_connections_data.v_conn_ids[v_conn_ids_indexes[i]].v_cellMeta = v_cellMeta
			}
		}
	}
}

function getGroups(p_reload_connections) {
	execAjax('/get_groups/',
			JSON.stringify({}),
			function(p_return) {
				v_connections_data.v_group_list = p_return.v_data;
				var select = document.getElementById('group_selector');
				var current_value = select.value;
				select.innerHTML = '';
				var option = document.createElement('option');
				option.value = -1;
				option.textContent = 'Select group';
				select.appendChild(option);
				var found = false;
				for (var i=0; i<p_return.v_data.length; i++) {
					option = document.createElement('option');
					option.value = p_return.v_data[i].id;
					option.textContent = p_return.v_data[i].name;
					if (option.value == current_value) {
						option.selected = true;
						found = true;
					}
					select.appendChild(option);
				}
				if (!found==true) {
					groupChange(-1);
				}

				if (p_reload_connections)
					showConnectionList();

			},
			null,
			'box');

}

function newGroupConfirm(p_name) {
	execAjax('/new_group/',
			JSON.stringify({"p_name": p_name}),
			function(p_return) {
				getGroups();
			},
			null,
			'box');
}

function editGroupConfirm(p_id, p_name) {
	execAjax('/edit_group/',
			JSON.stringify({"p_id": p_id,"p_name": p_name}),
			function(p_return) {
				getGroups();
			},
			null,
			'box');
}

function deleteGroupConfirm(p_group_id) {
	execAjax('/delete_group/',
			JSON.stringify({"p_id": p_group_id}),
			function(p_return) {
				getGroups();
			},
			null,
			'box');
}

function newGroup() {
	showConfirm('<input id="group_name_input"/ placeholder="Group Name" style="width: 200px;">',
							function() {
								newGroupConfirm(document.getElementById('group_name_input').value);
							});
	var v_input = document.getElementById('group_name_input');
	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('button_confirm_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('button_confirm_cancel').click();
	}
	document.getElementById('group_name_input').focus();
}

function editGroup() {
	var v_select = document.getElementById('group_selector');
	showConfirm('<input id="group_name_input"/ placeholder="Group Name" value="' + v_select.options[v_select.selectedIndex].text + '" style="width: 200px;">',
							function() {
								editGroupConfirm(
									document.getElementById('group_selector').value,
									document.getElementById('group_name_input').value);
							});
	var v_input = document.getElementById('group_name_input');
	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('button_confirm_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('button_confirm_cancel').click();
	}
	document.getElementById('group_name_input').focus();
}

function deleteGroup() {

	var v_group_id = document.getElementById('group_selector').value;

	//Check if group isn't already opened in a connection tab
	for (var i=0; i < v_connTabControl.tabList.length; i++) {
		var v_tab = v_connTabControl.tabList[i];
		if (v_tab.tag && v_tab.tag.mode=='connection') {
			if (v_group_id == v_tab.tag.selectedGroupIndex) {
				showAlert('This group is being used in one of the connection tabs, please close the tab or change the active group there.')
				return null;
			}
		}
	}

	showConfirm('Are you sure you want to delete the current group?',
							function() {
								deleteGroupConfirm(v_group_id);
							});
}

function startConnectionManagement() {
	v_connections_data.v_group_last_selected = -1;
	v_connections_data.v_group_changed = false;
	groupChange(-1);
	getGroups(true);
}

function showConnectionList() {

	v_connections_data.v_next_conn_id = -1;

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

				var ConnColumnProperties = [];

				var col = new Object();
				col.title =  'Group';
				col.type = "checkbox",
				col.checkedTemplate = true,
        col.uncheckedTemplate = false
				col.width = '60'
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Technology';
				col.type = 'dropdown';
				col.width = '80'
				col.allowInvalid = false,
				col.source = p_return.v_data.v_technologies;
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Connection String';
				col.width = '160'
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Server';
				col.width = '120'
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Port';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Database';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'User';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Title';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Tunnel';
				col.type = "checkbox",
				col.checkedTemplate = true,
        		col.uncheckedTemplate = false
				col.width = '60'
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Server';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Port';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'SSH User';
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Password';
				col.type = "password",
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'SSH Key';
				col.width = '80'
				ConnColumnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.readOnly = true;
				col.width = '80'
				ConnColumnProperties.push(col);

				var v_div_result = document.getElementById('connection_list_div_grid');

				if (v_div_result.innerHTML!='') {
					v_connections_data.ht.destroy();
				}

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

				v_connections_data.ht = new Handsontable(v_div_result,
					{
						data: p_return.v_data.v_data,
						columns : ConnColumnProperties,
						colHeaders : true,
						manualColumnResize: true,
						minSpareCols :0,
						minSpareRows :0,
						fillHandle:false,
						columnSorting: true,
						sortIndicator: true,
						stretchH: "all",
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
								else if (key === 'copy') {
									his.selectCell(options[0].start.row,options[0].start.col,options[0].end.row,options[0].end.col);
									document.execCommand('copy');
								}
							},
							items: {
								"copy": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-copy cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Copy</div>'},
								"view_data": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
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

									if (columnIndex==1 && newValue=='') {
										v_connections_data.ht.setDataAtCell(rowIndex,columnIndex,oldValue);
									}
							    else if(oldValue != newValue && v_connections_data.v_conn_ids[rowIndex].mode!=2 && columnIndex!=0) {

											if (v_connections_data.v_conn_ids[rowIndex].mode!=-1)
												v_connections_data.v_conn_ids[rowIndex].mode = 1;
											else
												v_connections_data.v_conn_ids[rowIndex].old_mode = 1;

							        document.getElementById('div_save').style.visibility = 'visible';

							    }
									else if (columnIndex==0) {
										v_connections_data.v_conn_ids[rowIndex].group_changed = true;
										v_connections_data.v_group_changed = true;
										document.getElementById('div_save').style.visibility = 'visible';
									}
							});

						},
						cells: function (row, col, prop) {

							if (v_connections_data.v_conn_ids.length!=0 && row < v_connections_data.v_conn_ids.length) {

								var cellProperties = {};

								if (!v_connections_data.v_groups_visible && col==0) {
									cellProperties.renderer = grayHtmlRenderer;
									cellProperties.readOnly = true;
								}
								else {
									var v_even = row % 2 == 0;

									var v_read_only = false;

									if (v_connections_data.v_conn_ids[row].locked && col!=0) {
										cellProperties.renderer = grayHtmlRenderer;
										cellProperties.readOnly = true;
										v_read_only = true;
									}

									if (col == 14)
										v_read_only = true;

									if (!v_read_only) {
										cellProperties.readOnly = false;
										if (v_connections_data.v_conn_ids[row].mode==2)
											cellProperties.renderer = greenHtmlRenderer;
										else if (v_connections_data.v_conn_ids[row].mode==-1)
											cellProperties.renderer = redHtmlRenderer;
										else if (v_connections_data.v_conn_ids[row].mode==1)
											cellProperties.renderer = yellowHtmlRenderer;
										else if (v_connections_data.v_conn_ids[row].group_changed && col==0)
											cellProperties.renderer = yellowHtmlRenderer;
										else if (v_even % 2 == 0)
											cellProperties.renderer = blueHtmlRenderer;
										else
											cellProperties.renderer =whiteHtmlRenderer;

									}
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
				configureConnectionGroups(document.getElementById('group_selector').value);
			},
			null,
			'box',
			true);

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

				//check if group still exists
				var v_found = false;
				for (var j=0; j<v_connTabControl.tag.groups.length; j++) {
					if (v_tab.tag.selectedGroupIndex==v_connTabControl.tag.groups[j].v_group_id) {
						v_found = true;
						break;
					}
				}
				if (!v_found) {
					v_tab.tag.selectedGroupIndex = 0;
				}

				v_tab.tag.divSelectGroup.innerHTML = v_connTabControl.tag.selectGroupHTML;
				v_tab.tag.divSelectGroup.childNodes[0].value = v_tab.tag.selectedGroupIndex;
				v_tab.tag.dd_group_object = $(v_tab.tag.divSelectGroup.childNodes[0]).msDropDown().data("dd");
				v_tab.tag.dd_group_selected_index = v_tab.tag.dd_group_object.selectedIndex;

				changeGroup(v_tab.tag.selectedGroupIndex)

			}
		}

		if (p_index)
			v_connTabControl.tag.createConnTab(p_index);

}
