function queryDataMining(p_data, p_callback = null) {
	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if(v_state != v_queryState.Idle) {
		showAlert('Tab with activity in progress.');
	}
	else {
		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
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

function dataMiningReturn(p_message, p_context) {
	console.log(p_message);
	console.log(p_context);
	console.log('kkk');

	var v_div_result = p_context.tab_tag.div_result;
	var v_query_info = p_context.tab_tag.query_info;

	if(p_message.v_error) {
		v_div_result.innerHTML = '<div class="error_text">' + p_message.v_data.message + '</div>';
		v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
	}
	else {
		v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
		v_div_result.innerHTML = '<div class="query_info">Done.</div>';

		var tree = createTree(p_div, '#fcfdfd', context_menu);
	}
}
