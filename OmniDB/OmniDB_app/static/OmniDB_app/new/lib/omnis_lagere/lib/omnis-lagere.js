/*
Copyright 2015-2020 The OmniDB Team
This file is part of OmniDB.
OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function createLagere(p_context = {parent: window, self: 'omnisLagere'}, p_options) {

  var v_lagereControl = {
    // Params
    backgroundColor: (p_options.backgroundColor) ? p_options.backgroundColor : '#e2e2e2',
    context: p_context,
    data: [],
    dataMatrix: [],
    defaultClass: (p_options.bem_class_root) ? p_options.bem_class_root : 'omnis-lagere',
    defaultMessage: 'No content',
    divElement: false,
		id: 'omnis_lagere_control_' + Date.now(),
    planCounter: 0,
    planList: [],
    planCountMatrix: [0],
		stateActive: false,
    targetDiv: (p_options.target) ? p_options.target : false,
    totalCols: 0,
    totalRows: 0,
    // Actions
    emptyPlanList : function() {
      this.data = [];
      this.dataMatrix = [];
      this.planCounter = 0;
      this.planList = [];
      this.planCounter = 0;
      this.planList = [];
      this.planCountMatrix = [0];
      this.totalCols = 0;
      this.totalRows = 0;
    },
    updatePlanList : function(p_data) {
      this.emptyPlanList();
      this.data = p_data;
      this.createPlans();

      this.setStateEnabled();

      this.renderPlans();
    },
    goToPlan : function(p_index) {
      this.stepSelected = p_index;
      this.renderStep();
    },
    createPlanCountMatrix: function({
      p_data = {},
      p_index = 0,
      p_index_map = []
    }) {
      var v_control = this;
      v_control.planCounter++;

      var v_index = p_index;
      var v_index_map = [];

      // Update v_index_map with parent p_index_map
      for (let i = 0; i < p_index_map.length; i++)
        v_index_map.push(p_index_map[i]);

      // Add current index to v_index_map
      v_index_map.push(v_index);

      // Updates planCountMatrix
      var v_row = v_index_map.length - 1;

      if (this.planCountMatrix[v_row] === undefined)
        this.planCountMatrix.push(1);
      else
        this.planCountMatrix[v_row] += 1;

      // Create child plans
      if (p_data['Plans'])
        if (p_data['Plans'].length > 0)
          for (let i = 0; i < p_data['Plans'].length; i++) {
            this.createPlanCountMatrix({
              p_data: p_data['Plans'][i],
              p_index: i,
              p_index_map: v_index_map
            });
          }

    },
    createDataMatrixRow: function({
      p_data = {},
      p_index = 0,
      p_index_map = []
    }) {
      var v_index = p_index;
      var v_index_map = [];

      // Update v_index_map with parent p_index_map
      for (let i = 0; i < p_index_map.length; i++)
        v_index_map.push(p_index_map[i]);

      // Add current index to v_index_map
      v_index_map.push(v_index);

      // Position the elements inside the grid
      var v_row_nodes = (p_data['Plans']) ? p_data['Plans'].length : 0;
      var v_row_empty_cols_half = (this.totalCols - v_row_nodes)%2;
      var v_row_empty_cols_left = 0;
      var v_row_empty_cols_right = 0;
      if (v_row_empty_cols_half > 0) {
        v_row_empty_cols_left = Math.floor((this.totalCols - v_row_nodes)/2);
        v_row_empty_cols_right = v_row_empty_cols_left + 1;
      }
      else {
        v_row_empty_cols_left = (this.totalCols - v_row_nodes)/2;
        v_row_empty_cols_right = v_row_empty_cols_left;
      }
      var v_row_empty_cols_right_start = this.totalCols - v_row_empty_cols_right;

      for (let i = 0; i < this.totalRows; i++) {
        var v_row = [];
        for (let j = 0; j < this.totalCols; j++) {
          if (j < v_row_empty_cols_left || j >= v_row_empty_cols_right_start)
            v_row.push(0);
          else
            v_row.push(1);
        }
        this.dataMatrix.push(v_row);
      }

    },
    createDataMatrix: function() {
      this.total_progress_key_name = (this.data[0]['Plan']['Actual Total Time']) ? 'Actual Total Time' : 'Total Cost';
      this.total_progress_cost = 0;
      // Creates the planCountMatrix to evaluate row and col range
      for (let i = 0; i < this.data.length; i++) {
        this.total_progress_cost += this.data[i]['Plan'][this.total_progress_key_name];
        this.createPlanCountMatrix({
          p_data: this.data[i]['Plan'],
          p_index: i,
          p_index_map: []
        });
      }
      // Updates the row and col range
      this.updateRowsColsCount();

      for (let i = 0; i < this.data.length; i++) {
        this.createDataMatrixRow({
          p_data: this.data[i]['Plan'],
          p_index: i,
          p_index_map: []
        });
      }
    },
    createPlan : function({
      p_data = {},
      p_index = 0,
      p_index_map = [],
      p_max_children_count = 1
    }) {
			var v_control = this;

      var v_id = v_control.id + '_plan';
      var v_index = p_index;
      var v_index_map = [];

      // Update v_index_map with parent p_index_map
      for (let i = 0; i < p_index_map.length; i++)
        v_index_map.push(p_index_map[i]);

      // Add current index to v_index_map
      v_index_map.push(v_index);

      // Update ID with index map
      for (let i = 0; i < v_index_map.length; i++)
        v_id += '_' + v_index_map[i];

      var v_plan_list = [];

      var v_data = {};
      Object.keys(p_data).forEach(function (p_data_key) {
        if (p_data_key !== 'Plans')
          v_data[p_data_key] = p_data[p_data_key];
      });


      // Sets max_children_count
      var v_max_children_count = p_max_children_count;
      if (p_data['Plans'])
        if (p_data['Plans'].length > p_max_children_count)
          v_max_children_count = p_data['Plans'].length;


      var v_plan = {
        data: v_data,
				id: v_id,
        index: v_index,
        index_map: v_index_map,
        max_children_count: v_max_children_count,
        planList: []
			};


      // Create child plans
      var v_plan_progress_cost_total = 0;
      v_plan_progress_cost_total += v_plan.data[v_control.total_progress_key_name];

      if (p_data['Plans']) {
        if (p_data['Plans'].length > 0) {
          var v_child_max_children_count = 1;

          for (let i = 0; i < p_data['Plans'].length; i++) {
            var v_new_plan = this.createPlan({
              p_data: p_data['Plans'][i],
              p_index: i,
              p_index_map: v_plan.index_map,
              p_max_children_count: 1
            });
            v_plan.planList.push(v_new_plan);

            v_child_max_children_count += v_new_plan.max_children_count;

            v_plan_progress_cost_total -= v_new_plan.data[v_control.total_progress_key_name];
          }
        }
      }

      // console.log(v_plan_progress_cost_total, v_new_plan_progress_cost_total);

      v_plan.progress_cost_percentage = v_plan_progress_cost_total / v_control.total_progress_cost;
      v_plan.progress_cost_value = v_plan_progress_cost_total;

      return v_plan;
    },
    createPlans : function() {
      this.createDataMatrix();

			for (let i = 0; i < this.data.length; i++) {
        var v_new_plan = this.createPlan({
          p_data: this.data[i]['Plan'],
          p_index: i,
          p_index_map: [],
          p_max_children_count: 1
        });

        this.planList.push(v_new_plan);
      }
    },
    destroy : function() {
      v_lagereControl = this;

      v_lagereControl.divElement.remove();

      delete v_lagereControl.context.parent[v_lagereControl.context.self];
    },
    renderPlan : function(p_plan_item) {
      var v_plan_item = p_plan_item;
      var v_plans_html = '';


      var v_title = '';
      var v_progress_cost_html = '';
      if (v_plan_item.data['Node Type']) {
        var v_child_count = (v_plan_item['planList'] !== undefined) ? v_plan_item['planList'].length : 0;
        v_title +=
        '<div class="' + this.defaultClass + '__title card-title p-2"><h5 class="mb-0">' +
          '<strong>' + v_plan_item.data['Node Type'] + '</strong>' +
          '<span>(' + v_child_count + ')</span>' +
          '<span class="ml-4" style="font-weight:400;">cost: ' + v_plan_item.progress_cost_value + '</span>' +
        '</h5></div>';

        v_progress_cost_html +=
        '<div class="' + this.defaultClass + '__body card-body p-2">' +
          '<div id="' + v_plan_item.id + '_svg_progress"></div>' +
        '</div>';
      }
      // CSS Grid ROWxCOL starts from 1, take this into account for p_index_map
      var v_index = v_plan_item.index;
      var v_index_map = v_plan_item.index_map;
      var v_row_depth = v_index_map.length - 1;
      // Get the grid_row
      var v_grid_row = v_plan_item.index_map.length;
      var v_grid_col = 0;
      // To prevent overlapping of child_nodes, we need to offset move each node to the right ,base on the number of child_nodes inside the previous node

      var v_parent_row = null;
      var v_temp_parent_node = null;
      var v_temp_parent_node_child_list = this.planList;
      var v_col_offset_shift = 0;
      // Find parent_row
      // Get the grid_col. Col initial number is the value of the index + 1 to account for CSS Grid start at 1.
      if (v_row_depth === 0) {
        v_grid_col = v_index + 1;
        v_temp_parent_node = v_plan_item;
      }
      else {
        if (v_row_depth === 1) {
          v_temp_parent_node = this.planList[v_index_map[0]];
          v_temp_parent_node_child_list = this.planList;
        }
        else {
          for (let i = 0; i < v_row_depth; i++) {
            v_temp_parent_node = v_temp_parent_node_child_list[v_index_map[i]];
            v_temp_parent_node_child_list = v_temp_parent_node.planList;
          }
        }

        v_grid_col = v_temp_parent_node.index_as_parent + v_index;

        v_parent_row = v_temp_parent_node_child_list;
        // Find number of children on previous nodes in the same row and add to the col_offset_shit
        for (let i = 0; i < v_index; i++) {

          if (v_parent_row[v_index_map[v_row_depth]]) {
            var v_previous_node = v_parent_row[v_index_map[v_row_depth]].planList[i];
            if (v_previous_node && v_plan_item.planList) {
              if (v_previous_node.planList && v_plan_item.planList.length > 0) {
                v_col_offset_shift += v_previous_node.planList.length;
              }
            }
          }

          v_grid_col += v_col_offset_shift;
        }
      }

      v_plan_item.index_as_parent = v_grid_col;

      var v_test_attr =
      ' data-index="' + v_index +'"' +
      ' data-row-depth="' + v_row_depth + '"' +
      ' data-col-shift="' + v_col_offset_shift + '"' +
      ' data-parent-index="' + v_temp_parent_node.index_as_parent + '"';


      var v_plans_html =
      '<div ' + v_test_attr + ' id="' + v_plan_item.id + '" class="' + this.defaultClass + '__item" style="grid-row: ' + v_grid_row + '; grid-column:' + v_grid_col + '">' +
        '<div class="' + this.defaultClass + '__card card">' +
          v_title +
          v_progress_cost_html +
        '</div>' +
      '</div>';



      var v_children_html = '';
      for (let i = 0; i < v_plan_item.planList.length; i++) {
        v_children_html += this.renderPlan(v_plan_item.planList[i]);
      }
      v_plans_html += v_children_html;

      return v_plans_html;
    },
    renderPlans : function() {
      if (this.divGrid) {
        this.divGrid.innerHTML = '';
      }

      if (this.stateActive) {
        var v_control = this;

        var v_plans_html = '';

        for (let i = 0; i < this.planList.length; i++)
          v_plans_html += this.renderPlan(this.planList[i]);

        this.renderTarget(v_plans_html);
      }
      else {
        this.divElement.style.display = 'none';
      }
    },
    renderProgressBar : function(p_plan_list) {
      var v_progress_bar_html = '';
      var v_node = null;

      for (let i = 0; i < p_plan_list.length; i++) {
        v_node = p_plan_list[i];
        var v_node_element = document.getElementById(v_node.id);

        var v_bar_width = 100;
        var v_bar_progress_width = v_bar_width - 4;
        var v_bar_progress_width_value = v_bar_progress_width*v_node.progress_cost_percentage;
        if (v_bar_progress_width_value < 0) {
          v_bar_progress_width_value = v_bar_progress_width_value*(-1);
        }

        var v_fill_color = '#4a81d4';
        if (v_node.progress_cost_percentage > 0.3 && v_node.progress_cost_percentage < 0.6) {
          v_fill_color = '#ceb22b';
        }
        else if (v_node.progress_cost_percentage >= 0.6) {
          v_fill_color = '#ce2b2b';
        }

        v_progress_bar_html =
        '<svg ' +
          'class="' + this.defaultClass + '__progress-bar"' +
          'xmlns="http://www.w3.org/2000/svg"' +
          'width="' + v_bar_width + '"' +
          'height="8"' +
          'viewBox="0 0 ' + v_bar_width + ' 8" ' +
        '>' +
          '<path d="M 2 2 H ' + v_bar_progress_width_value + ' v 6 H -' + v_bar_progress_width_value + ' z" stroke="none" stroke-width="0" fill="' + v_fill_color + '" /></path>' +
          '<path d="M 2 2 H ' + v_bar_progress_width + ' v 6 H -' + v_bar_progress_width + ' z" stroke="#d2d2d2" stroke-width="1" fill="none" /></path>' +
        '</svg>';

        var v_node_svg_container = document.getElementById(v_node.id + '_svg_progress');
        v_node_svg_container.innerHTML = v_progress_bar_html;

        if (v_node.planList) {
          this.renderProgressBar(v_node.planList);
        }
      }
    },
    renderSvg : function(p_plan_list) {

      // Create progress bars for each node and subsequent child;
      this.renderProgressBar(p_plan_list);

      var v_parent_container = this.divGridContainer;

      var v_parent_params = {
        container: v_parent_container,
        width: v_parent_container.offsetWidth,
        height: v_parent_container.offsetHeight
      }
      // Create svg paths for each combination of node - child_node
      var v_svg_paths_html = this.renderSvgPath(p_plan_list, v_parent_params);

      var v_svg_id = this.id + '_svg';
      var v_svg_element = document.getElementById(v_svg_id);
      if (v_svg_element) {
        v_svg_element.remove();
      }

      var v_svg_html =
      '<svg ' +
        'id="' + v_svg_id + '"' +
        'class="' + this.defaultClass + '__svg"' +
        'xmlns="http://www.w3.org/2000/svg"' +
        'width="' + v_parent_params.width + '"' +
        'height="' + v_parent_params.height + '" ' +
        'viewBox="0 0 ' + v_parent_params.width + ' ' + v_parent_params.height + '" ' +
        'style="position: absolute; top: 0px; left: 0px;"' +
      '>' +
        v_svg_paths_html +
      '</svg>';

      this.divGridContainer.innerHTML += v_svg_html;

    },
    renderSvgPath : function(p_plan_list, p_parent_params) {
      var v_svg_html = '';

      for (let i = 0; i < p_plan_list.length; i++) {
        // Compare existence of child_nodes inside each node
        var v_node = p_plan_list[i];
        if (v_node) {
          var v_node_child_list = v_node.planList;

          if (v_node_child_list) {
            // Get position attributes of the v_node (source of the line)
            var v_source = document.getElementById(v_node.id);
            if (v_source) {
              // var v_source_rect = v_source.getBoundingClientRect();
              var v_source_x = (v_source.offsetWidth / 2) + v_source.offsetLeft;
              var v_source_y = v_source.offsetTop + v_source.offsetHeight;

              for (let j = 0; j < v_node_child_list.length; j++) {
                // Get the position of each v_child_node (target of the line)
                var v_child_node = v_node_child_list[j];
                var v_target = document.getElementById(v_child_node.id);
                if (v_target) {
                  // var v_target_rect = v_target.getBoundingClientRect();
                  var v_target_x = (v_target.offsetWidth / 2) + v_target.offsetLeft;
                  var v_target_y = v_target.offsetTop;

                  var v_avg_width = v_target_x - v_source_x + 40;
                  var v_path_style = 'style="stroke-dasharray:' + v_avg_width + '; stroke-dashoffset:' + v_avg_width + '"';

                  // Create a path between the node and the node_child (source - target)
                  if (j > 0) {
                    // Account for line curves with 20 radius
                    v_target_x = v_target_x - 20;
                    // v_target_y = v_target_y + 40;
                    v_svg_html += '<path ' + v_path_style + ' d="M ' + v_source_x + ' ' + v_source_y + ' c 0 20, 0 20, 20 20 H ' + v_target_x + ' c 20 0, 20 0, 20 20 V ' + v_target_y + '" stroke="#4a81d4" stroke-width="1" fill="none" /></path>';
                  }
                  else {
                    v_svg_html += '<path ' + v_path_style + ' d="M ' + v_source_x + ' ' + v_source_y + ' L ' + v_target_x + ' ' + v_target_y + '" stroke="#4a81d4" stroke-width="1" fill="none" /></path>';
                  }
                }
              }
              // Recursively adds path for each subsequent child of thid v_child_node
              v_svg_html += this.renderSvgPath(v_node_child_list, p_parent_params);
            }
          }
        }
      }

      return v_svg_html;
    },
    renderTarget : function(p_plans_html) {
      var v_lagereControl = this;

      var v_parent = v_lagereControl.targetDiv;
      var v_parent_width = v_parent.clientWidth;
      var v_parent_height = v_parent.clientHeight;

      // Creates outter element of the component once
      if (!v_lagereControl.divElement) {
        v_lagereControl.divElement = document.createElement('div');
        v_lagereControl.divElement.setAttribute('id', v_lagereControl.id);
        v_lagereControl.divElement.classList = this.defaultClass + '__wrapper';

        // Template options when there's no targetDiv and the component needs a modal to render to render inside
        if (!v_lagereControl.targetDiv) {
          v_lagereControl.divElement.setAttribute(
            'style',
            `
            background-color: ` + v_lagereControl.backgroundColor + `;
            box-shadow: 1px 0px 3px rgba(0,0,0,0.15);
            display:none;
            height: 90vh;
            left: 5vw;
            max-width: 90vw;
            padding: 5px;
            position:fixed;
            top: 5vh;
            width: 90vw;
            z-index: 99999999;
            `
          );

          document.body.appendChild(v_lagereControl.divElement);

          // Adds close button to the modal
          var v_close_btn_html = '<div style="position:relative;"><button id="' + v_lagereControl.id + '_btn_close" type="button" class="btn btn-sm btn-danger ml-auto" style="position: absolute; top: -10px; right: -10px;"><i class="fas fa-times"></i></button></div>';
          v_lagereControl.divElement.innerHTML = v_close_btn_html;
        }
        // Template options when there's a targetDiv to render inside
        else {
          v_lagereControl.divElement.setAttribute(
            'style',
            `
            background-color: ` + v_lagereControl.backgroundColor + `;
            display:none;
            height:` + v_parent_height + `px;
            max-width: 100%;
            padding: 5px;
            width:` + v_parent_width + `px;
            z-index: 99999999;
            `
          );
          v_lagereControl.targetDiv.appendChild(v_lagereControl.divElement);
        }

        v_lagereControl.divElementContent = document.createElement('div');
        v_lagereControl.divElementContent.setAttribute('id', v_lagereControl.id + '_content');
        v_lagereControl.divElementContent.setAttribute('style', 'width:' + v_parent_width + 'px; height:' + v_parent_height + 'px; overflow: auto;');

        v_lagereControl.divElement.appendChild(v_lagereControl.divElementContent);

        v_lagereControl.divGrid = document.createElement('div');
        v_lagereControl.divGrid.style['grid-gap'] = '40px 10px';
        v_lagereControl.divGrid.style.display = 'grid';
        v_lagereControl.divGrid.style.position = 'relative';
        v_lagereControl.divGrid.style['z-index'] = 1;
        v_lagereControl.divGridContainer = document.createElement('div');
        v_lagereControl.divGridContainer.style.position = 'relative';
        v_lagereControl.divGridContainer.appendChild(v_lagereControl.divGrid);
        v_lagereControl.divElementContent.appendChild(v_lagereControl.divGridContainer);
      }

      // TODO:
      // - validate with other smaples the need of fixed row and column widths
      // - fix totalCols evaluation

      // var v_grid_col_attr = '200px';
      // for (let i = 1; i < this.totalCols; i++) {
        // v_grid_col_attr += ' 200px';
      // }

      // var v_grid_row_attr = '1fr';
      // for (let i = 0; i < this.totalRows; i++) {
        // v_grid_row_attr += ' 1fr';
      // }

      // this.divGrid.style['grid-template-columns'] = v_grid_col_attr;
      // this.divGrid.style['grid-template-rows'] = v_grid_row_attr;

      // Sets the new content for the divGrid
      v_lagereControl.divGrid.innerHTML = p_plans_html;

      // Render the svg with path lines based on the content positions
      setTimeout(function(){
        v_lagereControl.renderSvg(v_lagereControl.planList);
      }, 150);

      // Adds the click event to the button when there's no targetDiv and the component needs a modal to render to render inside
      if (!v_lagereControl.targetDiv) {
        var v_close_btn = document.getElementById(v_lagereControl.id + '_btn_close');
        if (v_close_btn !== undefined && v_close_btn !== null) {
          v_close_btn.onclick = function(){v_lagereControl.setStateDisabled()};
        }
      }

      v_lagereControl.divElement.style.display = 'block';
    },
    resize() {
      v_lagereControl = this;

      if (v_lagereControl.divElement) {
        var v_parent = v_lagereControl.targetDiv;
        var v_parent_width = v_parent.clientWidth;
        var v_parent_height = v_parent.clientHeight;

        v_lagereControl.divElement.setAttribute(
          'style',
          `
          background-color: ` + v_lagereControl.backgroundColor + `;
          display:none;
          height:` + v_parent_height + `px;
          max-width: 100%;
          padding: 5px;
          width:` + v_parent_width + `px;
          z-index: 99999999;
          `
        );

        v_lagereControl.divElementContent.setAttribute('style', 'width:' + v_parent_width + 'px; height:' + v_parent_height + 'px; overflow: auto; padding: 10px;');

        if (v_lagereControl.stateActive) {
          this.divElement.style.display = 'block';

          // Render the svg with path lines based on the content positions
          setTimeout(function(){
            v_lagereControl.renderSvg(v_lagereControl.planList);
          }, 150);
        }

      }
    },
    setStateEnabled: function() {
      this.stateActive = true;
    },
    setStateDisabled : function() {
      this.stateActive = false;
      this.updatePlanList([]);
      this.renderPlans();
    },
    updateRowsColsCount : function() {

      this.totalRows = this.planCountMatrix.length;

      var v_temp_largest_row = 0;

      for (let i = 0; i < this.totalRows; i++) {
        if (this.planCountMatrix[i] > v_temp_largest_row)
          v_temp_largest_row = this.planCountMatrix[i];
      }

      this.totalCols = v_temp_largest_row;

    },
    updateLagerePosition : function() {
      // TODO
    }
  }

  return v_lagereControl;

}
