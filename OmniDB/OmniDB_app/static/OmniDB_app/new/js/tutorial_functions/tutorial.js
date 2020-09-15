function startTutorial(p_tutorial_name) {
  if (!window.omnis_ui_assistant) {
    // Instantiate the component.
    window.omnis_ui_assistant = createOmnis({
      p_callback_end: function(){ delete window.omnis_ui_assistant; }
    });
    // Setting the tutorial to the default example tutorial `main`.
    var v_tutorial_name = (p_tutorial_name) ? p_tutorial_name : 'main';
    // Configuring the available tutorials.
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
      ],
      'utilities_menu': [
        {
          p_callback_end: function() {$('.omnidb__utilities-menu').removeClass('omnidb__utilities-menu--show');},
          p_callback_start: function() {$('.omnidb__utilities-menu').addClass('omnidb__utilities-menu--show');},
          p_clone_target: true,
          p_message: `
          <p>Contains general settings and options:</p>
          <ul>
          <li>Username and versioning.</li>
          <li><i class="fas fa-plug omnidb__theme__text--primary mr-2"></i>Connection management.</li>
          <li><i class="fas fa-user omnidb__theme__text--primary mr-2"></i>User management.</li>
          <li><i class="fas fa-cog omnidb__theme__text--primary mr-2"></i>UI settings (shortcuts, theme, fonts...).</li>
          <li><i class="fas fa-cube omnidb__theme__text--primary mr-2"></i>Plugins management.</li>
          <li><i class="fas fa-sign-out-alt omnidb__theme__text--primary mr-2"></i>About.</li>
          </ul>
          `,
          p_target: document.getElementsByClassName('omnidb__utilities-menu')[0],
          p_title: 'Utilities Menu',
          p_update_delay: 300
        },
        {
          p_callback_end: function() {$('.omnidb__utilities-menu').removeClass('omnidb__utilities-menu--show');},
          p_callback_start: function() {$('.omnidb__utilities-menu').addClass('omnidb__utilities-menu--show');},
          p_clone_target: true,
          p_message: `
          <p>If you just configured OmniDB and logged with the default <strong>admin</strong> user, you should create the first user.</p>
          <p>Follow this walkthrough if you want to create other users as well.</p>
          `,
          p_next_button: false,
          p_target: document.getElementById('omnidb__utilities-menu__link-user'),
          p_title: 'Managing Users'
        },
        {
          p_callback_after_update_start: function() {setTimeout(function(){var v_target = document.getElementById('omnidb_utilities_menu_btn_new_user'); window.omnis_ui_assistant.divClonedElement.children[0].classList.remove('ml-2');},50);},
          p_clone_target: true,
          p_message: `
          <p>Click on <strong>Add new user</strong>.</p>
          `,
          p_next_button: false,
          p_target: function() {var v_target = document.getElementById('omnidb_utilities_menu_btn_new_user'); return v_target},
          p_title: 'Add a New User',
          p_update_delay: 600
        },
        {
          p_message: `
          <ul>
          <li><i class="fas fa-user omnidb__theme__text--primary mr-2"></i>OmniDB login name.</li>
          <li><i class="fas fa-key omnidb__theme__text--primary mr-2"></i>OmniDB login password.</li>
          <li><i class="fas fa-star omnidb__theme__text--primary mr-2"></i>Defines if the user can manage other OmniDB users.</li>
          </ul>
          <div class="alert alert-danger">The default <strong>admin user</strong> should be deleted once a new super user has been created.</div>
          `,
          p_target: function() {var v_target = document.getElementById('omnidb_user_content'); return v_target},
          p_title: 'User Options',
          p_update_delay: 350
        }
      ],
      'connections_menu': [
        {
          p_clone_target: true,
          p_message: `
          <p>This is the outer connections menu. Each connection added becomes a new item in this menu.</p>
          <p>The menu initially contains.</p>
          <ul>
          <li>Connections manager.</li>
          <li>Welcome, tutorial and useful links.</li>
          <li>Snippets panel toggler.</li>
          <li>Add connection.</li>
          </ul>
          <p>Let's first <span class="badge badge-info">add a new connection</span>.</p>
          <p>Please, click on the <i class="fas fa-plus"></i> button.</p>
          `,
          p_target: document.getElementsByClassName('omnidb__tab-menu omnidb__tab-menu--primary')[0],
          p_title: 'Primary menu'
        },
        {
          p_callback_after_update_start: function() {setTimeout(function(){var v_target = document.getElementById('button_new_connection'); window.omnis_ui_assistant.divClonedElement.children[0].classList.remove('ml-2');},50);},
          p_callback_start: function() {startConnectionManagement();},
          p_clone_target: true,
          p_message: `
          <p>Click on <strong>New Connection</strong>.</p>
          `,
          p_next_button: false,
          p_target: function() {var v_target = document.getElementById('button_new_connection'); return v_target},
          p_title: 'Add a New Connection',
          p_update_delay: 600
        },
        {
          p_message: `
          <p>Select the proper DBMS technology.</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_type'); return v_target},
          p_title: 'Connection Type',
          p_update_delay: 300
        },
        {
          p_message: `
          <p>Type a helpful name for the connection.</p>
          <p>This is used as name reference on many UI areas.</p>
          <p>i.e: Local dvdrental barman.</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_title'); return v_target},
          p_title: 'Title'
        },
        {
          p_message: `
          <p>Type the server address. Do not include ports.</p>
          <p>i.e:127.0.0.1</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_server'); return v_target},
          p_title: 'Server'
        },
        {
          p_message: `
          <p>Type the port of the server.</p>
          <p>i.e: PostgreSQL uses 5432 by default, but if you are using pgbouncer, you may want to use 6432 as the entry point.</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_port'); return v_target},
          p_title: 'Port'
        },
        {
          p_message: `
          <p>Type the name of the database.</p>
          <p>i.e: postgres, dvdrental.</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_database'); return v_target},
          p_title: 'Database'
        },
        {
          p_message: `
          <p>Type the name of the user with priviledges to access the database.</p>
          <p>i.e: postgres.</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_user'); return v_target},
          p_title: 'User'
        },
        {
          p_message: `
          <p>You may want to hit 'test' before saving the conntion.</p>
          <p>After that, click save.</p>
          `,
          p_target: function() {var v_target = document.getElementById('conn_form_button_test_connection'); return v_target},
          p_title: 'Test the Connection'
        }
      ]
    }
    // Selecting a tutorial
    var v_steps = v_tutorials[v_tutorial_name];
    // Update the step list with the new walkthrough
    window.omnis_ui_assistant.updateStepList(v_steps);
    // Go to the first step of the walkthrough
    window.omnis_ui_assistant.goToStep(0);
  }
}
