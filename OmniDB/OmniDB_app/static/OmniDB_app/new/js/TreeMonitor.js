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
function getTreeMonitor(p_div) {

  var context_menu = {
    'cm_node_root' : {
      elements : [
        {
          text : 'Refresh',
          icon: '/static/OmniDB_app/images/refresh.png',
          action : function(node) {
            if (node.childNodes==0)
              refreshTreeMonitor(node);
            else {
              node.collapseNode();
              node.expandNode();
            }
          }
        },
        {
          text : 'New Node',
          icon: '/static/OmniDB_app/images/monitoring.png',
          action : function(node) {
            newNodeSnippet(node,'node');
          }
        }
      ]
    },
    'cm_node' : {
      elements : [
        {
          text : 'Refresh',
          icon: '/static/OmniDB_app/images/refresh.png',
          action : function(node) {
            if (node.childNodes==0)
              refreshTreeSnippets(node);
            else {
              node.collapseNode();
              node.expandNode();
            }
          }
        },
        {
          text : 'New Folder',
          icon: '/static/OmniDB_app/images/folder.png',
          action : function(node) {
            newNodeSnippet(node,'node');
          }
        },
        {
          text : 'New Snippet',
          icon: '/static/OmniDB_app/images/snippet_medium.png',
          action : function(node) {
            newNodeSnippet(node,'snippet');
          }
        },
        {
          text : 'Rename Folder',
          icon: '/static/OmniDB_app/images/rename.png',
          action : function(node) {
            renameNodeSnippet(node);
          }
        },
        {
          text : 'Delete Folder',
          icon: '/static/OmniDB_app/images/tab_close.png',
          action : function(node) {
            deleteNodeSnippet(node);
          }
        }
      ]
    },
    'cm_snippet' : {
      elements : [
        {
          text : 'Edit',
          icon: '/static/OmniDB_app/images/text_edit.png',
          action : function(node) {
            startEditSnippetText(node);
          }
        },
        {
          text : 'Rename',
          icon: '/static/OmniDB_app/images/rename.png',
          action : function(node) {
            renameNodeSnippet(node);
          }
        },
        {
          text : 'Delete',
          icon: '/static/OmniDB_app/images/tab_close.png',
          action : function(node) {
            deleteNodeSnippet(node);
          }
        }
      ]
    }
  };

  var tree = createTree(p_div,'#fcfdfd',context_menu);
  tree.tag = {
  }


  tree.nodeAfterOpenEvent = function(node) {
    refreshTreeMonitor(node);
  }

  var node1 = tree.createNode('Monitoring Nodes',false,'/static/OmniDB_app/images/monitoring.png',null,{ type: 'node_root', id:null},'cm_node_root');
  node1.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

  tree.drawTree();
  v_connTabControl.selectedTab.tag.tree = tree;

}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreeMonitor(node) {
	if (node.tag!=undefined)
    if (node.tag.type=='node_root') {
      getMonitorNodes(node);
    }
}

/// <summary>
/// Retrieving monitor nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getMonitorNodes(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_monitor_nodes/',
			null,
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				for (i=0; i<p_return.v_data.length; i++) {
          var v_node = node.createChildNode(p_return.v_data[i].v_name,false,'/static/OmniDB_app/images/monitoring.png',{ type: 'node', id: p_return.v_data[i].v_id, name: p_return.v_data[i].v_name},'cm_node');
          v_node.createChildNode('DBMS: ' + p_return.v_data[i].v_technology,true,'/static/OmniDB_app/images/circle_blue.png',null,null);
          v_node.createChildNode('Server: ' + p_return.v_data[i].v_server,true,'/static/OmniDB_app/images/circle_blue.png',null,null);
          v_node.createChildNode('Port: ' + p_return.v_data[i].v_port,true,'/static/OmniDB_app/images/circle_blue.png',null,null);
          v_node.createChildNode('Database: ' + p_return.v_data[i].v_service,true,'/static/OmniDB_app/images/circle_blue.png',null,null);
          v_node.createChildNode('User: ' + p_return.v_data[i].v_user,true,'/static/OmniDB_app/images/circle_blue.png',null,null);
        }


			},
			null,
			'box',
			false);
}
