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

var v_createOuterTerminalTabFunction = function(p_conn_id = -1, p_alias = 'Terminal') {

  // v_connTabControl.removeLastTab();

  let v_tooltip_name =
  '<h5 class="my-1">Terminal</h5>' +
  '<div class="mb-1">' + p_alias + '</div>';

  var v_tab = v_connTabControl.createTab({
    p_icon: '<i class="fas fa-terminal"></i>',
    p_name: p_alias,
    p_selectFunction: function() {
      if(this.tag != null) {
        refreshHeights();
      }
      if(this.tag != null && this.tag.editor_console != null) {
          this.tag.editor_console.focus();
      }
    },
    p_close: false,// Replacing default close icon with contextMenu.
    p_closeFunction: function(e,p_tab) {
      var v_this_tab = p_tab;
      v_this_tab.removeTab();
    },
    p_rightClickFunction: function(e) {
      terminalContextMenu(e,v_tab);
    },
    p_omnidb_tooltip_name: v_tooltip_name
  });

  v_connTabControl.selectTab(v_tab);

  var v_html =
  '<div class="container-fluid mt-2">' +
    '<div class="row">' +
      '<div class="col">' +
        '<div class="omnidb__txt-console p-2">' +
          '<div id="txt_console_' + v_tab.id + '" style="width: 100%; height: 120px;">' +
          '</div>' +
        '</div>' +
      '</div>' +
    '</div>' +
  '</div>';
  // var v_html = "<div id='txt_console_" + v_tab.id + "' class='omnidb__txt-console' style=' width: 100%; height: 120px;'></div>";

  var v_div = document.getElementById('div_' + v_tab.id);
  v_div.innerHTML = v_html;


  var term_div = document.getElementById('txt_console_' + v_tab.id);
  var term = new Terminal({
        fontSize: v_font_size,
        theme: v_current_terminal_theme,
        fontFamily: 'Monospace'
  });
  term.open(term_div);

  term.on('data', (key, ev) => {
          terminalKey(key);
  });

  Terminal.applyAddon(fit);

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'outer_terminal',
    editor_console: term,
    editorDivId: 'txt_console_' + v_tab.id,
    div_console: document.getElementById('txt_console_' + v_tab.id),
    context: null,
    tabControl: v_connTabControl,
    connTab: v_connTabControl.selectedTab,
    currDatabaseIndex: null,
    state: 0,
    terminalHistoryList: [],
    tempData: [],
    connId: p_conn_id
  };

  v_tab.tag = v_tag;

  // Creating `Add` tab in the outer tab list
  // v_connTabControl.createAddTab();

  $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips

  setTimeout(function() {
    refreshHeights();
    startTerminal(p_conn_id);
  },10);

};
