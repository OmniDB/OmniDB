var v_createSnippetTextTabFunction = function(p_snippet) {

  var v_name = 'New Snippet';
  if (p_snippet)
    v_name = p_snippet;

  v_connTabControl.selectedTab.tag.tabControl.removeTabIndex(v_connTabControl.selectedTab.tag.tabControl.tabList.length-1);
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_name: '<span id="tab_title">' + v_name + '</span><span id="tab_stub"><img style="width: 24px; display: inline-block;"/></span><span id="tab_loading" style="display:none;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i>',
    p_selectFunction: function() {
      if(this.tag != null) {
        refreshHeights();
      }
      if(this.tag != null && this.tag.editor != null) {
          this.tag.editor.focus();
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
  v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

  //Adding unique names to spans
  var v_tab_title_span = document.getElementById('tab_title');
  v_tab_title_span.id = 'tab_title_' + v_tab.id;
  var v_tab_loading_span = document.getElementById('tab_loading');
  v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
  var v_tab_check_span = document.getElementById('tab_check');
  v_tab_check_span.id = 'tab_check_' + v_tab.id;
  var v_tab_stub_span = document.getElementById('tab_stub');
  v_tab_stub_span.id = 'tab_stub_' + v_tab.id;
  //var v_tab_close_span = document.getElementById('tab_close');
  //v_tab_close_span.id = 'tab_close_' + v_tab.id;
  //v_tab_close_span.onclick = function(e) {
  //  var v_current_tab = v_tab;
  //  beforeCloseTab(e,
  //    function() {
  //      closeSnippetTab(v_current_tab);
  //    });
  //};

  var v_html =
  "<div id='txt_snippet_" + v_tab.id + "' style=' width: 100%; height: 200px; border: 1px solid #c3c3c3;'></div>" +
  "<div class='tab_actions omnidb__tab-actions'>" +
    "<button id='bt_indent_" + v_tab.id + "' class='btn btn-sm omnidb__theme__btn--primary omnidb__tab-actions__btn' title='Indent SQL' onclick='indentSQL();'><i class='fas fa-indent fa-light'></i></button>" +
    "<button id='bt_save_" + v_tab.id + "' class='btn btn-sm btn-success omnidb__tab-actions__btn' title='Save' style='margin-top: 5px; margin-bottom: 5px; margin-right: 5px; display: inline-block;' onclick='saveSnippetText();'><i class='fas fa-save fa-light'></i></button>" +
  "</div>";

  var v_div = document.getElementById('div_' + v_tab.id);
  v_div.innerHTML = v_html;

  var v_txt_snippet = document.getElementById('txt_snippet_' + v_tab.id);

  v_txt_snippet.style.height = window.innerHeight - $(v_txt_snippet).offset().top - 70 + 'px';

  var langTools = ace.require("ace/ext/language_tools");
  var v_editor = ace.edit('txt_snippet_' + v_tab.id);
  v_editor.$blockScrolling = Infinity;
  v_editor.setTheme("ace/theme/" + v_editor_theme);
  v_editor.session.setMode("ace/mode/sql");

  v_editor.setFontSize(Number(v_editor_font_size));

  v_editor.commands.bindKey("ctrl-space", null);

  //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
  v_editor.commands.bindKey("Cmd-,", null)
  v_editor.commands.bindKey("Ctrl-,", null)
  v_editor.commands.bindKey("Cmd-Delete", null)
  v_editor.commands.bindKey("Ctrl-Delete", null)
  v_editor.commands.bindKey("Ctrl-Up", null)
  v_editor.commands.bindKey("Ctrl-Down", null)

  v_txt_snippet.onclick = function() {

    v_editor.focus();

  };

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'snippet',
    editor: v_editor,
    editorDiv: v_txt_snippet,
    editorDivId: 'txt_snippet_' + v_tab.id,
    query_info: document.getElementById('div_query_info_' + v_tab.id),
    div_result: document.getElementById('div_result_' + v_tab.id),
    sel_export_type : document.getElementById('sel_export_type_' + v_tab.id),
    tab_title_span : v_tab_title_span,
    tab_loading_span : v_tab_loading_span,
    tab_check_span : v_tab_check_span,
    tab_stub_span : v_tab_stub_span,
    bt_start: document.getElementById('bt_start_' + v_tab.id),
    bt_save: document.getElementById('bt_save_' + v_tab.id),
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    snippetTab: v_connTabControl.selectedTab,
    snippetObject: null
  };

  v_tab.tag = v_tag;

  // Creating + tab in the outer tab list
  var v_add_tab = v_connTabControl.selectedTab.tag.tabControl.createTab(
    {
      p_name: '+',
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        // showMenuNewTab(e);
        v_connTabControl.tag.createSnippetTextTab();
      }
    });
  v_add_tab.tag = {
    mode: 'add'
  }

  setTimeout(function() {
    refreshHeights();
  },10);

  v_editor.focus();

};
