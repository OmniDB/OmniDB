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
$(function() {

	listConnections();
	checkSessionMessage();


});

/// <summary>
/// Creates a new connection.
/// </summary>
function newConnectionConfirm() {

	execAjax('/new_connection/',
			JSON.stringify({}),
			function(p_return) {

				listConnections();

			},
			null,
			'box');

}

function dropConnection() {

	var v_data = v_connections_data.ht.getData();
	var v_row = v_connections_data.ht.getSelected()[0];

	//New connection, just remove from grid
	if (v_connections_data.v_conn_ids[v_row].mode==2) {

		v_connections_data.v_conn_ids.splice(v_row,1);
		v_data.splice(v_row,1);

		v_connections_data.ht.loadData(v_data);

	}
	else {

		var v_mode = v_connections_data.v_conn_ids[v_row].mode;
		v_connections_data.v_conn_ids[v_row].mode = v_connections_data.v_conn_ids[v_row].old_mode;
		v_connections_data.v_conn_ids[v_row].old_mode = v_mode;

		v_connections_data.ht.loadData(v_data);

	}

	document.getElementById('div_save').style.visibility = 'visible';
}

/// <summary>
/// Displays question to create new connection.
/// </summary>
function newConnection() {

	var v_data = v_connections_data.ht.getData();
	v_data.push(['postgresql','','','','','','<img src="/static/OmniDB_app/images/tab_close.png" class="img_ht" onclick="dropConnection()"/>']);
	v_connections_data.v_conn_ids.push({'id': -1, 'mode': 2, 'old_mode': 2 })
	v_connections_data.ht.loadData(v_data);

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
					showError(p_return.v_data);

			},
			function(p_return) {
				if (p_return.v_data.password_timeout) {
					showPasswordPrompt(
						p_index,
						function() {
							testConnectionConfirm(p_index);
						},
						null
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

						saveConnections(p_index);

					});
	  else
	  	testConnectionConfirm(p_index);

}

/// <summary>
/// Saves all changes in the connections list.
/// </summary>
function saveConnections(p_index) {

	var v_data_list = [];
	var v_conn_id_list = [];

	for (var i=0; i < v_connections_data.v_conn_ids.length; i++) {
		if (v_connections_data.v_conn_ids[i].mode!=0) {
			v_conn_id_list.push(v_connections_data.v_conn_ids[i])
			var v_temp_row = v_connections_data.ht.getDataAtRow(i)
			v_data_list.push([v_temp_row[0],v_temp_row[1],v_temp_row[2],v_temp_row[3],v_temp_row[4],v_temp_row[5]])
		}
	}


	var input = JSON.stringify({"p_data_list": v_data_list, "p_conn_id_list": v_conn_id_list});

	execAjax('/save_connections/',
			input,
			function() {

				document.getElementById('div_save').style.visibility = 'hidden';
				listConnections();
				if (p_index)
					testConnectionConfirm(p_index);

			},
			null,
			'box');

}

/// <summary>
/// Retrieving and displaying connections.
/// </summary>
function listConnections() {

	execAjax('/get_connections/',
			JSON.stringify({}),
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Technology';
				col.type = 'dropdown';
				col.source = p_return.v_data.v_technologies;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Server';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Port';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Service';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'User';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Alias';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.readOnly = true;
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_conn_list');

				if (v_div_result.innerHTML!='') {
					v_connections_data.ht.destroy();
				}

				v_connections_data = new Object();
				v_connections_data.v_conn_ids = p_return.v_data.v_conn_ids;

				var container = v_div_result;
				v_connections_data.ht = new Handsontable(container,
														{
															data: p_return.v_data.v_data,
															columns : columnProperties,
															colHeaders : true,
															manualColumnResize: true,
															beforeChange: function (changes, source) {

																if (!changes)
																    return;

																$.each(changes, function (index, element) {
																    var change = element;
																    var rowIndex = change[0];
																    var columnIndex = change[1];
																    var oldValue = change[2];
																    var newValue = change[3];

																    var cellChange = {
																        'rowIndex': rowIndex,
																        'columnIndex': columnIndex
																    };

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

																if (v_connections_data.v_conn_ids.length!=0) {
																	var cellProperties = {};
																	if (v_connections_data.v_conn_ids[row].mode==2)
																		cellProperties.renderer = greenHtmlRenderer;
																	else if (v_connections_data.v_conn_ids[row].mode==-1)
																		cellProperties.renderer = redHtmlRenderer;
																	else if (v_connections_data.v_conn_ids[row].mode==1)
																		cellProperties.renderer = yellowHtmlRenderer;
																	else if (row % 2 == 0)
																		cellProperties.renderer = blueHtmlRenderer;
																	else
																		cellProperties.renderer =whiteHtmlRenderer;

																	return cellProperties;
																}

															}
														});


				},
				null,
				'box');

}
