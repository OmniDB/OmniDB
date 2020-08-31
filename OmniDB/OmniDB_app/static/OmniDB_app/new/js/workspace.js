/// <summary>
/// Startup function.
/// </summary>
$(function () {

  // Instantiating outer tab component
  v_connTabControl = createTabControl({
    p_div: 'omnidb_main_tablist',
    p_hierarchy: 'primary'
  });
  // Objects to control sequential change of active database tabs
  v_connTabControl.tag.change_active_database_call_list = [];
  v_connTabControl.tag.change_active_database_call_running = false;

  if (v_connTabControl.tabList.length === 0) {
    // Create the branding item for omnidb
    v_connTabControl.createTab({
      p_icon: `<svg class="omnidb-icon__theme--branding" height="27" viewBox="0 0 58 58" xmlns="http://www.w3.org/2000/svg">
                <path d="M40.8635 21.9291C39.8124 20.2722 38.403 18.8703 36.7378 17.827C37.1953 18.7168 37.5976 19.6889 37.9355 20.7357C38.9901 21.0739 39.9683 21.4761 40.8635 21.9291Z" fill="#878FC6"/>
                <path d="M30.6628 15.8552V19.5423C32.3082 19.5931 33.8876 19.7769 35.3722 20.0791C34.6859 18.4279 33.8104 17.0944 32.8125 16.1828C32.1155 16.0165 31.3987 15.9066 30.6628 15.8552Z" fill="#878FC6"/>
                <path d="M40.8621 35.8357C39.9661 36.2894 38.9901 36.6916 37.9355 37.0269C37.5976 38.0759 37.1946 39.0466 36.7378 39.9377C38.4037 38.8937 39.8124 37.4919 40.8621 35.8357Z" fill="#878FC6"/>
                <path d="M42.6299 31.4759C42.3757 30.9532 42.1965 30.3931 42.103 29.7986H39.1338C39.0829 31.4343 38.8987 33.0046 38.5984 34.4797C40.2586 33.7971 41.6001 32.925 42.5166 31.931C42.5534 31.7781 42.5995 31.6302 42.6299 31.4759Z" fill="#878FC6"/>
                <path d="M42.5173 25.8359C41.6015 24.8398 40.26 23.9677 38.5977 23.283C38.898 24.7602 39.0821 26.3297 39.1331 27.9655H42.1022C42.1957 27.3709 42.3749 26.8109 42.6313 26.2903C42.5994 26.136 42.5534 25.9867 42.5173 25.8359Z" fill="#878FC6"/>
                <path d="M36.9496 29.7986H30.6636V36.0492C32.6397 35.9844 34.5032 35.7146 36.1754 35.2785C36.6131 33.6153 36.8844 31.764 36.9496 29.7986Z" fill="#878FC6"/>
                <path d="M30.6628 27.9663H36.9488C36.8837 26.0008 36.6124 24.1474 36.174 22.4842C34.5017 22.0481 32.6382 21.7783 30.6621 21.7135V27.9663H30.6628Z" fill="#878FC6"/>
                <path d="M30.6628 41.9103C31.3987 41.8596 32.1148 41.749 32.8132 41.582C33.8112 40.669 34.6866 39.3369 35.3729 37.6857C33.8884 37.9865 32.3082 38.1696 30.6635 38.2204V41.9103H30.6628Z" fill="#878FC6"/>
                <path d="M20.8935 34.4797C20.5911 33.0046 20.4069 31.435 20.3559 29.7986H16.6445C16.6948 30.5284 16.806 31.2399 16.9718 31.9303C17.889 32.9271 19.2312 33.7971 20.8935 34.4797Z" fill="#878FC6"/>
                <path d="M28.8234 15.8552C28.0883 15.9059 27.3715 16.0165 26.6745 16.1828C25.6766 17.0944 24.8011 18.4286 24.1162 20.077C25.6008 19.7769 27.1788 19.5931 28.8234 19.5423V15.8552Z" fill="#878FC6"/>
                <path d="M28.8234 21.7135C26.848 21.7783 24.9852 22.0481 23.3137 22.4842C22.8738 24.1474 22.604 26.0008 22.5388 27.9663H28.8234V21.7135Z" fill="#878FC6"/>
                <path d="M22.7519 17.8256C21.0853 18.8689 19.6751 20.2714 18.6248 21.9269C19.5207 21.4739 20.4982 21.0717 21.5535 20.7357C21.8928 19.6874 22.2958 18.7146 22.7519 17.8256Z" fill="#878FC6"/>
                <path d="M28.8234 41.9103V38.2204C27.1788 38.1696 25.5994 37.9865 24.1162 37.6857C24.8011 39.3376 25.6758 40.6712 26.6745 41.582C27.3722 41.7483 28.0883 41.8589 28.8234 41.9103Z" fill="#878FC6"/>
                <path d="M16.6438 27.9662H20.3559C20.4062 26.3305 20.591 24.7602 20.8935 23.2837C19.2304 23.9663 17.8882 24.8405 16.971 25.8366C16.8053 26.527 16.6948 27.2378 16.6438 27.9662Z" fill="#878FC6"/>
                <path d="M22.752 39.9392C22.2958 39.0481 21.8928 38.0774 21.5543 37.0291C20.4996 36.6924 19.5229 36.2902 18.627 35.8379C19.6766 37.4934 21.0861 38.8952 22.752 39.9392Z" fill="#878FC6"/>
                <path d="M28.8234 29.7986H22.5388C22.604 31.764 22.8753 33.6153 23.3137 35.2785C24.9845 35.7146 26.848 35.9844 28.8234 36.0492V29.7986Z" fill="#878FC6"/>
                <path d="M25.8068 10.1681C26.2615 10.95 26.5002 11.7926 26.5732 12.6372C27.6009 12.4392 28.6584 12.3286 29.7441 12.3286C37.0387 12.3286 43.2227 17.0027 45.4701 23.4971C46.245 23.1357 47.0999 22.9173 48.0128 22.9173C48.3181 22.9173 48.612 22.9624 48.9053 23.0068C46.3831 14.8619 38.7591 8.94092 29.7449 8.94092C28.2114 8.94092 26.7247 9.1283 25.2891 9.45235C25.4704 9.6813 25.656 9.90814 25.8068 10.1681Z" fill="#878FC6"/>
                <path d="M15.4199 41.6361C15.8774 40.8507 16.4958 40.2223 17.1998 39.7376C14.6641 36.8444 13.1166 33.0713 13.1038 28.932C13.1038 28.9165 13.0996 28.901 13.0996 28.8841C13.0996 28.8707 13.1031 28.8587 13.1031 28.8453C13.1123 24.7073 14.6564 20.9364 17.187 18.0397C16.4858 17.5543 15.8739 16.9175 15.4185 16.1334C15.269 15.8756 15.1663 15.6072 15.0587 15.3395C11.7404 18.8984 9.69556 23.6485 9.69556 28.8841C9.69556 34.1224 11.7418 38.8725 15.0615 42.4293C15.1677 42.1624 15.2711 41.8925 15.4199 41.6361Z" fill="#878FC6"/>
                <path d="M48.0121 34.8495C47.0991 34.8495 46.2421 34.6304 45.4679 34.2676C43.2191 40.7641 37.0387 45.4353 29.7441 45.4353C28.6569 45.4353 27.5973 45.3233 26.5689 45.1268C26.4959 45.9735 26.2629 46.8182 25.8096 47.6029C25.6594 47.8622 25.4753 48.0869 25.2939 48.3144C26.7268 48.6385 28.2128 48.8252 29.7441 48.8252C38.7591 48.8252 46.383 42.9056 48.9066 34.7607C48.6105 34.8037 48.3173 34.8495 48.0121 34.8495Z" fill="#878FC6"/>
                <path d="M52.0317 28.8833C52.0317 26.6734 50.2334 24.8834 48.0115 24.8834C45.7896 24.8834 43.9863 26.6734 43.9863 28.8833C43.9863 31.0932 45.7896 32.8804 48.0115 32.8804C50.2334 32.8804 52.0317 31.0932 52.0317 28.8833Z" fill="#525678"/>
                <path d="M18.6008 9.68901C16.6757 10.7922 16.0177 13.2345 17.1283 15.1507C18.2375 17.0633 20.6995 17.7184 22.6225 16.6152C24.5476 15.5106 25.2041 13.0612 24.095 11.1522C22.9809 9.23957 20.5252 8.5809 18.6008 9.68901Z" fill="#525678"/>
                <path d="M18.6043 48.0832C20.5308 49.1878 22.9864 48.5334 24.097 46.6208C25.2062 44.7082 24.5475 42.2609 22.6259 41.1577C20.6994 40.051 18.2409 40.7076 17.1353 42.6188C16.0226 44.5349 16.6792 46.9808 18.6043 48.0832Z" fill="#525678"/>
              </svg>`,
      p_name: `<svg class="omnidb-icon__theme--branding" height="27" viewBox="0 0 133 58" xmlns="http://www.w3.org/2000/svg">
                <path d="M22.8526 21.4207H15.0254C11.1455 21.4207 8 24.8352 8 29.0471C8 33.2612 11.1455 36.6757 15.0254 36.6757H22.8526C26.734 36.6757 29.8795 33.2612 29.8795 29.0471C29.8795 24.8345 26.734 21.4207 22.8526 21.4207ZM21.271 33.2118H16.607C14.2952 33.2118 12.4204 31.3486 12.4204 29.0471C12.4204 26.7478 14.2945 24.8845 16.607 24.8845H21.271C23.5843 24.8845 25.4577 26.7485 25.4577 29.0471C25.4584 31.3486 23.5843 33.2118 21.271 33.2118Z" fill="#878FC6"/>
                <path d="M52.2109 23.7824C51.7439 22.2256 50.9429 21.4169 49.5109 21.4169C48.5809 21.4169 47.4339 21.712 46.8079 22.9406C45.6479 25.216 43.1874 30.1549 43.1874 30.1549C43.1874 30.1549 40.7339 25.2435 39.573 22.9681C38.9469 21.7388 37.7931 21.4169 36.8638 21.4169C35.4324 21.4169 34.6321 22.2256 34.1639 23.7824C33.7 25.328 30.4199 36.4366 30.4199 36.4366H34.9281L37.2768 27.4738C37.2768 27.4738 38.4355 30.5748 39.4916 33.0693C40.2183 34.7867 41.7559 35.4046 43.0238 35.4046C44.2916 35.4046 45.5389 34.8375 46.4529 33.2116C47.5729 31.2229 49.0979 27.4005 49.0979 27.4005L51.4459 36.4366H55.9539C55.9539 36.4366 52.6749 25.3287 52.2109 23.7824Z" fill="#878FC6"/>
                <path d="M57.6339 36.4366C57.6339 36.4366 57.6339 25.3689 57.6339 24.1783C57.6339 22.9871 58.4759 21.4169 59.9319 21.4169C61.3879 21.4169 62.5749 22.7335 63.2519 23.3393C63.9299 23.9452 71.3249 30.5163 71.3249 30.5163V21.6599H75.2899C75.2899 21.6599 75.2899 32.6706 75.2899 34.0302C75.2899 35.3898 74.4459 36.6796 72.7579 36.6796C71.0699 36.6796 70.2499 35.6391 69.1759 34.5719C68.1029 33.5046 61.7879 27.0067 61.7879 27.0067V36.438H57.6339V36.4366Z" fill="#878FC6"/>
                <path d="M82.0319 21.6599H78.0659V36.4373H82.0319V21.6599Z" fill="#878FC6"/>
                <path d="M84.8739 27.2261C84.8739 27.2261 84.8739 33.5598 84.8739 34.4644C84.8739 35.3689 85.2319 36.4368 86.7609 36.4368C88.2899 36.4368 91.1979 36.4368 94.8219 36.4368C98.4459 36.4368 103.774 33.5901 103.774 28.9048C103.774 24.2194 99.5759 21.6602 94.6979 21.6602C89.8199 21.6602 87.8059 21.6602 87.8059 21.6602L84.8749 25.5037C84.8749 25.5037 90.8709 25.5037 94.8229 25.5037C98.7749 25.5037 99.2219 28.2412 99.2219 29.1034C99.2219 29.9657 98.5889 32.637 94.8229 32.637C91.0569 32.637 89.4929 32.637 89.4929 32.637V27.2261H84.8739Z" fill="#515579"/>
                <path d="M122.871 28.8383C122.871 28.8383 124.892 27.8542 124.892 25.7457C124.892 23.6373 123.387 21.6592 119.053 21.6592C114.718 21.6592 109.213 21.6592 109.213 21.6592L106.104 25.5027C106.104 25.5027 117.651 25.5027 118.794 25.5027C119.938 25.5027 120.54 25.7521 120.54 26.4516C120.54 27.1511 119.997 27.4463 118.724 27.4463C117.449 27.4463 106.105 27.4463 106.105 27.4463C106.105 27.4463 106.105 33.1249 106.105 34.102C106.105 35.0791 106.564 36.4359 109.294 36.4359C112.025 36.4359 116.689 36.4359 119.163 36.4359C121.635 36.4359 125.198 35.0812 125.198 32.3282C125.196 29.5766 122.871 28.8383 122.871 28.8383ZM118.685 32.6367C117.449 32.6367 110.722 32.6367 110.722 32.6367V30.6051C110.722 30.6051 117.75 30.6051 118.794 30.6051C119.838 30.6051 120.605 30.6544 120.605 31.5998C120.605 32.5451 119.923 32.6367 118.685 32.6367Z" fill="#515579"/>
              </svg>`,
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        return startConnectionManagement();
      }
    });
  }

  // Creating first tab of the outer tab
  v_connTabControl.createTab(
    {
      p_name: '+',
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        showMenuNewTabOuter(e);
      }
    }
  );

  // Instantiating functions responsible for creating all the different types
  // of tabs
  initCreateTabFunctions();

  // Creates the snippets panel
  v_connTabControl.tag.createSnippetPanel();

  // Retrieving database list
  getDatabaseList(true);

  // TODO: design a worthy tutorial.
  // Create tutorial - tmp always active
  if (true) {
    startTutorial('main');
  }

});

/// <summary>
/// Retrieves database list.
/// </summary>
function getDatabaseList(p_init, p_callback) {

	execAjax('/get_database_list/',
			JSON.stringify({}),
			function(p_return) {

				v_connTabControl.tag.connections = p_return.v_data.v_connections;

				v_connTabControl.tag.groups = p_return.v_data.v_groups;
				v_connTabControl.tag.remote_terminals = p_return.v_data.v_remote_terminals;

				if (p_init) {

					if (v_connTabControl.tag.connections.length>0) {

						//Create existing tabs
						var v_current_parent = null;
						var v_has_old_tabs = false;
						if (p_return.v_data.v_existing_tabs.length>0)
							v_has_old_tabs = true;

						for (var i=0; i < p_return.v_data.v_existing_tabs.length; i++) {
							if (v_current_parent == null || v_current_parent != p_return.v_data.v_existing_tabs[i].index) {
                startLoading();
								v_connTabControl.tag.createConnTab(p_return.v_data.v_existing_tabs[i].index,false);
								v_connTabControl.tag.createConsoleTab();
							}

							v_current_parent = p_return.v_data.v_existing_tabs[i].index;
							v_connTabControl.tag.createQueryTab(p_return.v_data.v_existing_tabs[i].title,p_return.v_data.v_existing_tabs[i].tab_db_id);
					    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue(
					        p_return.v_data.v_existing_tabs[i].snippet);
							v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
					    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);
						}

						if (!v_has_old_tabs) {
              startLoading();
							v_connTabControl.tag.createConnTab(v_connTabControl.tag.connections[0].v_conn_id);
            }

					}
					else {/*
						var v_instance = new Tooltip($('#menu_connections'),{
					    title: 'Create your first connection!',
					    placement: "bottom",
					  });
						v_instance.show();
				    window.setTimeout(function() {
				        v_instance.dispose();
				    }, 4000);*/
					}
				}

				if (p_callback)
					p_callback();

        endLoading();

			},
			null,
			'box');
}

function queueChangeActiveDatabaseThreadSafe(p_data) {

	v_connTabControl.tag.change_active_database_call_list.push(p_data);
	if (!v_connTabControl.tag.change_active_database_call_running) {
		changeActiveDatabaseThreadSafe(v_connTabControl.tag.change_active_database_call_list.pop());
	}
}

function changeActiveDatabaseThreadSafe(p_data) {
	v_connTabControl.tag.change_active_database_call_running = true;
	execAjax('/change_active_database/',
			JSON.stringify(p_data),
			function(p_return) {
				v_connTabControl.tag.change_active_database_call_running = false;
				if (v_connTabControl.tag.change_active_database_call_list.length>0)
					changeActiveDatabaseThreadSafe(v_connTabControl.tag.change_active_database_call_list.pop());
			},
			null,
			'box');
}

/// <summary>
/// Changing database in the current connection tab.
/// </summary>
function changeDatabase(p_value) {

  v_connTabControl.selectedTab.tag.divDetails.innerHTML = '';

  //finding connection object
  var v_conn_object = null;
  for (var i=0; i<v_connTabControl.tag.connections.length; i++) {
  	if (p_value==v_connTabControl.tag.connections[i].v_conn_id) {
  		v_conn_object = v_connTabControl.tag.connections[i];
  		break;
  	}
  }
  if (!v_conn_object)
  	v_conn_object = v_connTabControl.tag.connections[0];

  v_connTabControl.selectedTab.tag.selectedDatabaseIndex = parseInt(p_value);
  v_connTabControl.selectedTab.tag.selectedDBMS = v_conn_object.v_db_type;
  v_connTabControl.selectedTab.tag.consoleHelp = v_conn_object.v_console_help;
  v_connTabControl.selectedTab.tag.selectedDatabase = v_conn_object.v_database;
  v_connTabControl.selectedTab.tag.selectedTitle = v_conn_object.v_alias;

  // Icons are now built inside the function with p_icon
  // if (v_connTabControl.selectedTab.tag.selectedTitle!='')
  // 	v_connTabControl.selectedTab.tag.tabTitle.innerHTML = '<img src="' + v_url_folder + '/static/OmniDB_app/images/' + v_connTabControl.selectedTab.tag.selectedDBMS + '_medium.png"/> ' + v_connTabControl.selectedTab.tag.selectedTitle + ' - ' + v_connTabControl.selectedTab.tag.selectedDatabase;
  // else
  // 	v_connTabControl.selectedTab.tag.tabTitle.innerHTML = '<img src="' + v_url_folder + '/static/OmniDB_app/images/' + v_connTabControl.selectedTab.tag.selectedDBMS + '_medium.png"/> ' + v_connTabControl.selectedTab.tag.selectedDatabase;


  queueChangeActiveDatabaseThreadSafe({
  		"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
  		"p_tab_id": v_connTabControl.selectedTab.id,
  		"p_database": v_connTabControl.selectedTab.tag.selectedDatabase
  });

  if (v_conn_object.v_db_type=='postgresql')
  	getTreePostgresql(v_connTabControl.selectedTab.tag.divTree.id);
    else if (v_conn_object.v_db_type=='oracle')
  	getTreeOracle(v_connTabControl.selectedTab.tag.divTree.id);
    else if (v_conn_object.v_db_type=='mysql')
  	getTreeMysql(v_connTabControl.selectedTab.tag.divTree.id);
    else if (v_conn_object.v_db_type=='mariadb')
  	getTreeMariadb(v_connTabControl.selectedTab.tag.divTree.id);

}

/// <summary>
/// Check if there are troublesome tabs
/// </summary>
/// <param name="p_cancel_function">Ok function.</param>
/// <param name="p_ok_function">Cancel function.</param>
function checkBeforeChangeDatabase(p_cancel_function, p_ok_function) {
	for (var i=0; i < v_connTabControl.selectedTab.tag.tabControl.tabList.length; i++) {

		var v_tab = v_connTabControl.selectedTab.tag.tabControl.tabList[i];
		if (v_tab.tag!=null)
			if (v_tab.tag.mode=='edit' || v_tab.tag.mode=='alter' || v_tab.tag.mode=='debug' || v_tab.tag.mode=='monitor_dashboard' || v_tab.tag.mode=='data_mining') {
				showAlert('Before changing connection please close any tab that belongs to the following types: <br/><br/><b>Edit Data<br/><br/>Alter Table<br/><br/>Function Debugging<br/><br/>Monitoring Dashboard<br/><br/>Advanced Object Search');
				v_connTabControl.selectedTab.tag.dd_object.set("selectedIndex",v_connTabControl.selectedTab.tag.dd_selected_index);
				if (p_cancel_function!=null)
					p_cancel_function();
				return null;
			}
	}
	if (p_ok_function!=null)
		p_ok_function();
}

function adjustQueryTabObjects(p_all_tabs) {
	var v_dbms = v_connTabControl.selectedTab.tag.selectedDBMS;

	var v_target_div = null;
	if (!p_all_tabs)
		v_target_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.elementDiv;
	else
		v_target_div = v_connTabControl.selectedTab.elementDiv;

	var v_objects = $(v_target_div).find(".dbms_object").each(function() {
	  $( this ).css('display','none');
	});

	var v_objects = $(v_target_div).find("." + v_dbms + "_object").each(function() {
		if (!$( this ).hasClass('dbms_object_hidden'))
	  	$( this ).css('display','inline-block');
	});

}

/// <summary>
/// Draws graph.
/// </summary>
function drawGraph(p_all, p_schema) {

	execAjax('/draw_graph/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_tab_id": v_connTabControl.selectedTab.id,
											"p_complete": p_all,
											"p_schema": p_schema}),
			function(p_return) {

          v_nodes = [];
          v_edges = [];

          for (var i=0; i<p_return.v_data.v_nodes.length; i++)
          {

	        	var v_node_object = new Object();
						v_node_object.data = new Object();
						v_node_object.position = new Object();
						v_node_object.data.id = p_return.v_data.v_nodes[i].id;
						v_node_object.data.label = p_return.v_data.v_nodes[i].label;
						v_node_object.classes = 'group' + p_return.v_data.v_nodes[i].group;

						v_nodes.push(v_node_object);

          }

          for (var i=0; i<p_return.v_data.v_edges.length; i++)
          {

          	var v_edge_object = new Object();
						v_edge_object.data = new Object();
						v_edge_object.data.source = p_return.v_data.v_edges[i].from;
						v_edge_object.data.target = p_return.v_data.v_edges[i].to;
						v_edge_object.data.label = p_return.v_data.v_edges[i].label;
						v_edge_object.data.faveColor = '#9dbaea';
						v_edge_object.data.arrowColor = '#9dbaea';
						v_edges.push(v_edge_object);

          }

					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.network = window.cy = cytoscape({
						container: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.graph_div,
						boxSelectionEnabled: false,
						autounselectify: true,
						layout: {
							name: 'spread',
	            			idealEdgeLength: 100,
	            			nodeOverlap: 20
						},
						style: [
							{
								selector: 'node',
								style: {
									'content': 'data(label)',
									'text-opacity': 0.5,
									'text-valign': 'top',
									'text-halign': 'right',
									'background-color': '#11479e',
									'text-wrap': 'wrap',


								}
							},
							{
								selector: 'node.group0',
								style: {
									'background-color': 'slategrey',
									'shape': 'square'
								}
							},
							{
								selector: 'node.group1',
								style: {
									'background-color': 'blue'
								}
							},
							{
								selector: 'node.group2',
								style: {
									'background-color': 'cyan'
								}
							},
							{
								selector: 'node.group3',
								style: {
									'background-color': 'lightgreen'
								}
							},
							{
								selector: 'node.group4',
								style: {
									'background-color': 'yellow'
								}
							},
							{
								selector: 'node.group5',
								style: {
									'background-color': 'orange'
								}
							},
							{
								selector: 'node.group6',
								style: {
									'background-color': 'red'
								}
							},

							{
								selector: 'edge',
								style: {
									'curve-style': 'bezier',
							        'target-arrow-shape': 'triangle',
							        'target-arrow-color': 'data(faveColor)',
							        'line-color': 'data(arrowColor)',
							        'text-opacity': 0.75,
							        'width': 2,
							        'control-point-distances': 50,
							        'content': 'data(label)',
							        'text-wrap': 'wrap',
							        'edge-text-rotation': 'autorotate',
							        'line-style': 'solid'
								}
							}
						],

						elements: {
							nodes: v_nodes,
							edges: v_edges
						}
					});

			},
			function(p_return) {
				if (p_return.v_data.password_timeout) {
					showPasswordPrompt(
						v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
						function() {
							drawGraph(p_all, p_schema);
						},
						null,
						p_return.v_data.message
					);
				}
			},
			'box');
}

/// <summary>
/// Rename tab.
/// </summary>
function renameTab(p_tab) {

	showConfirm('<input id="tab_name"/ class="form-control" value="' + p_tab.tag.tab_title_span.innerHTML + '" style="width: 100%;">',
        function() {
					renameTabConfirm(p_tab,document.getElementById('tab_name').value);
        },
        null,
        function() {
          var v_input = document.getElementById('tab_name');
          v_input.focus();
          v_input.selectionStart = v_input.selectionEnd = 10000;
        });
	var v_input = document.getElementById('tab_name');
	v_input.onkeydown = function() {
		if (event.keyCode == 13)
			document.getElementById('modal_message_ok').click();
		else if (event.keyCode == 27)
			document.getElementById('modal_message_cancel').click();
	}

}

/// <summary>
/// Renames tab.
/// </summary>
function renameTabConfirm(p_tab, p_name) {

	p_tab.tag.tab_title_span.innerHTML=p_name;

}

/// <summary>
/// Removes tab.
/// </summary>
function removeTab(p_tab) {

	if (p_tab.tag.ht!=null) {
		p_tab.tag.ht.destroy();
		p_tab.tag.div_result.innerHTML = '';
	}

	if (p_tab.tag.editor!=null)
		p_tab.tag.editor.destroy();

	if (p_tab.tag.mode=='query' || p_tab.tag.mode=='edit' || p_tab.tag.mode=='console' || p_tab.tag.mode=='outer_terminal') {
		var v_message_data = { tab_id: p_tab.tag.tab_id, tab_db_id: null };
		if (p_tab.tag.mode=='query')
			v_message_data.tab_db_id = p_tab.tag.tab_db_id;

    createRequest(v_queryRequestCodes.CloseTab, [v_message_data]);
	}
	p_tab.removeTab();

}

/// <summary>
/// Resize snippet panel and transforms position when its visible.
/// </summary>
var resizeSnippetPanel = function() {
  if (v_connTabControl.snippet_tag !== undefined) {
    var v_target_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    var v_target_tag_div_result_top = v_target_tag.div_result.getBoundingClientRect().height - 25;
    var v_snippet_tag = v_connTabControl.snippet_tag;
    var v_inner_snippet_tag = v_snippet_tag.tabControl.selectedTab.tag;
    if (v_inner_snippet_tag.editor !== undefined) {
      if (v_snippet_tag.isVisible) {
        v_snippet_tag.divPanel.style.transform = 'translateY(-' + v_target_tag_div_result_top + 'px)';
      }
      v_snippet_tag.divPanel.style.height = v_target_tag_div_result_top;
      v_snippet_tag.divTree.style.height = v_target_tag_div_result_top;
      v_inner_snippet_tag.editorDiv.style.height = v_target_tag_div_result_top - 90 + 'px';
    }
  }
}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeTreeVertical(event) {
	var v_verticalLine = document.createElement('div');
	v_verticalLine.id = 'vertical-resize-line';
  v_connTabControl.selectedTab.tag.divLeft.appendChild(v_verticalLine);

	document.body.addEventListener(
		'mousemove',
		getVerticalLinePosition
	)

	v_start_height = event.screenY;
	document.body.addEventListener("mouseup", resizeTreeVerticalEnd);

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeTreeVerticalEnd(event) {
  console.log(v_connTabControl.selectedTab.tag.mode);

	document.body.removeEventListener("mouseup", resizeTreeVerticalEnd);
	document.getElementById('vertical-resize-line').remove();

	document.body.removeEventListener(
		'mousemove',
		getVerticalLinePosition
	)

	var v_height_diff = event.screenY - v_start_height;

	var v_tag = v_connTabControl.selectedTab.tag;

	var v_tree_div = v_tag.divTree;
	var v_result_div = null;

  var v_tree_tabs_div = v_tag.divTreeTabs;

  var v_tree_tabs_height = v_tag.divLeft.clientHeight - 14 - event.pageY;
  v_tree_tabs_div.style.flexBasis = v_tree_tabs_height  + 'px';

  var v_inner_height = v_tree_tabs_height - 35  + 'px';

  if (v_tag.currTreeTab=='properties')
		v_result_div = v_tag.divProperties;
	else if (v_tag.currTreeTab=='ddl')
		v_result_div = v_tag.divDDL;

	v_tree_div.style.height = parseInt(v_tree_div.clientHeight, 10) + v_height_diff + 'px';
  v_result_div.style.height = v_inner_height;

	if (v_tag.currTreeTab=='properties')
		v_tag.gridProperties.render();
	else if (v_tag.currTreeTab=='ddl')
		v_tag.ddlEditor.resize();

}

/// <summary>
/// Redefines horizontal resize line position.
/// </summary>
function horizontalLinePosition(p_event) {
	document.getElementById('horizontal-resize-line').style.left = p_event.pageX + 'px';
}

/// <summary>
/// Resize Snippet panel editor horizontally.
/// </summary>
function resizeConnectionHorizontal(event) {
  event.preventDefault();
	var v_horizontalLine = document.createElement('div');
	v_horizontalLine.id = 'horizontal-resize-line';
	v_connTabControl.selectedDiv.appendChild(v_horizontalLine);

	document.body.addEventListener(
		'mousemove',
		horizontalLinePosition
	)

	v_start_width = event.screenX;
	document.body.addEventListener("mouseup", resizeConnectionHorizontalEnd);

}

/// <summary>
/// Resize Connection tab horizontally.
/// </summary>
function resizeConnectionHorizontalEnd(event) {

	document.body.removeEventListener("mouseup", resizeConnectionHorizontalEnd);
	document.getElementById('horizontal-resize-line').remove();

	document.body.removeEventListener(
		'mousemove',
		horizontalLinePosition
	)

	var v_div_left = v_connTabControl.selectedTab.tag.divLeft;
	var v_div_right = v_connTabControl.selectedTab.tag.divRight;

  var v_offsetLeft = v_connTabControl.selectedTab.tag.divLeft.getBoundingClientRect().left;
  var v_totalWidth = v_connTabControl.selectedDiv.getBoundingClientRect().width;

  var v_mousePosX = event.screenX;
  var v_paddingCompensation = 16;

  var v_fraction = (v_mousePosX > v_offsetLeft)
  ? 100*((v_paddingCompensation + v_mousePosX - v_offsetLeft) / v_totalWidth)
  : 0;

  var v_left_width_value = v_fraction + '%';

  v_div_left.style['max-width'] = v_left_width_value;
  v_div_left.style['flex'] = '0 0 ' + v_left_width_value;

  var v_right_width_value = (100 - v_fraction) + '%';

  v_div_right.style['max-width'] = v_right_width_value;
  v_div_right.style['flex'] = '0 0 ' + v_right_width_value;

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  refreshHeights();

}

/// <summary>
/// Resize Snippet panel editor horizontally.
/// </summary>
function resizeSnippetHorizontal(event) {
  event.preventDefault();
	var v_horizontalLine = document.createElement('div');
	v_horizontalLine.id = 'horizontal-resize-line';
	v_connTabControl.snippet_tag.divPanel.appendChild(v_horizontalLine);

	document.body.addEventListener(
		'mousemove',
		horizontalLinePosition
	)

	v_start_width = event.screenX;
	document.body.addEventListener("mouseup", resizeSnippetHorizontalEnd);

}

/// <summary>
/// Resize Snippet panel editor horizontally.
/// </summary>
function resizeSnippetHorizontalEnd(event) {

	document.body.removeEventListener("mouseup", resizeSnippetHorizontalEnd);
	document.getElementById('horizontal-resize-line').remove();

	document.body.removeEventListener(
		'mousemove',
		horizontalLinePosition
	)

	var v_div_left = v_connTabControl.snippet_tag.divLeft;
	var v_div_right = v_connTabControl.snippet_tag.divRight;

  var v_offsetLeft = v_connTabControl.snippet_tag.divLeft.getBoundingClientRect().left;
  var v_totalWidth = v_connTabControl.snippet_tag.divPanel.getBoundingClientRect().width;

  var v_mousePosX = event.screenX;
  var v_paddingCompensation = 16;

  var v_fraction = (v_mousePosX > v_offsetLeft)
  ? 100*((v_paddingCompensation + v_mousePosX - v_offsetLeft) / v_totalWidth)
  : 0;

  var v_left_width_value = v_fraction + '%';

  v_div_left.style['max-width'] = v_left_width_value;
  v_div_left.style['flex'] = '0 0 ' + v_left_width_value;

  var v_right_width_value = (100 - v_fraction) + '%';

  v_div_right.style['max-width'] = v_right_width_value;
  v_div_right.style['flex'] = '0 0 ' + v_right_width_value;

	var v_tab_tag = v_connTabControl.snippet_tag.tabControl.selectedTab.tag;

  refreshHeights();

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeVertical(event) {
  event.preventDefault();
	var v_verticalLine = document.createElement('div');
	v_verticalLine.id = 'vertical-resize-line';
	v_connTabControl.selectedTab.tag.divRight.appendChild(v_verticalLine);

	document.body.addEventListener(
		'mousemove',
		getVerticalLinePosition
	)

	v_start_height = event.screenY;
	document.body.addEventListener("mouseup", resizeVerticalEnd);

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeVerticalEnd(event) {

	document.body.removeEventListener("mouseup", resizeVerticalEnd);
	document.getElementById('vertical-resize-line').remove();

	document.body.removeEventListener(
		'mousemove',
		getVerticalLinePosition
	)

	var v_height_diff = event.screenY - v_start_height;

	var v_editor_div = document.getElementById(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editorDivId);
	var v_result_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

	if (v_height_diff < 0) {
		if (Math.abs(v_height_diff) > parseInt(v_editor_div.style.height, 10))
		 v_height_diff = parseInt(v_editor_div.style.height, 10)*-1 + 10;
	}
	else {
		if (Math.abs(v_height_diff) > parseInt(v_result_div.style.height, 10))
		 v_height_diff = parseInt(v_result_div.style.height, 10) - 10;
	}
	v_editor_div.style.height = parseInt(v_editor_div.style.height, 10) + v_height_diff + 'px';
	v_result_div.style.height = parseInt(v_result_div.style.height, 10) - v_height_diff + 'px';

  refreshHeights();

  // Centralizing all adjusts on refreshHeights.
  //
	// var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  //
	// if(v_tab_tag.editor != null) {
	// 	v_tab_tag.editor.resize();
	// }
  //
	// if (v_tab_tag.mode=='query') {
	// 	if (v_tab_tag.currQueryTab=='data') {
	// 		v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 29 + 'px';
	// 		if (v_tab_tag.ht!=null)
	// 			v_tab_tag.ht.render();
	// 	}
	// 	else if (v_tab_tag.currQueryTab=='message') {
	// 		v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 29 + 'px';
	// 	}
	// 	else if (v_tab_tag.currQueryTab=='explain') {
	// 		v_tab_tag.div_explain.style.height = window.innerHeight - $(v_tab_tag.div_explain).offset().top - 29 + 'px';
	// 	}
	// }
	// else if (v_tab_tag.mode=='debug') {
	// 	v_tab_tag.editor.resize();
	// 	if (v_tab_tag.currDebugTab=='variable') {
	// 		v_tab_tag.div_variable.style.height = window.innerHeight - $(v_tab_tag.div_variable).offset().top - 29 + 'px';
	// 		if (v_tab_tag.htVariable!=null)
	// 			v_tab_tag.htVariable.render();
	// 	}
	// 	if (v_tab_tag.currDebugTab=='parameter') {
	// 		v_tab_tag.div_parameter.style.height = window.innerHeight - $(v_tab_tag.div_parameter).offset().top - 29 + 'px';
	// 		if (v_tab_tag.htParameter!=null)
	// 			v_tab_tag.htParameter.render();
	// 	}
	// 	if (v_tab_tag.currDebugTab=='result') {
	// 		v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 29 + 'px';
	// 		if (v_tab_tag.htResult!=null)
	// 			v_tab_tag.htResult.render();
	// 	}
	// 	else if (v_tab_tag.currDebugTab=='message') {
	// 		v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 29 + 'px';
	// 	}
	// 	else if (v_tab_tag.currDebugTab=='statistics') {
	// 		v_tab_tag.div_statistics.style.height = window.innerHeight - $(v_tab_tag.div_statistics).offset().top - 29 + 'px';
	// 		if (v_tab_tag.chart!=null)
	// 			v_tab_tag.chart.update();
	// 	}
	// }
	// else if (v_tab_tag.mode=='edit') {
	// 	if (v_tab_tag.editDataObject.ht!=null) {
	// 		v_tab_tag.editDataObject.ht.render();
	// 	}
	// }
	// else if (v_tab_tag.mode=='console') {
	// 	v_tab_tag.editor_input.resize();
	// 	v_tab_tag.editor_console.resize();
	// }
	// else if(v_tab_tag.mode == 'data_mining') {
	// 	if(v_tab_tag.currQueryTab == 'data') {
	// 		v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 29 + 'px';
	// 	}
	// }
  //
  // resizeSnippetPanel();
  //
}

function resizeWindow(){
	refreshHeights(true);
}

var resizeTimeout;
$(window).resize(function() {
	clearTimeout(resizeTimeout);
	resizeTimeout = setTimeout(resizeWindow, 200);
});

/// <summary>
/// Refresh divs sizes and components of the currently selected tab
/// </summary>
function refreshHeights(p_all) {

  setTimeout(function(){
    //Adjusting tree height
    if (p_all) {
      refreshTreeHeight();
    }

    if (v_connections_data && v_connections_data.v_active) {
      v_connections_data.ht.render();
    }

    if (v_connTabControl.selectedTab.tag.mode=='monitor_all') {
      v_connTabControl.selectedTab.tag.tabControlDiv.style.height = window.innerHeight - $(v_connTabControl.selectedTab.tag.tabControlDiv).offset().top - 18 + 'px';
    }
    else if (v_connTabControl.selectedTab.tag.mode=='outer_terminal') {
      v_connTabControl.selectedTab.tag.div_console.style.height = window.innerHeight - $(v_connTabControl.selectedTab.tag.div_console).offset().top - 10 + 'px';
      v_connTabControl.selectedTab.tag.editor_console.fit();

    }

    //If inner tab exists
    if (v_connTabControl.selectedTab.tag.tabControl != null && v_connTabControl.selectedTab.tag.tabControl.selectedTab) {
      var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

      //Snippet tab, adjust editor only
      if (v_tab_tag.mode=='snippet') {
        v_tab_tag.editorDiv.style.height = window.innerHeight - $(v_tab_tag.editorDiv).offset().top - 60 + 'px';
        v_tab_tag.editor.resize();
      }
      else if (v_tab_tag.mode=='monitor_unit') {
        var v_new_height = window.innerHeight - $(v_tab_tag.editorDataDiv).offset().top - 12 + 'px';
        v_tab_tag.editorDiv.style.height = v_new_height;
        v_tab_tag.editorDataDiv.style.height = v_new_height;
        v_tab_tag.editor.resize();
        v_tab_tag.editor_data.resize();
      }
      else if (v_tab_tag.mode=='query') {
        if (v_tab_tag.currQueryTab=='data') {
          v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 15 + 'px';
          if (v_tab_tag.ht!=null) {
            v_tab_tag.ht.render();
          }
          if(v_tab_tag.editor != null) {
            v_tab_tag.editor.resize();
          }
        }
        else if (v_tab_tag.currQueryTab=='message') {
          v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 15 + 'px';
        }
        else if (v_tab_tag.currQueryTab=='explain') {
          v_tab_tag.div_explain.style.height = window.innerHeight - $(v_tab_tag.div_explain).offset().top - 15 + 'px';
          if (v_tab_tag.explainControl) {
            v_tab_tag.explainControl.resize();
          }
        }
      }
      else if (v_tab_tag.mode=='console') {
        v_tab_tag.div_console.style.height = window.innerHeight - $(v_tab_tag.div_console).offset().top - parseInt(v_tab_tag.div_result.style.height,10) - 50 + 'px';
        v_tab_tag.editor_console.resize();
        v_tab_tag.editor_input.resize();

      }
      else if (v_tab_tag.mode=='debug') {
        if (v_tab_tag.currDebugTab=='variable') {
          v_tab_tag.div_variable.style.height = window.innerHeight - $(v_tab_tag.div_variable).offset().top - 15 + 'px';
          if (v_tab_tag.htVariable!=null)
          v_tab_tag.htVariable.render();
        }
        else if (v_tab_tag.currDebugTab=='parameter') {
          v_tab_tag.div_parameter.style.height = window.innerHeight - $(v_tab_tag.div_parameter).offset().top - 15 + 'px';
          if (v_tab_tag.htParameter!=null)
          v_tab_tag.htParameter.render();
        }
        else if (v_tab_tag.currDebugTab=='result') {
          v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 15 + 'px';
          if (v_tab_tag.htResult!=null)
          v_tab_tag.htResult.render();
        }
        else if (v_tab_tag.currDebugTab=='message') {
          v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 15 + 'px';
        }
        else if (v_tab_tag.currDebugTab=='statistics') {
          v_tab_tag.div_statistics.style.height = window.innerHeight - $(v_tab_tag.div_statistics).offset().top - 15 + 'px';
          if (v_tab_tag.chart!=null)
          v_tab_tag.chart.update();
        }
      }
      else if (v_tab_tag.mode=='monitor_grid') {
        v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 21 + 'px';
        if (v_tab_tag.ht!=null)
        v_tab_tag.ht.render();
      }
      else if (v_tab_tag.mode=='query_history') {
        v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 21 + 'px';
        if (v_tab_tag.ht!=null)
        v_tab_tag.ht.render();
      }
      else if (v_tab_tag.mode=='graph') {
        v_tab_tag.graph_div.style.height = window.innerHeight - $(v_tab_tag.graph_div).offset().top - 10 + "px";

      }
      else if (v_tab_tag.mode=='website') {
        v_tab_tag.iframe.style.height = window.innerHeight - $(v_tab_tag.iframe).offset().top - 10 + "px";
      }
      else if (v_tab_tag.mode=='website_outer') {
        v_tab_tag.iframe.style.height = window.innerHeight - $(v_tab_tag.iframe).offset().top - 10 + "px";
      }
      else if (v_tab_tag.mode=='edit') {
        v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 10 + 'px';
        if (v_tab_tag.editDataObject.ht!=null) {
          v_tab_tag.editDataObject.ht.render();
        }
      }
      else if (v_tab_tag.mode=='monitor_dashboard') {
        v_tab_tag.dashboard_div.style.height = window.innerHeight - $(v_tab_tag.dashboard_div).offset().top - $(v_tab_tag.dashboard_div.parentElement).scrollTop() - 10 + "px";
      }
      else if (v_tab_tag.mode=='alter') {
        if (v_tab_tag.alterTableObject.window=='columns') {
          var v_height = window.innerHeight - $(v_tab_tag.htDivColumns).offset().top - 45;
          v_tab_tag.htDivColumns.style.height = v_height + 'px';
          if (v_tab_tag.alterTableObject.htColumns!=null) {
            v_tab_tag.alterTableObject.htColumns.render();
          }
        }
        else if (v_tab_tag.alterTableObject.window=='constraints') {
          var v_height = window.innerHeight - $(v_tab_tag.htDivConstraints).offset().top - 45;
          v_tab_tag.htDivConstraints.style.height = v_height + 'px';
          if (v_tab_tag.alterTableObject.htConstraints!=null) {
            v_tab_tag.alterTableObject.htConstraints.render();
          }
        }
        else {
          var v_height = window.innerHeight - $(v_tab_tag.htDivIndexes).offset().top - 45;
          v_tab_tag.htDivIndexes.style.height = v_height + 'px';
          if (v_tab_tag.alterTableObject.htIndexes!=null) {
            v_tab_tag.alterTableObject.htIndexes.render();
          }
        }
      }
      else if(v_tab_tag.mode == 'data_mining') {
        if(v_tab_tag.currQueryTab == 'data') {
          v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 15 + 'px';
        }
      }
    }

    //Hooks
    if (v_connTabControl.tag.hooks.windowResize.length>0) {
      for (var i=0; i<v_connTabControl.tag.hooks.windowResize.length; i++)
      v_connTabControl.tag.hooks.windowResize[i]();
    }

    //Snippet panel
    resizeSnippetPanel();

  },351);
}

function refreshTreeHeight() {
  var v_tag = v_connTabControl.selectedTab.tag;

	if (v_tag.currTreeTab=='properties') {
		var v_height  = window.innerHeight - $(v_tag.divProperties).offset().top - 8;
		v_tag.divProperties.style.height = v_height + "px";
		v_tag.gridProperties.render();
	}
	else if (v_tag.currTreeTab=='ddl') {
		var v_height  = window.innerHeight - $(v_tag.divDDL).offset().top - 8;
		v_tag.divDDL.style.height = v_height + "px";
		v_tag.ddlEditor.resize();
	}
	else if (v_tag.mode=='snippets') {
		var v_height  = window.innerHeight - $(v_tag.divTree).offset().top;
		v_tag.divTree.style.height = v_height + "px";
	}

}

function checkTabStatus(v_tab) {

	if (v_tab.tag.tabControl.selectedTab.tag.mode=='query')
		checkQueryStatus(v_tab.tag.tabControl.selectedTab);
	else if (v_tab.tag.tabControl.selectedTab.tag.mode=='edit')
		checkEditDataStatus(v_tab.tag.tabControl.selectedTab);
	else if (v_tab.tag.tabControl.selectedTab.tag.mode=='debug')
		checkDebugStatus(v_tab.tag.tabControl.selectedTab);
	else if (v_tab.tag.tabControl.selectedTab.tag.mode=='console')
		checkConsoleStatus(v_tab.tag.tabControl.selectedTab);

}

/// <summary>
/// Indent SQL.
/// </summary>
function indentSQL() {

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	var v_editor = null;
	if (v_tab_tag.mode=='query')
		v_editor = v_tab_tag.editor;
	else if (v_tab_tag.mode=='console')
		v_editor = v_tab_tag.editor_input;
  else if (v_tab_tag.mode=='snippet')
		v_editor = v_tab_tag.editor;

	var v_sql_value = v_editor.getValue();

	if (v_sql_value.trim()=='') {
		showAlert('Please provide a string.');
	}
	else {
		execAjax('/indent_sql/',
				JSON.stringify({"p_sql": v_sql_value}),
				function(p_return) {

					v_editor.setValue(p_return.v_data);
					v_editor.clearSelection();
					v_editor.gotoLine(0, 0, true);

				},
				null,
				'box');
	}
}

function showMenuNewTabOuter(e) {

	var v_option_list = [];
	//Hooks
	if (v_connTabControl.tag.hooks.outerTabMenu.length>0) {
		for (var i=0; i<v_connTabControl.tag.hooks.outerTabMenu.length; i++)
			v_option_list = v_option_list.concat(v_connTabControl.tag.hooks.outerTabMenu[i]());
	}

	if (v_show_terminal_option)
		v_option_list.push({
			text: 'Local Terminal',
			icon: 'fas cm-all fa-terminal',
			action: function() {
				v_connTabControl.tag.createOuterTerminalTab();
			}
		});

		//building connection list
		if (v_connTabControl.tag.connections.length>0) {

			// No custom groups, render all connections in the same list
			if (v_connTabControl.tag.groups.length==1) {
				var v_submenu_connection_list = []

				for (var i=0; i<v_connTabControl.tag.connections.length; i++) (function(i){
					var v_conn = v_connTabControl.tag.connections[i];
					v_submenu_connection_list.push({
						text: v_conn.v_details1 + ' - ' + v_conn.v_details2,
						icon: 'fas cm-all node-' + v_conn.v_db_type,
						action: function() {
								v_connTabControl.tag.createConnTab(v_conn.v_conn_id, true, v_conn.v_alias);
						}
					});
				})(i);

				v_option_list.push({
					text: 'Connections',
					icon: 'fas cm-all fa-plug',
					submenu: {
							elements: v_submenu_connection_list
					}
				});
			}
			//Render connections split in groups
			else {

				var v_group_list = [];

				for (var i=0; i<v_connTabControl.tag.groups.length; i++) (function(i){
					var v_current_group = v_connTabControl.tag.groups[i];

					var v_group_connections = [];

					//First group, add all connections
					if (i==0) {
						for (var k=0; k<v_connTabControl.tag.connections.length; k++) (function(k){
							var v_conn = v_connTabControl.tag.connections[k];
							v_group_connections.push({
								text: v_conn.v_details1 + ' - ' + v_conn.v_details2,
								icon: 'fas cm-all node-' + v_conn.v_db_type,
								action: function() {
                  startLoading();
                  setTimeout(function() { v_connTabControl.tag.createConnTab(v_conn.v_conn_id); },0);
								}
							});
						})(k);

					}
					else {
						for (var j=0; j<v_current_group.conn_list.length; j++) {

							//Search corresponding connection to use its data
							for (var k=0; k<v_connTabControl.tag.connections.length; k++) (function(k){
								var v_conn = v_connTabControl.tag.connections[k];
								if (v_conn.v_conn_id==v_current_group.conn_list[j]) {
									v_group_connections.push({
										text: v_conn.v_details1 + ' - ' + v_conn.v_details2,
										icon: 'fas cm-all node-' + v_conn.v_db_type,
										action: function() {
                        startLoading();
                				setTimeout(function() { v_connTabControl.tag.createConnTab(v_conn.v_conn_id); },0);
										}
									});
									return;
								}
							})(k);

						}
					}

					var v_group_data = {
						text: v_current_group.v_name,
						icon: 'fas cm-all fa-plug',
						submenu: {
								elements: v_group_connections
						}
					}

					v_group_list.push(v_group_data);

				})(i);

				v_option_list.push({
					text: 'Connections',
					icon: 'fas cm-all fa-plug',
					submenu: {
							elements: v_group_list
					}
				});

			}
	}

	if (v_connTabControl.tag.remote_terminals.length>0) {

		var v_submenu_terminal_list = []

		for (var i=0; i<v_connTabControl.tag.remote_terminals.length; i++) (function(i){
			var v_term = v_connTabControl.tag.remote_terminals[i];
			v_submenu_terminal_list.push({
				text: v_term.v_alias,
				icon: 'fas cm-all fa-terminal',
				action: function() {
						v_connTabControl.tag.createOuterTerminalTab(v_term.v_conn_id,v_term.v_alias);
				}
			});
		})(i);

		v_option_list.push({
			text: 'SSH Consoles',
			icon: 'fas cm-all fa-terminal',
			submenu: {
					elements: v_submenu_terminal_list
			}
		});
}



	if (v_option_list.length>0) {
		v_option_list.unshift({
			text: 'New Connection',
			icon: 'fas cm-all fa-plug',
			action: function() {
				startLoading();
				setTimeout(function() { v_connTabControl.tag.createConnTab(); },0);
			}
		});

		customMenu(
			{
				x:e.clientX+5,
				y:e.clientY+5
			},
			v_option_list,
			null);
	}
	else {
		startLoading();
		setTimeout(function() { v_connTabControl.tag.createConnTab(); },0);
	}

}

function showMenuNewTab(e) {
	var v_option_list = [
		{
			text: 'Query Tab',
			icon: 'fas cm-all fa-search',
			action: function() {
				v_connTabControl.tag.createQueryTab();
			}
		},
		{
			text: 'Console Tab',
			icon: 'fas cm-all fa-terminal',
			action: function() {
				v_connTabControl.tag.createConsoleTab();
			}
		}
	];

	if (v_connTabControl.selectedTab.tag.selectedDBMS=='postgresql' ||
			v_connTabControl.selectedTab.tag.selectedDBMS=='mysql' ||
			v_connTabControl.selectedTab.tag.selectedDBMS=='mariadb') {
		v_option_list.push(
			{
				text: 'Monitoring Dashboard',
				icon: 'fas cm-all fa-chart-line',
				action: function() {
					v_connTabControl.tag.createMonitorDashboardTab();
					startMonitorDashboard();
				}
			}
		);

		v_option_list.push(
			{
				text: 'Backends',
				icon: 'fas cm-all fa-tasks',
				action: function() {
					v_connTabControl.tag.createMonitoringTab(
							'Backends',
							'select * from pg_stat_activity', [{
									icon: 'fas fa-times action-grid action-close',
									title: 'Terminate',
									action: 'postgresqlTerminateBackend'
							}]);
				}
			}
		);
	}
	else if (v_connTabControl.selectedTab.tag.selectedDBMS=='mysql' || v_connTabControl.selectedTab.tag.selectedDBMS=='mariadb') {
		v_option_list.push(
			{
				text: 'Process List',
				icon: 'fas cm-all fa-tasks',
				action: function() {
					v_connTabControl.tag.createMonitoringTab(
							'Process List',
							'select * from information_schema.processlist', [{
									icon: 'fas fa-times action-grid action-close',
									title: 'Terminate',
									action: 'mysqlTerminateBackend'
							}]);
				}
			}
		);
	}

	//Hooks
	if (v_connTabControl.tag.hooks.innerTabMenu.length>0) {
		for (var i=0; i<v_connTabControl.tag.hooks.innerTabMenu.length; i++) {
      v_option_list = v_option_list.concat(v_connTabControl.tag.hooks.innerTabMenu[i]());
    }
	}

	customMenu(
		{
			x:e.clientX+5,
			y:e.clientY+5
		},
		v_option_list,
		null);

}

function toggleTreeTabsContainer(p_target_id,p_horizonta_line_id) {
  $('#' + p_target_id).toggleClass('omnidb__tree-tabs--not-in-view');
  $('#' + p_horizonta_line_id).toggleClass('d-none');
}

function dragStart(event, gridContainer) {
  try {
    event.dataTransfer.setData("Text", event.target.id);
    event.dataTransfer.effectAllowed = "move";
    gridContainer.classList.add('omnidb__workspace-resize-grid--active');
    event.srcElement.classList.add('omnidb__workspace-resize-grid__draggable--is-dragging');
  }
  catch (e) {

  }
}

function dragEnd(event, grid_container) {
  grid_container.classList.remove('omnidb__workspace-resize-grid--active');
  event.target.classList.remove('omnidb__workspace-resize-grid__draggable--is-dragging');
}

function dragEnter(event) {
  event.target.classList.add('omnidb__workspace-resize-grid__column--enter');
}

function dragLeave(event) {
  event.target.classList.remove('omnidb__workspace-resize-grid__column--enter');
}

function allowDrop(event) {
  event.preventDefault();
}

function drop(event, grid_container, div_left, div_right) {
  event.preventDefault();
  try {
    var data = event.dataTransfer.getData("Text");
    event.target.appendChild(document.getElementById(data));

  	let pos = parseInt( event.srcElement.getBoundingClientRect().left );
  	let space = parseInt( window.innerWidth );
  	let cells = Math.round( pos*12 / space );

    div_left.classList = [' omnidb__workspace__div-left col-md-' + cells];
    div_right.classList = [' omnidb__workspace__div-right col-md-' + (12 - cells)];

    let cols = document.getElementsByClassName('omnidb__workspace-resize-grid__column');
    for (let i = 0; i < cols.length; i++) {
      document.getElementsByClassName('omnidb__workspace-resize-grid__column')[i].classList.remove('omnidb__workspace-resize-grid__column--enter');
    }
    v_connTabControl.selectedTab.tag.gridProperties.render();
  }
  catch (e) {

  }

}

/**
 * ## getVerticalLinePosition
 * @desc Gets the Y position of the pointer event.
 *
 * @param  {Object} p_event UI action pointer event.
 * @return {String}         The Y position of the pointer in pixels.
 */
function getVerticalLinePosition(p_event) {
	document.getElementById('vertical-resize-line').style.top = p_event.pageY + 'px';
}

function toggleExpandToPanelView(p_target_id) {
  let v_target = document.getElementById(p_target_id);
  if (v_target) {
    v_target.classList.toggle('omnidb__panel-view--full');
    setTimeout(function(){
      refreshHeights();
    },350);
  }
}
