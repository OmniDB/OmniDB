var v_createEditDataTabFunction = function(p_table) {

  var v_name = 'Query';
  if (p_table)
    v_name = p_table;

  // Removing last tab of the inner tab list
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_icon: '<i class="fas fa-table icon-tab-title"></i>',
    p_name: '<span id="tab_title">' + v_name + '</span><span id="tab_stub"><img style="width: 24px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i>',
    p_selectFunction: function() {
      if(this.tag != null) {
        refreshHeights();
        $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips
      }
      if(this.tag != null && this.tag.editor != null) {
          this.tag.editor.focus();
          checkEditDataStatus(this);
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

  // //Adding unique names to spans
  // var v_tab_title_span = document.getElementById('tab_title');
  // v_tab_title_span.id = 'tab_title_' + v_tab.id;
  // var v_tab_loading_span = document.getElementById('tab_loading');
  // v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
  // var v_tab_close_span = document.getElementById('tab_close');
  // v_tab_close_span.id = 'tab_close_' + v_tab.id;
  // v_tab_close_span.onclick = function(e) {
  //   var v_current_tab = v_tab;
  //   beforeCloseTab(e,
  //     function() {
  //       removeTab(v_current_tab);
  //     });
  // };
  // var v_tab_check_span = document.getElementById('tab_check');
  // v_tab_check_span.id = 'tab_check_' + v_tab.id;
  // var v_tab_stub_span = document.getElementById('tab_stub');
  // v_tab_stub_span.id = 'tab_stub_' + v_tab.id;
  //
  // v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

  var v_html =
  "<div class='p-2 omnidb__theme-border-top--primary'>" +
    "<div id='div_edit_data_select_" + v_tab.id + "' class='query_info mb-2' style='font-size: 1.15rem;'>" +
      "<span class='text-primary'>select</span> * <span class='text-primary'>from</span> " + p_table + " t" +
    "</div>" +
  "</div>" +
  "<div id='txt_filter_data_" + v_tab.id + "' style=' width: 100%; height: 100px;border: 1px solid #c3c3c3;'></div>" +
  "<div onmousedown='resizeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dashed #acc4e8;'></div><div style='height:5px;'></div></div>" +
  "<div class='row mb-1'>" +
    "<div class='tab_actions omnidb__tab-actions col-12'>" +
      "<button id='bt_start_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn' title='Run' onclick='queryEditData();'><i class='fas fa-play'></i></button>" +
      "<select id='sel_filtered_data_" + v_tab.id + "' class='sel_export_file_type form-control w-auto mr-2' onchange='queryEditData()'><option selected='selected' value='10' >Query 10 rows</option><option value='100'>Query 100 rows</option><option value='1000'>Query 1000 rows</option></select>" +
      "<button id='bt_cancel_" + v_tab.id + "' class='btn btn-sm btn-danger omnidb__tab-actions__btn' title='Cancel' style='display: none;' onclick='cancelEditData();'>Cancel</button>" +
      "<div id='div_edit_data_query_info_" + v_tab.id + "' class='query_info' style='display: inline-block; margin-left: 5px; vertical-align: middle;'></div>" +
      "<button id='bt_saveEditData_" + v_tab.id + "' onclick='saveEditData()' class='btn btn-sm btn-success omnidb__tab-actions__btn' style='visibility: hidden;'>Save Changes</button>" +
    "</div>" +
  "</div>" +
  "<div class='p-2 omnidb__theme-border--primary'>" +
    "<div id='div_edit_data_data_" + v_tab.id + "' style='width: 100%; overflow: auto;'></div>";
  "</div>";

  v_tab.elementDiv.innerHTML = v_html;

  var v_height  = window.innerHeight - $('#div_edit_data_data_' + v_tab.id).offset().top - 20;

  document.getElementById('div_edit_data_data_' + v_tab.id).style.height = v_height + "px"

  var langTools = ace.require("ace/ext/language_tools");
  var v_editor = ace.edit('txt_filter_data_' + v_tab.id);
  v_editor.$blockScrolling = Infinity;
  v_editor.setTheme("ace/theme/" + v_editor_theme);
  v_editor.session.setMode("ace/mode/sql");
  v_editor.commands.bindKey(v_keybind_object.v_autocomplete, "startAutocomplete");
  v_editor.commands.bindKey(v_keybind_object.v_autocomplete_mac, "startAutocomplete");

  v_editor.setFontSize(Number(v_font_size));

  //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
  v_editor.commands.bindKey("Cmd-,", null)
  v_editor.commands.bindKey("Ctrl-,", null)
  v_editor.commands.bindKey("Cmd-Delete", null)
  v_editor.commands.bindKey("Ctrl-Delete", null)
  v_editor.commands.bindKey("Ctrl-Up", null)
  v_editor.commands.bindKey("Ctrl-Down", null)

  document.getElementById('txt_filter_data_' + v_tab.id).onclick = function() {

    v_editor.focus();

  };



  var qtags = {
    getCompletions: function(editor, session, pos, prefix, callback) {

      if (v_completer_ready && prefix!='') {

          var wordlist = [];

          v_completer_ready = false;

          addLoadingCursor();

          execAjax('/get_completions_table/',
              JSON.stringify({"p_database_index": v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                              "p_tab_id": v_connTabControl.selectedTab.id,
                              "p_table": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.table,
                              "p_schema": v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editDataObject.schema}),
              function(p_return) {

                removeLoadingCursor();
                v_completer_ready = true;

                wordlist = p_return.v_data;
                callback(null, wordlist);

              },
              function(p_return) {
                removeLoadingCursor();
                v_completer_ready = true;
                if (p_return.v_data.password_timeout) {
                  showPasswordPrompt(
                    v_connTabControl.selectedTab.tag.selectedDatabaseIndex,
                    function() {
                      v_editor.focus();
                    },
                    function() {
                      v_editor.focus();
                    },
                    p_return.v_data.message
                  );
                }
              },
              'box',
              false);
      }
      else {
        callback(null, wordlist);
      }
    }
  }
  langTools.addCompleter([qtags]);
  v_editor.completers = [qtags];
  v_editor.setOptions({enableBasicAutocompletion: true});

  var v_tag = {
    tab_id: v_tab.id,
    editor: v_editor,
    editorDivId: 'txt_filter_data_' + v_tab.id,
    query_info: document.getElementById('div_edit_data_query_info_' + v_tab.id),
    div_result: document.getElementById('div_edit_data_data_' + v_tab.id),
    sel_filtered_data : document.getElementById('sel_filtered_data_' + v_tab.id),
    button_save: document.getElementById('bt_saveEditData_' + v_tab.id),
    sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
    bt_cancel: document.getElementById('bt_cancel_' + v_tab.id),
    bt_save: document.getElementById('bt_save_' + v_tab.id),
    tab_title_span : v_tab_title_span,
    tab_loading_span : v_tab_loading_span,
    // tab_close_span : v_tab_close_span,
    tab_check_span : v_tab_check_span,
    tab_stub_span : v_tab_stub_span,
    state: 0,
    context: null,
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    connTab: v_connTabControl.selectedTab,
    // tabId: v_connTabControl.selectedTab.tag.tabControl.tabCounter,
    // tabCloseSpan: v_tab_close_span,
    mode: 'edit'
  };

  // {
  //   tab_id: v_tab.id,
  //   tabTitle: 'teste',
  //   divTree: document.getElementById(v_tab.id + '_tree'),
  //   divLeft: document.getElementById(v_tab.id + '_div_left'),
  //   divRight: document.getElementById(v_tab.id + '_div_right'),
  //   // tab_title_span : v_tab_title_span,
  //   // tab_close_span : v_tab_close_span,
  //   query_info: document.getElementById('div_query_info_' + v_tab.id),
  //   div_result: document.getElementById('div_result_' + v_tab.id),
  //   bt_refresh: v_bt_refresh,
  //   tabControl: v_connTabControl.selectedTab.tag.tabControl,
  //   ht: null,
  //   query: p_query,
  //   actions: p_actions,
  //   mode: 'monitor_grid'
  // };

  v_tab.tag = v_tag;

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

};
