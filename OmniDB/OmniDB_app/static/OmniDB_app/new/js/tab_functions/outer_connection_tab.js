var v_createConnTabFunction = function(p_index,p_create_query_tab = true) {

  if (v_connTabControl.tag.connections.length==0) {
    v_connTabControl.selectTabIndex(v_connTabControl.tabList.length-2);
    showAlert('Create connections first.');
  }
  else {

    v_connTabControl.removeLastTab();

    var v_tab = v_connTabControl.createTab({
      p_name: '<span id="tab_title"><img src="' + v_url_folder + '/static/OmniDB_app/images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/> ' + v_connTabControl.tag.connections[0].v_alias + '</span>',
      p_selectFunction: function() {
        document.title = 'OmniDB'
        if(this.tag != null) {
          checkTabStatus(this);
          refreshHeights(true);
        }
        if(this.tag != null && this.tag.tabControl != null && this.tag.tabControl.selectedTab.tag.editor != null) {
            this.tag.tabControl.selectedTab.tag.editor.focus();
        }
      },
      p_closeFunction: function(e,p_tab) {
        var v_this_tab = p_tab;
        beforeCloseTab(e,
          function() {
            var v_tabs_to_remove = [];
            for (var i=0; i < v_connTabControl.selectedTab.tag.tabControl.tabList.length; i++) {

              var v_tab = v_connTabControl.selectedTab.tag.tabControl.tabList[i];
              if (v_tab.tag!=null) {
                if (v_tab.tag.mode=='query' || v_tab.tag.mode=='edit' || v_tab.tag.mode=='debug' || v_tab.tag.mode=='console') {
                  var v_message_data = { tab_id: v_tab.tag.tab_id, tab_db_id: null };
                  if (v_tab.tag.mode=='query')
                    v_message_data.tab_db_id = v_tab.tag.tab_db_id;
                  v_tabs_to_remove.push(v_message_data);
                }
                else if (v_tab.tag.mode=='monitor_dashboard') {
                  v_tab.tag.tab_active = false;
                  cancelMonitorUnits(v_tab.tag);
                }
              }

              if (v_tab.tag.tabCloseFunction)
                v_tab.tag.tabCloseFunction(v_tab.tag);
            }
            if (v_tabs_to_remove.length>0)
              sendWebSocketMessage(v_queryWebSocket, v_queryRequestCodes.CloseTab, v_tabs_to_remove, false, null);
            v_this_tab.removeTab();
          });
      }
    });

    v_connTabControl.selectTab(v_tab);

    var v_width = Math.ceil((300/window.innerWidth)*100);
    var v_complement_width = 100 - v_width;

    var v_html =
    "<div class='container-fluid'>" +
      "<div class='row'>" +
        "<div id='" + v_tab.id + "_div_left' class='col-md-2'>" +
          "<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +
          "<div style='margin-right: 10px;'>" +
            "<div id='" + v_tab.id + "_details' class='connection_details' ></div>" +
            "<div id='" + v_tab.id + "_tree' style='margin-top: 5px; overflow: auto; height: 300px;'></div>" +
            "<div onmousedown='resizeTreeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
            "<div style='position: relative;'>" +
              "<div id='" + v_tab.id + "_loading' class='div_loading' style='z-index: 1000;'>" +

              '<div class="div_loading_cover"></div>' +
              '<div class="div_loading_content">' +
              '  <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">' +
              '    <span class="sr-only ">Loading...</span>' +
              '  </div>' +
              '</div>' +
              "</div>" +
              "<div id='tree_tabs_" + v_tab.id + "' style='position: relative;'></div>" +
            "</div>" +
          "</div>" +
        "</div>" +
        "<div id='" + v_tab.id + "_div_right' class='col-md-10'>" +
          "<div id='" + v_tab.id + "_tabs'></div>" +
        "</div>" +
      "</div>" +
    "</div>";

    var v_tab_title_span = document.getElementById('tab_title');
    v_tab_title_span.id = 'tab_title_' + v_tab.id;

    v_tab.elementDiv.innerHTML = v_html;

    // Tab control under the tree
    var v_treeTabs = createTabControl({ p_div: 'tree_tabs_' + v_tab.id });

    // Functions called when Properties and DDL tabs are clicked on
    var v_selectPropertiesTabFunc = function() {
      v_treeTabs.selectTabIndex(0);
      v_connTabControl.selectedTab.tag.currTreeTab = 'properties';
      refreshTreeHeight();
    }

    var v_selectDDLTabFunc = function() {
      v_treeTabs.selectTabIndex(1);
      v_connTabControl.selectedTab.tag.currTreeTab = 'ddl';
      refreshTreeHeight();
    }

    var v_properties_tab = v_treeTabs.createTab(
      {
        p_name: 'Properties',
        p_close: false,
        p_clickFunction: function(e) {
          v_selectPropertiesTabFunc();
        }
      });
      var v_ddl_tab = v_treeTabs.createTab(
        {
          p_name: 'DDL',
          p_close: false,
          p_clickFunction: function(e) {
            v_selectDDLTabFunc();
          }
        });
    v_treeTabs.selectTabIndex(0);

    // Tab control on the right (for queries, consoles, etc)
    var v_currTabControl = createTabControl({ p_div: v_tab.id + '_tabs' });
    v_currTabControl.createTab(
      {
        p_name: '+',
        p_close: false,
        p_selectable: false,
        p_clickFunction: function(e) {
          showMenuNewTab(e);
        }
      });

    //DDL editor
    var v_ddl_div = v_ddl_tab.elementDiv;

    var langTools = ace.require("ace/ext/language_tools");
    var v_editor = ace.edit(v_ddl_tab.elementDiv);
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
    v_editor.setReadOnly(true);

    v_ddl_div.onclick = function() {
      v_editor.focus();
    };

    //Properties Grid
    var v_divProperties = v_properties_tab.elementDiv;
    v_divProperties.classList.add('ht_invisible')
    v_divProperties.style.overflow = 'hidden';
    var v_ddlProperties = v_ddl_tab.elementDiv;

    var columnProperties = [];

    var col = new Object();
    col.title =  'Property';
    col.readOnly = true;
    columnProperties.push(col);

    var col = new Object();
    col.title =  'Value';
    col.readOnly = true;
    columnProperties.push(col);

    var ht = new Handsontable(v_divProperties,
                        {
                          licenseKey: 'non-commercial-and-evaluation',
                          data: [],
                          columns : columnProperties,
                          colHeaders : true,
                          stretchH: 'all',
                          autoColumnSize : true,
                          manualColumnResize: false,
                          minSpareCols :0,
                          minSpareRows :0,
                          fillHandle:false,
                          disableVisualSelection: true,
                          contextMenu: {
                            callback: function (key, options) {
                              if (key === 'view_data') {
                                  editCellData(this,options[0].start.row,options[0].start.col,this.getDataAtCell(options[0].start.row,options[0].start.col),false);
                              }
                              else if (key === 'copy') {
                                this.selectCell(options[0].start.row,options[0].start.col,options[0].end.row,options[0].end.col);
                                document.execCommand('copy');
                              }
                            },
                            items: {
                              "copy": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-copy cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Copy</div>'},
                              "view_data": {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
                            }
                          },
                          cells: function (row, col, prop) {

                            var cellProperties = {};
                            cellProperties.renderer = whiteHtmlRenderer;
                            return cellProperties;

                          }
                        });

    var v_tag = {
      tab_id: v_tab.id,
      tabControl: v_currTabControl,
      tabTitle: v_tab_title_span,
      divDetails: document.getElementById(v_tab.id + '_details'),
      divTree: document.getElementById(v_tab.id + '_tree'),
      divProperties: v_divProperties,
      gridProperties: ht,
      gridPropertiesCleared: true,
      divDDL: v_ddlProperties,
      divLoading: document.getElementById(v_tab.id + '_loading'),
      divLeft: document.getElementById(v_tab.id + '_div_left'),
      divRight: document.getElementById(v_tab.id + '_div_right'),
      selectedDatabaseIndex: 0,
      connTabControl: v_connTabControl,
      mode: 'connection',
      firstTimeOpen: true,
      TreeTabControl: v_treeTabs,
      currTreeTab: null,
      ddlEditor: v_editor,
      consoleHistoryFecthed: false,
      consoleHistoryList: null
    };

    v_tab.tag = v_tag;

    v_tag.selectPropertiesTabFunc = v_selectPropertiesTabFunc;
    v_tag.selectDDLTabFunc = v_selectDDLTabFunc;

    var v_index = v_connTabControl.tag.connections[0].v_conn_id;
    if (p_index)
      v_index = p_index;

    changeDatabase(v_index);

    if (p_create_query_tab) {
       v_connTabControl.tag.createConsoleTab();
       v_connTabControl.tag.createQueryTab();
    }

    // Creating + tab in the outer tab list
    v_connTabControl.createTab(
      {
        p_name: '+',
        p_close: false,
        p_selectable: false,
        p_clickFunction: function(e) {
          showMenuNewTabOuter(e);
        }
      });


    setTimeout(function() {
      v_selectPropertiesTabFunc();
    },10);

  }

  endLoading();

}
