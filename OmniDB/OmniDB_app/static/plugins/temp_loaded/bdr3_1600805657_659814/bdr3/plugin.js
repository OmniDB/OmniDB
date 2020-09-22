var bdr3_templates;

activateHook('postgresqlTreeNodeOpen',function(p_node) {
  refreshTreeBDR3(p_node);
});

activateHook('postgresqlTreeContextMenu',function(node) {

  if (node.tag.type == 'bdr3_inactive_nonode') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Create Local Node',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate(
                'Create Local Node',
                bdr3_templates.bdr3_create_local_node);
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'https://documentation.2ndquadrant.com/bdr3/release/latest/'
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_inactive_node') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Create Group',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Create Group',
                bdr3_templates.bdr3_create_group);
        }
    }, {
        text: 'Join Group',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Join Group',
                bdr3_templates.bdr3_join_group);
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'https://documentation.2ndquadrant.com/bdr3/release/latest/'
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_joining') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Join Group Wait',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate(
                'Join Group Wait', bdr3_templates.bdr3_join_wait);
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'https://documentation.2ndquadrant.com/bdr3/release/latest/'
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_standby') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Promote Local Node',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate(
                'Promote Local Node',
                bdr3_templates.bdr3_promote_local_node
            );
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'https://documentation.2ndquadrant.com/bdr3/release/latest/'
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_active') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
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
                bdr3_templates.bdr3_replicate_ddl_command
            );
        }
    }, {
        text: 'Doc: BDR',
        icon: 'fas cm-all fa-globe-americas',
        action: function(node) {
            v_connTabControl.tag.createWebsiteTab(
                'Documentation: BDR',
                'https://documentation.2ndquadrant.com/bdr3/release/latest/'
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_group_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }];

  } else if (node.tag.type == 'bdr3_group') {

    return v_elements = [];

  } else if (node.tag.type == 'bdr3_group_node_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }];

  } else if (node.tag.type == 'bdr3_group_node') {

    return v_elements = [{
        text: 'Alter Node Rep Sets',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Alter Node Rep Sets', bdr3_templates.bdr3_alter_node_repsets
                .replace('#node_name#', node.text)
            );
        }
    }, {
        text: 'Part Node',
        icon: 'fas cm-all fa-times',
        action: function(node) {
            tabSQLTemplate('Part Node', bdr3_templates.bdr3_part_node
                .replace('#node_name#', node.text)
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_local_group_node') {

    return v_elements = [{
        text: 'Alter Node Rep Sets',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Alter Node Rep Sets', bdr3_templates.bdr3_alter_node_repsets
                .replace('#node_name#', node.text)
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_repset_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Create Replication Set',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Create Replication Set',
                bdr3_templates.bdr3_create_repset
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_repset') {

    return v_elements = [{
        text: 'Alter Replication Set',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Alter Replication Set',
                bdr3_templates.bdr3_alter_repset
                .replace('#repset_name#', node.text)
            );
        }
    }, {
        text: 'Drop Replication Set',
        icon: 'fas cm-all fa-times',
        action: function(node) {
            tabSQLTemplate('Drop Replication Set',
                bdr3_templates.bdr3_drop_repset
                .replace('#repset_name#', node.text)
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_repset_table_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }, {
        text: 'Add Table',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Add Table',
                bdr3_templates.bdr3_repset_add_table
                .replace('#repset_name#', node.parent
                    .text)
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_repset_table') {

    return v_elements = [{
        text: 'Remove Table',
        icon: 'fas cm-all fa-times',
        action: function(node) {
            tabSQLTemplate('Remove Table',
                bdr3_templates.bdr3_repset_remove_table
                .replace('#repset_name#', node.parent
                    .parent.text)
                .replace('#table_name#', node.text)
            );
        }
    }];

  } else if (node.tag.type == 'bdr3_subscription_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }];

  } else if (node.tag.type == 'bdr3_subscription') {

    return v_elements = [];

  } else if (node.tag.type == 'bdr3_subscription_repset_list') {

    return v_elements = [{
        text: 'Refresh',
        icon: 'fas cm-all fa-sync-alt',
        action: function(node) {
            if (node.childNodes == 0)
                refreshTreeBDR3(node);
            else {
                node.collapseNode();
                node.expandNode();
            }
        }
    }];

  } else if (node.tag.type == 'bdr3_subscription_repset') {

    return v_elements = [];

  } else if (node.tag.type == 'sequence') {

    return v_elements = [{
        text: 'Alter Sequence Kind',
        icon: 'fas cm-all fa-edit',
        action: function(node) {
            tabSQLTemplate('Alter Sequence Kind',
                bdr3_templates.bdr3_alter_seq_kind
                .replace('#seq_name#', node.text)
            );
        }
    }];

  } else {

    return v_elements = [];

  }

});

function getBDR3MajorVersion(p_version) {
    return p_version.split('.')[0]
}

function refreshTreeBDR3(node) {
  if (node.tag.type == 'database') {
    startBDR3(node);
  } else if (node.tag.type == 'bdr3_inactive_nonode' ||
             node.tag.type == 'bdr3_inactive_node' ||
             node.tag.type == 'bdr3_joining' ||
             node.tag.type == 'bdr3_standby' ||
             node.tag.type == 'bdr3_active') {
    getBDR3Properties(node);
  } else if (node.tag.type == 'bdr3_group_list') {
    getBDR3Groups(node);
  } else if (node.tag.type == 'bdr3_group_node_list') {
    getBDR3GroupNodes(node);
  } else if (node.tag.type == 'bdr3_repset_list') {
    getBDR3ReplicationSets(node);
  } else if (node.tag.type == 'bdr3_repset_table_list') {
    getBDR3ReplicationSetTables(node);
  } else if (node.tag.type == 'bdr3_subscription_list') {
    getBDR3Subscriptions(node);
  } else if (node.tag.type == 'bdr3_subscription_repset_list') {
    getBDR3SubscriptionReplicationSets(node);
  }
}

function startBDR3(node) {

  var v_loading_node = node.createChildNode('', false, 'node-spin', null,
      null);

  callPluginFunction({
    p_plugin_name: 'bdr3',
    p_function_name: 'get_bdr3_version',
    p_data: null,
    p_callback: function(p_data) {
      if (p_data.bdr3_version != null &&
          parseInt(getBDR3MajorVersion(p_data.bdr3_version)) == 3) {

            callPluginFunction({
              p_plugin_name: 'bdr3',
              p_function_name: 'get_bdr3_templates',
              p_data: null,
              p_callback: function(p_data) {
                bdr3_templates = p_data;
              },
              p_loading: false,
              p_check_database_connection: true
            });

            callPluginFunction({
              p_plugin_name: 'bdr3',
              p_function_name: 'get_bdr3_properties',
              p_data: null,
              p_callback: function(p_data) {
                v_loading_node.removeNode();
                if (!p_data[0].v_active) {

                  if (p_data[0].v_node_name == 'Not set') {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'fas node-all fa-atom', {
                            type: 'bdr3_inactive_nonode',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  } else {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'fas node-all fa-atom', {
                            type: 'bdr3_inactive_node',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  }

                } else {

                  if (p_data[0].v_state ==
                      'BDR_PEER_STATE_JOINING') {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'fas node-all fa-atom', {
                            type: 'bdr3_joining',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  } else if (p_data[0].v_state ==
                      'BDR_PEER_STATE_STANDBY') {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'fas node-all fa-atom', {
                            type: 'bdr3_standby',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  } else {

                    var node_bdr = node.createChildNode(
                        'BDR', false,
                        'fas node-all fa-atom', {
                            type: 'bdr3_active',
                        }, null);
                    node_bdr.createChildNode('', true,
                        'node-spin', null, null);

                  }

                }
              },
              p_loading: false,
              p_check_database_connection: true
            });

      }
      else {
        v_loading_node.removeNode();
      }
    },
    p_loading: false,
    p_check_database_connection: true
  });
}

function getBDR3Properties(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null,
      null);

  callPluginFunction({
    p_plugin_name: 'bdr3',
    p_function_name: 'get_bdr3_properties',
    p_data: null,
    p_callback: function(p_data) {


      if (!p_data[0].v_active) {
        if (p_data[0].v_node_name == 'Not set') {
          node.tag.type = 'bdr3_inactive_nonode';
        } else {
          node.tag.type = 'bdr3_inactive_node'
        }
      }
      else {
        if (p_data[0].v_state ==
            'BDR_PEER_STATE_JOINING') {
          node.tag.type = 'bdr3_joining';
        } else if (p_data[0].v_state ==
            'BDR_PEER_STATE_STANDBY') {
          node.tag.type = 'bdr3_standby';
        } else {
          node.tag.type = 'bdr3_active';
        }
      }

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
      node.createChildNode('Node state: ' + p_data[0]
          .v_state, false,
          'fas node-all fa-ellipsis-h node-bullet', null, null);
      v_groups = node.createChildNode('Groups',
          false,
          'fas node-all fa-object-group fas node-all fa-atom-group', {
              type: 'bdr3_group_list',
          }, null);
      v_groups.createChildNode('', true,
          'node-spin', null, null);

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

function getBDR3Groups(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null,
      null);

  callPluginFunction({
    p_plugin_name: 'bdr3',
    p_function_name: 'get_bdr3_groups',
    p_data: null,
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.setText('Groups (' + p_data.length +
          ')');

      node.tag.num_groups = p_data.length;

      for (i = 0; i < p_data.length; i++) {

          v_group = node.createChildNode(p_data[i].v_name,
              false,
              'fas node-all fa-object-group fas node-all fa-atom-group', {
                  type: 'bdr3_group',
              }, null, null);
          v_nodes = v_group.createChildNode('Nodes',
              false,
              'fas node-all fa-server fas node-all fa-atom-server', {
                  type: 'bdr3_group_node_list',
              }, null);
          v_nodes.createChildNode('', true,
              'node-spin', null, null);
          v_repsets = v_group.createChildNode(
              'Replication Sets', false,
              'fas node-all fa-tasks fas node-all fa-atom-repset', {
                  type: 'bdr3_repset_list',
              }, null);
          v_repsets.createChildNode('', true,
              'node-spin', null, null);
          v_subscriptions = v_group.createChildNode(
              'Subscriptions', false,
              'fas node-all fa-arrow-alt-circle-up fas node-all fa-atom-subscription', {
                  type: 'bdr3_subscription_list',
              }, null);
          v_subscriptions.createChildNode('', true,
              'node-spin', null, null);

      }

      node.drawChildNodes();

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

function getBDR3GroupNodes(node) {

  node.removeChildNodes();
  node.createChildNode('', false, 'node-spin', null,
      null);

  callPluginFunction({
    p_plugin_name: 'bdr3',
    p_function_name: 'get_bdr3_group_nodes',
    p_data: {"p_group": node.parent.text},
    p_callback: function(p_data) {

      if (node.childNodes.length > 0)
          node.removeChildNodes();

      node.setText('Nodes (' + p_data.length + ')');

      node.tag.num_nodes = p_data.length;

      for (i = 0; i < p_data.length; i++) {

          if (p_data[i].v_is_local) {
              v_node = node.createChildNode(p_data[i].v_name,
                  false, 'fas node-all fa-server fas node-all fa-atom-server', {
                      type: 'bdr3_local_group_node',
                  }, null, null, false);
          } else {
              v_node = node.createChildNode(p_data[i].v_name,
                  false, 'fas node-all fa-server fas node-all fa-atom-server', {
                      type: 'bdr3_group_node',
                  }, null, null, false);
          }
          v_node.createChildNode('State: ' + p_data[i]
              .v_state, false,
              'fas node-all fa-ellipsis-h node-bullet', {
              },
              null, null, false);

      }

      node.drawChildNodes();

    },
    p_loading: false,
    p_check_database_connection: true
  });

}

function getBDR3ReplicationSets(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    callPluginFunction({
      p_plugin_name: 'bdr3',
      p_function_name: 'get_bdr3_replicationsets',
      p_data: null,
      p_callback: function(p_data) {

        if (node.childNodes.length > 0)
            node.removeChildNodes();

        node.setText('Replication Sets (' + p_data.length +
            ')');

        node.tag.num_repsets = p_data.length;

        for (i = 0; i < p_data.length; i++) {

            v_node = node.createChildNode(p_data[i].v_name,
                false,
                'fas node-all fa-tasks fas node-all fa-atom-repset', {
                    type: 'bdr3_repset',
                }, null, null, false);
            v_node.createChildNode('Insert: ' + p_data[i].v_insert,
                true, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Update: ' + p_data[i].v_update,
                true, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Delete: ' + p_data[i].v_delete,
                true, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Truncate: ' + p_data[i].v_truncate,
                true, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Autoadd Tables: ' + p_data[i].v_autoadd_tables,
                true, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Autoadd Seqs: ' + p_data[i].v_autoadd_seqs,
                true, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_tables = v_node.createChildNode('Tables',
                false,
                'fas node-all fa-th node-table-list', {
                    type: 'bdr3_repset_table_list',
                }, null, null, false);
            v_tables.createChildNode('', true,
                'node-spin', null, null,
                null, false);

        }

        node.drawChildNodes();

      },
      p_loading: false,
      p_check_database_connection: true
    });

}

function getBDR3ReplicationSetTables(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    callPluginFunction({
      p_plugin_name: 'bdr3',
      p_function_name: 'get_bdr3_repset_tables',
      p_data: { "p_repset": node.parent.text },
      p_callback: function(p_data) {

        if (node.childNodes.length > 0)
            node.removeChildNodes();

        node.setText('Tables (' + p_data.length + ')');

        node.tag.num_tables = p_data.length;

        for (i = 0; i < p_data.length; i++) {

            v_node = node.createChildNode(p_data[i].v_name,
                false, 'fas node-all fa-table node-table', {
                    type: 'bdr3_repset_table',
                }, null, null, false);

        }

        node.drawChildNodes();

      },
      p_loading: false,
      p_check_database_connection: true
    });

}

function getBDR3Subscriptions(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    callPluginFunction({
      p_plugin_name: 'bdr3',
      p_function_name: 'get_bdr3_subscriptions',
      p_data: null,
      p_callback: function(p_data) {

        if (node.childNodes.length > 0)
            node.removeChildNodes();

        node.setText('Subscriptions (' + p_data.length + ')');

        node.tag.num_subs = p_data.length;

        for (i = 0; i < p_data.length; i++) {

            v_node = node.createChildNode(p_data[i].v_name,
                false, 'fas node-all fa-arrow-alt-circle-up fas node-all fa-atom-subscription', {
                    type: 'bdr3_subscription',
                }, null, null, false);
            v_node.createChildNode('Status: ' + p_data[i].v_status,
                false, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Provider: ' + p_data[i].v_origin,
                false, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Enabled: ' + p_data[i].v_enabled,
                false, 'fas node-all fa-ellipsis-h node-bullet', {
                }, null, null, false);
            v_node.createChildNode('Apply Delay: ' + p_data[i]
                .v_delay,
                false, 'fas node-all fa-ellipsis-h node-bullet',
                null, null, null, false);
            v_repsets = v_node.createChildNode('Replication Sets',
                false,
                'fas node-all fa-tasks fas node-all fa-atom-repset', {
                    type: 'bdr3_subscription_repset_list',
                }, null, null, false
            );
            v_repsets.createChildNode('', true,
                'node-spin', null, null,
                null, false);

        }

        node.drawChildNodes();

      },
      p_loading: false,
      p_check_database_connection: true
    });

}

function getBDR3SubscriptionReplicationSets(node) {

    node.removeChildNodes();
    node.createChildNode('', false, 'node-spin', null,
        null);

    callPluginFunction({
      p_plugin_name: 'bdr3',
      p_function_name: 'get_bdr3_subscription_repsets',
      p_data: { "p_sub": node.parent.text },
      p_callback: function(p_data) {

        if (node.childNodes.length > 0)
            node.removeChildNodes();

        node.setText('Replication Sets (' + p_data.length + ')');

        node.tag.num_repsets = p_data.length;

        for (i = 0; i < p_data.length; i++) {

            v_node = node.createChildNode(p_data[i].v_name,
                false,
                'fas node-all fa-tasks fas node-all fa-atom-repset', {
                    type: 'bdr3_subscription_repset',
                }, null, null, false);

        }

        node.drawChildNodes();

      },
      p_loading: false,
      p_check_database_connection: true
    });

}
