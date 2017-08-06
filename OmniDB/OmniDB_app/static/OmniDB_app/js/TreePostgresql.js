/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function tabSQLTemplate(p_tab_name,p_template) {
	v_connTabControl.tag.createQueryTab(p_tab_name);
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(p_template);
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value = -2;

	var qtip = $(v_connTabControl.selectedTab.tag.tabControl.selectedLi).qtip({
	    content: { text: 'Adjust command and run!' },
			position: {
	        my: 'bottom center',
	        at: 'top center'
	    },
			style: { classes: 'qtip-bootstrap' },
	    show: { ready: true }
	})
	window.setTimeout(function () {
	  qtip.qtip('api').destroy();
	}, 4000);
}

/// <summary>
/// Retrieving tree.
/// </summary>
function getTreePostgresql(p_div) {

	execAjax('/get_tree_info_postgresql/',
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
											v_connTabControl.tag.createGraphTab('graph')
											drawGraph(false);
										}
									},
									{
										text : 'Complete Graph',
										icon: '/static/OmniDB_app/images/graph.png',
										action : function(node) {
											v_connTabControl.tag.createGraphTab('Complete graph')
											drawGraph(true);
										}
									}
								]
							}
						}
					]
				},
				'cm_databases' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
						{
							text : 'New Database',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('New Database',node.tree.tag.create_database);
							}
						}
					]
				},
				'cm_db' : {
					elements : [
                        {
							text : 'Alter Database',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('Alter Database',node.tree.tag.alter_database.replace('#database_name#',node.text));
							}
						},
						{
							text : 'Drop Database',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								tabSQLTemplate('Drop Database',node.tree.tag.drop_database.replace('#database_name#',node.text));
							}
						}
					]
				},
				'cm_tablespace' : {
					elements : [
                        {
							text : 'Alter Tablespace',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('Alter Tablespace',node.tree.tag.alter_tablespace.replace('#tablespace_name#',node.text));
							}
						},
						{
							text : 'Drop Tablespace',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								tabSQLTemplate('Drop Tablespace',node.tree.tag.drop_tablespace.replace('#tablespace_name#',node.text));
							}
						}
					]
				},
				'cm_role' : {
					elements : [
                        {
							text : 'Alter Role',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('Alter Role',node.tree.tag.alter_role.replace('#role_name#',node.text));
							}
						},
						{
							text : 'Drop Role',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								tabSQLTemplate('Drop Role',node.tree.tag.drop_role.replace('#role_name#',node.text));
							}
						}
					]
				},
				'cm_schema' : {
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
											v_connTabControl.tag.createGraphTab(node.text)
											drawGraph(false,node.text);
										}
									},
									{
										text : 'Complete Graph',
										icon: '/static/OmniDB_app/images/graph.png',
										action : function(node) {
											v_connTabControl.tag.createGraphTab(node.text)
											drawGraph(true,node.text);
										}
									}
								]
							}
						},
                        {
							text : 'Alter Schema',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('Alter Schema',node.tree.tag.alter_schema.replace('#schema_name#',node.text));
							}
						},
						{
							text : 'Drop Schema',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								tabSQLTemplate('Drop Schema',node.tree.tag.drop_schema.replace('#schema_name#',node.text));
							}
						}
					]
				},
				'cm_tablespaces' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
						{
							text : 'New Tablespace',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('New Tablespace',node.tree.tag.create_tablespace);
							}
						}
					]
				},
				'cm_roles' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
						{
							text : 'New Role',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('New Role',node.tree.tag.create_role);
							}
						}
					]
				},
				'cm_schemas' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
						{
							text : 'New Schema',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('New Schema',node.tree.tag.create_schema);
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
									refreshTreePostgresql(node);
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
								startAlterTable(true,'new', null, node.parent.text);
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
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
                        {
							text : 'New Function',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('New Function', node.tree.tag.create_function.replace('#schema_name#', node.parent.text));
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
									v_connTabControl.tag.createQueryTab(node.text);
								getFunctionDefinitionPostgresql(node);
							}
						},
						{
							text : 'Drop Function',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								tabSQLTemplate('Drop Function', node.tree.tag.drop_function.replace('#function_name#', node.tag.id));
							}
						},
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
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
									refreshTreePostgresql(node);
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
												v_connTabControl.tag.createQueryTab(node.text);

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
											startEditData(node.text,node.parent.parent.text);
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
												v_connTabControl.tag.createQueryTab(node.text);

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
											v_connTabControl.tag.createQueryTab('Delete Records');
											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue('DELETE FROM ' + node.text);
											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
											v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value = -2;
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
											startAlterTable(true,'alter', node.text, node.parent.parent.text);
										}
									},
									{
										text : 'Drop Table',
										icon: '/static/OmniDB_app/images/tab_close.png',
										action : function(node) {
											tabSQLTemplate('Drop Table', node.tree.tag.drop_table.replace('#table_name#',node.text));
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
									refreshTreePostgresql(node);
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
									refreshTreePostgresql(node);
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
								tabSQLTemplate('New Sequence', node.tree.tag.create_sequence.replace('#schema_name#', node.parent.text));
							}
						}
					]
				},
				'cm_sequence' : {
					elements : [
						{
							text : 'Alter Sequence',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('Alter Sequence', node.tree.tag.alter_sequence.replace('#sequence_name#', node.parent.parent.text + '.' + node.text));
							}
						},
						{
							text : 'Drop Sequence',
                            icon: '/static/OmniDB_app/images/tab_close.png',
                            action : function(node) {
            				    tabSQLTemplate('Drop Sequence', node.tree.tag.drop_sequence.replace('#sequence_name#', node.parent.parent.text + '.' + node.text));
                            }
						}
					]
				},
                'cm_views' : {
					elements : [
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						},
                        {
							text : 'New View',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								tabSQLTemplate('New View', node.tree.tag.create_view.replace('#schema_name#', node.parent.text));
							}
						}
					]
				},
				'cm_view' : {
					elements : [
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
                                    v_connTabControl.tag.createQueryTab(node.text);

                                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value = 10;

                                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue('-- Querying Data\nselect t.*\nfrom ' + v_table_name + ' t');
                                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
                                renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,node.text);

                                //minimizeEditor();

                                querySQL();
                            }
                        },
                        {
							text : 'Edit View',
							icon: '/static/OmniDB_app/images/text_edit.png',
							action : function(node) {
								if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='edit')
									v_connTabControl.tag.createQueryTab(node.text);
								getViewDefinitionPostgresql(node);
							}
						},
						{
							text : 'Drop View',
							icon: '/static/OmniDB_app/images/tab_close.png',
							action : function(node) {
								tabSQLTemplate('Drop View', node.tree.tag.drop_view.replace('#view_name#', node.parent.parent.text + '.' + node.text));
							}
						},
						{
							text : 'Refresh',
							icon: '/static/OmniDB_app/images/refresh.png',
							action : function(node) {
								if (node.childNodes==0)
									refreshTreePostgresql(node);
								else {
									node.collapseNode();
									node.expandNode();
								}
							}
						}
					]
				}
			};
		var tree = createTree(p_div,'#fcfdfd',context_menu);
		tree.tag = {
            create_tablespace: p_return.v_data.v_database_return.create_tablespace,
            alter_tablespace: p_return.v_data.v_database_return.alter_tablespace,
            drop_tablespace: p_return.v_data.v_database_return.drop_tablespace,
            create_role: p_return.v_data.v_database_return.create_role,
            alter_role: p_return.v_data.v_database_return.alter_role,
            drop_role: p_return.v_data.v_database_return.drop_role,
            create_database: p_return.v_data.v_database_return.create_database,
            alter_database: p_return.v_data.v_database_return.alter_database,
            drop_database: p_return.v_data.v_database_return.drop_database,
            create_schema: p_return.v_data.v_database_return.create_schema,
            alter_schema: p_return.v_data.v_database_return.alter_schema,
            drop_schema: p_return.v_data.v_database_return.drop_schema,
            //create_table
            //alter_table
            drop_table: p_return.v_data.v_database_return.drop_table,
            create_sequence: p_return.v_data.v_database_return.create_sequence,
            alter_sequence: p_return.v_data.v_database_return.alter_sequence,
            drop_sequence: p_return.v_data.v_database_return.drop_sequence,
            create_function: p_return.v_data.v_database_return.create_function,
            drop_function: p_return.v_data.v_database_return.drop_function,
            create_view: p_return.v_data.v_database_return.create_view,
            drop_view: p_return.v_data.v_database_return.drop_view
		}

		tree.nodeAfterOpenEvent = function(node) {
			refreshTreePostgresql(node);
		}

		var node1 = tree.createNode(p_return.v_data.v_database_return.v_database,true,'/static/OmniDB_app/images/db.png',null,null,null);
        var node_databases = tree.createNode('Databases',false,'/static/OmniDB_app/images/db.png',null,{ type:'database_list', num_databases : 0 },'cm_databases');
        node_databases.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
        var node_tablespaces = tree.createNode('Tablespaces',false,'/static/OmniDB_app/images/circle_blue.png',null,{ type:'tablespace_list', num_tablespaces : 0 },'cm_tablespaces');
        node_tablespaces.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
        var node_roles = tree.createNode('Roles',false,'/static/OmniDB_app/images/circle_blue.png',null,{ type:'role_list', num_roles : 0 },'cm_roles');
        node_roles.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

		var node2 = node1;

		node_schemas = tree.createNode('Schemas',false,'/static/OmniDB_app/images/schemas.png',node1,{ type:'schema_list', num_schemas : 0 },'cm_schemas');
        node_schemas.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

		tree.drawTree();
	},
	null,
	'box');

}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreePostgresql(node) {
	if (node.tag!=undefined)
    if (node.tag.type=='schema_list') {
      getSchemasPostgresql(node);
    }
		else if (node.tag.type=='table_list') {
			getTablesPostgresql(node);
		}
		else if (node.tag.type=='table') {
			getColumnsPostgresql(node);
		}
		else if (node.tag.type=='primary_key') {
			getPKPostgresql(node);
		}
		else if (node.tag.type=='uniques') {
			getUniquesPostgresql(node);
		}
		else if (node.tag.type=='foreign_keys') {
			getFKsPostgresql(node);
		}
		else if (node.tag.type=='sequence_list') {
			getSequencesPostgresql(node);
		}
		else if (node.tag.type=='view_list') {
			getViewsPostgresql(node);
		}
		else if (node.tag.type=='view') {
			getViewsColumnsPostgresql(node);
		}
		else if (node.tag.type=='indexes') {
			getIndexesPostgresql(node);
		}
		else if (node.tag.type=='function_list') {
			getFunctionsPostgresql(node);
		}
		else if (node.tag.type=='function') {
			getFunctionFieldsPostgresql(node);
		}
		else if (node.tag.type=='sequence_list') {
			getSequencesPostgresql(node);
		}
		else if (node.tag.type=='database_list') {
			getDatabasesPostgresql(node);
		}
		else if (node.tag.type=='tablespace_list') {
			getTablespacesPostgresql(node);
		}
		else if (node.tag.type=='role_list') {
			getRolesPostgresql(node);
		}

}

/// <summary>
/// Retrieving databases.
/// </summary>
/// <param name="node">Node object.</param>
function getDatabasesPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_databases_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Databases (' + p_return.v_data.length + ')');

				node.tag.num_databases = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/db.png',{ type:'database' },'cm_db');

        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving tablespaces.
/// </summary>
/// <param name="node">Node object.</param>
function getTablespacesPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_tablespaces_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Tablespaces (' + p_return.v_data.length + ')');

				node.tag.num_tablespaces = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/circle_blue.png',{ type:'tablespace' },'cm_tablespace');

        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving roles.
/// </summary>
/// <param name="node">Node object.</param>
function getRolesPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_roles_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Roles (' + p_return.v_data.length + ')');

				node.tag.num_tablespaces = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/circle_blue.png',{ type:'tablespace' },'cm_role');

        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving tables.
/// </summary>
/// <param name="node">Node object.</param>
function getTablesPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_tables_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                      "p_schema": node.parent.text}),
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving tables.
/// </summary>
/// <param name="node">Node object.</param>
function getSchemasPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_schemas_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Schemas (' + p_return.v_data.length + ')');

				node.tag.num_schemas = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/schemas.png',{ type:'schema', num_tables: 0},'cm_schema');

              var node_tables = v_node.createChildNode('Tables',false,'/static/OmniDB_app/images/table_multiple.png',{ type:'table_list', schema: p_return.v_data[i].v_name, num_tables : 0 },'cm_tables');
      				node_tables.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

      				var node_functions = v_node.createChildNode('Functions',false,'/static/OmniDB_app/images/gear.png',{ type:'function_list', schema: p_return.v_data[i].v_name, num_functions : 0 },'cm_functions');
      				node_functions.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

              var node_sequences = v_node.createChildNode('Sequences',false,'/static/OmniDB_app/images/sequence_list.png',{ type:'sequence_list', schema: p_return.v_data[i].v_name, num_sequences : 0 },'cm_sequences');
      				node_sequences.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

              var node_views = v_node.createChildNode('Views',false,'/static/OmniDB_app/images/circle_blue.png',{ type:'view_list', schema: p_return.v_data[i].v_name, num_views : 0 },'cm_views');
      				node_views.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
		        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving sequences.
/// </summary>
/// <param name="node">Node object.</param>
function getSequencesPostgresql(node) {
	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_sequences_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
										  "p_schema": node.parent.text}),
			function(p_return) {

				node.setText('Sequences (' + p_return.v_data.length + ')');

				node.tag.num_tables = p_return.v_data.length;

				if (node.childNodes.length > 0)
					node.removeChildNodes();

		        for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i],false,'/static/OmniDB_app/images/sequence_list.png',{ type:'sequence'},'cm_sequence');


		        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving views.
/// </summary>
/// <param name="node">Node object.</param>
function getViewsPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_views_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
							"p_schema": node.parent.text}),
			function(p_return) {

                if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Views (' + p_return.v_data.length + ')');

                node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/table.png',{ type:'view'},'cm_view');
                    v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',{ type:'view_field'},null);
		        }
			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving columns.
/// </summary>
/// <param name="node">Node object.</param>
function getColumnsPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_columns_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
										  "p_table": node.text,
										  "p_schema": node.parent.parent.text}),
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving PKs.
/// </summary>
/// <param name="node">Node object.</param>
function getPKPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_pk_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_table": node.parent.text,
										  "p_schema": node.parent.parent.parent.text}),
			function(p_return) {


				if (node.childNodes.length > 0)
					node.removeChildNodes();


	        	if (p_return.v_data.length>0)
	        	v_node = node.createChildNode(p_return.v_data[0][0],false,'/static/OmniDB_app/images/key.png',{ type:'pk'},null);

		        for (i=0; i<p_return.v_data.length; i++) {

		        	v_node.createChildNode(p_return.v_data[i][1],false,'/static/OmniDB_app/images/bullet_red.png',null,null);


		        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving Uniques.
/// </summary>
/// <param name="node">Node object.</param>
function getUniquesPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_uniques_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
										  "p_table": node.parent.text,
											"p_schema": node.parent.parent.parent.text}),
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving Indexes.
/// </summary>
/// <param name="node">Node object.</param>
function getIndexesPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_indexes_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
										  "p_table": node.parent.text,
											"p_schema": node.parent.parent.parent.text}),
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving FKs.
/// </summary>
/// <param name="node">Node object.</param>
function getFKsPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_fks_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
										  "p_table": node.parent.text,
											"p_schema": node.parent.parent.parent.text}),
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


		        	v_node.createChildNode(p_return.v_data[i][1] + ' <img style="vertical-align: middle;" src="/static/OmniDB_app/images/arrow_right.png"/> ' + p_return.v_data[i][3],false,'/static/OmniDB_app/images/add.png',null,null);


		        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
		false);
}

/// <summary>
/// Retrieving View Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getViewsColumnsPostgresql(node) {

    node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);

	execAjax('/get_views_columns_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
										  "p_table": node.text,
										  "p_schema": node.parent.parent.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_column_name,false,'/static/OmniDB_app/images/add.png',{ type:'table_field'},null);
		        	v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,false,'/static/OmniDB_app/images/bullet_red.png',null,null);
		        	v_node.createChildNode('Nullable: ' + p_return.v_data[i].v_nullable,false,'/static/OmniDB_app/images/bullet_red.png',null,null);

		        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving functions.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionsPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_functions_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_schema": node.parent.text}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				node.setText('Functions (' + p_return.v_data.length + ')');

				node.tag.num_tables = p_return.v_data.length;

				for (i=0; i<p_return.v_data.length; i++) {

		        	v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/gear.png',{ type:'function', id: p_return.v_data[i].v_id },'cm_function');
		        	v_node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',{ type:'function_field'},null);

		        }

			},
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving function fields.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionFieldsPostgresql(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_function_fields_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_function": node.tag.id,
											"p_schema": node.parent.parent.text}),
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			false);
}

/// <summary>
/// Retrieving function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionDefinitionPostgresql(node) {

	execAjax('/get_function_definition_postgresql/',
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			true);

}

/// <summary>
/// Retrieving view definition.
/// </summary>
/// <param name="node">Node object.</param>
function getViewDefinitionPostgresql(node) {

	execAjax('/get_view_definition_postgresql/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_view": node.text, "p_schema": node.parent.parent.text}),
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
			function(p_return) {
				nodeOpenError(p_return, node);
			},
			'box',
			true);

}

function nodeOpenError(p_return, p_node) {

	if (p_return.v_data.password_timeout) {
		p_node.collapseNode();
		showPasswordPrompt(
			v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
			function() {
				p_node.expandNode();
			},
			null
		);
	}
	else {
		if (p_node.childNodes.length > 0)
			p_node.removeChildNodes();

		v_node = p_node.createChildNode('Error',false,'/static/OmniDB_app/images/tab_close.png',{ type:'error' },null);
	}

}
