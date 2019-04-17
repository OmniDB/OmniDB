/*
Copyright 2015-2017 The OmniDB Team

This file is part of OmniDB.

OmniDB is free software: you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation, either version 3 of the License, or (at your option) any later version.

OmniDB is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.

You should have received a copy of the GNU General Public License along with OmniDB. If not, see http://www.gnu.org/licenses/.
*/

var v_autocomplete_object;
var Range = ace.require('ace/range').Range;

/// <summary>
/// Startup function.
/// </summary>
$(function() {

  v_autocomplete_object = {
    active: false,
    ready: false,
    selected: null,
    //label: document.getElementById('div_autocomplete_label'),
    input: document.getElementById('div_autocomplete_input'),
    input2: document.getElementById('div_autocomplete_input2'),
    active_input: null,
    div: document.getElementById('div_autocomplete'),
    test_length: document.getElementById('div_test_length'),
    scroll: document.getElementById('div_autocomplete_scroll'),
    no_results: document.getElementById('div_autocomplete_noresults'),
    loading: document.getElementById('div_autocomplete_loading'),
    elements: [
      { 'type': 'keyword', 'container': document.getElementById('autocomplete_grid_keyword'), 'count_div': document.getElementById('autocomplete_count_keyword'), elements: [], 'num_visible': 0 },
      { 'type': 'database', 'container': document.getElementById('autocomplete_grid_database'), 'count_div': document.getElementById('autocomplete_count_database'), elements: [], 'num_visible': 0 },
      { 'type': 'role', 'container': document.getElementById('autocomplete_grid_role'), 'count_div': document.getElementById('autocomplete_count_role'), elements: [], 'num_visible': 0 },
      { 'type': 'tablespace', 'container': document.getElementById('autocomplete_grid_tablespace'), 'count_div': document.getElementById('autocomplete_count_tablespace'), elements: [], 'num_visible': 0 },
      { 'type': 'schema', 'container': document.getElementById('autocomplete_grid_schema'), 'count_div': document.getElementById('autocomplete_count_schema'), elements: [], 'num_visible': 0 },
      { 'type': 'extension', 'container': document.getElementById('autocomplete_grid_extension'), 'count_div': document.getElementById('autocomplete_count_extension'), elements: [], 'num_visible': 0 },
      { 'type': 'table', 'container': document.getElementById('autocomplete_grid_table'), 'count_div': document.getElementById('autocomplete_count_table'), elements: [], 'num_visible': 0 },
      { 'type': 'view', 'container': document.getElementById('autocomplete_grid_view'), 'count_div': document.getElementById('autocomplete_count_view'), elements: [], 'num_visible': 0 },
      { 'type': 'column', 'container': document.getElementById('autocomplete_grid_column'), 'count_div': document.getElementById('autocomplete_count_column'), elements: [], 'num_visible': 0 },
      { 'type': 'function', 'container': document.getElementById('autocomplete_grid_function'), 'count_div': document.getElementById('autocomplete_count_function'), elements: [], 'num_visible': 0 },
      { 'type': 'index', 'container': document.getElementById('autocomplete_grid_index'), 'count_div': document.getElementById('autocomplete_count_index'), elements: [], 'num_visible': 0 }
    ]
  };

  for (var i=0; i<v_autocomplete_object.elements.length; i++) {
    if (v_autocomplete_object.elements[i].type!='keyword') {
    var columnProperties = [];

    var col = new Object();
    col.title =  '';
    col.readOnly = true;
    columnProperties.push(col);

    var col = new Object();
    col.title =  '';
    col.readOnly = true;
    columnProperties.push(col);

    v_autocomplete_object.elements[i].grid = new Handsontable(v_autocomplete_object.elements[i].container,
                      {
                        licenseKey: 'non-commercial-and-evaluation',
                        data: [],
                        columns : columnProperties,
                        colHeaders : false,
                        manualColumnResize: true,
                        fillHandle:false,
                        disableVisualSelection: true,
                        stretchH: 'last',
                        afterRender: function () {

                            if (v_autocomplete_object.selected_grid==this) {
                              var v_cell = this.getCell(v_autocomplete_object.selected_grid_row,0);
                              if (v_cell!=null) {
                                this.getCell(v_autocomplete_object.selected_grid_row,0).parentNode.classList.add('div_autocomplete_data_row_selected');
                              }
                            }
                        },
                        cells: function (row, col, prop) {

                            var cellProperties = {};
                            cellProperties.renderer = whiteHtmlRenderer;
                            if (col==1)
                              cellProperties.renderer = whiteRightHtmlRenderer;
                            return cellProperties;
                        },
                        cell: [
                           {col: 0, className: "htRight"}
                         ]
                      });

      v_autocomplete_object.elements[i].container.onclick = (function(group) {
        return function (event) {
          event.preventDefault()
          event.stopPropagation()
          close_autocomplete(group.elements[group.grid.getSelected()[0][0]].select_value);
        }
      }(v_autocomplete_object.elements[i]));


    }
  }
});

function build_autocomplete_elements(p_data, p_value) {
  var v_previous_element = null;
  var v_next_element = null;
  var v_first_element = null;
  var v_last_element = null;
  v_autocomplete_object.selected = null;

  //hiding nodes
  for (var k=0; k<v_autocomplete_object.elements.length; k++) {
    v_autocomplete_object.elements[k].container.parentNode.style.display = 'none';
    if (v_autocomplete_object.elements[k].type=='keyword')
      v_autocomplete_object.elements[k].container.parentNode.scrollTop = 0;
    v_autocomplete_object.elements[k].elements = [];
  }

  var v_num_results = 0;
  for (var i=0; i<p_data.length; i++) {
    var v_local_group = p_data[i];
    var v_global_group;

    //looking for group and hiding nodes
    for (var k=0; k<v_autocomplete_object.elements.length; k++) {
      if (v_autocomplete_object.elements[k].type == v_local_group.type) {
        v_global_group = v_autocomplete_object.elements[k];
        break;
      }
    }

    v_global_group.container.parentNode.style.display = 'block';
    v_global_group.num_visible = v_local_group.elements.length;
    v_global_group.count_div.innerHTML = v_local_group.elements.length + ' results';

    var v_list = [];
    var v_list_render = [];
    for (var j=0; j<v_local_group.elements.length; j++) {
      v_num_results++;
      var v_element;

      var div = document.createElement('div');
      if (v_local_group.type=='keyword') {
        div.className = 'div_autocomplete_data_word';
        div.innerHTML = v_local_group.elements[j].value.replace(p_value,'<b>' + p_value + '</b>');
        var v_element = {'value': v_local_group.elements[j].value, 'select_value': v_local_group.elements[j].select_value,'complement': v_local_group.elements[j].complement, 'container': div, 'visible': true, 'group_reference': v_global_group };
        v_global_group.container.appendChild(div);

        div.onclick = (function(v_value) {
          return function (event) {
            event.preventDefault()
            event.stopPropagation()
            close_autocomplete(v_value);
          }
        }(v_element.select_value));
      }
      else {
        v_list.push([v_local_group.elements[j].value,v_local_group.elements[j].complement]);
        v_list_render.push([v_local_group.elements[j].value.replace(p_value,'<b>' + p_value + '</b>'),v_local_group.elements[j].complement]);
        var v_element = {'value': v_local_group.elements[j].value, 'select_value': v_local_group.elements[j].select_value,'complement': v_local_group.elements[j].complement, 'visible': true, 'index': j, 'visible_index': j, 'grid_reference': v_global_group.grid, 'group_reference': v_global_group };
      }

      if (v_first_element == null)
        v_first_element = v_element;
      if (i==p_data.length-1 && j==v_local_group.elements.length-1)
        v_last_element = v_element;

      v_global_group.elements.push(v_element);

      if (v_previous_element != null)
        v_previous_element.next = v_element;
        v_element.previous = v_previous_element;
      v_previous_element = v_element;
    }
    if (v_global_group.type!='keyword') {
      v_global_group.grid_data = v_list;
      v_global_group.grid.loadData(v_list_render);
    }
  }

  //adjusting first and last elements links
  if (v_first_element!=null) {
    v_autocomplete_object.first_element = v_first_element;
    v_first_element.previous = v_last_element;
  }
  if (v_last_element!=null) {
    v_autocomplete_object.last_element = v_last_element;
    v_last_element.next = v_first_element;
  }

  if (v_num_results>0) {
    v_autocomplete_object.no_results.style.display = 'none';
  }
  else {
    v_autocomplete_object.no_results.style.display = 'block';
  }

  //refreshing grids
  for (var k=0; k<v_autocomplete_object.elements.length; k++) {
    if (v_autocomplete_object.elements[k].type!='keyword') {
      v_autocomplete_object.elements[k].grid.render();
      v_autocomplete_object.elements[k].grid.selectCell(0,0);
      v_autocomplete_object.elements[k].grid.deselectCell();
    }
  }
  v_autocomplete_object.active_input.focus();
}

function renew_autocomplete(p_base, p_new_value) {
  var v_search_regex = null;

  if(p_new_value != '') {
    v_search_regex = new RegExp('^(' + p_base + ').*' + p_new_value.split('').join('.*'), 'i');
  }
  else {
    v_search_regex = new RegExp('^(' + p_base + ')', 'i');
  }

  autocomplete_deselect_element();
  var v_num_results = 0;
  for (var i=v_autocomplete_object.elements.length-1; i>=0; i--) {
    var v_group = v_autocomplete_object.elements[i];
    v_group.num_visible = 0;
    if (v_group.type=='keyword') {
      for (var j=v_group.elements.length-1; j>=0; j--) {
        var v_element = v_group.elements[j];
        //doesn't match, hide
        if(!v_search_regex.test(v_element.value)) {
          v_element.container.style.display = 'none';
          v_element.visible = false;
        }
        else {
          var v_match_text = v_search_regex.exec(v_element.value)[0];
          v_num_results++;
          v_element.container.style.display = 'inline-block';
          v_element.visible = true;
          v_element.container.innerHTML = v_element.value.replace(v_match_text,'<b>' + v_match_text + '</b>')
          v_group.num_visible++;
        }
      }
    }
    //grid type
    else {
      var v_new_data = []
      for (var j=0; j<v_group.elements.length; j++) {
        var v_element = v_group.elements[j];
        //doesn't match, hide
        if(!v_search_regex.test(v_element.value)) {
          v_element.visible = false;
        }
        else {
          var v_match_text = v_search_regex.exec(v_element.value)[0];
          v_num_results++;
          v_element.visible = true;
          v_element.visible_index = v_group.num_visible;
          v_new_data.push([v_group.grid_data[j][0].replace(v_match_text,'<b>' + v_match_text + '</b>'),v_group.grid_data[j][1]]);
          v_group.num_visible++;
        }
      }
      v_group.grid.loadData(v_new_data);
    }

    //no more elements, hide div and group
    v_group.count_div.innerHTML = v_group.num_visible + ' results';
    if (v_group.num_visible==0) {
      v_group.container.parentNode.style.display = 'none';
    }
    else {
      v_group.container.parentNode.style.display = 'block';
    }
  }

  if (v_num_results>0) {
    v_autocomplete_object.no_results.style.display = 'none';
  }
  else {
    v_autocomplete_object.no_results.style.display = 'block';
  }

  //refreshing grids
  for (var k=0; k<v_autocomplete_object.elements.length; k++) {
    if (v_autocomplete_object.elements[k].type!='keyword') {
      v_autocomplete_object.elements[k].grid.render();
      v_autocomplete_object.elements[k].grid.selectCell(0,0);
      v_autocomplete_object.elements[k].grid.deselectCell();
    }
  }
  v_autocomplete_object.active_input.focus();
}

function autocomplete_get_results(p_sql,p_value,p_pos) {
  v_autocomplete_object.div.style.width = '200px';
  execAjax('/get_autocomplete_results/',
      JSON.stringify({
          "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
          "p_tab_id": v_connTabControl.selectedTab.id,
          "p_sql": p_sql,
          "p_value": p_value,
          "p_pos": p_pos
      }),
      function(p_return) {
        v_autocomplete_object.test_length.innerHTML = p_return.v_data.max_result_word;
        var v_new_width_result = v_autocomplete_object.test_length.clientWidth;
        v_autocomplete_object.test_length.innerHTML = p_return.v_data.max_complement_word;
        var v_new_width_complement = v_autocomplete_object.test_length.clientWidth;
        if (v_autocomplete_object.mode==0)
          v_autocomplete_object.scroll.style['max-height'] = window.innerHeight - $(v_autocomplete_object.div).offset().top - 50 + 'px';
        else
          v_autocomplete_object.scroll.style['max-height'] = $(v_autocomplete_object.div).offset().top - 20 + 'px';
        var v_new_width = v_new_width_result + v_new_width_complement + 160;
        if (v_new_width<400)
          v_new_width = 400;

        v_autocomplete_object.div.style.width = v_new_width + 'px';

        //adjust grid columns widths
        for (var i=0; i<v_autocomplete_object.elements.length; i++) {
          if (v_autocomplete_object.elements[i].type!='keyword') {
            var v_columns = v_autocomplete_object.elements[i].grid.getSettings().columns
            v_columns[0].width = v_new_width_result + 30;
            v_autocomplete_object.elements[i].grid.updateSettings({ columns: v_columns});
          }
        }

        build_autocomplete_elements(p_return.v_data.data,p_value);
        v_autocomplete_object.ready = true;

      },
      function(p_return) {
        if (p_return.v_data.password_timeout) {
          showPasswordPrompt(
            v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            function() {
              autocomplete_get_results(p_sql,p_value,p_pos);
            },
            null,
            p_return.v_data.message
          );
        }
      },
      'box',
      true,
    true);

}

function autocomplete_keyup(p_event, p_element) {
  if (p_event.keyCode != 40 && p_event.keyCode != 38 && p_event.keyCode != 13 && p_event.keyCode != 16 && p_event.keyCode != 17 && p_event.keyCode != 18) {
    if (v_autocomplete_object.ready) {
      renew_autocomplete(v_autocomplete_object.search_base, p_element.value)
    }
  }
}

function autocomplete_keydown(p_event, p_element) {
  //esc
  if(p_event.keyCode === 27){
    p_event.stopPropagation();
    p_event.preventDefault();
    close_autocomplete();
  }
  //enter
  if(p_event.keyCode === 13){
    p_event.stopPropagation();
    p_event.preventDefault();
    //get remaining string to include in editor
    if (v_autocomplete_object.selected)
      //close_autocomplete(v_autocomplete_object.selected.value.substring(v_autocomplete_object.search_base.length));
      close_autocomplete(v_autocomplete_object.selected.select_value);
    else
      close_autocomplete();
  }
  // up or down arrow
  else if(p_event.keyCode === 40 || p_event.keyCode === 38){
    p_event.stopPropagation();
    p_event.preventDefault();
    var v_new_selected = null;
    //select first visible element if null
    if (v_autocomplete_object.selected==null) {
      if (p_event.keyCode === 40 && v_autocomplete_object.first_element!=null) {
        v_new_selected = find_next_visible_element(v_autocomplete_object.first_element);
      }
      else if (p_event.keyCode === 38 && v_autocomplete_object.last_element!=null) {
        v_new_selected = find_previous_visible_element(v_autocomplete_object.last_element);
      }
    }
    else {
      if (p_event.keyCode === 40)
        v_new_selected = find_next_visible_element(v_autocomplete_object.selected.next);
      else if (p_event.keyCode === 38)
        v_new_selected = find_previous_visible_element(v_autocomplete_object.selected.previous);
    }

    if (v_new_selected)
      autocomplete_select_element(v_new_selected);
  }
}

function find_next_visible_element(p_element) {
  //avoid infinite loop
  var v_element = p_element;
  var v_first = p_element;
  if (v_element.visible==true)
    return v_element;
  if (v_element.next==p_element)
    return null;
  while (v_element.next.visible==false) {
    v_element = v_element.next;
    //searched all, avoid infinite
    if (v_element == v_first)
      return null;
  }
  return v_element.next;
}

function find_previous_visible_element(p_element) {
  //avoid infinite loop
  var v_element = p_element;
  var v_first = p_element;
  if (v_element.visible==true)
    return v_element;
  if (v_element.previous==p_element)
    return null;
  while (v_element.previous.visible==false) {
    v_element = v_element.previous;
    //searched all, avoid infinite
    if (v_element == v_first)
      return null;
  }
  return v_element.previous;
}

function autocomplete_select_element(p_element) {
  autocomplete_deselect_element();

  var v_parent_block = p_element.group_reference.container.parentNode;
  if (v_parent_block.offsetTop<v_parent_block.parentNode.scrollTop)
    v_parent_block.parentNode.scrollTop = v_parent_block.offsetTop;
  else {
    var v_value = v_parent_block.offsetTop + 80-v_parent_block.parentNode.offsetHeight-v_parent_block.parentNode.scrollTop;
    if (v_value > 0) {
      v_parent_block.parentNode.scrollTop += v_value;
    }
  }


  //keyword element
  if (p_element.visible_index==null) {
    p_element.container.classList.add('div_autocomplete_data_row_selected');

    if (p_element.container.offsetTop<p_element.container.parentNode.scrollTop)
      p_element.container.parentNode.scrollTop = p_element.container.offsetTop;
    else {
      var v_value = p_element.container.offsetTop + 22-80-2-p_element.container.parentNode.scrollTop;
      if (v_value > 0) {
        p_element.container.parentNode.scrollTop += v_value;
      }
    }
  }
  //grid element
  else {
    p_element.grid_reference.selectCell(p_element.visible_index,0)
    p_element.grid_reference.deselectCell()
    v_autocomplete_object.active_input.focus();
    v_autocomplete_object.selected_grid = p_element.grid_reference;
    v_autocomplete_object.selected_grid_row = p_element.visible_index;

    update_selected_grid_row_position(p_element.grid_reference.getCell(p_element.visible_index,0));
  }

  v_autocomplete_object.selected = p_element;
}

function autocomplete_deselect_element() {
  //removing selection of old row
  if (v_autocomplete_object.selected) {
    var v_previous = v_autocomplete_object.selected
    if (v_previous.visible_index==null)
      v_previous.container.classList.remove('div_autocomplete_data_row_selected');
    else {
      var v_cell = v_previous.grid_reference.getCell(v_previous.visible_index,0);
      if (v_cell!=null) {
        v_previous.grid_reference.getCell(v_previous.visible_index,0).parentNode.classList.remove('div_autocomplete_data_row_selected');
      }
      v_autocomplete_object.selected_grid = null;
      v_autocomplete_object.selected_grid_row = null;
    }
  }
  v_autocomplete_object.selected = null;
}

function update_selected_grid_row_position(p_cell) {
  p_cell.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.scrollTop = p_cell.offsetTop + parseInt(p_cell.parentNode.parentNode.parentNode.parentNode.style.top,10);
  p_cell.parentNode.classList.add('div_autocomplete_data_row_selected');
}

function close_autocomplete(p_additional_text) {
  v_autocomplete_object.active = false;
  v_autocomplete_object.ready = false;
  v_autocomplete_object.selected_grid = null;
  v_autocomplete_object.selected_grid_row = null;
  //hiding nodes
  for (var k=0; k<v_autocomplete_object.elements.length; k++) {
    v_autocomplete_object.elements[k].container.parentNode.style.display = 'none';
    if (v_autocomplete_object.elements[k].type=='keyword')
      v_autocomplete_object.elements[k].container.innerHTML = '';
    v_autocomplete_object.elements[k].elements = [];
  }
  v_autocomplete_object.div.style.display = 'none';
  v_autocomplete_object.close_div.parentNode.removeChild(v_autocomplete_object.close_div);

  var v_editor = v_autocomplete_object.editor;
  if (p_additional_text) {
    v_editor.session.replace(v_autocomplete_object.range, p_additional_text);
  }
  v_editor.focus();
  v_autocomplete_object.no_results.style.display = 'none';
}

function autocomplete_start(editor, mode) {

  if (!v_autocomplete_object.active) {
    v_autocomplete_object.editor = editor;
    v_autocomplete_object.active = true;
    v_autocomplete_object.mode = mode;
    if (mode==0) {
      v_autocomplete_object.active_input = v_autocomplete_object.input;
      v_autocomplete_object.input.style.display = 'block';
      v_autocomplete_object.input2.style.display = 'none';
    }
    else {
      v_autocomplete_object.active_input = v_autocomplete_object.input2;
      v_autocomplete_object.input.style.display = 'none';
      v_autocomplete_object.input2.style.display = 'block';
    }


    var v_pixel_position = editor.renderer.$cursorLayer.getPixelPosition();
    var v_editor_position = editor.container.getBoundingClientRect();
    var v_pos = { 'left': v_editor_position.left + v_pixel_position.left, 'top': v_editor_position.top + v_pixel_position.top}

    var v_top_pos = v_pos.top - editor.renderer.scrollTop;


    var v_autocomplete_div = v_autocomplete_object.div;
    v_autocomplete_div.style.left = v_pos.left + editor.renderer.gutterWidth;

    if (mode==0) {
      v_autocomplete_div.style.top = v_top_pos - 4;
      v_autocomplete_div.style.bottom = 'unset';
    }
    else {
      v_autocomplete_div.style.top = 'unset';
      v_autocomplete_div.style.bottom = window.innerHeight - v_top_pos - 26;

    }
    v_autocomplete_div.style.display = 'block';

    var v_closediv = document.createElement('div');
    v_autocomplete_object.close_div = v_closediv;
    v_closediv.className = 'div_close_cm';
    v_closediv.onmousedown = function() {
      close_autocomplete();
    };
    document.body.appendChild(v_closediv);

    //get editor word before cursor
    var v_cursor = editor.selection.getCursor();
    var v_prefix_pos = editor.session.doc.positionToIndex(v_cursor)-1;
    var v_editor_text = editor.getValue();
    //v_editor_text = v_editor_text.substring(0,v_prefix_pos);
    var v_pos_iterator = v_prefix_pos;
    var v_word_length = 0;
    while (v_editor_text[v_pos_iterator]!= ' ' && v_editor_text[v_pos_iterator]!= '\n' && v_pos_iterator>=0) {
      v_pos_iterator--;
      v_word_length++;
    }

    if (v_pos_iterator>=0) {
      v_pos_iterator++;
      v_autocomplete_object.range = new Range(v_cursor.row, v_cursor.column-v_word_length, v_cursor.row, v_cursor.column);
      var v_last_word = v_editor_text.substring(v_pos_iterator,v_pos_iterator+v_word_length);
    }
    else {
      v_autocomplete_object.range = new Range(v_cursor.row, v_cursor.column-v_word_length-1, v_cursor.row, v_cursor.column);
      var v_last_word = v_editor_text.substring(v_pos_iterator,v_pos_iterator+v_word_length+1);
    }
    v_autocomplete_object.active_input.value = '';
    v_autocomplete_object.search_base = v_last_word;
    v_autocomplete_object.active_input.focus();
    autocomplete_get_results(editor.getValue(),v_last_word,editor.session.doc.positionToIndex(v_cursor));
  }
}
