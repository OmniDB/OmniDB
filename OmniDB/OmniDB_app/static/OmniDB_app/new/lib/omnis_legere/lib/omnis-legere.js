/*
Copyright 2015-2020 The OmniDB Team
This file is part of OmniDB.
OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.
OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

function createLegere(p_context = {parent: window, self: 'omnisLegere'}, p_options) {

  var v_legereControl = {
    // Params
    backgroundColor: (p_options.backgroundColor) ? p_options.backgroundColor : '#e2e2e2',
    context: p_context,
    data: [],
    dataMatrix: [],
    defaultClass: (p_options.bem_class_root) ? p_options.bem_class_root : 'omnis-legere',
    defaultMessage: 'No content',
    divElement: false,
    global_children_count: 0,
    global_collapse: false,
    grid: {
      col_count: 0,
      row_count: 0,
    },
		id: 'omnis_legere_control_' + Date.now(),
    planCounter: 0,
    planCountMatrix: [0],
    planList: [],
		stateActive: false,
    targetDiv: (p_options.target) ? p_options.target : false,
    totalCols: 0,
    totalRows: 0,
    // Actions
    emptyPlanList : function() {
      this.data = [];
      this.dataMatrix = [];
      this.global_children_count = 0;
      this.grid = {
        col_count: 0,
        row_count: 0,
      };
      this.planCounter = 0;
      this.planCountMatrix = [0];
      this.planList = [];
      this.totalCols = 0;
      this.totalRows = 0;
    },
    updatePlanList : function(p_data) {
      var v_data = [];
      for (let i = 0; i < p_data.length; i++) {
        v_data.push(p_data[i]);
      }
      this.emptyPlanList();
      this.data = v_data;
      this.setStateEnabled();
      this.createPlans();
      this.renderPlans();
    },
    goToPlan : function(p_index) {
      this.stepSelected = p_index;
      this.renderStep();
    },
    /**
    * @params:
    * - p_data: node
    * - p_index: position of the node inside the array
    * - p_index_map: array[..., grand_parent_index, parent_index, node_index]
    **/
    createPlanCountMatrix: function({
      p_data = {},
      p_index = 0,
      p_index_map = []
    }) {
      var v_legereControl = this;
      // Updates total_count of nodes
      v_legereControl.planCounter++;

      var v_node = p_data;
      var v_index = p_index;
      var v_index_map = [];

      // Update v_index_map with parent p_index_map
      for (let i = 0; i < p_index_map.length; i++) {
        v_index_map.push(p_index_map[i]);
      }

      // Add current index to v_index_map
      v_index_map.push(v_index);

      // Get row
      var v_row = v_index_map.length - 1;
      // Get col
      var v_col = v_index;

      // Create child node
      if (v_node['Plans']) {
        if (v_node['Plans'].length > 0) {
          for (let i = 0; i < v_node['Plans'].length; i++) {
            this.createPlanCountMatrix({
              p_data: v_node['Plans'][i],
              p_index: i,
              p_index_map: v_index_map
            });
          }
        }
        else {
          v_col += 1
        }
      }
      else {
        v_col += 1
      }

      this.planCountMatrix.push([v_row, v_col]);

    },
    createDataMatrix: function() {
      this.total_progress_key_name = (this.data[0]['Plan']['Actual Total Time']) ? 'Actual Total Time' : 'Total Cost';
      this.total_progress_cost = 0;

      // Deep Search
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
    },
    createPlan : function({
      p_data = {},
      p_index = 0,
      p_index_map = []
    }) {
      var v_legereControl = this;
      // Updates total_count of nodes
      v_legereControl.planCounter++;

      if (p_data.omnis_legere_control === undefined) {
        p_data.omnis_legere_control = {
          is_collapsed: v_legereControl.global_collapse
        }
      }
      else if (p_data.omnis_legere_control.is_collapsed === undefined) {
        p_data.omnis_legere_control.is_collapsed = v_legereControl.global_collapse;
      }

      var v_id = v_legereControl.id + '_plan';
      var v_node = p_data;
      var v_index = p_index;
      var v_index_map = [];

      // Update v_index_map with parent p_index_map
      for (let i = 0; i < p_index_map.length; i++) {
        v_index_map.push(p_index_map[i]);
        v_index += p_index_map[i];
      }

      // Add current index to v_index_map
      v_index_map.push(v_index);

      // Get row
      var v_row = v_index_map.length;
      // Get col
      var v_col = v_legereControl.global_col_count;

      var v_plan_list = [];

      var v_data = {};
      Object.keys(p_data).forEach(function (p_data_key) {
        if (p_data_key !== 'Plans' && p_data_key !== 'omnis_legere_control') {
          v_data[p_data_key] = p_data[p_data_key];
        }
      });

      // var v_children_count = 0;
      // if (p_data['Plans']) {
      //   if (p_data['Plans'].length > 0) {
      //     v_children_count = p_data['Plans'].length;
      //   }
      // }


      var v_plan = {
        // children_count: v_children_count,
        data: v_data,
        grid: {
          // col: (v_children_count === 0) ? v_index + 1 : v_index + v_legereControl.global_children_count + 1,
          col: v_legereControl.global_children_count + 1,
          row: v_row
        },
				id: v_id,
        index: v_index,
        index_map: v_index_map,
        omnis_legere_control: p_data.omnis_legere_control,
        planList: []
			};


      // Create child plans
      var v_plan_cost = v_plan.data[v_legereControl.total_progress_key_name];

      var v_plan_total_cost = {
        label: v_legereControl.total_progress_key_name + ' (accumulated cost)',
        percentage: v_plan_cost / v_legereControl.total_progress_cost,
        value: v_plan_cost
      }

      v_plan.total_cost = v_plan_total_cost;

      var v_plan_node_cost = {
        label: v_legereControl.total_progress_key_name + ' (node cost)',
        value: v_plan_cost
      }

      if (p_data['Plans']) {
        if (p_data['Plans'].length > 0) {

          v_legereControl.grid.row_count += 1;

          for (let i = 0; i < p_data['Plans'].length; i++) {
            v_plan.global_children_count += 1;
            var v_new_plan = this.createPlan({
              p_data: p_data['Plans'][i],
              p_index: i,
              p_index_map: v_plan.index_map
            });
            v_plan.planList.push(v_new_plan);

            v_plan_node_cost.value -= v_new_plan.data[v_legereControl.total_progress_key_name];

          }
        }
        else {
          v_legereControl.global_children_count += 1;
        }
      }
      else {
        v_legereControl.global_children_count += 1;
      }

      // v_plan.grid.row = v_row + 1;
      // v_plan.grid.col = v_col + 1;

      // console.log(v_plan_progress_cost_total, v_new_plan_progress_cost_total);

      v_plan_node_cost.percentage = v_plan_node_cost.value / v_legereControl.total_progress_cost;

      v_plan.node_cost = v_plan_node_cost;

      // Update node_id with index map
      for (let i = 0; i < v_index_map.length; i++) {
        v_plan.id += '_' + v_index_map[i];
      }

      return v_plan;
    },
    createPlans : function() {
      this.createDataMatrix();

      this.grid.row_count += 1;

			for (let i = 0; i < this.data.length; i++) {
        var v_new_plan = this.createPlan({
          p_data: this.data[i]['Plan'],
          p_index: i,
          p_index_map: []
        });

        this.planList.push(v_new_plan);
      }
    },
    destroy : function() {
      v_legereControl = this;

      v_legereControl.divElement.remove();

      v_legereControl.context.parent[v_legereControl.context.self] = null;

      delete v_legereControl.context.parent[v_legereControl.context.self];
    },
    setClickEventButtonToggleCollapse: function(p_node) {
      var v_legereControl = this;


      var node_button_toggle_collapse_update = document.getElementById(p_node.id + '_button_toggle_collapse_update');

      node_button_toggle_collapse_update.onclick = function(event){
        v_legereControl.toggleCollapseNodeUpdate(p_node.index_map);
      }

      var v_child_node = null;

      // Recursively creates the buttons for the children
      if (p_node.planList) {
        for (let i = 0; i < p_node.planList.length; i++) {
          v_child_node = p_node.planList[i];
          this.setClickEventButtonToggleCollapse(v_child_node);
        }
      }
    },
    renderPlan : function(p_plan_item) {
      var v_legereControl = this;
      var v_plan_item = p_plan_item;
      var v_plans_html = '';

      var v_title = '';
      var v_progress_cost_html = '';
      if (v_plan_item.data['Node Type']) {
        var v_child_count = (v_plan_item['planList'] !== undefined) ? v_plan_item['planList'].length : 0;

        v_title +=
        '<div class="' + this.defaultClass + '__title card-title p-2 mb-0"><h5 class="mb-0">' +
          '<strong>' + v_plan_item.data['Node Type'] + '</strong>' +
          '<span>(' + v_child_count + ')</span>' +
        '</h5></div>';

        var v_temp_progress_bars_data = [
          v_plan_item.total_cost,
          v_plan_item.node_cost
        ];

        v_progress_cost_html +=
        '<div class="' + this.defaultClass + '__body card-body p-2">';

        for (let i = 0; i < v_temp_progress_bars_data.length; i++) {
          var temp_bar_data = v_temp_progress_bars_data[i];
          v_progress_cost_html +=
          '<div id="' + v_plan_item.id + '_svg_progress_' + i + '"></div>' +
          '<div>' + temp_bar_data.label + '</div>' +
          '<div>- percentage: ' + (100*temp_bar_data.percentage) + '%</div>' +
          '<div>- value: ' + temp_bar_data.value + '</div>';
        }

        var v_data_html =
        '<div class="mb-2">Toggle node data <button id="' + v_plan_item.id + '_button_toggle_collapse_update" class="btn btn-sm omnidb__theme__btn--secondary ml-2 ' + v_legereControl.defaultClass + '__btn-toggle-collapse-update" data-index-map="' + v_plan_item.index_map + '"></button></div>' +
        '<div class="alert alert-info mt-2">';
        Object.keys(v_plan_item.data).forEach(function (p_data_key) {
          v_data_html +=
          '<div>' + p_data_key + ': <span class="text-danger">' + v_plan_item.data[p_data_key] + '</span></div>';
        });
        v_data_html +=
        '</div>';

        v_data_html +=
        '</div>';
      }
      // CSS Grid ROWxCOL starts from 1, take this into account for p_index_map
      // var v_index = v_plan_item.index;
      // var v_index_map = v_plan_item.index_map;
      // var v_row_depth = v_index_map.length - 1;
      // Get the grid_row
      // var v_grid_row = v_plan_item.index_map.length;
      // var v_grid_col = 0;
      // To prevent overlapping of child_nodes, we need to offset move each node to the right ,base on the number of child_nodes inside the previous node

      // var v_parent_row = null;
      // var v_temp_parent_node = null;
      // var v_temp_parent_node_child_list = this.planList;
      // var v_col_offset_shift = 0;
      // Find parent_row
      // Get the grid_col. Col initial number is the value of the index + 1 to account for CSS Grid start at 1.
      // if (v_row_depth === 0) {
      //   v_grid_col = v_index + 1;
      //   v_temp_parent_node = v_plan_item;
      // }
      // else {
      //   if (v_row_depth === 1) {
      //     v_temp_parent_node = this.planList[v_index_map[0]];
      //     v_temp_parent_node_child_list = v_temp_parent_node.planList;
      //   }
      //   else {
      //     for (let i = 0; i < v_row_depth; i++) {
      //       v_temp_parent_node = v_temp_parent_node_child_list[v_index_map[i]];
      //       v_temp_parent_node_child_list = v_temp_parent_node.planList;
      //     }
      //   }
      //
      //   v_grid_col = v_temp_parent_node.index_as_parent + v_index;
      //
      //   v_parent_row = v_temp_parent_node_child_list;
      //   // Find number of children on previous nodes in the same row and add to the col_offset_shit
      //   for (let i = 0; i < v_index; i++) {
      //
      //     if (v_parent_row[i]) {
      //       var v_previous_node = v_parent_row[i];
      //       if (v_row_depth === 10) {
      //         console.log('v_parent_row', v_parent_row);
      //         console.log('v_previous_node', v_previous_node);
      //       }
      //       if (v_previous_node && v_plan_item.planList) {
      //         if (v_previous_node.planList && v_plan_item.planList.length > 1) {
      //           v_col_offset_shift += v_previous_node.planList.length - 1;
      //         }
      //       }
      //     }
      //
      //     v_grid_col += v_col_offset_shift;
      //   }
      // }
      // else {
      //   if (v_row_depth === 1) {
      //     v_temp_parent_node = this.planList[v_index_map[0]];
      //     v_temp_parent_node_child_list = v_temp_parent_node.planList;
      //   }
      //   else {
      //     for (let i = 0; i < v_row_depth; i++) {
      //       v_temp_parent_node = v_temp_parent_node_child_list[v_index_map[i]];
      //       v_temp_parent_node_child_list = v_temp_parent_node.planList;
      //     }
      //   }
      //   v_grid_col = v_index;
      // }

      v_grid_row = v_plan_item.grid.row;
      v_grid_col = v_plan_item.grid.col;


      var v_plan_item_state_classes = ' ';
      if (v_plan_item.omnis_legere_control.is_collapsed) {
        v_plan_item_state_classes += this.defaultClass + '__item--is_collapsed ';
      }



      // Setting color
      var v_node_percentage = v_plan_item.node_cost.percentage;

      var v_fill_color = false;
      if (v_node_percentage > 0.3 && v_node_percentage < 0.6) {
        v_fill_color = '#ceb22b;';
      }
      else if (v_node_percentage >= 0.6) {
        v_fill_color = '#ce2b2b;';
      }
      var v_temp_card_color = (v_fill_color) ? 'box-shadow: 0px 4px 12px ' + v_fill_color : '';




      var v_plans_html =
      '<div id="' + v_plan_item.id + '" class="' + this.defaultClass + '__item ' + v_plan_item_state_classes + '" style="grid-row: ' + v_grid_row + '; grid-column:' + v_grid_col + '">' +
        '<div class="' + this.defaultClass + '__card card" style="' + v_temp_card_color + '">' +
          v_title +
          v_progress_cost_html +
          v_data_html +
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
        var v_legereControl = this;

        var v_plans_html = '';

        for (let i = 0; i < this.planList.length; i++) {
          v_plans_html += this.renderPlan(this.planList[i]);
        }

        this.renderTarget(v_plans_html);
      }
      else {
        this.divElement.style.display = 'none';
      }
    },
    renderProgressBar : function(p_plan_list) {
      var v_legereControl = this;
      var v_node = null;

      for (let i = 0; i < p_plan_list.length; i++) {
        v_node = p_plan_list[i];
        var v_node_element = document.getElementById(v_node.id);


        var node_button_toggle_collapse_update = document.getElementById(v_node.id + '_button_toggle_collapse_update');

        if (node_button_toggle_collapse_update !== null) {
          if (v_node.omnis_legere_control.is_collapsed) {
            node_button_toggle_collapse_update.innerHTML = '<i class="fas fa-eye-slash"></i>';
          }
          else {
            node_button_toggle_collapse_update.innerHTML = '<i class="fas fa-eye"></i>';
          }
        }


        var v_bar_width = 100;
        // temp_params_for_style_construction
        var v_temp_progress_bars_data = [
          v_node.total_cost,
          v_node.node_cost
        ]
        var temp_svg_path_html = '';
        // Style construction
        for (let j = 0; j < v_temp_progress_bars_data.length; j++) {
          var v_bar_data = v_temp_progress_bars_data[j];
          var v_bar_data_label = v_bar_data.label;
          var v_bar_data_percentage = v_bar_data.percentage;
          var v_bar_data_value = v_bar_data.value;
          var v_bar_progress_width = v_bar_width - 4;
          var v_bar_progress_width_value = v_bar_progress_width*v_bar_data_percentage;
          if (v_bar_progress_width_value < 0) {
            v_bar_progress_width_value = v_bar_progress_width_value*(-1);
          }

          var v_fill_color = '#4a81d4';
          if (v_bar_data_percentage > 0.3 && v_bar_data_percentage < 0.6) {
            v_fill_color = '#ceb22b';
          }
          else if (v_bar_data_percentage >= 0.6) {
            v_fill_color = '#ce2b2b';
          }

          var v_progress_bar_html =
          '<svg ' +
            'class="' + this.defaultClass + '__progress-bar"' +
            'xmlns="http://www.w3.org/2000/svg"' +
            'width="' + v_bar_width + '"' +
            'height="8"' +
            'viewBox="0 0 ' + v_bar_width + ' 8" ' +
          '>' +
            // path progress bar
            '<path ' +
              'd="M 2 2 ' +
              'H ' + v_bar_progress_width_value + ' ' +
              'v 6 ' +
              'H 2 z" ' +
              'stroke="none" ' +
              'stroke-width="0" ' +
              'fill="' + v_fill_color + '" ' +
            '></path>' +
            // path progress border
            '<path ' +
              'd="M 2 2 ' +
              'H ' + v_bar_progress_width + ' ' +
              'v 6 ' +
              'H 2 z" ' +
              'stroke="#d2d2d2" ' +
              'stroke-width="1" ' +
              'fill="none" ' +
            '></path>' +
          '</svg>';
          var v_node_svg_container = document.getElementById(v_node.id + '_svg_progress_' + j);
          if (v_node_svg_container) {
            v_node_svg_container.innerHTML = v_progress_bar_html;
          }
        }

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
        width: v_parent_container.scrollWidth,
        height: v_parent_container.scrollHeight
      }
      // Create svg paths for each combination of node - child_node
      var v_svg_paths_html = this.renderSvgPath(p_plan_list);

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

      this.divGridContainer = document.getElementById(v_legereControl.divGridContainerId);

      if (this.divGridContainer !== null) {
        this.divGridContainer.innerHTML += v_svg_html;

        // Create node button toggle collapse content and events
        for (let i = 0; i < p_plan_list.length; i++) {
          var v_node = p_plan_list[i];
          this.setClickEventButtonToggleCollapse(v_node);
        }
      }

    },
    renderSvgPath : function(p_plan_list) {
      var v_svg_html = '';

      for (let i = 0; i < p_plan_list.length; i++) {
        // Compare existence of child_nodes inside each node
        var v_node = p_plan_list[i];
        if (v_node) {
          var v_node_child_list = v_node.planList;

          if (v_node_child_list) {
            // Get position attributes of the v_node (source of the line)
            var v_source_id = document.getElementById(v_node.id);
            if (v_source_id) {
              var v_source = document.getElementById(v_node.id).lastChild;
              if (v_source) {
                // var v_source_rect = v_source.getBoundingClientRect();
                var v_source_x = (v_source.offsetWidth / 2) + v_source.offsetLeft;
                var v_source_y = v_source.offsetTop + v_source.offsetHeight;

                for (let j = 0; j < v_node_child_list.length; j++) {
                  // Get the position of each v_child_node (target of the line)
                  var v_child_node = v_node_child_list[j];
                  var v_target = document.getElementById(v_child_node.id).firstChild;
                  if (v_target) {
                    // var v_target_rect = v_target.getBoundingClientRect();
                    var v_target_x = (v_target.offsetWidth / 2) + v_target.offsetLeft;
                    var v_target_y = v_target.offsetTop;

                    var v_avg_width = v_target_x - v_source_x + v_source_y - v_target_y;
                    // var v_path_style = 'style="stroke-dasharray:' + (v_avg_width + 40) + '; stroke-dashoffset:' + v_avg_width + '"';
                    var v_path_style = '';

                    // Create a path between the node and the node_child (source - target)
                    if (j > 0) {
                      // Account for line curves with 20 radius
                      v_target_x = v_target_x - 20;
                      v_target_y = v_target_y - 40;
                      // v_target_y = v_target_y + 40;
                      v_svg_html += '<path ' + v_path_style + ' d="M ' + v_source_x + ' ' + v_source_y + ' V ' + v_target_y  + ' c 0 20, 0 20, 20 20 H ' + v_target_x + ' c 20 0, 20 0, 20 20 ' + '" stroke="#4a81d4" stroke-width="1" fill="none" /></path>';
                    }
                    else {
                      v_svg_html += '<path ' + v_path_style + ' d="M ' + v_source_x + ' ' + v_source_y + ' L ' + v_target_x + ' ' + v_target_y + '" stroke="#4a81d4" stroke-width="1" fill="none" /></path>';
                    }
                  }
                }
                // Recursively adds path for each subsequent child of thid v_child_node
                v_svg_html += this.renderSvgPath(v_node_child_list);
              }
            }
          }
        }
      }

      return v_svg_html;
    },
    renderTarget : function(p_plans_html) {
      var v_legereControl = this;

      var v_parent = v_legereControl.targetDiv;
      var v_parent_width = v_parent.clientWidth;
      var v_parent_height = v_parent.clientHeight;

      // Creates outter element of the component once
      if (!v_legereControl.divElement) {
        v_legereControl.divElement = document.createElement('div');
        v_legereControl.divElementId = v_legereControl.id;
        v_legereControl.divElement.setAttribute( 'id', v_legereControl.divElementId );
        v_legereControl.divElement.classList = this.defaultClass + '__wrapper';

        // Template options when there's no targetDiv and the component needs a modal to render to render inside
        if (!v_legereControl.targetDiv) {
          v_legereControl.divElement.setAttribute(
            'style',
            `
            background-color: ` + v_legereControl.backgroundColor + `;
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

          document.body.appendChild(v_legereControl.divElement);

          // Adds close button to the modal
          var v_close_btn_html = '<div style="position:relative;"><button id="' + v_legereControl.id + '_btn_close" type="button" class="btn btn-sm btn-danger ml-auto" style="position: absolute; top: -10px; right: -10px;"><i class="fas fa-times"></i></button></div>';
          v_legereControl.divElement.innerHTML = v_close_btn_html;
        }
        // Template options when there's a targetDiv to render inside
        else {
          v_legereControl.divElement.setAttribute(
            'style',
            `
            background-color: ` + v_legereControl.backgroundColor + `;
            display:none;
            height:` + v_parent_height + `px;
            max-width: 100%;
            padding: 5px;
            position: relative;
            width:` + v_parent_width + `px;
            z-index: 99999999;
            `
          );
          v_legereControl.targetDiv.appendChild(v_legereControl.divElement);
        }

        v_legereControl.divElementContent = document.createElement('div');
        v_legereControl.divElementContentId = v_legereControl.id + '_content';
        v_legereControl.divElementContent.setAttribute('id', v_legereControl.divElementContentId);
        v_legereControl.divElementContent.setAttribute('style', 'width:' + v_parent_width + 'px; height:' + v_parent_height + 'px; overflow: auto; padding: 10px;');

        v_legereControl.divElement.appendChild(v_legereControl.divElementContent);

        v_legereControl.divGrid = document.createElement('div');
        v_legereControl.divGridId = v_legereControl.id + '_div_grid';
        v_legereControl.divGrid.setAttribute('id', v_legereControl.divGridId);
        v_legereControl.divGrid.style['grid-gap'] = '40px 40px';
        v_legereControl.divGrid.style.display = 'grid';
        v_legereControl.divGrid.style.position = 'relative';
        v_legereControl.divGrid.style['z-index'] = 1;
        v_legereControl.divGridContainer = document.createElement('div');
        v_legereControl.divGridContainerId = v_legereControl.id + '_div_grid_container';
        v_legereControl.divGridContainer.setAttribute('id', v_legereControl.divGridContainerId);
        v_legereControl.divGridContainer.style.position = 'relative';
        v_legereControl.divGridContainer.style['transform-origin'] = 'top left';
        v_legereControl.divGridContainer.style['transform'] = 'scale(1)';
        v_legereControl.divGridContainer.style['transition'] = 'transform 0.3s ease 0s';
        v_legereControl.divGridContainer.appendChild(v_legereControl.divGrid);
        v_legereControl.divElementContent.appendChild(v_legereControl.divGridContainer);

        // Create control panel buttons
        var v_control_panel_div = document.createElement('div');
        v_control_panel_div.classList = v_legereControl.defaultClass + '__control-panel';
        v_control_panel_div.setAttribute('style', 'align-items: center; display: flex; position: absolute; right: 15px; top: 15px;');

        v_control_panel_div.innerHTML =
        '<button id="' + v_legereControl.id + '_control_panel_button_toggle_collapse_update" class="btn btn-sm omnidb__theme__btn--secondary"><i class="fas fa-eye"></i></button>' +
        '<button id="' + v_legereControl.id + '_control_panel_button_zoomin" class="btn btn-sm omnidb__theme__btn--secondary ml-2"><i class="fas fa-search-plus"></i></button>' +
        '<button id="' + v_legereControl.id + '_control_panel_button_zoomout" class="btn btn-sm omnidb__theme__btn--secondary ml-2"><i class="fas fa-search-minus"></i></button>' +
        '<button id="' + v_legereControl.id + '_control_panel_button_fit" class="btn btn-sm omnidb__theme__btn--secondary ml-2"><i class="fas fa-vector-square"></i></button>' +
        '<button id="' + v_legereControl.id + '_control_panel_button_reset" class="btn btn-sm omnidb__theme__btn--secondary ml-2">reset</button>';

        v_legereControl.divElementContent.appendChild(v_control_panel_div);

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
      document.getElementById(v_legereControl.divGridId).innerHTML = p_plans_html;


      // Adds the click event to the control panel buttons
      var v_toggle_collapse_update_btn = document.getElementById(v_legereControl.id + '_control_panel_button_toggle_collapse_update');
      if (v_toggle_collapse_update_btn !== undefined && v_toggle_collapse_update_btn !== null) {
        v_toggle_collapse_update_btn.onclick = function(){
          v_legereControl.global_collapse = !v_legereControl.global_collapse;
          var v_toggle_collapse = v_legereControl.global_collapse;
          if (v_toggle_collapse) {
            v_toggle_collapse_update_btn.innerHTML = '<i class="fas fa-eye-slash"></i>';
          }
          else {
            v_toggle_collapse_update_btn.innerHTML = '<i class="fas fa-eye"></i>';
          }
          v_legereControl.toggleCollapseUpdate('all', false, v_toggle_collapse);
        };
      }
      var v_div_grid_container = document.getElementById(v_legereControl.id + '_div_grid_container');
      var v_zoomin_btn = document.getElementById(v_legereControl.id + '_control_panel_button_zoomin');
      if (v_zoomin_btn !== undefined && v_zoomin_btn !== null) {
        v_zoomin_btn.onclick = function(){
          var v_zoom_value = v_div_grid_container.style['transform'];
          v_zoom_value = v_zoom_value.split("scale(")[1];
          v_zoom_value = v_zoom_value.split(")")[0];
          v_zoom_value = parseFloat(v_zoom_value);
          v_zoom_value = v_zoom_value + 0.1;
          v_div_grid_container.style['transform'] = 'scale(' + v_zoom_value + ')';
        };
      }
      var v_zoomout_btn = document.getElementById(v_legereControl.id + '_control_panel_button_zoomout');
      if (v_zoomout_btn !== undefined && v_zoomout_btn !== null) {
        v_zoomout_btn.onclick = function(){
          var v_zoom_value = v_div_grid_container.style['transform'];
          v_zoom_value = v_zoom_value.split("scale(")[1];
          v_zoom_value = v_zoom_value.split(")")[0];
          v_zoom_value = parseFloat(v_zoom_value);
          v_zoom_value = v_zoom_value - 0.1;
          v_div_grid_container.style['transform'] = 'scale(' + v_zoom_value + ')';
        };
      }
      var v_fit_btn = document.getElementById(v_legereControl.id + '_control_panel_button_fit');
      if (v_fit_btn !== undefined && v_fit_btn !== null) {
        v_fit_btn.onclick = function(){
          var v_content_div = document.getElementById(v_legereControl.id + '_content');
          var v_svg_div = document.getElementById(v_legereControl.id + '_svg');
          var v_h_value = v_svg_div.clientWidth;
          var v_content_h_value = v_content_div.offsetWidth;
          var v_h_ratio = v_content_h_value / v_h_value;
          var v_v_value = v_svg_div.clientHeight;
          var v_content_v_value = v_content_div.offsetHeight;
          var v_v_ratio = v_content_v_value / v_v_value;
          if (v_h_ratio < v_v_ratio) {
            v_div_grid_container.style['transform'] = 'scale(' + v_h_ratio + ')';
          }
          else {
            v_div_grid_container.style['transform'] = 'scale(' + v_v_ratio + ')';
          }
        };
      }
      var v_reset_btn = document.getElementById(v_legereControl.id + '_control_panel_button_reset');
      if (v_reset_btn !== undefined && v_reset_btn !== null) {
        v_reset_btn.onclick = function(){
          v_div_grid_container.style['transform'] = 'scale(1)';
        };
      }

      // Render the svg with path lines based on the content positions
      setTimeout(function(){
        v_legereControl.renderSvg(v_legereControl.planList);
      }, 150);

      // Adds the click event to the button when there's no targetDiv and the component needs a modal to render to render inside
      if (!v_legereControl.targetDiv) {
        var v_close_btn = document.getElementById(v_legereControl.id + '_btn_close');
        if (v_close_btn !== undefined && v_close_btn !== null) {
          v_close_btn.onclick = function(){v_legereControl.setStateDisabled()};
        }
      }

      v_legereControl.divElement.style.display = 'block';

    },
    resize() {
      v_legereControl = this;

      if (v_legereControl.divElement) {
        var v_parent = v_legereControl.targetDiv;
        var v_parent_width = v_parent.clientWidth;
        var v_parent_height = v_parent.clientHeight;

        v_legereControl.divElement.setAttribute(
          'style',
          `
          background-color: ` + v_legereControl.backgroundColor + `;
          display:none;
          height:` + v_parent_height + `px;
          max-width: 100%;
          padding: 5px;
          position: relative;
          width:` + v_parent_width + `px;
          z-index: 99999999;
          `
        );

        v_legereControl.divElementContent.setAttribute('style', 'width:' + v_parent_width + 'px; height:' + v_parent_height + 'px; overflow: auto; padding: 10px;');

        if (v_legereControl.stateActive) {
          this.divElement.style.display = 'block';

          // Render the svg with path lines based on the content positions
          setTimeout(function(){
            v_legereControl.renderSvg(v_legereControl.planList);
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
    },
    toggleCollapse: function(p_type = false, p_node = false, p_set_state = null) {
      var v_legereControl = this;
      if (p_type === 'all') {
        var v_node_list = [];
        if (p_node) {
          v_legereControl.toggleCollapse(false, p_node, p_set_state);
          v_node_list = p_node.Plans;
          if (v_node_list) {
            for (let i = 0; i < v_node_list.length; i++) {
              var v_child_node = v_node_list[i];
              v_legereControl.toggleCollapse('all', v_child_node, p_set_state);
            }
          }
        }
        else {
          var v_data = v_legereControl.data;
          if (v_data) {
            v_node_list = v_legereControl.data;
            if (v_node_list) {
              for (let i = 0; i < v_node_list.length; i++) {
                if (v_node_list[i].Plan) {
                  var v_node = v_node_list[i].Plan;
                  v_legereControl.toggleCollapse('all', v_node, p_set_state);
                }
              }
            }
          }
        }
      }
      else if (p_set_state !== null && p_node) {
        p_node.omnis_legere_control.is_collapsed = p_set_state;
      }
      else if (p_node) {
        p_node.omnis_legere_control.is_collapsed = !p_node.omnis_legere_control.is_collapsed;
      }
    },
    toggleCollapseNodeUpdate: function(p_index_map) {
      var v_legereControl = this;

      var v_parent_node = v_legereControl.data[p_index_map[0]];

      if (p_index_map.length === 1) {
        v_legereControl.toggleCollapseUpdate(false, v_parent_node.Plan, null);
      }
      else {
        var v_node_list = v_parent_node.Plans;
        let v_temp_node = null;
        let v_temp_list = null;

        for (let i = 0; i < p_index_map.length; i++) {
          var v_index = p_index_map[i];
          if (i === 0) {
            v_temp_node = v_parent_node;
          }
          else {
            if (v_temp_node.Plan) {
              v_temp_list = v_temp_node.Plan.Plans;
              if (v_temp_list) {
                v_temp_node = v_temp_list[v_index];
                if (i === p_index_map.length - 1) {
                  v_legereControl.toggleCollapseUpdate(false, v_temp_node, null);
                }
              }
            }
          }
        }
      }

    },
    toggleCollapseUpdate: function(p_type = 'all', p_node = false, p_set_state = null) {
      this.toggleCollapse(p_type, p_node, p_set_state);
      var v_legereControl = this;
      this.updatePlanList(v_legereControl.data);
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
    updateLegerePosition : function() {
      // TODO
    }
  }

  return v_legereControl;

}
