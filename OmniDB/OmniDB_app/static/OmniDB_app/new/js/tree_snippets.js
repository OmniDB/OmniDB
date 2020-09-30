/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function getAllSnippets() {
  execAjax('/get_all_snippets/',
			JSON.stringify({}),
			function(p_return) {

        v_connTabControl.tag.globalSnippets = p_return;

			},
			null,
			'box',
			false);
}

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
  v_connTabControl.snippet_tree = tree;

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

function saveSnippetText(event) {

  var v_callback = function(p_return_object) {
    v_connTabControl.snippet_tag.tabControl.selectedTab.tag.snippetObject = p_return_object;
    v_connTabControl.snippet_tag.tabControl.selectedTab.tag.tab_title_span.innerHTML = p_return_object.name;
  }

  //var v_snippet_tab_list = v_connTabControl.snippet_tag.tabControl.tabList;

  if (v_connTabControl.snippet_tag.tabControl.selectedTab.tag.snippetObject.id != null) {
    var v_save_object = {
      v_id: v_connTabControl.snippet_tag.tabControl.selectedTab.tag.snippetObject.id,
      v_name : v_connTabControl.snippet_tag.tabControl.selectedTab.tag.snippetObject.name,
      v_parent : v_connTabControl.snippet_tag.tabControl.selectedTab.tag.snippetObject.parent
    }
    saveSnippetTextConfirm(
      v_save_object,
      v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.getValue(),
      v_callback
    )
  }
  else {
    customMenu(
      {
        x:event.clientX+5,
        y:event.clientY+5
      },
      buildSnippetContextMenuObjects('save',
                                     v_connTabControl.tag.globalSnippets,
                                     v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor,
                                     v_callback
                                   ),
      null
    );


  }
}

function snippetTreeFindNode(p_id, p_current_node) {
  var v_node = null;

  for (var i=0; i < p_current_node.childNodes.length; i++) {
    if (p_current_node.childNodes[i].tag.id == p_id)
      return p_current_node.childNodes[i];
    else {
      v_node = snippetTreeFindNode(p_id, p_current_node.childNodes[i]);
      if (v_node!=null)
        return v_node;
    }
  }
  return v_node;
}

function saveSnippetTextConfirm(p_save_object, p_text, p_callback) {
  execAjax('/save_snippet_text/',
     JSON.stringify({"p_id": p_save_object.v_id,
                     "p_parent": p_save_object.v_parent,
                     "p_name": p_save_object.v_name,
                     "p_text": p_text}),
     function(p_return) {
       var v_node = null;
       if (p_return.v_data.parent==null) {
         v_node = v_connTabControl.snippet_tree.childNodes[0];
       }
       else {
         v_node = snippetTreeFindNode(p_return.v_data.parent, v_connTabControl.snippet_tree.childNodes[0]);
       }

       if (v_node!=null) {
         if (v_node.childNodes==0)
           refreshTreeSnippets(v_node);
         else {
           v_node.collapseNode();
           v_node.expandNode();
         }
       }

      if (p_callback!=null)
        p_callback(p_return.v_data);

      showAlert('Snippet saved.')

      getAllSnippets();
     },
     null,
     'box');


}

function newNodeSnippet(p_node,p_mode) {
  var v_placeholder = 'Snippet Name';
  if (p_mode=='node')
    v_placeholder = 'Node Name';

  showConfirm('<input id="element_name"/ class="form-control" placeholder="' + v_placeholder + '" style="width: 100%;">',
	            function() {
                     execAjax('/new_node_snippet/',
                   			JSON.stringify({"p_sn_id_parent": p_node.tag.id,
                                        "p_mode": p_mode,
                                        "p_name": document.getElementById('element_name').value}),
                   			function(p_return) {
                           refreshTreeSnippets(p_node);

                           getAllSnippets();
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

  showConfirm('<input id="element_name"/ class="form-control" value="' + p_node.text + '" style="width: 100%;">',
	            function() {
                     execAjax('/rename_node_snippet/',
                   			JSON.stringify({"p_id": p_node.tag.id,
                                        "p_mode": p_node.tag.type,
                                        "p_name": document.getElementById('element_name').value}),
                   			function(p_return) {
                           refreshTreeSnippets(p_node.parent);

                           getAllSnippets();
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

                           getAllSnippets();
                   			},
                   			null,
                   			'box');

	            });
}

function startEditSnippetText(p_node) {
  // Checking if there is a tab for this snippet.
  var v_snippet_tab_list = v_connTabControl.snippet_tag.tabControl.tabList;
  var v_avaiable_tab = false;
  for (let i = 0; i < v_snippet_tab_list.length; i++) {
    var v_snippet_tab_snippet_object = v_snippet_tab_list[i].tag.snippetObject;
    if (typeof v_snippet_tab_snippet_object === 'object') {
      if (v_snippet_tab_snippet_object.id === p_node.tag.id) {
        v_avaiable_tab = v_snippet_tab_list[i];
      }
    }
  }

  if (v_avaiable_tab) {
    v_connTabControl.snippet_tag.tabControl.selectTab(v_avaiable_tab);
  }
  else {
    v_connTabControl.tag.createSnippetTextTab(p_node.tag);
  }

  execAjax('/get_snippet_text/',
			JSON.stringify({"p_st_id": p_node.tag.id}),
			function(p_return) {
        v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.setValue(p_return.v_data);
        v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.clearSelection();
        v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);

			},
			null,
			'box');
}

function executeSnippet(p_id,p_editor) {
	execAjax('/get_snippet_text/',
			JSON.stringify({"p_st_id": p_id}),
			function(p_return) {
				p_editor.insert(p_return.v_data);
				p_editor.clearSelection();
			},
			null,
			'box');
}

function buildSnippetContextMenuObjects(p_mode, p_object, p_editor, p_callback) {

  var v_elements = [];

  if (p_mode == 'save') {
    v_elements.push(
      {
        text: 'New Snippet',
        icon: 'fas cm-all fa-save',
        action: function() {
          showConfirm('<input id="element_name"/ class="form-control" placeholder="Snippet Name" style="width: 100%;">',
        	            function() {
                        saveSnippetTextConfirm(
                          {
                            v_id: null,
                            v_name : document.getElementById('element_name').value,
                            v_parent: p_object.id
                          },
                          p_editor.getValue(),
                          p_callback
                        );
        	            });
        }
      }
    );
  }

  for (var i=0; i<p_object.files.length; i++) (function(i){
    var v_file = p_object.files[i];

    if (p_mode == 'save')
      v_elements.push(
        {
          text: '<b>OVERWRITE</b> ' + v_file.name,
          icon: 'fas cm-all fa-align-left',
          action: function() {
            showConfirm("<b>WARNING</b>, are you sure you want to overwrite file '" + v_file.name + "'?",
          	            function() {
                          saveSnippetTextConfirm(
                            {
                              v_id: v_file.id,
                              v_name : null,
                              v_parent: null
                            },
                            p_editor.getValue(),
                            p_callback
                          );
          	            });
          }
        }
      );
    else
      v_elements.push(
        {
          text: v_file.name,
          icon: 'fas cm-all fa-align-left',
          action: function() {
              executeSnippet(v_file.id, p_editor)
          }
        }
      );
  })(i);

  for (var i=0; i<p_object.folders.length; i++) (function(i){
    var v_folder = p_object.folders[i];
    v_elements.push(
      {
        text: v_folder.name,
        icon: 'fas cm-all fa-folder',
        submenu: {
          elements: buildSnippetContextMenuObjects(p_mode, v_folder, p_editor, p_callback)
        }
      }
    );
  })(i);

  return v_elements;
}
