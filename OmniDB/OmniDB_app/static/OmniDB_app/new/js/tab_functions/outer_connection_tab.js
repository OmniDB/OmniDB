var v_createConnTabFunction = function(p_index,p_create_query_tab = true, p_name = false, p_tooltip_name = false) {
  if (v_connTabControl.tag.connections.length==0) {
    v_connTabControl.selectTabIndex(v_connTabControl.tabList.length-2);
    showAlert('Create connections first.');
  }
  else {
    v_connTabControl.removeLastTab();

    let v_conn = v_connTabControl.tag.connections[0];
    for (let i = 0; i < v_connTabControl.tag.connections.length; i++) {
      if (v_connTabControl.tag.connections[i].v_conn_id === p_index) {
        v_conn = v_connTabControl.tag.connections[i];
      }
    }
    let v_conn_name = (p_name) ? p_name : v_conn.v_alias;
    if (!p_tooltip_name) {
      p_tooltip_name = '';
      if (v_conn.v_alias) {
        p_tooltip_name += '<h5 class="my-1">' + v_conn.v_alias + '</h5>';
      }
      if (v_conn.v_details1) {
        p_tooltip_name += '<div class="mb-1">' + v_conn.v_details1 + '</div>';
      }
      if (v_conn.v_details2) {
        p_tooltip_name += '<div class="mb-1">' + v_conn.v_details2 + '</div>';
      }
    }

    var v_tab = v_connTabControl.createTab({
      p_icon: '<img src="' + v_url_folder + '/static/OmniDB_app/images/' + v_connTabControl.tag.connections[0].v_db_type + '_medium.png"/>',
      p_name: v_conn_name,
      p_selectFunction: function() {
        document.title = 'OmniDB'
        if(this.tag != null) {
          checkTabStatus(this);
          refreshHeights(true);
        }
        if(this.tag != null && this.tag.tabControl != null && this.tag.tabControl.selectedTab.tag.editor != null) {
            this.tag.tabControl.selectedTab.tag.editor.focus();
        }
        $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips
      },
      p_close: false,// Replacing default close icon with contextMenu.
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
            if (v_tabs_to_remove.length>0) {
              createRequest(v_queryRequestCodes.CloseTab, v_tabs_to_remove);
            }
            v_this_tab.removeTab();
          });
      },
      p_rightClickFunction: function(e) {
        var v_option_list = [
          {
            text: '<p class=\"mb-0 text-danger\">Close Connection Tab</p>',
            // icon: 'fas cm-all fa-terminal text-danger',
            action: function() {
              if (v_tab.closeFunction!=null) {
                v_tab.closeFunction(e,v_tab);
              }
            }
          }
        ];
        customMenu(
          {
            x:e.clientX+5,
            y:e.clientY+5
          },
          v_option_list,
          null);
      },
      p_tooltip_name: p_tooltip_name
    });

    v_connTabControl.selectTab(v_tab);

    var v_width = Math.ceil((300/window.innerWidth)*100);
    var v_complement_width = 100 - v_width;

    var v_html =
    '<div class="container-fluid" style="position: relative;">' +
      '<div class="row">' +
        '<div id="' + v_tab.id + '_div_left" class="omnidb__workspace__div-left col" style="flex: 0 0 16.667%; max-width: 16.667%;">' +
          "<div class='row'>" +

            // "<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dashed #acc4e8;'></div><div style='width:5px;'></div></div>" +


            '<div class="omnidb__workspace__content-left">' +
              '<div id="' + v_tab.id + '_details" class="omnidb__workspace__connection-details"></div>' +
              '<div id="' + v_tab.id + '_tree" style="overflow: auto; flex-grow: 1; transition: scroll 0.3s;"></div>' +
              '<div id="' + v_tab.id + '_left_resize_line_horizontal" class="omnidb__resize-line__container" onmousedown="resizeTreeVertical(event)" style="width: 100%; height: 10px; cursor: ns-resize;"><div class="resize_line_horizontal" style="height: 5px; border-bottom: 1px dashed #acc4e8;"></div><div style="height:5px;"></div></div>' +
              '<div id="tree_tabs_parent_' + v_tab.id + '" class="omnidb__tree-tabs" style="position: relative;flex-shrink: 0;flex-basis: 40vh;">' +
                '<div id="' + v_tab.id + '_loading" class="div_loading" style="z-index: 1000;">' +
                  '<div class="div_loading_cover"></div>' +
                  '<div class="div_loading_content">' +
                  '  <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">' +
                  '    <span class="sr-only ">Loading...</span>' +
                  '  </div>' +
                  '</div>' +
                '</div>' +
                '<button type="button" onclick="toggleTreeTabsContainer(' + "'tree_tabs_parent_" + v_tab.id + "','" + v_tab.id + "_left_resize_line_horizontal'" + ')" class="btn omnidb__theme__btn--secondary omnidb__tree-tabs__toggler"><i class="fas fa-arrows-alt-v"></i></button>' +
                '<div id="tree_tabs_' + v_tab.id + '" class="omnidb__tree-tabs__container" style="position: relative;"></div>' +
              '</div>' +
            '</div>' +
          '</div>' +
          '<div class="resize_line_vertical omnidb__resize-line__container" onmousedown="resizeConnectionHorizontal(event)" style="position:absolute;height: 100%;width: 10px;cursor: ew-resize;border-right: 1px dashed #acc4e8;top: 0px;right: 0px;"></div>' +
        '</div>' +//.div_left
        '<div id="' + v_tab.id + '_div_right" class="omnidb__workspace__div-right col" style="position: relative; flex: 0 0 83.333%; max-width: 83.333%;">' +
          // "<div class='row'>" +
            '<div id="' + v_tab.id + '_tabs" class="w-100"></div>' +
          // "</div>" +
        '</div>' +//.div_right
      '</div>' +//.row

      // "<div id='" + v_tab.id + "_workspace_resize_grid' class='omnidb__workspace-resize-grid'>" +
      //   "<div class='container-fluid h-100'>" +
      //     "<div class='row h-100'>" +
      //
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'>" +
      //         "<div id='"+ v_tab.id + "_workspace_resize_draggable' ondragstart='dragStart(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragend='dragEnd(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' draggable='true' class='omnidb__workspace-resize-grid__draggable' style='width: 30px; height: 100%; cursor: ew-resize;'>" +
      //           "<div class='resize_line_vertical'><span>&#8633;</span></div>" +
      //         "</div>" +
      //       "</div></div>" +
      //
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //       "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
      //
      //     "</div>" +
      //   "</div>" +
      // "</div>" +

    '</div>';

    // var v_tab_title_span = document.getElementById('tab_title');
    // v_tab_title_span.id = 'tab_title_' + v_tab.id;
    var v_tab_title_span = $(v_tab.elementA).find('.omnidb__tab-menu__link-name');
    if (v_tab_title_span) {
      v_tab_title_span.attr('id', 'tab_title_' + v_tab.id);
    }


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
    // var v_currTabControl = createTabControl({ p_div: v_tab.id + '_tabs' });
    var v_currTabControl = createTabControl({
      p_div: v_tab.id + '_tabs',
      p_hierarchy: 'secondary'
    });
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

    var langTools = ace.require('ace/ext/language_tools');
    var v_editor = ace.edit(v_ddl_tab.elementDiv);
    v_editor.$blockScrolling = Infinity;
    v_editor.setTheme('ace/theme/' + v_editor_theme);
    v_editor.session.setMode('ace/mode/sql');

    v_editor.setFontSize(Number(v_font_size));

    v_editor.commands.bindKey('ctrl-space', null);

    //Remove shortcuts from ace in order to avoid conflict with omnidb shortcuts
    v_editor.commands.bindKey('Cmd-,', null)
    v_editor.commands.bindKey('Ctrl-,', null)
    v_editor.commands.bindKey('Cmd-Delete', null)
    v_editor.commands.bindKey('Ctrl-Delete', null)
    v_editor.commands.bindKey('Ctrl-Up', null)
    v_editor.commands.bindKey('Ctrl-Down', null)
    v_editor.setReadOnly(true);

    v_ddl_div.onclick = function() {
      v_editor.focus();
    };

    //Properties Grid
    v_properties_tab.elementDiv.innerHTML =
    "<div class='p-2 omnidb__theme-border--primary'>" +
      "<div id='div_properties_result_" + v_tab.id + "' style='width: 100%; overflow: hidden;'></div>" +
    "</div>";
    var v_divProperties = document.getElementById('div_properties_result_' + v_tab.id);
    // v_divProperties.classList.add('omnidb__theme-border--primary');
    // v_divProperties.style.overflow = 'hidden';
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
          'copy': {name: '<div style=\"position: absolute;\"><i class=\"fas fa-copy cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">Copy</div>'},
          'view_data': {name: '<div style=\"position: absolute;\"><i class=\"fas fa-edit cm-all\" style=\"vertical-align: middle;\"></i></div><div style=\"padding-left: 30px;\">View Content</div>'}
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
      divTreeTabs: document.getElementById('tree_tabs_parent_' + v_tab.id),
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
    if (p_index) {
      v_index = p_index;
    }

    changeDatabase(v_index);

    if (p_create_query_tab) {
       v_connTabControl.tag.createConsoleTab();
       v_connTabControl.tag.createQueryTab();
    }

    // Creating `Add` tab in the outer tab list
    v_connTabControl.tag.createAddTab();

    $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips

    setTimeout(function() {
      v_selectPropertiesTabFunc();
    },10);

  }

  endLoading();

}
