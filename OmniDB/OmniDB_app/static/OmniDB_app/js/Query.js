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
	sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CancelThread, v_tab_tag.tab_id, false);

	cancelSQLTab();
}

function cancelSQLTab(p_tab_tag) {

	var v_tab_tag;
	if (p_tab_tag)
		v_tab_tag = p_tab_tag;
	else
		v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setReadOnly(false);

	v_tab_tag.state = v_queryState.Idle;
	v_tab_tag.tab_loading_span.style.display = 'none';
	v_tab_tag.tab_check_span.style.display = 'none';
	v_tab_tag.tab_close_span.style.display = '';
	v_tab_tag.bt_cancel.style.display = 'none';
	v_tab_tag.query_info.innerHTML = 'Canceled.';

	removeContext(v_queryWebSocket,v_tab_tag.context.v_context_code);

	SetAcked(v_tab_tag.context);

}

function querySQL(p_mode,
									p_all_data = false,
									p_query = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue(),
									p_callback = null) {

	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if (v_state!=v_queryState.Idle) {
		showAlert('Tab with activity in progress.');
	}
	else {

		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
		var v_sql_value = p_query;
		var v_sel_value = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_filtered_data.value;
		var v_db_index  = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
		var v_tab_loading_span = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_loading_span;
		var v_tab_close_span = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_close_span;

		if (v_sql_value.trim()=='') {
			showAlert('Please provide a string.');
		}
		else {

			//Change to run mode if database index changed
			if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDatabaseIndex==null || v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDatabaseIndex!=v_connTabControl.selectedTab.tag.selectedDatabaseIndex) {
				p_mode = 0;
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currDatabaseIndex = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
			}

			var v_message_data = {
				v_sql_cmd : v_sql_value,
				v_cmd_type: v_sel_value,
				v_db_index: v_db_index,
				v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
				v_mode: p_mode,
				v_all_data: p_all_data
			}

			v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setReadOnly(true);

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
			v_tab_tag.bt_fetch_more.style.display = 'none';
			v_tab_tag.bt_fetch_all.style.display = 'none';
			v_tab_tag.div_notices.innerHTML = '';

			var v_context = {
				tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
				start_time: new Date().getTime(),
				start_datetime: dformat,
				sel_value: v_sel_value,
				database_index: v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
				mode: p_mode,
				callback: p_callback,
				acked: false
			}
			v_context.tab_tag.context = v_context;

			if (p_mode==0 && p_callback==null) {
				if (v_context.tab_tag.ht!=null) {
					v_context.tab_tag.ht.destroy();
					v_context.tab_tag.ht = null;
				}

				v_context.tab_tag.div_result.innerHTML = '';
			}
			v_context.tab_tag.query_info.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Running...</b>';

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

function querySQLReturnRender(p_message,p_context) {
	p_context.tab_tag.state = v_queryState.Idle;
	p_context.tab_tag.context = null;
	p_context.tab_tag.data = null;

	p_context.tab_tag.editor.setReadOnly(false);

	var v_div_result = p_context.tab_tag.div_result;
	var v_query_info = p_context.tab_tag.query_info;

	if (p_context.callback!=null) {
		v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
		p_context.callback(p_message);
	}
	else {
		p_context.tab_tag.selectDataTabFunc();
		p_context.tab_tag.div_count_notices.style.display = 'none';

		if (p_message.v_error) {

			v_div_result.innerHTML = '<div class="error_text">' + p_message.v_data.message + '</div>';
			v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
			if (p_message.v_data.position!=null) {
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(p_message.v_data.position.row,p_message.v_data.position.col)
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.textInput.focus()
			}

		}
		else {

			//Script
			if (p_context.sel_value==0) {

				v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;

				v_div_result.innerHTML = '<div class="query_info">' + p_message.v_data.v_data + '</div>';

			}
			//Query
			else {

				var v_data = p_message.v_data;

				if (v_data.v_notices_length>0) {
					p_context.tab_tag.div_count_notices.innerHTML = v_data.v_notices_length;
					p_context.tab_tag.div_count_notices.style.display = 'inline-block';
					p_context.tab_tag.div_notices.innerHTML = v_data.v_notices;
				}

				//Show fetch buttons if data has 50 rows
				if (v_data.v_data.length>=50 && p_context.mode!=2) {
					p_context.tab_tag.bt_fetch_more.style.display = '';
					p_context.tab_tag.bt_fetch_all.style.display = '';
				}
				else {
					p_context.tab_tag.bt_fetch_more.style.display = 'none';
					p_context.tab_tag.bt_fetch_all.style.display = 'none';
				}

				if (p_context.mode==0) {

					v_div_result.innerHTML = '';

					window.scrollTo(0,0);

					if (v_data.v_data.length==0 && v_data.v_col_names.length==0) {
						v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
						v_div_result.innerHTML = '<div class="query_info">Done.</div>';
					}
					else {

						v_query_info.innerHTML = "Number of records: " + v_data.v_data.length + "<br/><b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;

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
							fillHandle:false,
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
				//Adding fetched data
				else {
					v_new_data = p_context.tab_tag.ht.getSourceData();
					v_query_info.innerHTML = "Number of records: " + (v_new_data.length+v_data.v_data.length) + "<br/><b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
					for (var i = 0; i < v_data.v_data.length; i ++) {
	            v_new_data.push(v_data.v_data[i]);
	        }
					p_context.tab_tag.ht.loadData(v_new_data);
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.childNodes[0].childNodes[0].scrollTop = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.childNodes[0].childNodes[0].scrollHeight;
				}

			}

		}
	}

	p_context.tab_tag.tab_loading_span.style.display = 'none';
	p_context.tab_tag.tab_check_span.style.display = 'none';
	p_context.tab_tag.tab_close_span.style.display = '';
	p_context.tab_tag.bt_cancel.style.display = 'none';

}
