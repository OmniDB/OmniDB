var v_createSnippetTabFunction = function(p_index) {

  v_connTabControl.removeLastTab();

  var v_tab = v_connTabControl.createTab({
    p_icon: `<i class="fas fa-align-left icon-tab-title"></i>`,
    p_name: `Snippets`,
    p_close: false,
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
  });

  console.log(v_tab);

  v_connTabControl.selectTab(v_tab);

  var v_width = Math.ceil((300/window.innerWidth)*100);
  var v_complement_width = 100 - v_width;

  var v_html =
  "<div class='container-fluid' style='position: relative;'>" +
    "<div class='row'>" +
      "<div id='" + v_tab.id + "_div_left' class='omnidb__workspace__div-left col-md-2'>" +
        "<div class='row'>" +

          // "<div onmousedown='resizeHorizontal(event)' style='width: 10px; height: 100%; cursor: ew-resize; position: absolute; top: 0px; right: 0px;'><div class='resize_line_vertical' style='width: 5px; height: 100%; border-right: 1px dotted #c3c3c3;'></div><div style='width:5px;'></div></div>" +


          "<div class='omnidb__workspace__content-left'>" +
            "<div id='" + v_tab.id + "_details' class='omnidb__workspace__connection-details' ></div>" +
            "<div id='" + v_tab.id + "_tree' style='overflow: auto; flex-grow: 1;'></div>" +
            "<div id='" + v_tab.id + "_left_resize_line_horizontal' onmousedown='resizeTreeVertical(event)' style='width: 100%; height: 10px; cursor: ns-resize;'><div class='resize_line_horizontal' style='height: 5px; border-bottom: 1px dotted #c3c3c3;'></div><div style='height:5px;'></div></div>" +
            "<div id='tree_tabs_parent_" + v_tab.id + "' class='omnidb__tree-tabs' style='position: relative;flex-shrink: 0;flex-basis: 40vh;'>" +
              "<div id='" + v_tab.id + "_loading' class='div_loading' style='z-index: 1000;'>" +

              '<div class="div_loading_cover"></div>' +
              '<div class="div_loading_content">' +
              '  <div class="spinner-border text-primary" style="width: 4rem; height: 4rem;" role="status">' +
              '    <span class="sr-only ">Loading...</span>' +
              '  </div>' +
              '</div>' +
              "</div>" +
              "<button type='button' onclick='toggleTreeTabsContainer(" + '"tree_tabs_parent_' + v_tab.id + '","' + v_tab.id + '_left_resize_line_horizontal"' + ")' class='btn btn-secondary omnidb__tree-tabs__toggler'><i class='fas fa-arrows-alt-v'></i></button>" +
              "<div id='tree_tabs_" + v_tab.id + "' class='omnidb__tree-tabs__container' style='position: relative;'></div>" +
            "</div>" +
          "</div>" +
        "</div>" +
      "</div>" +//.div_left
      "<div id='" + v_tab.id + "_div_right' class='omnidb__workspace__div-right col-md-10' style='position: relative;'>" +
        // "<div class='row'>" +
          "<div id='" + v_tab.id + "_tabs' class='w-100'></div>" +
        // "</div>" +
      "</div>" +//.div_right
    "</div>" +//.row

    "<div id='" + v_tab.id + "_workspace_resize_grid' class='omnidb__workspace-resize-grid'>" +
      "<div class='container-fluid h-100'>" +
        "<div class='row h-100'>" +

          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +

          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'>" +
            "<div id='"+ v_tab.id + "_workspace_resize_draggable' ondragstart='dragStart(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragend='dragEnd(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' draggable='true' class='omnidb__workspace-resize-grid__draggable' style='width: 30px; height: 100%; cursor: ew-resize;'>" +
              "<div class='resize_line_vertical'><span>&#8633;</span></div>" +
            "</div>" +
          "</div></div>" +

          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +
          "<div class='col-1 d-flex' style='position: relative;'><div class='omnidb__workspace-resize-grid__column h-100 ml-auto' ondragenter='dragEnter(event)' ondragleave='dragLeave(event)' ondrop='drop(event, " + v_tab.id + "_workspace_resize_grid, " + v_tab.id + "_div_left, " + v_tab.id + "_div_right)' ondragover='allowDrop(event)'></div></div>" +

        "</div>" +
      "</div>" +
    "</div>" +

  "</div>";

  v_tab.elementDiv.innerHTML = v_html;


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

  var v_tag = {
    tab_id: v_tab.id,
    tabControl: v_currTabControl,
    tabTitle: 'teste',
    divTree: document.getElementById(v_tab.id + '_tree'),
    divLeft: document.getElementById(v_tab.id + '_div_left'),
    divRight: document.getElementById(v_tab.id + '_div_right'),
    connTabControl: v_connTabControl,
    mode: 'snippets'
  };

  v_tab.tag = v_tag;

  getTreeSnippets(v_tag.divTree.id);

  v_connTabControl.tag.createSnippetTextTab('Welcome');
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.setValue('Welcome to OmniDB!');
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.clearSelection();
  v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);

  v_connTabControl.createTab('+',false,v_connTabControl.tag.createConnTab,false);

  setTimeout(function() {
    refreshTreeHeight();
  },10);

}
