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

activateHook('postgresqlTreeNodeOpen',function(p_node) {
  callPluginFunction({
    p_plugin_name: 'test_plugin',
    p_function_name: 'test_func',
    p_data: null,
    p_callback: function(p_data) {
      console.log(p_data);
    },
    p_loading: false,
    p_check_database_connection: true
  });
});

activateHook('changeTheme',function(p_new_theme, p_new_type) {
  console.log(p_new_theme);
  console.log(p_new_type);
});

activateHook('postgresqlTreeContextMenu',function(p_node) {
  if (p_node.tag.type == 'server') {
    return v_elements = [{
        text: 'Test',
        icon: getPluginPath('test_plugin') + 'images/refresh.png',
        action: function(node) {
          console.log(node);
        }
    }];
  } else {
    return v_elements = [];
  }
});

activateHook('postgresqlTreeNodeClick',function(p_node) {
  console.log(p_node);
});

activateHook('innerTabMenu',function() {
  return v_elements = [{
      text: 'Test',
      icon: getPluginPath('test_plugin') + 'images/refresh.png',
      action: function() {
        var v_tab_tag = createInnerTab({
          p_name: 'test',
          p_image: getPluginPath('test_plugin') + 'images/refresh.png',
          p_select_function: function() {
            console.log('selected')
          }
        });
        console.log(v_tab_tag);
      }
  }];
});

activateHook('outerTabMenu',function() {
  return v_elements = [{
      text: 'Test',
      icon: getPluginPath('test_plugin') + 'images/refresh.png',
      action: function() {
        var v_tab_tag = createOuterTab({
          p_name: 'test',
          p_image: getPluginPath('test_plugin') + 'images/refresh.png'
        });
        v_tab_tag.div.innerHTML = 'test';
        var tag = getSelectedOuterTabTag();
      }
  }];
});

activateHook('windowResize',function(p_node) {
});
