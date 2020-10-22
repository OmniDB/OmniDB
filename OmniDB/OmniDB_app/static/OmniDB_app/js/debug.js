/*
This file is part of OmniDB.
OmniDB is open-source software, distributed "AS IS" under the MIT license in the hope that it will be useful.

The MIT License (MIT)

Portions Copyright (c) 2015-2020, The OmniDB Team
Portions Copyright (c) 2017-2020, 2ndQuadrant Limited

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
*/

/// <summary>
/// Debug state
/// </summary>
var v_debugState = {
	Initial: 0,
	Starting: 1,
	Ready: 2,
  Step: 3,
  Finished: 4,
	Cancel: 5
}

function setupDebug(p_node, p_type) {
	getDebugFunctionDefinitionPostgresql(p_node);

  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
	v_tab_tag.database_index = v_connTabControl.selectedTab.tag.selectedDatabaseIndex;
	v_tab_tag.function = p_node.parent.parent.text + '.' + p_node.text;
	v_tab_tag.type = p_type;

	v_tab_tag.bt_reload.onclick = function() {
		if (v_tab_tag.state!=v_debugState.Initial && v_tab_tag.state!=v_debugState.Finished && v_tab_tag.state!=v_debugState.Cancel)
			showAlert('Not ready reload function attributes.');
		else {
			setupDebug(p_node,v_tab_tag.type);
		}
	};
	v_tab_tag.selectParameterTabFunc();

  //Instantiate grids

	//Retrieve parameters
	execAjax('/get_function_fields_postgresql/',
			JSON.stringify({
					"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
					"p_tab_id": v_connTabControl.selectedTab.id,
					"p_function": p_node.tag.id,
					"p_schema": p_node.parent.parent.text
			}),
			function(p_return) {

				var v_data = [];

				for (i = 0; i < p_return.v_data.length; i++) {

						if (p_return.v_data[i].v_type != 'O')
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

				if (v_tab_tag.htParameter) {
					v_tab_tag.htParameter.destroy();
					v_tab_tag.div_parameter.innerHTML = '';
				}

			  v_tab_tag.htParameter = new Handsontable(v_tab_tag.div_parameter,
			  {
				licenseKey: 'non-commercial-and-evaluation',
			    data: v_data,
			    columns : columnProperties,
			    colHeaders : true,
			    rowHeaders : true,
			    //copyRowsLimit : 1000000000,
			    //copyColsLimit : 1000000000,
                copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
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

				v_tab_tag.debug_info.innerHTML = 'Adjust parameters and start';

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

	if (v_tab_tag.htVariable) {
		v_tab_tag.htVariable.destroy();
		v_tab_tag.div_variable.innerHTML = '';
	}

  v_tab_tag.htVariable = new Handsontable(v_tab_tag.div_variable,
  {
	licenseKey: 'non-commercial-and-evaluation',
    data: [],
    columns : columnProperties,
    colHeaders : true,
    rowHeaders : true,
    //copyRowsLimit : 1000000000,
    //copyColsLimit : 1000000000,
    copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
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

	//Remove markers
	for (var i=0; i<v_tab_tag.markerList.length; i++) {
		v_tab_tag.editor.session.removeMarker(v_tab_tag.markerList[i]);
	}
	v_tab_tag.markerList = [];

}

function startDebug() {

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	if (v_tab_tag.state!=v_debugState.Initial && v_tab_tag.state!=v_debugState.Finished && v_tab_tag.state!=v_debugState.Cancel)
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
			v_conn_tab_id: v_connTabControl.selectedTab.id,
	    v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
	    v_function: v_function,
			v_type: v_tab_tag.type
	  }

	  var v_context = {
	    tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
	    acked: false
	  }
	  v_context.tab_tag.context = v_context;

		v_tab_tag.bt_start.style.display = 'none';
		v_tab_tag.bt_reload.style.display = 'none';
		v_tab_tag.bt_step_over.style.display = 'inline-block';
		v_tab_tag.bt_step_out.style.display = 'inline-block';
		v_tab_tag.bt_cancel.style.display = 'inline-block';
		v_tab_tag.div_notices.innerHTML = '';
		v_tab_tag.div_result.innerHTML = '';
		v_tab_tag.div_count_notices.style.display = 'none';
		v_tab_tag.tab_loading_span.style.visibility = '';
		v_tab_tag.tab_check_span.style.display = 'none';

		if (v_tab_tag.htResult!=null) {
			v_tab_tag.htResult.destroy();
			v_tab_tag.htResult = null;
			v_tab_tag.div_result.innerHTML = '';
		}

		if (v_tab_tag.chart!=null) {
			v_tab_tag.chart.destroy();
			v_tab_tag.chart = null;
			//v_tab_tag.div_statistics.innerHTML = '';
		}

		//Remove markers
		for (var i=0; i<v_tab_tag.markerList.length; i++) {
			v_tab_tag.editor.session.removeMarker(v_tab_tag.markerList[i]);
		}
		v_tab_tag.markerList = [];

		createRequest(v_queryRequestCodes.Debug, v_message_data, v_context);

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
	else if (v_state==v_debugState.Cancel) {
    showAlert('Debugger is being canceled.');
  }
  //Ready to step
  else {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

		var d = new Date,
		dformat = [(d.getMonth()+1).padLeft(),
							 d.getDate().padLeft(),
							 d.getFullYear()].join('/') +' ' +
							[d.getHours().padLeft(),
							 d.getMinutes().padLeft(),
							 d.getSeconds().padLeft()].join(':');

		v_tab_tag.debug_info.innerHTML = '<b>Start time</b>: ' + dformat + '<br><b>Stepping...</b>';
		v_tab_tag.tab_loading_span.style.visibility = '';
		v_tab_tag.tab_check_span.style.display = 'none';
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
			v_next_breakpoint: v_next_breakpoint,
			v_type: v_tab_tag.type
    }

    var v_context = {
      tab_tag: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag,
			acked: false
    }
    v_context.tab_tag.context = v_context;

		createRequest(v_queryRequestCodes.Debug, v_message_data, v_context);

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

function cancelDebug() {

	var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	if (v_tab_tag.state == v_debugState.Cancel) {
		showAlert('Debugger is being canceled.')
	}
	else {
		v_tab_tag.tab_check_span.style.display = 'none';
		v_tab_tag.tab_loading_span.style.visibility = '';

		v_tab_tag.state = v_debugState.Cancel;

		v_tab_tag.debug_info.innerHTML = '<b>Canceling...</b>';

		var v_message_data = {
			v_db_index: v_tab_tag.database_index,
			v_state: v_debugState.Cancel,
			v_tab_id: v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.tab_id,
			v_type: v_tab_tag.type
		}

		var v_context = {
	    tab_tag: v_tab_tag,
	    acked: false
	  }

		createRequest(v_queryRequestCodes.Debug, v_message_data);

	}
}

function checkDebugStatus(p_tab) {
	if (p_tab.tag.hasDataToRender) {
		p_tab.tag.hasDataToRender = false;
		debugResponseRender(p_tab.tag.data,p_tab.tag.context);
	}
}

function debugResponse(p_message, p_context) {

	p_context.tab_tag.tab_loading_span.style.visibility = 'hidden';

	if (p_context.tab_tag.tab_id == p_context.tab_tag.tabControl.selectedTab.id && p_context.tab_tag.connTab.id == p_context.tab_tag.connTab.tag.connTabControl.selectedTab.id) {
		debugResponseRender(p_message,p_context);
	}
	else {
		p_context.tab_tag.tab_check_span.style.display = '';
		p_context.tab_tag.hasDataToRender = true;
		p_context.tab_tag.context = p_context;
		p_context.tab_tag.data = p_message;
	}

}

function cancelDebugInterface(p_context) {
	p_context.tab_tag.state = v_debugState.Cancel;
	p_context.tab_tag.tab_check_span.style.display = 'none';
	p_context.tab_tag.tab_loading_span.style.visibility = 'hidden';

	p_context.tab_tag.debug_info.innerHTML = '<b>Canceled.</b>';

	//Update buttons
	p_context.tab_tag.bt_start.style.display = 'inline-block';
	p_context.tab_tag.bt_reload.style.display = 'inline-block';
	p_context.tab_tag.bt_step_over.style.display = 'none';
	p_context.tab_tag.bt_step_out.style.display = 'none';
	p_context.tab_tag.bt_cancel.style.display = 'none';

	//Remove marker
	if (p_context.tab_tag.markerId) {
		p_context.tab_tag.editor.session.removeMarker(p_context.tab_tag.markerId);
		p_context.tab_tag.markerId = null;
	}
}

function debugResponseRender(p_message, p_context) {

	p_context.tab_tag.tab_check_span.style.display = 'none';

	if (p_context.tab_tag.state != v_debugState.Finished) {

  p_context.tab_tag.state = p_message.v_data.v_state;

	//Cancelled
	if (p_context.tab_tag.state==v_debugState.Cancel) {
		cancelDebugInterface(p_context);
	}
	else {

		//Ready
		if (p_context.tab_tag.state==v_debugState.Ready)
			p_context.tab_tag.debug_info.innerHTML = '<b>Ready</b>';

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

				p_context.tab_tag.editor.session.removeMarker(p_context.tab_tag.markerId);

				if (p_message.v_data.v_error) {
					p_context.tab_tag.debug_info.innerHTML = '<b>Finished</b>';
					p_context.tab_tag.selectResultTabFunc();
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
						licenseKey: 'non-commercial-and-evaluation',
						data: p_message.v_data.v_result_rows,
						columns : columnProperties,
						colHeaders : true,
						rowHeaders : true,
						//copyRowsLimit : 1000000000,
						//copyColsLimit : 1000000000,
                        copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
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
					p_context.tab_tag.selectStatisticsTabFunc();
					//building data object
					var v_chart_data = [];
					var v_total_duration = 0.0;
					var v_chart_labels = [];
					var v_max_value = 0;
					for (var i=0; i<p_message.v_data.v_result_statistics.length; i++) {
						var v_curr_val = parseFloat(p_message.v_data.v_result_statistics[i][1]);
						if (v_curr_val > v_max_value)
							v_max_value = v_curr_val;
						v_chart_labels.push(parseFloat(p_message.v_data.v_result_statistics[i][0]));
						v_chart_data.push({meta: 'Duration', value: v_curr_val });
						v_total_duration += v_curr_val;
					}

					p_context.tab_tag.debug_info.innerHTML = '<b>Finished</b> - <b>Total duration</b>: ' + (v_total_duration).toFixed(3) + ' s';

					var v_width = 30*p_message.v_data.v_result_statistics.length;
					v_width = Math.max(v_width,400)
					p_context.tab_tag.div_statistics_container.style.width = v_width + 'px';

					var v_chart_data_list = [];
					for (var i=0; i<v_chart_data.length;i++) {
						v_chart_data_list.push(v_chart_data[i].value);
					}
					var ctx = p_context.tab_tag.div_statistics_canvas.getContext('2d');
					p_context.tab_tag.chart = new Chart(ctx,result = {
					    "type": "line",
					    "data": {
					    "labels": v_chart_labels,
					    "datasets": [{
					            //"label": 'Title 1',
					            "fill": false,
					            "backgroundColor": "rgb(75, 192, 192)",
					            "borderColor": "rgb(75, 192, 192)",
					            "lineTension": 0,
					            "pointRadius": 2,
					            "borderWidth": 1,
					            "data": v_chart_data_list
					        }]
					},
					    "options": {
					        "responsive": true,
									"maintainAspectRatio": false,
					        "title":{
					            "display":false,
					            "text":"Statistics"
					        },
									"legend": {
					        	"display": false
					        },
					        "tooltips": {
					            "mode": "index",
					            "intersect": false
					        },
					        "hover": {
					            "mode": "nearest",
					            "intersect": true
					        },
					        "scales": {
					            "xAxes": [{
					                "display": true,
					                "scaleLabel": {
					                    "display": true,
					                    "labelString": "Line Number"
					                }
					            }],
					            "yAxes": [{
					                "display": true,
					                "scaleLabel": {
					                    "display": true,
					                    "labelString": "Duration(s)"
					                },
													"ticks": {
					                    "beginAtZero": true,
					                    "max": Math.ceil(v_max_value + 0.5)
					                }
					            }]
					        }
					    }
					}
					);
					adjustChartTheme(p_context.tab_tag.chart);

					//Adding heat colors to function body
					v_max_value = v_max_value + 0.5;
					var v_increment = v_max_value/5;
					var v_color_range = [0,v_increment, v_increment*2,v_increment*3,v_increment*4,v_max_value];
					for (var i=0; i<p_message.v_data.v_result_statistics_summary.length; i++) {
						var v_curr_val = parseFloat(p_message.v_data.v_result_statistics_summary[i][1]);
						var v_scheme_index = 1;
						if (v_curr_val >= v_color_range[0] && v_curr_val < v_color_range[1])
							v_scheme_index = 1;
						else if (v_curr_val >= v_color_range[1] && v_curr_val < v_color_range[2])
							v_scheme_index = 2;
						else if (v_curr_val >= v_color_range[2] && v_curr_val < v_color_range[3])
							v_scheme_index = 3;
						else if (v_curr_val >= v_color_range[3] && v_curr_val < v_color_range[4])
							v_scheme_index = 4;
						else
							v_scheme_index = 5;
						p_context.tab_tag.markerList.push(p_context.tab_tag.editor.session.addMarker(new Range(p_message.v_data.v_result_statistics_summary[i][0]-1,0,p_message.v_data.v_result_statistics_summary[i][0]-1,200),"editorMarkerScale" + v_scheme_index,"fullLine"));
					}

				}

				//notices
				if (p_message.v_data.v_result_notices_length>0) {
					p_context.tab_tag.div_count_notices.innerHTML = p_message.v_data.v_result_notices_length;
					p_context.tab_tag.div_count_notices.style.display = 'inline-block';
					p_context.tab_tag.div_notices.innerHTML = p_message.v_data.v_result_notices;
				}

				//Update buttons
				p_context.tab_tag.bt_start.style.display = 'inline-block';
				p_context.tab_tag.bt_reload.style.display = 'inline-block';
				p_context.tab_tag.bt_step_over.style.display = 'none';
				p_context.tab_tag.bt_step_out.style.display = 'none';
				p_context.tab_tag.bt_cancel.style.display = 'none';
			}
		}
	}
}
