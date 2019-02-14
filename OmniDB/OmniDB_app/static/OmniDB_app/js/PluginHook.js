/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/*
# Plugin API

## Javascript functions

- ```activateHook(p_hook, p_function)```
  - **DESCRIPTION**: Enables a specific hook.
  - **PARAMETERS**:
    - p_hook: the name of hook to be activated.
    - p_function: the function to be called whenever that hook is triggered. Depending on the hook, this function is called with specific arguments and expects a specific returning value.
  - **AVAILABLE HOOKS**:
    - innerTabMenu: Used to insert custom options in the + internal tab.
      - **MUST RETURN**: List of menu itens (Check test_plugin for example).
    - outerTabMenu: Used to insert custom options in the + external tab.
      - **MUST RETURN**: List of menu itens (Check test_plugin for example).
    - windowResize: Called every time window is resized, including when internal objects are resized
    - changeTheme: Called when theme is changed.
      - **PARAMETERS**:
        - p_editor_theme: The name of the new selected theme.
        - p_theme_type: The type of the new theme (dark or light).
    - postgresqlTreeNodeOpen: After opening a postgresql tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - postgresqlTreeContextMenu: Used to insert custom options in the current postgresql tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
      - **MUST RETURN**: List of menu itens (Check test_plugin for example).
    - postgresqlTreeNodeClick: After clicking on postgresql tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - oracleTreeNodeOpen: After opening a oracle tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - oracleTreeContextMenu: Used to insert custom options in the current oracle tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
      - **MUST RETURN**: List of menu itens (Check test_plugin for example).
    - oracleTreeNodeClick: After clicking on oracle tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - mysqlTreeNodeOpen: After opening a mysql tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - mysqlTreeContextMenu: Used to insert custom options in the current mysql tree node.
      - **MUST RETURN**: List of menu itens (Check test_plugin for example).
    - mysqlTreeNodeClick: After clicking on mysql tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - mariadbTreeNodeOpen: After opening a mariadb tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
    - mariadbTreeContextMenu: Used to insert custom options in the current mariadb tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.
      - **MUST RETURN**: List of menu itens (Check test_plugin for example).
    - mariadbTreeNodeClick: After clicking on mariadb tree node.
      - **PARAMETERS**:
        - p_node: Tree node object.

- ```p_node.createChildNode(p_text,p_expanded,p_icon,p_tag)```
  - **DESCRIPTION**: Creates a child node in the current node. This function is supposed to be called with hooks that contain p_node as parameter.
  - **PARAMETERS**:
    - p_text: node text.
    - p_expanded: whether to expand the node when creating it. This is useful when creating childs of childs.
    - p_icon: path of an image to be used in the tab title. Use together with getPluginPath() to get the correct relative path.
    - p_tag: sets a tag for the child node. This is useful to create custom attributes that will be used to identify this node when other hooks are triggered.

- ```callPluginFunction({ p_plugin_name: '', p_function_name: '', p_data: null, p_callback: null, p_loading: true, p_check_database_connection: true })```
  - **DESCRIPTION**: Asynchronously calls a specific python function of a specific plugin (python backend).
  - **PARAMETERS**:
    - p_plugin_name: the name of the plugin.
    - p_function_name: the name of the function being called.
    - p_data: data to be sent to the python function.
    - p_callback: javascript function to be called when the function ends.
    - p_loading: whether to show the loading image.
    - p_check_database_connection: whether to check if the database connection is working before calling the python function.

- ```createInnerTab({ p_name: '', p_image: '', p_select_function: null, p_before_close_function: null })```
  - **DESCRIPTION**: Creates an internal blank tab.
  - **PARAMETERS**:
    - p_name: the name of the tab.
    - p_image: path of an image to be used in the tab title. Use together with getPluginPath() to get the correct relative path.
    - p_select_function: function to be called whenever the tab is selected.
    - p_before_close_function: function to be called before the tab is closed.
  - **RETURNS**: tab object tag.

- ```createOuterTab({ p_name: '', p_image: '', p_select_function: null, p_before_close_function: null })```
  - **DESCRIPTION**: Creates an external blank tab.
  - **PARAMETERS**:
    - p_name: the name of the tab.
    - p_image: path of an image to be used in the tab title. Use together with getPluginPath() to get the correct relative path.
    - p_select_function: function to be called whenever the tab is selected.
    - p_before_close_function: function to be called before the tab is closed.
  - **RETURNS**: tab object tag.

- ```getSelectedInnerTabTag()```
  - **DESCRIPTION**: Gets the tag of the selected internal tab, allowing to store information there.
  - **RETURNS**: Selected internal tab tag.

- ```getSelectedOuterTabTag()```
  - **DESCRIPTION**: Gets the tag of the selected external tab, allowing to store information there.
  - **RETURNS**: Selected external tab tag.

- ```createSQLTab({ p_name: '', p_template: '', p_show_tip: true })```
  - **DESCRIPTION**: Creates an internal Query Tab with a specific SQL passed as a parameter.
  - **PARAMETERS**:
    - p_name: the name of the tab.
    - p_template: the SQL to be filled in the editor.
    - p_show_tip: whether to show a tip with the message "Adjust command and run!"

- ```getPluginPath(p_plugin_name)```
  - **DESCRIPTION**: Get the path of the specific plugin to use reference static files.
  - **PARAMETERS**:
    - p_plugin_name: the name of the plugin.

- ```showError(p_message)```
  - **DESCRIPTION**: Shows a popup with the specific error message.

- ```setDDL({ p_ddl: '', p_select: true})```
  - **DESCRIPTION**: Sets the content of the DDL box in the DDL tab.
  - **PARAMETERS**:
    - p_ddl: the DDL to be filled in the editor.
    - p_select: whether to also select the DDL tab.

- ```setProperties({ p_properties: [], p_select: true})```
  - **DESCRIPTION**: Sets the content of the Properties grid in the Properties tab.
  - **PARAMETERS**:
    - p_properties: the properties to be displayed in the grid. This is a list of lists.
    - p_select: whether to also select the Properties tab.

## Python side

Plugins on the python side are implemented as user defined functions that will be called by
the javascript API function `callPluginFunction()`. The functions are called always
with 2 parameters:

- ```my_python_function(p_database_object, p_data)```
  - **PARAMETERS**:
    - p_database_object: OmniDB's database object that contains several attributes
    and functions to retrieve data from the database.
    - p_data: optional paramater to send data from the javascript side.

*/
var v_plugins = {}

$(function () {
  v_connTabControl.tag.hooks = {
    innerTabMenu: [],
    outerTabMenu: [],
    windowResize: [],
    changeTheme: [],
    postgresqlTreeNodeOpen: [],
    postgresqlTreeContextMenu: [],
    postgresqlTreeNodeClick: [],
    oracleTreeNodeOpen: [],
    oracleTreeContextMenu: [],
    oracleTreeNodeClick: [],
    mysqlTreeNodeOpen: [],
    mysqlTreeContextMenu: [],
    mysqlTreeNodeClick: [],
    mariadbTreeNodeOpen: [],
    mariadbTreeContextMenu: [],
    mariadbTreeNodeClick: []
  }

  execAjax('/get_plugins/',
			JSON.stringify({}),
			function(p_return) {
        var timestamp = new Date().getTime();
        for (var i=0; i<p_return.v_data.length; i++) {

          // loading CSS
          if (p_return.v_data[i].cssfile) {
            var importedcss = document.createElement('link');
            importedcss.rel = 'stylesheet';
            importedcss.href = p_return.v_data[i].cssfile + '?v' + timestamp;
            document.head.appendChild(importedcss);
          }

          // loading JS
          var importedjs = document.createElement('script');
          importedjs.src = p_return.v_data[i].file + '?v' + timestamp;
          document.head.appendChild(importedjs);

          v_plugins[p_return.v_data[i].name] = p_return.v_data[i];
        }

			},
			null,
			'box');

});

var csrftoken = getCookie('omnidb_csrftoken');

function upload(p_file_selector) {

var formData = new FormData();
formData.append('file', p_file_selector.files[0]);
p_file_selector.value = null;
startLoading();
$.ajax({
    url: '/upload/',
    type: 'POST',
		beforeSend: function(xhr, settings) {
			if(!csrfSafeMethod(settings.type) && !this.crossDomain) {
				xhr.setRequestHeader("X-CSRFToken", csrftoken);
			}
		},
    data: formData,
    cache: false,
    processData: false,
    contentType: false,
    success: function(data) {
        if (!data.v_error) {
          showAlert('Plugin successfully installed, please restart OmniDB.');
          showPlugins();
        }
        else
        {
          showError(data.v_message);
        }
        endLoading();
    },
    error: function(msg) {
			endLoading();
		}
});
return false;
}

function activateHook(p_hook,p_function) {
  try {
    v_connTabControl.tag.hooks[p_hook].push(p_function);
  }
  catch(err) {
  }
}

function reloadPlugins() {
  showConfirm('This operation will reload all plugins, are you sure you want to continue?',
              function() {
                execAjax('/reload_plugins/',
              			JSON.stringify({}),
              			function(p_return) {
                      showPlugins();
                      showAlert('Plugins reloaded, please reload this page to reload client changes.<br><br><button onclick="location.reload();">Reload now</button>')
              			},
              			null,
              			'box');

              });

}

function getPluginPath(p_name) {
  try {
    if (p_name == 'OmniDB') {
      return '/static/OmniDB_app/'
    } else {
      return v_plugins[p_name].folder;
    }
  }
  catch(err) {
    return ''
  }
}

function hidePlugins() {
  document.getElementById('div_plugins').classList.remove('isActive');
  v_connTabControl.tag.plugin_ht.destroy();
  v_connTabControl.tag.plugin_ht = null;
}

function deletePlugin(p_plugin_name,p_plugin_folder) {
  showConfirm('Are you sure you want to delete the following plugin? You will have to restart OmniDB after this operation.',
  function() {
    execAjax('/delete_plugin/',
  			JSON.stringify({'p_plugin_name': p_plugin_name, "p_plugin_folder": p_plugin_folder}),
  			function(p_return) {
          showAlert(p_return.v_data);
          showPlugins();
        },
        null,
        'box');
  })
}

function showPlugins() {

  document.getElementById('div_plugins').classList.add('isActive');

	execAjax('/list_plugins/',
			JSON.stringify({}),
			function(p_return) {

				var columnProperties = [];

				var col = new Object();

				var col = new Object();
				col.title =  'Folder';
				col.width = '80';
        col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Plugin Name';
        col.width = '100';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Version';
        col.width = '60';
        col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Config file';
        col.width = '70';
        col.readOnly = true;
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Javascript File';
        col.width = '80';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Python File';
        col.width = '80';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'CSS File';
        col.width = '60';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Status';
        col.width = '50';
        col.readOnly = true;
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Actions';
        col.width = '50';
        col.readOnly = true;
				columnProperties.push(col);

				var v_div_result = document.getElementById('plugin_grid');
        v_connTabControl.tag.plugin_message_list = p_return.v_data.message;

				if (v_div_result.innerHTML!='') {
					v_connTabControl.tag.plugin_ht.destroy();
				}

				v_connTabControl.tag.plugin_ht = new Handsontable(v_div_result,
														{
															data: p_return.v_data.list,
															columns : columnProperties,
															colHeaders : true,
															manualColumnResize: true,
															minSpareCols :0,
															minSpareRows :0,
															fillHandle:false,
															cells: function (row, col, prop) {

																var cellProperties = {};
																cellProperties.renderer = grayHtmlRenderer;

																return cellProperties;

															}
														});

				},
				null,
				'box');
}

function getPluginMessage() {
  var v_row = v_connTabControl.tag.plugin_ht.getSelected()[0][0];
  if (v_connTabControl.tag.plugin_message_list[v_row]!='')
    showError(v_connTabControl.tag.plugin_message_list[v_row])
}

////////////////////////////////////////////////////////////////////////////////

function callPluginFunction({ p_plugin_name, p_function_name, p_data = null, p_callback = null, p_loading = true, p_check_database_connection = true }) {
  var v_database_index = null;
  if (v_connTabControl.selectedTab.tag.selectedDatabaseIndex)
    v_database_index = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
  execAjax('/exec_plugin_function/',
      JSON.stringify({'p_plugin_name': p_plugin_name,
                      'p_function_name': p_function_name,
                      'p_data': p_data,
                      'p_database_index': v_database_index,
                      'p_tab_id': v_connTabControl.selectedTab.id,
                      'p_check_database_connection': p_check_database_connection
                    }),
      function(p_return) {
        p_callback(p_return.v_data);
      },
      function(p_return) {
        if (p_return.v_data.password_timeout) {
            showPasswordPrompt(
                v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                function() {
                    callPluginFunction({ p_plugin_name, p_function_name, p_data, p_callback, p_loading, p_check_database_connection })
                },
                null,
                p_return.v_data.message
            );
        } else {
            showError(p_return.v_data);
        }
      },
      'box',
      p_loading);
}

function createSQLTab({ p_name = '', p_template = '', p_show_tip = true }) {
  tabSQLTemplate(p_name, p_template, p_show_tip);
}

function createInnerTab({ p_name = '', p_image = '', p_select_function = null, p_before_close_function = null }) {
  v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
    '<i class="' + p_image + ' icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i>',
    false,
    null,
    null,
    null,
    null,
    true,
    function() {
      if(p_select_function != null) {
        p_select_function();
      }
    });
    v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);
    var v_tab_title_span = document.getElementById('tab_title');
    v_tab_title_span.id = 'tab_title_' + v_tab.id;
    var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          if(p_before_close_function != null) {
            p_before_close_function();
          }
          v_current_tab.removeTab();
        });
		};
    var v_div = document.getElementById('div_' + v_tab.id);
    v_div.style.height = 'calc(100% - 137px)';
    v_tab.tag = {
      mode: '',
      div: v_div
    };
    var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab('+',false,function(e) {showMenuNewTab(e); },null,null,null,null,null,false);
    return v_tab.tag;
}

function getSelectedInnerTabTag() {
  return v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
}

function getSelectedOuterTabTag() {
  return v_connTabControl.selectedTab.tag;
}

function createOuterTab({ p_name = '', p_image = '', p_select_function = null, p_before_close_function = null }) {
  v_connTabControl.removeTabIndex(v_connTabControl.tabList.length-1);
  var v_tab = v_connTabControl.createTab(
    '<i class="' + p_image + ' icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span><i title="Close" id="tab_close" class="fas fa-times tab-icon icon-close"></i>',
    false,
    null,
    null,
    null,
    null,
    true,
    function() {
      if(p_select_function != null) {
        p_select_function();
      }
    });
    v_connTabControl.selectTab(v_tab);
    var v_tab_title_span = document.getElementById('tab_title');
    v_tab_title_span.id = 'tab_title_' + v_tab.id;
    var v_tab_close_span = document.getElementById('tab_close');
		v_tab_close_span.id = 'tab_close_' + v_tab.id;
		v_tab_close_span.onclick = function(e) {
      var v_current_tab = v_tab;
      beforeCloseTab(e,
        function() {
          if(p_before_close_function != null) {
            p_before_close_function();
          }
          v_current_tab.removeTab();
        });
		};
    var v_div = document.getElementById('div_' + v_tab.id);
    v_div.style.height = 'calc(100% - 86px)';
    v_tab.tag = {
      mode: '',
      div: v_div
    };
    v_connTabControl.createTab('+',false,function(e) {showMenuNewTabOuter(e); },null,null,null,null,null,false);
    return v_tab.tag;
}

function setDDL({ p_ddl = '', p_select = true}) {
  if (v_connTabControl.selectedTab.tag.mode=='connection') {
    var v_tab_tag = v_connTabControl.selectedTab.tag;
    v_tab_tag.ddlEditor.setValue(p_ddl);
    v_tab_tag.ddlEditor.clearSelection();
    v_tab_tag.ddlEditor.gotoLine(0, 0, true);
    if (p_select) {
      v_connTabControl.selectedTab.tag.selectDDLTabFunc();
    }
  }
}

function setProperties({ p_properties = [], p_select = true}) {
  if (v_connTabControl.selectedTab.tag.mode=='connection') {
    var v_tab_tag = v_connTabControl.selectedTab.tag;
    v_tab_tag.gridProperties.loadData(p_properties);
    if (p_select) {
      v_connTabControl.selectedTab.tag.selectPropertiesTabFunc();
    }
  }
}
