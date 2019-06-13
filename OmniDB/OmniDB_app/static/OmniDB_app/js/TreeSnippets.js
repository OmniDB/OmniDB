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
function getTreeSnippets(p_div) {

  var context_menu = {
    'cm_node_root' : {
      elements : [
        {
          text : 'Refresh',
          icon: 'fas cm-all fa-sync-alt',
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
          icon: 'fas cm-all fa-folder',
          action : function(node) {
            newNodeSnippet(node,'node');
          }
        },
        {
          text : 'New Snippet',
          icon: 'fas cm-all fa-align-left',
          action : function(node) {
            newNodeSnippet(node,'snippet');
          }
        }
      ]
    },
    'cm_node' : {
      elements : [
        {
          text : 'Refresh',
          icon: 'fas cm-all fa-sync-alt',
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
          icon: 'fas cm-all fa-folder',
          action : function(node) {
            newNodeSnippet(node,'node');
          }
        },
        {
          text : 'New Snippet',
          icon: 'fas cm-all fa-align-left',
          action : function(node) {
            newNodeSnippet(node,'snippet');
          }
        },
        {
          text : 'Rename Folder',
          icon: 'fas cm-all fa-edit',
          action : function(node) {
            renameNodeSnippet(node);
          }
        },
        {
          text : 'Delete Folder',
          icon: 'fas cm-all fa-times',
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
          icon: 'fas cm-all fa-edit',
          action : function(node) {
            startEditSnippetText(node);
          }
        },
        {
          text : 'Rename',
          icon: 'fas cm-all fa-edit',
          action : function(node) {
            renameNodeSnippet(node);
          }
        },
        {
          text : 'Delete',
          icon: 'fas cm-all fa-times',
          action : function(node) {
            deleteNodeSnippet(node);
          }
        },
        {
          text : 'Run Snippet',
          icon: 'fas cm-all fa-play',
          submenu : {
            elements: function(node) { return getOpenedConnTabs(node) }
          }
        }
      ]
    }
  };

  var tree = createTree(p_div,'#fcfdfd',context_menu);
  tree.tag = {
  }


  tree.nodeAfterOpenEvent = function(node) {
    refreshTreeSnippets(node);
  }

  var node1 = tree.createNode('Snippets',false,'fas node-all fa-list-alt node-snippet-list',null,{ type: 'node', id:null},'cm_node_root');
  node1.createChildNode('',true,'node-spin',null,null);

  tree.drawTree();
  v_connTabControl.selectedTab.tag.tree = tree;

}

/// <summary>
/// Refreshing tree node.
/// </summary>
/// <param name="node">Node object.</param>
function refreshTreeSnippets(node) {
	if (node.tag!=undefined)
    if (node.tag.type=='node') {
      getChildSnippetNodes(node);
    }
}

/// <summary>
/// Retrieving snippet nodes.
/// </summary>
/// <param name="node">Node object.</param>
function getChildSnippetNodes(node) {

	node.removeChildNodes();
	node.createChildNode('',false,'node-spin',null,null);


	execAjax('/get_node_children/',
			JSON.stringify({"p_sn_id_parent": node.tag.id}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				for (i=0; i<p_return.v_data.v_list_nodes.length; i++) {
          var v_node = node.createChildNode(p_return.v_data.v_list_nodes[i].v_name,false,'fas node-all fa-folder node-snippet-folder',{ type: 'node', id: p_return.v_data.v_list_nodes[i].v_id, id_parent: node.tag.id, name: p_return.v_data.v_list_nodes[i].v_name},'cm_node');
          v_node.createChildNode('',true,'node-spin',null,null);
        }

        for (i=0; i<p_return.v_data.v_list_texts.length; i++) {
          var v_node = node.createChildNode(p_return.v_data.v_list_texts[i].v_name,false,'fas node-all fa-align-left node-snippet-snippet',{ type: 'snippet', id: p_return.v_data.v_list_texts[i].v_id, id_parent: node.tag.id, name: p_return.v_data.v_list_texts[i].v_name},'cm_snippet');
          v_node.doubleClickNodeEvent = function(p_node) {
            startEditSnippetText(p_node);
          }
        }

			},
			null,
			'box',
			false);
}

/// <summary>
/// Removes tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function closeSnippetTab(p_tab) {

  p_tab.removeTab();
  if (p_tab.tag.ht!=null) {
  	p_tab.tag.ht.destroy();
  	p_tab.tag.div_result.innerHTML = '';
  }

  if (p_tab.tag.editor!=null)
  	p_tab.tag.editor.destroy();

}

function saveSnippetText() {
  if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.snippetObject) {
    var v_save_object = {
      v_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.snippetObject.id,
      v_name : v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.snippetObject.name
    }
    saveSnippetTextConfirm(v_save_object)
  }
  else {
    showConfirm('<input id="element_name"/ placeholder="Snippet Name" style="width: 200px;">',
  	            function() {
                  var v_save_object = {
                    v_id: null,
                    v_name : document.getElementById('element_name').value
                  }
                  saveSnippetTextConfirm(v_save_object)
  	            });

    var v_input = document.getElementById('element_name');
  	v_input.onkeydown = function() {
  		if (event.keyCode == 13)
  			document.getElementById('button_confirm_ok').click();
  		else if (event.keyCode == 27)
  			document.getElementById('button_confirm_cancel').click();
  	}
    v_input.focus();
  }
}

function saveSnippetTextConfirm(p_save_object) {
  execAjax('/save_snippet_text/',
     JSON.stringify({"p_id": p_save_object.v_id,
                     "p_name": p_save_object.v_name,
                     "p_text": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue()}),
     function(p_return) {
        if (p_save_object.v_id==null) {
          var node = v_connTabControl.selectedTab.tag.tree.childNodes[0];
          if (node.childNodes==0)
            refreshTreeSnippets(node);
          else {
            node.collapseNode();
            node.expandNode();
          }
        }
        showAlert('Snippet saved.')
     },
     null,
     'box');


}

function newNodeSnippet(p_node,p_mode) {
  var v_placeholder = 'Snippet Name';
  if (p_mode=='node')
    v_placeholder = 'Node Name';

  showConfirm('<input id="element_name"/ placeholder="' + v_placeholder + '" style="width: 200px;">',
	            function() {
                     execAjax('/new_node_snippet/',
                   			JSON.stringify({"p_sn_id_parent": p_node.tag.id,
                                        "p_mode": p_mode,
                                        "p_name": document.getElementById('element_name').value}),
                   			function(p_return) {
                           refreshTreeSnippets(p_node);
                   			},
                   			null,
                   			'box');

	            });

  var v_input = document.getElementById('element_name');
	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('button_confirm_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('button_confirm_cancel').click();
	}
}

function renameNodeSnippet(p_node) {

  showConfirm('<input id="element_name"/ value="' + p_node.text + '" style="width: 200px;">',
	            function() {
                     execAjax('/rename_node_snippet/',
                   			JSON.stringify({"p_id": p_node.tag.id,
                                        "p_mode": p_node.tag.type,
                                        "p_name": document.getElementById('element_name').value}),
                   			function(p_return) {
                           refreshTreeSnippets(p_node.parent);
                   			},
                   			null,
                   			'box');

	            });

  var v_input = document.getElementById('element_name');
	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('button_confirm_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('button_confirm_cancel').click();
	}
}

function deleteNodeSnippet(p_node) {

  showConfirm('Are you sure you want to delete this ' + p_node.tag.type + '?',
	            function() {
                     execAjax('/delete_node_snippet/',
                   			JSON.stringify({"p_id": p_node.tag.id,
                                        "p_mode": p_node.tag.type}),
                   			function(p_return) {
                           refreshTreeSnippets(p_node.parent);
                   			},
                   			null,
                   			'box');

	            });
}

function startEditSnippetText(p_node) {
  v_connTabControl.tag.createSnippetTextTab(p_node.tag.name);
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.snippetObject = p_node.tag;
  execAjax('/get_snippet_text/',
			JSON.stringify({"p_st_id": p_node.tag.id}),
			function(p_return) {
        v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(p_return.v_data);
        v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
        v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);

			},
			null,
			'box');
}

function executeSnippet(p_node,p_tab) {
	execAjax('/get_snippet_text/',
			JSON.stringify({"p_st_id": p_node.tag.id}),
			function(p_return) {
				v_connTabControl.selectTab(p_tab);
				v_connTabControl.tag.createQueryTab();
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(p_return.v_data);
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
			},
			null,
			'box');
}
