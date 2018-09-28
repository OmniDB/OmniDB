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
    selected: null,
    //label: document.getElementById('div_autocomplete_label'),
    input: document.getElementById('div_autocomplete_input'),
    div: document.getElementById('div_autocomplete'),
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
      { 'type': 'index', 'container': document.getElementById('autocomplete_grid_index'), 'count_div': document.getElementById('autocomplete_count_index'), elements: [], 'num_visible': 0 }
    ]
  };

  build_autocomplete_elements([]);


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
    v_autocomplete_object.elements[k].container.innerHTML = '';
    v_autocomplete_object.elements[k].container.parentNode.scrollTop = 0;
    v_autocomplete_object.elements[k].elements = [];
  }

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

    for (var j=0; j<v_local_group.elements.length; j++) {
      var div = document.createElement('div');
      var div_left = document.createElement('div');
      div_left.className = 'div_autocomplete_data_row_left';
      var div_right = document.createElement('div');
      div_right.className = 'div_autocomplete_data_row_right';
      div.appendChild(div_left);
      div.appendChild(div_right);
      var v_element = {'value': v_local_group.elements[j].value, 'select_value': v_local_group.elements[j].select_value, 'container': div,'container_left': div_left,'container_right': div_right, 'visible': true };

      div.onclick = (function(event,v_value) {
        return function () {
          event.preventDefault()
          event.stopPropagation()
          close_autocomplete(v_value);
        }
      }(event,v_element.select_value))

      if (v_first_element == null)
        v_first_element = v_element;
      if (i==p_data.length-1 && j==v_local_group.elements.length-1)
        v_last_element = v_element;

      v_global_group.elements.push(v_element);
      div_left.innerHTML = v_element.value.replace(p_value,'<b>' + p_value + '</b>');
      div_right.innerHTML = v_local_group.elements[j].complement;
      div.className = 'div_autocomplete_data_row';
      v_global_group.container.appendChild(div);

      if (v_previous_element != null)
        v_previous_element.next = v_element;
        v_element.previous = v_previous_element;
      v_previous_element = v_element;
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
}

function renew_autocomplete(p_new_value) {
  for (var i=v_autocomplete_object.elements.length-1; i>=0; i--) {
    var v_group = v_autocomplete_object.elements[i];
    v_group.num_visible = 0;
    for (var j=v_group.elements.length-1; j>=0; j--) {
      var v_element = v_group.elements[j];
      //doesn't match, hide
      if (!v_element.value.toLowerCase().includes(p_new_value.toLowerCase())) {
        v_element.container.style.display = 'none';
        v_element.visible = false;
      }
      else {
        v_element.container.style.display = 'block';
        v_element.visible = true;
        v_element.container_left.innerHTML = v_element.value.replace(p_new_value,'<b>' + p_new_value + '</b>')
        v_group.num_visible++;
      }
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
}

function autocomplete_get_results(p_value) {
  execAjax('/get_autocomplete_results/',
      JSON.stringify({
          "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
          "p_tab_id": v_connTabControl.selectedTab.id,
          "p_value": p_value
      }),
      function(p_return) {
        build_autocomplete_elements(p_return.v_data,p_value);

      },
      function(p_return) {
        if (p_return.v_data.password_timeout) {
          showPasswordPrompt(
            v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
            function() {
              autocomplete_get_results(p_value);
            },
            null,
            p_return.v_data.message
          );
        }
      },
      'box',
      true);

}

function autocomplete_keyup(p_event, p_element) {
  if (p_event.keyCode != 40 && p_event.keyCode != 38 && p_event.keyCode != 13) {
    renew_autocomplete(v_autocomplete_object.search_base + p_element.value)
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
  if (v_autocomplete_object.selected) {
    v_autocomplete_object.selected.container.className = 'div_autocomplete_data_row';
  }

  p_element.container.className = 'div_autocomplete_data_row_selected';
  if (p_element.container.offsetTop<p_element.container.parentNode.scrollTop)
    p_element.container.parentNode.scrollTop = p_element.container.offsetTop;
  else {
    var v_value = p_element.container.offsetTop + 22-80-2-p_element.container.parentNode.scrollTop;
    if (v_value > 0) {
      p_element.container.parentNode.scrollTop += v_value;
    }
  }
  v_autocomplete_object.selected = p_element;
}

function close_autocomplete(p_additional_text) {
  //hiding nodes
  for (var k=0; k<v_autocomplete_object.elements.length; k++) {
    v_autocomplete_object.elements[k].container.parentNode.style.display = 'none';
    v_autocomplete_object.elements[k].container.innerHTML = '';
    v_autocomplete_object.elements[k].elements = [];
  }
  v_autocomplete_object.div.style.display = 'none';
  v_autocomplete_object.close_div.parentNode.removeChild(v_autocomplete_object.close_div);
  //editor.focus();

  var v_editor = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor;
  if (p_additional_text) {
    v_editor.session.replace(v_autocomplete_object.range, p_additional_text);
  }
  v_editor.focus();

}

function autocomplete_start(editor) {

  var v_pixel_position = editor.renderer.$cursorLayer.getPixelPosition();
  var v_editor_position = editor.container.getBoundingClientRect();
  var v_pos = { 'left': v_editor_position.left + v_pixel_position.left, 'top': v_editor_position.top + v_pixel_position.top}
  var v_autocomplete_div = v_autocomplete_object.div;
  v_autocomplete_div.style.left = v_pos.left + 50;
  v_autocomplete_div.style.top = v_pos.top - 2 - editor.renderer.scrollTop;
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
  while (v_editor_text[v_pos_iterator]!= ' ' && v_editor_text[v_pos_iterator]!= '\n' && v_pos_iterator>0) {
    v_pos_iterator--;
    v_word_length++;
  }
  if (v_pos_iterator!=0)
    v_pos_iterator++;
  if (v_pos_iterator!=0) {
    v_autocomplete_object.range = new Range(v_cursor.row, v_cursor.column-v_word_length, v_cursor.row, v_cursor.column);
    var v_last_word = v_editor_text.substring(v_pos_iterator,v_pos_iterator+v_word_length);
  }
  else {
    v_autocomplete_object.range = new Range(v_cursor.row, v_cursor.column-v_word_length-1, v_cursor.row, v_cursor.column);
    var v_last_word = v_editor_text.substring(v_pos_iterator,v_pos_iterator+v_word_length+1);
  }
  v_autocomplete_object.input.value = '';
  v_autocomplete_object.search_base = v_last_word;
  v_autocomplete_object.input.focus();
  autocomplete_get_results(v_last_word);

}
