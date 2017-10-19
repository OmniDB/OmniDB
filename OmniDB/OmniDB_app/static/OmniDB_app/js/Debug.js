/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

/// <summary>
/// Debug state
/// </summary>
var v_debugState = {
	Initial: 0,
	Starting: 1,
	Ready: 2,
  Step: 3,
  Finished: 4
}

function setupDebug(p_node) {

  //console.log(p_node);
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_tab_tag.database_index = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
	v_tab_tag.function = p_node.parent.parent.text + '.' + p_node.text;

  //Instantiate grids

	//Retrieve parameters
	execAjax('/get_function_fields_postgresql/',
			JSON.stringify({
					"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
					"p_function": p_node.tag.id,
					"p_schema": p_node.parent.parent.text
			}),
			function(p_return) {

				var v_data = [];

				for (i = 0; i < p_return.v_data.length; i++) {

						if (p_return.v_data[i].v_type == 'I')
							v_data.push([p_return.v_data[i].v_name,''])
				}

				var columnProperties = [];
			  var col = new Object();
			  col.readOnly = true;
			  col.title =  'Parameter';
			  columnProperties.push(col);
				var col = new Object();
			  col.readOnly = false;
			  col.title =  'Value';
			  columnProperties.push(col);
			  v_tab_tag.div_result.innerHTML = '';

			  v_tab_tag.htParameter = new Handsontable(v_tab_tag.div_parameter,
			  {
			    data: v_data,
			    columns : columnProperties,
			    colHeaders : true,
			    rowHeaders : true,
			    copyRowsLimit : 1000000000,
			    copyColsLimit : 1000000000,
			    manualColumnResize: true,
			    fillHandle:false,
			        cells: function (row, col, prop) {
			        var cellProperties = {};
			        if (row % 2 == 0)
			        cellProperties.renderer = blueRenderer;
			      else
			        cellProperties.renderer = whiteRenderer;
			        return cellProperties;
			    }
			  });

			},
			function(p_return) {
			},
			'box',
			false);

  var columnProperties = [];
  var col = new Object();
  col.readOnly = true;
  col.title =  'Variable';
  columnProperties.push(col);
	var col = new Object();
  col.readOnly = true;
  col.title =  'Attribute';
  columnProperties.push(col);
  var col = new Object();
  col.readOnly = true;
  col.title =  'Type';
  columnProperties.push(col);
  var col = new Object();
  col.readOnly = true;
  col.title =  'Value';
  columnProperties.push(col);
  v_tab_tag.div_result.innerHTML = '';

  v_tab_tag.htVariable = new Handsontable(v_tab_tag.div_variable,
  {
    data: [],
    columns : columnProperties,
    colHeaders : true,
    rowHeaders : true,
    copyRowsLimit : 1000000000,
    copyColsLimit : 1000000000,
    manualColumnResize: true,
    fillHandle:false,
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

function startDebug() {

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_tab_tag.div_result.innerHTML = '';

	if (v_tab_tag.state!=v_debugState.Initial && v_tab_tag.state!=v_debugState.Finished)
		showAlert('Not ready to start new debugging procedure.');
	else {
		v_tab_tag.state = v_debugState.Starting;

	//Creating select statement
	var v_num_params = v_tab_tag.htParameter.countRows();
	var v_function = v_tab_tag.function + '(';
	var v_first = true;
	for (var i=0; i<v_num_params; i++) {
		if (!v_first)
			v_function += ',';
		v_first = false;

		v_function += v_tab_tag.htParameter.getDataAtRow(i)[1];
	}
	v_function += ')';

		var v_message_data = {
	    v_db_index: v_tab_tag.database_index,
	    v_state: v_tab_tag.state,
	    v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
	    v_function: v_function
	  }

	  var v_context = {
	    tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
	    acked: false
	  }
	  v_context.tab_tag.context = v_context;

	  sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Debug, v_message_data, false, v_context);
	}

}

function stepDebug() {
  var v_state = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.state;
	if (v_state==v_debugState.Initial) {
    showAlert('Debugger wasn\'t started.');
  }
  else if (v_state==v_debugState.Starting) {
    showAlert('Debugger is starting.');
  }
  else if (v_state==v_debugState.Step) {
    showAlert('Step in progress.');
  }
  else if (v_state==v_debugState.Finished) {
    showAlert('Function already finished.');
  }
  //Ready to step
  else {

    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    v_tab_tag.state = v_debugState.Step;

    var v_message_data = {
      v_db_index: v_tab_tag.database_index,
      v_state: v_tab_tag.state,
      v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id
    }

    var v_context = {
      tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
    }
    v_context.tab_tag.context = v_context;

    sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Debug, v_message_data, false, v_context);


  }
}

function debugResponse(p_message, p_context) {
  //console.log(p_message.v_data)
  p_context.tab_tag.state = p_message.v_data.v_state;

  var Range = ace.require('ace/range').Range;
  if (p_message.v_data.v_lineno) {
		p_context.tab_tag.editor.scrollToLine(p_message.v_data.v_lineno+2, true, true, function () {});
    if (p_context.tab_tag.markerId)
      p_context.tab_tag.editor.session.removeMarker(p_context.tab_tag.markerId);
    p_context.tab_tag.markerId = p_context.tab_tag.editor.session.addMarker(new Range(p_message.v_data.v_lineno+2,0,p_message.v_data.v_lineno+2,200),"editorMarker","fullLine");
  }

  if (p_message.v_data.v_variables) {
		p_context.tab_tag.selectVariableTabFunc();
    p_context.tab_tag.htVariable.loadData(p_message.v_data.v_variables);
  }

  if (p_context.tab_tag.state==v_debugState.Finished) {
		p_context.tab_tag.selectResultTabFunc();
    //showAlert('Function finished.');

		if (p_message.v_data.v_error) {
			p_context.tab_tag.div_result.innerHTML = '<div class="error_text">' + p_message.v_data.v_error_msg + '</div>';
		}
		else {
			var columnProperties = [];
			for (var i = 0; i < p_message.v_data.v_result_columns.length; i++) {
					var col = new Object();
					col.readOnly = true;
					col.title =  p_message.v_data.v_result_columns[i];
				columnProperties.push(col);
			}

			p_context.tab_tag.ht = new Handsontable(p_context.tab_tag.div_result,
			{
				data: p_message.v_data.v_result_rows,
				columns : columnProperties,
				colHeaders : true,
				rowHeaders : true,
				copyRowsLimit : 1000000000,
				copyColsLimit : 1000000000,
				manualColumnResize: true,
				fillHandle:false,
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
}
