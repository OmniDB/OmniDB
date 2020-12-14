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

var v_autocomplete_object;
var Range = ace.require('ace/range').Range;

var v_keywords = [
        'ABORT',
        'ABS',
        'ABSOLUTE',
        'ACCESS',
        'ACTION',
        'ADA',
        'ADD',
        'ADMIN',
        'AFTER',
        'AGGREGATE',
        'ALIAS',
        'ALL',
        'ALLOCATE',
        'ALTER',
        'ANALYSE',
        'ANALYZE',
        'AND',
        'ANY',
        'ARE',
        'ARRAY',
        'AS',
        'ASC',
        'ASENSITIVE',
        'ASSERTION',
        'ASSIGNMENT',
        'ASYMMETRIC',
        'AT',
        'ATOMIC',
        'AUTHORIZATION',
        'AVG',
        'BACKWARD',
        'BEFORE',
        'BEGIN',
        'BETWEEN',
        'BIGINT',
        'BINARY',
        'BIT',
        'BITVAR',
        'BIT_LENGTH',
        'BLOB',
        'BOOLEAN',
        'BOTH',
        'BREADTH',
        'BY',
        'C',
        'CACHE',
        'CALL',
        'CALLED',
        'CARDINALITY',
        'CASCADE',
        'CASCADED',
        'CASE',
        'CAST',
        'CATALOG',
        'CATALOG_NAME',
        'CHAIN',
        'CHAR',
        'CHARACTER',
        'CHARACTERISTICS',
        'CHARACTER_LENGTH',
        'CHARACTER_SET_CATALOG',
        'CHARACTER_SET_NAME',
        'CHARACTER_SET_SCHEMA',
        'CHAR_LENGTH',
        'CHECK',
        'CHECKED',
        'CHECKPOINT',
        'CLASS',
        'CLASS_ORIGIN',
        'CLOB',
        'CLOSE',
        'CLUSTER',
        'COALESCE',
        'COBOL',
        'COLLATE',
        'COLLATION',
        'COLLATION_CATALOG',
        'COLLATION_NAME',
        'COLLATION_SCHEMA',
        'COLUMN',
        'COLUMN_NAME',
        'COMMAND_FUNCTION',
        'COMMAND_FUNCTION_CODE',
        'COMMENT',
        'COMMIT',
        'COMMITTED',
        'COMPLETION',
        'CONDITION_NUMBER',
        'CONNECT',
        'CONNECTION',
        'CONNECTION_NAME',
        'CONSTRAINT',
        'CONSTRAINTS',
        'CONSTRAINT_CATALOG',
        'CONSTRAINT_NAME',
        'CONSTRAINT_SCHEMA',
        'CONSTRUCTOR',
        'CONTAINS',
        'CONTINUE',
        'CONVERSION',
        'CONVERT',
        'COPY',
        'CORRESPONDING',
        'COUNT',
        'CREATE',
        'CREATEDB',
        'CREATEUSER',
        'CROSS',
        'CUBE',
        'CURRENT',
        'CURRENT_DATE',
        'CURRENT_PATH',
        'CURRENT_ROLE',
        'CURRENT_TIME',
        'CURRENT_TIMESTAMP',
        'CURRENT_USER',
        'CURSOR',
        'CURSOR_NAME',
        'CYCLE',
        'DATA',
        'DATABASE',
        'DATE',
        'DATETIME_INTERVAL_CODE',
        'DATETIME_INTERVAL_PRECISION',
        'DAY',
        'DEALLOCATE',
        'DEC',
        'DECIMAL',
        'DECLARE',
        'DEFAULT',
        'DEFERRABLE',
        'DEFERRED',
        'DEFINED',
        'DEFINER',
        'DELETE',
        'DELIMITER',
        'DELIMITERS',
        'DEPTH',
        'DEREF',
        'DESC',
        'DESCRIBE',
        'DESCRIPTOR',
        'DESTROY',
        'DESTRUCTOR',
        'DETERMINISTIC',
        'DIAGNOSTICS',
        'DICTIONARY',
        'DISCONNECT',
        'DISPATCH',
        'DISTINCT',
        'DO',
        'DOMAIN',
        'DOUBLE',
        'DROP',
        'DYNAMIC',
        'DYNAMIC_FUNCTION',
        'DYNAMIC_FUNCTION_CODE',
        'EACH',
        'ELSE',
        'ENCODING',
        'ENCRYPTED',
        'END',
        'END-EXEC',
        'EQUALS',
        'ESCAPE',
        'EVERY',
        'EXCEPT',
        'EXCEPTION',
        'EXCLUSIVE',
        'EXEC',
        'EXECUTE',
        'EXISTING',
        'EXISTS',
        'EXPLAIN',
        'EXTERNAL',
        'EXTRACT',
        'FALSE',
        'FETCH',
        'FINAL',
        'FIRST',
        'FLOAT',
        'FOR',
        'FORCE',
        'FOREIGN',
        'FORTRAN',
        'FORWARD',
        'FOUND',
        'FREE',
        'FREEZE',
        'FROM',
        'FULL',
        'FUNCTION',
        'G',
        'GENERAL',
        'GENERATED',
        'GET',
        'GLOBAL',
        'GO',
        'GOTO',
        'GRANT',
        'GRANTED',
        'GROUP',
        'GROUPING',
        'HANDLER',
        'HAVING',
        'HIERARCHY',
        'HOLD',
        'HOST',
        'HOUR',
        'IDENTITY',
        'IGNORE',
        'ILIKE',
        'IMMEDIATE',
        'IMMUTABLE',
        'IMPLEMENTATION',
        'IMPLICIT',
        'IN',
        'INCREMENT',
        'INDEX',
        'INDICATOR',
        'INFIX',
        'INHERITS',
        'INITIALIZE',
        'INITIALLY',
        'INNER',
        'INOUT',
        'INPUT',
        'INSENSITIVE',
        'INSERT',
        'INSTANCE',
        'INSTANTIABLE',
        'INSTEAD',
        'INT',
        'INTEGER',
        'INTERSECT',
        'INTERVAL',
        'INTO',
        'INVOKER',
        'IS',
        'ISNULL',
        'ISOLATION',
        'ITERATE',
        'JOIN',
        'K',
        'KEY',
        'KEY_MEMBER',
        'KEY_TYPE',
        'LANCOMPILER',
        'LANGUAGE',
        'LARGE',
        'LAST',
        'LATERAL',
        'LEADING',
        'LEFT',
        'LENGTH',
        'LESS',
        'LEVEL',
        'LIKE',
        'LIMIT',
        'LISTEN',
        'LOAD',
        'LOCAL',
        'LOCALTIME',
        'LOCALTIMESTAMP',
        'LOCATION',
        'LOCATOR',
        'LOCK',
        'LOWER',
        'M',
        'MAP',
        'MATCH',
        'MAX',
        'MAXVALUE',
        'MESSAGE_LENGTH',
        'MESSAGE_OCTET_LENGTH',
        'MESSAGE_TEXT',
        'METHOD',
        'MIN',
        'MINUTE',
        'MINVALUE',
        'MOD',
        'MODE',
        'MODIFIES',
        'MODIFY',
        'MODULE',
        'MONTH',
        'MORE',
        'MOVE',
        'MUMPS',
        'NAME',
        'NAMES',
        'NATIONAL',
        'NATURAL',
        'NCHAR',
        'NCLOB',
        'NEW',
        'NEXT',
        'NO',
        'NOCREATEDB',
        'NOCREATEUSER',
        'NONE',
        'NOT',
        'NOTHING',
        'NOTIFY',
        'NOTNULL',
        'NULL',
        'NULLABLE',
        'NULLIF',
        'NUMBER',
        'NUMERIC',
        'OBJECT',
        'OCTET_LENGTH',
        'OF',
        'OFF',
        'OFFSET',
        'OIDS',
        'OLD',
        'ON',
        'ONLY',
        'OPEN',
        'OPERATION',
        'OPERATOR',
        'OPTION',
        'OPTIONS',
        'OR',
        'ORDER',
        'ORDINALITY',
        'OUT',
        'OUTER',
        'OUTPUT',
        'OVERLAPS',
        'OVERLAY',
        'OVERRIDING',
        'OWNER',
        'PAD',
        'PARAMETER',
        'PARAMETERS',
        'PARAMETER_MODE',
        'PARAMETER_NAME',
        'PARAMETER_ORDINAL_POSITION',
        'PARAMETER_SPECIFIC_CATALOG',
        'PARAMETER_SPECIFIC_NAME',
        'PARAMETER_SPECIFIC_SCHEMA',
        'PARTIAL',
        'PASCAL',
        'PASSWORD',
        'PATH',
        'PENDANT',
        'PLACING',
        'PLI',
        'POSITION',
        'POSTFIX',
        'PRECISION',
        'PREFIX',
        'PREORDER',
        'PREPARE',
        'PRESERVE',
        'PRIMARY',
        'PRIOR',
        'PRIVILEGES',
        'PROCEDURAL',
        'PROCEDURE',
        'READ',
        'READS',
        'REAL',
        'RECHECK',
        'RECURSIVE',
        'REF',
        'REFERENCES',
        'REFERENCING',
        'REINDEX',
        'RELATIVE',
        'RENAME',
        'REPEATABLE',
        'REPLACE',
        'RESET',
        'RESTRICT',
        'RESULT',
        'RETURN',
        'RETURNED_LENGTH',
        'RETURNED_OCTET_LENGTH',
        'RETURNED_SQLSTATE',
        'RETURNS',
        'REVOKE',
        'RIGHT',
        'ROLE',
        'ROLLBACK',
        'ROLLUP',
        'ROUTINE',
        'ROUTINE_CATALOG',
        'ROUTINE_NAME',
        'ROUTINE_SCHEMA',
        'ROW',
        'ROWS',
        'ROW_COUNT',
        'RULE',
        'SAVEPOINT',
        'SCALE',
        'SCHEMA',
        'SCHEMA_NAME',
        'SCOPE',
        'SCROLL',
        'SEARCH',
        'SECOND',
        'SECTION',
        'SECURITY',
        'SELECT',
        'SELF',
        'SENSITIVE',
        'SEQUENCE',
        'SERIALIZABLE',
        'SERVER_NAME',
        'SESSION',
        'SESSION_USER',
        'SET',
        'SETOF',
        'SETS',
        'SHARE',
        'SHOW',
        'SIMILAR',
        'SIMPLE',
        'SIZE',
        'SMALLINT',
        'SOME',
        'SOURCE',
        'SPACE',
        'SPECIFIC',
        'SPECIFICTYPE',
        'SPECIFIC_NAME',
        'SQL',
        'SQLCODE',
        'SQLERROR',
        'SQLEXCEPTION',
        'SQLSTATE',
        'SQLWARNING',
        'STABLE',
        'START',
        'STATE',
        'STATEMENT',
        'STATIC',
        'STATISTICS',
        'STDIN',
        'STDOUT',
        'STORAGE',
        'STRICT',
        'STRUCTURE',
        'STYLE',
        'SUBCLASS_ORIGIN',
        'SUBLIST',
        'SUBSTRING',
        'SUM',
        'SYMMETRIC',
        'SYSID',
        'SYSTEM',
        'SYSTEM_USER',
        'TABLE',
        'TABLE_NAME',
        'TEMP',
        'TEMPLATE',
        'TEMPORARY',
        'TERMINATE',
        'THAN',
        'THEN',
        'TIME',
        'TIMESTAMP',
        'TIMEZONE_HOUR',
        'TIMEZONE_MINUTE',
        'TO',
        'TOAST',
        'TRAILING',
        'TRANSACTION',
        'TRANSACTIONS_COMMITTED',
        'TRANSACTIONS_ROLLED_BACK',
        'TRANSACTION_ACTIVE',
        'TRANSFORM',
        'TRANSFORMS',
        'TRANSLATE',
        'TRANSLATION',
        'TREAT',
        'TRIGGER',
        'TRIGGER_CATALOG',
        'TRIGGER_NAME',
        'TRIGGER_SCHEMA',
        'TRIM',
        'TRUE',
        'TRUNCATE',
        'TRUSTED',
        'TYPE',
        'UNCOMMITTED',
        'UNDER',
        'UNENCRYPTED',
        'UNION',
        'UNIQUE',
        'UNKNOWN',
        'UNLISTEN',
        'UNNAMED',
        'UNNEST',
        'UNTIL',
        'UPDATE',
        'UPPER',
        'USAGE',
        'USER',
        'USER_DEFINED_TYPE_CATALOG',
        'USER_DEFINED_TYPE_NAME',
        'USER_DEFINED_TYPE_SCHEMA',
        'USING',
        'VACUUM',
        'VALID',
        'VALIDATOR',
        'VALUE',
        'VALUES',
        'VARCHAR',
        'VARIABLE',
        'VARYING',
        'VERBOSE',
        'VERSION',
        'VIEW',
        'VOLATILE',
        'WHEN',
        'WHENEVER',
        'WHERE',
        'WITH',
        'WITHOUT',
        'WORK',
        'WRITE',
        'YEAR',
        'ZONE',
    ]

/// <summary>
/// Startup function.
/// </summary>
$(function() {

  v_autocomplete_object = {
    active: false,
    ready: false,
    selected: null,
    alt_shift_meta_pressed: false,
    //label: document.getElementById('div_autocomplete_label'),
    active_input: null,
    div: document.getElementById('div_autocomplete'),
    test_length: document.getElementById('div_test_length'),
    scroll: document.getElementById('div_autocomplete_scroll'),
    no_results: document.getElementById('div_autocomplete_noresults'),
    searching: document.getElementById('div_autocomplete_searching'),
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
                                this.getCell(v_autocomplete_object.selected_grid_row,0).parentNode.classList.add('omnidb__autocomplete__data-row--selected');
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
    if (v_autocomplete_object.elements[k].type=='keyword') {
      v_autocomplete_object.elements[k].container.parentNode.scrollTop = 0;
      v_autocomplete_object.elements[k].container.innerHTML = '';
    }
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
        div.className = 'omnidb__autocomplete__data-word';
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
  v_autocomplete_object.editor.focus();
}

function renew_autocomplete(p_new_value) {
  var v_search_regex = null;

  v_search_regex = new RegExp('^(' + p_new_value + ')', 'i');

  //v_search_regex = new RegExp('^' + p_new_value.split('').join('.*'), 'i');

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

  var v_new_selected = null;

  //select first visible element if null
  if (v_autocomplete_object.selected==null) {
    v_new_selected = find_next_visible_element(v_autocomplete_object.first_element);
  }
  else {
    v_new_selected = find_element_by_value(v_autocomplete_object.first_element,v_autocomplete_object.selected.value);

    // Currently selected doesn`t exist anymore, get the first
    if (v_new_selected==null) {
      v_new_selected = find_next_visible_element(v_autocomplete_object.first_element);
    }
  }

  autocomplete_deselect_element();

  if (v_new_selected) {
    autocomplete_select_element(v_new_selected);
  }

  v_autocomplete_object.editor.focus();
}

function autocomplete_get_results(p_sql,p_value,p_pos) {
  v_autocomplete_object.div.style.width = '500px';

  var v_data = [
    {
      "type": "keyword",
      "elements": [

      ]
    }
  ]

  for (var i=0; i<v_keywords.length; i++) {
    v_data[0].elements.push(
      {
        "value" : v_keywords[i],
        "select_value": v_keywords[i]
      }
    )
  }

  build_autocomplete_elements(v_data,p_value);

  renew_autocomplete(p_value);
  v_autocomplete_object.ready = true;

  v_autocomplete_object.searching.style.display = 'block';

  execAjax('/get_autocomplete_results/',
      JSON.stringify({
          "p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
          "p_tab_id": v_connTabControl.selectedTab.id,
          "p_sql": p_sql,
          "p_value": p_value,
          "p_pos": p_pos
      }),
      function(p_return) {

        v_autocomplete_object.searching.style.display = 'none';

        // Check that the autocomplete is still active
        if (v_autocomplete_object.active) {

          v_autocomplete_object.test_length.innerHTML = p_return.v_data.max_result_word;
          var v_new_width_result = v_autocomplete_object.test_length.clientWidth;
          v_autocomplete_object.test_length.innerHTML = p_return.v_data.max_complement_word;
          var v_new_width_complement = v_autocomplete_object.test_length.clientWidth;
          if (v_autocomplete_object.mode==0)
            v_autocomplete_object.scroll.style['max-height'] = window.innerHeight - $(v_autocomplete_object.div).offset().top - 50 + 'px';
          else
            v_autocomplete_object.scroll.style['max-height'] = $(v_autocomplete_object.div).offset().top - 20 + 'px';
          var v_new_width = v_new_width_result + v_new_width_complement + 160;
          if (v_new_width<500)
            v_new_width = 500;

          v_autocomplete_object.div.style.width = v_new_width + 'px';

          //adjust grid columns widths
          for (var i=0; i<v_autocomplete_object.elements.length; i++) {
            if (v_autocomplete_object.elements[i].type!='keyword') {
              var v_columns = v_autocomplete_object.elements[i].grid.getSettings().columns
              v_columns[0].width = v_new_width_result + 30;
              v_autocomplete_object.elements[i].grid.updateSettings({ columns: v_columns});
            }
          }

          var v_selected_value = null;
          if (v_autocomplete_object.selected!=null) {
            v_selected_value = v_autocomplete_object.selected.value;
          }

          v_data = v_data.concat(p_return.v_data.data);


          build_autocomplete_elements(v_data,p_value);

          if (v_selected_value!=null) {
            var v_new_selected = find_element_by_value(v_autocomplete_object.first_element,v_selected_value);
            setTimeout(function() {
                autocomplete_select_element(v_new_selected);
            },100);
          }

          renew_autocomplete(get_editor_last_word(v_autocomplete_object.editor).last_word);
          v_autocomplete_object.ready = true;

        }

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
      false,
    true);

}

function autocomplete_keyup(p_event) {
  if (p_event.keyCode != 27 && p_event.keyCode != 40 && p_event.keyCode != 38 && p_event.keyCode != 13 && p_event.keyCode != 16 && p_event.keyCode != 17 && p_event.keyCode != 18) {
    if (v_autocomplete_object.ready) {

      var v_last_word = get_editor_last_word(v_autocomplete_object.editor).last_word;

      if (v_last_word.length < v_autocomplete_object.search_base.length)
        close_autocomplete();
      else
        renew_autocomplete(v_last_word);
    }
  }
}

function autocomplete_keydown(p_editor, p_event) {

  if (event.ctrlKey==true ||
  event.altKey==true ||
  event.metaKey==true ) {
    v_autocomplete_object.alt_shift_meta_pressed = true;
  }
  else {
    v_autocomplete_object.alt_shift_meta_pressed = false;
  }

  if (v_autocomplete_object.active) {

    //esc
    if(p_event.keyCode === 27){
      p_event.stopPropagation();
      p_event.preventDefault();
      close_autocomplete();
    }
    //space
    if(p_event.keyCode === 32){
      close_autocomplete();
    }
    //enter or tab
    if(p_event.keyCode === 13 || p_event.keyCode === 9){
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

      if (v_new_selected) {
        autocomplete_select_element(v_new_selected);
      }
    }
  }
  else {
    autocomplete_update_editor_cursor(p_editor, p_event);
  }
}

function autocomplete_update_editor_cursor(p_editor, p_event) {
  // Handle UP or DOWN if autocomplete is not enbled, just move cursor position
  if (!p_event.shiftKey && !p_event.altKey && !p_event.ctrlKey && !p_event.metaKey) {
    if(p_event.keyCode === 40 || p_event.keyCode === 38){
      var v_cursor_pos = p_editor.getCursorPosition();

      //p_editor.moveCursorTo(p_editor.getCursorPosition().row+1,p_editor.getCursorPosition().column);
      let v_target_row;
      if(p_event.keyCode === 40) {
        v_target_row = v_cursor_pos.row+1;
      }
      else {
        v_target_row = v_cursor_pos.row-1;
      }
      p_editor.moveCursorTo(v_target_row,v_cursor_pos.column);
      p_editor.clearSelection();
      p_editor.renderer.scrollCursorIntoView({row:v_target_row});
    }
    // Handle TAB if autocomplete is not enbled
    if(p_event.keyCode === 9){
      var v_cursor_range = p_editor.getSelectionRange();
      p_editor.indent();
      p_editor.focus();
    }
  }
  // Enter
  if (p_event.keyCode === 13) {
    if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.mode=='console') {
      consoleSQL();
    }
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

function find_element_by_value(p_first_element, p_value) {
  //avoid infinite loop
  var v_element = p_first_element;
  var v_first = p_first_element;
  if (v_element.visible==true && v_element.value == p_value)
    return v_element;
  if (v_element.next==v_element)
    return null;
  while (v_element.next.visible==false || v_element.value != p_value) {
    v_element = v_element.next;
    //searched all, avoid infinite
    if (v_element == v_first)
      return null;
  }
  return v_element;
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
    p_element.container.classList.add('omnidb__autocomplete__data-row--selected');

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
    v_autocomplete_object.selected_grid = p_element.grid_reference;
    v_autocomplete_object.selected_grid_row = p_element.visible_index;

    update_selected_grid_row_position(p_element.grid_reference.getCell(p_element.visible_index,0));
    v_autocomplete_object.editor.focus();
  }

  v_autocomplete_object.selected = p_element;
}

function autocomplete_deselect_element() {
  //removing selection of old row
  if (v_autocomplete_object.selected) {
    var v_previous = v_autocomplete_object.selected
    if (v_previous.visible_index==null)
      v_previous.container.classList.remove('omnidb__autocomplete__data-row--selected');
    else {
      var v_cell = v_previous.grid_reference.getCell(v_previous.visible_index,0);
      if (v_cell!=null) {
        v_previous.grid_reference.getCell(v_previous.visible_index,0).parentNode.classList.remove('omnidb__autocomplete__data-row--selected');
      }
      v_autocomplete_object.selected_grid = null;
      v_autocomplete_object.selected_grid_row = null;
    }
  }
  v_autocomplete_object.selected = null;
}

function update_selected_grid_row_position(p_cell) {
  p_cell.parentNode.parentNode.parentNode.parentNode.parentNode.parentNode.scrollTop = p_cell.offsetTop + parseInt(p_cell.parentNode.parentNode.parentNode.parentNode.style.top,10);
  p_cell.parentNode.classList.add('omnidb__autocomplete__data-row--selected');
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

function autocomplete_start(editor, mode, event, force = null) {

  // Autocomplete doesn't start nor filters with the following keys:
  // 32 = SPACE
  // 27 = ESC
  // 13 = ENTER
  // 39 = RIGHT
  // 37 = LEFT
  // 40 = DOWN
  // 38 = UP

  // 16 = SHIFT
  // 17 = CTRL
  // 18 = ALT
  // 91 = META
  if ((event.keyCode != 32 &&
      event.keyCode != 27 &&
      event.keyCode != 39 &&
      event.keyCode != 37 &&
      event.keyCode != 40 &&
      event.keyCode != 38 &&
      event.keyCode != 13 &&
      event.keyCode != 16 &&
      event.keyCode != 17 &&
      event.keyCode != 18 &&
      event.keyCode != 91
    ) || force) {

    if (!v_autocomplete_object.active) {

      // autocomplete starts only with characters from A to Z or NUMBERS or dot or dash
      if ((
          (
            (event.keyCode >= 65 && event.keyCode < 90) ||
             event.keyCode == 189 ||
             (event.keyCode >= 48 && event.keyCode < 57 && event.shiftKey!=true) ||
             event.keyCode == 190
           ) &&
           !v_autocomplete_object.alt_shift_meta_pressed
         ) || force) {

        //get editor word before cursor
        var v_last_word_object = get_editor_last_word(editor);
        var v_last_word = v_last_word_object.last_word;
        var v_character_position = v_last_word_object.character_position;

        if (v_last_word != '' && v_last_word[0]!="'" && (v_last_word.length>2 || (v_last_word.length==2 && v_last_word[1]=='.') || force)) {

          v_autocomplete_object.editor = editor;
          v_autocomplete_object.active = true;
          v_autocomplete_object.mode = mode;


          var v_pixel_position = editor.renderer.$cursorLayer.getPixelPosition();
          var v_editor_position = editor.container.getBoundingClientRect();
          var v_pos = { 'left': v_editor_position.left + v_pixel_position.left, 'top': v_editor_position.top + v_pixel_position.top + 25}

          var v_top_pos = v_pos.top - editor.renderer.scrollTop;


          var v_autocomplete_div = v_autocomplete_object.div;
          v_autocomplete_div.style.left = v_pos.left + editor.renderer.gutterWidth + 'px';

          if (mode==0) {
            v_autocomplete_div.style.top = v_top_pos - 4 + 'px';
            v_autocomplete_div.style.bottom = 'unset';
          }
          else {
            v_autocomplete_div.style.top = 'unset';
            v_autocomplete_div.style.bottom = window.innerHeight - v_top_pos + 30 + 'px';

          }
          v_autocomplete_div.style.display = 'block';

          var v_closediv = document.createElement('div');
          v_autocomplete_object.close_div = v_closediv;
          v_closediv.className = 'div_close_cm';
          v_closediv.onmousedown = function() {
            close_autocomplete();
          };
          document.body.appendChild(v_closediv);

          v_autocomplete_object.search_base = v_last_word;

          autocomplete_get_results(editor.getValue(),v_last_word,v_character_position);

        }
      }
    }
    else {
      autocomplete_keyup(event);
    }

  }
}

function get_editor_last_word(p_editor) {
  var v_cursor = p_editor.selection.getCursor();
  var v_character_position = p_editor.session.doc.positionToIndex(v_cursor)
  var v_prefix_pos = p_editor.session.doc.positionToIndex(v_cursor)-1;
  var v_editor_text = p_editor.getValue();
  //v_editor_text = v_editor_text.substring(0,v_prefix_pos);
  var v_pos_iterator = v_prefix_pos;
  var v_word_length = 0;

  while (v_editor_text[v_pos_iterator]!= ' ' &&
         v_editor_text[v_pos_iterator]!= '\n' &&
         v_editor_text[v_pos_iterator]!= "'" &&
         v_editor_text[v_pos_iterator]!= '(' &&
         v_editor_text[v_pos_iterator]!= ')' &&
         v_editor_text[v_pos_iterator]!= ',' &&
         v_pos_iterator>=0
       ) {
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

  return {
    'last_word': v_last_word,
    'character_position': v_character_position
  }
}
