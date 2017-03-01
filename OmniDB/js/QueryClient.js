/// <summary>
/// Transaction codes of client requests.
/// </summary>
var v_queryRequestCodes = {
	Login: '0',
	Query: '1',
	Execute: '2',
	Script: '3'
}

/// <summary>
/// Transaction codes of server responses.
/// </summary>
var v_queryResponseCodes = {
	LoginResult: '0',
	QueryResult: '1'
}

/// <summary>
/// The variable that will receive the WebSocket object.
/// </summary>
var v_queryWebSocket;

/// <summary>
/// Starts query client
/// </summary>
/// <param name="p_port">Port where chat will listen for connections.</param>
function startQueryWebSocket(p_port) {
	v_queryWebSocket  = createWebSocket(
		'ws://' + window.location.hostname,
		p_port,
		function(p_event) {//Open
			sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Login, v_user_id, false);
		},
		function(p_message, p_context) {//Message
			var v_message = p_message;

			if(v_message.v_error) {
				querySQLReturn(v_message,p_context);
				return;
			}

			switch(v_message.v_code) {
				case parseInt(v_queryResponseCodes.QueryResult): {

					querySQLReturn(v_message,p_context);
					
					break;
				}
				default: {
					break;
				}
			}
		},
		function(p_event) {//Close
			//showError('The connection with query server was closed.<br>WebSocket error code: ' + p_event.code + '.');
			startQueryWebSocket(p_port);
		},
		function(p_event) {//Error
			//showError('An error has occurred during the communication with the chat server.');
		}
	);

}

function querySQL() {

	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if (v_state!=0) {
		showAlert('Tab with activity in progress.');
	}
	else {

		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state = 1;

		var v_sql_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
		var v_sel_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value;
		var v_db_index  = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
		var v_tab_loading_span = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_loading_span;
		var v_tab_close_span = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_close_span;


		var v_message_data = {
			v_sql_cmd : v_sql_value,
			v_cmd_type: v_sel_value,
			v_db_index: v_db_index

		}

		if (v_sql_value=='') {
			showAlert('Please provide a string.');
		}
		else {

			var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_sql": v_sql_value, "p_select_value" : v_sel_value});

			var start_time = new Date().getTime();

			v_tab_loading_span.style.display = '';
			v_tab_close_span.style.display = 'none';

			var v_context = {
				tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
				start_time: new Date().getTime(),
				sel_value: v_sel_value
			}

			if (v_context.tab_tag.ht!=null) {
				v_context.tab_tag.ht.destroy();
				v_context.tab_tag.ht = null;
			}
			v_context.tab_tag.div_result.innerHTML = '';
			v_context.tab_tag.query_info.innerHTML = '';

			sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Query, v_message_data, false, v_context);
		}

	}

}

function checkQueryStatus(p_tab) {

	if (p_tab.tag.state == 2) {
		querySQLReturnRender(p_tab.tag.data,p_tab.tag.context);
	}

}

function querySQLReturn(p_data,p_context) {

	p_context.duration = new Date().getTime() - p_context.start_time;

	if (p_context.tab_tag.tab_id == p_context.tab_tag.tabControl.selectedTab.id && p_context.tab_tag.connTab.id == p_context.tab_tag.connTab.tag.connTabControl.selectedTab.id) {
		querySQLReturnRender(p_data,p_context);
	}
	else {
		p_context.tab_tag.state = 2;
		p_context.tab_tag.context = p_context;
		p_context.tab_tag.data = p_data;

		p_context.tab_tag.tab_loading_span.style.display = 'none';
		p_context.tab_tag.tab_check_span.style.display = '';

	}

}

function querySQLReturnRender(p_message,p_context) {
	p_context.tab_tag.state = 0;
	p_context.tab_tag.context = null;
	p_context.tab_tag.data = null;

	var v_data = p_message.v_data;

	var v_div_result = p_context.tab_tag.div_result;
	var v_query_info = p_context.tab_tag.query_info;

	if (p_context.tab_tag.ht!=null) {
		p_context.tab_tag.ht.destroy();
		p_context.tab_tag.ht = null;
	}

	v_div_result.innerHTML = '';

	var request_time = p_context.duration;

	if (p_message.v_error) {

		v_div_result.innerHTML = '<div class="query_info">' + p_message.v_data + '</div>';
		v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";

	}
	else {

		if (p_context.sel_value==-2) {
			v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";
			v_div_result.innerHTML = '';
		}
		else if (p_context.sel_value==-3) {

			v_query_info.innerHTML = "Response time: " + request_time/1000 + " seconds";

			v_div_result.innerHTML = '<div class="query_info">' + v_data + '</div>';

		}
		else {

			window.scrollTo(0,0);

			v_query_info.innerHTML = v_data.v_query_info + "<br/>Response time: " + request_time/1000 + " seconds";

			var columnProperties = [];

			for (var i = 0; i < v_data.v_col_names.length; i++) {
			    var col = new Object();

			    col.readOnly = true;

			    col.title =  v_data.v_col_names[i];

				columnProperties.push(col);

			}

			var container = v_div_result;
			p_context.tab_tag.ht = new Handsontable(container,
			{
				data: v_data.v_data,
				columns : columnProperties,
				colHeaders : true,
				rowHeaders : true,
				copyRowsLimit : 1000000000,
				copyColsLimit : 1000000000,
				manualColumnResize: true,
				contextMenu: {
					callback: function (key, options) {
						if (key === 'view_data') {
						  	editCellData(this,options.start.row,options.start.col,this.getDataAtCell(options.start.row,options.start.col),false);
						}
					},
					items: {
						"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"../images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
					}
			    },
		        cells: function (row, col, prop) {
				    var cellProperties = {};
				    if (row % 2 == 0)
						cellProperties.renderer = blueRenderer;
					else
						cellProperties.renderer = whiteRenderer;
				    return cellProperties;
				}
			});

		}

	}

	p_context.tab_tag.tab_loading_span.style.display = 'none';
	p_context.tab_tag.tab_check_span.style.display = 'none';
	p_context.tab_tag.tab_close_span.style.display = '';

}