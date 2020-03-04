var v_createWebsiteTabFunction = function(p_name, p_site) {

  // Removing last tab of the inner tab list
  v_connTabControl.selectedTab.tag.tabControl.removeLastTab();

  // Creating console tab in the inner tab list
  var v_tab = v_connTabControl.selectedTab.tag.tabControl.createTab({
    p_name: '<i class="fas fa-globe-americas icon-tab-title"></i><span id="tab_title"> ' + p_name + '</span>',
    p_selectFunction: function() {
      if(this.tag != null) {
        refreshHeights();
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

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'website',
    iframe: document.getElementById('website_' + v_tab.id),
    tabControl: v_connTabControl.selectedTab.tag.tabControl,
    tabCloseSpan: v_tab.elementClose
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
    refreshHeights();
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
        refreshHeights();
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

  var v_tag = {
    tab_id: v_tab.id,
    mode: 'website_outer',
    iframe: document.getElementById('website_' + v_tab.id),
    tabControl: v_connTabControl
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
    console.log('OP')
    refreshHeights();
  },10);

};
