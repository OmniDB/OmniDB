var v_createOuterTerminalTabFunction = function(p_conn_id = -1, p_alias = 'Terminal') {

  v_connTabControl.removeLastTab();

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
      beforeCloseTab(e,
        function() {
          v_this_tab.removeTab();
        });
    },
    p_rightClickFunction: function(e) {
      terminalContextMenu(e);
    },
    p_tooltip_name: p_alias
  });

  v_connTabControl.selectTab(v_tab);

  var v_html = "<div id='txt_console_" + v_tab.id + "' style=' width: 100%; height: 120px;'></div>";

  var v_div = document.getElementById('div_' + v_tab.id);
  v_div.innerHTML = v_html;


  var term_div = document.getElementById('txt_console_' + v_tab.id);
  var term = new Terminal({
        fontSize: v_font_size,
        theme: v_current_terminal_theme
  });
  term.open(term_div);

  term.on('data', (key, ev) => {
          terminalKey(key);
  });

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

  // Creating + tab in the outer tab list
  v_connTabControl.createTab(
    {
      p_icon: '<i class="fas fa-plus"></i>',
      p_name: 'Add connection',
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        showMenuNewTabOuter(e);
      },
      p_tooltip_name: '<h5 class="my-1">Add/Select Connections</h5>'
    });

  $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips

  setTimeout(function() {
    refreshHeights();
    startTerminal(p_conn_id);
  },10);

};
