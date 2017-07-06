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
    refreshTreeSnippets(node);
  }

  var node1 = tree.createNode('Snippets',false,'/static/OmniDB_app/images/circle_blue.png',null,{ type: 'node', id:null},'cm_node_root');
  node1.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);

  tree.drawTree();

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
	node.createChildNode('',false,'/static/OmniDB_app/images/spin.svg',null,null);


	execAjax('/get_node_children/',
			JSON.stringify({"p_sn_id_parent": node.tag.id}),
			function(p_return) {

				if (node.childNodes.length > 0)
					node.removeChildNodes();

				for (i=0; i<p_return.v_data.v_list_nodes.length; i++) {
          var v_node = node.createChildNode(p_return.v_data.v_list_nodes[i].v_name,false,'/static/OmniDB_app/images/folder.png',{ type: 'node', id: p_return.v_data.v_list_nodes[i].v_id, id_parent: node.tag.id, name: p_return.v_data.v_list_nodes[i].v_name},'cm_node');
          v_node.createChildNode('',true,'/static/OmniDB_app/images/spin.svg',null,null);
        }

        for (i=0; i<p_return.v_data.v_list_texts.length; i++) {
          var v_node = node.createChildNode(p_return.v_data.v_list_texts[i].v_name,false,'/static/OmniDB_app/images/snippet_medium.png',{ type: 'snippet', id: p_return.v_data.v_list_texts[i].v_id, id_parent: node.tag.id, name: p_return.v_data.v_list_texts[i].v_name},'cm_snippet');
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

	showConfirm('Are you sure you want to close this snippet?',
                function() {
                	p_tab.removeTab();
                	if (p_tab.tag.ht!=null) {
						p_tab.tag.ht.destroy();
						p_tab.tag.div_result.innerHTML = '';
					}

					if (p_tab.tag.editor!=null)
						p_tab.tag.editor.destroy();
                });

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
  }
}

function saveSnippetTextConfirm(p_save_object) {
  execAjax('/save_snippet_text/',
     JSON.stringify({"p_id": p_save_object.v_id,
                     "p_name": p_save_object.v_name,
                     "p_text": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue()}),
     function(p_return) {
        //if (p_save_object.v_id==null)
        //refreshTreeSnippets(p_node);
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
