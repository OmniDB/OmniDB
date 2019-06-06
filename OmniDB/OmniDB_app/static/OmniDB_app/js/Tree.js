/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Retrieving tree.
/// </summary>
function getTree(p_div) {

	execAjax('/get_tree_info/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				var context_menu = {
				'cm_database' : {
					elements : [
						{
							text : 'Render Graph',
							icon: '/static/OmniDB_app/images/graph.png',
							action : function(node) {

							},
							submenu: {
								elements : [
									{
										text : 'Simple Graph',
										icon: '/static/OmniDB_app/images/graph.png',
										action : function(node) {
											modalGraph('show',false);
										}
									},
									{
										text : 'Complete Graph',
										icon: '/static/OmniDB_app/images/graph.png',
										action : function(node) {
											modalGraph('show',true);
										}
									}
								]
							}
						},
						{
							text : 'Refresh Tree',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								getTree();
							}
						}
					]
				},
				'cm_tables' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTree(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
						{
							text : 'New Table',
							icon: '/static/OmniDB_app/images/new_table.png',
							action : function(node) {
								//v_firstModeTable = 'new';
								//startAlterTable('new',null);
								v_connTabControl.selectedTab.tag.tabControl.tag.createAlterTableTab("New Table");
								startAlterTable('new',null);
							}
						}
					]
				},
				'cm_functions' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									getFunctions(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				},
				'cm_function' : {
					elements : [
						{
							text : 'Edit Function',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='edit')
									v_connTabControl.selectedTab.tag.tabControl.tag.createQueryTab(node.text);

								getFunctionDefinition(node);
							}
						},
						{
							text : 'Drop Function',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								dropFunction(node);
							}
						},
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTree(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				},
				'cm_procedures' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									getProcedures(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				},
				'cm_procedure' : {
					elements : [
						{
							text : 'Edit Procedure',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='edit')
									v_connTabControl.selectedTab.tag.tabControl.tag.createQueryTab(node.text);

								getProcedureDefinition(node);
							}
						},
						{
							text : 'Drop Procedure',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								dropProcedure(node);
							}
						},
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTree(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				},
				'cm_refresh' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTree(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				},
				'cm_table' : {
					elements : [
						{
							text : 'Data Actions',
							icon: '/static/OmniDB_app/images/list.png',
							submenu: {
							elements: [
								    {
										text : 'Query Data',
										icon: '/static/OmniDB_app/images/query.png',
										action : function(node) {

											var v_table_name = '';
											if (node.parent.parent.parent.parent!=null)
												v_table_name = node.parent.parent.text + '.' + node.text;
											else
												v_table_name = node.text;

											if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode!='query')
												v_connTabControl.selectedTab.tag.tabControl.tag.createQueryTab(node.text);

											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value = 10;

											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue('-- Querying Data\nselect t.*\nfrom ' + v_table_name + ' t');
											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
											renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,node.text);

											//minimizeEditor();

			                				querySQL();
										}
									},
									{
										text : 'Edit Data',
										icon: '/static/OmniDB_app/images/edit_data.png',
										action : function(node) {

											v_connTabControl.selectedTab.tag.tabControl.tag.createEditDataTab(node.text);
											startEditData(node.text);

										}
									},
									{
										text : 'Count Records',
										icon: '/static/OmniDB_app/images/counter.png',
										action : function(node) {

											var v_table_name = '';
											if (node.parent.parent.parent.parent!=null)
												v_table_name = node.parent.parent.text + '.' + node.text;
											else
												v_table_name = node.text;

											if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode!='query')
												v_connTabControl.selectedTab.tag.tabControl.tag.createQueryTab(node.text);

											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue("-- Counting Records\nselect count(*) as count\nfrom " + v_table_name + " t");
											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
											renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,node.text);

			                				querySQL();
										}
									},
									{
										text : 'Delete Records',
										icon: '/static/OmniDB_app/images/tab_close.png',
										action : function(node) {
											deleteData(node);
										}
									}
								]
							}
						},
						{
							text : 'Table Actions',
							icon: '/static/OmniDB_app/images/list.png',
							submenu: {
							elements: [
								    {
										text : 'Alter Table',
										icon: '/static/OmniDB_app/images/table_edit.png',
										action : function(node) {
											//v_firstModeTable = 'alter';
											//startAlterTable('alter',node.text);
											v_connTabControl.selectedTab.tag.tabControl.tag.createAlterTableTab(node.text);
											startAlterTable('alter',node.text);
										}
									},

									{
										text : 'Drop Table',
										icon: '/static/OmniDB_app/images/tab_close.png',
										action : function(node) {
											dropTable(node);
										}
									}
								]
							}
						},
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTree(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				},
				'cm_sequences' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTree(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
						{
							text : 'New Sequence',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								v_connTabControl.selectedTab.tag.tabControl.tag.createSequenceTab('New Sequence');
								startAlterSequence('new',null);
							}
						}
					]
				},
				'cm_sequence' : {
					elements : [
						{
							text : 'Edit Sequence',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								v_connTabControl.selectedTab.tag.tabControl.tag.createSequenceTab(node.text);
								startAlterSequence('alter',node.text);
							}
						},
						{
							text : 'Drop Sequence',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								dropSequence(node);
							}
						}
					]
				}
			};
				tree = createTree(p_div,'#fcfdfd',context_menu);

				tree.nodeAfterOpenEvent = function(node) {
					refreshTree(node);
				}

				node1 = tree.createNode(p_return.v_data.v_database_return.v_database,true,'/static/OmniDB_app/images/db.png',null,null,'cm_database');

				v_tree_object = new Object();

				var node2 = node1;

				if (p_return.v_data.v_database_return.v_has_schema) {

					node2 = tree.createNode(p_return.v_data.v_database_return.v_schema,true,'/static/OmniDB_app/images/schemas.png',node1,null,null);

				}

				var node_tables = tree.createNode('Tables',false,'/static/OmniDB_app/images/table_multiple.png',node2,{ type:'table_list', num_tables : 0 },'cm_tables');
				node_tables.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

				v_tree_object.tables_node = node_tables;

				if (p_return.v_data.v_database_return.v_has_functions) {
					var node_tables = tree.createNode('Functions',false,'/static/OmniDB_app/images/gear.png',node2,{ type:'function_list', num_tables : 0 },'cm_functions');
					node_tables.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
				}

				if (p_return.v_data.v_database_return.v_has_procedures) {
					var node_tables = tree.createNode('Procedures',false,'/static/OmniDB_app/images/gear.png',node2,{ type:'procedure_list', num_tables : 0 },'cm_procedures');
					node_tables.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
				}

				if (p_return.v_data.v_database_return.v_has_sequences) {
					var node_tables = tree.createNode('Sequences',false,'/static/OmniDB_app/images/sequence_list.png',node2,{ type:'sequence_list', num_tables : 0 },'cm_sequences');
					node_tables.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
				}

				v_tree_object.refreshTables = function() {
					refreshTree(v_tree_object.tables_node);
				}


				tree.drawTree('div_tree');
				v_tree_object;


			},
			null,
			'box');

}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTree(node) {
	if (node.tag!=undefined)
		if (node.tag.type=='table_list') {
			getTables(node);
		}
		else if (node.tag.type=='table') {
			getColumns(node);
		}
		else if (node.tag.type=='primary_key') {
			getPK(node);
		}
		else if (node.tag.type=='uniques') {
			getUniques(node);
		}
		else if (node.tag.type=='foreign_keys') {
			getFKs(node);
		}
		else if (node.tag.type=='sequence_list') {
			getSequences(node);
		}
		else if (node.tag.type=='view_list') {
			getViews(node);
		}
		else if (node.tag.type=='view') {
			getViewsColumns(node);
		}
		else if (node.tag.type=='indexes') {
			getIndexes(node);
		}
		else if (node.tag.type=='function_list') {
			getFunctions(node);
		}
		else if (node.tag.type=='function') {
			getFunctionFields(node);
		}
		else if (node.tag.type=='procedure_list') {
			getProcedures(node);
		}
		else if (node.tag.type=='procedure') {
			getProcedureFields(node);
		}
		else if (node.tag.type=='sequence_list') {
			getSequences(node);
		}

}

/// <summary>
/// Retrieving tables.
/// </summary>
/// <param name="node">Node object.</param>
function getTables(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_tables/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Tables (' + p_return.v_data.length + ')');

				node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/table.png',{ type:'table', has_primary_keys: p_return.v_data[i].v_has_primary_keys, has_foreign_keys: p_return.v_data[i].v_has_foreign_keys, has_uniques: p_return.v_data[i].v_has_uniques, has_indexes: p_return.v_data[i].v_has_indexes},'cm_table');
		        	v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',{ type:'table_field'},null);

		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving sequences.
/// </summary>
/// <param name="node">Node object.</param>
function getSequences(node) {
	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_sequences/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				node.setText('Sequences (' + p_return.v_data.length + ')');

				node.tag.num_tables = p_return.v_data.length;

				if (node.childNodes.length > 0)
					node.removeChildNodes();

		        for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i],false,'/static/OmniDB_app/images/sequence_list.png',{ type:'sequence'},'cm_sequence');


		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving views.
/// </summary>
/// <param name="node">Node object.</param>
function getViews(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('Tree.aspx/GetViews',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				node.setText('Views (' + p_return.v_data.length + ')');

				if (node.childNodes.length > 0)
					node.removeChildNodes();

		        for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i],false,'/static/OmniDB_app/images/table.png',{ type:'view'},null);
		        }


			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving columns.
/// </summary>
/// <param name="node">Node object.</param>
function getColumns(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_columns/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": node.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_column_name,false,'/static/OmniDB_app/images/add.png',{ type:'table_field'},null);
		        	v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,false,'/static/OmniDB_app/images/bullet_red.png',null,null);
		        	v_node.createChildNode('Nullable: ' + p_return.v_data[i].v_nullable,false,'/static/OmniDB_app/images/bullet_red.png',null,null);

		        }

		        if (node.tag.has_primary_keys)
		        {
		        	v_node = node.createChildNode('Primary Key',false,'/static/OmniDB_app/images/key.png',{ type:'primary_key'},'cm_refresh');
		        	v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);
		        }

		        if (node.tag.has_foreign_keys)
		        {
		        	v_node = node.createChildNode('Foreign Keys',false,'/static/OmniDB_app/images/silver_key.png',{ type:'foreign_keys'},'cm_refresh');
		        	v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);
		        }

		        if (node.tag.has_uniques)
		        {
		        	v_node = node.createChildNode('Uniques',false,'/static/OmniDB_app/images/blue_key.png',{ type:'uniques'},'cm_refresh');
		        	v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);
		        }

		        if (node.tag.has_indexes)
		        {
		        	v_node = node.createChildNode('Indexes',false,'/static/OmniDB_app/images/index.png',{ type:'indexes'},'cm_refresh');
		        	v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);
		        }


			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving PKs.
/// </summary>
/// <param name="node">Node object.</param>
function getPK(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_pk/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": node.parent.text}),
			function(p_return) {


				if (node.childNodes.length > 0)
					node.removeChildNodes();


	        	if (p_return.v_data.length>0)
	        	v_node = node.createChildNode(p_return.v_data[0][0],false,'/static/OmniDB_app/images/key.png',{ type:'pk'},null);

		        for (i=0; i<p_return.v_data.length; i++) {

		        	v_node.createChildNode(p_return.v_data[i][1],false,'/static/OmniDB_app/images/bullet_red.png',null,null);


		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving Uniques.
/// </summary>
/// <param name="node">Node object.</param>
function getUniques(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_uniques/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": node.parent.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				v_curr_fk = '';

	        	new_node = '';
	        	new_name = '';

	        	var v_node;


	        	if (p_return.v_data.length>0) {

	        		for (i=0; i<p_return.v_data.length; i++) {

		        		if (v_curr_fk=='' || (p_return.v_data[i][0]!=v_curr_fk && v_curr_fk!='')) {

		        			v_curr_fk=p_return.v_data[i][0];

		        			v_node = node.createChildNode(p_return.v_data[i][0],false,'/static/OmniDB_app/images/blue_key.png',{ type:'unique'},null);

		        		}

		        		v_node.createChildNode(p_return.v_data[i][1],false,'/static/OmniDB_app/images/bullet_red.png',null,null);

	        		}

	        	}

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving Indexes.
/// </summary>
/// <param name="node">Node object.</param>
function getIndexes(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_indexes/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": node.parent.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				v_curr_fk = '';

	        	new_node = '';
	        	new_name = '';

	        	var v_node;


	        	if (p_return.v_data.length>0) {

	        		for (i=0; i<p_return.v_data.length; i++) {

		        		if (v_curr_fk=='' || (p_return.v_data[i][0]!=v_curr_fk && v_curr_fk!='')) {

		        			v_curr_fk=p_return.v_data[i][0];

		        			v_node = node.createChildNode(p_return.v_data[i][0] + ' (' + p_return.v_data[i][1] + ')',false,'/static/OmniDB_app/images/index.png',{ type:'index'},null);

		        		}

		        		v_node.createChildNode(p_return.v_data[i][2],false,'/static/OmniDB_app/images/add.png',null,null);

	        		}

	        	}

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving FKs.
/// </summary>
/// <param name="node">Node object.</param>
function getFKs(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_fks/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": node.parent.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();


		        v_curr_fk = '';

	        	new_node = '';
	        	new_name = '';

	        	var v_node;

		        for (i=0; i<p_return.v_data.length; i++) {

		        	if (v_curr_fk=='' || (p_return.v_data[i][0]!=v_curr_fk && v_curr_fk!='')) {

		        		v_node = node.createChildNode(p_return.v_data[i][0],false,'/static/OmniDB_app/images/silver_key.png',{ type:'foreign_key'},null);
		        		v_node.createChildNode('Referenced Table: ' + p_return.v_data[i][2],false,'/static/OmniDB_app/images/table.png',null,null);
		        		v_node.createChildNode('Delete Rule: ' + p_return.v_data[i][4],false,'/static/OmniDB_app/images/bullet_red.png',null,null);
		        		v_node.createChildNode('Update Rule: ' + p_return.v_data[i][5],false,'/static/OmniDB_app/images/bullet_red.png',null,null);


		        		v_curr_fk=p_return.v_data[i][0];



		        	}


		        	v_node.createChildNode(p_return.v_data[i][1] + ' <img style="vertical-align: middle;" src="../../../static/OmniDB_app/images/arrow_right.png"/> ' + p_return.v_data[i][3],false,'/static/OmniDB_app/images/add.png',null,null);


		        }

			},
			null,
			'box',
		false);
}

/// <summary>
/// Retrieving View Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getViewsColumns(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('Tree.aspx/GetViewColumns',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_table": node.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				for (i=0; i<p_return.v_data.length; i++) {


		        	v_node = node.createChildNode(p_return.v_data[i],false,'/static/OmniDB_app/images/add.png',{ type:'column'},null);

		        }


			},
			null,
			'box');
}

/// <summary>
/// Retrieving functions.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctions(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_functions/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Functions (' + p_return.v_data.length + ')');

				node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/gear.png',{ type:'function', id: p_return.v_data[i].v_id },'cm_function');
		        	getFunctionFields(v_node);

		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving function fields.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionFields(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_function_fields/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_function": node.tag.id}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

					if (p_return.v_data[i].v_type == 'O')
						v_node = node.createChildNode(p_return.v_data[i].v_name, false, '/static/OmniDB_app/images/output.png', null, null);
					else {
						if (p_return.v_data[i].v_type == 'I')
							v_node = node.createChildNode(p_return.v_data[i].v_name, false, '/static/OmniDB_app/images/input.png', null, null);
						else
 							v_node = node.createChildNode(p_return.v_data[i].v_name, false, '/static/OmniDB_app/images/input_output.png', null, null);
					}

		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionDefinition(node) {

	execAjax('/get_function_definition/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_function": node.tag.id}),
			function(p_return) {

				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(p_return.v_data);
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
				//v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
				renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,node.text);
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value = -2;

				var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

				if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht!=null) {
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.destroy();
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht = null;
				}

				v_div_result.innerHTML = '';

				maximizeEditor();

			},
			null,
			'box',
			true);

}

/// <summary>
/// Retrieving procedures.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedures(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_procedures/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Procedures (' + p_return.v_data.length + ')');

				node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/gear.png',{ type:'procedure', id: p_return.v_data[i].v_id },'cm_procedure');
		        	getProcedureFields(v_node);

		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving procedure fields.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedureFields(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_procedure_fields/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_procedure": node.tag.id}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

					if (p_return.v_data[i].v_type == 'O')
						v_node = node.createChildNode(p_return.v_data[i].v_name, false, '/static/OmniDB_app/images/output.png', null, null);
					else {
						if (p_return.v_data[i].v_type == 'I')
							v_node = node.createChildNode(p_return.v_data[i].v_name, false, '/static/OmniDB_app/images/input.png', null, null);
						else
 							v_node = node.createChildNode(p_return.v_data[i].v_name, false, '/static/OmniDB_app/images/input_output.png', null, null);
					}

		        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Retrieving procedure definition.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedureDefinition(node) {

	execAjax('/get_procedure_definition',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_procedure": node.tag.id}),
			function(p_return) {

				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(p_return.v_data);
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
				//v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
				renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,node.text);
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value = -2;

				var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

				if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht!=null) {
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.destroy();
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht = null;
				}

				v_div_result.innerHTML = '';

				maximizeEditor();

			},
			null,
			'box',
			true);

}
