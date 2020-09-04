var v_createWelcomeTabFunction = function(p_index,p_create_query_tab = true, p_name = false, p_tooltip_name = false) {
  // Removing the last `add` tab
  v_connTabControl.removeLastTab();

  var v_tab = v_connTabControl.createTab({
    p_icon: '<i class="fas fa-hand-spock"></i>',
    // p_icon: '<strong>W</strong>',
    p_name: 'Welcome',
    p_selectFunction: function() {
      document.title = 'Welcome toOmniDB'
      // if(this.tag != null) {
      //   checkTabStatus(this);
      //   refreshHeights(true);
      // }
      // if(this.tag != null && this.tag.tabControl != null && this.tag.tabControl.selectedTab.tag.editor != null) {
      //     this.tag.tabControl.selectedTab.tag.editor.focus();
      // }
      $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips
    },
    p_close: false,// Replacing default close icon with contextMenu.
    p_closeFunction: function(e,p_tab) {
      var v_this_tab = p_tab;
      beforeCloseTab(e,
        function() {
          v_this_tab.removeTab();
        });
    },
    p_rightClickFunction: function(e) {
      var v_option_list = [
        {
          text: '<p class=\"mb-0 text-danger\">Close Welcome Tab</p>',
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
    p_tooltip_name: '<h5 class="my-1">Welcome to OmniDB</h5>'
  });

  v_connTabControl.selectTab(v_tab);

  var v_width = Math.ceil((300/window.innerWidth)*100);
  var v_complement_width = 100 - v_width;

  // Intro html string
  let v_html_intro =
  '<h1 class="mb-4" style="padding-left: 100px; position: relative;">' +
    '<span class="omnidb__welcome__loading"></span>' +
    '<span class="omnidb__welcome__intro-text">Hi, welcome to <span style="color:#4a6cbb;">OmniDB!</span></span>' +
  '</h1>' +
  '<div class="card p-3 omnidb__welcome__intro-card">' +
    '<p class="text-center"><span class="badge badge-danger" style="vertical-align: middle;">disclaimer</span> OmniDB is a powerful tool, and with great power...<br/>Please <strong><span class="text-danger">learn how to use it on a testing environment, NOT on production</span></strong>!</p>' +
    '<div class="alert-info p-2 rounded" style="display: grid; grid-template: \'icon text\';">' +
      '<i class="fas fa-exclamation-triangle p-4" style="grid-area: icon;"></i>' +
      '<div style="grid-area: text;">' +
        `
        Our focus is to provide a very flexible, secure and work-effective environment for multiple DBMS.<br>
        With that in mind, you should <strong>be aware the many actions on the UI can lead to a direct interaction with the database</strong> that you are connected with.</br>
        ` +
      '</div>' +
    '</div>' +
  '</div>';
  // Usel links html string
  let v_html_useful_links =
  '<div class="alert alert-success p-3 omnidb__welcome__useful-card">' +
    '<h2 class="text-center mb-4">Useful stuff</h2>' +
    '<ul>' +
      '<li class="mb-2"><a class="btn btn-success text-white" target="_blank" href="https://omnidb.org"><i class="fas fa-user"></i> <span>OmniDB website</span></a></li>' +
      '<li class="mb-2"><a class="btn btn-success text-white" target="_blank" href="https://github.com/OmniDB/OmniDB"><i class="fab fa-github"></i> <span>Github repo</span></a></li>' +
      '<li><a class="btn btn-success text-white" target="_blank" href="https://omnidb.readthedocs.io/"><i class="fas fa-list"></i> <span>Read the docs</span></a></li>' +
    '</ul>' +
  '</div>';
  // Template html string
  var v_html =
  '<div class="container" style="position: relative;">' +
    '<div class="row">' +
      '<div class="col-12">' +

        // Welcome main block
        '<div id="' + v_tab.id + '_welcome" class="omnidb__welcome" style="height: 100vh;display: flex;align-items: center;font-size: 1.2rem;justify-content: center;">' +
          // Welcome grid
          '<div style="display: grid; grid-template: \'intro links\'; grid-gap: 64px;">' +
            // Intro area
            '<div style="grid-area: intro;">' +
              v_html_intro +
            '</div>' +
            // Links area
            '<div style="grid-area: links;">' +
              v_html_useful_links +
            '</div>' +
          '</div>' +
        '</div>' +

    '</div>' +//.row

  '</div>';

  v_tab.elementDiv.innerHTML = v_html;

  var v_tag = {
    tab_id: v_tab.id,
    divWelcome: document.getElementById(v_tab.id + '_welcome'),
    selectedDatabaseIndex: 0,
    connTabControl: v_connTabControl,
    mode: 'welcome'
  };

  v_tab.tag = v_tag;

  // Creating + tab in the outer tab list
  v_connTabControl.createTab(
    {
      p_icon: '<i class="fas fa-plus"></i>',
      p_name: 'Add connection',
      p_close: false,
      p_selectable: false,
      p_clickFunction: function(e) {
        showMenuNewTabOuter(e);
      },
      p_tooltip_name: '<h5 class="my-1">Add/Select Connections</h5>'
    }
  );

  $('[data-toggle="tooltip"]').tooltip({animation:true});// Loads or Updates all tooltips

  endLoading();

}
