/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

var v_browserTabActive = true;

/// <summary>
/// Startup function.
/// </summary>
$(function () {
	$(window).focus(function() {
	    v_browserTabActive = true;
	    document.title = 'OmniDB';
	});

	$(window).blur(function() {
	    v_browserTabActive = false;
	});

	v_connTabControl = createTabControl('conn_tabs',0,null);
	v_connTabControl.tag.change_active_database_call_list = [];
	v_connTabControl.tag.change_active_database_call_running = false;

	initCreateTabFunctions();


	v_connTabControl.tag.createSnippetTab();
	v_connTabControl.tag.createWebsiteOuterTab(v_short_version,'/welcome');

	//v_connTabControl.tag.createServerMonitoringTab();


	/*if(!gv_desktopMode) {
		v_connTabControl.tag.createChatTab();
	}*/

	getDatabaseList(true);

	//Prevent "cannot edit" bug in ace editor
	$(document).on(
		'mousedown',
		'.ace_editor',
		function(p_event) {
			var v_textarea = this.querySelector('.ace_text-input');

			if(v_textarea != null) {
				v_textarea.blur();
				v_textarea.focus();
			}
		}
	);

	//Improve mouse wheel scrolling in grid div. Whitout this, it scrolls just 1 pixel at a time
	$(document).on(
		'wheel',
		'.ht_master > .wtHolder',
		function(p_event) {
			if(p_event.originalEvent.deltaY > 0) {
				this.scrollTop += 19;
			}
			else {
				this.scrollTop -= 19;
			}
		}
	)

	//Prevent dragging files to OmniDB's window
	window.addEventListener("dragover",function(e){
	  e = e || event;
	  e.preventDefault();
	},false);
	window.addEventListener("drop",function(e){
	  e = e || event;
	  e.preventDefault();
	},false);

	window.addEventListener("focus", function(event)
	{
		if (v_connTabControl.selectedTab.tag.mode=='connection') {
			if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='query')
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.focus();
			else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console')
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor_input.focus();
			else if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='edit')
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.focus();
		}
	}, false);

/*
	//WebSockets
	startChatWebSocket(2011, v_enable_omnichat);

	if(!v_enable_omnichat) {
		document.getElementById('div_chat').style.display = 'none';
	}
*/
	startQueryWebSocket();
});

/// <summary>
/// Retrieves database list.
/// </summary>
/// <param name="p_sel_id">Selection tag ID.</param>
/// <param name="p_filter">Filtering a specific database technology.</param>
function getDatabaseList(p_init, p_callback) {

	execAjax('/get_database_list/',
			JSON.stringify({}),
			function(p_return) {

				v_connTabControl.tag.selectHTML = p_return.v_data.v_select_html;
				v_connTabControl.tag.connections = p_return.v_data.v_connections;

				v_connTabControl.tag.selectGroupHTML = p_return.v_data.v_select_group_html;
				v_connTabControl.tag.groups = p_return.v_data.v_groups;

				if (p_init) {

					//v_connTabControl.createTab('+',false,v_connTabControl.tag.createConnTab,false);

					if (v_connTabControl.tag.connections.length>0) {

						//Create existing tabs
						var v_current_parent = null;
						var v_has_old_tabs = false;
						if (p_return.v_data.v_existing_tabs.length>0)
							v_has_old_tabs = true;

						for (var i=0; i < p_return.v_data.v_existing_tabs.length; i++) {
							if (v_current_parent == null || v_current_parent != p_return.v_data.v_existing_tabs[i].index) {
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

						if (!v_has_old_tabs)
							v_connTabControl.tag.createConnTab(v_connTabControl.tag.connections[0].v_conn_id);

					}
					else {
						var v_instance = new Tooltip($('#menu_connections'),{
					    title: 'Create your first connection!',
					    placement: "bottom",
					  });
						v_instance.show();
				    window.setTimeout(function() {
				        v_instance.dispose();
				    }, 4000);
					}

				}

				if (p_callback)
					p_callback();

			},
			null,
			'box');

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

/// <summary>
/// Changing selected database.
/// </summary>
/// <param name="p_value">Database ID.</param>
function changeDatabase(p_value) {

	//check if there are troublesome tabs
	checkBeforeChangeDatabase(
		function() {
			v_connTabControl.selectedTab.tag.dd_object.set("selectedIndex",v_connTabControl.selectedTab.tag.dd_selected_index);
		},
		function() {

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
			v_connTabControl.selectedTab.tag.dd_selected_index = v_connTabControl.selectedTab.tag.dd_object.selectedIndex;
			v_connTabControl.selectedTab.tag.selectedTitle = v_conn_object.v_alias;

			if (v_connTabControl.selectedTab.tag.selectedTitle!='')
				v_connTabControl.selectedTab.tag.tabTitle.innerHTML = '<img src="/static/OmniDB_app/images/' + v_connTabControl.selectedTab.tag.selectedDBMS + '_medium.png"/> ' + v_connTabControl.selectedTab.tag.selectedTitle + ' - ' + v_connTabControl.selectedTab.tag.selectedDatabase;
			else
				v_connTabControl.selectedTab.tag.tabTitle.innerHTML = '<img src="/static/OmniDB_app/images/' + v_connTabControl.selectedTab.tag.selectedDBMS + '_medium.png"/> ' + v_connTabControl.selectedTab.tag.selectedDatabase;


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
			else
				getTree(v_connTabControl.selectedTab.tag.divTree.id);

			adjustQueryTabObjects(true);
		});

}

function changeGroup(p_value) {
	//finding group object
	var v_group_object = null;
	for (var i=0; i<v_connTabControl.tag.groups.length; i++) {
		if (p_value==v_connTabControl.tag.groups[i].v_group_id) {
			v_group_object = v_connTabControl.tag.groups[i];
			break;
		}
	}
	if (!v_group_object) {
		v_group_object = v_connTabControl.tag.groups[0];
		v_connTabControl.tag.divSelectGroup.childNodes[0].value = 0;
	}

	v_connTabControl.selectedTab.tag.selectedGroupIndex = parseInt(p_value);

  //check if next group contains the currently selected connection
	var v_found = false;
	//first group contains all connections
	if (v_group_object.v_group_id==0) {
		v_found = true;
	}
	else {
		for (var i=0; i<v_group_object.conn_list.length; i++) {
			if (v_connTabControl.selectedTab.tag.selectedDatabaseIndex==v_group_object.conn_list[i]) {
				v_found = true;
				break;
			}
		}
	}

	//not found, check if there aren't troublesome tabs before changing selector
	if (!v_found) {
		for (var i=0; i < v_connTabControl.selectedTab.tag.tabControl.tabList.length; i++) {

			var v_tab = v_connTabControl.selectedTab.tag.tabControl.tabList[i];
			if (v_tab.tag!=null)
				if (v_tab.tag.mode=='edit' || v_tab.tag.mode=='alter' || v_tab.tag.mode=='debug' || v_tab.tag.mode=='monitor_dashboard' || v_tab.tag.mode=='data_mining') {
					showAlert("Before changing group please close any tab of the selected connection that belongs to the following types: <br/><br/><b>Edit Data<br/><br/>Alter Table<br/><br/>Function Debugging<br/><br/>Monitoring Dashboard<br/><br/>Advanced Object Search.");
					v_connTabControl.selectedTab.tag.dd_group_object.set("selectedIndex",v_connTabControl.selectedTab.tag.dd_group_selected_index);
					return null;
				}
		}
	}

	//Filtering connection list
	var v_tag = v_connTabControl.selectedTab.tag;
	v_tag.divSelectDB.innerHTML = v_connTabControl.tag.selectHTML;
	var v_select = v_tag.divSelectDB.childNodes[0];

	//filter if not default group
	if (v_group_object.v_group_id!=0) {
		for (var i=v_select.childNodes.length-1; i>=0; i--) {
			var v_option = v_select.childNodes[i];

			var v_found_conn = false;
			for (var j=0; j<v_group_object.conn_list.length; j++) {
				if (v_option.value==v_group_object.conn_list[j]) {
					v_found_conn = true;
					if (!v_found) {
						changeDatabase(v_option.value);
						v_found = true;
					}
					break;
				}
			}
			if (!v_found_conn) {
				v_option.parentNode.removeChild(v_option);
			}
		}
	}

	//Rebuild selector
	v_tag.divSelectDB.childNodes[0].value = v_tag.selectedDatabaseIndex;
	v_tag.dd_object = $(v_tag.divSelectDB.childNodes[0]).msDropDown().data("dd");
	v_tag.dd_selected_index = v_tag.dd_object.selectedIndex;


	v_connTabControl.selectedTab.tag.dd_group_selected_index = v_connTabControl.selectedTab.tag.dd_group_object.selectedIndex;
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
/// Renames tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function renameTab(p_tab) {

	showConfirm('<input id="tab_name"/ value="' + p_tab.tag.tab_title_span.innerHTML + '" style="width: 200px;">',
	            function() {

					renameTabConfirm(p_tab,document.getElementById('tab_name').value);

	            });

}

/// <summary>
/// Renames tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
/// <param name="p_name">New name.</param>
function renameTabConfirm(p_tab, p_name) {

	p_tab.tag.tab_title_span.innerHTML=p_name;

}

/// <summary>
/// Removes tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function removeTab(p_tab) {

	if (p_tab.tag.ht!=null) {
		p_tab.tag.ht.destroy();
		p_tab.tag.div_result.innerHTML = '';
	}

	if (p_tab.tag.editor!=null)
		p_tab.tag.editor.destroy();

	if (p_tab.tag.mode=='query' || p_tab.tag.mode=='edit' || p_tab.tag.mode=='console') {
		var v_message_data = { tab_id: p_tab.tag.tab_id, tab_db_id: null };
		if (p_tab.tag.mode=='query')
			v_message_data.tab_db_id = p_tab.tag.tab_db_id;

		sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CloseTab, [v_message_data], false, null);
	}
	p_tab.removeTab();

}

/// <summary>
/// Redefines vertical resize line position.
/// </summary>
function verticalLinePosition(p_event) {
	document.getElementById('vertical-resize-line').style.top = p_event.pageY;
}

function resizeWindow(){
	refreshHeights(true);
}

var resizeTimeout;
$(window).resize(function() {
	clearTimeout(resizeTimeout);
	resizeTimeout = setTimeout(resizeWindow, 200);
});

function refreshTreeHeight() {
	var v_tag = v_connTabControl.selectedTab.tag;

	if (v_tag.currTreeTab=='properties') {
		var v_height  = window.innerHeight - $(v_tag.divProperties).offset().top - 8;
		v_tag.divProperties.style.height = v_height + "px";
		v_tag.gridProperties.render();
		v_tag.gridProperties.render();
	}
	else if (v_tag.currTreeTab=='ddl') {
		var v_height  = window.innerHeight - $(v_tag.divDDL).offset().top - 8;
		v_tag.divDDL.style.height = v_height + "px";
		v_tag.ddlEditor.resize();
	}

}

function refreshHeights(p_all) {

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

	//If inner tab exists
	if (v_connTabControl.selectedTab.tag.tabControl != null && v_connTabControl.selectedTab.tag.tabControl.selectedTab) {
		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

		//Snippet tab, adjust editor only
		if (v_tab_tag.mode=='snippet') {
			v_tab_tag.editorDiv.style.height = window.innerHeight - $(v_tab_tag.editorDiv).offset().top - 62 + 'px';
			v_tab_tag.editor.resize();
		}
		else if (v_tab_tag.mode=='monitor_unit') {
			var v_new_height = window.innerHeight - $(v_tab_tag.editorDataDiv).offset().top - 364 + 'px';
			v_tab_tag.editorDiv.style.height = v_new_height;
			v_tab_tag.editorDataDiv.style.height = v_new_height;
			v_tab_tag.editor.resize();
			v_tab_tag.editor_data.resize();
		}
		else if (v_tab_tag.mode=='query') {
			if (v_tab_tag.currQueryTab=='data') {
				v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 15 + 'px';
				if (v_tab_tag.ht!=null)
					v_tab_tag.ht.render();
				if(v_tab_tag.editor != null)
						v_tab_tag.editor.resize();
			}
			else if (v_tab_tag.currQueryTab=='message') {
				v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 15 + 'px';
			}
			else if (v_tab_tag.currQueryTab=='explain') {
				v_tab_tag.div_explain.style.height = window.innerHeight - $(v_tab_tag.div_explain).offset().top - 15 + 'px';
			}
		}
		else if (v_tab_tag.mode=='console') {
			v_tab_tag.div_console.style.height = window.innerHeight - $(v_tab_tag.div_console).offset().top - parseInt(v_tab_tag.div_result.style.height,10) - 59 + 'px';
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
			v_tab_tag.iframe.style.height = window.innerHeight - $(v_tab_tag.iframe).offset().top - 4 + "px";
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

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeVertical(event) {
	var v_verticalLine = document.createElement('div');
	v_verticalLine.id = 'vertical-resize-line';
	document.body.appendChild(v_verticalLine);

	document.body.addEventListener(
		'mousemove',
		verticalLinePosition
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
		verticalLinePosition
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

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	if(v_tab_tag.editor != null) {
		v_tab_tag.editor.resize();
	}

	if (v_tab_tag.mode=='query') {
		if (v_tab_tag.currQueryTab=='data') {
			v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 29 + 'px';
			if (v_tab_tag.ht!=null)
				v_tab_tag.ht.render();
		}
		else if (v_tab_tag.currQueryTab=='message') {
			v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 29 + 'px';
		}
		else if (v_tab_tag.currQueryTab=='explain') {
			v_tab_tag.div_explain.style.height = window.innerHeight - $(v_tab_tag.div_explain).offset().top - 29 + 'px';
		}
	}
	else if (v_tab_tag.mode=='debug') {
		v_tab_tag.editor.resize();
		if (v_tab_tag.currDebugTab=='variable') {
			v_tab_tag.div_variable.style.height = window.innerHeight - $(v_tab_tag.div_variable).offset().top - 29 + 'px';
			if (v_tab_tag.htVariable!=null)
				v_tab_tag.htVariable.render();
		}
		if (v_tab_tag.currDebugTab=='parameter') {
			v_tab_tag.div_parameter.style.height = window.innerHeight - $(v_tab_tag.div_parameter).offset().top - 29 + 'px';
			if (v_tab_tag.htParameter!=null)
				v_tab_tag.htParameter.render();
		}
		if (v_tab_tag.currDebugTab=='result') {
			v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 29 + 'px';
			if (v_tab_tag.htResult!=null)
				v_tab_tag.htResult.render();
		}
		else if (v_tab_tag.currDebugTab=='message') {
			v_tab_tag.div_notices.style.height = window.innerHeight - $(v_tab_tag.div_notices).offset().top - 29 + 'px';
		}
		else if (v_tab_tag.currDebugTab=='statistics') {
			v_tab_tag.div_statistics.style.height = window.innerHeight - $(v_tab_tag.div_statistics).offset().top - 29 + 'px';
			if (v_tab_tag.chart!=null)
				v_tab_tag.chart.update();
		}
	}
	else if (v_tab_tag.mode=='edit') {
		if (v_tab_tag.editDataObject.ht!=null) {
			v_tab_tag.editDataObject.ht.render();
		}
	}
	else if (v_tab_tag.mode=='console') {
		v_tab_tag.editor_input.resize();
		v_tab_tag.editor_console.resize();
	}
	else if(v_tab_tag.mode == 'data_mining') {
		if(v_tab_tag.currQueryTab == 'data') {
			v_tab_tag.div_result.style.height = window.innerHeight - $(v_tab_tag.div_result).offset().top - 29 + 'px';
		}
	}
}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeTreeVertical(event) {
	var v_verticalLine = document.createElement('div');
	v_verticalLine.id = 'vertical-resize-line';
	document.body.appendChild(v_verticalLine);

	document.body.addEventListener(
		'mousemove',
		verticalLinePosition
	)

	v_start_height = event.screenY;
	document.body.addEventListener("mouseup", resizeTreeVerticalEnd);

}

/// <summary>
/// Resize SQL editor and result div.
/// </summary>
function resizeTreeVerticalEnd(event) {

	document.body.removeEventListener("mouseup", resizeTreeVerticalEnd);
	document.getElementById('vertical-resize-line').remove();

	document.body.removeEventListener(
		'mousemove',
		verticalLinePosition
	)

	var v_height_diff = event.screenY - v_start_height;

	var v_tag = v_connTabControl.selectedTab.tag;

	var v_tree_div = v_tag.divTree;
	var v_result_div = null;

	if (v_tag.currTreeTab=='properties') {
		v_result_div = v_tag.divProperties;
		v_tag.gridProperties.render();
		v_tag.gridProperties.render();
	}
	else if (v_tag.currTreeTab=='ddl') {
		v_result_div = v_tag.divDDL;
		v_tag.ddlEditor.resize();
	}


	if (v_height_diff < 0) {
		if (Math.abs(v_height_diff) > parseInt(v_tree_div.clientHeight, 10))
		 v_height_diff = parseInt(v_tree_div.clientHeight, 10)*-1 + 10;
	}
	else {
		if (Math.abs(v_height_diff) > parseInt(v_result_div.clientHeight, 10))
		 v_height_diff = parseInt(v_result_div.clientHeight, 10) - 10;
	}

	v_tree_div.style.height = parseInt(v_tree_div.clientHeight, 10) + v_height_diff + 'px';
	v_result_div.style.height = parseInt(v_result_div.clientHeight, 10) - v_height_diff + 'px';

	if (v_tag.currTreeTab=='properties') {
		var v_height  = window.innerHeight - $(v_tag.divProperties).offset().top - 21;
		v_tag.divProperties.style.height = v_height + "px";
		v_tag.gridProperties.render();
		v_tag.gridProperties.render();
	}
	else if (v_tag.currTreeTab=='ddl') {
		var v_height  = window.innerHeight - $(v_tag.divDDL).offset().top - 21;
		v_tag.divDDL.style.height = v_height + "px";
		v_tag.ddlEditor.resize();
	}

}


/// <summary>
/// Maximize SQL Editor.
/// </summary>
function maximizeEditor() {

	var v_editor_div = document.getElementById(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editorDivId);
	var v_result_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

	var v_height_diff = parseInt(v_result_div.style.height, 10) - 10;

	v_editor_div.style.height = parseInt(v_editor_div.style.height, 10) + v_height_diff + 'px';
	v_result_div.style.height = parseInt(v_result_div.style.height, 10) - v_height_diff + 'px';

	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();

}

/// <summary>
/// Minimize SQL Editor.
/// </summary>
function minimizeEditor() {

	var v_editor_div = document.getElementById(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editorDivId);
	var v_result_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result;

	var v_height_diff = parseInt(v_editor_div.style.height, 10) - 10;


	v_result_div.style.height = (parseInt(v_result_div.style.height, 10) + parseInt(v_editor_div.style.height, 10) - 300) + 'px';

	v_editor_div.style.height = '300px';

	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.resize();

}

/// <summary>
/// Redefines horizontal resize line position.
/// </summary>
function horizontalLinePosition(p_event) {
	document.getElementById('horizontal-resize-line').style.left = p_event.pageX;
}

/// <summary>
/// Resize Tab.
/// </summary>
function resizeHorizontal(event) {
	var v_horizontalLineBase = document.createElement('div');
	v_horizontalLineBase.id = 'horizontal-resize-line-base';
	v_horizontalLineBase.style.position = 'absolute';
	v_horizontalLineBase.style.width = '100%';
	v_horizontalLineBase.style.height = '100%';
	v_horizontalLineBase.style.left = '0';
	v_horizontalLineBase.style.top = '0';
	var v_horizontalLine = document.createElement('div');
	v_horizontalLine.id = 'horizontal-resize-line';
	document.body.appendChild(v_horizontalLineBase);
	v_horizontalLineBase.appendChild(v_horizontalLine)

	document.body.addEventListener(
		'mousemove',
		horizontalLinePosition
	)

	document.body.addEventListener("mouseup", resizeHorizontalEnd);
	v_start_width = event.screenX;
}

/// <summary>
/// Resize Tab.
/// </summary>
function resizeHorizontalEnd(event) {
	document.body.removeEventListener("mouseup", resizeHorizontalEnd);
	document.getElementById('horizontal-resize-line-base').remove();

	document.body.removeEventListener(
		'mousemove',
		horizontalLinePosition
	)

	var v_width_diff = event.screenX - v_start_width;

	v_width_diff = Math.ceil(v_width_diff/window.innerWidth*100);

	var v_left_div = v_connTabControl.selectedTab.tag.divLeft;
	var v_right_div = v_connTabControl.selectedTab.tag.divRight;

	v_left_div.style.width = parseInt(v_left_div.style.width, 10) + v_width_diff + '%';
	v_right_div.style.width = parseInt(v_right_div.style.width, 10) - v_width_diff + '%';

	if (v_connTabControl.selectedTab.tag.tabControl.selectedTab!=null) {

		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

		if (v_tab_tag.mode=='query') {
			v_tab_tag.editor.resize();
			if (v_tab_tag.currQueryTab=='data') {
				if (v_tab_tag.ht!=null)
					v_tab_tag.ht.render();
			}
		}
		if (v_tab_tag.mode=='console') {
			v_tab_tag.editor_input.resize();
			v_tab_tag.editor_console.resize();
		}
		if (v_tab_tag.mode=='debug') {
			v_tab_tag.editor.resize();
			if (v_tab_tag.currDebugTab=='parameter') {
				if (v_tab_tag.htParameter!=null)
					v_tab_tag.htParameter.render();
			}
			else if (v_tab_tag.currDebugTab=='variable') {
				if (v_tab_tag.htVariable!=null)
					v_tab_tag.htVariable.render();
			}
			else if (v_tab_tag.currDebugTab=='result') {
				if (v_tab_tag.htResult!=null)
					v_tab_tag.htResult.render();
			}
			else if (v_tab_tag.currDebugTab=='statistics') {
				if (v_tab_tag.chart!=null)
					v_tab_tag.chart.update();
			}
		}
		else if (v_tab_tag.mode=='edit') {
			v_tab_tag.editor.resize();
			if (v_tab_tag.editDataObject.ht!=null)
				v_tab_tag.editDataObject.ht.render();
		}
		else if (v_tab_tag.mode=='snippet') {
			v_tab_tag.editor.resize();
		}
		else if (v_tab_tag.mode=='monitor_grid' || v_tab_tag.mode=='query_history') {
			if (v_tab_tag.ht!=null) {
				v_tab_tag.ht.render();
			}
		}
		else if (v_tab_tag.mode=='alter') {
	        v_tab_tag.tabControl.selectedTab.tag.ht.render();
		}

	}

	if (v_connTabControl.selectedTab.tag.TreeTabControl!=null) {
		var v_conn_tab_tag = v_connTabControl.selectedTab.tag;
		if (v_conn_tab_tag.currTreeTab=='properties') {
			v_conn_tab_tag.gridProperties.render();
			v_conn_tab_tag.gridProperties.render();
		}
		else if (v_conn_tab_tag.currTreeTab=='ddl') {
			v_conn_tab_tag.ddlEditor.resize();
		}
	}

	//Hooks
  if (v_connTabControl.tag.hooks.windowResize.length>0) {
    for (var i=0; i<v_connTabControl.tag.hooks.windowResize.length; i++)
      v_connTabControl.tag.hooks.windowResize[i]();
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
							name: 'cose',
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
						},
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
/// Hides command history window.
/// </summary>
function hideCommandsLog() {

	$('#div_commands_log').removeClass('isActive');

}

/// <summary>
/// Refreshes monitoring tab.
/// </summary>
function refreshMonitoring(p_tab_tag) {

	if (!p_tab_tag)
		var p_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	execAjax('/refresh_monitoring/',
			JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
											"p_tab_id": v_connTabControl.selectedTab.id,
											"p_query": p_tab_tag.query}),
			function(p_return) {

				var v_data = p_return.v_data;

				if (p_tab_tag.ht!=null) {
					p_tab_tag.ht.destroy();
					p_tab_tag.ht = null;
				}

				p_tab_tag.query_info.innerHTML = v_data.v_query_info;

				var columnProperties = [];

				var v_fixedColumnsLeft = 0;

				if (p_tab_tag.actions!=null) {
					v_fixedColumnsLeft = 1;
					for (var i=0; i<v_data.v_data.length; i++) {
						var v_actions_html = '';
						for (var j=0; j<p_tab_tag.actions.length; j++) {
							v_actions_html += '<i class="' + p_tab_tag.actions[j].icon + '" onclick="monitoringAction(' + i + ',&apos;' + p_tab_tag.actions[j].action + '&apos;)">';
						}
						v_data.v_data[i].unshift(v_actions_html);
					}

					var col = new Object();
			    col.readOnly = true;
			    col.title =  'Actions';
					col.renderer = 'html';
					columnProperties.push(col);

				}


				for (var i = 0; i < v_data.v_col_names.length; i++) {
			    var col = new Object();
			    col.readOnly = true;
			    col.title =  v_data.v_col_names[i];
					columnProperties.push(col);
				}

				p_tab_tag.ht = new Handsontable(p_tab_tag.div_result,
				{
					data: v_data.v_data,
					columns : columnProperties,
					colHeaders : true,
					rowHeaders : true,
					fixedColumnsLeft: v_fixedColumnsLeft,
					fillHandle:false,
					//copyRowsLimit : 1000000000,
					//copyColsLimit : 1000000000,
                    copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
					manualColumnResize: true,
					contextMenu: {
						callback: function (key, options) {
							if (key === 'view_data') {
							  	editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),false);
							}
							else if (key === 'copy') {
								this.selectCell(options[0].start.row,options[0].start.col,options[0].end.row,options[0].end.col);
								document.execCommand('copy');
							}
						},
						items: {
							"copy": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-copy cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Copy</div>'},
							"view_data": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
						}
				    },
			        cells: function (row, col, prop) {
					    var cellProperties = {};
					    if (row % 2 == 0)
							cellProperties.renderer = blueHtmlRenderer;
						else
							cellProperties.renderer = whiteHtmlRenderer;
					    return cellProperties;
					}
				});

			},
			function(p_return) {
				if (p_return.v_data.password_timeout) {
					showPasswordPrompt(
						v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
						function() {
							refreshMonitoring(p_tab_tag);
						},
						null,
						p_return.v_data.message
					);
				}
				else {
					showError(p_return.v_data);
				}
			},
			'box',
			true);

}

function monitoringAction(p_row_index, p_function) {
	var v_fn = window[p_function];
	var v_row_data = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.ht.getDataAtRow(p_row_index);
	v_row_data.shift();
	if(typeof v_fn === 'function') {
		v_fn(v_row_data);
	}
}

function addLoadingCursor() {
	document.body.classList.add("cursor_loading");
}

function removeLoadingCursor() {
	document.body.classList.remove("cursor_loading");
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

function showMenuNewTabOuter(e) {

	var v_option_list = [];
	//Hooks
	if (v_connTabControl.tag.hooks.outerTabMenu.length>0) {
		for (var i=0; i<v_connTabControl.tag.hooks.outerTabMenu.length; i++)
			v_option_list = v_option_list.concat(v_connTabControl.tag.hooks.outerTabMenu[i]());
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
	]

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
		for (var i=0; i<v_connTabControl.tag.hooks.innerTabMenu.length; i++)
			v_option_list = v_option_list.concat(v_connTabControl.tag.hooks.innerTabMenu[i]());
	}

	customMenu(
		{
			x:e.clientX+5,
			y:e.clientY+5
		},
		v_option_list,
		null);

}

function exportData() {

	var v_query = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
	var v_export_type = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_export_type.value;
	querySQL(0, true, v_query, exportDataReturn,true,v_query,'export_' + v_export_type,true);
}

function exportDataReturn(p_data) {
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.selectDataTabFunc();
	var v_text = '<div style="font-size: 14px;">The file is ready. <a class="link_text" href="' + p_data.v_data.v_filename + '" download="'+ p_data.v_data.v_downloadname + '">Save</a></div>';
	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.innerHTML = v_text;
}
