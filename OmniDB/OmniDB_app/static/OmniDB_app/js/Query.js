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

	if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor) {
		v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setReadOnly(false);
	}

	v_tab_tag.state = v_queryState.Idle;
	v_tab_tag.tab_loading_span.style.display = 'none';
	v_tab_tag.tab_check_span.style.display = 'none';
	v_tab_tag.tab_stub_span.style.display = '';
	v_tab_tag.bt_cancel.style.display = 'none';
	v_tab_tag.query_info.innerHTML = 'Canceled.';
	setTabStatus(v_tab_tag,0);

	removeContext(v_queryWebSocket,v_tab_tag.context.v_context_code);

	SetAcked(v_tab_tag.context);

}

function getQueryEditorValue() {

	var v_selected_text = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getSelectedText();

	if (v_selected_text!='')
		return v_selected_text;
	else
		return v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
}

function querySQL(p_mode,
									p_all_data = false,
									p_query = getQueryEditorValue(),
									p_callback = null,
									p_log_query = true,
									p_save_query = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue(),
									p_cmd_type = null,
									p_clear_data = false,
									p_tab_title = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_title_span.innerHTML) {

	var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;

	if (v_state!=v_queryState.Idle) {
		showAlert('Tab with activity in progress.');
	}
	else {

		var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
		v_tab_tag.tempData = [];
		var v_sql_value = p_query;
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
				v_sql_save : p_save_query,
				v_cmd_type: p_cmd_type,
				v_db_index: v_db_index,
				v_conn_tab_id: v_connTabControl.selectedTab.id,
				v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
				v_tab_db_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_db_id,
				v_mode: p_mode,
				v_all_data: p_all_data,
				v_log_query: p_log_query,
				v_tab_title: p_tab_title,
				v_autocommit: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.check_autocommit.checked
			}

			if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor) {
				v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setReadOnly(true);
			}

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
			v_tab_tag.bt_cancel.style.display = 'inline-block';
			v_tab_tag.bt_fetch_more.style.display = 'none';
			v_tab_tag.bt_fetch_all.style.display = 'none';
			v_tab_tag.bt_commit.style.display = 'none';
			v_tab_tag.bt_rollback.style.display = 'none';
			v_tab_tag.div_notices.innerHTML = '';
			setTabStatus(v_tab_tag,2);

			var v_has_selected_text = false;
			if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getSelectedText()!='')
				v_has_selected_text = true;

			var v_context = {
				tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
				start_time: new Date().getTime(),
				start_datetime: dformat,
				cmd_type: p_cmd_type,
				database_index: v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
				mode: p_mode,
				has_selected_text: v_has_selected_text,
				callback: p_callback,
				acked: false,
				all_data: p_all_data,
				query: p_query,
				log_query: p_log_query,
				save_query: p_save_query,
				clear_data: p_clear_data,
				tab_title: p_tab_title
			}
			v_context.tab_tag.context = v_context;

			if ((p_mode==0 && p_callback==null) || p_clear_data) {
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
			},10000);

		}
	}
}

function checkQueryStatus(p_tab) {

	if (p_tab.tag.state == v_queryState.Ready) {
		querySQLReturnRender(p_tab.tag.data,p_tab.tag.context);
	}
}

function querySQLReturn(p_data,p_context) {

	//Update tab_db_id if not null in response
	if (p_data.v_data.v_inserted_id) {
		p_context.tab_tag.tab_db_id = p_data.v_data.v_inserted_id;
	}

	if (!p_data.v_error)
		p_data.v_data.v_data = p_context.tab_tag.tempData;

	p_context.tab_tag.tempData = [];

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

function setTabStatus(p_tab_tag, p_con_status) {
	if (p_con_status==0) {
		p_tab_tag.query_tab_status_text.innerHTML = 'Not connected';
		p_tab_tag.query_tab_status.className = 'fas fa-dot-circle tab-status tab-status-closed';
		p_tab_tag.query_tab_status.title = 'Not connected';
	}
	else if (p_con_status==1) {
		p_tab_tag.query_tab_status_text.innerHTML = 'Idle';
		p_tab_tag.query_tab_status.className = 'fas fa-dot-circle tab-status tab-status-idle';
		p_tab_tag.query_tab_status.title = 'Idle';
	}
	else if (p_con_status==2) {
		p_tab_tag.query_tab_status_text.innerHTML = 'Running'
		p_tab_tag.query_tab_status.className = 'fas fa-dot-circle tab-status tab-status-running';
		p_tab_tag.query_tab_status.title = 'Running';
	}
	else if (p_con_status==3) {
		p_tab_tag.query_tab_status_text.innerHTML = 'Idle in transaction'
		p_tab_tag.query_tab_status.className = 'fas fa-dot-circle tab-status tab-status-idle_in_transaction';
		p_tab_tag.query_tab_status.title = 'Idle in transaction';
	}
	else if (p_con_status==4) {
		p_tab_tag.query_tab_status_text.innerHTML = 'Idle in transaction (aborted)'
		p_tab_tag.query_tab_status.className = 'fas fa-dot-circle tab-status tab-status-idle_in_transaction_aborted';
		p_tab_tag.query_tab_status.title = 'Idle in transaction (aborted)';
	}


}

function querySQLReturnRender(p_message,p_context) {
	p_context.tab_tag.state = v_queryState.Idle;
	p_context.tab_tag.context = null;
	p_context.tab_tag.data = null;

	if(p_context.tab_tag.editor) {
		p_context.tab_tag.editor.setReadOnly(false);
	}

	var v_div_result = p_context.tab_tag.div_result;
	var v_query_info = p_context.tab_tag.query_info;

	var v_data = p_message.v_data;

	//Show commit/rollback buttons if transaction is open
	if (v_data.v_con_status==3 || v_data.v_con_status==4) {
		p_context.tab_tag.bt_commit.style.display = '';
		p_context.tab_tag.bt_rollback.style.display = '';
	}
	else {
		p_context.tab_tag.bt_commit.style.display = 'none';
		p_context.tab_tag.bt_rollback.style.display = 'none';
	}

	setTabStatus(p_context.tab_tag,p_message.v_data.v_con_status);

	if (p_context.callback!=null) {
		if (p_message.v_error) {
			v_div_result.innerHTML = '<div class="error_text">' + p_message.v_data.message + '</div>';
			v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
		}
		else {
			v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
			p_context.callback(p_message);
		}
	}
	else {
		p_context.tab_tag.selectDataTabFunc();

		if(p_context.tab_tag.div_count_notices) {
			p_context.tab_tag.div_count_notices.style.display = 'none';
		}

		if (v_data.v_notices_length>0) {
			if(p_context.tab_tag.div_count_notices) {
				p_context.tab_tag.div_count_notices.innerHTML = v_data.v_notices_length;
				p_context.tab_tag.div_count_notices.style.display = 'inline-block';
				p_context.tab_tag.div_notices.innerHTML = v_data.v_notices;
			}
		}

		if (p_message.v_error) {
			v_div_result.innerHTML = '<div class="error_text">' + p_message.v_data.message + '</div>';
			v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
			if (p_message.v_data.position!=null) {
				if(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor && !p_context.has_selected_text) {
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(p_message.v_data.position.row,p_message.v_data.position.col)
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.textInput.focus()
				}
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

				//Show fetch buttons if data has 50 rows
				if (v_data.v_data.length>=50 && p_context.mode!=2) {
					if(p_context.tab_tag.bt_fetch_more) {
						p_context.tab_tag.bt_fetch_more.style.display = '';
					}

					if(p_context.tab_tag.bt_fetch_all) {
						p_context.tab_tag.bt_fetch_all.style.display = '';
					}
				}
				else {
					if(p_context.tab_tag.bt_fetch_more) {
						p_context.tab_tag.bt_fetch_more.style.display = 'none';
					}

					if(p_context.tab_tag.bt_fetch_all) {
						p_context.tab_tag.bt_fetch_all.style.display = 'none';
					}
				}

				if (p_context.mode==0) {

					v_div_result.innerHTML = '';

					window.scrollTo(0,0);
					if (v_data.v_data.length==0 && v_data.v_col_names.length==0) {
						v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
						if (typeof(p_message.v_data.v_status)=='string')
							v_div_result.innerHTML = '<div class="query_info">' + p_message.v_data.v_status + '</div>';
						else
							v_div_result.innerHTML = '<div class="query_info">Done</div>';
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
							licenseKey: 'non-commercial-and-evaluation',
							data: v_data.v_data,
							columns : columnProperties,
							colHeaders : true,
							rowHeaders : true,
							autoRowSize: false,
							//copyRowsLimit : 1000000000,
							//copyColsLimit : 1000000000,
                            copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
							manualColumnResize: true,
							fillHandle:false,
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
									cellProperties.renderer = blueRenderer;
								else
									cellProperties.renderer = whiteRenderer;
							    return cellProperties;
							}
						});

					}

				}
				//Adding fetched data
				else if (p_context.mode==1 || p_context.mode==2) {
					v_new_data = p_context.tab_tag.ht.getSourceData();
					v_query_info.innerHTML = "Number of records: " + (v_new_data.length+v_data.v_data.length) + "<br/><b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
					for (var i = 0; i < v_data.v_data.length; i ++) {
	            v_new_data.push(v_data.v_data[i]);
	        }
					p_context.tab_tag.ht.loadData(v_new_data);
					v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.childNodes[0].childNodes[0].scrollTop = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.childNodes[0].childNodes[0].scrollHeight;
				}
				//COMMIT or ROLLBACK
				else {
					if (p_context.tab_tag.ht!=null)
						v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration + '<br/>Status: ' + p_message.v_data.v_status;
					else {
						v_query_info.innerHTML = "<b>Start time</b>: " + p_context.start_datetime + " <b>Duration</b>: " + p_message.v_data.v_duration;
						v_div_result.innerHTML = '<div class="query_info">' + p_message.v_data.v_status + '</div>'
					}
				}

			}

		}
	}

	p_context.tab_tag.tab_loading_span.style.display = 'none';
	p_context.tab_tag.tab_check_span.style.display = 'none';
	p_context.tab_tag.tab_stub_span.style.display = '';
	p_context.tab_tag.bt_cancel.style.display = 'none';

}
