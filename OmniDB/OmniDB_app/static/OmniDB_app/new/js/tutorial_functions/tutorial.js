function startTutorial(p_tutorial_name) {
  var v_tutorial_name = (p_tutorial_name) ? p_tutorial_name : 'main';
  var v_tutorials = {
    'main': [
      {
        p_message: 'This contains the outer connection and global panels [ connections_list_manager, snippets_panel, [conn_1, conn_2, ...], add_connection]',
        p_target: document.getElementsByClassName('omnidb__tab-menu omnidb__tab-menu--primary')[0],
        p_title: 'Primary menu'
      },
      {
        p_message: 'This contains general settings and options, such as [ versioning, connections_list_manager, user_setting, plugins...]',
        p_target: document.getElementsByClassName('omnidb__utilities-menu')[0],
        p_title: 'Utilities menu'
      }
    ]
  }

  // Instanciate the component
  var v_omnisControl = createOmnis();
  // Selecting a tutorial
  var v_steps = v_tutorials[v_tutorial_name];
  // Update the step list with the new walkthrough
  v_omnisControl.updateStepList(v_steps);
  // Go to the first step of the walkthrough
  v_omnisControl.goToStep(0);
}
