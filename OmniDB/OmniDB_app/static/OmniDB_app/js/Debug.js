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


	//Customize editor to enable adding breakpoints
	//Creating breakpoint options
	$('#' + v_tab_tag.editorDivId).children('.ace_gutter').each(function () {
	    var v_gutter = $(this);
			v_gutter.css('cursor', 'pointer');
			v_gutter.click(function() {
				v_tab_tag.editor.session.selection.clearSelection();

				var v_row = v_tab_tag.editor.getSelectionRange().start.row;
				if (v_tab_tag.breakPoint == v_row)
					v_tab_tag.breakPoint = null;
				else
					v_tab_tag.breakPoint = v_row;
				/*
				//Check if there is a breakpoint for the current row, if there is, remove it
				//if not, add it.
				var v_found = false;
				for (var i=0; i<v_tab_tag.breakPoints.length; i++) {
					if (v_tab_tag.breakPoints[i].row == v_row) {
						v_found = true;
						v_tab_tag.breakPoints.splice(i, 1);
						break;
					}
				}
				if (!v_found) {
					v_tab_tag.breakPoints.push(
						{
						  row: v_row,
						  column: 0,
						  text: "Breakpoint",
						  type: "warning"
						}
					)
				}*/

				v_tab_tag.editor.getSession().setAnnotations([{
					row: v_tab_tag.breakPoint,
					column: 0,
					text: "Breakpoint",
					type: "warning"
				}]);
			});
	});

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

	if (v_tab_tag.state!=v_debugState.Initial && v_tab_tag.state!=v_debugState.Finished)
		showAlert('Not ready to start new debugging procedure.');
	else {

		v_tab_tag.debug_info.innerHTML = 'Preparing debugger...';
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

		v_tab_tag.bt_start.style.display = 'none';
		v_tab_tag.bt_step_over.style.display = 'inline-block';
		v_tab_tag.bt_step_out.style.display = 'inline-block';
		v_tab_tag.div_notices.innerHTML = '';
		v_tab_tag.div_result.innerHTML = '';
		v_tab_tag.div_count_notices.style.display = 'none';
		if (v_tab_tag.chart!=null) {
			v_tab_tag.chart.detach();
			v_tab_tag.chart = null;
			v_tab_tag.div_statistics.innerHTML = '';
		}

	  sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Debug, v_message_data, false, v_context);
	}

}

function stepDebug(p_mode) {
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
		v_tab_tag.debug_info.innerHTML = 'Stepping...';
    v_tab_tag.state = v_debugState.Step;

		var v_next_breakpoint = 0;
		//Not next stmt, check breakpoint
		if (p_mode!=0) {
			if (v_tab_tag.breakPoint==null || v_tab_tag.breakPoint<=2)
				//no breakpoint go to the end of the function
				v_next_breakpoint = -1;
			else
				v_next_breakpoint = v_tab_tag.breakPoint+1;
		}

    var v_message_data = {
      v_db_index: v_tab_tag.database_index,
      v_state: v_tab_tag.state,
      v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
			v_next_breakpoint: v_next_breakpoint
    }

    var v_context = {
      tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag
    }
    v_context.tab_tag.context = v_context;

    sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.Debug, v_message_data, false, v_context);


  }
}

function ctPointLabels(options) {
    return function ctPointLabels(chart) {
        var defaultOptions = {
            labelClass: 'ct-label',
            labelOffset: {
                x: 0,
                y: -10
            },
            textAnchor: 'middle'
        };

        options = Chartist.extend({}, defaultOptions, options);

        if (chart instanceof Chartist.Line) {
            chart.on('draw', function (data) {
                if (data.type === 'point') {
                    data.group.elem('text', {
                        x: data.x + options.labelOffset.x,
                        y: data.y + options.labelOffset.y,
                        style: 'text-anchor: ' + options.textAnchor
                    }, options.labelClass).text(data.value.y);  // 07.11.17 added ".y"
                }
            });
        }
    }
}

function debugResponse(p_message, p_context) {
  //console.log(p_message.v_data)
  p_context.tab_tag.state = p_message.v_data.v_state;

	if (p_context.tab_tag.state==v_debugState.Ready)
		p_context.tab_tag.debug_info.innerHTML = 'Ready';

  var Range = ace.require('ace/range').Range;
  if (p_message.v_data.v_lineno) {
		p_context.tab_tag.editor.scrollToLine(p_message.v_data.v_lineno, true, true, function () {});
    if (p_context.tab_tag.markerId)
      p_context.tab_tag.editor.session.removeMarker(p_context.tab_tag.markerId);
    p_context.tab_tag.markerId = p_context.tab_tag.editor.session.addMarker(new Range(p_message.v_data.v_lineno-1,0,p_message.v_data.v_lineno-1,200),"editorMarker","fullLine");
  }

  if (p_message.v_data.v_variables) {
		p_context.tab_tag.selectVariableTabFunc();
    p_context.tab_tag.htVariable.loadData(p_message.v_data.v_variables);
  }

	//Finished
  if (p_context.tab_tag.state==v_debugState.Finished) {

		p_context.tab_tag.debug_info.innerHTML = 'Finished';

		p_context.tab_tag.editor.session.removeMarker(p_context.tab_tag.markerId);
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

			p_context.tab_tag.htResult = new Handsontable(p_context.tab_tag.div_result,
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

			//Chart
			//building data object
			var v_chart_data = [];
			var v_chart_labels = [];
			var v_max_value = 0;
			for (var i=0; i<p_message.v_data.v_result_statistics.length; i++) {
				var v_curr_val = parseFloat(p_message.v_data.v_result_statistics[i][1]);
				if (v_curr_val > v_max_value)
					v_max_value = v_curr_val;
				v_chart_labels.push(parseFloat(p_message.v_data.v_result_statistics[i][0]));
				v_chart_data.push({meta: 'Duration', value: parseFloat(p_message.v_data.v_result_statistics[i][1]) });
			}

			var v_width = 80*p_message.v_data.v_result_statistics.length;

			p_context.tab_tag.chart = new Chartist.Line(p_context.tab_tag.div_statistics, {
		  labels: v_chart_labels,
		  series: [
		    v_chart_data
		  ]
			}, {
			  fullWidth: true,
				lineSmooth: false,
				high: v_max_value + 0.5,
				width: v_width + 'px',
				plugins: [
			    ctPointLabels({
			      textAnchor: 'middle'
			    }),
					Chartist.plugins.ctAxisTitle({
			      axisX: {
			        axisTitle: 'Line Number',
			        axisClass: 'ct-axis-title',
			        offset: {
			          x: 0,
			          y: 30
			        },
			        textAnchor: 'middle'
			      },
			      axisY: {
			        axisTitle: 'Duration(s)',
			        axisClass: 'ct-axis-title',
			        offset: {
			          x: 0,
			          y: 0
			        },
			        textAnchor: 'middle',
			        flipTitle: false
			      }
			    })
			  ],
			  chartPadding: {
			    right: 40,
					left: 40
			  }
			});
		}

		//notices
		if (p_message.v_data.v_result_notices_length>0) {
			p_context.tab_tag.div_count_notices.innerHTML = p_message.v_data.v_result_notices_length;
			p_context.tab_tag.div_count_notices.style.display = 'inline-block';
			p_context.tab_tag.div_notices.innerHTML = p_message.v_data.v_result_notices;
		}

		//Update buttons
		p_context.tab_tag.bt_start.style.display = 'inline-block';
		p_context.tab_tag.bt_step_over.style.display = 'none';
		p_context.tab_tag.bt_step_out.style.display = 'none';
	}
}
