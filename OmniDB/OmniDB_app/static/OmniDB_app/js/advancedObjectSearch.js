function queryAdvancedObjectSearch(p_data, p_callback = null) {
	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if(v_state != v_queryState.Idle) {
		showAlert('Tab with activity in progress.');
	}
	else {
		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
		//v_tab_tag.queryTabControl.tabList[0].elementDiv.innerHTML = '';
		var v_db_index  = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
		var v_tab_loading_span = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_loading_span;
		var v_tab_close_span = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_close_span;

		//Change to run mode if database index changed
		if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDatabaseIndex == null || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDatabaseIndex != v_connTabControl.selectedTab.tag.selectedDatabaseIndex) {
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDatabaseIndex = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
		}

		var v_message_data = {
			v_sql_cmd : '',
			v_db_index: v_db_index,
			v_conn_tab_id: v_connTabControl.selectedTab.id,
			v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
			v_tab_db_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_db_id,
            text: p_data.text,
            regex: p_data.regex,
            caseSensitive: p_data.caseSensitive,
            categoryList: p_data.categoryList,
            schemaList: p_data.schemaList,
			dataCategoryFilter: p_data.dataCategoryFilter
		};

		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state = v_queryState.Executing;

		var start_time = new Date().getTime();

		var d = new Date,
        dformat = [(d.getMonth()+1).padLeft(),
                   d.getDate().padLeft(),
                   d.getFullYear()].join('/') +' ' +
                  [d.getHours().padLeft(),
                   d.getMinutes().padLeft(),
                   d.getSeconds().padLeft()].join(':');

		v_tab_tag.tab_loading_span.style.display = '';
		v_tab_tag.tab_stub_span.style.display = 'none';
		v_tab_tag.bt_cancel.style.display = '';

		var v_context = {
			tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
			start_time: new Date().getTime(),
			start_datetime: dformat,
			database_index: v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
			callback: p_callback,
			acked: false,
            mode: 0
		}

		v_context.tab_tag.context = v_context;

		if (p_callback==null) {
			if (v_context.tab_tag.ht!=null) {
				v_context.tab_tag.ht.destroy();
				v_context.tab_tag.ht = null;
			}

			v_context.tab_tag.div_result.innerHTML = '';
			refreshHeights(true);
		}

		v_context.tab_tag.query_info.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Running...</b>';

		sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.AdvancedObjectSearch, v_message_data, false, v_context);

		setTimeout(function() {
			if (!v_context.acked) {
				cancelSQLTab(v_context.tab_tag);
				showAlert('No response from query server.');
			}
		},20000);
	}
}

function checkAdvancedObjectSearchStatus(p_tab) {
	if(p_tab.tag.state == v_queryState.Ready) {
		advancedObjectSearchReturnRender(p_tab.tag.data, p_tab.tag.context);
	}
}

function advancedObjectSearchReturn(p_message, p_context) {
	//If data mining wasn't canceled already
	if(p_context.tab_tag.state!=v_queryState.Idle) {

		if(p_context.tab_tag.tab_id == p_context.tab_tag.tabControl.selectedTab.id && p_context.tab_tag.connTab.id == p_context.tab_tag.connTab.tag.connTabControl.selectedTab.id) {
			advancedObjectSearchReturnRender(p_message, p_context);
		}
		else {
			p_context.tab_tag.state = v_queryState.Ready;
			p_context.tab_tag.context = p_context;
			p_context.tab_tag.data = p_message;

			p_context.tab_tag.tab_loading_span.style.display = 'none';
			p_context.tab_tag.tab_check_span.style.display = '';
		}
	}
}

function advancedObjectSearchReturnRender(p_message, p_context) {
	p_context.tab_tag.state = v_queryState.Idle;
	p_context.tab_tag.context = null;
	p_context.tab_tag.data = null;

	var v_div_result = p_context.tab_tag.div_result;
	var v_query_info = p_context.tab_tag.query_info;

	if(p_message.v_error) {
		v_div_result.innerHTML = '<div class="error_text">' + p_message.v_data.message + '</div>';
		v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
	}
	else {
		v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
		v_div_result.innerHTML = '';

		var v_sortable = [];

		for(v_key in p_message.v_data.v_result) {
			v_sortable.push([v_key, p_message.v_data.v_result[v_key]]);
		}

		v_sortable.sort(function(a, b) {
			if(b[1]['count'] != a[1]['count']) {
				return b[1]['count'] - a[1]['count'];
			}
			else {
				var v_string1 = a[0].toLowerCase();
				var v_string2 = b[0].toLowerCase();

				if(v_string1 < v_string2) {
					return -1;
				}
				else if(v_string1 > v_string2) {
					return 1;
				}
				else {
					return 0;
				}
			}
		});

		p_message.v_data.v_result = {};

		for(var i = 0; i < v_sortable.length; i++) {
			p_message.v_data.v_result[v_sortable[i][0]] = v_sortable[i][1];
		}

		if('Data' in p_message.v_data.v_result) {
			var v_sortable2 = [];

			for(v_key in p_message.v_data.v_result['Data']['result']) {
				v_sortable2.push([v_key, p_message.v_data.v_result['Data']['result'][v_key]]);
			}

			v_sortable2.sort(function(a, b) {
				if(b[1]['count'] != a[1]['count']) {
					return b[1]['count'] - a[1]['count'];
				}
				else {
					var v_string1 = a[0].toLowerCase();
					var v_string2 = b[0].toLowerCase();

					if(v_string1 < v_string2) {
						return -1;
					}
					else if(v_string1 > v_string2) {
						return 1;
					}
					else {
						return 0;
					}
				}
			});

			p_message.v_data.v_result['Data']['result'] = {};

			for(var i = 0; i < v_sortable2.length; i++) {
				p_message.v_data.v_result['Data']['result'][v_sortable2[i][0]] = v_sortable2[i][1];
			}
		}

		var v_context_menu = {
	        'cm_see_details': {
	            elements: [{
	                text: 'See More',
	                icon: 'fas cm-all fa-search',
	                action: function(p_node) {
						tabSQLTemplate('Search - ' + p_node.tag.key, p_node.tag.sql, false);
	                }
	            }]
	        },
			'cm_see_error': {
				elements: [{
					text: 'See Errors',
					icon: 'fas cm-all fa-search',
					action: function(p_node) {
						showError(p_node.tag.exception);
					}
				}]
			}
		};

		var v_tree = createTree(v_div_result.id, '#fcfdfd', v_context_menu);
		var v_num_nodes = 0;

		for(v_key in p_message.v_data.v_result) {
			if (p_message.v_data.v_result[v_key]['count'] > 0) {
				if(v_key == 'Data') {
					var v_dataMatches = '';
					var v_data_cm = null;

					if (p_message.v_data.v_result[v_key]['count'] == 1)
						v_dataMatches = v_key + ' (1 match)';
					else
						v_dataMatches = v_key + ' (' + p_message.v_data.v_result[v_key]['count'] + ' matches)';

					if(p_message.v_data.v_result[v_key]['exception'] != null) {
						v_data_cm = 'cm_see_error';
						v_dataMatches = '<span style="color:red;">' + v_dataMatches + ' (Error)</span>';
					}

					var v_node = v_tree.createNode(
						v_dataMatches,
						false,
						'fas node-all fa-search node-advanced-object-search',
						null,
						p_message.v_data.v_result[v_key],
						v_data_cm
					);

					v_node.tag.key = v_key;

					for(v_key2 in p_message.v_data.v_result[v_key]['result']) {
						if(p_message.v_data.v_result[v_key]['result'][v_key2].count > 0) {
							var v_matches = '';
							var v_cm = 'cm_see_details';

							if (p_message.v_data.v_result[v_key]['result'][v_key2].count == 1)
								v_matches = v_key2 + ' (1 match)';
							else
								v_matches = v_key2 + ' (' + p_message.v_data.v_result[v_key]['result'][v_key2].count + ' matches)';

							if(p_message.v_data.v_result[v_key]['result'][v_key2]['exception'] != null) {
								v_cm = 'cm_see_error';
								v_matches = '<span style="color:red;">' + v_matches + ' (Error)</span>';
							}

							var v_childNode = v_node.createChildNode(
								v_matches,
								false,
								'fas node-all fa-search node-advanced-object-search',
								p_message.v_data.v_result[v_key]['result'][v_key2],
								v_cm
							);
							v_num_nodes++;

							v_childNode.tag.key = v_key2;
						}
					}
				}
				else {
					var v_matches = '';
					var v_cm = 'cm_see_details';

					if (p_message.v_data.v_result[v_key].count == 1)
						v_matches = v_key + ' (1 match)';
					else
						v_matches = v_key + ' (' + p_message.v_data.v_result[v_key].count + ' matches)';

					if(p_message.v_data.v_result[v_key]['exception'] != null) {
						v_cm = 'cm_see_error';
						v_matches = '<span style="color:red;">' + v_matches + ' (Error)</span>';
					}

					var v_node = v_tree.createNode(
						v_matches,
						false,
						'fas node-all fa-search node-advanced-object-search',
						null,
						p_message.v_data.v_result[v_key],
						v_cm
					);
					v_num_nodes++;

					v_node.tag.key = v_key;
				}
			}
		}

		if (v_num_nodes == 0) {
			var v_node = v_tree.createNode(
				'Advanced Object Search found no matches.',
				false,
				'fas node-all fa-search node-advanced-object-search',
				null,
				'no_matches',
				null
			);
		}

		v_tree.drawTree();
	}

	p_context.tab_tag.tab_loading_span.style.display = 'none';
	p_context.tab_tag.tab_check_span.style.display = 'none';
	p_context.tab_tag.tab_stub_span.style.display = '';
	p_context.tab_tag.bt_cancel.style.display = 'none';
	refreshHeights(true);
}
