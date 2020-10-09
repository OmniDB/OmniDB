var v_createQueryTabFunction = function(p_table, p_tab_db_id) {
  // Removing last tab of the inner tab list.
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  // Updating inner tab_name.
  var v_name = 'Query';
  if (p_table) {
    v_name = p_table;
  }
  let v_name_html =
  '<span id="tab_title">' +
    v_name +
  '</span>' +
  '<span id="tab_loading" style="visibility:hidden;">' +
    '<i class="tab-icon node-spin"></i>' +
  '</span>' +
  '<i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i>';

  // Creating console tab in the inner tab list.
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_name: v_name_html,
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

  // Selecting newly created tab.
  v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

  // Adding unique names to spans.
  var v_tab_title_span = document.getElementById('tab_title');
  v_tab_title_span.id = 'tab_title_' + v_tab.id;
  var v_tab_loading_span = document.getElementById('tab_loading');
  v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
  var v_tab_check_span = document.getElementById('tab_check');
  v_tab_check_span.id = 'tab_check_' + v_tab.id;

  // Creating the template for the command_history_modal.
  var command_history_modal =
  "<div class='modal fade' id='modal_command_history_" + v_tab.id + "' tabindex='-1' role='dialog' aria-hidden='true'>" +
    "<div class='modal-dialog modal-xl' role='document'>" +
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
            "<div id='command_history_grid_" + v_tab.id + "' class='query_command_history_grid' style='width: 100%; height: calc(100vh - 16.5rem); overflow: hidden;'></div>" +
          "</div>" +
        "</div>" +
      "</div>" +
    "</div>" +
  "</div>";

  // Creating the template for the inner_query_tab.
  var v_html =
  "<div id='txt_query_" + v_tab.id + "' style=' width: 100%; height: 200px;'></div>" +
  "<div class='omnidb__resize-line__container' onmousedown='resizeVertical(event)' style='width: 100%; height: 5px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 0px; border-bottom: 1px dashed #acc4e8;'></div><div style='height:5px;'></div></div>" +
  command_history_modal +
  "<div class='row mb-1'>" +
    "<div class='tab_actions omnidb__tab-actions col-12'>" +
      "<button id='bt_start_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn' title='Run' onclick='querySQL(0);'><i class='fas fa-play fa-light'></i></button>" +
      "<button id='bt_indent_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Indent SQL' onclick='indentSQL();'><i class='fas fa-indent fa-light'></i></button>" +
      "<button id='bt_history_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Command History' onclick='showCommandList();'><i class='fas fa-list fa-light'></i></button>" +
      "<button id='bt_explain_" + v_tab.id + "' class='dbms_object postgresql_object btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' onclick='getExplain(0)' title='Explain' style='display: none;'><i class='fas fa-search fa-light'></i></button>" +
      "<button id='bt_analyze_" + v_tab.id + "' class='dbms_object postgresql_object btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' onclick='getExplain(1)' title='Explain Analyze' style='display: none;'><i class='fas fa-search-plus fa-light'></i></button>" +
      "<div class='dbms_object postgresql_object omnidb__form-check form-check form-check-inline'><input id='check_autocommit_" + v_tab.id + "' class='form-check-input' type='checkbox' checked='checked'><label class='form-check-label dbms_object postgresql_object custom_checkbox query_info' for='check_autocommit_" + v_tab.id + "'>Autocommit</label></div>" +
      "<div class='dbms_object postgresql_object omnidb__tab-status'><i id='query_tab_status_" + v_tab.id + "' title='Not connected' class='fas fa-dot-circle tab-status tab-status-closed dbms_object postgresql_object omnidb__tab-status__icon'></i><span id='query_tab_status_text_" + v_tab.id + "' title='Not connected' class='tab-status-text query_info dbms_object postgresql_object ml-1'>Not connected</span></div>" +
      "<button id='bt_fetch_more_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Run' style='display: none; ' onclick='querySQL(1);'>Fetch more</button>" +
      "<button id='bt_fetch_all_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(2);'>Fetch all</button>" +
      "<button id='bt_commit_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(3);'>Commit</button>" +
      "<button id='bt_rollback_" + v_tab.id + "' class='dbms_object dbms_object_hidden postgresql_object btn btn-sm omnidb__theme__btn--secondary omnidb__tab-actions__btn' title='Run' style='margin-left: 5px; display: none; ' onclick='querySQL(4);'>Rollback</button>" +
      "<button id='bt_cancel_" + v_tab.id + "' class='btn btn-sm btn-danger omnidb__tab-actions__btn' title='Cancel' style='display: none; ' onclick='cancelSQL();'>Cancel</button>" +
      "<div id='div_query_info_" + v_tab.id + "' class='omnidb__query-info'></div>" +
      "<button class='btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn ml-auto' title='Export Data' onclick='v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.exportData();'><i class='far fa-file fa-light'></i></button>" +
      "<select id='sel_export_type_" + v_tab.id + "' class='form-control omnidb__tab-actions__select' style='width: 80px;'><option selected='selected' value='csv' >CSV</option><option value='xlsx' >XLSX</option></select>" +
    "</div>" +
  "</div>" +
  "<div id='query_result_tabs_container" + v_tab.id + "' class='omnidb__query-result-tabs'>" +
    "<button style='position:absolute;top:0.25rem;right:0.25rem;' type='button' class='btn btn-sm omnidb__theme__btn--secondary' onclick=toggleExpandToPanelView('query_result_tabs_container" + v_tab.id + "')><i class='fas fa-expand'></i></button>" +
    "<div id='query_result_tabs_" + v_tab.id + "'>" +
    "</div>" +
  "</div>";

  // Updating the html.
  v_tab.elementDiv.innerHTML = v_html;

  // Creating tab list at the bottom of the query tab.
  var v_curr_tabs = createTabControl({ p_div: 'query_result_tabs_' + v_tab.id });

  // Tab selection callback for `data` tab.
  var v_selectDataTabFunc = function() {
    v_curr_tabs.selectTabIndex(0);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currQueryTab = 'data';
    refreshHeights();
  }

  // Tab selection callback for `message` tab.
  var v_selectMessageTabFunc = function() {
    v_curr_tabs.selectTabIndex(1);
    v_tag.currQueryTab = 'message';
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_count_notices.style.display = 'none';
    refreshHeights();
  }

  // Tab selection callback for `explain` tab.
  var v_selectExplainTabFunc = function() {
    v_curr_tabs.selectTabIndex(2);
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.currQueryTab = 'explain';
    refreshHeights();
  }

  // Creating the `data` tab.
  var v_data_tab = v_curr_tabs.createTab({
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

  // Creating the `message` tab.
  var v_messages_tab = v_curr_tabs.createTab({
    p_name: "Messages <div id='query_result_tabs_count_notices_" + v_tab.id + "' class='count_notices' style='display: none;'></div>",
    p_close: false,
    p_clickFunction: function(e) {
      v_selectMessageTabFunc();
    }
  });
  v_messages_tab.elementDiv.innerHTML =
  "<div class='p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary'>" +
    "<div id='div_notices_" + v_tab.id + "' class='omnidb__query-result-tabs__content' style='width: 100%; overflow: hidden;'></div>" +
  "</div>";
  v_messages_tab.elementA.classList.add('dbms_object');
  v_messages_tab.elementA.classList.add('postgresql_object');

  // Creating the `explain` tab.
  var v_explain_tab = v_curr_tabs .createTab({
    p_name: "Explain",
    p_close: false,
    p_clickFunction: function(e) {
      v_selectExplainTabFunc();
    }
  });
  v_explain_tab.elementDiv.innerHTML =
  "<div class='p-2 omnidb__query-result-tabs__content omnidb__theme-border--primary'>" +
    "<div id='div_explain_" + v_tab.id + "' class='omnidb__query-result-tabs__content' style='width: 100%; overflow: hidden;'></div>" +
  "</div>";
  v_explain_tab.elementA.classList.add('dbms_object');
  v_explain_tab.elementA.classList.add('postgresql_object');

  // Creating the editor for `query`.
  var langTools = ace.require("ace/ext/language_tools");
  var v_editor = ace.edit('txt_query_' + v_tab.id);
  v_editor.$blockScrolling = Infinity;
  v_editor.setTheme("ace/theme/" + v_editor_theme);
  v_editor.session.setMode("ace/mode/sql");
  v_editor.setFontSize(Number(v_font_size));

  // Setting custom keyboard shortcuts callbacks.
  $('#txt_query_' + v_tab.id).find('.ace_text-input').on('keyup',function(event){
    if (v_connTabControl.selectedTab.tag.enable_autocomplete !== false) {
      autocomplete_start(v_editor,0, event);
    }
  });
  $('#txt_query_' + v_tab.id).find('.ace_text-input').on('keydown',function(event){
    if (v_connTabControl.selectedTab.tag.enable_autocomplete !== false) {
      autocomplete_keydown(v_editor, event);
    }
  });
  // document.getElementById('txt_query_' + v_tab.id).addEventListener('keyup',function(event) {
  //   autocomplete_start(v_editor,0, event);
  // });
  // document.getElementById('txt_query_' + v_tab.id).addEventListener('keydown',function(event) {
  //   autocomplete_keydown(v_editor, event);
  // });

  document.getElementById('txt_query_' + v_tab.id).addEventListener('contextmenu',function(event) {
    event.stopPropagation();
    event.preventDefault();

    var v_option_list = [
      {
        text: 'Copy',
        icon: 'fas cm-all fa-terminal',
        action: function() {
          // Getting the value
          var copy_text = v_editor.getValue();
          // Calling copy to clipboard.
          uiCopyTextToClipboard(copy_text);
        }
      },
      {
        text: 'Save as snippet',
        icon: 'fas cm-all fa-save',
        submenu: {
          elements: buildSnippetContextMenuObjects('save', v_connTabControl.tag.globalSnippets, v_editor)
        }
      }
    ];

    if (v_connTabControl.tag.globalSnippets.files.length != 0 || v_connTabControl.tag.globalSnippets.folders.length != 0)
      v_option_list.push(
        {
          text: 'Use snippet',
          icon: 'fas cm-all fa-book',
          submenu: {
            elements: buildSnippetContextMenuObjects('load', v_connTabControl.tag.globalSnippets, v_editor)
          }
        }
      )
    customMenu(
      {
        x:event.clientX+5,
        y:event.clientY+5
      },
      v_option_list,
      null
    );
  });


  // Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
  v_editor.commands.bindKey("ctrl-space", null);
  v_editor.commands.bindKey("Cmd-,", null);
  v_editor.commands.bindKey("Ctrl-,", null);
  v_editor.commands.bindKey("Cmd-Delete", null);
  v_editor.commands.bindKey("Ctrl-Delete", null);
  v_editor.commands.bindKey("Ctrl-Up", null);
  v_editor.commands.bindKey("Ctrl-Down", null);
  v_editor.commands.bindKey("Up", null);
  v_editor.commands.bindKey("Down", null);
  v_editor.commands.bindKey("Tab", null);

  // Setting the autofocus for the editor component.
  document.getElementById('txt_query_' + v_tab.id).onclick = function() {
    v_editor.focus();
  };

  // Updating the tab_db_id.
  var v_tab_db_id = null;
  if (p_tab_db_id) {
    v_tab_db_id = p_tab_db_id;
  }

  // Creating the exportData action for the tab.
  var v_export_data = function() {
    var v_exp_callback = function(p_data) {
      console.log('exportData callback: ', p_data);
    	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.selectDataTabFunc();
    	var v_text = '<div style="font-size: 14px;">The file is ready. <a class="link_text" href="' + p_data.v_data.v_filename + '" download="'+ p_data.v_data.v_downloadname + '">Save</a></div>';
    	v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.div_result.innerHTML = v_text;
    }

  	var v_exp_query = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.getValue();
  	var v_exp_type = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.sel_export_type.value;
  	querySQL(0, true, v_exp_query, v_exp_callback,true,v_exp_query,'export_' + v_exp_type,true);
  }

  // Setting all tab_tag params.
  var v_tag = {
    tab_id: v_tab.id,
    mode: 'query',
    editor: v_editor,
    editorDivId: 'txt_query_' + v_tab.id,
    exportData: v_export_data,
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

  // Setting the v_tab_tag.
  v_tab.tag = v_tag;
  v_tag.selectDataTabFunc    = v_selectDataTabFunc;
  v_tag.selectMessageTabFunc = v_selectMessageTabFunc;
  v_tag.selectExplainTabFunc = v_selectExplainTabFunc;

  // Selecting the `data` tab by default.
  v_selectDataTabFunc();

  // Creating `Add` tab in the `inner_query` tab list
  var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
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

  // Requesting an update on the workspace layout and sizes.
  setTimeout(function() {
    refreshHeights();
  },10);
  adjustQueryTabObjects(false);
  v_editor.focus();

  // Sets a render refresh for the grid on the commandHistory.modal after the modal is fully loaded
  $(v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.modal).on('shown.bs.modal', function () {
    v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.commandHistory.grid.render();
  });
}
