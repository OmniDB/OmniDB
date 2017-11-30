/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function closeMonitorUnit(p_div) {
  for (var i=0; i<v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units.length; i++) {
    var v_unit = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[i];
    if (v_unit.div == p_div) {
      v_unit.div.parentElement.removeChild(v_unit.div);
      v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units.splice(i,1);
      break;
    }
  }
}

function buildMonitorUnit(p_unit, p_first) {
  var v_dashboard_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.dashboard_div;

  var v_return_unit = p_unit;

  var v_unit = null;

  var div = document.createElement('div');
  div.classList.add('dashboard_unit');
  var div_loading = document.createElement('div');
  div_loading.classList.add('div_loading_local');

  var div_header = document.createElement('div');
  var title = document.createElement('h3');
  title.classList.add('unit_header_element');
  title.innerHTML = v_return_unit.v_title;
  var button_refresh = document.createElement('button');
  button_refresh.onclick = (function(div) {
    return function() {
      refreshMonitorDashboard(div);
    }
  })(div);
  button_refresh.innerHTML = '<img src="/static/OmniDB_app/images/refresh.png"/>';
  button_refresh.classList.add('unit_header_element');
  var button_close = document.createElement('button');
  button_close.onclick = (function(div) {
    return function() {
      closeMonitorUnit(div);
    }
  })(div);
  button_close.innerHTML = '<img src="/static/OmniDB_app/images/tab_close.png"/>';
  button_close.classList.add('unit_header_element');
  button_close.classList.add('unit_close_button');
  var details = document.createElement('div');
  details.classList.add('unit_header_element');
  details.innerHTML = '';
  var div_error = document.createElement('div');
  div_error.classList.add('error_text');
  var div_content = document.createElement('div');

  div_header.appendChild(title);
  div_header.appendChild(button_refresh);
  div_header.appendChild(button_close);
  div_header.appendChild(details);
  div.appendChild(div_loading);
  div.appendChild(div_header);
  div.appendChild(div_error);
  div.appendChild(div_content);
  if (p_first)
    $(v_dashboard_div).prepend(div);
  else
    v_dashboard_div.appendChild(div);

  v_unit = {
    'type': '',
    'object': null,
    'id': v_return_unit.v_id,
    'div': div,
    'div_loading': div_loading,
    'div_details': details,
    'div_error': div_error,
    'div_content': div_content,
    'error': false
  }
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units.push(v_unit);

  return div;

}

function startMonitorDashboard() {

  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex});

	execAjax('/get_monitor_units/',
				input,
				function(p_return) {

          for (var i=0; i<p_return.v_data.length; i++) {
            buildMonitorUnit(p_return.v_data[i]);
          }
          refreshMonitorDashboard();
        },
        null,
        'box');

}

function includeMonitorUnit(p_id) {
  var v_grid = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid;
  var v_row_data = v_grid.getDataAtRow(v_grid.getSelected()[0]);

  var div = buildMonitorUnit({'v_id': p_id, 'v_title': v_row_data[1]},true);
  refreshMonitorDashboard(div);
}

function deleteMonitorUnit(p_unit_id) {

  showConfirm('Are you sure you want to delete this monitor unit?',
      function() {

        var input = JSON.stringify({"p_unit_id": p_unit_id});

        execAjax('/delete_monitor_unit/',
              input,
              function(p_return) {
                showMonitorUnitList();
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
  v_connTabControl.tag.createNewMonitorUnitTab();

  var input1 = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex});

  execAjax('/get_monitor_unit_list/',
				input1,
				function(p_return) {

          var v_select_template = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.select_template;

          p_return.v_data.data.forEach(function(p_unit, p_index) {
            var v_option = document.createElement('option');
            v_option.value = p_return.v_data.id_list[p_index];
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
            v_tab_tag.select_type.value = p_return.v_data.type;
            v_tab_tag.editor.setValue(p_return.v_data.script);
            v_tab_tag.editor.clearSelection();
            v_tab_tag.editor.gotoLine(0, 0, true);
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
  else if (v_tab_tag.editor.getValue().trim()=='') {
    showAlert('Please provide script for this monitor.');
  }
  else {
    var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                                "p_unit_id": v_tab_tag.unit_id,
                                "p_unit_name": v_tab_tag.input_unit_name.value,
                                "p_unit_type": v_tab_tag.select_type.value,
                                "p_unit_script": v_tab_tag.editor.getValue()});

    execAjax('/save_monitor_unit/',
  				input,
  				function(p_return) {

            v_tab_tag.unit_id = p_return.v_data;

            showAlert('Monitor unit saved.')

          },
          null,
          'box');

  }


}

function selectUnitTemplate(p_value) {
  if (p_value!=-1) {
    var input = JSON.stringify({"p_unit_id": p_value});

    execAjax('/get_monitor_unit_template/',
  				input,
  				function(p_return) {

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.innerHTML = '';

            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.select_type.value = p_return.v_data.type;

            var v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor;
            v_editor.setValue(p_return.v_data.script);
            v_editor.clearSelection();
            v_editor.gotoLine(0, 0, true);

          },
          null,
          'box');
  }
}

function testMonitorScript(p_create_tab, p_mode, p_table, p_schema) {

  var v_script = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();

	var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_script": v_script});

	execAjax('/test_monitor_script/',
				input,
				function(p_return) {

          var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
          var v_type = v_tab_tag.select_type.value;
          var v_div_result = v_tab_tag.div_result;

          v_div_result.innerHTML = '';

          if (v_tab_tag.object!=null) {
            v_tab_tag.object.destroy();
            v_tab_tag.object = null;
          }

          try {
            if (p_return.v_data.v_error) {
              v_div_result.innerHTML = '<div class=error_text>' + p_return.v_data.v_message + '</div>';
            }
            else if (v_type=='chart_append' || v_type=='chart') {
              var canvas = document.createElement('canvas');
              v_div_result.appendChild(canvas);

              var ctx = canvas.getContext('2d');
              v_tab_tag.object = new Chart(ctx, p_return.v_data.v_object);

            }
            else if (v_type=='grid') {
              var columnProperties = [];

              for (var j = 0; j < p_return.v_data.v_object.columns.length; j++) {
                var col = new Object();
                col.readOnly = true;
                col.title =  p_return.v_data.v_object.columns[j];
                columnProperties.push(col);
              }

              v_tab_tag.object = new Handsontable(v_div_result,
              {
                data: p_return.v_data.v_object.data,
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
          catch(err) {
            v_div_result.innerHTML = '<div class=error_text>' + err + '</div>';
          }

				},
				function(p_return) {
					if (p_return.v_data.password_timeout) {
						showPasswordPrompt(
							v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
							function() {
								startAlterTable(p_create_tab, p_mode, p_table, p_schema);
							},
							null,
							p_return.v_data.message
						);
					}
          else {
            console.log(p_return.v_data)
            showError(p_return.v_data)
          }
				},
				'box');

}

function showMonitorUnitList() {

  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex});

  var v_grid_div = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid_div;
  v_grid_div.innerHTML = '';

  execAjax('/get_monitor_unit_list/',
				input,
				function(p_return) {

          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_id_list = p_return.v_data.id_list;

          var columnProperties = [];

          var col = new Object();
          col.readOnly = true;
          col.title =  'Actions';
          col.width = '60px';
          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Title';
          columnProperties.push(col);

          var col = new Object();
          col.readOnly = true;
          col.title =  'Type';
          columnProperties.push(col);

          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_div.style.display = 'block';

          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid)
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid.destroy();


          v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.unit_list_grid = new Handsontable(v_grid_div,
          {
            data: p_return.v_data.data,
            columns : columnProperties,
            colHeaders : true,
            rowHeaders : true,
            copyRowsLimit : 1000000000,
            copyColsLimit : 1000000000,
            manualColumnResize: true,
            fillHandle:false,
            fixedColumnsLeft: 1,
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
                cellProperties.renderer = blueHtmlRenderer;
              else
                cellProperties.renderer = whiteHtmlRenderer;
                return cellProperties;
            }
          });

        },
        null,
        'box');

}

function refreshMonitorDashboard(p_div) {

  var v_units = [];

  for (var i=0; i<v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units.length; i++) {
    if (!p_div) {
      v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[i].div_loading.style.display = 'block';
      v_units.push({ 'id': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[i].id, 'index': i })
    }
    else if (p_div == v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[i].div) {
      v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[i].div_loading.style.display = 'block';
      v_units.push({ 'id': v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[i].id, 'index': i })
      break;
    }
  }

  var input = JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex, "p_ids": v_units});

	execAjax('/refresh_monitor_units/',
				input,
				function(p_return) {

          for (var i=0; i<p_return.v_data.length; i++) {

            var v_return_unit = p_return.v_data[i];

            var v_unit = null;

            if (v_return_unit.v_index!=-1)
              v_unit = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.units[v_return_unit.v_index];

            try {
              // Chart unit
              if (v_return_unit.v_type=='chart_append' || v_return_unit.v_type=='chart') {

                v_unit.div_loading.style.display = 'none';

                v_return_unit.type='chart';
                v_unit.div_error.innerHTML = '';

                if (v_return_unit.v_error) {

                  v_unit.div_error.innerHTML = v_return_unit.v_message;
                  v_unit.error = true;
                  v_unit.object = null;
                  v_unit.div_content.innerHTML = '';

                }
                // New chart
                else if (v_unit.object==null) {
                  v_unit.div_content.innerHTML = '';

                  var canvas = document.createElement('canvas');
                  v_unit.div_content.appendChild(canvas);

                  var ctx = canvas.getContext('2d');
                  var v_chart = new Chart(ctx, v_return_unit.v_object);

                  v_unit.object = v_chart;

                }
                // Update existing chart
                else {
                  //Don't append, simply replace labels and datasets
                  if (v_return_unit.v_type=='chart') {
                    v_unit.object.data.labels = v_return_unit.v_object.data.labels;
                    v_unit.object.data.datasets = v_return_unit.v_object.data.datasets;
                    v_unit.object.update();
                  }

                  else {
                    //adding new label in X axis
                    v_unit.object.data.labels.push(v_return_unit.v_object.data.labels[0]);
                    var v_shift = false;
                    if (v_unit.object.data.labels.length > 20) {
                      v_unit.object.data.labels.shift();
                      v_shift = true;
                    }

                    //foreach dataset in existing chart, find corresponding dataset in returning data
                    for (var j=v_unit.object.data.datasets.length-1; j>=0; j--) {
                      var dataset = v_unit.object.data.datasets[j];
                      if (v_shift)
                        dataset.data.shift();
                      var v_found = false;
                      for (var k=0; k<v_return_unit.v_object.data.datasets.length; k++) {
                        var return_dataset = v_return_unit.v_object.data.datasets[k];
                        //Dataset exists
                        if (return_dataset.label == dataset.label) {
                          v_found = true;
                          break;
                        }
                      };
                      //dataset doesn't exist, remove it
                      if (!v_found) {
                        v_unit.object.data.datasets.splice(j,1);
                      }
                    };

                    //foreach dataset in returning data, find corresponding dataset in existing chart
                    for (var j=0; j<v_return_unit.v_object.data.datasets.length; j++) {
                      var return_dataset = v_return_unit.v_object.data.datasets[j];

                      var v_found = false;
                      for (var k=0; k<v_unit.object.data.datasets.length; k++) {
                        var dataset = v_unit.object.data.datasets[k];
                        //Dataset exists, update data
                        if (return_dataset.label == dataset.label) {
                          var new_dataset = dataset;
                          new_dataset.data[new_dataset.data.length]=return_dataset.data[0];
                          dataset = new_dataset;

                          v_found = true;
                          break;
                        }
                      };
                      //dataset doesn't exist, create it
                      if (!v_found) {
                        //populate dataset with empty data prior to newest value
                        for (var k=0; k<v_unit.object.data.labels.length-1; k++) {
                          return_dataset.data.unshift('');
                        }
                        v_unit.object.data.datasets.push(return_dataset);
                      }
                    };

                    v_unit.object.update();
                  }
                }
              }
              // Grid unit
              else if (v_return_unit.v_type=='grid') {

                v_unit.div_error.innerHTML = '';
                v_unit.div_details.innerHTML = '';

                v_unit.div_loading.style.display = 'none';

                v_return_unit.type='grid';

                if (v_return_unit.v_error) {

                  v_unit.div_error.innerHTML = v_return_unit.v_message;
                  v_unit.error = true;
                  v_unit.object = null;
                  v_unit.div_content.innerHTML = '';

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
      							data: v_return_unit.v_object.data,
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

                  v_unit.object = v_grid;
                }
                // Existing grid
                else {

                  v_unit.div_details.innerHTML = v_return_unit.v_object.data.length + ' rows';

                  v_unit.object.loadData(v_return_unit.v_object.data);

                }
              }
            }
            catch(err) {
              v_unit.div_error.innerHTML = err;
              v_unit.error = true;
              v_unit.object = null;
              v_unit.div_content.innerHTML = '';
            }

            //Adding timeout to get data again
            /*setTimeout(function() {
              refreshMonitorDashboard(v_unit.div);
            },5000);*/

          }
				},
				function(p_return) {
					if (p_return.v_data.password_timeout) {
						showPasswordPrompt(
							v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
							function() {
								refreshMonitorDashboard();
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
