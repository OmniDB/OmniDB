/*
Copyright 2016 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Startup function.
/// </summary>
$(function () {

	var v_configTabControl = createTabControl('config_tabs',0,null);
	v_configTabControl.selectTabIndex(0);

	v_copyPasteObject = new Object();

	v_copyPasteObject.v_tabControl = createTabControl('find_replace',0,null);
	v_copyPasteObject.v_tabControl.selectTabIndex(0);

	getDatabaseList('sl_database',null);
	getTree();

	var v_height  = $(window).height() - $('#tree1').offset().top - 50;
	document.getElementById('tree1').style.height = v_height + "px"

	var v_contextMenu = {
		'cm_tab' : {
			elements : [
				{
					text : 'Remove Tab',
					icon: 'images/tab_close.png',
					action : function(tab) {
						showConfirm('Are you sure you want to remove this tab?',
		                    function() {
													removeTab(tab);
													tab.removeTab();
		                    });
					}
				},
				{
					text : 'Rename',
					icon: 'images/rename.png',
					action : function(tab) {
						renameTab(tab);
					}
				}
			]
		}
	};

	v_tabControl = createTabControl('tabs',0,v_contextMenu);

	v_alterTabControl = createTabControl('alter_tabs',0,null);

	v_alterTabControl.tabList[0].elementLi.onclick = function() {

		v_alterTabControl.selectTabIndex(0);
		v_alterTableObject.ht.render();
		v_alterTableObject.window = 'columns';

	}

	v_alterTabControl.tabList[1].elementLi.onclick = function() {

		v_alterTabControl.selectTabIndex(1);
		v_alterTableObject.ht_constraints.render();
		v_alterTableObject.window = 'constraints';

	}

	v_alterTabControl.tabList[2].elementLi.onclick = function() {

		if (v_alterTableObject.mode!='alter')
			showAlert('Create the table first.');
		else {
			v_alterTabControl.selectTabIndex(2);
			v_alterTableObject.ht_indexes.render();
			v_alterTableObject.window = 'indexes';
		}

	}

	v_alterTabControl.selectTabIndex(0);
	v_tabControl.createTab('+',false,createTab);

	createTab();

});

/// <summary>
/// Opens copy & paste window.
/// </summary>
function showFindReplace(p_editor) {

	v_copyPasteObject.v_editor = p_editor;

	$('#div_find_replace').show();

	document.getElementById('txt_replacement_text').value = '';
	document.getElementById('txt_replacement_text_new').value = '';

}

/// <summary>
/// Hides copy & paste window.
/// </summary>
function replaceText() {
	
	var v_old_text = v_copyPasteObject.v_editor.getValue();

	var v_new_text = v_old_text.split(document.getElementById('txt_replacement_text').value).join(document.getElementById('txt_replacement_text_new').value);

	v_copyPasteObject.v_editor.setValue(v_new_text);

	hideFindReplace();

}

/// <summary>
/// Opens copy & paste window.
/// </summary>
function hideFindReplace() {

	$('#div_find_replace').hide();

}

/// <summary>
/// Renames tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function renameTab(p_tab) {

	showConfirm('<input id="tab_name"/ value="' + p_tab.text + '" style="width: 200px;">',
	            function() {

					p_tab.renameTab(document.getElementById('tab_name').value);

	            });

}

/// <summary>
/// Removes tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function removeTab(p_tab) {

	if (p_tab.tag.ht!=null) {
		p_tab.tag.ht.destroy();
		p_tab.tag.div_result.innerHTML = '';
	}

	p_tab.tag.editor.destroy();

}

/// <summary>
/// Creates tab.
/// </summary>
function createTab() {

	v_tabControl.removeTabIndex(v_tabControl.tabList.length-1);
	var v_tab = v_tabControl.createTab('Query',true,null,renameTab,'cm_tab',removeTab);
	v_tabControl.selectTab(v_tab);

	var v_html = "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 300px;border: 1px solid #c3c3c3;'></div>" +
				 "<button id='bt_execute' title='Run' style='margin-top: 15px; margin-bottom: 15px; margin-right: 15px; display: inline-block;' onclick='querySQL();'><img src='images/play.png' style='vertical-align: middle;'/></button>" +
				 "<select id='sel_filtered_data_" + v_tab.id + "'><option value='-3' >Script</option><option value='-2' >Execute</option><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option><option value='-1'>Query All rows</option></select>" +
				 "<div id='div_query_info_" + v_tab.id + "' style='display: inline-block; margin-left: 15px; vertical-align: middle;'></div>" +
				 "<button id='bt_export' title='Export Data' style='margin-top: 15px; margin-bottom: 15px; margin-left: 15px; float: right; display: inline-block;' onclick='exportData();'><img src='images/table_export.png' style='vertical-align: middle;'/></button>" +
				 "<select id='sel_export_type_" + v_tab.id + "' style='margin-top: 15px; float: right;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option><option value='DBF' >DBF</option></select>" +
				 "<div id='div_result_" + v_tab.id + "' style='width: 100%; height: 250px; overflow: auto;'></div>";

	var v_div = document.getElementById('div_' + v_tab.id);
	v_div.innerHTML = v_html;

	var v_height  = $(window).height() - $('#div_result_' + v_tab.id).offset().top - 20;

	document.getElementById('div_result_' + v_tab.id).style.height = v_height + "px"

	var langTools = ace.require("ace/ext/language_tools");
	var v_editor = ace.edit('txt_query_' + v_tab.id);
	v_editor.setTheme("ace/theme/" + v_editor_theme);
	v_editor.session.setMode("ace/mode/sql");
	v_editor.commands.bindKey(".", "startAutocomplete");

	v_editor.setFontSize(Number(v_editor_font_size));

	v_editor.commands.bindKey("ctrl-space", null);

	document.getElementById('txt_query_' + v_tab.id).onclick = function() {

		v_editor.focus();

	};


	var command = {
		name: "save",
		bindKey: {
		      mac: v_keybind_object.v_execute_mac,
		      win: v_keybind_object.v_execute
		    },
		exec: function(){
		querySQL();
		}
	}

	v_editor.commands.addCommand(command);

	var command = {
		name: "replace",
		bindKey: {
		      mac: v_keybind_object.v_replace_mac,
		      win: v_keybind_object.v_replace
		    },
		exec: function(){
			v_copyPasteObject.v_tabControl.selectTabIndex(0);
			showFindReplace(v_editor);
		}
	}

	v_editor.commands.addCommand(command);

	var qtags = {
		getCompletions: function(editor, session, pos, prefix, callback) {

			if (v_completer_ready) {

			  	var wordlist = [];

			  	v_completer_ready = false;
			  	setTimeout(function(){ v_completer_ready = true; }, 1000);

			  	if (prefix!='') {

					execAjax('MainDB.aspx/GetCompletions',
							JSON.stringify({ p_prefix: prefix, p_sql: editor.getValue(), p_prefix_pos: editor.session.doc.positionToIndex(editor.selection.getCursor())}),
							function(p_return) {

								if (p_return.v_data.length==0)
									editor.insert('.');

								wordlist = p_return.v_data;
								callback(null, wordlist);

							},
							null,
							'box',
							false);

				}

			}

		}
	}

	langTools.setCompleters([qtags]);
	v_editor.setOptions({enableBasicAutocompletion: true});

	var v_tag = {
		editor: v_editor,
		query_info: document.getElementById('div_query_info_' + v_tab.id),
		div_result: document.getElementById('div_result_' + v_tab.id),
		sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
		sel_export_type : document.getElementById('sel_export_type_' + v_tab.id)
	};

	v_tab.tag = v_tag;

	v_tabControl.createTab('+',false,createTab);

}

/// <summary>
/// Retrieves database list.
/// </summary>
/// <param name="p_sel_id">Selection tag ID.</param>
/// <param name="p_filter">Filtering a specific database technology.</param>
function getDatabaseList(p_sel_id,p_filter) {

	execAjax('MainDB.aspx/GetDatabaseList',
			JSON.stringify({"p_sel_id": p_sel_id, "p_filter": p_filter}),
			function(p_return) {

				document.getElementById('div_select_db').innerHTML = p_return.v_data.v_select_html;
				$('#' + p_sel_id).msDropDown();

			},
			null,
			'box');

}

/// <summary>
/// Changing selected database.
/// </summary>
/// <param name="p_sel_id">Selection tag ID.</param>
/// <param name="p_value">Database ID.</param>
function changeDatabase(p_sel_id,p_value) {

	execAjax('MainDB.aspx/ChangeDatabase',
			JSON.stringify({"p_value": p_value}),
			function(p_return) {

				getTree();

			},
			null,
			'box');

}

/// <summary>
/// Shows or hides graph window.
/// </summary>
/// <param name="p_mode">Mode.</param>
/// <param name="p_graph_type">Graph Type.</param>
function modalGraph(p_mode,p_graph_type) {

    if (p_mode == 'hide') {
        $('#div_graph').hide();
        network.destroy();
    }
    else if (p_mode == 'show') {
        drawGraph(p_graph_type);
    }

}

/// <summary>
/// Draws graph.
/// </summary>
/// <param name="p_graph_type">Graph Type.</param>
function drawGraph(p_graph_type) {

	v_type = '';

	if (p_graph_type==0)
		v_type='DrawGraphSimple';
	else if (p_graph_type==1)
		v_type='DrawGraph';
	else
		v_type='DrawGraphComplete';

	execAjax('MainDB.aspx/' + v_type,
			null,
			function(p_return) {

				$('#div_legend').hide();
				$('#div_graph').show();

				if (p_graph_type==1) {
		        	$('#div_legend').show();

		        	for (i=0; i<6; i++) {
		        		document.getElementById('p_legend_' + i).innerHTML = p_return.v_data.v_legends[i];
		        	}
		        }

	            v_nodes = [];
	            v_edges = [];

	            for (var i=0; i<p_return.v_data.v_nodes.length; i++)
	            {

	            	var v_node_object = new Object();
					v_node_object.data = new Object();
					v_node_object.position = new Object();
					v_node_object.data.id = p_return.v_data.v_nodes[i].id;
					v_node_object.data.label = p_return.v_data.v_nodes[i].label;
					v_node_object.classes = 'group' + p_return.v_data.v_nodes[i].group;

					v_nodes.push(v_node_object);

	            }

	            for (var i=0; i<p_return.v_data.v_edges.length; i++)
	            {
	            	
	            	var v_edge_object = new Object();
					v_edge_object.data = new Object();
					v_edge_object.data.target = p_return.v_data.v_edges[i].from;
					v_edge_object.data.source = p_return.v_data.v_edges[i].to;
					v_edge_object.data.label = p_return.v_data.v_edges[i].label;
					v_edge_object.data.faveColor = '#9dbaea';
					v_edge_object.data.arrowColor = '#9dbaea';
					v_edges.push(v_edge_object);

	            }



				network = window.cy = cytoscape({
					container: document.getElementById('div_graph_content'),
					boxSelectionEnabled: false,
					autounselectify: true,
					layout: {
						name: 'cose',
            			idealEdgeLength: 100,
            			nodeOverlap: 20
					},
					style: [
						{
							selector: 'node',
							style: {
								'content': 'data(label)',
								'text-opacity': 0.5,
								'text-valign': 'top',
								'text-halign': 'right',
								'background-color': '#11479e',
								'text-wrap': 'wrap',


							}
						},
						{
							selector: 'node.group1',
							style: {
								'background-color': 'blue'
							}
						},
						{
							selector: 'node.group2',
							style: {
								'background-color': 'cyan'
							}
						},
						{
							selector: 'node.group3',
							style: {
								'background-color': 'lightgreen'
							}
						},
						{
							selector: 'node.group4',
							style: {
								'background-color': 'yellow'
							}
						},
						{
							selector: 'node.group5',
							style: {
								'background-color': 'orange'
							}
						},
						{
							selector: 'node.group6',
							style: {
								'background-color': 'red'
							}
						},

						{
							selector: 'edge',
							style: {
								'curve-style': 'bezier',
						        'target-arrow-shape': 'triangle',
						        'target-arrow-color': 'data(faveColor)',
						        'line-color': 'data(arrowColor)',
						        'text-opacity': 0.75,
						        'width': 2,
						        'control-point-distances': 50,
						        'content': 'data(label)',
						        'text-wrap': 'wrap',
						        'edge-text-rotation': 'autorotate'
							}
						}
					],

					elements: {
						nodes: v_nodes,
						edges: v_edges
					},
				});

			},
			null,
			'box');

}

/// <summary>
/// Hides statistics.
/// </summary>
function hideStatistics() {

    $('#div_statistics').hide();
    myBarChart.destroy();

}

/// <summary>
/// Retrieves and displays statistics.
/// </summary>
function getStatistics() {

	execAjax('MainDB.aspx/GetStatistics',
			null,
			function(p_return) {

				$('#div_statistics').show();

	            var data = {
				    labels: p_return.v_data.texts,
				    datasets: [{
				            label: "My Second dataset",
				            fillColor: "rgba(151,187,205,0.5)",
				            strokeColor: "rgba(151,187,205,0.8)",
				            highlightFill: "rgba(151,187,205,0.75)",
				            highlightStroke: "rgba(151,187,205,1)",
				            data: p_return.v_data.values
				        }
				    ]
				};

                document.getElementById('tot_records').innerHTML = '<b>Total Records:</b> ' + p_return.v_data.total;
                document.getElementById('stat_chart').width = 400 + 50*p_return.v_data.texts.length;
				var ctx = document.getElementById("stat_chart").getContext("2d");
				myBarChart = new Chart(ctx).Bar(data);

			},
			null,
			'box');


}

/// <summary>
/// Queries and displays query results.
/// </summary>
function querySQL() {

	var v_sql_value = v_tabControl.selectedTab.tag.editor.getValue();
	var v_sel_value = v_tabControl.selectedTab.tag.sel_filtered_data.value;

	if (v_sql_value=='') {
		showAlert('Please provide a string.');
	}
	else {
		var input = JSON.stringify({"p_sql": v_sql_value, "p_select_value" : v_sel_value});

		var start_time = new Date().getTime();

		execAjax('MainDB.aspx/QuerySQL',
				input,
				function(p_return) {

					var v_div_result = v_tabControl.selectedTab.tag.div_result;
					var v_query_info = v_tabControl.selectedTab.tag.query_info;

					if (v_tabControl.selectedTab.tag.ht!=null) {
						v_tabControl.selectedTab.tag.ht.destroy();
						v_tabControl.selectedTab.tag.ht = null;
					}

					v_div_result.innerHTML = '';

					var request_time = new Date().getTime() - start_time;

					if (v_sel_value==-2) {
						v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";
						v_div_result.innerHTML = '';
					}
					else if (v_sel_value==-3) {

						v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";

						v_div_result.innerHTML = p_return.v_data;

					}
					else {

						window.scrollTo(0,0);

						v_query_info.innerHTML = p_return.v_data.v_query_info + "<br/>Response time: " + request_time/1000 + " seconds";

						var columnProperties = [];

						for (var i = 0; i < p_return.v_data.v_col_names.length; i++) {
						    var col = new Object();

						    col.readOnly = true;

						    col.title =  p_return.v_data.v_col_names[i];

							columnProperties.push(col);

						}

						var container = v_div_result;
						v_tabControl.selectedTab.tag.ht = new Handsontable(container,
						{
							data: p_return.v_data.v_data,
							columns : columnProperties,
							colHeaders : true,
							rowHeaders : true,
							copyRowsLimit : 1000000000,
							copyColsLimit : 1000000000,
							manualColumnResize: true,
							contextMenu: {
								callback: function (key, options) {
									if (key === 'view_data') {
									  	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),false);
									}
								},
								items: {
									"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
								}
						    },
				            cells: function (row, col, prop) {
							    var cellProperties = {};
							    if (row % 2 == 0)
									cellProperties.renderer = blueRenderer;
							    return cellProperties;
							}
						});

					}

				},
				null,
				'box');
	}

}

/// <summary>
/// Queries and displays query results.
/// </summary>
function exportData() {

	var v_sql_value = v_tabControl.selectedTab.tag.editor.getValue();
	var v_sel_value = v_tabControl.selectedTab.tag.sel_export_type.value;

	if (v_sql_value=='') {
		showAlert('Please provide a string.');
	}
	else {

		showConfirm('Are you sure you want to export data from the result of this query?',
				function() {

					var input = JSON.stringify({"p_sql": v_sql_value, "p_select_value" : v_sel_value, "p_tab_name" : v_tabControl.selectedTab.text});

					var start_time = new Date().getTime();

					execAjax('MainDB.aspx/ExportData',
							input,
							function(p_return) {

								var iframe = document.createElement('iframe');
								iframe.style.display = 'none';
								iframe.setAttribute("src", "DownloadFile.aspx");
								document.body.appendChild(iframe);
								setTimeout(function(){ iframe.parentElement.removeChild(iframe); }, 5000);

							},
							null,
							'box');

				});
		
	}

}

/// <summary>
/// Hides alter table window.
/// </summary>
function hideAlterTable() {
	
	$('#div_alter_table').hide();

	document.getElementById('div_alter_table_data').innerHTML = '';

	v_alterTableObject.ht_constraints.destroy();
	v_alterTableObject.ht_indexes.destroy();
	v_alterTableObject.ht.destroy();

	document.getElementById('bt_saveAlterTable').style.visibility = 'hidden';

	v_tree_object.refreshTables();

}

/// <summary>
/// Hides edit data window.
/// </summary>
function hideAlterData() {
	
	$('#div_edit_data').hide();

	v_editDataObject.ht.destroy();
	v_editDataObject.editor.destroy();

	document.getElementById('div_edit_data_data').innerHTML = '';

	document.getElementById('bt_saveEditData').style.visibility = 'hidden';

}

/// <summary>
/// Saves alter table changes.
/// </summary>
function saveAlterTable() {

	var v_changedRowsColumnsInfo = [];
	var v_changedRowsColumnsData = [];

	var v_changedRowsConstraintsInfo = [];
	var v_changedRowsConstraintsData = [];

	var v_changedRowsIndexesInfo = [];
	var v_changedRowsIndexesData = [];

	for (var i=0; i < v_alterTableObject.infoRowsColumns.length; i++) {
		if (v_alterTableObject.infoRowsColumns[i].mode!=0) {
			v_alterTableObject.infoRowsColumns[i].index = i;
			v_changedRowsColumnsInfo.push(v_alterTableObject.infoRowsColumns[i]);
			v_changedRowsColumnsData.push(v_alterTableObject.ht.getDataAtRow(i));

		}
	}

	for (var i=0; i < v_alterTableObject.infoRowsConstraints.length; i++) {
		if (v_alterTableObject.infoRowsConstraints[i].mode!=0) {
			v_alterTableObject.infoRowsConstraints[i].index = i;
			v_changedRowsConstraintsInfo.push(v_alterTableObject.infoRowsConstraints[i]);
			var v_row = v_alterTableObject.ht_constraints.getDataAtRow(i);

			v_row[2] = v_row[2].substring(95);

			v_changedRowsConstraintsData.push(v_row);
		}

	}

	for (var i=0; i < v_alterTableObject.infoRowsIndexes.length; i++) {
		if (v_alterTableObject.infoRowsIndexes[i].mode!=0) {
			v_alterTableObject.infoRowsIndexes[i].index = i;
			v_changedRowsIndexesInfo.push(v_alterTableObject.infoRowsIndexes[i]);
			var v_row = v_alterTableObject.ht_indexes.getDataAtRow(i);

			v_row[2] = v_row[2].substring(91);

			v_changedRowsIndexesData.push(v_row);
		}

	}

	var v_new_table_name = document.getElementById('txt_tableNameAlterTable').value;


	var input = JSON.stringify({"p_mode" : v_alterTableObject.mode,"p_new_table_name": v_new_table_name, "p_original_table_name": v_alterTableObject.tableName, "p_data_columns": v_changedRowsColumnsData, "p_row_columns_info": v_changedRowsColumnsInfo, "p_data_constraints": v_changedRowsConstraintsData, "p_row_constraints_info": v_changedRowsConstraintsInfo, "p_data_indexes": v_changedRowsIndexesData, "p_row_indexes_info": v_changedRowsIndexesInfo});

	execAjax('MainDB.aspx/SaveAlterTable',
			input,
			function(p_return) {

				var v_div_commands_log = document.getElementById('div_commands_log_list');
				v_div_commands_log.innerHTML = '';
				var v_commands_log = '';

				var v_has_error = false;

				document.getElementById('bt_saveAlterTable').style.visibility = 'hidden';

				//Creating new table
				if (p_return.v_data.v_create_table_command!=null) {

					if (!p_return.v_data.v_create_table_command.error) {
						startAlterTable('alter',v_new_table_name);
					}
					else {
						v_has_error = true;

						v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_create_table_command.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_create_table_command.v_message + '<br/><br/>';

						document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

					}


				}
				else {

					if (p_return.v_data.v_rename_table_command!=null) {

						if (!p_return.v_data.v_rename_table_command.error) {

							v_alterTableObject.tableName = v_new_table_name;
							document.getElementById('txt_tableNameAlterTable').style.backgroundColor = 'rgb(255, 255, 255)';


							
						}
						else {
							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_rename_table_command.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_rename_table_command.v_message + '<br/><br/>';

							document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

						}


					}
					else {
						document.getElementById('txt_tableNameAlterTable').style.backgroundColor = 'rgb(255, 255, 255)';
					}

					// New column or delete column
					for (var i = p_return.v_data.v_columns_simple_commands_return.length-1; i >= 0; i--) {
						
						if (p_return.v_data.v_columns_simple_commands_return[i].mode==-1) {
							if (!p_return.v_data.v_columns_simple_commands_return[i].error) {

								v_alterTableObject.infoRowsColumns.splice(p_return.v_data.v_columns_simple_commands_return[i].index, 1);
								v_alterTableObject.ht.alter('remove_row', p_return.v_data.v_columns_simple_commands_return[i].index);


							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_message + '<br/><br/>';

								document.getElementById('bt_saveAlterTable').style.visibility = 'visible';
							}
						}
						else if (p_return.v_data.v_columns_simple_commands_return[i].mode==2) {
							if (!p_return.v_data.v_columns_simple_commands_return[i].error) {

								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].mode = 0;
								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].old_mode = -1;

								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].originalColName = v_alterTableObject.ht.getDataAtCell(p_return.v_data.v_columns_simple_commands_return[i].index,0);
								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].originalDataType = v_alterTableObject.ht.getDataAtCell(p_return.v_data.v_columns_simple_commands_return[i].index,1);
								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_simple_commands_return[i].index].originalNullable = v_alterTableObject.ht.getDataAtCell(p_return.v_data.v_columns_simple_commands_return[i].index,2);

							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_simple_commands_return[i].v_message  + '<br/><br/>';

								document.getElementById('bt_saveAlterTable').style.visibility = 'visible';
							}
						}

					}

					var v_has_group_error;

					// Altering column
					for (var i = p_return.v_data.v_columns_group_commands_return.length-1; i >= 0; i--) {

						v_has_group_error = false;
						
						if (p_return.v_data.v_columns_group_commands_return[i].alter_datatype!=null) {
							if (!p_return.v_data.v_columns_group_commands_return[i].alter_datatype.error) {

								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].originalDataType = v_alterTableObject.ht.getDataAtCell(p_return.v_data.v_columns_group_commands_return[i].index,1);

							}
							else {

								v_has_error = true;
								v_has_group_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_datatype.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_datatype.v_message  + '<br/><br/>';


							}

						}

						if (p_return.v_data.v_columns_group_commands_return[i].alter_nullable!=null) {
							if (!p_return.v_data.v_columns_group_commands_return[i].alter_nullable.error) {

								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].originalNullable = v_alterTableObject.ht.getDataAtCell(p_return.v_data.v_columns_group_commands_return[i].index,2);

							}
							else {

								v_has_error = true;
								v_has_group_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_nullable.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_nullable.v_message  + '<br/><br/>';


							}

						}

						if (p_return.v_data.v_columns_group_commands_return[i].alter_colname!=null) {
							if (!p_return.v_data.v_columns_group_commands_return[i].alter_colname.error) {

								v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].originalColName = v_alterTableObject.ht.getDataAtCell(p_return.v_data.v_columns_group_commands_return[i].index,0);

							}
							else {

								v_has_error = true;
								v_has_group_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_colname.v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_columns_group_commands_return[i].alter_colname.v_message  + '<br/><br/>';


							}

						}

						if (!v_has_group_error) {
							v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].mode = 0;
							v_alterTableObject.infoRowsColumns[p_return.v_data.v_columns_group_commands_return[i].index].old_mode = -1;
						}

					}

					// New constraint or delete constraint
					for (var i = p_return.v_data.v_constraints_commands_return.length-1; i >= 0; i--) {
						
						if (p_return.v_data.v_constraints_commands_return[i].mode==-1) {
							if (!p_return.v_data.v_constraints_commands_return[i].error) {

								v_alterTableObject.infoRowsConstraints.splice(p_return.v_data.v_constraints_commands_return[i].index, 1);
								v_alterTableObject.ht_constraints.alter('remove_row', p_return.v_data.v_constraints_commands_return[i].index);


							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_message + '<br/><br/>';

							}
						}
						else if (p_return.v_data.v_constraints_commands_return[i].mode==2) {
							if (!p_return.v_data.v_constraints_commands_return[i].error) {

								v_alterTableObject.infoRowsConstraints[p_return.v_data.v_constraints_commands_return[i].index].mode = 0;
								v_alterTableObject.infoRowsConstraints[p_return.v_data.v_constraints_commands_return[i].index].old_mode = -1;

							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_constraints_commands_return[i].v_message  + '<br/><br/>';

							}
						}

					}

					// New index or delete index
					for (var i = p_return.v_data.v_indexes_commands_return.length-1; i >= 0; i--) {
						
						if (p_return.v_data.v_indexes_commands_return[i].mode==-1) {
							if (!p_return.v_data.v_indexes_commands_return[i].error) {

								v_alterTableObject.infoRowsIndexes.splice(p_return.v_data.v_indexes_commands_return[i].index, 1);
								v_alterTableObject.ht_indexes.alter('remove_row', p_return.v_data.v_indexes_commands_return[i].index);


							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_message + '<br/><br/>';

							}
						}
						else if (p_return.v_data.v_indexes_commands_return[i].mode==2) {
							if (!p_return.v_data.v_indexes_commands_return[i].error) {

								v_alterTableObject.infoRowsIndexes[p_return.v_data.v_indexes_commands_return[i].index].mode = 0;
								v_alterTableObject.infoRowsIndexes[p_return.v_data.v_indexes_commands_return[i].index].old_mode = -1;

							}
							else {

								v_has_error = true;

								v_commands_log += '<b>Command:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data.v_indexes_commands_return[i].v_message  + '<br/><br/>';

							}
						}

					}
				}

				if (v_has_error) {
					v_div_commands_log.innerHTML = v_commands_log;
					$('#div_commands_log').show();

				}
				else {
					document.getElementById('bt_saveAlterTable').style.visibility = 'hidden';
				}

				v_alterTableObject.ht.render();
				v_alterTableObject.ht_constraints.render();
				v_alterTableObject.ht_indexes.render();

			},
			null,
			'box');

}

/// <summary>
/// Saves edit data changes.
/// </summary>
function saveEditData() {

	var v_changedRowsInfo = [];
	var v_changedRowsData = [];

	for (var i = 0; i < v_editDataObject.infoRows.length; i++) {
		if (v_editDataObject.infoRows[i].mode!=0) {
			v_editDataObject.infoRows[i].index = i;
			v_changedRowsInfo.push(v_editDataObject.infoRows[i]);
			v_changedRowsData.push(v_editDataObject.ht.getDataAtRow(i));
		}
	}

	var input = JSON.stringify({"p_table_name": v_editDataObject.table, "p_data_rows": v_changedRowsData, "p_rows_info": v_changedRowsInfo, "p_columns": v_editDataObject.columns, "p_pk_info" : v_editDataObject.pk});

	execAjax('MainDB.aspx/SaveEditData',
			input,
			function(p_return) {

				var v_div_commands_log = document.getElementById('div_commands_log_list');
				v_div_commands_log.innerHTML = '';
				var v_commands_log = '';

				var v_has_error = false;

				document.getElementById('bt_saveEditData').style.visibility = 'hidden';

				for (var i = p_return.v_data.length-1; i >= 0; i--) {
					
					if (p_return.v_data[i].mode==-1) {
						if (!p_return.v_data[i].error) {

							v_editDataObject.infoRows.splice(p_return.v_data[i].index, 1);
							v_editDataObject.ht.alter('remove_row', p_return.v_data[i].index);

						}
						else {

							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data[i].v_message + '<br/><br/>';

							document.getElementById('bt_saveEditData').style.visibility = 'visible';
						}
					}
					else if (p_return.v_data[i].mode==2) {
						if (!p_return.v_data[i].error) {

							v_editDataObject.infoRows[p_return.v_data[i].index].mode = 0;
							v_editDataObject.infoRows[p_return.v_data[i].index].old_mode = -1;
							v_editDataObject.infoRows[p_return.v_data[i].index].changed_cols = [];

							//Creating pk
							var v_pk_list = [];

							for (var j = 0; j < v_editDataObject.pk.length; j++) {
								
								var v_pk = { v_column: v_editDataObject.pk[j].v_column,
											 v_value : v_editDataObject.ht.getDataAtCell(p_return.v_data[i].index, v_editDataObject.pk[j].v_index + 1)
										   };
							    v_pk_list.push(v_pk);
							}

							v_editDataObject.infoRows[p_return.v_data[i].index].pk = v_pk_list;

						}
						else {

							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data[i].v_message  + '<br/><br/>';

							document.getElementById('bt_saveEditData').style.visibility = 'visible';
						}
					}
					else if (p_return.v_data[i].mode==1) {
						if (!p_return.v_data[i].error) {

							v_editDataObject.infoRows[p_return.v_data[i].index].mode = 0;
							v_editDataObject.infoRows[p_return.v_data[i].index].old_mode = -1;
							v_editDataObject.infoRows[p_return.v_data[i].index].changed_cols = [];

							//Creating pk
							var v_pk_list = [];

							for (var j = 0; j < v_editDataObject.pk.length; j++) {
								
								var v_pk = { v_column: v_editDataObject.pk[j].v_column,
											 v_value : v_editDataObject.ht.getDataAtCell(p_return.v_data[i].index, v_editDataObject.pk[j].v_index + 1)
										   };
							    v_pk_list.push(v_pk);
							}

							v_editDataObject.infoRows[p_return.v_data[i].index].pk = v_pk_list;


						}
						else {

							v_has_error = true;

							v_commands_log += '<b>Command:</b> ' + p_return.v_data[i].v_command + '<br/><br/><b>Message:</b> ' + p_return.v_data[i].v_message  + '<br/><br/>';

							document.getElementById('bt_saveEditData').style.visibility = 'visible';
						}
					}

				}

				if (v_has_error) {
					v_div_commands_log.innerHTML = v_commands_log;
					$('#div_commands_log').show();

				}

				v_editDataObject.ht.render();


			},
			null,
			'box');

}

/// <summary>
/// Changes table name.
/// </summary>
function changeTableName() {
	
	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';
	document.getElementById('txt_tableNameAlterTable').style.backgroundColor = 'rgb(206, 255, 209)';

}

/// <summary>
/// Queries edit data window.
/// </summary>
function queryEditData() {

	var input = JSON.stringify({"p_table" : v_editDataObject.table, "p_filter" : v_editDataObject.editor.getValue(), "p_count": document.getElementById('sel_filtered_data').value, "p_pk_list" : v_editDataObject.pk, "p_columns" : v_editDataObject.columns});

	document.getElementById('bt_saveEditData').style.visibility = 'hidden';

	execAjax('MainDB.aspx/QueryEditData',
			input,
			function(p_return) {

				if (v_editDataObject.pk.length==0) {
					if (v_editDataObject.firstRender)
						showAlert('Table has no primary key, existing rows will be read only.');

					v_editDataObject.firstRender = false;
					v_editDataObject.hasPK = false;
				}
				else
					v_editDataObject.hasPK = true;

				document.getElementById('div_edit_data_query_info').innerHTML = p_return.v_data.v_query_info;

				var columnProperties = [];

				var col = new Object();
				col.title = ' ';
				col.width = 28;
				columnProperties.push(col);

				for (var i = 0; i < v_editDataObject.columns.length; i++) {
				    var col = new Object();

				    if (!v_editDataObject.columns[i].v_is_pk)
				    	col.title =  '<b>' + v_editDataObject.columns[i].v_column + '</b> (' + v_editDataObject.columns[i].v_type + ')';
				    else
				    	col.title = '<img src="images/key.png" style="vertical-align: middle;"/> <b>' + v_editDataObject.columns[i].v_column + '</b> (' + v_editDataObject.columns[i].v_type + ')';

				    col.renderer = 'text';
					columnProperties.push(col);

				}

				var v_infoRows = [];

                for (var i=0; i < p_return.v_data.v_data.length; i++) {
                	var v_object = new Object();
                	v_object.mode = 0;
                	v_object.old_mode = -1;
                	v_object.index = i;
                	v_object.changed_cols = [];
                	v_object.pk = p_return.v_data.v_row_pk[i];
                	v_infoRows.push(v_object);
                }

				var v_div_result = document.getElementById('div_edit_data_data');

				if (v_div_result.innerHTML!='') {

					v_editDataObject.ht.destroy();
				}

				v_editDataObject.infoRows = v_infoRows;

				var container = v_div_result;
				v_editDataObject.ht = new Handsontable(container,
				{
					columns : columnProperties,
					data : p_return.v_data.v_data,
					colHeaders : true,
					rowHeaders : true,
					manualColumnResize: true,
					minSpareRows: 1,
					contextMenu: {
				      callback: function (key, options) {
				        if (key === 'edit_data') {
				          if (v_editDataObject.hasPK)
				          	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),true);
				          else
				          	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),false);
				        }
				      },
				      items: {
				        "edit_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">Edit Content</div>'}
				      }
				    },
					beforeChange: function (changes, source) {
                        if (!changes) {
                            return;
                        }

                        $.each(changes, function (index, element) {
                            var change = element;
                            var rowIndex = change[0];
                            var columnIndex = change[1];
                            var oldValue = change[2];
                            var newValue = change[3];

                            if (rowIndex >= v_editDataObject.infoRows.length)
                            {
                            	var v_object = new Object();
					        	v_object.mode = 2;
					        	v_object.old_mode = -1;
					        	v_object.changed_cols = [];
					        	v_object.index = v_editDataObject.infoRows.length;
					        	v_object.pk = null;

								v_editDataObject.infoRows.push(v_object);

								document.getElementById('bt_saveEditData').style.visibility = 'visible';

                            }

                            if(oldValue != newValue && v_editDataObject.infoRows[rowIndex].mode!=2){

                            	var v_found = false;

                            	if (v_editDataObject.infoRows[rowIndex].changed_cols.indexOf(columnIndex-1)==-1) {
                        			v_editDataObject.infoRows[rowIndex].changed_cols.push(columnIndex-1);
                        		}


                            	if (v_editDataObject.infoRows[rowIndex].mode!=-1) {
                            		v_editDataObject.infoRows[rowIndex].mode = 1;

                            	}
                            	else
                            		v_editDataObject.infoRows[rowIndex].old_mode = 1;

                                document.getElementById('bt_saveEditData').style.visibility = 'visible';

                            }
                        });
                    },
                    cells: function (row, col, prop) {

                    	var cellProperties = {};


					    if (v_editDataObject.infoRows[row]!=null) {

					    	if (!v_editDataObject.hasPK && v_editDataObject.infoRows[row].mode!=2) {
					    		if (col==0)
					    			cellProperties.renderer = grayEmptyRenderer;
					    		else
					    			cellProperties.renderer = grayRenderer;
    							cellProperties.readOnly = true;
					    	}
					    	else if (col==0) {
					    		cellProperties.renderer = editDataActionRenderer;
    							cellProperties.readOnly = true;
							}
    						else if (v_editDataObject.infoRows[row].mode==2) {
    							cellProperties.renderer = greenRenderer;
    						}
    						else if (v_editDataObject.infoRows[row].mode==-1) {
    							cellProperties.renderer = redRenderer;
    						}
    						else if (v_editDataObject.infoRows[row].mode==1) {
    							cellProperties.renderer = yellowRenderer;
    						}
    						else {
    							if (row % 2 == 0) {
    								cellProperties.renderer = blueRenderer;
    							}
    							else {
    								cellProperties.renderer = whiteRenderer;
    							}
    						}

						}
						else {
							if (col==0) {
					    		cellProperties.renderer = newRowRenderer;
    							cellProperties.readOnly = true;
							}
						}

					    return cellProperties;

					}
				});

			},
			null,
			'box');

}

/// <summary>
/// Displays edit cell window.
/// </summary>
/// <param name="p_ht">Handsontable object.</param>
/// <param name="p_row">Row number.</param>
/// <param name="p_col">Column number.</param>
/// <param name="p_content">Cell content.</param>
/// <param name="p_can_alter">If ready only or not.</param>
function editCellData(p_ht, p_row, p_col, p_content, p_can_alter) {

	v_canEditContent = p_can_alter;

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

    var command = {
		name: "replace",
		bindKey: {
		      mac: v_keybind_object.v_replace_mac,
		      win: v_keybind_object.v_replace
		    },
		exec: function(){
			v_copyPasteObject.v_tabControl.selectTabIndex(0);
			showFindReplace(v_editor);
		}
	}

	v_editor.commands.addCommand(command);

	if (p_content!=null)
		v_editor.setValue(p_content);
	else
		v_editor.setValue('');

	v_editor.clearSelection();

	if (p_can_alter)
		v_editor.setReadOnly(false);
	else
		v_editor.setReadOnly(true);

	v_editContentObject = new Object();
	v_editContentObject.editor = v_editor;
	v_editContentObject.row = p_row;
	v_editContentObject.col = p_col;
	v_editContentObject.ht = p_ht;

	$('#div_edit_content').show();

}

/// <summary>
/// Hides edit cell window.
/// </summary>
function hideEditContent() {
	
	$('#div_edit_content').hide();

	if (v_canEditContent)
		v_editContentObject.ht.setDataAtCell(v_editContentObject.row, v_editContentObject.col, v_editContentObject.editor.getValue());

	v_editContentObject.editor.setValue('');

}

/// <summary>
/// Hides command history window.
/// </summary>
function hideCommandList() {
	
	$('#div_command_list').hide();

	v_commandListObject.ht.destroy();

	document.getElementById('div_command_list_data').innerHTML = '';

}

/// <summary>
/// Wipes command history.
/// </summary>
function deleteCommandList() {

	showConfirm('Are you sure you want to clear command history?',
				function() {

					execAjax('MainDB.aspx/ClearCommandList',
					null,
					function(p_return) {

						hideCommandList();

					});

				});

}

/// <summary>
/// Retrieves and displays command history.
/// </summary>
function showCommandList() {

	execAjax('MainDB.aspx/GetCommandList',
			null,
			function(p_return) {

				$('#div_command_list').show();

				var v_height  = $(window).height() - $('#div_command_list_data').offset().top - 120;
				document.getElementById('div_command_list_data').style.height = v_height + "px";

				var columnProperties = [];

				var col = new Object();
				col.title =  'Date';
				col.readOnly = true;
				col.width = 200;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Command';
				col.readOnly = true;
				col.width = 400;
				columnProperties.push(col);

				var v_div_result = document.getElementById('div_command_list_data');

				if (v_div_result.innerHTML!='')
					v_commandListObject.ht.destroy();

				v_commandListObject = new Object();

				var container = v_div_result;
				v_commandListObject.ht = new Handsontable(container,
														{
															data: p_return.v_data,
															columns : columnProperties,
															colHeaders : true,
															rowHeaders : true,
															copyRowsLimit : 1000000000,
															copyColsLimit : 1000000000,
															manualColumnResize: true,
															contextMenu: {
																callback: function (key, options) {

																	if (key === 'view_data') {
																	  	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),false);
																	}

																},
																items: {
																	"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
																}
														    },
														    cells: function (row, col, prop) {

															    var cellProperties = {};
															    if (row % 2 == 0)
																	cellProperties.renderer = blueRenderer;
															    return cellProperties;

															}
														});

			},
			null,
			'box');

}

/// <summary>
/// Initiates edit data window.
/// </summary>
/// <param name="p_table">Table name.</param>
function startEditData(p_table) {

	var input = JSON.stringify({"p_table" : p_table});

	execAjax('MainDB.aspx/StartEditData',
			input,
			function(p_return) {

				$('#div_edit_data').show();

				var v_height  = $(window).height() - $('#div_edit_data_data').offset().top - 80;
				document.getElementById('div_edit_data_data').style.height = v_height + "px";

				document.getElementById('div_edit_data_select').innerHTML = 'select * from ' + p_table + ' t';

				if (v_editDataObject!=null)
				if (v_editDataObject.editor!=null) {
					 v_editDataObject.editor.destroy();
					 document.getElementById('txt_filter_data').innerHTML = '';
				}

				var langTools = ace.require("ace/ext/language_tools");
				var v_editor = ace.edit('txt_filter_data');
				v_editor.setTheme("ace/theme/" + v_editor_theme);
				v_editor.session.setMode("ace/mode/sql");
				v_editor.commands.bindKey(".", "startAutocomplete");

				v_editor.setFontSize(Number(v_editor_font_size));

				document.getElementById('txt_filter_data').onclick = function() {
			  		v_editor.focus();
			    };

				var command = {
			         name: "save",
			         bindKey: {
			                  mac: v_keybind_object.v_execute_mac,
			                  win: v_keybind_object.v_execute
			                },
			         exec: function(){
			           queryEditData();
			         }
			      }

			    v_editor.commands.addCommand(command);

			    var command = {
					name: "replace",
					bindKey: {
					      mac: v_keybind_object.v_replace_mac,
					      win: v_keybind_object.v_replace
					    },
					exec: function(){
						v_copyPasteObject.v_tabControl.selectTabIndex(0);
						showFindReplace(v_editor);
					}
				}

				v_editor.commands.addCommand(command);

				var qtags = {
					getCompletions: function(editor, session, pos, prefix, callback) {

						if (v_completer_ready) {

						  	var wordlist = [];

						  	v_completer_ready = false;
						  	setTimeout(function(){ v_completer_ready = true; }, 1000);

						  	if (prefix!='') {

								execAjax('MainDB.aspx/GetCompletionsTable',
								JSON.stringify({ p_table: p_table}),
								function(p_return) {

									if (p_return.v_data.length==0)
										editor.insert('.');

									wordlist = p_return.v_data;
									callback(null, wordlist);

								},
								null,
								'box',
								false);

							}

						}

					}
				}

				langTools.setCompleters([qtags]);
				v_editor.setOptions({enableBasicAutocompletion: true});

				v_editor.setValue(p_return.v_data.v_ini_orderby);
				v_editor.clearSelection();

				v_editDataObject = new Object();
				v_editDataObject.editor = v_editor;
				v_editDataObject.table = p_table;
				v_editDataObject.firstRender = true;
				v_editDataObject.pk = p_return.v_data.v_pk;
				v_editDataObject.columns = p_return.v_data.v_cols;

				queryEditData();

			});

}

/// <summary>
/// Initiates alter table window.
/// </summary>
/// <param name="p_mode">Alter or new table.</param>
/// <param name="p_table">Table name.</param>
function startAlterTable(p_mode,p_table) {

	v_alterTabControl.selectTabIndex(0);

	document.getElementById('txt_tableNameAlterTable').value = p_table;
	document.getElementById('txt_tableNameAlterTable').style.backgroundColor = 'white';

	var input = JSON.stringify({"p_table": p_table});

	execAjax('MainDB.aspx/AlterTableData',
				input,
				function(p_return) {

					if (!p_return.v_data.v_can_add_constraint && p_mode=='alter')
						$('#bt_newConstraintAlterTable').hide();
					else
						$('#bt_newConstraintAlterTable').show();

					if (!p_return.v_data.v_can_rename_table && p_mode=='alter') {
						$('#txt_tableNameAlterTable').prop("readonly", true);
						document.getElementById('txt_tableNameAlterTable').style.backgroundColor = 'rgb(242, 242, 242)';

					}
					else {
						$('#txt_tableNameAlterTable').prop("readonly", false);
						$('#txt_tableNameAlterTable').removeClass("txt_readonly");
					}

					$('#div_alter_table').show();

					var v_height  = $(window).height() - $('#div_alter_table_data').offset().top - 120;
					document.getElementById('div_alter_table_data').style.height = v_height + "px";
					document.getElementById('div_alter_constraint_data').style.height = v_height + "px";

					//Columns Table
					var v_div_result = document.getElementById('div_alter_table_data');

					var columnProperties = [];

					var col = new Object();
      				col.title =  'Column Name';
      				col.width = '100px';
     	 			columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  'Data Type';
      				col.width = '160px';
      				col.type = 'autocomplete';
	                col.source = p_return.v_data.v_data_types;
     	 			columnProperties.push(col);

					var col = new Object();
	                col.title =  'Nullable';
	                col.width = '80px';
	                col.type = 'dropdown';
	                col.source = ['YES','NO'];
	                columnProperties.push(col);

	                var col = new Object();
      				col.title =  ' ';
      				col.renderer = 'html';
     	 			columnProperties.push(col);


	                var v_infoRowsColumns = [];

	                for (var i=0; i < p_return.v_data.v_data_columns.length; i++) {
	                	var v_object = new Object();
	                	v_object.mode = 0;
	                	v_object.old_mode = -1;
	                	v_object.index = i;
	                	v_object.originalColName = p_return.v_data.v_data_columns[i][0];
	                	v_object.originalDataType = p_return.v_data.v_data_columns[i][1];
	                	v_object.originalNullable = p_return.v_data.v_data_columns[i][2];
	                	v_infoRowsColumns.push(v_object);
	                }



					if (document.getElementById('div_alter_table_data').innerHTML!='') {

						v_alterTableObject.ht.destroy();

					}

					if (document.getElementById('div_alter_constraint_data').innerHTML!='') {

						v_alterTableObject.ht_constraints.destroy();

					}

					if (document.getElementById('div_alter_index_data').innerHTML!='') {

						v_alterTableObject.ht_indexes.destroy();

					}

					var container = v_div_result;

					v_alterTableObject = new Object();

					v_alterTableObject.tableName = p_table;
					v_alterTableObject.infoRowsColumns = v_infoRowsColumns;
					v_alterTableObject.cellChanges = [];
					v_alterTableObject.mode = p_mode;
					v_alterTableObject.window = 'columns';
					v_alterTableObject.canAlterType = p_return.v_data.v_can_alter_type;
                	v_alterTableObject.canAlterNullable = p_return.v_data.v_can_alter_nullable;
                	v_alterTableObject.canRenameColumn = p_return.v_data.v_can_rename_column;
                	v_alterTableObject.hasUpdateRule = p_return.v_data.v_has_update_rule;
					v_alterTableObject.ht_constraints = null;
					v_alterTableObject.fkRefColumns = p_return.v_data.table_ref_columns;
					v_alterTableObject.can_drop_column = p_return.v_data.v_can_drop_column;


					v_alterTableObject.ht = new Handsontable(container,
					{
						data: p_return.v_data.v_data_columns,
						columns : columnProperties,
						colHeaders : true,
						rowHeaders : true,
						manualColumnResize: true,
						minSpareRows: 1,
						beforeChange: function (changes, source) {

	                        if (!changes) {
	                            return;
	                        }

	                        $.each(changes, function (index, element) {
	                            var change = element;
	                            var rowIndex = change[0];
	                            var columnIndex = change[1];
	                            var oldValue = change[2];
	                            var newValue = change[3];

	                            if (rowIndex >= v_alterTableObject.infoRowsColumns.length)
	                            {
	                            	var v_object = new Object();
						        	v_object.mode = 2;
						        	v_object.old_mode = 2;
						        	v_object.originalColName = '';
						        	v_object.originalDataType = '';
						        	v_object.index = v_alterTableObject.infoRowsColumns.length;
						        	v_object.nullable = '';

									v_alterTableObject.infoRowsColumns.push(v_object);

									document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

	                            }

	                            if(oldValue != newValue && v_alterTableObject.infoRowsColumns[rowIndex].mode!=2) {

	                            	if (v_alterTableObject.infoRowsColumns[rowIndex].mode!=-1)
	                            		v_alterTableObject.infoRowsColumns[rowIndex].mode = 1;
	                            	else
	                            		v_alterTableObject.infoRowsColumns[rowIndex].old_mode = 1;

	                                document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

	                            }
	                        });

	                    },
	                    cells: function (row, col, prop) {

						    var cellProperties = {};

						    if (v_alterTableObject.infoRowsColumns[row]!=null) {

						    	if (col==3) {
						    		if (v_alterTableObject.can_drop_column || v_alterTableObject.infoRowsColumns[row].mode==2)
						    			cellProperties.renderer = columnsActionRenderer;
						    		else
						    			cellProperties.renderer = grayEmptyRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_alterTableObject.infoRowsColumns[row].mode==2) {
	    							cellProperties.renderer = greenHtmlRenderer;
	    						}
	    						else if (v_alterTableObject.infoRowsColumns[row].mode==-1) {
	    							cellProperties.renderer = redHtmlRenderer;
	    						}
	    						else if (v_alterTableObject.infoRowsColumns[row].mode== 1) {
	    							cellProperties.renderer = yellowHtmlRenderer;
	    						}
	    						else if ((!v_alterTableObject.canAlterType && col==1) || (!v_alterTableObject.canAlterNullable && col==2) || (!v_alterTableObject.canRenameColumn && col==0)) {
	    							cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
	    						}
	    						else {
	    							if (row % 2 == 0)
	    								cellProperties.renderer = blueHtmlRenderer;
	    							else
	    								cellProperties.renderer = whiteHtmlRenderer;
	    						}

    						}
    						else {
    							if (col==3) {
						    		cellProperties.renderer = grayEmptyRenderer;
	    							cellProperties.readOnly = true;
								}
    						}

						    return cellProperties;

						}
					});

					//Constraints Table
					var v_div_result = document.getElementById('div_alter_constraint_data');

					var columnProperties = [];

					var col = new Object();
      				col.title =  'Constraint Name';
      				col.width = '100px';
     	 			columnProperties.push(col);

					var col = new Object();
	                col.title =  'Type';
	                col.width = '100px';
	                col.type = 'dropdown';
	                col.source = ['Primary Key','Foreign Key','Unique'];
	                columnProperties.push(col);

	                var col = new Object();
      				col.title =  'Columns';
      				col.width = '160px';
     	 			columnProperties.push(col);

     	 			var col = new Object();
	                col.title =  'Referenced Table';
	                col.width = '160px';
	                col.type = 'autocomplete';
	                col.source = p_return.v_data.v_tables;
	                columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  'Referenced Columns';
      				col.width = '240px';
      				col.type = 'autocomplete';
     	 			columnProperties.push(col);

     	 			var col = new Object();
	                col.title =  'Delete Rule';
	                col.width = '160px';
	                col.type = 'autocomplete';
	                col.source = p_return.v_data.v_delete_rules;
	                columnProperties.push(col);

	                var col = new Object();
	                col.title =  'Update Rule';
	                col.width = '160px';
	                col.type = 'autocomplete';
	                col.source = p_return.v_data.v_update_rules;
	                columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  ' ';
      				col.renderer = 'html';
     	 			columnProperties.push(col);

     	 			var v_infoRowsConstraints = [];

	                for (var i=0; i < p_return.v_data.v_data_constraints.length; i++) {
	                	var v_object = new Object();
	                	v_object.mode = 0;
	                	v_object.old_mode = -1;
	                	v_object.index = i;
	                	v_infoRowsConstraints.push(v_object);
	                }

	                v_alterTableObject.infoRowsConstraints = v_infoRowsConstraints;
	                v_alterTableObject.canAlterConstraints = false;


					var container = v_div_result;


					v_alterTableObject.ht_constraints = new Handsontable(container,
					{
						data: p_return.v_data.v_data_constraints,
						columns : columnProperties,
						colHeaders : true,
						manualColumnResize: true,
						beforeChange: function (changes, source) {

	                        if (!changes) {
	                            return;
	                        }
	                        $.each(changes, function (index, element) {
	                            var change = element;
	                            var rowIndex = change[0];
	                            var columnIndex = change[1];
	                            var oldValue = change[2];
	                            var newValue = change[3];

	                            if(oldValue != newValue){

	                            	if (columnIndex == 3) {
	                            		getReferenceColumnsList(rowIndex,newValue);
	                            	}

	                            	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';
	                            }
	                        });

	                    },
						cells: function (row, col, prop) {

						    var cellProperties = {};

						    if (v_alterTableObject.infoRowsConstraints[row]!=null) {

					    		var v_constraint_type = p_return.v_data.v_data_constraints[row][1];

						    	if (col==7 || (!v_alterTableObject.hasUpdateRule && col==6)) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_alterTableObject.infoRowsConstraints[row].mode==-1) {
	    							cellProperties.renderer = redHtmlRenderer;
	    						}
								else if ( (v_constraint_type!='Primary Key' && v_constraint_type!='Foreign Key' && v_constraint_type!='Unique') && (col==2) ) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if ( (v_constraint_type!='Foreign Key') && (col==3 || col==4 || col==5 || col==6) ) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_alterTableObject.infoRowsConstraints[row].mode==2) {
	    							cellProperties.renderer = greenHtmlRenderer;
	    							cellProperties.readOnly = false;
	    						}
	    						else if (!v_alterTableObject.canAlterConstraints) {
	    							cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
	    						}
	    						else {
	    							if (row % 2 == 0)
	    								cellProperties.renderer = blueHtmlRenderer;
	    							else
	    								cellProperties.renderer = whiteHtmlRenderer;
	    						}

	    						if (col==2)
						    		cellProperties.readOnly = true;

	    						if (col==4) {
							    	if (p_return.v_data.v_data_constraints[row][1]=='Foreign Key') {

							    		cellProperties.type='dropdown';
							    		cellProperties.source = v_alterTableObject.fkRefColumns[row];

							    	}
						    	}

    						}

						    return cellProperties;

						}

					});

					//Indexes Table
					var v_div_result = document.getElementById('div_alter_index_data');

					var columnProperties = [];

					var col = new Object();
      				col.title =  'Index Name';
      				col.width = '100px';
     	 			columnProperties.push(col);

					var col = new Object();
	                col.title =  'Type';
	                col.width = '100px';
	                col.type = 'dropdown';
	                col.source = ['Non Unique','Unique'];
	                columnProperties.push(col);

	                var col = new Object();
      				col.title =  'Columns';
      				col.width = '160px';
     	 			columnProperties.push(col);

     	 			var col = new Object();
      				col.title =  ' ';
      				col.renderer = 'html';
     	 			columnProperties.push(col);

     	 			var v_infoRowsIndexes = [];

	                for (var i=0; i < p_return.v_data.v_data_indexes.length; i++) {
	                	var v_object = new Object();
	                	v_object.mode = 0;
	                	v_object.old_mode = -1;
	                	v_object.index = i;
	                	v_infoRowsIndexes.push(v_object);
	                }

	                v_alterTableObject.infoRowsIndexes = v_infoRowsIndexes;
	                v_alterTableObject.canAlterIndexes = false;


					var container = v_div_result;

					v_alterTableObject.ht_indexes = new Handsontable(container,
					{
						data: p_return.v_data.v_data_indexes,
						columns : columnProperties,
						colHeaders : true,
						manualColumnResize: true,
						beforeChange: function (changes, source) {

	                        if (!changes) {
	                            return;
	                        }
	                        $.each(changes, function (index, element) {
	                            var change = element;
	                            var rowIndex = change[0];
	                            var columnIndex = change[1];
	                            var oldValue = change[2];
	                            var newValue = change[3];

	                            if(oldValue != newValue){

	                            	if (columnIndex == 3) {
	                            		getReferenceColumnsList(rowIndex,newValue);
	                            	}

	                            	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';
	                            }
	                        });

	                    },
						cells: function (row, col, prop) {

						    var cellProperties = {};

						    if (v_alterTableObject.infoRowsIndexes[row]!=null) {

						    	if (col==3) {
						    		cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
								}
								else if (v_alterTableObject.infoRowsIndexes[row].mode==-1) {
	    							cellProperties.renderer = redHtmlRenderer;
	    						}
								else if (v_alterTableObject.infoRowsIndexes[row].mode==2) {
	    							cellProperties.renderer = greenHtmlRenderer;
	    							cellProperties.readOnly = false;
	    						}
	    						else if (!v_alterTableObject.canAlterIndexes) {
	    							cellProperties.renderer = grayHtmlRenderer;
	    							cellProperties.readOnly = true;
	    						}
	    						else {
	    							if (row % 2 == 0)
	    								cellProperties.renderer = blueHtmlRenderer;
	    							else
	    								cellProperties.renderer = whiteHtmlRenderer;
	    						}

	    						if (col==2)
						    		cellProperties.readOnly = true;


    						}

						    return cellProperties;
						}

					});


				},
				null,
				'box');

}

/// <summary>
/// Retrieves list of pks and uniques referenced by FKs in specific table.
/// </summary>
/// <param name="p_row_index">Row number of current FK.</param>
/// <param name="p_table_name">Table name.</param>
function getReferenceColumnsList(p_row_index, p_table_name) {

	var input = JSON.stringify({"p_table_name": p_table_name});

	execAjax('MainDB.aspx/RefreshRefColumnsList',
				input,
				function(p_return) {
					
					v_alterTableObject.fkRefColumns[p_row_index] = p_return.v_data;
					v_alterTableObject.ht_constraints.render();

				},
				null,
				'box');

}

/// <summary>
/// Displays message to drop table.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropTable(p_node) {

	showConfirm('Are you sure you want to drop the table ' + p_node.text + '?',
				function() {

					dropTableConfirm(p_node);

				});

}

/// <summary>
/// Displays message to delete table records.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function deleteData(p_node) {

	showConfirm('Are you sure you want to delete all records from table ' + p_node.text + '?',
				function() {

					deleteDataConfirm(p_node);

				});

}

/// <summary>
/// Drops table.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function dropTableConfirm(p_node) {

	p_node.tag.num_tables = 0;

	var input = JSON.stringify({"p_table": p_node.text});

	execAjax('MainDB.aspx/DropTable',
				input,
				function(p_return) {

					p_node.removeNode();

					p_node.parent.tag.num_tables = p_node.parent.tag.num_tables-1;
					p_node.parent.setText('Tables (' + p_node.parent.tag.num_tables + ')');

					showAlert('Table dropped.');

				},
				null,
				'box');

}

/// <summary>
/// Deletes table records.
/// </summary>
/// <param name="p_node">Tree node object.</param>
function deleteDataConfirm(p_node) {

	p_node.tag.num_tables = 0;

	var input = JSON.stringify({"p_table": p_node.text});

	execAjax('MainDB.aspx/DeleteData',
				input,
				function(p_return) {

					showAlert('Records deleted.');

				},
				null,
				'box');

}

/// <summary>
/// Triggered when X is pressed in specific record at the edit table data window.
/// </summary>
function deleteRowEditData() {

	var v_data = v_editDataObject.ht.getData();
	var v_row = v_editDataObject.ht.getSelected()[0];

	if (v_editDataObject.infoRows[v_row].mode==2) {

		v_editDataObject.infoRows.splice(v_row,1);
		v_data.splice(v_row,1);
		v_editDataObject.ht.loadData(v_data);


	}
	else {

		var v_mode = v_editDataObject.infoRows[v_row].mode;
		v_editDataObject.infoRows[v_row].mode = v_editDataObject.infoRows[v_row].old_mode;
		v_editDataObject.infoRows[v_row].old_mode = v_mode;
		v_editDataObject.ht.render();

	}

	document.getElementById('bt_saveEditData').style.visibility = 'visible';

}

/// <summary>
/// Triggered when X is pressed in specific column at the alter table window.
/// </summary>
function dropColumnAlterTable() {

	var v_data = v_alterTableObject.ht.getData();
	var v_row = v_alterTableObject.ht.getSelected()[0];

	if (v_alterTableObject.infoRowsColumns[v_row].mode==2) {

		v_alterTableObject.infoRowsColumns.splice(v_row,1);
		v_data.splice(v_row,1);

		v_alterTableObject.ht.loadData(v_data);

	}
	else {

		var v_mode = v_alterTableObject.infoRowsColumns[v_row].mode;
		v_alterTableObject.infoRowsColumns[v_row].mode = v_alterTableObject.infoRowsColumns[v_row].old_mode;
		v_alterTableObject.infoRowsColumns[v_row].old_mode = v_mode;

		v_alterTableObject.ht.loadData(v_data);

	}

	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

}

/// <summary>
/// Triggered when X is pressed in specific constraint at the alter table window.
/// </summary>
function dropConstraintAlterTable() {

	var v_data = v_alterTableObject.ht_constraints.getData();
	var v_row = v_alterTableObject.ht_constraints.getSelected()[0];

	if (v_alterTableObject.infoRowsConstraints[v_row].mode==2) {

		v_alterTableObject.infoRowsConstraints.splice(v_row,1);
		v_data.splice(v_row,1);

		v_alterTableObject.ht_constraints.loadData(v_data);

	}
	else {

		var v_mode = v_alterTableObject.infoRowsConstraints[v_row].mode;
		v_alterTableObject.infoRowsConstraints[v_row].mode = v_alterTableObject.infoRowsConstraints[v_row].old_mode;
		v_alterTableObject.infoRowsConstraints[v_row].old_mode = v_mode;

		v_alterTableObject.ht_constraints.loadData(v_data);

	}

	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

}

/// <summary>
/// Triggered when X is pressed in specific index at the alter table window.
/// </summary>
function dropIndexAlterTable() {

	var v_data = v_alterTableObject.ht_indexes.getData();
	var v_row = v_alterTableObject.ht_indexes.getSelected()[0];

	if (v_alterTableObject.infoRowsIndexes[v_row].mode==2) {

		v_alterTableObject.infoRowsIndexes.splice(v_row,1);
		v_data.splice(v_row,1);

		v_alterTableObject.ht_indexes.loadData(v_data);

	}
	else {

		var v_mode = v_alterTableObject.infoRowsIndexes[v_row].mode;
		v_alterTableObject.infoRowsIndexes[v_row].mode = v_alterTableObject.infoRowsIndexes[v_row].old_mode;
		v_alterTableObject.infoRowsIndexes[v_row].old_mode = v_mode;

		v_alterTableObject.ht_indexes.loadData(v_data);

	}

	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

}

/// <summary>
/// Adds new column at the alter table window.
/// </summary>
function newColumnAlterTable() {

	var v_data = v_alterTableObject.ht.getData();

	var v_object = new Object();
	v_object.canAlterType = true;
	v_object.canAlterNullable = true;
	v_object.canRenameColumn = true;
	v_object.mode = 2;
	v_object.originalColName = '';
	v_object.originalDataType = '';
	v_object.nullable = '';

	v_alterTableObject.infoRowsColumns.push(v_object);

	v_data.push(['','','YES','<img src="images/tab_close.png" onclick="dropColumnAlterTable()"/>']);

	v_alterTableObject.ht.loadData(v_data);

	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

}

/// <summary>
/// Adds new index at the alter table window.
/// </summary>
function newIndexAlterTable() {

	var v_data = v_alterTableObject.ht_indexes.getData();

	var v_object = new Object();
	v_object.mode = 2;
	v_object.old_mode = 2;
	v_object.index = v_alterTableObject.infoRowsIndexes.length;


	v_alterTableObject.infoRowsIndexes.push(v_object);

	v_data.push(['','',"<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> ",'<img src="images/tab_close.png" onclick="dropIndexAlterTable()"/>']);

	v_alterTableObject.ht_indexes.loadData(v_data);

	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

}

/// <summary>
/// Adds new constraint at the alter table window.
/// </summary>
function newConstraintAlterTable() {

	var v_data = v_alterTableObject.ht_constraints.getData();

	var v_object = new Object();
	v_object.mode = 2;
	v_object.old_mode = 2;
	v_object.index = v_alterTableObject.infoRowsConstraints.length;


	v_alterTableObject.infoRowsConstraints.push(v_object);

	v_data.push(['','',"<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> ",'','','','','<img src="images/tab_close.png" onclick="dropConstraintAlterTable()"/>']);

	v_alterTableObject.ht_constraints.loadData(v_data);

	document.getElementById('bt_saveAlterTable').style.visibility = 'visible';

}

/// <summary>
/// Adds column to right list at columns list window.
/// </summary>
function addColumnToList() {

	var v_select_left = document.getElementById("sel_columns_left");

	var v_select_right = document.getElementById("sel_columns_right");
	var option = document.createElement("option");
	option.text = v_select_left.options[v_select_left.selectedIndex].text;
	v_select_right.add(option);

	v_select_left.remove(v_select_left.selectedIndex);

}

/// <summary>
/// Adds column to left list at columns list window.
/// </summary>
function remColumnFromList() {

	var v_select_right = document.getElementById("sel_columns_right");

	var v_select_left = document.getElementById("sel_columns_left");
	var option = document.createElement("option");
	option.text = v_select_right.options[v_select_right.selectedIndex].text;
	v_select_left.add(option);

	v_select_right.remove(v_select_right.selectedIndex);

}

/// <summary>
/// Hides command history window.
/// </summary>
function hideCommandsLog() {

	$('#div_commands_log').hide();

}

/// <summary>
/// Hides column list window.
/// </summary>
function hideColumnSelection() {

	var v_select_right = document.getElementById('sel_columns_right');

	var v_first = true;
	var v_column_string = '';

	for (var i=0; i < v_select_right.options.length; i++) {
		if (!v_first)
			v_column_string += ', ';

		v_first = false;
		v_column_string += v_select_right.options[i].text;

	}

	if (v_alterTableObject.window=='constraints') {
		v_column_string = "<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionConstraints()'/> " + v_column_string;
		v_alterTableObject.ht_constraints.setDataAtCell(v_alterTableObject.selectedConstraintRow, 2, v_column_string);
	}
	else {
		v_column_string = "<img src='images/edit_columns.png' class='img_ht' onclick='showColumnSelectionIndexes()'/> " + v_column_string;
		v_alterTableObject.ht_indexes.setDataAtCell(v_alterTableObject.selectedIndexRow, 2, v_column_string);
	}
	$('#div_column_selection').hide();

}

/// <summary>
/// Displays columns list window for constraints.
/// </summary>
function showColumnSelectionConstraints() {

	$("#sel_columns_left").empty();
	$("#sel_columns_right").empty();

	var v_select_left = document.getElementById('sel_columns_left');
	var v_select_right = document.getElementById('sel_columns_right');

	var v_selected = v_alterTableObject.ht_constraints.getSelected();

	if (v_alterTableObject.infoRowsConstraints[v_selected[0]].mode==2) {

		v_alterTableObject.selectedConstraintRow = v_selected[0];

		var v_type = v_alterTableObject.ht_constraints.getDataAtCell(v_selected[0],1);

		if (v_type=='Primary Key' || v_type=='Foreign Key' || v_type=='Unique') {

			var v_columns = v_alterTableObject.ht_constraints.getDataAtCell(v_selected[0],v_selected[1]);
			v_columns = v_columns.substring(95);

			var v_constraint_columns_list;

			if (v_columns=='')
				v_constraint_columns_list = [];
			else
				v_constraint_columns_list = v_columns.split(', ')

			for (var i=0; i < v_constraint_columns_list.length; i++) {
				var option = document.createElement("option");
				option.text = v_constraint_columns_list[i];
				v_select_right.add(option);
			}

			var v_table_columns_list = v_alterTableObject.ht.getDataAtCol(0);

			for (var i=0; i < v_table_columns_list.length-1; i++) {
				if (v_constraint_columns_list.indexOf(v_table_columns_list[i])==-1) {
					var option = document.createElement("option");
					option.text = v_table_columns_list[i];
					v_select_left.add(option);
				}
			}

			$('#div_column_selection').show();

		}

	}

}

/// <summary>
/// Displays columns list window for indexes.
/// </summary>
function showColumnSelectionIndexes() {

	$("#sel_columns_left").empty();
	$("#sel_columns_right").empty();

	var v_select_left = document.getElementById('sel_columns_left');
	var v_select_right = document.getElementById('sel_columns_right');

	var v_selected = v_alterTableObject.ht_indexes.getSelected();

	if (v_alterTableObject.infoRowsIndexes[v_selected[0]].mode==2) {

		v_alterTableObject.selectedIndexRow = v_selected[0];

		var v_type = v_alterTableObject.ht_indexes.getDataAtCell(v_selected[0],1);


		var v_columns = v_alterTableObject.ht_indexes.getDataAtCell(v_selected[0],v_selected[1]);
		v_columns = v_columns.substring(91);

		var v_index_columns_list;

		if (v_columns=='')
			v_index_columns_list = [];
		else
			v_index_columns_list = v_columns.split(', ')

		for (var i=0; i < v_index_columns_list.length; i++) {
			var option = document.createElement("option");
			option.text = v_index_columns_list[i];
			v_select_right.add(option);
		}

		var v_table_columns_list = v_alterTableObject.ht.getDataAtCol(0);

		for (var i=0; i < v_table_columns_list.length-1; i++) {
			if (v_index_columns_list.indexOf(v_table_columns_list[i])==-1) {
				var option = document.createElement("option");
				option.text = v_table_columns_list[i];
				v_select_left.add(option);
			}
		}

		$('#div_column_selection').show();

	}

}