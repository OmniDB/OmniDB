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

/// <summary>
/// Displays question to create new connection.
/// </summary>
function newConnection() {

	if (v_connections_data.v_cellChanges.length>0)
		showConfirm2('There are changes on the connections list, would you like to save them?',
					function() {

						saveConnections();
						newConnectionConfirm();

					},
					function() {

						newConnectionConfirm();

					});
	else
		newConnectionConfirm();

}

/// <summary>
/// Removes connection.
/// </summary>
/// <param name="p_id">Connection ID.</param>
function removeConnectionConfirm(p_id) {

	var input = JSON.stringify({"p_id": p_id});

	execAjax('/remove_connection/',
			input,
			function(p_return) {

				document.getElementById('div_save').style.visibility = 'hidden';
				listConnections();

			},
			null,
			'box');

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
			null,
			'box');

}

/// <summary>
/// Displays question to test specific connection.
/// </summary>
/// <param name="p_index">Connection index in the connection list.</param>
function testConnection(p_index) {

	if (v_connections_data.v_cellChanges.length>0)
		showConfirm('There are changes on the connections list, would you like to save them?',
					function() {

						saveConnections();
						testConnectionConfirm(p_index);

					});
	  else
	  	testConnectionConfirm(p_index);

}

/// <summary>
/// Removes specific connection.
/// </summary>
/// <param name="p_id">Connection ID.</param>
function removeConnection(p_id) {

	showConfirm('Are you sure you want to remove this connection?',
	            function() {

					if (v_connections_data.v_cellChanges.length>0)
						showConfirm2('There are changes on the connections list, would you like to save them?',
						            function() {

						            	saveConnections();
						            	removeConnectionConfirm(p_id);

						            },
						            function() {

						            	removeConnectionConfirm(p_id);

						            });
	              else
	              	removeConnectionConfirm(p_id);

	            });

}

/// <summary>
/// Saves all changes in the connections list.
/// </summary>
function saveConnections() {

	if (v_connections_data.v_cellChanges.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_conn_id_list = [];

	$.each(v_connections_data.v_cellChanges, function(i, el){
	    if($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) v_unique_rows_changed.push(el['rowIndex']);
	});

	$.each(v_unique_rows_changed, function(i, el){
	    v_data_changed[i] = v_connections_data.ht.getDataAtRow(el);
	    v_conn_id_list[i] = v_connections_data.v_conn_ids[el];
	});


	var input = JSON.stringify({"p_data": v_data_changed, "p_conn_id_list": v_conn_id_list});

	execAjax('/save_connections/',
			input,
			function() {

				v_connections_data.v_cellChanges = [];
				document.getElementById('div_save').style.visibility = 'hidden';
				listConnections();

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

				checkSessionMessage();

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
				col.title =  'Password';
				col.type = 'password';
				col.hashLength = 10;
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
				v_connections_data.v_cellChanges = [];

				var container = v_div_result;
				v_connections_data.ht = new Handsontable(container,
														{
															data: p_return.v_data.v_data,
															columns : columnProperties,
															colHeaders : true,
															manualColumnResize: true,
															maxRows: p_return.v_data.v_data.length,
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

																    if(oldValue != newValue) {

															        	v_connections_data.v_cellChanges.push(cellChange);
																        document.getElementById('div_save').style.visibility = 'visible';

																    }
																});

															},
															afterRender: function () {

																$.each(v_connections_data.v_cellChanges, function (index, element) {
														    		var cellChange = element;
																    var rowIndex = cellChange['rowIndex'];
																    var columnIndex = cellChange['columnIndex'];
																    var cell = v_connections_data.ht.getCell(rowIndex, columnIndex);
																    var foreColor = '#000';
																    var backgroundColor = 'rgb(255, 251, 215)';
																    //cell.style.color = foreColor;
																    //cell.style.background = backgroundColor;
																    cell.className = 'cellEdit';
																});

															},
															cells: function (row, col, prop) {

																var cellProperties = {};
																if (row % 2 == 0)
																	cellProperties.renderer = blueHtmlRenderer;

																return cellProperties;

															}
														});


				},
				null,
				'box');

}
