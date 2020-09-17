var bdr_templates;

activateHook('postgresqlTreeNodeOpen',function(p_node) {
  refreshTreeBDR(p_node);
});

activateHook('postgresqlTreeContextMenu',function(p_node) {

  if (p_node.tag.type == 'bdr_notset') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Create Group',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Create Group', bdr_templates
                .bdr_create_group);
        }
    }, {
        text: 'Join Group',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Join Group', bdr_templates
                .bdr_join_group);
        }
    }, {
        text: 'Join Group Wait',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Join Group Wait', bdr_templates
                .bdr_join_wait);
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'http://bdr-project.org/docs/1.0/index.html'
            );
        }
    }];

  } else if (p_node.tag.type == 'bdr_paused') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Replicate DDL',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate(
                'Replicate DDL Command',
                bdr_templates
                .bdr_replicate_ddl_command);
        }
    }, {
        text: 'Resume Apply',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Resume Apply',
                bdr_templates.bdr_resume);
        }
    }, {
        text: 'Remove BDR',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Remove BDR',
                bdr_templates
                .bdr_remove);
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'http://bdr-project.org/docs/1.0/index.html'
            );
        }
    }];

  } else if (p_node.tag.type == 'bdr') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Replicate DDL',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate(
                'Replicate DDL Command',
                bdr_templates
                .bdr_replicate_ddl_command);
        }
    }, {
        text: 'Pause Apply',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Pause Apply',
                bdr_templates.bdr_pause);
        }
    }, {
        text: 'Remove BDR',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Remove BDR',
                bdr_templates
                .bdr_remove);
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'http://bdr-project.org/docs/1.0/index.html'
            );
        }
    }];

  } else if (p_node.tag.type == 'bdr_node_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }];

  } else if (p_node.tag.type == 'bdr_node') {

    return v_elements = [{
        text: 'Terminate Apply',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Terminate Apply',
                bdr_templates
                .bdr_terminate_apply
                .replace('#node_name#',
                    v_node.text));
        }
    }, {
        text: 'Terminate WAL Sender',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate(
                'Terminate WAL Sender',
                bdr_templates
                .bdr_terminate_walsender
                .replace('#node_name#',
                    v_node.text));
        }
    }, {
        text: 'Part Node',
        icon: 'fas cm-all fa-times',
        action: function(node) {
            tabSQLTemplate('Part Node', bdr_templates
                .bdr_part_node
                .replace('#node_name#', v_node.text)
            );
        }
    }];

  } else if (p_node.tag.type == 'bdr_local_node') {

    return v_elements = [];

  } else if (p_node.tag.type == 'bdr_repset_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Insert Replication Set',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Insert Replication Set',
                bdr_templates.bdr_insert_repset);
        }
    }];

  } else if (p_node.tag.type == 'bdr_repset') {

    return v_elements = [{
        text: 'Update Rep. Set',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Update Replication Set',
                bdr_templates.bdr_update_repset
                .replace('#set_name#', node.text));
        }
    }, {
        text: 'Delete Replication Set',
        icon: 'fas cm-all fa-times',
        action: function(node) {
            tabSQLTemplate('Delete Replication Set',
                bdr_templates.bdr_delete_repset
                .replace('#set_name#', node.text));
        }
    }];

  } else if (p_node.tag.type == 'bdr_table') {

    return v_elements = [];

  } else if (p_node.tag.type == 'bdr_table_repset_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Set Replication Sets',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Set Replication Sets', bdr_templates.bdr_set_repsets
                .replace('#table_name#', node.parent
                    .parent.parent.parent.text +
                    '.' + node.parent.parent.text));
        }
    }];

  } else if (p_node.tag.type == 'bdr_table_repset') {

    return v_elements = [];

  } else if (p_node.tag.type == 'bdr_table_confhand_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Create Conf. Handler',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Create Conflict Handler',
                bdr_templates.bdr_create_confhand
                .replace(/#table_name#/g, node.parent
                    .parent.parent.parent.text +
                    '.' + node.parent.parent.text));
        }
    }];

  } else if (p_node.tag.type == 'bdr_table_confhand') {

    return v_elements = [{
        text: 'Drop Conf. Handler',
        icon: 'fas cm-all fa-times',
        action: function(node) {
            tabSQLTemplate('Drop Conflict Handler',
                bdr_templates.bdr_drop_confhand
                .replace('#table_name#', node.parent
                    .parent.parent.parent.parent.text +
                    '.' + node.parent.parent.parent
                    .text)
                .replace('#ch_name#', node.text));
        }
    }];

  } else {

    return v_elements = [];

  }

});

function getBDRMajorVersion(p_version) {
    return p_version.split('.')[0]
}

function refreshTreeBDR(node) {
  if (node.tag.type == 'database') {
    startBDR(node);
  } else if (node.tag.type == 'bdr' ||
             node.tag.type == 'bdr_notset' ||
             node.tag.type == 'bdr_paused') {
    getBDRProperties(node);
  } else if (node.tag.type == 'bdr_node_list') {
    getBDRNodes(node);
  } else if (node.tag.type == 'bdr_repset_list') {
    getBDRReplicationSets(node);
  } else if (node.tag.type == 'table') {
    startBDRTable(node);
  } else if (node.tag.type == 'bdr_table_repset_list') {
    getBDRTableReplicationSets(node);
  } else if (node.tag.type == 'bdr_table_confhand_list') {
    getBDRTableConflictHandlers(node);
  }
}

function startBDR(node) {
  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_version',
    p_data: null,
    p_callback: function(p_data) {
      if (p_data.bdr_version != null &&
          parseInt(getBDRMajorVersion(p_data.bdr_version)) < 3) {

            callPluginFunction({
              p_plugin_name: 'bdr',
              p_function_name: 'get_bdr_templates',
              p_data: null,
              p_callback: function(p_data) {
                bdr_templates = p_data;
              },
              p_loading: false,
              p_check_database_connection: true
            });

            callPluginFunction({
              p_plugin_name: 'bdr',
              p_function_name: 'get_bdr_properties',
              p_data: null,
              p_callback: function(p_data) {

                if (p_data[0].v_node_name == 'Not set') {

                  var node_bdr = node.createChildNode(
                      'BDR', false,
                      'node-bdr', {
                          type: 'bdr_notset',
                      }, null);
                  node_bdr.createChildNode('', true,
                      'node-spin', null, null);

                } else {

                  if (p_data[0].v_paused) {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'node-bdr', {
                            type: 'bdr_paused',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  } else {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'node-bdr', {
                            type: 'bdr',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  }

                }

                node_bdr.createChildNode('Version: ' + p_data[0]
                    .v_version, false,
                    'fas node-all fa-ellipsis-h node-bullet', null, null);
                node_bdr.createChildNode('Active: ' + p_data[0]
                    .v_active, false,
                    'fas node-all fa-ellipsis-h node-bullet', null, null);
                node_bdr.createChildNode('Node name: ' + p_data[0]
                    .v_node_name, false,
                    'fas node-all fa-ellipsis-h node-bullet', null, null);
                node_bdr.createChildNode('Paused: ' + p_data[0]
                    .v_paused, false,
                    'fas node-all fa-ellipsis-h node-bullet', null, null);
                v_nodes = node_bdr.createChildNode('Nodes',
                    false, 'fas node-all fa-server node-bdr-server', {
                        type: 'bdr_node_list',
                    }, null);
                v_nodes.createChildNode('', true,
                    'node-spin', null, null);
                v_repsets = node_bdr.createChildNode('Replication Sets',
                    false,
                    'fas node-all fa-tasks node-bdr-repset', {
                        type: 'bdr_repset_list',
                    }, null);
                v_repsets.createChildNode('', true,
                    'node-spin', null, null);

              },
              p_loading: false,
              p_check_database_connection: true
            });

      }
    },
    p_loading: false,
    p_check_database_connection: true
  });
}

function getBDRProperties(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null, null);

  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_properties',
    p_data: null,
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.createChildNode('Version: ' + p_data[0]
          .v_version, false,
          'fas node-all fa-ellipsis-h node-bullet', null, null);
      node.createChildNode('Active: ' + p_data[0]
          .v_active, false,
          'fas node-all fa-ellipsis-h node-bullet', null, null);
      node.createChildNode('Node name: ' + p_data[0]
          .v_node_name, false,
          'fas node-all fa-ellipsis-h node-bullet', null, null);
      node.createChildNode('Paused: ' + p_data[0]
          .v_paused, false,
          'fas node-all fa-ellipsis-h node-bullet', null, null);
      v_nodes = node.createChildNode('Nodes',
          false, 'fas node-all fa-server node-bdr-server', {
              type: 'bdr_node_list',
          }, null);
      v_nodes.createChildNode('', true,
          'node-spin', null, null);
      v_repsets = node.createChildNode('Replication Sets',
          false,
          'fas node-all fa-tasks node-bdr-repset', {
              type: 'bdr_repset_list',
          }, null);
      v_repsets.createChildNode('', true,
          'node-spin', null, null);

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

/// <summary>
/// Retrieving BDR Nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRNodes(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null, null);

  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_nodes',
    p_data: null,
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.setText('Nodes (' + p_data.length + ')');

      node.tag.num_nodes = p_data.length;

      for (i = 0; i < p_data.length; i++) {

          if (p_data[i].v_is_local) {
              v_node = node.createChildNode(p_data[i].v_name,
                  false, 'fas node-all fa-server node-bdr-server', {
                      type: 'bdr_local_node',
                  }, null, null, false);
          } else {
              v_node = node.createChildNode(p_data[i].v_name,
                  false, 'fas node-all fa-server node-bdr-server', {
                      type: 'bdr_node',
                  }, null, null, false);
          }

      }

      node.drawChildNodes();

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

/// <summary>
/// Retrieving BDR Replication Sets.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRReplicationSets(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null, null);

  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_replicationsets',
    p_data: null,
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.setText('Replication Sets (' + p_data.length + ')');

      node.tag.num_repsets = p_data.length;

      for (i = 0; i < p_data.length; i++) {

          v_node = node.createChildNode(p_data[i].v_name,
              false,
              'fas node-all fa-tasks node-bdr-repset', {
                  type: 'bdr_repset',
              }, null, null, false);
          v_node.createChildNode('Inserts: ' + p_data[0]
              .v_inserts, false,
              'fas node-all fa-ellipsis-h node-bullet', null,
              null, null, false);
          v_node.createChildNode('Updates: ' + p_data[0]
              .v_updates, false,
              'fas node-all fa-ellipsis-h node-bullet', null,
              null, null, false);
          v_node.createChildNode('Deletes: ' + p_data[0]
              .v_deletes, false,
              'fas node-all fa-ellipsis-h node-bullet', null,
              null, null, false);

      }

      node.drawChildNodes();

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

function startBDRTable(node) {

  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_version',
    p_data: null,
    p_callback: function(p_data) {
      if (p_data.bdr_version != null &&
          parseInt(getBDRMajorVersion(p_data.bdr_version)) < 3) {

            var node_bdr = node.createChildNode('BDR', false,
                'node-bdr', {
                    type: 'bdr_table',
                }, null, null, true);
            var node_repset = node_bdr.createChildNode('Replication Sets',
                false,
                'fas node-all fa-tasks node-bdr-repset', {
                    type: 'bdr_table_repset_list',
                }, null, null, true);
            node_repset.createChildNode('', true,
                'node-spin', null, null,
                null, true);
            var node_confhand = node_bdr.createChildNode('Conflict Handlers',
                false,
                'fas node-all fa-exchange-alt node-bdr-conflict', {
                    type: 'bdr_table_confhand_list',
                }, null, null, true);
            node_confhand.createChildNode('', true,
                'node-spin', null, null,
                null, true);

      }
    },
    p_loading: false,
    p_check_database_connection: true
  });

}

/// <summary>
/// Retrieving BDR Table Replication Sets.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRTableReplicationSets(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null, null);

  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_table_replicationsets',
    p_data: {
      "p_table": node.parent.parent.text,
      "p_schema": node.parent.parent.parent.parent.text
    },
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.setText('Replication Sets (' + p_data.length + ')');

      node.tag.num_repsets = p_data.length;

      for (i = 0; i < p_data.length; i++) {

          node.createChildNode(p_data[i].v_name, false,
              'fas node-all fa-tasks node-bdr-repset', {
                  type: 'bdr_table_repset',
              }, null, null, false);

      }

      node.drawChildNodes();

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

/// <summary>
/// Retrieving BDR Table Conflict Handlers.
/// </summary>
/// <param name="node">Node object.</param>
function getBDRTableConflictHandlers(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null, null);

  callPluginFunction({
    p_plugin_name: 'bdr',
    p_function_name: 'get_bdr_table_conflicthandlers',
    p_data: {
      "p_table": node.parent.parent.text,
      "p_schema": node.parent.parent.parent.parent.text
    },
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.setText('Conflict Handlers (' + p_data.length + ')');

      node.tag.num_chs = p_data.length;

      for (i = 0; i < p_data.length; i++) {

          v_node = node.createChildNode(p_data[i].v_name,
              false,
              'fas node-all fa-exchange-alt node-bdr-conflict', {
                  type: 'bdr_table_confhand',
              }, null, null, false);
          v_node.createChildNode('Type: ' + p_data[i]
              .v_type, false,
              'fas node-all fa-ellipsis-h node-bullet', null,
              null, null, false);
          v_node.createChildNode('Function: ' + p_data[i]
              .v_function, false,
              'fas node-all fa-ellipsis-h node-bullet', null,
              null, null, false);

      }

      node.drawChildNodes();

    },
    p_loading: false,
    p_check_database_connection: true
  });

}
