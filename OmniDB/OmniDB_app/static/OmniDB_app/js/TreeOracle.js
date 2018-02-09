/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function tabSQLTemplate(p_tab_name, p_template) {
    v_connTabControl.tag.createQueryTab(p_tab_name);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(
        p_template);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(
        0, 0, true);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
        .value = 1;

    var qtip = $(v_connTabControl.selectedTab.tag.tabControl.selectedLi).qtip({
        content: {
            text: 'Adjust command and run!'
        },
        position: {
            my: 'bottom center',
            at: 'top center'
        },
        style: {
            classes: 'qtip-bootstrap'
        },
        show: {
            ready: true
        }
    })
    window.setTimeout(function() {
        qtip.qtip('api').destroy();
    }, 4000);
}

/// <summary>
/// Retrieving tree.
/// </summary>
function getTreeOracle(p_div) {

    var context_menu = {
        'cm_server': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }]
        },
        'cm_connection': {
            elements: [{
                text: 'Render Graph',
                icon: '/static/OmniDB_app/images/graph.png',
                action: function(node) {

                },
                submenu: {
                    elements: [{
                        text: 'Simple Graph',
                        icon: '/static/OmniDB_app/images/graph.png',
                        action: function(node) {
                            v_connTabControl.tag.createGraphTab(
                                node.text)
                            drawGraph(false, node.tree.tag.v_username);
                        }
                    }, {
                        text: 'Complete Graph',
                        icon: '/static/OmniDB_app/images/graph.png',
                        action: function(node) {
                            v_connTabControl.tag.createGraphTab(
                                node.text)
                            drawGraph(true, node.tree.tag.v_username);
                        }
                    }]
                }
            }]
        },
        'cm_databases': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Database',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Database', node.tree
                        .tag.create_database);
                }
            }/*, {
                text: 'Doc: Databases',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Databases',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/managing-databases.html');
                }
            }*/]
        },
        'cm_database': {
            elements: [{
                text: 'Alter Database',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Database', node.tree.tag
                        .alter_database.replace(
                            '#database_name#', node.text));
                }
            }, {
                text: 'Drop Database',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Database', node.tree.tag
                        .drop_database.replace(
                            '#database_name#', node.text));
                }
            }]
        },
        'cm_tablespaces': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Tablespace',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Tablespace', node.tree
                        .tag.create_tablespace);
                }
            }/*, {
                text: 'Doc: Tablespaces',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Tablespaces',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/manage-ag-tablespaces.html'
                    );
                }
            }*/]
        },
        'cm_tablespace': {
            elements: [{
                text: 'Alter Tablespace',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Tablespace', node.tree
                        .tag.alter_tablespace.replace(
                            '#tablespace_name#', node.text)
                    );
                }
            }, {
                text: 'Drop Tablespace',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Tablespace', node.tree
                        .tag.drop_tablespace.replace(
                            '#tablespace_name#', node.text)
                    );
                }
            }]
        },
        'cm_roles': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Role',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Role', node.tree.tag
                        .create_role);
                }
            }/*, {
                text: 'Doc: Roles',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Roles',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/user-manag.html');
                }
            }*/]
        },
        'cm_role': {
            elements: [{
                text: 'Alter Role',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Role', node.tree.tag.alter_role
                        .replace('#role_name#', node.text));
                }
            }, {
                text: 'Drop Role',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Role', node.tree.tag.drop_role
                        .replace('#role_name#', node.text));
                }
            }]
        },
        'cm_tables': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Table',
                icon: '/static/OmniDB_app/images/new_table.png',
                action: function(node) {
                    startAlterTable(true, 'new', null, node.tree.tag.v_username);
                }
            }/*, {
                text: 'Doc: Basics',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Table Basics',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-basics.html');
                }
            }, {
                text: 'Doc: Constraints',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Table Constraints',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-constraints.html');
                }
            }, {
                text: 'Doc: Modifying',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Modifying Tables',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-alter.html');
                }
            }*/]
        },
        'cm_table': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Data Actions',
                icon: '/static/OmniDB_app/images/list.png',
                submenu: {
                    elements: [{
                        text: 'Query Data',
                        icon: '/static/OmniDB_app/images/query.png',
                        action: function(node) {

                            var v_table_name = '';
                            v_table_name = node.tree.tag.v_username + '.' + node.text;

                            v_connTabControl.tag.createQueryTab(
                                node.text);

                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.sel_filtered_data.value =
                                1;

                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    '-- Querying Data\nselect t.*\nfrom ' +
                                    v_table_name + ' t'
                                );
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            renameTabConfirm(
                                v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab,
                                node.text);

                            //minimizeEditor();

                            querySQL(0);
                        }
                    }, {
                        text: 'Edit Data',
                        icon: '/static/OmniDB_app/images/edit_data.png',
                        action: function(node) {
                            startEditData(node.text,
                                node.tree.tag.v_username
                            );
                        }
                    }, {
                        text: 'Count Records',
                        icon: '/static/OmniDB_app/images/counter.png',
                        action: function(node) {

                            var v_table_name = '';
                            v_table_name = node.tree.tag.v_username + '.' + node.text;

                            v_connTabControl.tag.createQueryTab(
                                node.text);

                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    "-- Counting Records\nselect count(*) as count\nfrom " +
                                    v_table_name + " t"
                                );
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            renameTabConfirm(
                                v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab,
                                node.text);

                            querySQL(0);
                        }
                    }, {
                        text: 'Delete Records',
                        icon: '/static/OmniDB_app/images/tab_close.png',
                        action: function(node) {
                            v_connTabControl.tag.createQueryTab(
                                'Delete Records');
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.setValue(
                                    'DELETE FROM ' +
                                    node.tree.tag.v_username + '.' + node.text);
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.clearSelection();
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.editor.gotoLine(0,
                                    0, true);
                            v_connTabControl.selectedTab
                                .tag.tabControl.selectedTab
                                .tag.sel_filtered_data.value =
                                1;
                        }
                    }]
                }
            }, {
                text: 'Table Actions',
                icon: '/static/OmniDB_app/images/list.png',
                submenu: {
                    elements: [{
                        text: 'Alter Table',
                        icon: '/static/OmniDB_app/images/table_edit.png',
                        action: function(node) {
                            startAlterTable(true,
                                'alter', node.text,
                                node.tree.tag.v_username
                            );
                        }
                    }, {
                        text: 'Drop Table',
                        icon: '/static/OmniDB_app/images/tab_close.png',
                        action: function(node) {
                            tabSQLTemplate('Drop Table',
                                node.tree.tag.drop_table
                                .replace(
                                    '#table_name#',
                                    node.tree.tag.v_username + '.' + node.text));
                        }
                    }]
                }
            }]
        },
        'cm_columns': {
            elements: [{
                text: 'Create Column',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Field', node.tree.tag
                        .create_column.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_column': {
            elements: [{
                text: 'Alter Column',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Column', node.tree.tag
                        .alter_column.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            /#column_name#/g, node.text));
                }
            }, {
                text: 'Drop Column',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Column', node.tree.tag
                        .drop_column.replace('#table_name#',
                            node.tree.tag.v_username + '.' + node.parent.parent
                            .text).replace(/#column_name#/g,
                            node.text));
                }
            }]
        },
        'cm_pks': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Primary Key',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Primary Key', node.tree
                        .tag.create_primarykey.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_pk': {
            elements: [{
                text: 'Drop Primary Key',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Primary Key', node.tree
                        .tag.drop_primarykey.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_fks': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Foreign Key',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Foreign Key', node.tree
                        .tag.create_foreignkey.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_fk': {
            elements: [{
                text: 'Drop Foreign Key',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Foreign Key', node.tree
                        .tag.drop_foreignkey.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_uniques': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Unique',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Unique', node.tree.tag
                        .create_unique.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }]
        },
        'cm_unique': {
            elements: [{
                text: 'Drop Unique',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Unique', node.tree.tag
                        .drop_unique.replace('#table_name#',
                            node.tree.tag.v_username + '.' + node.parent.parent
                            .text).replace(
                            '#constraint_name#', node.text)
                    );
                }
            }]
        },
        'cm_indexes': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Index',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Index', node.tree.tag
                        .create_index.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }/*, {
                text: 'Doc: Indexes',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Indexes',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/indexes.html');
                }
            }*/]
        },
        'cm_index': {
            elements: [{
                text: 'Alter Index',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Index', node.tree.tag
                        .alter_index.replace('#index_name#',
                            node.tree.tag.v_username + '.' +
                            node.text.replace(' (Unique)',
                                '').replace(' (Non Unique)',
                                '')));
                }
            }, {
                text: 'Drop Index',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Index', node.tree.tag.drop_index
                        .replace('#index_name#', node.tree.tag.v_username + '.' + node.text.replace(
                                ' (Unique)', '').replace(
                                ' (Non Unique)', '')));
                }
            }]
        },
        'cm_sequences': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Sequence',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Sequence', node.tree
                        .tag.create_sequence.replace(
                            '#schema_name#', node.tree.tag.v_username
                        ));
                }
            }/*, {
                text: 'Doc: Sequences',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Sequences',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createsequence.html');
                }
            }*/]
        },
        'cm_sequence': {
            elements: [{
                text: 'Alter Sequence',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Sequence', node.tree.tag
                        .alter_sequence.replace(
                            '#sequence_name#', node.tree.tag.v_username + '.' + node.text));
                }
            }, {
                text: 'Drop Sequence',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Sequence', node.tree.tag
                        .drop_sequence.replace(
                            '#sequence_name#', node.tree.tag.v_username + '.' + node.text));
                }
            }]
        },
        'cm_views': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create View', node.tree.tag
                        .create_view.replace(
                            '#schema_name#', node.tree.tag.v_username
                        ));
                }
            }/*, {
                text: 'Doc: Views',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Views',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createview.html');
                }
            }*/]
        },
        'cm_view': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Query Data',
                icon: '/static/OmniDB_app/images/query.png',
                action: function(node) {

                    var v_table_name = '';
                    v_table_name = node.tree.tag.v_username + '.' + node.text;

                    v_connTabControl.tag.createQueryTab(
                        node.text);

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.sel_filtered_data.value =
                        1;

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.setValue(
                            '-- Querying Data\nselect t.*\nfrom ' +
                            v_table_name + ' t');
                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.clearSelection();
                    renameTabConfirm(v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab, node.text
                    );

                    //minimizeEditor();

                    querySQL(0);
                }
            }, {
                text: 'Edit View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getViewDefinitionOracle(node);
                }
            }, {
                text: 'Drop View',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop View', node.tree.tag.drop_view
                        .replace('#view_name#', node.tree.tag.v_username + '.' + node.text)
                    );
                }
            }]
        },
        /*'cm_triggers': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                },
            }, {
                text: 'Create Trigger',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Trigger', node.tree.tag
                        .create_trigger.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Triggers',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Triggers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/trigger-definition.html');
                }
            }]
        },
        'cm_view_triggers': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                },
            }, {
                text: 'Create Trigger',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Trigger', node.tree.tag
                        .create_view_trigger.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Triggers',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Triggers',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/trigger-definition.html');
                }
            }]
        },
        'cm_trigger': {
            elements: [{
                text: 'Alter Trigger',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Alter Trigger', node.tree.tag
                        .alter_trigger.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }, {
                text: 'Enable Trigger',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Enable Trigger', node.tree.tag
                        .enable_trigger.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }, {
                text: 'Disable Trigger',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Disable Trigger', node.tree
                        .tag.disable_trigger.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }, {
                text: 'Drop Trigger',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Trigger', node.tree.tag
                        .drop_trigger.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#trigger_name#', node.text));
                }
            }]
        },
        'cm_partitions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Partition',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Partition', node.tree
                        .tag.create_partition.replace(
                            '#table_name#', node.tree.tag.v_username + '.' + node.parent
                            .text));
                }
            }, {
                text: 'Doc: Partitions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Partitions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/ddl-partitioning.html');
                }
            }]
        },
        'cm_partition': {
            elements: [{
                text: 'No Inherit Partition',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('No Inherit Partition', node
                        .tree.tag.noinherit_partition.replace(
                            '#table_name#', node.tree.tag.v_username + '.' +
                            node.parent.parent.text).replace(
                            '#partition_name#', node.text));
                }
            }, {
                text: 'Drop Partition',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Partition', node.tree.tag
                        .drop_partition.replace(
                            '#partition_name#', node.text));
                }
            }]
        },*/
        'cm_functions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Function',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Function', node.tree
                        .tag.create_function.replace(
                            '#schema_name#', node.tree.tag.v_username
                        ));
                }
            }/*, {
                text: 'Doc: Functions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createfunction.html');
                }
            }*/]
        },
        'cm_function': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Edit Function',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getFunctionDefinitionOracle(node);
                }
            }/*, {
                text: 'Debug Function',
                icon: '/static/OmniDB_app/images/debug.png',
                action: function(node) {
                    v_connTabControl.tag.createDebuggerTab(
                        node.text);
                    getDebugFunctionDefinitionOracle(node);
                    setupDebug(node);
                }
            }*/, {
                text: 'Drop Function',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Function', node.tree.tag
                        .drop_function.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_procedures': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Procedure',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Procedure', node.tree
                        .tag.create_procedure.replace(
                            '#schema_name#', node.tree.tag.v_username
                        ));
                }
            }/*, {
                text: 'Doc: Procedures',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-createfunction.html');
                }
            }*/]
        },
        'cm_procedure': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Edit Procedure',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getProcedureDefinitionOracle(node);
                }
            }/*, {
                text: 'Debug Procedure',
                icon: '/static/OmniDB_app/images/debug.png',
                action: function(node) {
                    v_connTabControl.tag.createDebuggerTab(
                        node.text);
                    getDebugProcedureDefinitionOracle(node);
                    setupDebug(node);
                }
            }*/, {
                text: 'Drop Procedure',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Procedure', node.tree.tag
                        .drop_procedure.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        /*'cm_triggerfunctions': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Trigger Function',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Trigger Function',
                        node.tree.tag.create_triggerfunction
                        .replace('#schema_name#', node.tree.tag.v_username));
                }
            }, {
                text: 'Doc: Trigger Functions',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Trigger Functions',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/plpgsql-trigger.html');
                }
            }]
        },
        'cm_triggerfunction': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Edit Trigger Function',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getTriggerFunctionDefinitionOracle(node);
                }
            }, {
                text: 'Drop Trigger Function',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Trigger Function',
                        node.tree.tag.drop_triggerfunction.replace(
                            '#function_name#', node.tag.id)
                    );
                }
            }]
        },
        'cm_mviews': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Create Mat. View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Create Materialized View',
                        node.tree.tag
                        .create_mview.replace(
                            '#schema_name#', node.tree.tag.v_username
                        ));
                }
            }, {
                text: 'Doc: Mat. Views',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: Materialized Views',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-creatematerializedview.html'
                    );
                }
            }]
        },
        'cm_mview': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }, {
                text: 'Query Data',
                icon: '/static/OmniDB_app/images/query.png',
                action: function(node) {

                    var v_table_name = '';
                    v_table_name = node.tree.tag.v_username + '.' + node.text;

                    v_connTabControl.tag.createQueryTab(
                        node.text);

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.sel_filtered_data.value =
                        1;

                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.setValue(
                            '-- Querying Data\nselect t.*\nfrom ' +
                            v_table_name + ' t');
                    v_connTabControl.selectedTab.tag.tabControl
                        .selectedTab.tag.editor.clearSelection();
                    renameTabConfirm(v_connTabControl.selectedTab
                        .tag.tabControl.selectedTab, node.text
                    );

                    //minimizeEditor();

                    querySQL(0);
                }
            }, {
                text: 'Edit Mat. View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    v_connTabControl.tag.createQueryTab(
                        node.text);
                    getMaterializedViewDefinitionOracle(
                        node);
                }
            }, {
                text: 'Refresh Mat. View',
                icon: '/static/OmniDB_app/images/text_edit.png',
                action: function(node) {
                    tabSQLTemplate('Refresh Materialized View',
                        node.tree.tag.refresh_mview
                        .replace('#view_name#', node.tree.tag.v_username + '.' + node.text)
                    );
                }
            }, {
                text: 'Drop Mat. View',
                icon: '/static/OmniDB_app/images/tab_close.png',
                action: function(node) {
                    tabSQLTemplate('Drop Materialized View',
                        node.tree.tag.drop_mview
                        .replace('#view_name#', node.tree.tag.v_username + '.' + node.text)
                    );
                }
            }]
        },*/
        'cm_refresh': {
            elements: [{
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            }]
        }
    };
    var tree = createTree(p_div, '#fcfdfd', context_menu);

    tree.nodeAfterOpenEvent = function(node) {
        refreshTreeOracle(node);
    }

    tree.clickNodeEvent = function(node) {
        getPropertiesOracle(node);
    }

    var node_server = tree.createNode('Oracle', false,
        '/static/OmniDB_app/images/oracle_medium.png', null, {
            type: 'server'
        }, 'cm_server');
    node_server.createChildNode('', true, '/static/OmniDB_app/images/spin.svg',
        null, null);
    tree.drawTree();


}

/// <summary>
/// Retrieving properties.
/// </summary>
/// <param name="node">Node object.</param>
function getPropertiesOracle(node) {
    if (node.tag != undefined)
        if (node.tag.type == 'role') {
          getProperties('/get_properties_oracle/',
            {
              p_schema: null,
              p_table: null,
              p_object: node.text,
              p_type: node.tag.type
            });
        } else if (node.tag.type == 'tablespace') {
          getProperties('/get_properties_oracle/',
            {
              p_schema: null,
              p_table: null,
              p_object: node.text,
              p_type: node.tag.type
            });
        } else if (node.tag.type == 'database') {
          getProperties('/get_properties_oracle/',
            {
              p_schema: null,
              p_table: null,
              p_object: node.text,
              p_type: node.tag.type
            });
        } else if (node.tag.type == 'table') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'sequence') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'view') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'mview') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'function') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'procedure') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'trigger') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: node.parent.parent.text,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else if (node.tag.type == 'triggerfunction') {
        getProperties('/get_properties_oracle/',
          {
            p_schema: null,
            p_table: null,
            p_object: node.text,
            p_type: node.tag.type
          });
      } else {
        clearProperties();
      }
}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreeOracle(node) {
    if (node.tag != undefined)
        if (node.tag.type == 'table_list') {
            getTablesOracle(node);
    } else if (node.tag.type == 'table') {
        getColumnsOracle(node);
    } else if (node.tag.type == 'primary_key') {
        getPKOracle(node);
    } else if (node.tag.type == 'uniques') {
        getUniquesOracle(node);
    } else if (node.tag.type == 'foreign_keys') {
        getFKsOracle(node);
    } else if (node.tag.type == 'view_list') {
        getViewsOracle(node);
    } else if (node.tag.type == 'view') {
        getViewsColumnsOracle(node);
    } /*else if (node.tag.type == 'mview_list') {
        getMaterializedViewsOracle(node);
    } else if (node.tag.type == 'mview') {
        getMaterializedViewsColumnsOracle(node);
    } */else if (node.tag.type == 'indexes') {
        getIndexesOracle(node);
    } else if (node.tag.type == 'function_list') {
        getFunctionsOracle(node);
    } else if (node.tag.type == 'function') {
        getFunctionFieldsOracle(node);
    } else if (node.tag.type == 'procedure_list') {
        getProceduresOracle(node);
    } else if (node.tag.type == 'procedure') {
        getProcedureFieldsOracle(node);
    } else if (node.tag.type == 'sequence_list') {
        getSequencesOracle(node);
    } else if (node.tag.type == 'database_list') {
        getDatabasesOracle(node);
    } else if (node.tag.type == 'tablespace_list') {
        getTablespacesOracle(node);
    } else if (node.tag.type == 'role_list') {
        getRolesOracle(node);
    } /*else if (node.tag.type == 'trigger_list') {
        getTriggersOracle(node);
    } else if (node.tag.type == 'triggerfunction_list') {
        getTriggerFunctionsOracle(node);
    } else if (node.tag.type == 'partition_list') {
        getPartitionsOracle(node);
    } */else if (node.tag.type == 'server') {
        getTreeDetailsOracle(node);
    }
}

/// <summary>
/// Retrieving tree details.
/// </summary>
/// <param name="node">Node object.</param>
function getTreeDetailsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_tree_info_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            node.tree.contextMenu.cm_server.elements = []
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Refresh',
                icon: '/static/OmniDB_app/images/refresh.png',
                action: function(node) {
                    if (node.childNodes == 0)
                        refreshTreeOracle(node);
                    else {
                        node.collapseNode();
                        node.expandNode();
                    }
                }
            });

            /*node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: PostgreSQL',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: PostgreSQL',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/');
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: SQL Language',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: SQL Language',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql.html');
                }
            });
            node.tree.contextMenu.cm_server.elements.push({
                text: 'Doc: SQL Commands',
                icon: '/static/OmniDB_app/images/globe.png',
                action: function(node) {
                    v_connTabControl.tag.createWebsiteTab(
                        'Documentation: SQL Commands',
                        'https://www.postgresql.org/docs/' +
                        getMajorVersion(node.tree.tag.version) +
                        '/static/sql-commands.html');
                }
            });*/

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tree.tag = {
                version: p_return.v_data.v_database_return.version,
                v_username: p_return.v_data.v_database_return.v_username,
                superuser: p_return.v_data.v_database_return.superuser,
                express: p_return.v_data.v_database_return.express,
                create_role: p_return.v_data.v_database_return.create_role,
                alter_role: p_return.v_data.v_database_return.alter_role,
                drop_role: p_return.v_data.v_database_return.drop_role,
                create_tablespace: p_return.v_data.v_database_return.create_tablespace,
                alter_tablespace: p_return.v_data.v_database_return.alter_tablespace,
                drop_tablespace: p_return.v_data.v_database_return.drop_tablespace,
                create_database: p_return.v_data.v_database_return.create_database,
                alter_database: p_return.v_data.v_database_return.alter_database,
                drop_database: p_return.v_data.v_database_return.drop_database,
                create_sequence: p_return.v_data.v_database_return.create_sequence,
                alter_sequence: p_return.v_data.v_database_return.alter_sequence,
                drop_sequence: p_return.v_data.v_database_return.drop_sequence,
                create_function: p_return.v_data.v_database_return.create_function,
                drop_function: p_return.v_data.v_database_return.drop_function,
                create_procedure: p_return.v_data.v_database_return.create_procedure,
                drop_procedure: p_return.v_data.v_database_return.drop_procedure,
                //create_triggerfunction: p_return.v_data.v_database_return
                //    .create_triggerfunction,
                //drop_triggerfunction: p_return.v_data.v_database_return
                //    .drop_triggerfunction,
                create_view: p_return.v_data.v_database_return.create_view,
                drop_view: p_return.v_data.v_database_return.drop_view,
                //create_mview: p_return.v_data.v_database_return.create_mview,
                //refresh_mview: p_return.v_data.v_database_return.refresh_mview,
                //drop_mview: p_return.v_data.v_database_return.drop_mview,
                //create_table
                //alter_table
                drop_table: p_return.v_data.v_database_return.drop_table,
                create_column: p_return.v_data.v_database_return.create_column,
                alter_column: p_return.v_data.v_database_return.alter_column,
                drop_column: p_return.v_data.v_database_return.drop_column,
                create_primarykey: p_return.v_data.v_database_return.create_primarykey,
                drop_primarykey: p_return.v_data.v_database_return.drop_primarykey,
                create_unique: p_return.v_data.v_database_return.create_unique,
                drop_unique: p_return.v_data.v_database_return.drop_unique,
                create_foreignkey: p_return.v_data.v_database_return.create_foreignkey,
                drop_foreignkey: p_return.v_data.v_database_return.drop_foreignkey,
                create_index: p_return.v_data.v_database_return.create_index,
                alter_index: p_return.v_data.v_database_return.alter_index,
                drop_index: p_return.v_data.v_database_return.drop_index//,
                //create_trigger: p_return.v_data.v_database_return.create_trigger,
                //create_view_trigger: p_return.v_data.v_database_return.create_view_trigger,
                //alter_trigger: p_return.v_data.v_database_return.alter_trigger,
                //enable_trigger: p_return.v_data.v_database_return.enable_trigger,
                //disable_trigger: p_return.v_data.v_database_return.disable_trigger,
                //drop_trigger: p_return.v_data.v_database_return.drop_trigger,
                //create_partition: p_return.v_data.v_database_return.create_partition,
                //noinherit_partition: p_return.v_data.v_database_return.noinherit_partition,
                //drop_partition: p_return.v_data.v_database_return.drop_partition
            }

            if (node.tree.tag.superuser) {
                node.tree.contextMenu.cm_server.elements.push({
                    text: 'Monitoring',
                    icon: '/static/OmniDB_app/images/monitoring.png',
                    action: function(node) {},
                    submenu: {
                        elements: [/*{
                            text: 'Dashboard',
                            icon: '/static/OmniDB_app/images/monitoring.png',
                            action: function(node) {
                                v_connTabControl.tag.createMonitorDashboardTab();
                                startMonitorDashboard();
                            }
                        }, */{
                            text: 'Sessions',
                            icon: '/static/OmniDB_app/images/monitoring.png',
                            action: function(node) {
                                v_connTabControl.tag.createMonitoringTab(
                                    'Sessions',
                                    'select * from v$session', [{
                                        icon: '/static/OmniDB_app/images/tab_close.png',
                                        title: 'Terminate',
                                        action: 'oracleTerminateBackend'
                                    }]);
                            }
                        }]
                    }
                });
            }/* else {
                node.tree.contextMenu.cm_server.elements.push({
                    text: 'Monitoring',
                    icon: '/static/OmniDB_app/images/monitoring.png',
                    action: function(node) {},
                    submenu: {
                        elements: [{
                            text: 'Dashboard',
                            icon: '/static/OmniDB_app/images/monitoring.png',
                            action: function(node) {
                                v_connTabControl.tag.createMonitorDashboardTab();
                                startMonitorDashboard();
                            }
                        }]
                    }
                });
            }*/

            node.setText(p_return.v_data.v_database_return.version);

            var node_connection = node.createChildNode(p_return.v_data.v_database_return
                .v_database, true, '/static/OmniDB_app/images/db.png', {
                    type: 'connection'
                }, 'cm_connection');

            if (node.tree.tag.superuser) {
                if (!node.tree.tag.express) {
                    var node_databases = node.createChildNode('Databases', false,
                        '/static/OmniDB_app/images/db.png', {
                            type: 'database_list',
                            num_databases: 0
                        }, 'cm_databases');
                    node_databases.createChildNode('', true,
                        '/static/OmniDB_app/images/spin.svg', null, null);
                }
                var node_tablespaces = node.createChildNode('Tablespaces',
                    false, '/static/OmniDB_app/images/folder.png', {
                        type: 'tablespace_list',
                        num_tablespaces: 0
                    }, 'cm_tablespaces');
                node_tablespaces.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
                var node_roles = node.createChildNode('Roles', false,
                    '/static/OmniDB_app/images/role.png', {
                        type: 'role_list',
                        num_roles: 0
                    }, 'cm_roles');
                node_roles.createChildNode('', true,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            var node_tables = node_connection.createChildNode('Tables', false,
                '/static/OmniDB_app/images/table_multiple.png', {
                    type: 'table_list',
                    num_tables: 0
                }, 'cm_tables');
            node_tables.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);

            var node_sequences = node_connection.createChildNode('Sequences',
                false,
                '/static/OmniDB_app/images/sequence_list.png', {
                    type: 'sequence_list',
                    num_sequences: 0
                }, 'cm_sequences');
            node_sequences.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);

            var node_views = node_connection.createChildNode('Views', false,
                '/static/OmniDB_app/images/view_multiple.png', {
                    type: 'view_list',
                    num_views: 0
                }, 'cm_views');
            node_views.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);

            /*var node_mviews = node_connection.createChildNode(
                'Materialized Views', false,
                '/static/OmniDB_app/images/view_multiple.png', {
                    type: 'mview_list',
                    num_views: 0
                }, 'cm_mviews');
            node_mviews.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);*/

            var node_functions = node_connection.createChildNode('Functions',
                false, '/static/OmniDB_app/images/gear2.png', {
                    type: 'function_list',
                    num_functions: 0
                }, 'cm_functions');
            node_functions.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);

            var node_functions = node_connection.createChildNode('Procedures',
                false, '/static/OmniDB_app/images/gear2.png', {
                    type: 'procedure_list',
                    num_functions: 0
                }, 'cm_procedures');
            node_functions.createChildNode('', true,
                '/static/OmniDB_app/images/spin.svg', null, null);

            if (v_connTabControl.selectedTab.tag.firstTimeOpen) {
              v_connTabControl.selectedTab.tag.firstTimeOpen = false;
              //v_connTabControl.tag.createMonitorDashboardTab();
              //startMonitorDashboard();
            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);

}

/// <summary>
/// Retrieving databases.
/// </summary>
/// <param name="node">Node object.</param>
function getDatabasesOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_databases_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Databases (' + p_return.v_data.length + ')');

            node.tag.num_databases = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/db.png', {
                        type: 'database'
                    }, 'cm_database');

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
function getTablespacesOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_tablespaces_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tablespaces (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/folder.png', {
                        type: 'tablespace'
                    }, 'cm_tablespace');

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
function getRolesOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_roles_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Roles (' + p_return.v_data.length + ')');

            node.tag.num_tablespaces = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/role.png', {
                        type: 'role'
                    }, 'cm_role');

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
function getTablesOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_tables_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Tables (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/table.png', {
                        type: 'table',
                        has_primary_keys: p_return.v_data[i].v_has_primary_keys,
                        has_foreign_keys: p_return.v_data[i].v_has_foreign_keys,
                        has_uniques: p_return.v_data[i].v_has_uniques,
                        has_indexes: p_return.v_data[i].v_has_indexes,
                        has_checks: p_return.v_data[i].v_has_checks,
                        has_excludes: p_return.v_data[i].v_has_excludes,
                        has_rules: p_return.v_data[i].v_has_rules,
                        has_triggers: p_return.v_data[i].v_has_triggers,
                        has_partitions: p_return.v_data[i].v_has_partitions
                    }, 'cm_table');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'table_field'
                    }, null);

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
function getSequencesOracle(node) {
    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_sequences_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Sequences (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_sequence_name,
                    false,
                    '/static/OmniDB_app/images/sequence_list.png', {
                        type: 'sequence'
                    }, 'cm_sequence');

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
function getViewsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_views_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Views (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/view.png', {
                        type: 'view',
                        has_triggers: p_return.v_data[i].v_has_triggers
                    }, 'cm_view');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'view_field'
                    }, null);
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
function getViewsColumnsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_views_columns_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.text,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, '/static/OmniDB_app/images/add.png', null,
                null);

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, '/static/OmniDB_app/images/add.png', {
                        type: 'table_field'
                    }, null);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }

            if (node.tag.has_rules) {
                v_node = node.createChildNode('Rules', false,
                    '/static/OmniDB_app/images/rule.png', {
                        type: 'rule_list'
                    }, 'cm_rules');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_triggers) {
                v_node = node.createChildNode('Triggers', false,
                    '/static/OmniDB_app/images/trigger.png', {
                        type: 'trigger_list'
                    }, 'cm_view_triggers');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving view definition.
/// </summary>
/// <param name="node">Node object.</param>
function getViewDefinitionOracle(node) {

    execAjax('/get_view_definition_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_view": node.text,
            "p_schema": null
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
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

/*
/// <summary>
/// Retrieving materialized views.
/// </summary>
/// <param name="node">Node object.</param>
function getMaterializedViewsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_mviews_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Materialized Views (' + p_return.v_data.length +
                ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/view.png', {
                        type: 'mview'
                    }, 'cm_mview');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'mview_field'
                    }, null);
            }
        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving Materialized View Columns.
/// </summary>
/// <param name="node">Node object.</param>
function getMaterializedViewsColumnsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_mviews_columns_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.text,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_column_name,
                    false, '/static/OmniDB_app/images/add.png', {
                        type: 'table_field'
                    }, null);
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving materialized view definition.
/// </summary>
/// <param name="node">Node object.</param>
function getMaterializedViewDefinitionOracle(node) {

    execAjax('/get_mview_definition_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_view": node.text,
            "p_schema": null
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
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
*/

/// <summary>
/// Retrieving columns.
/// </summary>
/// <param name="node">Node object.</param>
function getColumnsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_columns_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.text,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_list = node.createChildNode('Columns (' + p_return.v_data.length +
                ')', false, '/static/OmniDB_app/images/add.png', {
                    type: 'column_list'
                }, 'cm_columns');

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = v_list.createChildNode(p_return.v_data[i].v_column_name,
                    false, '/static/OmniDB_app/images/add.png', {
                        type: 'table_field'
                    }, 'cm_column');
                v_node.createChildNode('Type: ' + p_return.v_data[i].v_data_type,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);
                v_node.createChildNode('Nullable: ' + p_return.v_data[i].v_nullable,
                    false, '/static/OmniDB_app/images/bullet_red.png',
                    null, null);

            }

            if (node.tag.has_primary_keys) {
                v_node = node.createChildNode('Primary Key', false,
                    '/static/OmniDB_app/images/key.png', {
                        type: 'primary_key'
                    }, 'cm_pks');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_foreign_keys) {
                v_node = node.createChildNode('Foreign Keys', false,
                    '/static/OmniDB_app/images/silver_key.png', {
                        type: 'foreign_keys'
                    }, 'cm_fks');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_uniques) {
                v_node = node.createChildNode('Uniques', false,
                    '/static/OmniDB_app/images/blue_key.png', {
                        type: 'uniques'
                    }, 'cm_uniques');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_indexes) {
                v_node = node.createChildNode('Indexes', false,
                    '/static/OmniDB_app/images/index.png', {
                        type: 'indexes'
                    }, 'cm_indexes');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_triggers) {
                v_node = node.createChildNode('Triggers', false,
                    '/static/OmniDB_app/images/trigger.png', {
                        type: 'trigger_list'
                    }, 'cm_triggers');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
            }

            if (node.tag.has_partitions) {
                v_node = node.createChildNode('Partitions', false,
                    '/static/OmniDB_app/images/partition.png', {
                        type: 'partition_list'
                    }, 'cm_partitions');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', null, null);
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
function getPKOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_pk_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Primary Key (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0) {
                node.removeChildNodes();
                //node.contextMenu = 'cm_refresh'
            } else {
                //node.contextMenu = 'cm_pks'
            }

            if (p_return.v_data.length > 0)
                v_node = node.createChildNode(p_return.v_data[0][0], false,
                    '/static/OmniDB_app/images/key.png', {
                        type: 'pk'
                    }, 'cm_pk');

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node.createChildNode(p_return.v_data[i][1], false,
                    '/static/OmniDB_app/images/add.png', null, null);

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
function getUniquesOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_uniques_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Uniques (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_curr_fk = '';

            new_node = '';
            new_name = '';

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    if (v_curr_fk == '' || (p_return.v_data[i][0] !=
                            v_curr_fk && v_curr_fk != '')) {

                        v_curr_fk = p_return.v_data[i][0];

                        v_node = node.createChildNode(p_return.v_data[i][0],
                            false,
                            '/static/OmniDB_app/images/blue_key.png', {
                                type: 'unique'
                            }, 'cm_unique');

                    }

                    v_node.createChildNode(p_return.v_data[i][1], false,
                        '/static/OmniDB_app/images/add.png', null, null
                    );

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
function getIndexesOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_indexes_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Indexes (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_curr_fk = '';

            new_node = '';
            new_name = '';

            var v_node;


            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    if (v_curr_fk == '' || (p_return.v_data[i][0] !=
                            v_curr_fk && v_curr_fk != '')) {

                        v_curr_fk = p_return.v_data[i][0];

                        v_node = node.createChildNode(p_return.v_data[i][0] +
                            ' (' + p_return.v_data[i][1] + ')', false,
                            '/static/OmniDB_app/images/index.png', {
                                type: 'index'
                            }, 'cm_index');

                    }

                    v_node.createChildNode(p_return.v_data[i][2], false,
                        '/static/OmniDB_app/images/add.png', null, null
                    );

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
function getFKsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_fks_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Foreign Keys (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            v_curr_fk = '';

            new_node = '';
            new_name = '';

            var v_node;

            for (i = 0; i < p_return.v_data.length; i++) {

                if (v_curr_fk == '' || (p_return.v_data[i][0] != v_curr_fk &&
                        v_curr_fk != '')) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false,
                        '/static/OmniDB_app/images/silver_key.png', {
                            type: 'foreign_key'
                        }, 'cm_fk');
                    v_node.createChildNode('Referenced Table: ' + p_return.v_data[
                            i][2], false,
                        '/static/OmniDB_app/images/table.png', null,
                        null);
                    v_node.createChildNode('Delete Rule: ' + p_return.v_data[
                            i][4], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);
                    v_node.createChildNode('Update Rule: ' + p_return.v_data[
                            i][5], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);

                    v_curr_fk = p_return.v_data[i][0];

                }

                v_node.createChildNode(p_return.v_data[i][1] +
                    ' <img style="vertical-align: middle;" src="/static/OmniDB_app/images/arrow_right.png"/> ' +
                    p_return.v_data[i][3], false,
                    '/static/OmniDB_app/images/add.png', null, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/*
/// <summary>
/// Retrieving Triggers.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggersOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_triggers_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Triggers (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false, '/static/OmniDB_app/images/trigger.png', {
                            type: 'trigger'
                        }, 'cm_trigger');
                    v_node.createChildNode('Enabled: ' + p_return.v_data[i]
                        [1], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);
                    v_node.createChildNode('Function: ' + p_return.v_data[i]
                        [2], false,
                        '/static/OmniDB_app/images/bullet_red.png',
                        null, null);

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
/// Retrieving Partitions.
/// </summary>
/// <param name="node">Node object.</param>
function getPartitionsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_partitions_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_table": node.parent.text,
            "p_schema": null
        }),
        function(p_return) {

            node.setText('Partitions (' + p_return.v_data.length + ')');

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            var v_node;

            if (p_return.v_data.length > 0) {

                for (i = 0; i < p_return.v_data.length; i++) {

                    v_node = node.createChildNode(p_return.v_data[i][0],
                        false,
                        '/static/OmniDB_app/images/partition.png', {
                            type: 'partition'
                        }, 'cm_partition');

                }

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}
*/

/// <summary>
/// Retrieving functions.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_functions_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Functions (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/gear2.png', {
                        type: 'function',
                        id: p_return.v_data[i].v_id
                    }, 'cm_function');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'function_field'
                    }, null);

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
function getFunctionFieldsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_function_fields_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_function": node.tag.id,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                if (p_return.v_data[i].v_type == 'O')
                    v_node = node.createChildNode(p_return.v_data[i].v_name,
                        false, '/static/OmniDB_app/images/output.png', null,
                        null);
                else {
                    if (p_return.v_data[i].v_type == 'I')
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false, '/static/OmniDB_app/images/input.png',
                            null, null);
                    else
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false,
                            '/static/OmniDB_app/images/input_output.png',
                            null, null);
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
/*function getDebugFunctionDefinitionOracle(node) {

    execAjax('/get_function_debug_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}*/

/// <summary>
/// Retrieving function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getFunctionDefinitionOracle(node) {

    execAjax('/get_function_definition_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
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
/// Retrieving procedures.
/// </summary>
/// <param name="node">Node object.</param>
function getProceduresOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_procedures_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Procedures (' + p_return.v_data.length + ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                v_node = node.createChildNode(p_return.v_data[i].v_name,
                    false, '/static/OmniDB_app/images/gear2.png', {
                        type: 'procedure',
                        id: p_return.v_data[i].v_id
                    }, 'cm_procedure');
                v_node.createChildNode('', false,
                    '/static/OmniDB_app/images/spin.svg', {
                        type: 'procedure_field'
                    }, null);

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving procedure fields.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedureFieldsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);

    execAjax('/get_procedure_fields_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_procedure": node.tag.id,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                if (p_return.v_data[i].v_type == 'O')
                    v_node = node.createChildNode(p_return.v_data[i].v_name,
                        false, '/static/OmniDB_app/images/output.png', null,
                        null);
                else {
                    if (p_return.v_data[i].v_type == 'I')
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false, '/static/OmniDB_app/images/input.png',
                            null, null);
                    else
                        v_node = node.createChildNode(p_return.v_data[i].v_name,
                            false,
                            '/static/OmniDB_app/images/input_output.png',
                            null, null);
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
/// Retrieving procedure definition.
/// </summary>
/// <param name="node">Node object.</param>
/*function getDebugProcedureDefinitionOracle(node) {

    execAjax('/get_function_debug_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        true);

}*/

/// <summary>
/// Retrieving procedure definition.
/// </summary>
/// <param name="node">Node object.</param>
function getProcedureDefinitionOracle(node) {

    execAjax('/get_procedure_definition_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_procedure": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
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

/*
/// <summary>
/// Retrieving trigger functions.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggerFunctionsOracle(node) {

    node.removeChildNodes();
    node.createChildNode('', false, '/static/OmniDB_app/images/spin.svg', null,
        null);


    execAjax('/get_triggerfunctions_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_schema": null
        }),
        function(p_return) {

            if (node.childNodes.length > 0)
                node.removeChildNodes();

            node.setText('Trigger Functions (' + p_return.v_data.length +
                ')');

            node.tag.num_tables = p_return.v_data.length;

            for (i = 0; i < p_return.v_data.length; i++) {

                node.createChildNode(p_return.v_data[i].v_name, false,
                    '/static/OmniDB_app/images/gear2.png', {
                        type: 'triggerfunction',
                        id: p_return.v_data[i].v_id
                    }, 'cm_triggerfunction');

            }

        },
        function(p_return) {
            nodeOpenError(p_return, node);
        },
        'box',
        false);
}

/// <summary>
/// Retrieving trigger function definition.
/// </summary>
/// <param name="node">Node object.</param>
function getTriggerFunctionDefinitionOracle(node) {

    execAjax('/get_triggerfunction_definition_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_function": node.tag.id
        }),
        function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .setValue(p_return.v_data);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .clearSelection();
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor
                .gotoLine(0, 0, true);
            //v_connTabControl.selectedTab.tag.tabControl.selectedTab.renameTab(node.text);
            renameTabConfirm(v_connTabControl.selectedTab.tag.tabControl.selectedTab,
                node.text);
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data
                .value = 1;

            var v_div_result = v_connTabControl.selectedTab.tag.tabControl.selectedTab
                .tag.div_result;

            if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                .ht != null) {
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht.destroy();
                v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
                    .ht = null;
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
*/

function nodeOpenError(p_return, p_node) {

    if (p_return.v_data.password_timeout) {
        p_node.collapseNode();
        showPasswordPrompt(
            v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            function() {
                p_node.expandNode();
            },
            null,
            p_return.v_data.message
        );
    } else {

        if (p_node.childNodes.length > 0)
            p_node.removeChildNodes();

        v_node = p_node.createChildNode(
            "Error - <a class='a_link' onclick='showError(&quot;" +
            p_return.v_data.replace(/\n/g, "<br/>").replace(/"/g, '') +
            "&quot;)'>View Detail</a>", false,
            '/static/OmniDB_app/images/tab_close.png', {
                type: 'error',
                message: p_return.v_data
            }, null);
    }

}

/*function getMajorVersion(p_version) {
    var v_version = p_version.split(' (')[0]
    var tmp = v_version.replace('PostgreSQL ', '').replace('beta', '.').split(
        '.')
    tmp.pop()
    return tmp.join('.')
}*/

function oracleTerminateBackendConfirm(p_pid) {
    execAjax('/kill_backend_oracle/',
        JSON.stringify({
            "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            "p_pid": p_pid
        }),
        function(p_return) {

            refreshMonitoring();

        },
        function(p_return) {
            if (p_return.v_data.password_timeout) {
                showPasswordPrompt(
                    v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                    function() {
                        oracleTerminateBackendConfirm(p_pid);
                    },
                    null,
                    p_return.v_data.message
                );
            } else {
                showError(p_return.v_data);
            }
        },
        'box',
        true);

}

function oracleTerminateBackend(p_row) {

    var v_pid = p_row[1] + ',' + p_row[2];

    showConfirm('Are you sure you want to terminate session ' + v_pid + '?',
        function() {

            oracleTerminateBackendConfirm(v_pid);

        });

}
