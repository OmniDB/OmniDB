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

var v_createWebsiteTabFunction = function(p_name, p_site) {

  // Removing last tab of the inner tab list
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  // Creating console tab in the inner tab list
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_name: '<i class="fas fa-globe-americas icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span>',
    p_selectFunction: function() {
      if(this.tag != null) {
        this.tag.resize();
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

  var v_html = "<iframe id='website_" + v_tab.id + "' src='" + p_site + "' style=' width: 100%; height: 200px;'></iframe>";

  var v_div = document.getElementById('div_' + v_tab.id);
  v_div.innerHTML = v_html;

  var v_resizeFunction = function () {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    if (v_tab_tag.iframe) {
      v_tab_tag.iframe.style.height = window.innerHeight - $(v_tab_tag.iframe).offset().top - (0.833)*v_font_size + "px";
    }
  }

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'website',
    iframe: document.getElementById('website_' + v_tab.id),
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    tabCloseSpan: v_tab.elementClose,
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

var v_createWebsiteOuterTabFunction = function(p_name, p_site, p_html, p_close_function) {

  // Removing last tab of the outer tab list
  v_connTabControl.removeLastTab();

  // Creating console tab in the inner tab list
  var v_tab = v_connTabControl.createTab({
    p_name: '<i class="fas fa-globe-americas icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span>',
    p_selectFunction: function() {
      if(this.tag != null) {
        this.tag.resize();
      }
    },
    p_closeFunction: function(e,p_tab) {
      var v_current_tab = p_tab;
      beforeCloseTab(e,
        function() {
          if (p_close_function!=null) {
            p_close_function();
          }
          removeTab(v_current_tab);
        });
    },
    p_dblClickFunction: renameTab
  });

  // Selecting newly created tab
  v_connTabControl.selectTab(v_tab);

  var v_html = '';

  if (p_html==null) {
    v_html = "<iframe id='website_" + v_tab.id + "' src='" + p_site + "' style=' width: 100%; height: 200px;'></iframe>";
  }
  else {
    v_html = "<div id='website_" + v_tab.id + "' style=' width: 100%; height: 200px;'>" + p_html + "</div>";
  }

  var v_div = document.getElementById('div_' + v_tab.id);
  v_div.innerHTML = v_html;

  var v_resizeFunction = function () {
    var v_tab_tag = v_connTabControl.selectedTab.tag.tabControl.selectedTab.tag;
    if (v_tab_tag.iframe) {
      v_tab_tag.iframe.style.height = window.innerHeight - $(v_tab_tag.iframe).offset().top - (0.833)*v_font_size + "px";
    }
  }

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'website_outer',
    iframe: document.getElementById('website_' + v_tab.id),
    tabControl: v_connTabControl,
    resize: v_resizeFunction
  };

  v_tab.tag = v_tag;

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
    v_resizeFunction();
  },10);

};
