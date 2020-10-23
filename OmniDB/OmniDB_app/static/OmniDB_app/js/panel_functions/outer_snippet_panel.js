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

var toggleSnippetPanel = function(p_set_state = false) {
  v_element = $('#' + v_connTabControl.snippet_tag.divPanel.getAttribute('id'));
  var v_snippet_tag = v_connTabControl.snippet_tag;

  let v_set_state = p_set_state;
  if (v_set_state === 'visible') {
    v_element.addClass('omnidb__panel--slide-in');
  }
  else if (v_set_state === 'hidden') {
    v_element.removeClass('omnidb__panel--slide-in');
  }
  else {
    v_element.toggleClass('omnidb__panel--slide-in');
  }

  resizeSnippetPanel();
}

var v_createSnippetPanelFunction = function(p_index) {

  // v_connTabControl.removeLastTab();

  var v_tab = v_connTabControl.createTab({
    p_icon: `<i class="fas fa-book"></i>`,
    p_name: `Snippets`,
    p_close: false,
    p_selectable: false,
    p_clickFunction: function() {
      toggleSnippetPanel();
    },
    p_omnidb_tooltip_name: '<h5 class="my-1">Snippets Panel</h5>'
  });

  v_connTabControl.selectTab(v_tab);

  var v_html =
  "<div id='" + v_tab.id + "_panel_snippet' class='omnidb__panel omnidb__panel--snippet'>" +

    "<button type='button' onclick='toggleSnippetPanel()' class='px-4 btn omnidb__theme__btn--secondary omnidb__panel__toggler'><i class='fas fa-arrows-alt-v'></i></button>" +

    "<div class='container-fluid' style='position: relative;'>" +
      "<div id='" + v_tab.id + "_snippet_div_layout_grid' class='row'>" +
        "<div id='" + v_tab.id + "_snippet_div_left' class='omnidb__workspace__div-left col' style='flex: 0 0 16.667%'>" +
          "<div class='row'>" +
            "<div class='omnidb__workspace__content-left'>" +
              "<div id='" + v_tab.id + "_snippet_tree' style='overflow: auto; flex-grow: 1; transition: scroll 0.3s;'></div>" +
            "</div>" +
          "</div>" +
          "<div class='resize_line_vertical omnidb__resize-line__container' onmousedown='resizeSnippetHorizontal(event)' style='position:absolute;height: 100%;width: 10px;cursor: ew-resize;border-right: 1px dashed #acc4e8;top: 0px;right: 0px;'></div>" +
        "</div>" +//.div_left
        "<div id='" + v_tab.id + "_snippet_div_right' class='omnidb__workspace__div-right col pt-0' style='position: relative;'>" +
          // "<div class='row'>" +
            "<div id='" + v_tab.id + "_snippet_tabs' class='w-100'></div>" +
          // "</div>" +
        "</div>" +//.div_right
      "</div>" +//.row

    "</div>" +//.container-fluid

  "</div>";

  v_connTabControl.snippet_div = document.createElement('div');
  v_connTabControl.snippet_div.id = v_tab.id + '_snippet';
  v_connTabControl.snippet_div.innerHTML = v_html;
  document.getElementById(v_connTabControl.id).append(v_connTabControl.snippet_div);

  var v_currTabControl = createTabControl({
    p_div: v_tab.id + '_snippet_tabs',
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
    divLayoutGrid: document.getElementById(v_tab.id + '_snippet_div_layout_grid'),
    divLeft: document.getElementById(v_tab.id + '_snippet_div_left'),
    divPanel: document.getElementById(v_tab.id + '_panel_snippet'),
    divRight: document.getElementById(v_tab.id + '_snippet_div_right'),
    divTree: document.getElementById(v_tab.id + '_snippet_tree'),
    connTabControl: v_connTabControl,
    isVisible: false,
    mode: 'snippets'
  };

  v_tab.tag = v_tag;

  v_connTabControl.snippet_tag = v_tag;

  getTreeSnippets(v_tag.divTree.id);

  if (v_connTabControl.snippet_tag.tabControl.tabList.length > 0) {
    v_connTabControl.snippet_tag.tabControl.selectTab(v_connTabControl.snippet_tag.tabControl.tabList[0]);
  }
  v_connTabControl.tag.createSnippetTextTab();
  v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.setValue('');
  v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.clearSelection();
  v_connTabControl.snippet_tag.tabControl.selectedTab.tag.editor.gotoLine(0, 0, true);

  // Creating `Add` tab in the outer tab list
  // v_connTabControl.createAddTab();
  // v_connTabControl.createTab('+',false,v_connTabControl.tag.createConnTab,false);

  //setTimeout(function() {
  //  refreshTreeHeight();
  //},10);

}
