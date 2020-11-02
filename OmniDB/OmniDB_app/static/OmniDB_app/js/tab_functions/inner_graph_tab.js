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

var v_createGraphTabFunction = function(p_name) {

  var v_name = 'Graph';
  if (p_name)
    v_name = p_name;

  // Removing last tab of the inner tab list
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_icon: `<i class="fab fa-hubspot icon-tab-title"></i>`,
    p_name: '<span id="tab_title">' + v_name + '</span><span id="tab_loading" style="visibility:hidden;"><i class="tab-icon node-spin"></i></span><i title="" id="tab_check" style="display: none;" class="fas fa-check-circle tab-icon icon-check"></i>',
    p_selectFunction: function() {
      document.title = 'OmniDB'
      if(this.tag != null) {
        this.tag.resize();
      }
    },
    p_closeFunction: function(e,p_tab) {
      var v_current_tab = p_tab;
      beforeCloseTab(e,
        function() {
          if (v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.network) {
            v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag.network.destroy();
          }
          removeTab(v_current_tab);
        });
    },
    p_dblClickFunction: renameTab
  });

  v_connTabControl.selectedTab.tag.tabControl.selectTab(v_tab);

  // Adding unique names to spans
  var v_tab_title_span = document.getElementById('tab_title');
  v_tab_title_span.id = 'tab_title_' + v_tab.id;
  var v_tab_loading_span = document.getElementById('tab_loading');
  v_tab_loading_span.id = 'tab_loading_' + v_tab.id;
  var v_tab_check_span = document.getElementById('tab_check');
  v_tab_check_span.id = 'tab_check_' + v_tab.id;

  var v_html =
  "<div class='omnidb__theme-border--primary'>" +
    "<div id='graph_" + v_tab.id + "' style=' width: 100%; height: 200px;'></div>" +
  "</div>";

  // var v_div = document.getElementById('div_' + v_tab.id);
  // v_div.innerHTML = v_html;
  v_tab.elementDiv.innerHTML = v_html;

  var v_resizeFunction = function () {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    if (v_tab_tag.graph_div) {
      v_tab_tag.graph_div.style.height = window.innerHeight - $(v_tab_tag.graph_div).offset().top - (0.833)*v_font_size + "px";
    }
  }

  var v_tag = {
    tab_id: v_tab.id,
    divTree: document.getElementById(v_tab.id + '_tree'),
    divLeft: document.getElementById(v_tab.id + '_div_left'),
    divRight: document.getElementById(v_tab.id + '_div_right'),
    graph_div: document.getElementById('graph_' + v_tab.id),
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    network: null,
    mode: 'graph',
    resize: v_resizeFunction
  };

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
    v_resizeFunction();
  },10);

};
