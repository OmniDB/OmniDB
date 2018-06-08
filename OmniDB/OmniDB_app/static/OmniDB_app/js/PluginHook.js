/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

//Plugin API functions

//activateHook(): enables a specific hook
// ** AVAILABLE HOOKS **
// innerTabMenu: Used to insert custom options in the + internal tab
// outerTabMenu: Used to insert custom options in the + external tab
// windowResize: Called every time window is resized, including when internal objects are resized
// changeTheme: Called when theme is changed
// postgresqlTreeNodeOpen: After opening a postgresql tree node
// postgresqlTreeContextMenu: Used to insert custom options in the current postgresql tree node
// postgresqlTreeNodeClick: After clicking on postgresql tree node
// oracleTreeNodeOpen: After opening a oracle tree node
// oracleTreeContextMenu: Used to insert custom options in the current oracle tree node
// oracleTreeNodeClick: After clicking on oracle tree node
// mysqlTreeNodeOpen: After opening a mysql tree node
// mysqlTreeContextMenu: Used to insert custom options in the current mysql tree node
// mysqlTreeNodeClick: After clicking on mysql tree node
// mariadbTreeNodeOpen: After opening a mariadb tree node
// mariadbTreeContextMenu: Used to insert custom options in the current mariadb tree node
// mariadbTreeNodeClick: After clicking on mariadb tree node

//callPluginFunction(): calls a specific function of a specific plugin (python backend)

//createInnerTab(): creates an internal blank tab

//createOuterTab(): creates an external blank tab

//getSelectedInnerTabTag(): gets the tag of the selected internal tab, allowing to store information there

//getSelectedOuterTabTag(): gets the tag of the selected external tab, allowing to store information there

//tabSQLTemplate(): creates an internal Query Tab with a specific SQL passed as a parameter

//getPluginPath(): get the path of the specific plugin to use reference static files

//showError(): shows a popup with the specific error message

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
        for (var i=0; i<p_return.v_data.length; i++) {
          var imported = document.createElement('script');
          imported.src = p_return.v_data[i].file;
          document.head.appendChild(imported);
          v_plugins[p_return.v_data[i].name] = p_return.v_data[i]
        }

			},
			null,
			'box');

});

function activateHook(p_hook,p_function) {
  try {
    v_connTabControl.tag.hooks[p_hook].push(p_function);
  }
  catch(err) {
  }
}

function getPluginPath(p_name) {
  try {
    return v_plugins[p_name].folder;
  }
  catch(err) {
    return ''
  }
}

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

function createInnerTab({ p_name = '', p_image = '', p_select_function = null, p_before_close_function = null }) {
  v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
    '<img src="' + p_image + '"/><span id="tab_title"> ' + p_name + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
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
    '<img src="' + p_image + '"/><span id="tab_title"> ' + p_name + '</span><span title="Close" id="tab_close"><img src="/static/OmniDB_app/images/tab_close.png"/></span>',
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

function hidePlugins() {
  document.getElementById('div_plugins').style.display = 'none';
  v_connTabControl.tag.plugin_ht.destroy();
  v_connTabControl.tag.plugin_ht = null;
}

function showPlugins() {

  document.getElementById('div_plugins').style.display = 'block';

	execAjax('/list_plugins/',
			JSON.stringify({}),
			function(p_return) {

				var columnProperties = [];

				var col = new Object();

				var col = new Object();
				col.title =  'Folder';
				col.width = '120'
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Plugin Name';
        col.width = '120'
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Version';
        col.width = '60'
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Config file';
        col.width = '80'
				columnProperties.push(col);

				var col = new Object();
				col.title =  'Javascript File';
        col.width = '80'
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Python File';
        col.width = '80'
				columnProperties.push(col);

        var col = new Object();
				col.title =  'Enabled';
        col.width = '50'
				columnProperties.push(col);

				var v_div_result = document.getElementById('plugin_grid');

				if (v_div_result.innerHTML!='') {
					v_connTabControl.tag.plugin_ht.destroy();
				}

				v_connTabControl.tag.plugin_ht = new Handsontable(v_div_result,
														{
															data: p_return.v_data,
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
