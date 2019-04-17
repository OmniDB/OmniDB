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

	listNodes();
	checkSessionMessage();

  $("#chart_start_date").flatpickr({
    enableTime: true,
		allowInput: true
	});
	$("#chart_end_date").flatpickr({
    enableTime: true,
		allowInput: true
	});

  //$('').datetimepicker({format: 'YYYY-MM-DD HH:mm:ss'});
  //$('#chart_end_date').datetimepicker({format: 'YYYY-MM-DD HH:mm:ss'});

});

function clearDatesChart() {

		$("#chart_start_date").flatpickr().clear();
		$("#chart_end_date").flatpickr().clear();
		refreshAlertChart();

}

/// <summary>
/// Creates a new node.
/// </summary>
function newNodeConfirm() {

	execAjax('/new_node/',
			JSON.stringify({}),
			function(p_return) {

				listNodes();

			},
			null,
			'box');

}

/// <summary>
/// Displays question to create new connection.
/// </summary>
function newNode() {

	if (v_nodes_data.v_cellChanges.length>0)
		showConfirm2('There are changes on the nodes list, would you like to save them?',
					function() {

						saveNodes();
						newNodeConfirm();

					},
					function() {

						newNodeConfirm();

					});
	else
		newNodeConfirm();

}

/// <summary>
/// Removes node.
/// </summary>
/// <param name="p_id">Node ID.</param>
function removeNodeConfirm(p_id) {

	var input = JSON.stringify({"p_id": p_id});

	execAjax('/remove_node/',
			input,
			function(p_return) {

				document.getElementById('div_save_nodes').style.visibility = 'hidden';
				listNodes();

			},
			null,
			'box');

}

/// <summary>
/// Removes specific node.
/// </summary>
/// <param name="p_id">Node ID.</param>
function removeNode(p_id) {

	showConfirm('Are you sure you want to remove this node?',
	            function() {

      					if (v_nodes_data.v_cellChanges.length>0)
      						showConfirm2('There are changes on the nodes list, would you like to save them?',
      						            function() {

      						            	saveNodes();
      						            	removeNodeConfirm(p_id);

      						            },
      						            function() {

      						            	removeNodeConfirm(p_id);

      						            });
	              else
	              	removeNodeConfirm(p_id);

	            });

}

function refreshNodeKeyConfirm(p_id) {

	var input = JSON.stringify({"p_id": p_id});

	execAjax('/refresh_node_key/',
			input,
			function(p_return) {

				document.getElementById('div_save_nodes').style.visibility = 'hidden';
				listNodes();

			},
			null,
			'box');

}

function refreshNodeKey(p_id) {

	showConfirm('Are you sure you want to refresh the key?',
	            function() {

      					if (v_nodes_data.v_cellChanges.length>0)
      						showConfirm2('There are changes on the nodes list, would you like to save them?',
      						            function() {

      						            	saveNodes();
      						            	refreshNodeKeyConfirm(p_id);

      						            },
      						            function() {

      						            	refreshNodeKeyConfirm(p_id);

      						            });
	              else
	              	refreshNodeKeyConfirm(p_id);

	            });

}

/// <summary>
/// Saves all changes in the connections list.
/// </summary>
function saveNodes() {

	if (v_nodes_data.v_cellChanges.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_node_id_list = [];

	$.each(v_nodes_data.v_cellChanges, function(i, el){
	    if($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) v_unique_rows_changed.push(el['rowIndex']);
	});

	$.each(v_unique_rows_changed, function(i, el){
	    v_data_changed[i] = v_nodes_data.ht.getDataAtRow(el);
	    v_node_id_list[i] = v_nodes_data.v_node_ids[el];
	});


	var input = JSON.stringify({"p_data": v_data_changed, "p_node_id_list": v_node_id_list});

	execAjax('/save_nodes/',
			input,
			function() {

				v_nodes_data.v_cellChanges = [];
				document.getElementById('div_save_nodes').style.visibility = 'hidden';
				listNodes();

			},
			null,
			'box');

}

/// <summary>
/// Retrieving and displaying nodes.
/// </summary>
function listNodes() {

	execAjax('/get_nodes/',
			JSON.stringify({}),
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Name';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Description';
        col.width = '300px';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Monitor Key';
        col.width = '230px';
				col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.width = '60px';
				col.readOnly = true;
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_node_list');

				if (v_div_result.innerHTML!='') {
					v_nodes_data.ht.destroy();
				}

				v_nodes_data = new Object();
				v_nodes_data.v_node_ids = p_return.v_data.v_node_ids;
				v_nodes_data.v_cellChanges = [];

				var container = v_div_result;
				v_nodes_data.ht = new Handsontable(container,
														{
															licenseKey: 'non-commercial-and-evaluation',
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

															        	v_nodes_data.v_cellChanges.push(cellChange);
																        document.getElementById('div_save_nodes').style.visibility = 'visible';

																    }
																});

															},
															afterRender: function () {

																$.each(v_nodes_data.v_cellChanges, function (index, element) {
														    		var cellChange = element;
																    var rowIndex = cellChange['rowIndex'];
																    var columnIndex = cellChange['columnIndex'];
																    var cell = v_nodes_data.ht.getCell(rowIndex, columnIndex);
																    var foreColor = '#000';
																    var backgroundColor = 'rgb(255, 251, 215)';
																    cell.className = 'cellEdit';
																});

															},
															cells: function (row, col, prop) {

																var cellProperties = {};
																if (row % 2 == 0)
																	cellProperties.renderer = blueHtmlRenderer;

                                if (col == 2 || col == 3)
                                  cellProperties.renderer = grayHtmlRenderer;

																return cellProperties;

															}
														});
				},
				null,
				'box');
}

function viewNode(p_node_id) {
  $('#div_alerts').show();

  var v_width = document.getElementById("div_alerts_box").offsetWidth;

	$('#div_alert_list').width(v_width*0.95 + 'px');

	var v_height  = window.innerHeight - $('#div_alert_list').offset().top - 80;
	document.getElementById('div_alert_list').style.height = v_height + "px";

  listAlerts(p_node_id);
}

/// <summary>
/// Retrieving and displaying alerts.
/// </summary>
function listAlerts(p_node_id) {

  if (p_node_id==null)
    p_node_id = v_alerts_data.v_node_id;

	execAjax('/get_alerts/',
			JSON.stringify({'p_node_id': p_node_id}),
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Name';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Description';
        col.width = '300px';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Enabled';
				col.type = 'checkbox';
				col.checkedTemplate = '1';
        col.uncheckedTemplate = '0';
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Interval';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Timeout';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Min Value';
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Max Value';
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Status';
        col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Acknowledge';
				col.type = 'checkbox';
				col.checkedTemplate = '1';
        col.uncheckedTemplate = '0';
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Last Received Data';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Monitor Count';
        col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Actions';
				col.renderer = 'html';
				col.readOnly = true;
        col.width = '60px';
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_alert_list');

				if (v_div_result.innerHTML!='') {
					v_alerts_data.ht.destroy();
				}

				v_alerts_data = new Object();
        v_alerts_data.v_node_id = p_node_id;
				v_alerts_data.v_alert_ids = p_return.v_data.v_alert_ids;
				v_alerts_data.v_cellChanges = [];

				var container = v_div_result;
				v_alerts_data.ht = new Handsontable(container,
														{
															licenseKey: 'non-commercial-and-evaluation',
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

															        	v_alerts_data.v_cellChanges.push(cellChange);
																        document.getElementById('div_save_alerts').style.visibility = 'visible';

																    }
																});

															},
															afterRender: function () {

																$.each(v_alerts_data.v_cellChanges, function (index, element) {
														    		var cellChange = element;
																    var rowIndex = cellChange['rowIndex'];
																    var columnIndex = cellChange['columnIndex'];
																    var cell = v_alerts_data.ht.getCell(rowIndex, columnIndex);
																    var foreColor = '#000';
																    var backgroundColor = 'rgb(255, 251, 215)';
																    cell.className = 'cellEdit';
																});

															},
															cells: function (row, col, prop) {

																var cellProperties = {};
																if (row % 2 == 0)
																	cellProperties.renderer = blueHtmlRenderer;

                                if (col == 7)
                                  cellProperties.renderer = monitorStatusRenderer;

                                if (col == 9 || col == 10 || col == 11)
                                  cellProperties.renderer = grayHtmlRenderer;

																return cellProperties;

															}
														});
				},
				null,
				'box');
}

/// <summary>
/// Creates a new alert.
/// </summary>
function newAlertConfirm() {

	execAjax('/new_alert/',
			JSON.stringify({'p_node_id': v_alerts_data.v_node_id}),
			function(p_return) {

				listAlerts(v_alerts_data.v_node_id);

			},
			null,
			'box');

}

/// <summary>
/// Displays question to create new alert.
/// </summary>
function newAlert() {

	if (v_nodes_data.v_cellChanges.length>0)
		showConfirm2('There are changes on the alert list, would you like to save them?',
					function() {

						saveAlerts();
						newAlertConfirm();

					},
					function() {

						newAlertConfirm();

					});
	else
		newAlertConfirm();

}

/// <summary>
/// Removes alert.
/// </summary>
/// <param name="p_id">Alert ID.</param>
function removeAlertConfirm(p_id) {

	var input = JSON.stringify({"p_id": p_id});

	execAjax('/remove_alert/',
			input,
			function(p_return) {

				document.getElementById('div_save_nodes').style.visibility = 'hidden';
				listAlerts(v_alerts_data.v_node_id);

			},
			null,
			'box');

}

/// <summary>
/// Removes specific alert.
/// </summary>
/// <param name="p_id">Node ID.</param>
function removeAlert(p_id) {

	showConfirm('Are you sure you want to remove this alert?',
	            function() {

      					if (v_nodes_data.v_cellChanges.length>0)
      						showConfirm2('There are changes on the alerts list, would you like to save them?',
      						            function() {

      						            	saveAlerts();
      						            	removeAlertConfirm(p_id);

      						            },
      						            function() {

      						            	removeAlertConfirm(p_id);

      						            });
	              else
	              	removeAlertConfirm(p_id);

	            });

}

/// <summary>
/// Saves all changes in the alerts list.
/// </summary>
function saveAlerts() {

	if (v_alerts_data.v_cellChanges.length==0)
			return;

	var v_unique_rows_changed = [];
	var v_data_changed = [];
	var v_alert_id_list = [];

	$.each(v_alerts_data.v_cellChanges, function(i, el){
	    if($.inArray(el['rowIndex'], v_unique_rows_changed) === -1) v_unique_rows_changed.push(el['rowIndex']);
	});

	$.each(v_unique_rows_changed, function(i, el){
	    v_data_changed[i] = v_alerts_data.ht.getDataAtRow(el);
	    v_alert_id_list[i] = v_alerts_data.v_alert_ids[el];
	});


	var input = JSON.stringify({"p_data": v_data_changed, "p_alert_id_list": v_alert_id_list});

	execAjax('/save_alerts/',
			input,
			function() {

				v_alerts_data.v_cellChanges = [];
				document.getElementById('div_save_alerts').style.visibility = 'hidden';
				listAlerts(v_alerts_data.v_node_id);

			},
			null,
			'box');

}

function viewAlert(p_alert_id, p_alert_name) {
  $('#div_alert_data').show();

  var v_width = document.getElementById("div_alert_data_box").offsetWidth;

	$('#div_alert_data_list').width(v_width*0.95 + 'px');
	$('#alert_title').html(p_alert_name);

	var v_height  = window.innerHeight - $('#div_alert_data_list').offset().top - 120;
	document.getElementById('div_alert_data_list').style.height = v_height + "px";

  listAlertData(p_alert_id)
}



function listAlertData(p_alert_id) {

  if (p_alert_id==null)
    p_alert_id = v_curr_alert_data.v_alert_id;

	execAjax('/get_alert_data_list/',
			JSON.stringify({'p_alert_id': p_alert_id}),
			function(p_return) {

				window.scrollTo(0,0);

				var columnProperties = [];

				var col = new Object();
				col.title =  'Status';
        col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Value';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Message';
        col.width = '500px';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Date';
        col.readOnly = true;
				columnProperties.push(col);


				var v_div_result = document.getElementById('div_alert_data_list');

				if (v_div_result.innerHTML!='') {
					v_curr_alert_data.ht.destroy();
				}

        v_curr_alert_data =new Object();
        v_curr_alert_data.v_alert_id = p_alert_id;

				var container = v_div_result;
				v_curr_alert_data.ht = new Handsontable(container,
														{
															licenseKey: 'non-commercial-and-evaluation',
															data: p_return.v_data.v_data,
															columns : columnProperties,
															colHeaders : true,
                              rowHeaders : true,
															manualColumnResize: true,
															maxRows: p_return.v_data.v_data.length,
															contextMenu: {
																callback: function (key, options) {

																	if (key === 'view_data') {
																	  	editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),false);
																	}

																},
																items: {
																	"view_data": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
																}
													    },
															cells: function (row, col, prop) {

                                var cellProperties = {};

                                if (col == 0)
                                  cellProperties.renderer = monitorStatusRenderer;
                                else
									                cellProperties.renderer = grayHtmlRenderer;

																return cellProperties;

															}
														});
				},
				null,
				'box');
}

function refreshAlertChart() {

  execAjax('/view_alert_chart/',
      JSON.stringify({'p_alert_id': v_chart_data.v_alert_id,
                      'p_chart_start_date': $('#chart_start_date').val(),
                      'p_chart_end_date': $('#chart_end_date').val()}),
      function(p_return) {

				var ctx = document.getElementById("stat_chart");

        if (v_chart_data.v_chart) {
          v_chart_data.v_chart.destroy();
        }

				var yAxis;
				var v_min_value = parseFloat(p_return.v_data.v_min_value);
				var v_max_value = parseFloat(p_return.v_data.v_max_value);

				if (v_min_value==0 && v_max_value==0)
					yAxis = {
							display: true
					};
				else
					yAxis = {
							display: true,
							ticks: {
								suggestedMin: parseFloat(p_return.v_data.v_min_value),
								max: parseFloat(p_return.v_data.v_max_value)
							}
					};

        v_chart_data.v_chart = new Chart(ctx, {
          type: 'bar',
          data: {
              labels: p_return.v_data.v_labels,
              datasets: [{
                  label: 'OK',
                  data: p_return.v_data.v_values_ok,
                  lineTension: 0,
                  borderWidth: 1,
                  backgroundColor : 'rgba(58, 145, 227,0.4)',
                  borderColor: 'rgb(58, 145, 227)',
									spanGaps: true,
									stack: 0
              },
							{
									label: 'UNKNOWN',
									data: p_return.v_data.v_values_unknown,
									lineTension: 0,
									borderWidth: 1,
									backgroundColor : 'rgba(146, 7, 252,0.4)',
									borderColor: 'rgb(146, 7, 252)',
									spanGaps: true,
									stack: 0
							},
							{
									label: 'WARNING',
									data: p_return.v_data.v_values_warning,
									lineTension: 0,
									borderWidth: 1,
									backgroundColor : 'rgba(255, 165, 0,0.4)',
									borderColor: 'rgb(255, 165, 0)',
									spanGaps: true,
									stack: 0
							},
							{
									label: 'CRITICAL',
									data: p_return.v_data.v_values_critical,
									lineTension: 0,
									borderWidth: 1,
									backgroundColor : 'rgba(255, 0, 0,0.4)',
									borderColor: 'rgb(255, 0, 0)',
									spanGaps: true,
									stack: 0
							}]
          },
          options: {
            responsive: true,
            maintainAspectRatio: false,
            scales: {
                yAxes: [yAxis]
            }
          }
      });

      },
      null,
      'box');


}

function viewAlertChart(p_alert_id,p_alert_name) {
  $('#div_chart').show();
  var v_height  = window.innerHeight - $('#div_chart_container').offset().top - 100 ;
  document.getElementById('stat_chart').style.height = v_height + 'px';

	if (v_chart_data) {
		v_chart_data.v_chart.destroy();
	}

  v_chart_data = new Object();
  v_chart_data.v_title = p_alert_name;
  v_chart_data.v_alert_id = p_alert_id;
  refreshAlertChart();

}

function editCellData(p_ht, p_row, p_col, p_content, p_can_alter) {

	if (v_editContentObject!=null)
		if (v_editContentObject.editor!=null) {
			 v_editContentObject.editor.destroy();
			 document.getElementById('txt_edit_content').innerHTML = '';
		}

	var langTools = ace.require("ace/ext/language_tools");
	var v_editor = ace.edit('txt_edit_content');
	v_editor.setTheme("ace/theme/" + v_editor_theme);
	v_editor.session.setMode("ace/mode/text");

	v_editor.setFontSize(Number(v_editor_font_size));

	v_editor.setOptions({enableBasicAutocompletion: true});

	document.getElementById('txt_edit_content').onclick = function() {
  		v_editor.focus();
    };

	if (p_content!=null)
		v_editor.setValue(p_content);
	else
		v_editor.setValue('');

	v_editor.clearSelection();

	if (p_can_alter)
		v_editor.setReadOnly(false);
	else
		v_editor.setReadOnly(true);

	//Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
	v_editor.commands.bindKey("Cmd-,", null)
	v_editor.commands.bindKey("Ctrl-,", null)
	v_editor.commands.bindKey("Cmd-Delete", null)
	v_editor.commands.bindKey("Ctrl-Delete", null)

	v_editContentObject = new Object();
	v_editContentObject.editor = v_editor;
	v_editContentObject.row = p_row;
	v_editContentObject.col = p_col;
	v_editContentObject.ht = p_ht;

	$('#div_edit_content').addClass('isActive');

}

/// <summary>
/// Hides edit cell window.
/// </summary>
function hideEditContent() {

	$('#div_edit_content').removeClass('isActive');

	v_editContentObject.editor.setValue('');

}
