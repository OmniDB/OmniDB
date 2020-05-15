var v_createQueryTabFunction = function(p_table, p_tab_db_id) {

  var v_name = 'Query';
  if (p_table)
    v_name = p_table;

  // Removing last tab of the inner tab list
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  // Creating console tab in the inner tab list
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_name: '<span id="tab_title">' + v_name + '</span><span id="tab_stub"><img style="width: 24px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i>',
    p_selectFunction: function() {
      if(this.tag != null) {
        refreshHeights();
      }
      if(this.tag != null && this.tag.editor != null) {
          this.tag.editor.focus();
          checkQueryStatus(this);
      }
    },
    p_closeFunction: function(e,p_tab) {
      var v_current_tab = p_tab;
      beforeCloseTab(e,
        function() {
          removeTab(v_current_tab);
        });
    },
    p_dblClickFunction: renameTab
  });

  // Selecting newly created tab
  v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

  // Adding unique names to spans
  var v_tab_title_span = document.getElementById('tab_title');
  v_tab_title_span.id = 'tab_title_' + v_tab.id;
  var v_tab_loading_span = document.getElementById('tab_loading');
  v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
  var v_tab_check_span = document.getElementById('tab_check');
  v_tab_check_span.id = 'tab_check_' + v_tab.id;
  var v_tab_stub_span = document.getElementById('tab_stub');
  v_tab_stub_span.id = 'tab_stub_' + v_tab.id;

  var command_history_modal =
  "<div class='modal fade' id='modal_command_history_" + v_tab.id + "' tabindex='-1' role='dialog' aria-hidden='true'>" +
    "<div class='modal-dialog modal-xl modal-dialog-scrollable' role='document'>" +
      "<div class='modal-content'>" +
        "<div class='modal-header'>" +
          "<h5 class='modal-title'>" +
            "Command history" +
          "</h5>" +
          "<button type='button' class='close' data-dismiss='modal' aria-label='Close' onclick='closeCommandHistory()'>" +
            "<span aria-hidden='true'>&times;</span>" +
          "</button>" +
        "</div>" +
        "<div class='modal-body'>" +
          "<div id='command_history_div_" + v_tab.id + "' class='query_command_history'>" +
            "<div id='command_history_header_" + v_tab.id + "' class='query_command_history_header'></div>" +
            "<div id='command_history_grid_" + v_tab.id + "' class='query_command_history_grid'></div>" +
          "</div>" +
        "</div>" +
      "</div>" +
    "</div>" +
  "</div>";

  var v_html =
  "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 200px;'></div>" +
  "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dashed #acc4e8;'></div><div style='height:5px;'></div></div>" +
  command_history_modal +
  "<div class='row mb-1'>" +
    "<div class='tab_actions omnidb__tab-actions col-12'>" +
      "<button id='bt_start_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn' title='Run' onclick='querySQL(0);'><i class='fas fa-play fa-light'></i></button>" +
      "<button id='bt_indent_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Indent SQL' onclick='indentSQL();'><i class='fas fa-indent fa-light'></i></button>" +
      "<button id='bt_history_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Command History' onclick='showCommandList();'><i class='fas fa-list fa-light'></i></button>" +
      "<button id='bt_explain_" + v_tab.id + "' class='dbms_object postgresql_object btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' onclick='getExplain(0)' title='Explain' style='display: none;'><i class='fas fa-search fa-light'></i></button>" +
      "<button id='bt_analyze_" + v_tab.id + "' class='dbms_object postgresql_object btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' onclick='getExplain(1)' title='Explain Analyze' style='display: none;'><i class='fas fa-search-plus fa-light'></i></button>" +
      "<div class='omnidb__form-check form-check form-check-inline'><input id='check_autocommit_" + v_tab.id + "' class='form-check-input' type='checkbox' checked='checked'><label class='form-check-label dbms_object postgresql_object custom_checkbox query_info' for='check_autocommit_" + v_tab.id + "'>Autocommit</label></div>" +
      "<div class='omnidb__tab-status'><i id='query_tab_status_" + v_tab.id + "' title='Not connected' class='fas fa-dot-circle tab-status tab-status-closed dbms_object postgresql_object omnidb__tab-status__icon'></i><span id='query_tab_status_text_" + v_tab.id + "' title='Not connected' class='tab-status-text query_info dbms_object postgresql_object'>Not connected</span></div>" +
      "<button id='bt_fetch_more_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Run' style='display: none; ' onclick='querySQL(1);'>Fetch more</button>" +
      "<button id='bt_fetch_all_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(2);'>Fetch all</button>" +
      "<button id='bt_commit_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(3);'>Commit</button>" +
      "<button id='bt_rollback_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(4);'>Rollback</button>" +
      "<button id='bt_cancel_" + v_tab.id + "' class='btn btn-sm btn-danger omnidb__tab-actions__btn' title='Cancel' style='display: none; ' onclick='cancelSQL();'>Cancel</button>" +
      "<div id='div_query_info_" + v_tab.id + "' class='query_info query_info_summary' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
      "<button class='btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn ml-auto' title='Export Data' onclick='exportData();'><i class='far fa-file fa-light'></i></button>" +
      "<select id='sel_export_type_" + v_tab.id + "' class='form-control omnidb__tab-actions__select' style='width: 80px;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option></select>" +
    "</div>" +
  "</div>" +
  "<div id='query_result_tabs_" + v_tab.id + "' class='omnidb__query-result-tabs'></div>";

  v_tab.elementDiv.innerHTML = v_html;

  // Creating tab list at the bottom of the query tab
  var v_curr_tabs = createTabControl({ p_div: 'query_result_tabs_' + v_tab.id });

  // Functions called when each tab is clicked on
  var v_selectDataTabFunc = function() {
    v_curr_tabs.selectTabIndex(0);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currQueryTab = 'data';
    refreshHeights();
  }

  var v_selectMessageTabFunc = function() {

    v_curr_tabs.selectTabIndex(1);
    v_tag.currQueryTab = 'message';
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_count_notices.style.display = 'none';
    refreshHeights();
  }

  var v_selectExplainTabFunc = function() {
    v_curr_tabs.selectTabIndex(2);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currQueryTab = 'explain';
    refreshHeights();
  }

  var v_data_tab = v_curr_tabs.createTab(
    {
      p_name: 'Data',
      p_close: false,
      p_clickFunction: function(e) {
        v_selectDataTabFunc();
      }
    });
  v_data_tab.elementDiv.innerHTML =
  "<div class='p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary'>" +
    "<div id='div_result_" + v_tab.id + "' class='omnidb__query-result-tabs__content' style='width: 100%; overflow: hidden;'></div>" +
  "</div>";
  var v_messages_tab = v_curr_tabs.createTab(
    {
      p_name: "Messages <div id='query_result_tabs_count_notices_" + v_tab.id + "' class='count_notices' style='display: none;'></div>",
      p_close: false,
      p_clickFunction: function(e) {
        v_selectMessageTabFunc();
      }
    });
  v_messages_tab.elementDiv.innerHTML = "<div id='div_notices_" + v_tab.id + "' class='p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary' style='width: 100%; line-height: 16px; user-select: initial;'></div>";
  v_messages_tab.elementA.classList.add('dbms_object');
  v_messages_tab.elementA.classList.add('postgresql_object');
  var v_explain_tab = v_curr_tabs .createTab(
    {
      p_name: "Explain",
      p_close: false,
      p_clickFunction: function(e) {
        v_selectExplainTabFunc();
      }
    });
  v_explain_tab.elementDiv.innerHTML = "<div id='div_explain_" + v_tab.id + "' class='p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary' style='width: 100%; overflow: auto;'></div>";
  v_explain_tab.elementA.classList.add('dbms_object');
  v_explain_tab.elementA.classList.add('postgresql_object');

  var langTools = ace.require("ace/ext/language_tools");
  var v_editor = ace.edit('txt_query_' + v_tab.id);
  v_editor.$blockScrolling = Infinity;
  v_editor.setTheme("ace/theme/" + v_editor_theme);
  v_editor.session.setMode("ace/mode/sql");

  v_editor.setFontSize(Number(v_font_size));

  //v_editor.commands.bindKey("ctrl-space", null);

  //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
  v_editor.commands.bindKey("Cmd-,", null)
  v_editor.commands.bindKey("Ctrl-,", null)
  v_editor.commands.bindKey("Cmd-Delete", null)
  v_editor.commands.bindKey("Ctrl-Delete", null)
  v_editor.commands.bindKey("Ctrl-Up", null)
  v_editor.commands.bindKey("Ctrl-Down", null)

  document.getElementById('txt_query_' + v_tab.id).onclick = function() {
    v_editor.focus();
  };

  var v_tab_db_id = null;
  if (p_tab_db_id)
    v_tab_db_id = p_tab_db_id;

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'query',
    editor: v_editor,
    editorDivId: 'txt_query_' + v_tab.id,
    query_info: document.getElementById('div_query_info_' + v_tab.id),
    div_result: document.getElementById('div_result_' + v_tab.id),
    div_notices: document.getElementById('div_notices_' + v_tab.id),
    div_explain: document.getElementById('div_explain_' + v_tab.id),
    div_count_notices: document.getElementById('query_result_tabs_count_notices_' + v_tab.id),
    sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
    sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
    tab_title_span : v_tab_title_span,
    tab_loading_span : v_tab_loading_span,
    tab_check_span : v_tab_check_span,
    tab_stub_span : v_tab_stub_span,
    query_tab_status: document.getElementById('query_tab_status_' + v_tab.id),
    query_tab_status_text: document.getElementById('query_tab_status_text_' + v_tab.id),
    bt_start: document.getElementById('bt_start_' + v_tab.id),
    bt_fetch_more: document.getElementById('bt_fetch_more_' + v_tab.id),
    bt_fetch_all: document.getElementById('bt_fetch_all_' + v_tab.id),
    bt_commit: document.getElementById('bt_commit_' + v_tab.id),
    bt_rollback: document.getElementById('bt_rollback_' + v_tab.id),
    bt_start: document.getElementById('bt_start_' + v_tab.id),
    bt_indent: document.getElementById('bt_indent_' + v_tab.id),
    bt_explain: document.getElementById('bt_explain_' + v_tab.id),
    bt_analyze: document.getElementById('bt_analyze_' + v_tab.id),
    bt_history: document.getElementById('bt_history_' + v_tab.id),
    bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
    bt_export: document.getElementById('bt_export_' + v_tab.id),
    check_autocommit: document.getElementById('check_autocommit_' + v_tab.id),
    state : 0,
    context: null,
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    queryTabControl: v_curr_tabs,
    currQueryTab: null,
    connTab: v_connTabControl.selectedTab,
    currDatabaseIndex: null,
    tab_db_id: v_tab_db_id,
    tempData: [],
    commandHistory: {
        modal: document.getElementById('modal_command_history_' + v_tab.id),
        div: document.getElementById('command_history_div_' + v_tab.id),
        headerDiv: document.getElementById('command_history_header_' + v_tab.id),
        gridDiv: document.getElementById('command_history_grid_' + v_tab.id),
        grid: null,
        currentPage: 1,
        pages: 1,
        spanNumPages: null,
        spanCurrPage: null,
        inputStartedFrom: null,
        inputStartedFromLastValue: null,
        inputStartedTo: null,
        inputStartedToLastValue: null,
        inputCommandContains: null,
        inputCommandContainsLastValue: null
     }
  };

  v_tab.tag = v_tag;

  v_tag.selectDataTabFunc    = v_selectDataTabFunc;
  v_tag.selectMessageTabFunc = v_selectMessageTabFunc;
  v_tag.selectExplainTabFunc = v_selectExplainTabFunc;

  v_selectDataTabFunc();

  // Creating + tab in the outer tab list
  var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
    {
      p_name: '+',
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        showMenuNewTab(e);
      }
    });
  v_add_tab.tag = {
    mode: 'add'
  }

  setTimeout(function() {
    refreshHeights();
  },10);

  //adjustQueryTabObjects(false);
  v_editor.focus();

};
