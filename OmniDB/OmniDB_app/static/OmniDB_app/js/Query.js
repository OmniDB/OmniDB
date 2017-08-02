/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Query state
/// </summary>
var v_queryState = {
	Idle: 0,
	Executing: 1,
	Ready: 2
}

//Adding padLeft function to Number
Number.prototype.padLeft = function(base,chr){
    var  len = (String(base || 10).length - String(this).length)+1;
    return len > 0? new Array(len).join(chr || '0')+this : this;
}

function cancelSQL(p_tab_tag) {

	var v_tab_tag;
	if (p_tab_tag)
		v_tab_tag = p_tab_tag;
	else
		v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CancelThread, v_tab_tag.context.v_context_code, false);

	cancelSQLTab();
}

function cancelSQLTab(p_tab_tag) {

	var v_tab_tag;
	if (p_tab_tag)
		v_tab_tag = p_tab_tag;
	else
		v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	v_tab_tag.state = v_queryState.Idle;
	v_tab_tag.tab_loading_span.style.display = 'none';
	v_tab_tag.tab_check_span.style.display = 'none';
	v_tab_tag.tab_close_span.style.display = '';
	v_tab_tag.bt_cancel.style.display = 'none';
	v_tab_tag.div_result.innerHTML = 'Canceled.';

	removeContext(v_queryWebSocket,v_tab_tag.context.v_context_code);

	SetAcked(v_tab_tag.context);

}

function querySQL() {

	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if (v_state!=v_queryState.Idle) {
		showAlert('Tab with activity in progress.');
	}
	else {

		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
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

		if (v_sql_value.trim()=='') {
			showAlert('Please provide a string.');
		}
		else {

			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state = v_queryState.Executing;

			var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_sql": v_sql_value, "p_select_value" : v_sel_value});

			var start_time = new Date().getTime();

			var d = new Date,
	    dformat = [(d.getMonth()+1).padLeft(),
	               d.getDate().padLeft(),
	               d.getFullYear()].join('/') +' ' +
	              [d.getHours().padLeft(),
	               d.getMinutes().padLeft(),
	               d.getSeconds().padLeft()].join(':');

			v_tab_tag.tab_loading_span.style.display = '';
			v_tab_tag.tab_close_span.style.display = 'none';
			v_tab_tag.bt_cancel.style.display = '';

			var v_context = {
				tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
				start_time: new Date().getTime(),
				start_datetime: dformat,
				sel_value: v_sel_value,
				database_index: v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
				acked: false
			}
			v_context.tab_tag.context = v_context;

			if (v_context.tab_tag.ht!=null) {
				v_context.tab_tag.ht.destroy();
				v_context.tab_tag.ht = null;
			}

			v_context.tab_tag.div_result.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Running...</b>';
			v_context.tab_tag.query_info.innerHTML = '';

			sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Query, v_message_data, false, v_context);

			setTimeout(function() {
				if (!v_context.acked) {
					cancelSQLTab(v_context.tab_tag);
					showAlert('No response from query server.');
				}
			},20000);

		}
	}
}

function checkQueryStatus(p_tab) {

	if (p_tab.tag.state == v_queryState.Ready) {
		querySQLReturnRender(p_tab.tag.data,p_tab.tag.context);
	}
}

function querySQLReturn(p_data,p_context) {

	//If query wasn't canceled already
	if (p_context.tab_tag.state!=v_queryState.Idle) {
		p_context.duration = new Date().getTime() - p_context.start_time;

		if (p_context.tab_tag.tab_id == p_context.tab_tag.tabControl.selectedTab.id && p_context.tab_tag.connTab.id == p_context.tab_tag.connTab.tag.connTabControl.selectedTab.id) {
			querySQLReturnRender(p_data,p_context);
		}
		else {
			p_context.tab_tag.state = v_queryState.Ready;
			p_context.tab_tag.context = p_context;
			p_context.tab_tag.data = p_data;

			p_context.tab_tag.tab_loading_span.style.display = 'none';
			p_context.tab_tag.tab_check_span.style.display = '';

		}
	}
}

function get_duration(p_seconds) {

	if (p_seconds < 1) {
		return p_seconds + ' seconds'
	}
	else {
		var date = new Date(null);
		date.setSeconds(p_seconds);
		return date.toISOString().substr(11, 8);
	}
}

function querySQLReturnRender(p_message,p_context) {
	p_context.tab_tag.state = v_queryState.Idle;
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

	var v_duration = get_duration(request_time/1000);

	if (p_message.v_error) {

		v_div_result.innerHTML = '<div class="error_text">' + p_message.v_data.message + '</div>';
		v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + v_duration;
		if (p_message.v_data.position!=null) {
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(p_message.v_data.position.row,p_message.v_data.position.col)
			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.textInput.focus()
		}

	}
	else {

		if (p_context.sel_value==-2) {
			v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + v_duration;
			v_div_result.innerHTML = '';
		}
		else if (p_context.sel_value==-3) {

			v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + v_duration;

			v_div_result.innerHTML = '<div class="query_info">' + v_data + '</div>';

		}
		else {

			window.scrollTo(0,0);

			v_query_info.innerHTML = v_data.v_query_info + "<br/><b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + v_duration;

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
						"view_data": {name: '<div style=\"position: absolute;\"><img class="img_ht" src=\"/static/OmniDB_app/images/rename.png\"></div><div style=\"padding-left: 30px;\">View Content</div>'}
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
	p_context.tab_tag.bt_cancel.style.display = 'none';

}
