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

var v_unit_list_grid = null;

function closeMonitorUnit(p_div) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  for (var i=0; i<v_tab_tag.units.length; i++) {

    var v_unit = v_tab_tag.units[i];
    if (v_unit.div == p_div) {

      //Clear timeout
      clearTimeout(v_unit.timeout_object);

      if (v_unit.type == 'graph' && v_unit.object != null) {
        v_unit.object.destroy();
      }

      v_unit.div.parentElement.removeChild(v_unit.div);
      v_tab_tag.units.splice(i,1);

      //Removing saved unit
      execAjax('/remove_saved_monitor_unit/',
    				JSON.stringify({"p_saved_id": v_unit.saved_id}),
    				function(p_return) {
            },
            null,
            'box',
            false);

      break;
    }
  }
}

function updateUnitSavedInterval(p_div) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  for (var i=0; i<v_tab_tag.units.length; i++) {
    var v_unit = v_tab_tag.units[i];
    if (v_unit.div == p_div) {
      //Removing saved unit
      execAjax('/update_saved_monitor_unit_interval/',
    				JSON.stringify({"p_saved_id": v_unit.saved_id, "p_interval": v_unit.input_interval.value}),
    				function(p_return) {
            },
            null,
            'box',
            false);

      break;
    }
  }
}

function pauseMonitorUnit(p_div) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  for (var i=0; i<v_tab_tag.units.length; i++) {
    var v_unit = v_tab_tag.units[i];
    if (v_unit.div == p_div) {
      //Clear timeout
      clearTimeout(v_unit.timeout_object);
      v_unit.active = false;
      v_unit.button_play.style.display = 'inline-block';
      v_unit.button_pause.style.display = 'none';
      break;
    }
  }
}

function playMonitorUnit(p_div) {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  for (var i=0; i<v_tab_tag.units.length; i++) {
    var v_unit = v_tab_tag.units[i];
    if (v_unit.div == p_div) {
      //Clear timeout
      clearTimeout(v_unit.timeout_object);
      v_unit.active = true;
      v_unit.button_play.style.display = 'none';
      v_unit.button_pause.style.display = 'inline-block';
      refreshMonitorDashboard(true,v_tab_tag,v_unit.div);
      break;
    }
  }
}

function buildMonitorUnit(p_unit, p_first) {
  var v_dashboard_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.dashboard_div;
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  var v_return_unit = p_unit;

  var v_unit = null;

  var div = document.createElement('div');
  div.className = 'col-md-6 my-2';
  var div_card = document.createElement('div');
  div_card.className = 'card';
  var div_card_body = document.createElement('div');
  div_card_body.className = 'card-body';
  var div_loading = document.createElement('div');
  div_loading.classList.add('div_loading');
  div_loading.innerHTML =
  '<div class="div_loading_cover"></div>' +
  '<div class="div_loading_content">' +
  '  <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">' +
  '    <span class="sr-only ">Loading...</span>' +
  '  </div>' +
  '</div>';

  var div_header = document.createElement('div');
  div_header.className = 'form-inline'
  var title = document.createElement('span');
  title.className = ' mr-1';
  title.innerHTML = v_return_unit.v_title;
  var button_refresh = document.createElement('button');
  button_refresh.onclick = (function(div) {
    return function() {
      refreshMonitorDashboard(true,v_tab_tag,div);
    }
  })(div);
  button_refresh.innerHTML = "<i class='fas fa-sync-alt fa-light'></i>";
  button_refresh.className = 'btn omnidb__theme__btn--secondary btn-sm mr-1';
  button_refresh.title = 'Refresh';
  var button_pause = document.createElement('button');
  button_pause.onclick = (function(div) {
    return function() {
      pauseMonitorUnit(div);
    }
  })(div);
  button_pause.innerHTML = "<i class='fas fa-pause-circle fa-light'></i>";
  button_pause.className = 'btn omnidb__theme__btn--secondary btn-sm mr-1';
  button_pause.title = 'Pause';
  var button_play = document.createElement('button');
  button_play.onclick = (function(div) {
    return function() {
      playMonitorUnit(div);
    }
  })(div);
  button_play.innerHTML = "<i class='fas fa-play-circle fa-light'></i>";
  button_play.className = 'btn omnidb__theme__btn--secondary btn-sm my-2 mr-1';
  button_play.title = 'Play';
  button_play.style.display = 'none';
  var interval = document.createElement('input');
  interval.value = v_return_unit.v_interval;
  interval.className = 'form-control form-control-sm mr-2';
  interval.style.width = '60px';
  interval.onkeypress= function() {
    return event.charCode >= 48 && event.charCode <= 57;
  }
  interval.onchange= function() {
    var v_value = interval.value;
    if (v_value == '' || v_value == '0') {
      interval.value = 30;
    }
    updateUnitSavedInterval(div);
  }
  var interval_text = document.createElement('span');
  interval_text.classList.add('unit_header_element');
  interval_text.innerHTML = 'seconds';
  var button_close = document.createElement('button');
  button_close.className = 'close';
  button_close.onclick = (function(div) {
    return function() {
      closeMonitorUnit(div);
    }
  })(div);
  button_close.innerHTML = '<span aria-hidden="true">&times;</span>';
  var details = document.createElement('span');
  details.classList.add('unit_header_element');
  details.innerHTML = '';
  var div_error = document.createElement('div');
  div_error.classList.add('error_text');
  var div_content = document.createElement('div');
  var div_label = document.createElement('div');
  div_label.className = 'dashboard_unit_legend_box';

  var div_content_group = document.createElement('div');
  div_content_group.className = 'dashboard_unit_content_group';

  div_header.appendChild(title);
  div_header.appendChild(button_refresh);
  div_header.appendChild(button_pause);
  div_header.appendChild(button_play);
  div_header.appendChild(interval);
  div_header.appendChild(interval_text);
  div_header.appendChild(details);
  div_card_body.appendChild(button_close);
  div_card_body.appendChild(div_loading);
  div_card_body.appendChild(div_header);
  div_card_body.appendChild(div_error);

  div_card.appendChild(div_card_body);
  div.appendChild(div_card);

  div_content_group.appendChild(div_content);
  div_content_group.appendChild(div_label);
  div_card_body.appendChild(div_content_group);


  if (p_first)
    $(v_dashboard_div).prepend(div);
  else
    v_dashboard_div.appendChild(div);

  //Increment unit sequence
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_sequence += 1;

  v_unit = {
    'type': '',
    'object': null,
    'object_data': null,
    'saved_id': v_return_unit.v_saved_id,
    'id': v_return_unit.v_id,
    'plugin_name': v_return_unit.v_plugin_name,
    'div': div,
    'div_loading': div_loading,
    'div_details': details,
    'div_error': div_error,
    'div_content': div_content,
    'div_label': div_label,
    'button_pause': button_pause,
    'button_play': button_play,
    'input_interval': interval,
    'error': false,
    'timeout_object': null,
    'unit_sequence': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_sequence,
    'active': true
  }
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units.push(v_unit);

  return div;

}

function startMonitorDashboard() {

  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                              "p_tab_id": v_connTabControl.selectedTab.id});
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

	execAjax('/get_monitor_units/',
				input,
				function(p_return) {

          for (var i=0; i<p_return.v_data.length; i++) {
            buildMonitorUnit(p_return.v_data[i]);
          }
          refreshMonitorDashboard(true,v_tab_tag);
        },
        null,
        'box');

}

function includeMonitorUnit(p_id,p_plugin_name) {
  var v_grid = v_unit_list_grid;
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  var v_row_data = v_grid.getDataAtRow(v_grid.getSelected()[0][0]);
  var v_plugin_name = '';
  if (p_plugin_name!=null)
    v_plugin_name = p_plugin_name;

  var div = buildMonitorUnit({'v_saved_id': -1, 'v_id': p_id, 'v_title': v_row_data[1], 'v_interval': v_row_data[3], 'v_plugin_name': v_plugin_name},true);
  refreshMonitorDashboard(true,v_tab_tag,div);
}

function deleteMonitorUnit(p_unit_id) {

  showConfirm('Are you sure you want to delete this monitor unit?',
      function() {

        var input = JSON.stringify({"p_unit_id": p_unit_id});

        execAjax('/delete_monitor_unit/',
              input,
              function(p_return) {
                refreshMonitorUnitsList();
              },
              null,
              'box');

      });

}

function closeMonitorUnitList() {
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid_div.innerHTML = '';
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_div.style.display = 'none';
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid.destroy();
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid = null;
}

function editMonitorUnit(p_unit_id) {

  $('#modal_monitoring_units').modal('hide');

  v_connTabControl.tag.createNewMonitorUnitTab();

  var input1 = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                               "p_tab_id": v_connTabControl.selectedTab.id,
                               "p_mode": 1});

  execAjax('/get_monitor_unit_list/',
				input1,
				function(p_return) {

          var v_select_template = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.select_template;
          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.template_list = [];

          p_return.v_data.data.forEach(function(p_unit, p_index) {
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.template_list.push({'plugin_name':p_unit[0], 'id': p_return.v_data.id_list[p_index]})
            var v_option = document.createElement('option');
            v_option.value = p_index;
            v_option.innerHTML = '(' + p_unit[2] + ') ' + p_unit[1];
            v_select_template.appendChild(v_option);
          });

        },
        null,
        'box');

  if (p_unit_id!=null) {

    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

    var input2 = JSON.stringify({"p_unit_id": p_unit_id});

    execAjax('/get_monitor_unit_details/',
  				input2,
  				function(p_return) {

            v_tab_tag.input_unit_name.value = p_return.v_data.title;
            v_tab_tag.input_interval.value = p_return.v_data.interval;
            v_tab_tag.select_type.value = p_return.v_data.type;
            v_tab_tag.editor.setValue(p_return.v_data.script_chart);
            v_tab_tag.editor.clearSelection();
            v_tab_tag.editor.gotoLine(0, 0, true);
            v_tab_tag.editor_data.setValue(p_return.v_data.script_data);
            v_tab_tag.editor_data.clearSelection();
            v_tab_tag.editor_data.gotoLine(0, 0, true);
            v_tab_tag.unit_id = p_unit_id;

          },
          null,
          'box');

  }
}

function saveMonitorScript() {
  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  if (v_tab_tag.input_unit_name.value.trim()=='') {
    showAlert('Please provide name for this monitor.');
  }
  else {
    var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                                "p_tab_id": v_connTabControl.selectedTab.id,
                                "p_unit_id": v_tab_tag.unit_id,
                                "p_unit_name": v_tab_tag.input_unit_name.value,
                                "p_unit_type": v_tab_tag.select_type.value,
                                "p_unit_interval": v_tab_tag.input_interval.value,
                                "p_unit_script_data": v_tab_tag.editor_data.getValue(),
                                "p_unit_script_chart": v_tab_tag.editor.getValue()});

    execAjax('/save_monitor_unit/',
  				input,
  				function(p_return) {

            v_tab_tag.unit_id = p_return.v_data;

            showAlert('Monitor unit saved.')

          },
          function(p_return) {
  					if (p_return.v_data.password_timeout) {
  						showPasswordPrompt(
  							v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
  							function() {
  								saveMonitorScript();
  							},
  							null,
  							p_return.v_data.message
  						);
  					}
            else {
              showError(p_return.v_data)
            }
  				},
          'box');

  }


}

function selectUnitTemplate(p_value) {
  if (p_value!=-1) {
    var v_element_item = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.template_list[p_value];
    var input = JSON.stringify({"p_unit_id": v_element_item.id, "p_unit_plugin_name": v_element_item.plugin_name});

    execAjax('/get_monitor_unit_template/',
  				input,
  				function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.innerHTML = '';
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result_label.innerHTML = '';
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.select_type.value = p_return.v_data.type;
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.input_interval.value = p_return.v_data.interval;

            var v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor;
            v_editor.setValue(p_return.v_data.script_chart);
            v_editor.clearSelection();
            v_editor.gotoLine(0, 0, true);

            var v_editor_data = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor_data;
            v_editor_data.setValue(p_return.v_data.script_data);
            v_editor_data.clearSelection();
            v_editor_data.gotoLine(0, 0, true);

          },
          null,
          'box');
  }
}

$('#modal_monitoring_unit_test').on('shown.bs.modal', function (e) {

  var v_script_chart = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
  var v_script_data = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor_data.getValue();
  var v_type = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.select_type.value;

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                              "p_tab_id": v_connTabControl.selectedTab.id,
                              "p_script_chart": v_script_chart,
                              "p_script_data": v_script_data,
                              "p_type": v_type});

	execAjax('/test_monitor_script/',
				input,
				function(p_return) {

          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_type = v_tab_tag.select_type.value;
          var v_div_result = v_tab_tag.div_result;

          if (v_tab_tag.object!=null) {
            v_tab_tag.object.destroy();
            v_tab_tag.object = null;
          }

          try {
            if (p_return.v_data.v_error) {
              v_div_result.innerHTML = '<div class=error_text>' + p_return.v_data.v_message + '</div>';
            }
            else if (v_type=='timeseries' || v_type=='chart') {
              var canvas = document.createElement('canvas');
              canvas.style.height = '250px';
              canvas.style.width = v_div_result.offsetWidth;
              v_div_result.appendChild(canvas);

              var v_return_unit = p_return.v_data;

              var ctx = canvas.getContext('2d');
              var v_show_legend = false;
              try {
                v_return_unit.v_object.options.responsive = true;
                v_return_unit.v_object.options.maintainAspectRatio = false;
                if (v_return_unit.v_object.options.legend==null) {
                  v_return_unit.v_object.options.legend = {
                    'display': false
                  }
                  v_show_legend = true;
                }
                else {
                  if (v_return_unit.v_object.options.legend.display==true)
                    v_show_legend = true;
                  v_return_unit.v_object.options.legend.display = false;
                }
              }
              catch (err) {

              }
              v_return_unit.v_object.options.legendCallback = function(chart) {
                var text = [];
                for (var i = 0; i < chart.legend.legendItems.length; i++) {
                    text.push('<span class="dashboard_unit_label_group"><span class="dashboard_unit_label_box" style="background-color:' + chart.legend.legendItems[i].fillStyle + '"></span><span id="legend-' + i + '-item" class="dashboard_unit_label" onclick="updateDataset(event, ' + '\'' + i + '\'' + ')">' + chart.legend.legendItems[i].text + '</span></span>');
                }
                return text.join("");
              }
              v_tab_tag.object = new Chart(ctx, v_return_unit.v_object);
              adjustChartTheme(v_tab_tag.object);
              if (v_show_legend) {
                var v_legend = v_tab_tag.object.generateLegend();
                v_tab_tag.div_result_label.innerHTML += v_legend;
              }


            }
            else if (v_type=='grid') {
              var columnProperties = [];

              for (var j = 0; j < p_return.v_data.v_object.columns.length; j++) {
                var col = new Object();
                col.readOnly = true;
                col.title =  p_return.v_data.v_object.columns[j];
                columnProperties.push(col);
              }
              v_div_result.className = 'dashboard_unit_grid';
              v_tab_tag.object = new Handsontable(v_div_result,
              {
                licenseKey: 'non-commercial-and-evaluation',
                data: p_return.v_data.v_object.data,
                columns : columnProperties,
                colHeaders : true,
                rowHeaders : true,
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
                    return cellProperties;
                }
              });

            }
            else if (v_type=='graph') {
              v_div_result.className = 'unit_graph';
              p_return.v_data.v_object.container = v_div_result;
              v_tab_tag.object = cytoscape(p_return.v_data.v_object);
              adjustGraphTheme(v_tab_tag.object);
            }
          }
          catch(err) {
            v_div_result.innerHTML = '<div class=error_text>' + err + '</div>';
          }

          endLoading();

				},
				function(p_return) {
					if (p_return.v_data.password_timeout) {
						showPasswordPrompt(
							v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
							function() {
								testMonitorScript();
							},
							null,
							p_return.v_data.message
						);
					}
          else {
            showError(p_return.v_data)
          }
				},
				'box');

});

function testMonitorScript() {

  startLoading();

  var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  v_tab_tag.div_result_label.innerHTML = '';
  var v_div_result = v_tab_tag.div_result;
  v_div_result.innerHTML = '';
  v_div_result.className = '';

  $('#modal_monitoring_unit_test').modal();

}

function refreshMonitorUnitsList() {
  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                              "p_tab_id": v_connTabControl.selectedTab.id,
                              "p_mode": 0});

  var v_grid_div = document.getElementById('monitoring_units_grid');

  execAjax('/get_monitor_unit_list/',
				input,
				function(p_return) {

          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_id_list = p_return.v_data.id_list;

          var columnProperties = [];

          var col = new Object();
          col.readOnly = true;
          col.title =  'Actions';

          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Title';
          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Type';
          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Interval(s)';
          columnProperties.push(col);



          if (v_unit_list_grid)
            v_unit_list_grid.destroy();

          v_unit_list_grid = new Handsontable(v_grid_div,
          {
            licenseKey: 'non-commercial-and-evaluation',
            data: p_return.v_data.data,
            columns : columnProperties,
            colHeaders : true,
            stretchH: 'all',
            tableClassName: 'omnidb__ht__first-col-actions',
            //copyRowsLimit : 1000000000,
            //copyColsLimit : 1000000000,
            copyPaste: {pasteMode: '', rowsLimit: 1000000000, columnsLimit: 1000000000},
            manualColumnResize: true,
            fillHandle:false,
            disableVisualSelection: true,
            fixedColumnsLeft: 1,
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
              cellProperties.renderer =whiteHtmlRenderer;
              return cellProperties;
            }
          });

          endLoading();

        },
        null,
        'box');
}

function refreshMonitorUnitsObjects() {
  v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
  for (var i=0; i<v_tab_tag.units.length; i++) {
    if (v_tab_tag.units[i].type=='grid') {
      if (v_tab_tag.units[i].object) {
        v_tab_tag.units[i].object.render();
      }
    }
  }

}

$('#modal_monitoring_units').on('shown.bs.modal', function (e) {

  refreshMonitorUnitsList();

});

function showMonitorUnitList() {

  startLoading();

  var v_grid_div = document.getElementById('monitoring_units_grid');
  v_grid_div.innerHTML = '';
  $('#modal_monitoring_units').modal();

}

function refreshMonitorDashboard(p_loading,p_tab_tag,p_div) {


  var v_units = [];
  var v_tab_tag = null;
  if (p_tab_tag)
    v_tab_tag = p_tab_tag;
  else
    v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;

  if (v_tab_tag.units.length>0) {
    for (var i=0; i<v_tab_tag.units.length; i++) {
      var v_unit_rendered = 0
      if (v_tab_tag.units[i].object!=null)
        v_unit_rendered = 1

      if (!p_div) {
        if (p_loading)
          $(v_tab_tag.units[i].div_loading).fadeIn(100);
        v_units.push({ 'saved_id': v_tab_tag.units[i].saved_id,
                       'id': v_tab_tag.units[i].id,
                       'sequence': v_tab_tag.units[i].unit_sequence,
                       'rendered': v_unit_rendered,
                       'interval': v_tab_tag.units[i].input_interval.value,
                       'plugin_name': v_tab_tag.units[i].plugin_name,
                       'object_data': v_tab_tag.units[i].object_data
                     })
        clearTimeout(v_tab_tag.units[i].timeout_object);
      }
      else if (p_div == v_tab_tag.units[i].div) {
        if (p_loading)
          $(v_tab_tag.units[i].div_loading).fadeIn(100);
        v_units.push({ 'saved_id': v_tab_tag.units[i].saved_id,
                       'id': v_tab_tag.units[i].id,
                       'sequence': v_tab_tag.units[i].unit_sequence,
                       'rendered': v_unit_rendered,
                       'interval': v_tab_tag.units[i].input_interval.value,
                       'plugin_name': v_tab_tag.units[i].plugin_name,
                       'object_data': v_tab_tag.units[i].object_data
                     })
        clearTimeout(v_tab_tag.units[i].timeout_object);
        break;
      }
    }

    var input = JSON.stringify({"p_database_index": v_tab_tag.connTabTag.selectedDatabaseIndex,
                                "p_tab_id": v_tab_tag.connTabTag.tab_id,
                                "p_ids": v_units});

  	execAjax('/refresh_monitor_units/',
  				input,
  				function(p_return) {
            for (var i=0; i<p_return.v_data.length; i++) {

              var v_return_unit = p_return.v_data[i];

              var v_unit = null;
              //find corresponding object
              for (var p=0; p<v_tab_tag.units.length; p++) {
                if (v_return_unit.v_sequence == v_tab_tag.units[p].unit_sequence) {
                  v_tab_tag.units[p].saved_id = v_return_unit.v_saved_id;
                  v_tab_tag.units[p].type = v_return_unit.v_type;
                  if (v_return_unit.v_object) {
                    if (v_return_unit.v_object.data) {
                      v_tab_tag.units[p].object_data = JSON.parse(JSON.stringify(v_return_unit.v_object.data));
                    }
                    else if (v_return_unit.v_object.elements) {
                      v_tab_tag.units[p].object_data = JSON.parse(JSON.stringify(v_return_unit.v_object.elements));
                    }
                    else {
                      v_tab_tag.units[p].object_data = JSON.parse(JSON.stringify(v_return_unit.v_object));
                    }
                  }
                  v_unit = v_tab_tag.units[p];
                  break;
                }
              }

              try {
                // Chart unit
                if (v_return_unit.v_type=='timeseries' || v_return_unit.v_type=='chart') {

                  $(v_unit.div_loading).fadeOut(100);

                  v_return_unit.type='chart';
                  v_unit.div_error.innerHTML = '';

                  if (v_return_unit.v_error) {

                    v_unit.div_error.innerHTML = v_return_unit.v_message;
                    v_unit.error = true;
                    //v_unit.object = null;
                    //v_unit.div_content.innerHTML = '';

                  }
                  // New chart
                  else if (v_unit.object==null) {
                    v_unit.div_content.innerHTML = '';

                    var canvas = document.createElement('canvas');
                    canvas.style.height = '250px';
                    canvas.style.width = v_unit.div_content.offsetWidth;
                    v_unit.div_content.appendChild(canvas);

                    var ctx = canvas.getContext('2d');
                    var v_show_legend = false;
                    try {
                      v_return_unit.v_object.options.responsive = true;
                      v_return_unit.v_object.options.maintainAspectRatio = false;
                      if (v_return_unit.v_object.options.legend==null) {
                        v_return_unit.v_object.options.legend = {
                          'display': false
                        }
                        v_show_legend = true;
                      }
                      else {
                        if (v_return_unit.v_object.options.legend.display==true)
                          v_show_legend = true;
                        v_return_unit.v_object.options.legend.display = false;
                      }
                    }
                    catch (err) {

                    }
                    v_return_unit.v_object.options.legendCallback = function(chart) {
                      var text = [];
                      for (var j=0; j < chart.legend.legendItems.length; j++) {
                          text.push('<span class="dashboard_unit_label_group"><span class="dashboard_unit_label_box" style="background-color:' + chart.legend.legendItems[j].fillStyle + '"></span><span id="legend-' + i + '-item" class="dashboard_unit_label" onclick="updateDataset(event, ' + '\'' + j + '\'' + ')">' + chart.legend.legendItems[j].text + '</span></span>');
                      }
                      return text.join("");
                    }
                    var v_chart = new Chart(ctx, v_return_unit.v_object);
                    adjustChartTheme(v_chart);
                    if (v_show_legend) {
                      var v_legend = v_chart.generateLegend();
                      v_unit.div_label.innerHTML = v_legend;
                    }

                    v_unit.object = v_chart;

                  }
                  // Update existing chart
                  else {
                    //Don't append, simply update labels and datasets
                    if (v_return_unit.v_type=='chart') {

                      //checking labels
                      var v_need_rebuild_legend = false;

                      //foreach dataset in existing chart, check if it still exists, if not, remove it
                      for (var j=v_unit.object.data.datasets.length-1; j>=0; j--) {
                        var dataset = v_unit.object.data.datasets[j];

                        var v_found = false;
                        for (var k=0; k<v_return_unit.v_object.datasets.length; k++) {
                          var return_dataset = v_return_unit.v_object.datasets[k];
                          if (return_dataset.label == dataset.label) {
                            v_found = true;
                            break;
                          }
                        }
                        //dataset doesn't exist, remove it
                        if (!v_found) {
                          v_need_rebuild_legend = true;
                          v_unit.object.data.datasets.splice(j,1);
                        }
                      }

                      //foreach label in existing chart, check if it still exists, if not, legend needs to be rebuilt
                      for (var j=v_unit.object.data.labels.length-1; j>=0; j--) {
                        var v_found = false;
                        for (var k=0; k<v_return_unit.v_object.labels.length; k++) {
                          if (JSON.stringify(v_return_unit.v_object.labels[k]) == JSON.stringify(v_unit.object.data.labels[j])) {
                            v_found = true;
                            break;
                          }
                        }
                        if (!v_found) {
                          v_need_rebuild_legend = true;
                        }
                      }

                      //foreach dataset in returning data, find corresponding dataset in existing chart
                      for (var j=0; j<v_return_unit.v_object.datasets.length; j++) {
                        var return_dataset = v_return_unit.v_object.datasets[j];

                        //checking datasets
                        var v_found = false;
                        for (var k=0; k<v_unit.object.data.datasets.length; k++) {
                          var dataset = v_unit.object.data.datasets[k];
                          //Dataset exists, update data and adjust colors
                          if (return_dataset.label == dataset.label) {
                            var new_dataset = dataset;

                            //rebuild color list if it exists
                            if (return_dataset.backgroundColor && return_dataset.backgroundColor.length) {
                              var v_color_list = [];
                              for (var l=0; l<v_return_unit.v_object.labels.length; l++) {
                                var v_found_label = false;
                                for (var m=0; m<v_unit.object.data.labels.length; m++) {
                                  if (JSON.stringify(v_return_unit.v_object.labels[l]) == JSON.stringify(v_unit.object.data.labels[m])) {
                                    v_color_list.push(dataset.backgroundColor[m]);
                                    v_found_label = true;
                                    break;
                                  }
                                }

                                if (!v_found_label) {
                                  v_need_rebuild_legend = true;
                                  v_color_list.push(return_dataset.backgroundColor[l]);
                                }
                              }
                              new_dataset.backgroundColor=v_color_list;
                            }
                            new_dataset.data=return_dataset.data;

                            dataset = new_dataset;

                            v_found = true;
                            break;
                          }
                        };
                        //dataset doesn't exist, create it
                        if (!v_found) {
                          v_need_rebuild_legend = true;
                          v_unit.object.data.datasets.push(return_dataset);
                        }
                      };

                      v_unit.object.data.labels = v_return_unit.v_object.labels;

                      //update title
                      if (v_return_unit.v_object.title && v_unit.object.options && v_unit.object.options.title) {
                        v_unit.object.options.title.text = v_return_unit.v_object.title;
                      }


                      try {
                        v_unit.object.update();
                        if (v_need_rebuild_legend) {
                          //rebuild labels
                          var v_legend = v_unit.object.generateLegend();
                          v_unit.div_label.innerHTML = v_legend;
                        }
                      }
                      catch (err) {
                      }
                    }
                    // Append data
                    else {
                      //adding new label in X axis
                      v_unit.object.data.labels.push(v_return_unit.v_object.labels[0]);
                      var v_shift = false;
                      if (v_unit.object.data.labels.length > 100) {
                        v_unit.object.data.labels.shift();
                        v_shift = true;
                      }

                      //foreach dataset in existing chart, find corresponding dataset in returning data
                      for (var j=v_unit.object.data.datasets.length-1; j>=0; j--) {
                        var dataset = v_unit.object.data.datasets[j];
                        dataset.data.push(null);
                        if (v_shift)
                          dataset.data.shift();
                      };

                      //foreach dataset in returning data, find corresponding dataset in existing chart
                      for (var j=0; j<v_return_unit.v_object.datasets.length; j++) {
                        var return_dataset = v_return_unit.v_object.datasets[j];

                        var v_found = false;
                        for (var k=0; k<v_unit.object.data.datasets.length; k++) {
                          var dataset = v_unit.object.data.datasets[k];
                          //Dataset exists, update data
                          if (return_dataset.label == dataset.label) {
                            var new_dataset = dataset;
                            new_dataset.data[new_dataset.data.length-1]=return_dataset.data[0];
                            dataset = new_dataset;

                            v_found = true;
                            break;
                          }
                        };
                        //dataset doesn't exist, create it
                        if (!v_found) {
                          v_need_rebuild_legend = true;
                          //populate dataset with empty data prior to newest value
                          for (var k=0; k<v_unit.object.data.labels.length-1; k++) {
                            return_dataset.data.unshift(null);
                          }
                          v_unit.object.data.datasets.push(return_dataset);
                        }
                      };

                      //update title
                      if (v_return_unit.v_object.title && v_unit.object.options && v_unit.object.options.title) {
                        v_unit.object.options.title.text = v_return_unit.v_object.title;
                      }

                      try {
                        v_unit.object.update();
                        if (v_need_rebuild_legend) {
                          //rebuild labels
                          var v_legend = v_unit.object.generateLegend();
                          v_unit.div_label.innerHTML = v_legend;
                        }
                      }
                      catch (err) {
                      }
                    }
                  }
                }
                // Grid unit
                else if (v_return_unit.v_type=='grid') {

                  v_unit.div_error.innerHTML = '';
                  v_unit.div_details.innerHTML = '';

                  $(v_unit.div_loading).fadeOut(100);

                  v_return_unit.type='grid';

                  if (v_return_unit.v_error) {

                    v_unit.div_error.innerHTML = v_return_unit.v_message;
                    v_unit.error = true;
                    //v_unit.object = null;
                    //v_unit.div_content.innerHTML = '';

                  }
                  // New grid
                  else if (v_unit.object==null) {
                    v_unit.div_content.classList.add('unit_grid');
                    v_unit.div_content.innerHTML = '';

                    var columnProperties = [];

        						for (var j = 0; j < v_return_unit.v_object.columns.length; j++) {
      						    var col = new Object();
      						    col.readOnly = true;
      						    col.title =  v_return_unit.v_object.columns[j];
        							columnProperties.push(col);
        						}

                    v_unit.div_details.innerHTML = v_return_unit.v_object.data.length + ' rows';

        						var v_grid = new Handsontable(v_unit.div_content,
        						{
                                    licenseKey: 'non-commercial-and-evaluation',
        							data: v_return_unit.v_object.data,
        							columns : columnProperties,
        							colHeaders : true,
        							rowHeaders : true,
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
        							    return cellProperties;
        							}
        						});

                    v_unit.object = v_grid;
                  }
                  // Existing grid
                  else {

                    v_unit.div_details.innerHTML = v_return_unit.v_object.data.length + ' rows';

                    v_unit.object.loadData(v_return_unit.v_object.data);

                  }
                }



                // Graph unit
                else if (v_return_unit.v_type=='graph') {

                  v_unit.div_error.innerHTML = '';
                  v_unit.div_details.innerHTML = '';

                  $(v_unit.div_loading).fadeOut(100);

                  v_return_unit.type='graph';

                  if (v_return_unit.v_error) {

                    v_unit.div_error.innerHTML = v_return_unit.v_message;
                    v_unit.error = true;
                    //v_unit.object = null;
                    //v_unit.div_content.innerHTML = '';

                  }
                  // New graph
                  else if (v_unit.object==null) {
                    v_unit.div_content.classList.add('unit_graph');
                    v_unit.div_content.innerHTML = '';

                    v_return_unit.v_object.container = v_unit.div_content;
                    v_unit.object = cytoscape(v_return_unit.v_object);
                    adjustGraphTheme(v_unit.object);
                  }
                  // Existing graph
                  else {

                    var v_existing_nodes = v_unit.object.nodes()
                    var v_existing_edges = v_unit.object.edges()

                    var v_new_objects = []

                    //Updating existing nodes and adding new ones
                    for (var j=0; j<v_return_unit.v_object.nodes.length; j++) {
                      var v_found_node = false;
                      var node = v_return_unit.v_object.nodes[j];
                      for (var k=0; k<v_existing_nodes.length; k++) {
                        //New node already exists, update data
                        if (v_existing_nodes[k].data('id') == node.data['id']) {
                          v_found_node = true;
                          for (var property in node.data) {
                              if (node.data.hasOwnProperty(property)) {
                                  v_existing_nodes[k].data(property,node.data[property])
                              }
                          }
                          break;
                        }
                      }
                      if (!v_found_node) {
                        node['group'] = 'nodes';
                        v_new_objects.push(node);
                      }
                    }

                    //Updating existing edges and adding new ones
                    for (var j=0; j<v_return_unit.v_object.edges.length; j++) {
                      var v_found_edge = false;
                      var edge = v_return_unit.v_object.edges[j];
                      for (var k=0; k<v_existing_edges.length; k++) {
                        //New edge already exists, update data
                        if (v_existing_edges[k].data('id') == edge.data['id']) {
                          v_found_edge = true;
                          for (var property in edge.data) {
                              if (edge.data.hasOwnProperty(property)) {
                                  v_existing_edges[k].data(property,edge.data[property])
                              }
                          }
                          break;
                        }
                      }
                      if (!v_found_edge) {
                        edge['group'] = 'edges';
                        v_new_objects.push(edge);
                      }
                    }
                    //Removing edges that doesn't exist anymore
                    for (var k=0; k<v_existing_edges.length; k++) {
                      var v_found_edge = false;
                      for (var j=0; j<v_return_unit.v_object.edges.length; j++) {
                        var edge = v_return_unit.v_object.edges[j];
                        if (v_existing_edges[k].data('id') == edge.data['id']) {
                          v_found_edge = true;
                          break;
                        }
                      }
                      //Not found, remove it
                      if (!v_found_edge) {
                        v_existing_edges[k].remove();
                      }
                    }
                    //Removing nodes that doesn't exist anymore
                    for (var k=0; k<v_existing_nodes.length; k++) {
                      var v_found_node = false;
                      for (var j=0; j<v_return_unit.v_object.nodes.length; j++) {
                        var node = v_return_unit.v_object.nodes[j];
                        if (v_existing_nodes[k].data('id') == node.data['id']) {
                          v_found_node = true;
                          break;
                        }
                      }
                      //Not found, remove it
                      if (!v_found_node) {
                        v_existing_nodes[k].remove();
                      }
                    }

                    //Adding new objects and rendering graph again
                    if (v_new_objects.length > 0) {
                      v_unit.object.add(v_new_objects);
                      v_unit.object.layout();
                    }


                  }
                }
              }
              catch(err) {
                v_unit.div_error.innerHTML = err;
                v_unit.error = true;
                v_unit.object = null;
                v_unit.div_content.innerHTML = '';
              }

              //Adding timeout to get data again if tab is still active
              if (v_tab_tag.tab_active && v_unit.active) {
                v_unit.timeout_object = setTimeout((function(p_div) {
                  return function() {
                    refreshMonitorDashboard(false,v_tab_tag,p_div);
                  }
                })(v_unit.div),v_unit.input_interval.value*1000);
              }
            }
  				},
  				function(p_return) {
  					if (p_return.v_data.password_timeout) {
  						showPasswordPrompt(
  							v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
  							function() {
  								refreshMonitorDashboard(true,v_tab_tag);
  							},
  							null,
  							p_return.v_data.message
  						);
  					}
            else {
              showError(p_return.v_data)
            }
  				},
          null,
  				'box',
          false);
  }
}

function cancelMonitorUnits(p_tab_tag) {
  var v_tab_tag = p_tab_tag;
  for (var i=0; i<v_tab_tag.units.length; i++) {
    var v_unit = v_tab_tag.units[i];
    clearTimeout(v_unit.timeout_object);
    if (v_unit.type == 'graph' && v_unit.object != null) {
      v_unit.object.destroy();
    }
  }
}

/// <summary>
/// Removes tab.
/// </summary>
/// <param name="p_tab">Tab object.</param>
function closeMonitorDashboardTab(p_tab) {

  p_tab.removeTab();
  p_tab.tag.tab_active = false;
  cancelMonitorUnits(p_tab.tag);

}
