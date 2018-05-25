function queryDataMining(p_data, p_callback = null) {
	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if(v_state != v_queryState.Idle) {
		showAlert('Tab with activity in progress.');
	}
	else {
		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
		v_tab_tag.queryTabControl.tabList[0].elementDiv.innerHTML = '';
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
            schemaList: p_data.schemaList
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
		}

		v_context.tab_tag.query_info.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Running...</b>';

		sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.DataMining, v_message_data, false, v_context);

		setTimeout(function() {
			if (!v_context.acked) {
				cancelSQLTab(v_context.tab_tag);
				showAlert('No response from query server.');
			}
		},20000);
	}
}

function checkDataMiningStatus(p_tab) {
	if(p_tab.tag.state == v_queryState.Ready) {
		dataMiningReturnRender(p_tab.tag.data, p_tab.tag.context);
	}
}

function dataMiningReturn(p_message, p_context) {
	//If data mining wasn't canceled already
	if(p_context.tab_tag.state!=v_queryState.Idle) {

		if(p_context.tab_tag.tab_id == p_context.tab_tag.tabControl.selectedTab.id && p_context.tab_tag.connTab.id == p_context.tab_tag.connTab.tag.connTabControl.selectedTab.id) {
			dataMiningReturnRender(p_message, p_context);
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

function dataMiningReturnRender(p_message, p_context) {
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
		v_div_result.innerHTML = '<div class="query_info"></div>';

		var v_context_menu = {
	        'cm_see_details': {
	            elements: [{
	                text: 'See More',
	                icon: '/static/OmniDB_app/images/explain.png',
	                action: function(p_node) {
						tabSQLTemplate('Data Mining - ' + p_node.tag.key, p_node.tag.sql, false);
	                }
	            }]
	        }
		};

		var v_tree = createTree(p_context.tab_tag.queryTabControl.tabList[0].elementDiv.id, '#fcfdfd', v_context_menu);

		for(v_key in p_message.v_data.v_result) {
			if(v_key == 'Data') {
				var v_count = 0;

				var v_node = v_tree.createNode(
					v_key,
					false,
					'/static/OmniDB_app/images/data_mining.png',
					null,
					p_message.v_data.v_result[v_key],
					null
				);

				v_node.tag.key = v_key;

				for(v_key2 in p_message.v_data.v_result[v_key]) {
					if(p_message.v_data.v_result[v_key][v_key2].count > 0) {
						var v_matches = '';
						v_count += p_message.v_data.v_result[v_key][v_key2].count;

						switch(p_message.v_data.v_result[v_key][v_key2].count) {
							case 1: {
								v_matches = '(1 match)';
								break;
							}
							default: {
								v_matches = '(' + p_message.v_data.v_result[v_key][v_key2].count + ' matches)';
								break;
							}
						}

						var v_childNode = v_node.createChildNode(
							v_key2 + ' ' + v_matches,
							false,
							'/static/OmniDB_app/images/data_mining.png',
							p_message.v_data.v_result[v_key][v_key2],
							'cm_see_details'
						);

						v_childNode.tag.key = v_key2;
					}
				}

				var v_dataMatches = '';

				switch(v_count) {
					case 0: {
						v_dataMatches = '(No match)';
						break;
					}
					case 1: {
						v_dataMatches = '(1 match)';
						break;
					}
					default: {
						v_dataMatches = '(' + v_count + ' matches)';
						break;
					}
				}

				v_node.text = v_key + ' ' + v_dataMatches;
			}
			else {
				var v_matches = '';

				switch(p_message.v_data.v_result[v_key].count) {
					case 0: {
						v_matches = '(No match)';
						break;
					}
					case 1: {
						v_matches = '(1 match)';
						break;
					}
					default: {
						v_matches = '(' + p_message.v_data.v_result[v_key].count + ' matches)';
						break;
					}
				}

				var v_node = v_tree.createNode(
					v_key + ' ' + v_matches,
					false,
					'/static/OmniDB_app/images/data_mining.png',
					null,
					p_message.v_data.v_result[v_key],
					'cm_see_details'
				);

				v_node.tag.key = v_key;
			}
		}

		v_tree.drawTree();
	}

	p_context.tab_tag.tab_loading_span.style.display = 'none';
	p_context.tab_tag.tab_check_span.style.display = 'none';
	p_context.tab_tag.tab_stub_span.style.display = '';
	p_context.tab_tag.bt_cancel.style.display = 'none';
}
